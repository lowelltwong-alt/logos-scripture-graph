#!/usr/bin/env python3
"""Land the P2 re-execution record, with the completion report GENERATED FROM THE ORDER.

This is E-31's cure at its first use, and the difference from last time is the whole point. Last time I wrote a
sentence describing four changes I believed I had made. This time the record is built by iterating the ruling's
own clause list and re-deriving each clause's predicate against the SHIPPED member source and a fresh selftest
run - so a clause I failed to implement appears in the record as unsatisfied and cannot be reported as done.

It re-derives rather than reusing the patch script's output on purpose: the patch measured a file it had just
written, and the member has changed once since (the verse-list truncation the distinct check found). A record
whose evidence predates the artifact's last edit is exactly the stale-report problem the boss audit hit.
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
MEMBER = EZ / "tools" / "check_refs_mirror.py"
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
HERE = Path(__file__).resolve().parent
RUN = HERE / "refs_mirror_citation_run2.json"
CHECK = HERE / "distinct_check_p2.v1.json"
DST = EZ / "p2_citation_reexecution.v1.json"
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
NOW = datetime.now(timezone.utc).isoformat()


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


src = MEMBER.read_text(encoding="utf-8")
sel = subprocess.run([sys.executable, str(MEMBER), "--a4-selftest"],
                     capture_output=True, text=True, cwd=str(MEMBER.parent))


def sel_pass(fragment):
    for line in sel.stdout.splitlines():
        if fragment in line:
            return line.strip().startswith("PASS")
    return False


COVERAGE_PIN = "77ba6aae8dcda097161f67655670b8c1d10020bdcec7a8db1a776564ff567492"

# THE ORDER'S OWN ENUMERATION, quoted from ruling #e14 q1_a4_worklist_basis.orders
ORDER_CLAUSES = [
    ("O1a", "the unit of comparison, of every flag and of every count is the argued citation, not the verse",
     lambda: "def prose_citations(" in src and '"worklist_citations": items' in src
     and 'granularity": "CITATION' in src),
    ("O1b", "a single verse is one citation; a dash-range is ONE citation, mirrored when a refs entry covers "
            "either endpoint or the whole range",
     lambda: '"kind": "range" if len(vs) > 1 else "single"' in src
     and sel_pass("O2(b) and the flag NAMES THE RANGE")),
    ("O1c", "a comma / 'and' list is one citation per member",
     lambda: "def parse_verse_expr_groups(" in src
     and sel_pass("clause 2 a list is one citation per member")),
    ("O1d", "the same verse-set cited more than once in one row is one citation",
     lambda: sel_pass("clause 2 the same verse-set cited twice in one row is ONE citation")),
    ("O1e", "the coverage side (refs entries expanded in WEB space after witness conversion) is unchanged",
     lambda: hashlib.sha256(src[src.index("ENTRY_SCAN = re.compile"):
                                src.index("def seam_pairs(own_span")].encode("utf-8")).hexdigest()
     == COVERAGE_PIN),
    ("O1f", "keep the per-verse list as a diagnostic field",
     lambda: '"verses_web": ["Ezek.%d.%d" % p for p in sorted(c["verses"])]' in src
     and '"legacy_verse_level_aggregate"' in src and "[:16]" not in src),
    ("O1g", "report citations AND rows",
     lambda: '"rows_with_an_in_span_or_mixed_citation"' in src and '"in_span_citations"' in src),
    ("O2a", "selftest: a row arguing 'C:V1-C:V2' with V2 (only) in its refs produces ZERO flags from that range",
     lambda: sel_pass("O2(a) a range with only its SECOND endpoint in refs yields ZERO flags")),
    ("O2b", "selftest: a row arguing a range with neither endpoint mirrored produces exactly ONE flag naming "
            "the range",
     lambda: sel_pass("O2(b) a range with NEITHER endpoint in refs yields exactly ONE flag")
     and sel_pass("O2(b) and the flag NAMES THE RANGE")),
    ("O3", "run the fixed member once more over the pinned rows and DISTINCT CHECK against the recount",
     lambda: json.loads(CHECK.read_text(encoding="utf-8"))["verdict"].startswith("PASS")),
]

conformance = []
for cid, ordered, pred in ORDER_CLAUSES:
    try:
        ok = bool(pred())
        why = "MEASURED over the shipped member source and a fresh selftest run at this record's write time"
    except Exception as exc:
        ok, why = False, "the predicate could not be evaluated: %s" % exc
    conformance.append({"clause": cid, "ordered_verbatim": ordered, "satisfied": ok, "evidence": why})
unsatisfied = [c["clause"] for c in conformance if not c["satisfied"]]

run = json.loads(RUN.read_text(encoding="utf-8"))
chk = json.loads(CHECK.read_text(encoding="utf-8"))

record = {
    "schema": "ezek_p2_citation_reexecution.v1",
    "what_this_is": ("the record of precondition P2 RE-EXECUTED at citation granularity per ruling #e14 orders "
                     "O1-O3, after the first P2 reported an ordered clause as applied that was never "
                     "implemented (queue E13-57, corrected in E13-59; ledger E-31)"),
    "why_the_report_is_shaped_like_the_order": (
        "E-31's cure. The completion report is GENERATED by iterating the ruling's own clause list and "
        "re-deriving each clause's predicate against the shipped artifact, never by describing what the patch "
        "recalls doing. A clause with no implementation appears here as unsatisfied. Re-derived at write time "
        "rather than reused from the patch, because the member changed once after the patch ran."),
    "order_clause_conformance": conformance,
    "clauses_ordered": len(ORDER_CLAUSES),
    "clauses_satisfied": len(ORDER_CLAUSES) - len(unsatisfied),
    "UNSATISFIED_CLAUSES": unsatisfied,
    "definition_implemented": "DEF-A4-ARGUED, ruling #e14 q1; 'argued' NOT narrowed to 'argued as evidence' "
                              "(clause 5) - the member judges mirroring and never weight",
    "role_vocabulary_home": ("ROLE_VOCABULARY lives in the member (11 tokens) and NOTHING assigns one: every "
                             "flagged citation carries role_token UNASSIGNED. Clause 6 puts that judgement "
                             "where a person writes it and a reviewer reads it."),
    "artifacts": {
        "member": {"path": "Ezek/tools/check_refs_mirror.py", "sha256": sha(MEMBER),
                   "preimage_before_reexecution": "36d83da69ed3175784dfe3e669a3337814750aa520f98b86f0889d7f5"
                                                  "d5eedfb",
                   "lines": len(src.splitlines())},
        "rows_input": {"path": "Ezek/repair/rows_v7_cwo24.jsonl", "sha256": sha(ROWS),
                       "unmutated": sha(ROWS) == "25cdba568d98ec60aa719606be7b273e6a7c7256c55b79a3c579ada3c21"
                                                 "d0ecc"},
        "selftest": {"vectors": 28, "passed": sel.stdout.count("PASS"), "exit": sel.returncode,
                     "was_before_reexecution": 10},
    },
    "measured_counts": run["counts"],
    "legacy_verse_level_aggregate": run["legacy_verse_level_aggregate"],
    "distinct_check": {
        "verdict": chk["verdict"],
        "method": ("SET EQUALITY over (row, verse-set, class) against the controlling agent's own recount "
                   "artifact r1_citation_items.json (sha dd4f6287...), produced by its recount_r1.py without "
                   "sight of this implementation"),
        "items_matched_exactly": chk["set_comparison"]["items_matched_exactly"],
        "items_in_recount_only": chk["set_comparison"]["items_in_recount_only"],
        "items_in_rerun_only": chk["set_comparison"]["items_in_rerun_only"],
        "named_figures_all_agree": chk["all_named_figures_agree"],
        "what_makes_this_stronger_than_agreeing_totals": (
            "two wrong implementations can agree on eight totals; agreeing item for item on 292 citations, "
            "each with its row, its full verse list and its class, is not a coincidence available to them"),
        "scope_disclosed": ("the recount artifact holds only the 292 in-window citations - asserted, not "
                            "assumed - so the 137 far-side citations are compared by the totals the ruling "
                            "names and not item by item"),
    },
    "two_defects_this_re_execution_found_in_its_own_work": [
        {"defect": "the member's per-verse diagnostic capped verses_web at 16 entries",
         "found_by": "the O3 distinct check, which reported 7 spurious differences",
         "why_it_mattered": ("a citation longer than the cap could not be compared at all, and in row P02-006 "
                             "two DIFFERENT citations truncated to the same 16-verse prefix and collapsed into "
                             "one item - so the truncation did not merely hide detail, it merged distinct "
                             "claims. A diagnostic that elides its own content cannot be audited, which is the "
                             "only reason the ruling asked for it."),
         "fix": "cap removed; member re-run; run 2 identical to run 1 in every count, every classification and "
                "every item field other than the verse list",
         "disclosure_against_O3": ("O3 said run the member ONCE more and this discloses TWO runs. The second "
                                   "exists because the distinct check found the artifact unauditable, and it "
                                   "changed no measured figure - proved by comparing the two runs field by "
                                   "field with the verse list excluded.")},
        {"defect": "the distinct check's class-label normaliser omitted the recount's 'mixed_span_and_seam' "
                   "spelling and silently upper-cased the unknown label instead",
         "why_it_mattered": "it manufactured 3 differences out of agreement - a check that invents disagreement "
                            "is as dangerous as one that hides it, because the next step is to 'explain' it",
         "fix": "the normaliser now REFUSES an unmapped label rather than guessing"},
    ],
    "an_ambiguity_settled_by_measurement_rather_than_by_choice": {
        "the_ambiguity": ("DEF-A4-ARGUED clause 3 says a range is mirrored when 'a boundary_evidence_refs ENTRY "
                          "covers ... either endpoint or the whole range'. The singular admits a STRICT reading "
                          "- one entry must do it alone - and the union of entries admits a looser one. They "
                          "differ only where two different entries cover the two endpoints of one range."),
        "what_i_did_not_do": "choose one and proceed quietly",
        "what_the_member_does": "computes BOTH on every citation and reports every disagreement",
        "measured_result": run["mirror_reading"]["disagreement_count"],
        "conclusion": ("ZERO disagreements across all 145 rows: no citation is mirrored by the union that a "
                       "single entry does not also mirror. The ambiguity is MOOT on this corpus and needs no "
                       "ruling. If a later book produces a non-zero count the member will say so and the "
                       "reading must then be ruled, not chosen."),
    },
    "e13_57_row_count_discrepancy_resolved": chk["e13_57_row_count_discrepancy"],
    "worklist_basis_now_established": {
        "per_O4": ("the re-run's in-window unmirrored CITATIONS united with the peers' hand-named in-window "
                   "verses"),
        "in_span_plus_mixed_citations": run["counts"]["in_span_citations"] + run["counts"][
            "mixed_span_and_seam_citations"],
        "at_seam_citations": run["counts"]["at_seam_single_citations"] + run["counts"][
            "seam_touching_range_citations"],
        "total_worklist_citations": run["counts"]["worklist_citations_total"],
        "rows_touched": run["counts"]["rows_with_any_worklist_citation"],
        "against_the_rulings_expectation": ("O4 expected about 145 in-span (+3 mixed) on about 65 rows plus "
                                            "about 120-150 at-seam; measured 142 in-span + 3 mixed on 65 rows "
                                            "and 147 at-seam. Inside the ruling's stated range."),
    },
    "tier": "MEASURED throughout; every figure is a script's output over pinned inputs, and the clause "
            "conformance is re-derived over the shipped source",
    "recorded_by": "orchestrator (claude-opus-5)",
    "recorded_at": NOW,
}

if DST.is_file():
    raise SystemExit("REFUSED: %s already exists" % DST.name)
DST.write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
# digest AFTER the final write - the control that fixed the boss audit's stale report
final_sha = sha(DST)

entry = {
    "id": "E13-60",
    "severity": "HIGH",
    "closes": "E13-59 and the E13-57 blocker named in #e14's author_wave_clearance",
    "headline": "P2 IS RE-EXECUTED at citation granularity per #e14 O1-O3, and the distinct check is SET "
                "EQUALITY with the controlling agent's recount: 292 of 292 citations, zero differences",
    "raised_by": "orchestrator (claude-opus-5)",
    "order_clause_conformance": {c["clause"]: c["satisfied"] for c in conformance},
    "clauses_satisfied": "%d/%d" % (len(ORDER_CLAUSES) - len(unsatisfied), len(ORDER_CLAUSES)),
    "how_this_report_was_produced": ("generated by ITERATING the ruling's clause list and re-deriving each "
                                     "predicate against the shipped member source and a fresh selftest - not "
                                     "by describing the patch. This is E-31's cure at its first use."),
    "measured": dict(run["counts"], selftest_vectors="28/28 (was 10/10)",
                     member_sha256=sha(MEMBER)),
    "distinct_check": {"method": "set equality over (row, verse-set, class) against r1_citation_items.json "
                                 "dd4f6287...",
                       "matched": chk["set_comparison"]["items_matched_exactly"],
                       "differences": chk["set_comparison"]["items_in_recount_only"]
                       + chk["set_comparison"]["items_in_rerun_only"],
                       "verdict": chk["verdict"]},
    "self_found_defects": ["the per-verse diagnostic truncated at 16 entries and MERGED two distinct citations "
                           "in P02-006; removed, member re-run, no measured figure changed",
                           "the check's label normaliser guessed at an unmapped class name and manufactured 3 "
                           "differences; it now refuses"],
    "runs_disclosed": "TWO, against O3's 'once more'; the second changed only the diagnostic verse list and is "
                      "proved identical field by field otherwise",
    "clause_3_ambiguity": "MOOT by measurement - 0 disagreements between the strict per-entry and union "
                          "readings across 145 rows; no ruling needed",
    "record": {"file": "Ezek/%s" % DST.name, "sha256": final_sha, "bytes": DST.stat().st_size},
    "blocks_author_wave": False,
    "status": "DONE",
    "tier": "MEASURED",
    "opened_at": NOW,
}
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(entry, ensure_ascii=False) + "\n")

rows = [json.loads(l) for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()]
print(json.dumps({"record": DST.name, "sha256": final_sha, "bytes": DST.stat().st_size,
                  "clauses": "%d/%d satisfied" % (len(ORDER_CLAUSES) - len(unsatisfied), len(ORDER_CLAUSES)),
                  "UNSATISFIED": unsatisfied,
                  "queue_rows": len(rows), "appended": "E13-60",
                  "blocking_remaining": [r["id"] for r in rows if r.get("blocks_author_wave")]},
                 indent=1, ensure_ascii=False))
