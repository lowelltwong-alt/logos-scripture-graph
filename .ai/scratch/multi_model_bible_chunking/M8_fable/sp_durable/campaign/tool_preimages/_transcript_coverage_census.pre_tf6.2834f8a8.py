#!/usr/bin/env python3
"""OW-10: report transcript coverage from an EXPLICIT PER-BOOK CENSUS, never from prose.

WHY THIS EXISTS. The breach report said the transcript-reading discovery method "existed for about one attempt in
eight in Lamentations and for none of the earlier books", while its own findings cited five Jeremiah attempts read
from transcripts. Jeremiah IS an earlier book. A prose summary drifted from the evidence underneath it; the owner
ordered the claim replaced by a census.

THE CENSUS COUNTS THREE DIFFERENT THINGS AND NEVER ADDS THEM TOGETHER, because they answer different questions:

  attempts            - the denominator: distinct attempt_ids in the book's receipts.
  transcript_retained - a transcript for that attempt exists with bytes > 0 somewhere we can still read.
                        A mapped entry of zero bytes is NOT retention; it is a name with nothing behind it.
  observed            - a stage-1 transcript auditor actually READ it and wrote per-transcript findings.
                        This is the only number that supports a claim about discovered breaches.

`observed` is normally <= `transcript_retained`, but NOT in this campaign's history: Jeremiah attempts were
observed although Jeremiah never had a book-level manifest, because those transcripts sat in the same session store
as Lamentations' and fell into the auditors' slices. The census reports what happened, not what should have.

This tool READS ONLY. It does not launch an audit and OW-10 forbids using it as a reason to.
"""
import collections
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SP = HERE.parent
OUT = HERE / "transcript_coverage_census.v1.json"

KNOWN = {"jer": "Jer", "lam": "Lam", "isa": "Isa", "ps": "Ps", "job": "Job", "prov": "Prov",
         "eccl": "Eccl", "song": "Song", "ezek": "Ezek", "campaign": "campaign"}


def sha(p):
    try:
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    except Exception:
        return None


def normalise_book(raw, attempt_id):
    """An auditor wrote free prose into its `book` field, e.g. "Jer (Jeremiah corpus-wide-order wave, NOT a
    Lamentations attempt)". The attempt_id prefix is the stable key; the prose is kept as evidence elsewhere but is
    never used as an identity."""
    aid = (attempt_id or "").strip()
    pref = aid.split("_")[0].lower() if aid else ""
    if pref in KNOWN:
        return KNOWN[pref]
    r = (raw or "").strip().lower()
    for k, v in KNOWN.items():
        if r.startswith(k):
            return v
    return "UNIDENTIFIED"


