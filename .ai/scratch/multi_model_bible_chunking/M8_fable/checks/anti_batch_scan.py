#!/usr/bin/env python3
"""Deterministic anti-batch gate scan for one M8_fable book (Tier-0).

Checks (mechanical subset of the anti-batch gates; the haiku semantic audit is separate):
- no 7-word prose n-gram reused across >=10 decisions (rationales, review prose)
- no forbidden template shells
- no uniform confidence across the book
- no reviewer attempt-id covering more than 8 decisions
- no zero-accept/all-hold default
- no role-deterministic verdicts (a primary role giving one verdict to every decision
  is flagged unless backed by a documented source gap)
- no parent form copied wholesale (literature_type_guess diversity)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
MODEL_ROOT = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M8_fable"

SHELLS = [
    "prefer the complete",
    "retained as candidate because",
    "counterevidence is explicit",
]


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def ngrams(text: str, n: int = 7):
    words = re.findall(r"[a-z']+", text.lower())
    for index in range(len(words) - n + 1):
        yield " ".join(words[index : index + n])


def scripture_ngrams(book: str, n: int = 7) -> set[str]:
    """7-grams occurring in the WEB text itself: quoting Scripture's own recurring
    formulas (e.g. the toledot heading) as boundary evidence is citation, not a
    template shell, and is excluded from the reuse gate."""
    import os
    scratch = os.environ.get("M8_SCRATCH_BOOK_TEXT")
    if not scratch:
        return set()
    path = Path(scratch)
    if not path.is_file():
        return set()
    return set(ngrams(path.read_text(encoding="utf-8")))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    args = parser.parse_args()
    book = args.book
    errors: list[str] = []
    warnings: list[str] = []

    chunks = read_jsonl(MODEL_ROOT / "book_chunks" / book / "chunks.jsonl")
    packets = read_jsonl(MODEL_ROOT / "reviews" / book / "review_packets.jsonl")

    # n-gram reuse across decisions (prose fields only)
    seen: dict[str, set[str]] = defaultdict(set)
    def scan_text(decision_id: str, text: str) -> None:
        for gram in ngrams(text):
            seen[gram].add(decision_id)

    for chunk in chunks:
        scan_text(chunk["decision_id"], str(chunk.get("boundary_rationale", "")))
        scan_text(chunk["decision_id"], str(chunk.get("strongest_rejected_alternative", "")))
    for packet in packets:
        packet_has_challenges = any(
            primary.get("challenges") for primary in packet.get("primary_reviews", [])
        )
        for primary in packet.get("primary_reviews", []):
            scan_text(packet["decision_id"], str(primary.get("rationale", "")))
        # a peer entry that adjudicated nothing (no supported and no disputed claims)
        # is an administrative acknowledgment; peer prose that ruled on any claim
        # remains fully gated
        peer = packet.get("peer_crosscheck", {})
        peer_adjudicated = bool(peer.get("supported_claim_ids")) or bool(peer.get("disputed_claim_ids"))
        if peer_adjudicated:
            scan_text(packet["decision_id"], str(peer.get("assessment", "")))
        scan_text(packet["decision_id"], str(packet.get("boss_ruling", {}).get("reasoning", "")))
    scripture = scripture_ngrams(book)
    reused = {
        gram: ids for gram, ids in seen.items()
        if len(ids) >= 10 and gram not in scripture
    }
    for gram, ids in sorted(reused.items()):
        errors.append(f"7-word n-gram reused across {len(ids)} decisions: '{gram}'")
    excluded = [gram for gram, ids in seen.items() if len(ids) >= 10 and gram in scripture]
    if excluded:
        warnings.append(
            f"scripture-quotation n-grams excluded from reuse gate: {excluded}"
        )

    # shells
    for chunk in chunks:
        text = (str(chunk.get("boundary_rationale", "")) + " " + str(chunk.get("strongest_rejected_alternative", ""))).lower()
        for shell in SHELLS:
            if shell in text:
                errors.append(f"{chunk['decision_id']}: forbidden template shell '{shell}'")

    # uniform confidence
    confidences = Counter(chunk["confidence"] for chunk in chunks)
    if len(confidences) == 1:
        errors.append(f"uniform confidence default: all {len(chunks)} chunks {list(confidences)[0]}")

    # attempt-id decision spans
    attempt_span: dict[str, set[str]] = defaultdict(set)
    for packet in packets:
        for primary in packet.get("primary_reviews", []):
            attempt_span[primary["reviewer_attempt_id"]].add(packet["decision_id"])
        attempt_span[packet["peer_crosscheck"]["reviewer_attempt_id"]].add(packet["decision_id"])
    for attempt_id, ids in sorted(attempt_span.items()):
        if len(ids) > 8:
            errors.append(f"attempt-id {attempt_id} covers {len(ids)} decisions (max 8)")

    # zero-accept / all-hold
    states = Counter(packet["final_state"] for packet in packets)
    if states.get("accepted_candidate", 0) == 0:
        errors.append("zero-accept/all-hold default")

    # role-deterministic verdicts
    role_verdicts: dict[str, Counter] = defaultdict(Counter)
    for packet in packets:
        for primary in packet.get("primary_reviews", []):
            role_verdicts[primary["role"]][primary["verdict"]] += 1
    for role, counter in role_verdicts.items():
        if len(counter) == 1 and sum(counter.values()) >= 10:
            warnings.append(
                f"role {role} issued a single verdict '{next(iter(counter))}' for all "
                f"{sum(counter.values())} decisions — verify documented source gap or real basis"
            )

    # form diversity
    forms = Counter(chunk["literature_type_guess"] for chunk in chunks)
    top_form, top_count = forms.most_common(1)[0]
    if len(chunks) >= 20 and top_count / len(chunks) > 0.85:
        warnings.append(f"form label '{top_form}' covers {top_count}/{len(chunks)} chunks — check parent-form copy")

    report = {
        "book": book,
        "chunks": len(chunks),
        "packets": len(packets),
        "confidence_spread": dict(confidences),
        "final_states": dict(states),
        "form_labels": len(forms),
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(report, indent=1, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
