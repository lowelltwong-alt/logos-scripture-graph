#!/usr/bin/env python3
"""Build the Q8 coverage statement for Ezekiel from the record: ruling Q8 of ezek_controlling_rulings_a1#e2, with the shape
fixed by SP/Ezek/Q8_COVERAGE_STATEMENT_TEMPLATE.md and amended by ruling Q8-T (a)-(e) of ezek_controlling_rulings_a1#e4. It
reads, and never writes, the campaign census, the capture index, the receipts and the transcript map.

  1. CENSUS: the Ezek block of _transcript_coverage_census.py's stdout, verbatim.
  2. PER-EXECUTION LAYER TABLE: one line per Ezek execution in capture_index.v1.jsonl, with layers A, B and C separate.
     Beside layer A it carries two behaviour classes, both labelled and never substituted for each other:
       - the CENSUS-TIME class from finding_ezek_transcripts_decayed_before_mirror.v3.json (Q8-T (b)), for the executions that
         finding covers;
       - the class OBSERVED NOW from the runtime transcript file (A = bytes > 0, B = zero bytes). The runtime root is recorded
         with whether it exists; when it is absent the column reads 'UNAVAILABLE (runtime root not present)' (Q8-T (c)).
  3. COMPENSATIONS:
       1. EVIDENCE PRESENT only when the primaries index lists every row id of the final rows file against both blind lanes'
          execution ids; otherwise 'PENDING (index covers N of M rows)' (Q8-T (d)).
       2. The second Fable review's deliverable; PENDING while it is absent.
       3. Per layer-A-lost execution: its landing receipt (file path and the sha256 of its receipt line) and the deterministic
          results that receipt carries - outcome, form defects, local tiling, E-01 normalizer counts - read from the receipt,
          never a generic sentence (Q8-T (a)).
  4. WHAT THE AUDIT READ.
No count is summed across layers, lanes or executions. The stdout tally is labelled a tally of table rows and is never copied
into the statement (Q8-T (e)).

Usage: _coverage_statement_ezek.py --label <name> [--primaries-index <json>] [--final-rows <jsonl>] [--second-review <path>] [--dry-run]
  --primaries-index JSON shape: {"rows": [{"decision_id": ..., "LF_execution_id": ..., "OL_execution_id": ...}, ...]}
Writes SP/Ezek/coverage/coverage_statement.<label>.md and .json; refuses to overwrite a differing file; --dry-run writes nothing."""
import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
SP = EZ.parent
# TOOLFIX-6 (#e11 Q3): the hardcoded session root is GONE. It named ONE session's tasks/ tree - the route OW-11-m
# established holds 0 bytes - so it classed 78 preserved transcripts as B/unknown. The observed-now class is now read
# per execution from the per-book preserver index, and every session root that index names is recorded with whether
# it exists.
SUBIDX = SP / "transcripts" / "_subagents_index.ezek.v1.json"
CENSUS_V2 = SP / "campaign" / "transcript_coverage_census.v2.json"
FINDING = SP / "campaign" / "finding_ezek_transcripts_decayed_before_mirror.v3.json"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load_receipts():
    """{execution_id: (receipts file relative to SP, sha256 of the receipt line, receipt)}"""
    out = {}
    for f in sorted(EZ.rglob("*_attempt_receipts.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                out[r.get("execution_id")] = (str(f.relative_to(SP)).replace("\\", "/"), hashlib.sha256(line.encode("utf-8")).hexdigest(), r)
    return out


def census_classes():
    if not FINDING.is_file():
        return {}
    d = json.loads(FINDING.read_text(encoding="utf-8")).get("final_census_writer_wave_and_phase_0") or {}
    out = {}
    for group, label in (("durable", "durable"), ("lost", "lost")):
        for e in d.get(group) or []:
            if isinstance(e, dict) and e.get("execution"):
                out[e["execution"]] = "%s; behaviour %s" % (label, e.get("behaviour"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--primaries-index")
    ap.add_argument("--final-rows")
    ap.add_argument("--second-review")
    ap.add_argument("--dry-run", action="store_true", help="print the summary and write nothing")
    a = ap.parse_args()
    # the statement's census block must EQUAL census v2's Ezek block (#e11 Q5), so it is read from the written
    # artifact rather than re-derived from a fresh run that could drift from the file the close quotes.
    if not CENSUS_V2.is_file():
        raise SystemExit("ABORT: %s is absent; the statement's census block must equal census v2 (#e11 Q5)" % CENSUS_V2)
    census = (json.loads(CENSUS_V2.read_text(encoding="utf-8")).get("per_book") or {}).get("Ezek")
    tmap = json.loads((EZ / "_transcript_map.ezek.json").read_text(encoding="utf-8"))
    by_exec = {v["execution_id"]: v for v in tmap.values() if isinstance(v, dict) and v.get("execution_id")}
    rows = [json.loads(l) for l in (SP / "campaign" / "capture_index.v1.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    ez = [r for r in rows if r.get("book") == "Ezek"]
    classes_at_census = census_classes()
    receipts = load_receipts()
    # the preserver index, keyed by agent id, is the route the runtime actually writes (OW-11-m)
    sub = json.loads(SUBIDX.read_text(encoding="utf-8")) if SUBIDX.is_file() else {"entries": []}
    by_agent = {e.get("agent_id"): e for e in sub.get("entries", []) if e.get("agent_id")}
    session_roots = {}
    for e in sub.get("entries", []):
        s = e.get("session")
        if s and s not in session_roots:
            d_ = SP / "transcripts" / s
            session_roots[s] = {"durable_store": str(d_), "exists": d_.is_dir()}

    # the index also keys by map_key, which for the pre-execution-id executions IS the attempt id. 19 rows of this
    # table carry no agent_id in the capture index (the executions that predate L-0017's write-the-map-at-launch
    # rule), and resolving them by agent id alone reports UNAVAILABLE for transcripts that are demonstrably
    # preserved. So the lookup falls back to the attempt id, and the fallback is disclosed per row.
    by_attempt = {}
    for e in sub.get("entries", []):
        k = (e.get("execution_id") or "").split("#")[0] or (e.get("map_key") or "")
        if k:
            by_attempt.setdefault(k, e)

    def observed_now(agent_id, attempt_id=None):
        """A | B | UNAVAILABLE, from the index entry for this agent id (or, disclosed, its attempt id),
        re-hashed at build time."""
        e = by_agent.get(agent_id)
        via = "agent id"
        if not e and attempt_id:
            e = by_attempt.get(attempt_id)
            via = "attempt id (no agent id recorded for this execution)"
        if not e:
            return "UNAVAILABLE (not in the preserver index)"
        t = e.get("transcript") or {}
        dur = t.get("durable")
        p = SP / dur if dur else None
        if p and p.is_file() and p.stat().st_size > 0:
            got = sha(p)
            want = t.get("durable_sha256")
            if want and got != want:
                return "UNAVAILABLE (durable copy does not re-hash to the index digest)"
            return "A (durable copy holds %d bytes and re-hashes; matched by %s)" % (p.stat().st_size, via)
        if (t.get("live_bytes") or 0) == 0 and (t.get("durable_bytes") or 0) == 0:
            return "B (the index records 0 live and 0 durable bytes)"
        return "UNAVAILABLE (not in the preserver index)"

    root_present = any(v["exists"] for v in session_roots.values())
    table = []
    for r in ez:
        aid = r.get("agent_id") if r.get("agent_id") not in (None, "", "UNAVAILABLE") else (by_exec.get(r["execution_id"]) or {}).get("agent_id")
        now = observed_now(aid, str(r.get("execution_id") or "").split("#")[0])
        table.append({"execution_id": r["execution_id"], "role": r.get("role"), "model_ordered": r.get("model_ordered"),
                      "outcome": r.get("outcome_recorded_by_the_receipt"), "layer_a": r.get("layer_a_runtime_actions"),
                      "behaviour_class_at_census": classes_at_census.get(r["execution_id"], "not in the census finding"),
                      "behaviour_class_observed_now": now, "layer_b": r.get("layer_b_exposed_thinking"), "layer_c": r.get("layer_c_evidence_note")})

    # ---- compensation 1 (Q8-T (d)) ----
    if a.primaries_index and a.final_rows and Path(a.primaries_index).is_file() and Path(a.final_rows).is_file():
        idx = json.loads(Path(a.primaries_index).read_text(encoding="utf-8"))
        final_ids = [json.loads(l)["decision_id"] for l in Path(a.final_rows).read_text(encoding="utf-8").splitlines() if l.strip()]
        covered = {e.get("decision_id") for e in idx.get("rows", []) if e.get("LF_execution_id") and e.get("OL_execution_id")}
        full = len(covered) == len(final_ids) and covered == set(final_ids)
        comp1 = {"status": "EVIDENCE PRESENT" if full else "PENDING (index covers %d of %d rows)" % (len(covered & set(final_ids)), len(final_ids)),
                 "evidence": a.primaries_index, "sha256": sha(a.primaries_index), "final_rows": a.final_rows, "final_rows_sha256": sha(a.final_rows),
                 "rule": "every row id of the final rows file against both blind lanes' execution ids; no sampling"}
    else:
        comp1 = {"status": "PENDING (no primaries index and final rows file given)", "evidence": None,
                 "rule": "every row id of the final rows file against both blind lanes' execution ids; no sampling"}
    # ---- compensation 2 ----
    if a.second_review and Path(a.second_review).is_file():
        comp2 = {"status": "EVIDENCE PRESENT", "evidence": a.second_review, "sha256": sha(a.second_review)}
    else:
        comp2 = {"status": "PENDING", "evidence": a.second_review}
    comp2["rule"] = ">= 3 byte-level re-derivations per layer-A-lost part, from the section-7 regions"
    # ---- compensation 3 (Q8-T (a)) ----
    lost = [t for t in table if not (t["layer_a"] or {}).get("sha256")]
    comp3_entries = []
    for t in lost:
        rec = receipts.get(t["execution_id"])
        if not rec:
            comp3_entries.append({"execution_id": t["execution_id"], "receipt": "NO RECEIPT FOUND"})
            continue
        path, line_sha, r = rec
        ls = r.get("landing_summary") or {}
        comp3_entries.append({"execution_id": t["execution_id"], "receipt_file": path, "receipt_line_sha256": line_sha,
                              "outcome": r.get("outcome"), "form_defects": r.get("form_defects"),
                              "local_tiling": ls.get("local_tiling"), "e01_normalizer": ls.get("normalizer"),
                              "deliverable_sha256": r.get("output_sha256"), "e19_selfreported": r.get("e19_selfreported")})
    comp3 = {"status": "RECORDED", "rule": "the E-19 and splice-never-type self-reports of layer-A-lost executions are carried as SELF-REPORTED; "
                                           "the receipts' deterministic results are the layer-A-equivalent evidence", "executions": comp3_entries}
    comp = {"1_full_dual_blind_primaries": comp1, "2_second_fable_review_rederivations": comp2, "3_self_reports_carried_as_self_reported": comp3}
    doc = {"schema": "m8_q8_coverage_statement.v2", "book": "Ezek", "label": a.label, "built": datetime.now(timezone.utc).isoformat(),
           "authority": "ruling Q8 of ezek_controlling_rulings_a1#e2, amended by ruling Q8-T (a)-(e) of ezek_controlling_rulings_a1#e4",
           "census_verbatim": census, "session_roots_named_by_the_index": session_roots,
           "route_note": "Q8-T (f): the class at census was measured on the tasks/ route and the class observed now on the subagents route the preserver index records; neither is ever substituted for the other",
           "per_execution_layers": table, "compensations": comp,
           "what_the_audit_read": "deliverables; layer-C evidence notes; layer A only where present", "never_summed": True}
    out_dir = EZ / "coverage"
    jp, mp = out_dir / ("coverage_statement.%s.json" % a.label), out_dir / ("coverage_statement.%s.md" % a.label)
    lines = ["# Q8 coverage statement - Ezekiel (%s)" % a.label, "",
             "Built %s. Authority: ruling Q8 (#e2), amended by Q8-T (#e4). Never a summed count." % doc["built"], "",
             "## 1. Census (verbatim)", "", "```", json.dumps(census, ensure_ascii=False, indent=1), "```", "",
             "## 2. Per-execution layer table", "",
             "Session roots named by the preserver index: %s. The census-time class comes from `%s` and was measured on the tasks/ route (OW-11-m); "
             "the observed-now class is read at build time from the subagents route. The two are never substituted for each other (Q8-T (f))."
             % (json.dumps(session_roots, ensure_ascii=False), FINDING.name), "",
             "| execution | role | model ordered | outcome | layer A | class at census (tasks/ route, OW-11-m) | class observed now (subagents route) | layer B | layer C |",
             "|---|---|---|---|---|---|---|---|---|"]
    for t in table:
        lines.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            t["execution_id"], t["role"], t["model_ordered"], t["outcome"], str(t["layer_a"])[:120].replace("|", "/"),
            t["behaviour_class_at_census"], t["behaviour_class_observed_now"], str(t["layer_b"])[:60].replace("|", "/"),
            str(t["layer_c"])[:120].replace("|", "/")))
    lines += ["", "## 3. Compensations", "", "```", json.dumps(comp, ensure_ascii=False, indent=1), "```", "",
              "## 4. What the audit read", "", doc["what_the_audit_read"], ""]
    if not a.dry_run:
        out_dir.mkdir(exist_ok=True)
        for p, body in ((jp, json.dumps(doc, ensure_ascii=False, indent=1)), (mp, "\n".join(lines))):
            if p.exists() and p.read_text(encoding="utf-8") != body:
                raise SystemExit("ABORT: %s exists with different content" % p.name)
            p.write_text(body, encoding="utf-8", newline="\n")
    tally = {}
    for t in table:
        c = t["behaviour_class_observed_now"].split(" ")[0]
        tally[c] = tally.get(c, 0) + 1
    print(json.dumps({"statement": None if a.dry_run else str(mp), "dry_run": a.dry_run, "executions_in_table": len(table), "census": census,
                      "runtime_root_exists": root_present,
                      "tally_of_table_rows_by_class_observed_now (a tally of table rows; never a statement figure)": tally,
                      "compensations": {k: v["status"] for k, v in comp.items()},
                      "layer_a_lost_executions_with_receipts": sum(1 for e in comp3_entries if "receipt_file" in e),
                      "layer_a_lost_executions_without_receipts": [e["execution_id"] for e in comp3_entries if "receipt_file" not in e]},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