def build():
    # ---- denominator: distinct attempt_ids per book, from the receipts themselves ----
    attempts = collections.defaultdict(set)
    receipt_files = []
    for rp in sorted(SP.rglob("*_attempt_receipts.jsonl")):
        receipt_files.append({"path": str(rp.relative_to(SP)).replace("\\", "/"), "sha256": sha(rp)})
        book_dir = rp.relative_to(SP).parts[0]
        for line in rp.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            aid = json.loads(line).get("attempt_id")
            if aid:
                attempts[book_dir].add(aid)

    # ---- retention: a transcript with real bytes, from every manifest we have ----
    retained = collections.defaultdict(set)
    zero_byte = collections.defaultdict(set)
    manifests = []
    for mp in sorted(SP.rglob("transcript_manifest.v*.json")):
        try:
            m = json.loads(mp.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        manifests.append({"path": str(mp.relative_to(SP)).replace("\\", "/"), "sha256": sha(mp),
                          "declares_book": m.get("book"), "mapped": m.get("mapped_count")})
        for e in m.get("mapped_transcripts", []):
            b = normalise_book(e.get("book"), e.get("attempt_id"))
            (retained if (e.get("bytes") or 0) > 0 else zero_byte)[b].add(e.get("attempt_id"))

    # ---- observation: what a stage-1 auditor actually read and reported on ----
    observed = collections.defaultdict(dict)
    audit_packets = []
    for ap in sorted(SP.rglob("transcript_audit_0*.json")):
        d = json.loads(ap.read_text(encoding="utf-8-sig"))
        audit_packets.append({"path": str(ap.relative_to(SP)).replace("\\", "/"), "sha256": sha(ap),
                              "auditor_attempt": d.get("attempt_id"),
                              "per_transcript": len(d.get("per_transcript", []))})
        for t in d.get("per_transcript", []):
            aid = (t.get("attempt_id") or "UNIDENTIFIED").split(" ")[0]
            b = normalise_book(t.get("book"), aid)
            observed[b][aid] = {"auditor": d.get("attempt_id"), "packet": ap.name,
                                "bytes": t.get("bytes"), "lane": t.get("lane")}

    books = sorted(set(attempts) | set(retained) | set(observed) | set(zero_byte))
    per_book = {}
    for b in books:
        n = len(attempts.get(b, ()))
        obs = observed.get(b, {})
        ret = retained.get(b, set())
        per_book[b] = {
            "attempts": n,
            "attempts_note": ("denominator from this book's own receipts; 0 means the book kept no per-attempt "
                              "receipts under sp_durable, which is itself the finding" if not n else None),
            "transcript_retained": len(ret),
            "transcript_mapped_but_zero_bytes": len(zero_byte.get(b, ())),
            "observed": len(obs),
            "observed_attempt_ids": sorted(obs),
            "observed_pct_of_attempts": (round(100.0 * len(obs) / n, 1) if n else None),
            "observed_by": sorted({v["auditor"] for v in obs.values()}) or None,
        }

    total_obs = sum(v["observed"] for v in per_book.values())
    corpus = {b: v for b, v in per_book.items() if b not in ("campaign", "UNIDENTIFIED")}
    zero_coverage = sorted(b for b, v in corpus.items() if v["observed"] == 0)
    covered = sorted(b for b, v in corpus.items() if v["observed"])

    return {
        "schema": "m8_transcript_coverage_census.v1",
        "built": datetime.now(timezone.utc).isoformat(),
        "authority": "owner directive OW-10 (2026-09-08): report coverage from an explicit per-book census; do "
                     "not launch another blanket audit",
        "read_only": True,
        "what_the_three_numbers_mean": {
            "attempts": "distinct attempt_ids in the book's receipts - the denominator",
            "transcript_retained": "a transcript with bytes>0 still readable; a zero-byte mapped entry is a name "
                                   "with nothing behind it and is counted separately, never as retention",
            "observed": "a stage-1 auditor READ it and wrote per-transcript findings - the only number that "
                        "supports a claim about discovered breaches",
        },
        "per_book": per_book,
        "rollup": {
            "observed_attempts_total": total_obs,
            "books_with_observation": covered,
            "books_with_zero_observation": zero_coverage,
            "plain_statement": (
                "Transcript-based observation covered %d attempts in total: %s. Every other book, including every "
                "other book before Jeremiah, had zero observed attempts." % (
                    total_obs,
                    ", ".join("%d in %s (%s%% of its %d attempts)" % (
                        per_book[b]["observed"], b, per_book[b]["observed_pct_of_attempts"],
                        per_book[b]["attempts"]) for b in covered))),
        },
        "correction_this_census_forces": {
            "superseded_claim": "the discovery method 'existed for about one attempt in eight in Lamentations and "
                                "for none of the earlier books'",
            "why_it_was_wrong": "Jeremiah is an earlier book and five of its attempts were observed and are cited "
                                "by name in the same report's own findings; and the Lamentations figure was stated "
                                "as a remembered ratio rather than a counted one",
            "replacement": "the per_book census above, cited by number",
        },
        "evidence": {"receipt_files": receipt_files, "manifests": manifests, "audit_packets": audit_packets},
        "limits": [
            "observation is per ATTEMPT, not per byte; an observed attempt was read closely over the auditor's "
            "stated slice, and each packet carries its own coverage_statement",
            "this census counts what the record shows was read. It is not a claim that unobserved attempts were "
            "sound, and OW-8 forbids treating their absence as a defect",
        ],
    }


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    d = build()
    if "--write" in sys.argv:
        OUT.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps({"per_book": {b: {k: v[k] for k in ("attempts", "transcript_retained", "observed",
                                                         "observed_pct_of_attempts")}
                                   for b, v in d["per_book"].items()},
                      "rollup": d["rollup"], "written": "--write" in sys.argv,
                      "out": str(OUT) if "--write" in sys.argv else None},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
