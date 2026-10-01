#!/usr/bin/env python3
"""Record the remediation batch, its four escalations, the restored GREEN, and the spot wave's launch."""
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
SPOT = HERE.parent / "ezek_spot"
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
NOW = datetime.now(timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()          # noqa: E731

for n in ("spot_wave_coverage.v1.json", "SPOT_WAVE_BRIEF.md"):
    shutil.copy2(SPOT / n, EZ / n)
E = []


def add(**kw):
    E.append(dict(kw, opened_at=NOW))


add(id="E13-83",
    severity="HIGH",
    headline="THE CORPUS IS BACK TO GREEN AND BETTER THAN ITS PRE-WAVE BASELINE: hard_status GREEN, and "
             "refs_mirror GREEN where it was FLAGS before the wave. The A4 class is 292 -> 0, certified by the "
             "member itself.",
    raised_by="orchestrator (claude-opus-5)", status="DONE", blocks_close=False,
    tier="MEASURED on both sides",
    rows={"pre_wave": "25cdba568d98ec60aa719606be7b273e6a7c7256c55b79a3c579ada3c21d0ecc",
          "now": sha(EZ / "repair" / "rows_v7_cwo24.jsonl"), "count": 145},
    suite_baseline_vs_now={
        "hard_status": {"before": "GREEN", "after": "GREEN"},
        "refs_mirror": {"before": "FLAGS (292 worklist citations)", "after": "GREEN (0)",
                        "note": "this was the wave's whole purpose and it was FLAGS even at baseline"},
        "citation_sweep": {"before": "GREEN", "after": "GREEN", "peak": "RED, 65 problems"},
        "register": {"before": "GREEN, 0", "after": "GREEN, 0", "peak": "FLAGS, 96"},
        "hebrew_normalize": {"before": "0 defects", "after": "0 defects", "peak": "8"},
        "web_quotes": {"before": 101, "after": 40},
        "mark_symmetry": {"before": 6, "after": 4},
        "universals": {"before": 584, "after": 665,
                       "note": "+81. This member is declared NON-SCORING by #e13 P4, so it is not a gate - but "
                               "it is 81 new absolute-sounding claims in new prose, and it is routed to the "
                               "spot wave rather than waved through on the ruling's licence."},
        "ngram7": {"before": "GREEN", "after": "GREEN"},
        "triage_flags": {"before": 691, "after": 709,
                         "reconciliation": "-61 web_quotes, -2 marks, +81 universals = +18, exact"},
    },
    total_mutation={"edits": 461, "sweeps": 12, "rows_touched": 137, "seam_moves": 0,
                    "seam_moves_basis": ("MEASURED by byte comparison of every protected field across all 145 "
                                         "rows between the pre-wave and current corpora, not inferred from the "
                                         "harness's refusals")})

add(id="E13-84",
    severity="HIGH",
    headline="FOR THE CONTROLLING AGENT: the citation sweep's Hebrew arm locates each run with find(), so two "
             "byte-identical runs in one field are BOTH judged at the first one's position. That is the blind "
             "spot that let the orchestrator's wrong-verse repair pass every byte check.",
    raised_by="the remediation agent (claude-opus-5 subagent), unprompted",
    status="OPEN - needs the controlling agent", blocks_close=False, tier="MEASURED",
    the_mechanism=("the arm finds a Hebrew run's position with a first-match search, then collates it against "
                   "the references near THAT position. Where the same run appears twice in one field, the "
                   "second occurrence is judged in the first's neighbourhood."),
    what_it_hid=("my Hebrew repair gave both occurrences of one word Ezek.5.7's bytes although the second "
                 "occurrence's clause attributes it to Ezek.5.10. It passed every byte check and every "
                 "collation check, because the second run was judged where the first one stood."),
    it_still_bites=("after the remediation agent's fix the row is byte-correct for both verses, but MT 5:8 and "
                    "MT 5:10 carry identical therefore-head bytes, so the 5:10 run is still checked in 5:8's "
                    "neighbourhood. It passes and it is correct - and NO GATE PROTECTS THAT CLASS."),
    the_proposed_fix="finditer with per-match offsets, so each occurrence is collated at its own position",
    the_agents_own_words="'Reported, not exploited.'",
    why_it_matters_beyond_this_row=("a checker that judges the second instance at the first's position cannot "
                                    "see a wrong-verse attribution in any field carrying a repeated formula - "
                                    "and this book's prose repeats formulae constantly, because that is what "
                                    "its boundaries are made of"))

add(id="E13-85",
    severity="MEDIUM",
    headline="FOR THE CONTROLLING AGENT: a TRUE ABSENCE CLAIM about a paseq is UNWRITABLE in the ROLE "
             "vocabulary - the sweep's paseq arm has no negation guard and the DISCLOSURE-paseq token itself "
             "supplies the device name that fires it",
    raised_by="the remediation agent, resolving REM-059", status="OPEN - needs the controlling agent",
    blocks_close=False, tier="MEASURED",
    the_mechanism=("the paseq arm fires whenever the device name appears anywhere in an annotation and the "
                   "census is empty at that verse. It has no adjacent-negation guard - unlike the puncta arm, "
                   "which does. And [DISCLOSURE-paseq] itself contains the device name, so the token alone "
                   "trips it."),
    consequence="'no paseq stands here' cannot be written with the token whose job is paseq disclosure",
    what_the_agent_did=("used [ANCHOR]: 'oshb:Ezek.41.9 [ANCHOR] device census records no stroke here "
                        "(single-witness, tier-3)'. Not WARRANT-absence-over-range, because the claim is "
                        "single-verse rather than over a range, and the row's own prose says stroke density is "
                        "never a boundary argument - so a WARRANT token would be a defect under the role "
                        "rule."),
    the_question_for_the_ruling=("if absence claims are to be expressible at all, the paseq arm needs the "
                                 "adjacent-negation guard the puncta arm already has, or the vocabulary needs "
                                 "a single-verse absence token. The agent's ANCHOR reading is defensible and "
                                 "is not a substitute for that decision."))

add(id="E13-86",
    severity="MEDIUM",
    headline="MY REGISTER SUBSTITUTION BROKE FIVE SENTENCES GRAMMATICALLY, all scholar-visible; the "
             "remediation agent found them and correctly declined to fix prose outside its mandate",
    raised_by="the remediation agent; owned by the orchestrator", status="DONE - repaired",
    blocks_close=False, tier="MEASURED",
    what_broke=["'Read off the pinned the section-mark record' - a doubled article",
                "'not capped. the mark-disclosure duty, MEASURED from' - a sentence beginning lower case",
                "'the division the division plan holds at the division plan's held question' - two of my "
                "substitutions colliding in one clause",
                "'a scene seam the division plan's held question names by verse' - my section-number "
                "substitution reading as the clause's subject",
                "'reading each section mark as standing on the verse it follows no samekh or pe falls' - a "
                "dropped clause boundary running two clauses together"],
    the_cause=("I replaced internal labels with descriptive phrases by regex and never checked that the result "
               "read as English. A substitution that satisfies a checker and mangles a sentence has moved the "
               "defect from one audience to another - the gate was green and the prose was broken."),
    repaired="5 edits, grammar only, no claim changed; register re-verified GREEN afterwards so the repair did "
             "not reintroduce what it removed",
    the_lesson=("a mechanical text substitution over prose needs a READING pass, or a check that the result "
                "parses as language. I have no such check and did not read the 30 edited fields."))

add(id="E13-87",
    headline="THE SPOT WAVE IS LAUNCHED at FULL coverage: 92 of 145 rows, derived by DIFFING the pre-wave and "
             "current corpora field by field rather than listed from memory",
    raised_by="orchestrator (claude-opus-5)", status="RUNNING", blocks_close=False, tier="MEASURED",
    coverage={"rows": 92, "basis": "every row whose grounds-bearing fields changed, plus #e14 C3's four "
                                   "RETURNed rows (all of which changed grounds anyway)",
              "index_only_rows_excluded": 49,
              "why_excluded": "their only change indexes claims the prose already made; the ruling scopes full "
                              "coverage to the grounds-bearing fields, and the exclusion is reported so the "
                              "scoping is visible rather than implied",
              "untouched_rows": 4,
              "reconciliation": "92 + 49 + 4 = 145",
              "artifact": "Ezek/spot_wave_coverage.v1.json",
              "artifact_sha256": sha(EZ / "spot_wave_coverage.v1.json")},
    why_derived_not_listed=("I know which sweeps ran and roughly which rows they touched, and that is exactly "
                            "the knowledge that produced ledger E-32. The set is derived from bytes so a row I "
                            "have forgotten cannot be omitted."),
    lanes={"count": 3, "rows": [31, 31, 30],
           "interleaved_by_stride": ("the author lanes were contiguous stretches, so a contiguous spot lane "
                                     "would map onto one author's work and that author's habits would read as "
                                     "the shape of the book. Each reviewer sees all six authors mixed."),
           "each_slice_carries": "the PRE-wave and POST-wave bytes of its rows, field by field, because "
                                 "'did a repair change a conclusion it was only meant to reword' cannot be "
                                 "answered from the result alone"},
    checklist=["role tokens against what the rationale actually rests on",
               "DID A REPAIR CHANGE A CONCLUSION IT WAS ONLY MEANT TO REWORD - the item I most want answered",
               "every factual claim true to the bytes",
               "the 81 new absolute claims the non-scoring universals member will not stop",
               "quotations accurate to the verse CITED, not merely to some verse",
               "confidence against CONF-CAL where a grade moved, and where it did not but the grounds did"],
    brief_sha256=sha(EZ / "SPOT_WAVE_BRIEF.md"))

with Q.open("a", encoding="utf-8", newline="\n") as fh:
    for e in E:
        fh.write(json.dumps(e, ensure_ascii=False) + "\n")
rows = [json.loads(l) for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()]
print(json.dumps({"appended": [e["id"] for e in E], "queue_rows": len(rows),
                  "open_for_the_controlling_agent": [r["id"] for r in rows
                                                     if "needs the controlling agent" in str(r.get("status"))],
                  "blocking_close": [r["id"] for r in rows if r.get("blocks_close")]}, indent=1))
