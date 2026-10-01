#!/usr/bin/env python3
"""Build the one-call Fable brief for Ezekiel's item22 atlas holds (OW-29, 2026-09-23).

The owner chose the item22 atlas feed for the close, after fixes, and asked for the decision Fable must make, kept
token-efficient. The item22 option fails the coverage validator's per-book rule on 8 rows: 7 feed rows are held while
their corpus rows are final, and 1 held row (M8-Ezek-082) is graded high, so it is outside the low/medium_low set.

The brief is self-contained: Fable reads no files and uses no tools. Every "now" fact is MEASURED here on the pinned
v9 corpus; every "held_because" line is the orchestrator's one-sentence summary of the cited adjudication item
(INFERRED paraphrase; the item id lets anyone check it). No recommendation is given, so the ruling is not anchored.
Fable echoes facts_sha256, so its ruling is bound to exactly these facts.

usage: gen_atlas_hold_brief.py --check | --write
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
EZ = HERE.parent
SP = EZ.parent
OUT = HERE / "atlas_hold_brief.v1.md"
PINS = {
    "rows_v9_final.jsonl": "a80b6e6712aa43bf3d8652255b4655a934af08a9cd3e036f9b320a37bbd1098c",
    "deliverables/atlas_candidate_feed_rows.jsonl": "6adc037d01ce02d4991162959e1b364bfe771915760a7875e6eae0d2de4d0f38",
    "repair2/fixround_v9/delta_docket_v9.v1.json": "9463a68183dd69e3b3f3caf6efa52655b86638be9030c0c3b2bff7e8ef015791",
    "author/final/s1_adjudication/adjudication.json": "1f068df5f395117f84ddd232fa3be8291182a2ae67075678f375d3a5c4a102f8",
    "author/final/s2_adjudication/adjudication.json": "7cb64b936381444465a34947526f2805c15eb911e2ca1a3e5045bbd7c29c8cad",
    "author/final/s3_adjudication/adjudication.json": "356b816dfa665a43811bbf7fbb76d426bea9219cae8314e1d49f3d2719b93e5a",
    "author/final/s5_adjudication/adjudication.json": "ecf425272a058b694a940f38850d4e4a94e743d6e4e2b51b3354100fe966a0aa",
    "author/final/s6_adjudication/adjudication.json": "7012a9eb9051fb4c6192a51b93925b5452f66a4ccb5471b40b4590f951a34fd7",
}
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731

# atlas id -> (row, adjudication stage, item, held_because summary, flagged signal values or None, docket keys)
HOLDS = {
    "M8-Ezek-035": ("P03-001", 5, "F-414", "GRADE_QUESTION: the medium_low grade had no stated ground.", None, ["A0", "B7"]),
    "M8-Ezek-037": ("P03-003", 3, "F-199", "STOP: signal wordevent.strict_onset contradicted the prose; signals were "
                    "outside that pass's writable scope.", ["wordevent.strict_onset"], []),
    "M8-Ezek-038": ("P03-004", 5, "F-200", "STOP: same defect as F-199 (wordevent.strict_onset; no word-event formula "
                    "opens 16:20).", ["wordevent.strict_onset"], []),
    "M8-Ezek-039": ("P03-005", 3, "F-201", "STOP: same bar as F-199 (wordevent.strict_onset, oath.as_i_live).",
                    ["wordevent.strict_onset", "oath.as_i_live"], []),
    "M8-Ezek-049": ("P03-021", 2, "F-279", "STOP: signal closure.formula_final did not fit the span; signals were "
                    "outside that pass's writable scope.", ["closure.formula_final"], []),
    "M8-Ezek-082": ("P07-003", 6, "F-494", "STOP: a class question on the classified signal utterance.mid_unit; "
                    "no edit could discharge it in that pass.", ["utterance.mid_unit"], ["B19"]),
    "M8-Ezek-083": ("P07-004", 6, "F-495", "STOP: as F-494, on utterance.mid_unit and recognition.mid_unit.",
                    ["utterance.mid_unit", "recognition.mid_unit"], ["B19"]),
    "M8-Ezek-113": ("P10-016", 1, "F-337", "STOP: evidence clause 'the gate circuit is one list the plan never cuts "
                    "inside' is false; the plan cuts inside chapter 40.", None, ["A3", "B3"]),
}
LANE_NOTES = {"M8-Ezek-113": "Both v9 blind delta lanes found the clause still present and still false "
                             "(lane A R1, lane B N1); both still judged the book fit_to_close.",
              "M8-Ezek-035": "Both v9 blind delta lanes list P03-001's grade for the campaign-end Fable review."}


def load():
    for rel, want in PINS.items():
        got = sha((EZ / rel).read_bytes())
        if got != want:
            raise SystemExit("REFUSED: %s is at %s, not the pinned digest" % (rel, got[:12]))
    rows = {r["decision_id"]: r for r in (json.loads(l) for l in (EZ / "rows_v9_final.jsonl").read_text(
        encoding="utf-8").splitlines() if l.strip())}
    feed = {r["chunk_decision_id"]: r for r in (json.loads(l) for l in (EZ / PINS_FEED).read_text(
        encoding="utf-8").splitlines() if l.strip())}
    docket = json.loads((EZ / "repair2/fixround_v9/delta_docket_v9.v1.json").read_text(encoding="utf-8"))["entries"]
    return rows, feed, docket


PINS_FEED = "deliverables/atlas_candidate_feed_rows.jsonl"


def facts():
    rows, feed, docket = load()
    out = []
    for aid, (rid, stage, item, why, flagged, dkeys) in HOLDS.items():
        adj = json.loads((EZ / ("author/final/s%d_adjudication/adjudication.json" % stage)).read_text(
            encoding="utf-8"))["items"][item]
        if adj.get("row") != rid or str(adj.get("status", "")).split()[0] not in ("STOP", "GRADE_QUESTION"):
            raise SystemExit("REFUSED: item %s no longer holds row %s" % (item, rid))
        r, f = rows[rid], feed[aid]
        if f["candidate_hold_state"] != "deferred_human_or_external_ai" or r["span"] != f["span"]:
            raise SystemExit("REFUSED: feed row %s is not the held row this brief describes" % aid)
        sig = r["observed_substrate_signals"]
        if flagged is not None:
            still = [s for s in flagged if s in sig]
            now = ("flagged signal%s still present: %s" % ("" if len(still) == 1 else "s", ", ".join(still))
                   if still else "flagged signal%s absent from the v9 row" % ("" if len(flagged) == 1 else "s"))
        else:
            now = ("clause still present in the v9 row" if "never cuts inside" in json.dumps(r, ensure_ascii=False)
                   else "clause absent from the v9 row") if rid == "P10-016" else "grade unchanged: " + r["confidence"]
        e = {"atlas_id": aid, "row": rid, "span": r["span"], "grade": r["confidence"],
             "corpus_status": [r.get("review_status"), r.get("candidate_hold_state")],
             "held_by": "author/final s%d %s" % (stage, item), "held_because": why, "now_measured": now,
             "docket_v9": {k: "%s: %s" % (docket[k]["claim"], docket[k]["class"]) for k in dkeys}}
        if aid in LANE_NOTES:
            e["delta_lanes"] = LANE_NOTES[aid]
        out.append(e)
    return out


def brief():
    fx = facts()
    fx_b = json.dumps(fx, ensure_ascii=False, sort_keys=True).encode("utf-8")
    fsha = sha(fx_b)
    lines = [
        "# Fable ruling: Ezekiel atlas-feed holds (8 rows)",
        "",
        "Use no tools and read no files; everything you need is below. Reply with the JSON object only.",
        "",
        "## The rule",
        "A book's rows in the shared atlas feed must be exactly its low/medium_low chunks, and each must mirror its "
        "chunk's span, confidence, review status and hold state (checks/validate_book_review_coverage.py). Ezekiel's "
        "v9 corpus marks every row final (candidate_review_complete, hold null). Eight feed rows break the rule: seven "
        "are held (final_deferred_review, deferred_human_or_external_ai) while their chunk is final, and one "
        "(M8-Ezek-082) is held but graded high, so it is outside the low/medium_low set.",
        "",
        "## Context",
        "Every holding reason below was set by the book's final review wave (author/final). The later fix rounds "
        "(repair, repair2 v8, v9) changed some rows. By owner ruling OW-28, you will review every low/medium_low row "
        "of every book at campaign end; this book's end packet already carries its open questions (docket keys given). "
        "Releasing a hold therefore does not drop a question from your end review; it only stops the feed claiming "
        "the chunk is unfinished.",
        "",
        "## Options",
        "- release: the feed row becomes candidate_review_complete, hold null, accepted_candidate, matching the "
        "corpus. No corpus change.",
        "- keep_held: the corpus row changes to final_deferred_review / deferred_human_or_external_ai (as Gen, Deut "
        "and Judg did for 4 rows), with its review packet held_lower_confidence. This needs a v10 corpus and two new "
        "blind delta re-check lanes before the book can close.",
        "- For M8-Ezek-082 only: drop_from_feed (the feed stays low/medium_low only; its question goes into your end "
        "packet; no corpus change) or regrade_medium_low (the corpus grade becomes medium_low with a stated ground, so "
        "the row belongs in the feed and in the low-confidence register and frontier queue; v10 plus two lanes).",
        "",
        "Scope: rule only on the hold (and on 082's grade, as its options name). Other grades and wording are for your "
        "campaign-end review.",
        "",
        "## Facts (facts_sha256 %s)" % fsha,
        "```json",
        json.dumps(fx, ensure_ascii=False, indent=1),
        "```",
        "",
        "## Reply (JSON only; each reason at most two sentences)",
        "```json",
        json.dumps({"schema": "ezek_atlas_hold_ruling.v1", "facts_sha256": fsha,
                    "rulings": {e["atlas_id"]: {"decision": ("drop_from_feed|regrade_medium_low"
                                                             if e["atlas_id"] == "M8-Ezek-082" else
                                                             "release|keep_held"), "reason": "..."} for e in fx}},
                   ensure_ascii=False, indent=1),
        "```",
        "",
    ]
    return "\n".join(lines).encode("utf-8"), fsha


def guard(target):
    g = subprocess.run([sys.executable, "-B", str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek",
                        "--target", target], cwd=str(SP), capture_output=True, text=True, encoding="utf-8",
                       env=dict(os.environ, PYTHONUTF8="1"))
    if json.loads(g.stdout)["verdict"] != "CLEAR":
        raise SystemExit("REFUSED by pin guard: " + g.stdout[-300:])


ap = argparse.ArgumentParser()
m = ap.add_mutually_exclusive_group(required=True)
m.add_argument("--check", action="store_true")
m.add_argument("--write", action="store_true")
a = ap.parse_args()
b, fsha = brief()
if a.check:
    ok = OUT.exists() and OUT.read_bytes() == b
    print(json.dumps({"verdict": "MATCH" if ok else "MISMATCH", "brief_sha256": sha(b), "facts_sha256": fsha,
                      "bytes": len(b)}))
    sys.exit(0 if ok else 1)
guard("Ezek/fable_end_review/" + OUT.name)
if OUT.exists() and OUT.read_bytes() != b:
    keep = OUT.with_name(OUT.name + ".pre_" + sha(OUT.read_bytes())[:12])
    keep.write_bytes(OUT.read_bytes())
tmp = OUT.with_suffix(".tmp")
tmp.write_bytes(b)
os.replace(tmp, OUT)
if OUT.read_bytes() != b:
    raise SystemExit("post-write check failed")
print(json.dumps({"wrote": OUT.name, "brief_sha256": sha(b), "facts_sha256": fsha, "bytes": len(b),
                  "builder_sha256": sha(Path(__file__).read_bytes())}))
