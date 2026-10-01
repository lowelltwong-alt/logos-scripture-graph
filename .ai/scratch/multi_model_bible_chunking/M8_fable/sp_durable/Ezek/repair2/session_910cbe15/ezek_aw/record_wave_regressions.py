#!/usr/bin/env python3
"""Record the author wave's applied state AND the three checks it regressed, with the baseline measured.

I ran the validator suite for the first time AFTER mutating, which meant I had no baseline and could not tell a
new flag from an old one. The harness's per-sweep preimage backups let me recover the pre-wave corpus and
measure it, so the comparison below is MEASURED on both sides rather than remembered. Running the suite before
the wave was the obvious thing to do and I did not do it.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
NOW = datetime.now(timezone.utc).isoformat()
E = []


def add(**kw):
    E.append(dict(kw, opened_at=NOW))


add(id="E13-78",
    severity="HIGH",
    headline="THE AUTHOR WAVE IS APPLIED (427 edits, 137 rows, exact parity on all seven sweeps) AND IT "
             "REGRESSED THREE CHECKS THAT WERE GREEN. hard_status GREEN -> RED. The A4 class fell 292 -> 17, "
             "which is what the wave was for; citation_sweep, hebrew_normalize and register broke.",
    raised_by="orchestrator (claude-opus-5)", status="OPEN - a remediation round is owed before any close",
    blocks_close=True, tier="MEASURED on both sides",
    applied={"preimage": "25cdba568d98ec60aa719606be7b273e6a7c7256c55b79a3c579ada3c21d0ecc",
             "postimage_after_all_repairs": "9da4b940834c9045dd47cf7c7248715986120cc47d263807f72a4323fe6f7bc2",
             "edits": 427, "rows_touched": 137, "seams_moved": 0,
             "sweeps": {"confidence": "13/13", "grounds": "29/29", "marks": "3/3", "a4": "292/292",
                        "a6": "85/85", "disclosures": "3/3", "vocab": "2/2"},
             "post_wave_repairs_by_the_orchestrator": {
                 "disclosure_remediation": "39 entries on 34 rows + 7 on 6 rows in a second pass",
                 "hebrew_byte_repair": "4 runs re-sliced from the verse their field cites"}},
    baseline_vs_now={
        "hard_status": {"before": "GREEN", "after": "RED"},
        "triage_flags": {"before": 691, "after": 804},
        "citation_sweep": {"before": "GREEN", "after": "RED (65 problems at first measurement, 19 now)"},
        "hebrew_normalize_defects": {"before": 0, "after": "8 at first measurement, 4 now"},
        "register": {"before": "GREEN, 0 flags", "after": "FLAGS, 96"},
        "refs_mirror_worklist_citations": {"before": 292, "after": 17, "note": "the improvement the wave was "
                                                                              "for"},
        "ngram7": {"before": "GREEN", "after": "GREEN", "note": "the lanes rotated their own formulations and "
                                                                "three of them ran this gate against "
                                                                "themselves before delivering"},
    },
    THE_ROOT_CAUSE_AND_IT_IS_MINE=(
        "I wrote the author brief from the RULINGS and never checked it against the VALIDATOR SUITE. The "
        "rulings say what to repair; the suite decides what 'correct' looks like mechanically. Three "
        "consequences, all of them my brief's:\n"
        "  1. The contract requires the literal phrase 'single-witness' on any entry claiming a parashah mark, "
        "paseq or puncta - 320 pre-existing entries observe it. My brief never named the duty AND capped the "
        "annotation at six words, which made the phrase impossible to write. 46 entries failed.\n"
        "  2. The register sweep forbids campaign-internal vocabulary in row prose. My brief INSTRUCTED authors "
        "to name rules in their weighings. 96 flags, from a baseline of zero.\n"
        "  3. The toolkit says 'NEVER hand-type Hebrew - slice from verse_map_oshb.json'. My brief never said "
        "so. Eight runs came back without the accents the witness carries."),
    why_this_is_the_same_shape_as_E_32_and_E_33=(
        "an artifact built from PART of its governing set. E-32 was a worklist built from part of a ruling; "
        "E-33 was a class measured from part of a definition; this is a brief written from part of the "
        "controls. In each case the part I used was the part I was thinking about."),
    the_structural_cure=("a brief that governs a mutation wave must be CHECKED AGAINST THE GATE IT WILL BE "
                         "MEASURED BY, mechanically, before launch: for every check in the suite, either the "
                         "brief carries its duty or the check is declared out of scope. That is a generated "
                         "test over the suite's own member list, not a reading."),
    what_i_did_not_do=("report the wave as complete. Every figure above is measured on both sides, and the "
                       "baseline was recovered from the harness's own per-sweep preimage backups - which "
                       "existed because the harness keeps one per sweep, not because I planned for this."),
    remaining_to_clear=["4 Hebrew normalize defects, 2 of which need an author to say which verse is meant",
                        "19 citation_sweep problems, mostly Hebrew quotes whose field cites no verse",
                        "96 register flags - prose rewrites to drop internal vocabulary",
                        "17 new A4 citations the authors' own rewrites introduced",
                        "53 A4 citations the member still cannot see (the extraction gap, E13-77)"])

add(id="E13-79",
    severity="MEDIUM",
    headline="A CONTROL THAT WORKED AND SHOULD BE KEPT: the harness's per-sweep preimage backup is what let me "
             "measure the baseline after the fact",
    raised_by="orchestrator (claude-opus-5)", status="RECORDED", blocks_close=False, tier="MEASURED",
    what_happened=("I ran the validator suite for the first time AFTER mutating 137 rows, so I had no baseline "
                   "and could not distinguish a flag the wave caused from one it inherited. The guarded "
                   "mutation harness writes a preimage backup before every sweep it applies; ten of them were "
                   "on disk, including the original at 25cdba56. I recovered the pre-wave corpus from that "
                   "backup and ran the suite on it."),
    why_it_matters=("the backup existed because the harness keeps one per sweep as a matter of course, not "
                    "because I anticipated needing it. Without it the honest report would have been 'three "
                    "checks are red and I cannot tell you whether the wave did it'."),
    the_lesson=("a cheap, unconditional, per-step artifact beats a planned one, because the thing you need it "
                "for is by definition the thing you did not plan for. And: RUN THE GATE BEFORE THE MUTATION. "
                "Measuring the baseline is one command and I skipped it."))

with Q.open("a", encoding="utf-8", newline="\n") as fh:
    for e in E:
        fh.write(json.dumps(e, ensure_ascii=False) + "\n")
rows = [json.loads(l) for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()]
print(json.dumps({"appended": [e["id"] for e in E], "queue_rows": len(rows),
                  "blocking_close": [r["id"] for r in rows if r.get("blocks_close")],
                  "queue_sha256": hashlib.sha256(Q.read_bytes()).hexdigest()}, indent=1))
