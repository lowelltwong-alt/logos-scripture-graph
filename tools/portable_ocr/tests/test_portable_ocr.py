from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from portable_ocr.comparison import compare_candidates, compare_text
from portable_ocr.conversation import ConversationReviewer
from portable_ocr.handoff import build_handoff
from portable_ocr.pipeline import run_pipeline
from portable_ocr.review import build_review
from portable_ocr.routing import route_third_engine


class FakeEngine:
    def __init__(self, engine_id: str, text: str, fail: bool = False):
        self.engine_id, self.text, self.fail = engine_id, text, fail
        self.diversity_signature = (f"family-{engine_id}", f"model-{engine_id}", f"runtime-{engine_id}", f"exe-{engine_id}")
    def recognize(self, source: Path):
        if self.fail:
            raise RuntimeError("synthetic failure")
        return {"text": self.text, "raw_confidence": None, "confidence_is_calibrated": False}


class MutatingEngine(FakeEngine):
    def recognize(self, source: Path):
        value = super().recognize(source)
        source.write_bytes(b"mutation")
        return value


class PortableOcrTests(unittest.TestCase):
    def test_canonical_unicode_forms_agree(self):
        self.assertEqual(0, compare_text("λόγος", "λόγος")["delta_count"])

    def test_greek_diacritic_disagreement_routes_c(self):
        comparison = compare_candidates([{"candidate_id": "a", "text": "λογος"},
                                         {"candidate_id": "b", "text": "λόγος"}])
        self.assertIn("diacritic_disagreement", comparison["pairwise"][0]["flags"])
        self.assertTrue(route_third_engine(comparison, {"third_engine_mode": "on_critical_or_threshold"})["run_third_engine"])

    def test_hebrew_niqqud_disagreement_is_visible(self):
        result = compare_text("שלום", "שָׁלוֹם")
        self.assertIn("diacritic_disagreement", result["flags"])
        self.assertEqual(["Hebrew"], result["scripts"]["left"])

    def test_greek_and_hebrew_punctuation_is_visible(self):
        self.assertIn("punctuation_disagreement", compare_text("λόγος", "λόγος·")["flags"])
        self.assertIn("punctuation_disagreement", compare_text("שלום", "שלום׃")["flags"])
        self.assertIn("punctuation_disagreement", compare_text("שלום", "שלום׳")["flags"])
        self.assertIn("punctuation_disagreement", compare_text("שלום", "שלום״")["flags"])

    def test_relocated_greek_and_hebrew_marks_route_c_even_in_long_context(self):
        greek = compare_candidates([
            {"candidate_id": "a", "text": "x " * 300 + "άα"},
            {"candidate_id": "b", "text": "x " * 300 + "αά"},
        ])
        self.assertIn("diacritic_disagreement", greek["pairwise"][0]["flags"])
        self.assertTrue(route_third_engine(greek, {"third_engine_mode": "on_critical_or_threshold"})["run_third_engine"])
        hebrew = compare_text("אְב", "אבְ")
        self.assertIn("diacritic_disagreement", hebrew["flags"])

    def test_pipeline_runs_required_c_without_selecting_winner(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / "page.svg"; source.write_text("<svg/>", encoding="utf-8")
            run_dir = run_pipeline(source, root / "runs", [FakeEngine("a", "λογος"), FakeEngine("b", "λόγος"),
                               FakeEngine("c", "λόγος")], {"third_engine_mode": "on_critical_or_threshold"})
            run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(3, len(run["candidates"]))
            self.assertIsNone(run["winner"])
            self.assertFalse(run["promoted"])

    def test_required_c_unavailable_fails_closed_and_atomic(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / "page.png"; source.write_bytes(b"image")
            with self.assertRaises(Exception):
                run_pipeline(source, root / "runs", [FakeEngine("a", "א"), FakeEngine("b", "ב")],
                             {"third_engine_mode": "on_disagreement"})
            self.assertEqual([], list((root / "runs").iterdir()))

    def test_source_mutation_fails_and_original_is_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / "page.png"; source.write_bytes(b"original")
            with self.assertRaises(Exception):
                run_pipeline(source, root / "runs", [MutatingEngine("a", "x"), FakeEngine("b", "y")],
                             {"third_engine_mode": "disabled"})
            self.assertEqual(b"original", source.read_bytes())
            self.assertEqual([], list((root / "runs").iterdir()))

    def test_conversation_drills_down_and_requires_confirmation(self):
        reviewer = ConversationReviewer()
        session = reviewer.start({"review_item_id": "x", "candidates": [{"blind_label": "Candidate A"}]})
        session = reviewer.answer(session, "I am not sure")
        self.assertEqual("context_ready", session["question"]["question_id"])
        session = reviewer.answer(session, "Candidate A")
        self.assertEqual("confirm_interpretation", session["state"])
        session = reviewer.answer(session, "yes")
        self.assertEqual("complete", session["state"])
        self.assertFalse(session["decision"]["automatic_promotion_performed"])

    def test_offline_review_has_no_network_or_persistence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / "page.svg"; source.write_text("<svg/>", encoding="utf-8")
            run_dir = run_pipeline(source, root / "runs", [FakeEngine("a", "λόγος"), FakeEngine("b", "λόγος")],
                                   {"third_engine_mode": "disabled"})
            text = build_review(run_dir, root / "review.html", confidential_mode=True).read_text(encoding="utf-8")
            self.assertIn("Answer in your own words", text)
            self.assertNotIn("fetch(", text)
            self.assertNotIn("localStorage", text)

    def test_replay_bound_handoff_remains_unpromoted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / "page.png"; source.write_bytes(b"image")
            run_dir = run_pipeline(source, root / "runs", [FakeEngine("a", "λόγος"), FakeEngine("b", "λογος")],
                                   {"third_engine_mode": "disabled"})
            run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            review = {"schema": "portable_ocr_review_session.v1", "run_id": run["run_id"], "state": "complete",
                "source_sha256": run["source"]["sha256"], "reviewer_attestation": True,
                "candidate_hashes": [{"candidate_id": c["candidate_id"], "text_sha256": c["text_sha256"]} for c in run["candidates"]],
                "events": [{"sequence": 1, "question_state": "ask_reading", "interpreted_intent": "choose_candidate", "interpreted_value": "Candidate A"},
                           {"sequence": 2, "question_state": "confirm_interpretation", "interpreted_intent": "confirm"}],
                "decision": {"disposition": "selected_engine_candidate", "value": "Candidate A", "human_confirmed": True,
                             "automatic_promotion_performed": False}}
            review_path = root / "review.json"; review_path.write_text(json.dumps(review), encoding="utf-8")
            handoff = json.loads(build_handoff(run_dir, review_path, root / "handoff.json").read_text(encoding="utf-8"))
            self.assertEqual("λόγος", handoff["reviewed_text"])
            self.assertTrue(handoff["host_promotion_required"])

    def test_review_and_handoff_reject_post_run_source_or_candidate_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / "page.png"; source.write_bytes(b"image")
            run_dir = run_pipeline(source, root / "runs", [FakeEngine("a", "alpha"), FakeEngine("b", "beta")],
                                   {"third_engine_mode": "disabled"})
            snapshot = next(run_dir.glob("source.*"))
            snapshot.write_bytes(b"tampered")
            with self.assertRaisesRegex(Exception, "source snapshot hash mismatch"):
                build_review(run_dir, root / "review.html")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / "page.png"; source.write_bytes(b"image")
            run_dir = run_pipeline(source, root / "runs", [FakeEngine("a", "alpha"), FakeEngine("b", "beta")],
                                   {"third_engine_mode": "disabled"})
            run_path = run_dir / "run.json"
            run = json.loads(run_path.read_text(encoding="utf-8"))
            run["candidates"][0]["text"] = "TAMPERED TEXT"
            run_path.write_text(json.dumps(run), encoding="utf-8")
            review = {"schema": "portable_ocr_review_session.v1", "run_id": run["run_id"], "state": "complete",
                "source_sha256": run["source"]["sha256"], "reviewer_attestation": True,
                "candidate_hashes": [{"candidate_id": c["candidate_id"], "text_sha256": c["text_sha256"]} for c in run["candidates"]],
                "events": [{"sequence": 1, "question_state": "ask_reading", "interpreted_intent": "choose_candidate", "interpreted_value": "Candidate A"},
                           {"sequence": 2, "question_state": "confirm_interpretation", "interpreted_intent": "confirm"}],
                "decision": {"disposition": "selected_engine_candidate", "value": "Candidate A", "human_confirmed": True,
                             "automatic_promotion_performed": False}}
            review_path = root / "review.json"; review_path.write_text(json.dumps(review), encoding="utf-8")
            with self.assertRaisesRegex(Exception, "candidate text hash mismatch"):
                build_handoff(run_dir, review_path, root / "handoff.json")


if __name__ == "__main__":
    unittest.main()
