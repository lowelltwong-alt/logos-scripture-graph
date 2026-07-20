"""Deterministic adaptive review questions with an optional typed interpreter."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Protocol


class LanguageInterpreter(Protocol):
    """May interpret an answer, but may not select truth or promote text."""
    def interpret(self, question: dict[str, Any], answer: str, allowed_intents: list[str]) -> dict[str, Any]: ...


@dataclass(frozen=True)
class ParsedAnswer:
    intent: str
    value: str | None = None
    confidence_state: str = "low"
    source: str = "deterministic"


def _parse(answer: str, labels: list[str]) -> ParsedAnswer:
    text, low = " ".join(answer.strip().split()), " ".join(answer.lower().strip().split())
    if not text:
        return ParsedAnswer("unclear")
    if any(x in low for x in ("cannot read", "can't read", "unreadable", "illegible")):
        return ParsedAnswer("cannot_read", confidence_state="high")
    if any(x in low for x in ("blank page", "no text", "nothing to read", "image only")):
        return ParsedAnswer("no_text_by_design", confidence_state="high")
    if any(x in low for x in ("more context", "not sure", "unsure", "don't know")):
        return ParsedAnswer("request_context", confidence_state="high")
    for label in labels:
        simple = label.lower().replace("candidate ", "")
        if low in {label.lower(), simple, f"{label.lower()} is right", f"{simple} is right"}:
            return ParsedAnswer("choose_candidate", label, "high")
    match = re.search(r"(?:text is|it says|it reads|should (?:say|read|be))\s*[:\-]?\s*(.+)$", text, re.I)
    if match:
        return ParsedAnswer("supply_text", match.group(1).strip(" \"'"), "medium")
    if low in {"yes", "correct", "readable", "that's right", "that is right"}:
        return ParsedAnswer("confirm", confidence_state="medium")
    if low in {"no", "wrong", "not right"}:
        return ParsedAnswer("reject", confidence_state="medium")
    return ParsedAnswer("unclear")


class ConversationReviewer:
    def __init__(self, interpreter: LanguageInterpreter | None = None):
        self.interpreter = interpreter

    def start(self, item: dict[str, Any]) -> dict[str, Any]:
        return {"schema": "portable_ocr_review_session.v1", "review_item_id": item["review_item_id"],
                "state": "ask_readability", "candidate_labels": [c["blind_label"] for c in item.get("candidates", [])],
                "events": [], "decision": None,
                "question": {"question_id": "readability", "plain_language": "Can you clearly read the highlighted text?",
                             "examples": ["Readable", "Unreadable", "I need more context"]}}

    def answer(self, session: dict[str, Any], answer: str) -> dict[str, Any]:
        parsed = _parse(answer, session.get("candidate_labels", []))
        if parsed.intent == "unclear" and self.interpreter:
            result = self.interpreter.interpret(session["question"], answer,
                ["choose_candidate", "supply_text", "cannot_read", "no_text_by_design", "request_context", "unclear"])
            if result.get("confidence_state") in {"medium", "high"}:
                parsed = ParsedAnswer(str(result.get("intent", "unclear")), result.get("value"),
                                      str(result["confidence_state"]), "language_adapter")
        session = {**session, "events": list(session.get("events", []))}
        session["events"].append({"sequence": len(session["events"]) + 1, "question_state": session["state"],
                                  "question_id": session["question"]["question_id"], "answer": answer,
                                  "interpreted_intent": parsed.intent, "interpreted_value": parsed.value,
                                  "interpretation_source": parsed.source, "confidence_state": parsed.confidence_state})
        if session["state"] == "confirm_interpretation":
            if parsed.intent == "confirm":
                pending = session["pending_interpretation"]
                disposition = pending["value"] if pending["intent"] == "disposition" else (
                    "selected_engine_candidate" if pending["intent"] == "choose_candidate" else "verified_with_corrections")
                value = None if pending["intent"] == "disposition" else pending["value"]
                return self._finish(session, disposition, value)
            if parsed.intent == "reject":
                session.pop("pending_interpretation", None)
                return self._ask(session, "ask_reading", "reading_retry",
                                 "Please name the right candidate or type the exact text you see.")
            return self._ask(session, "confirm_interpretation", "confirm_clarify",
                             "Please answer yes or no: did I understand you correctly?")
        if parsed.intent == "request_context":
            return self._ask(session, "ask_reading", "context_ready",
                             "Look at the nearby lines. What does the highlighted text say, or is it still unreadable?")
        if parsed.intent == "cannot_read":
            return self._confirm(session, "disposition", "needs_second_review")
        if parsed.intent == "no_text_by_design":
            return self._confirm(session, "disposition", "no_extractable_text_by_design")
        if parsed.intent in {"choose_candidate", "supply_text"}:
            return self._confirm(session, parsed.intent, parsed.value)
        if session["state"] == "ask_readability" and parsed.intent == "confirm":
            return self._ask(session, "ask_reading", "reading", "Which candidate matches, or what is the exact text?")
        return self._ask(session, session["state"], "clarify",
                         "I did not understand. Say readable, name a candidate, type the exact text, or say unreadable.")

    @staticmethod
    def _ask(session: dict[str, Any], state: str, qid: str, text: str) -> dict[str, Any]:
        session["state"], session["question"] = state, {"question_id": qid, "plain_language": text, "examples": []}
        return session

    @staticmethod
    def _confirm(session: dict[str, Any], intent: str, value: str | None) -> dict[str, Any]:
        session["state"] = "confirm_interpretation"
        session["pending_interpretation"] = {"intent": intent, "value": value}
        session["question"] = {"question_id": "confirm_interpretation",
            "plain_language": f"I understood your answer as: {value}. Is that correct?", "examples": ["Yes", "No"]}
        return session

    @staticmethod
    def _finish(session: dict[str, Any], disposition: str, value: str | None) -> dict[str, Any]:
        session["state"] = "complete"
        session["decision"] = {"disposition": disposition, "value": value, "human_confirmed": True,
                               "automatic_promotion_performed": False}
        session["question"] = {"question_id": "complete", "plain_language": "Recorded; no text was promoted.", "examples": []}
        return session
