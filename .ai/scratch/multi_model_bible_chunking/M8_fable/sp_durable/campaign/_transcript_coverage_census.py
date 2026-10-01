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
OUT_V2 = HERE / "transcript_coverage_census.v2.json"
TRANSCRIPTS = SP / "transcripts"

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
    skipped_manifests = []
    manifest_blank_ids = []
    for mp in sorted(SP.rglob("transcript_manifest.v*.json")):
        # TOOLFIX-6: a manifest kept as the RECORD OF A DEFECT is not a manifest the census may read. #e11 (Q1) ruled
        # transcript_manifest.v2.CANDIDATE.json "kept under its digest as the record of the defect and never
        # installed" - but the glob matched it, so its 17 blank attempt ids reached the union. A file whose name
        # marks it CANDIDATE or SUPERSEDED is skipped and recorded.
        if any(w in mp.name.upper() for w in ("CANDIDATE", "SUPERSEDED")):
            skipped_manifests.append({"path": str(mp.relative_to(SP)).replace("\\", "/"), "sha256": sha(mp),
                                      "why": "kept as a record, never installed; not a route the census reads"})
            continue
        try:
            m = json.loads(mp.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        manifests.append({"path": str(mp.relative_to(SP)).replace("\\", "/"), "sha256": sha(mp),
                          "declares_book": m.get("book"), "mapped": m.get("mapped_count")})
        for e in m.get("mapped_transcripts", []):
            aid_ = (e.get("attempt_id") or "").strip()
            if not aid_:
                # the blank-id refusal applies to EVERY route, not only the two new ones
                manifest_blank_ids.append({"route": str(mp.relative_to(SP)).replace("\\", "/"),
                                           "entry": str(e)[:80]})
                continue
            b = normalise_book(e.get("book"), aid_)
            (retained if (e.get("bytes") or 0) > 0 else zero_byte)[b].add(aid_)

    # ---- TOOLFIX-6 (#e11 TRANSCRIPT-ROUTE Q2): the routes a producer actually writes ----
    # A consumer that reads only the manifest route measures whatever that route still holds. OW-11-m moved subagent
    # transcripts to <session>/subagents/, indexed per book, and nothing downstream was swept - so Ezekiel read 5
    # retained where 63 attempts are readable. These are the other two routes, each named per book in the output.
    index_retained = collections.defaultdict(set)
    store_retained = collections.defaultdict(set)
    route_records = collections.defaultdict(list)
    blank_ids = []

    def _stable(entry):
        """the STABLE attempt id (OW-10). map_key is a per-transcript key for relaunches (..._wave2), so it is used
        only where no execution_id exists - the pre-execution-id executions, whose map_keys are attempt-shaped."""
        x = entry.get("execution_id")
        return (x.split("#")[0] if x else (entry.get("map_key") or "")).strip()

    for ip in sorted(TRANSCRIPTS.glob("_subagents_index.*.json")):
        try:
            d = json.loads(ip.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        b = normalise_book(d.get("book"), "")
        rec = {"route": "per_book_subagents_index", "path": str(ip.relative_to(SP)).replace("\\", "/"),
               "sha256": sha(ip), "entries": len(d.get("entries") or []), "read": True,
               "rule": "retained when the durable transcript has bytes > 0 and re-hashes to its durable_sha256 at count time"}
        kept = rehash_fail = 0
        for e in d.get("entries") or []:
            aid = _stable(e)
            if not aid:
                blank_ids.append({"route": rec["path"], "agent_id": e.get("agent_id")})
                continue
            t = e.get("transcript") or {}
            dur = t.get("durable")
            p = SP / dur if dur else None
            if not (p and p.is_file() and p.stat().st_size > 0):
                continue
            want = t.get("durable_sha256")
            if want and sha(p) != want:
                rehash_fail += 1
                continue
            index_retained[b].add(aid)
            kept += 1
        rec["retained"] = kept
        rec["rehash_mismatches"] = rehash_fail
        route_records[b].append(rec)

    for sess in sorted(p for p in TRANSCRIPTS.iterdir() if p.is_dir()):
        sp_idx = sess / "_index.json"
        if not sp_idx.is_file():
            continue
        try:
            d = json.loads(sp_idx.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        # The shape binds attempt ids to preserved files with bytes only if it says so; otherwise it is RECORDED,
        # not guessed at, and the shape question returns to the controlling agent. In this campaign's stores `files`
        # is a LIST OF FILENAME STRINGS with no attempt id and no byte count, so every store falls to the second case.
        rows_ = d.get("files") or d.get("entries") or []
        if isinstance(rows_, dict):
            rows_ = list(rows_.values())
        binds = isinstance(rows_, list) and bool(rows_) and all(
            isinstance(v, dict) and ("attempt_id" in v or "attempt" in v) and ("bytes" in v or "size" in v)
            for v in rows_)
        rec = {"route": "preserved_store_index", "path": str(sp_idx.relative_to(SP)).replace("\\", "/"),
               "sha256": sha(sp_idx), "read": bool(binds), "rows": len(rows_),
               "attempt_ids_mapped_it_declares": d.get("attempt_ids_mapped")}
        if not binds:
            rec["note"] = ("present, not read by this tool: its shape does not bind attempt ids to preserved files "
                           "with bytes (its `files` is a list of file names). The shape question returns to the "
                           "controlling agent (#e11 Q2); nothing is inferred from it here.")
            route_records["UNBOUND_STORE"].append(rec)
            continue
        kept = 0
        for v in rows_:
            aid = str(v.get("attempt_id") or v.get("attempt") or "").strip()
            nb = v.get("bytes") or v.get("size") or 0
            if aid and nb:
                store_retained[normalise_book(v.get("book"), aid)].add(aid)
                kept += 1
            elif not aid and nb:
                blank_ids.append({"route": rec["path"], "file": str(v)[:60]})
        rec["retained"] = kept
        route_records["STORE"].append(rec)

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

    blank_ids = manifest_blank_ids + blank_ids
    if blank_ids:
        raise SystemExit("ABORT: %d preserved entries carry a blank attempt id; a blank id is refused (#e11 Q2):\n%s"
                         % (len(blank_ids), json.dumps(blank_ids[:10], indent=1)))
    retained_union = collections.defaultdict(set)
    for src in (retained, index_retained, store_retained):
        for b, s in src.items():
            retained_union[b] |= s
    books = sorted(set(attempts) | set(retained) | set(observed) | set(zero_byte) | set(retained_union))
    per_book = {}
    for b in books:
        n = len(attempts.get(b, ()))
        obs = observed.get(b, {})
        ret = retained.get(b, set())
        per_book[b] = {
            "attempts": n,
            "attempts_note": ("denominator from this book's own receipts; 0 means the book kept no per-attempt "
                              "receipts under sp_durable, which is itself the finding" if not n else None),
            "transcript_retained": len(retained_union.get(b, set()) & set(attempts.get(b, ()))),
            "transcript_retained_by_route": {
                "manifest": len(ret),
                "per_book_subagents_index": len(index_retained.get(b, set())),
                "preserved_store_index": len(store_retained.get(b, set())),
                "union_before_intersection": len(retained_union.get(b, set())),
                "rule": "retention is the union of the routes INTERSECTED with this book's receipt attempt ids",
            },
            "preserved_not_a_receipt_attempt": sorted(retained_union.get(b, set()) - set(attempts.get(b, ()))),
            "routes_read": route_records.get(b, []),
            "transcript_retained_manifest_route_only": len(ret),
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
        "schema": "m8_transcript_coverage_census.v2",
        "supersedes": "transcript_coverage_census.v1.json, which kept its bytes; amended by TOOLFIX-6 under "
                      "ezek_controlling_rulings_a1#e11 ruling TRANSCRIPT-ROUTE (Q2)",
        "routes": {
            "manifest": "**/transcript_manifest.v*.json, as v1 read",
            "per_book_subagents_index": "transcripts/_subagents_index.<book>.v1.json (OW-11-m), re-hashed at count time",
            "preserved_store_index": "transcripts/<session>/_index.json where its shape binds attempt ids to files with bytes",
            "retention_rule": "the union of the routes INTERSECTED with the book's receipt attempt ids; ids outside "
                              "that intersection are listed as preserved_not_a_receipt_attempt, so a _wave2 or "
                              "relaunch key never inflates retention; a blank attempt id is refused",
        },
        "manifests_skipped_as_records_not_routes": skipped_manifests,
        "unbound_store_indexes": route_records.get("UNBOUND_STORE", []),
        "store_indexes_read": route_records.get("STORE", []),
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
        # v1 keeps its bytes (#e11 Q2); the recount is written as v2
        OUT_V2.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps({"per_book": {b: {k: v[k] for k in ("attempts", "transcript_retained", "observed",
                                                         "observed_pct_of_attempts")}
                                   for b, v in d["per_book"].items()},
                      "rollup": d["rollup"], "written": "--write" in sys.argv,
                      "out": str(OUT) if "--write" in sys.argv else None},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
