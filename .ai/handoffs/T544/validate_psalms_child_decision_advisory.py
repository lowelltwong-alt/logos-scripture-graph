#!/usr/bin/env python3
"""Validate the T544 182-row Psalms child advisory against current local sources."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_LEDGER = ROOT / ".ai/handoffs/T544/psalms_child_decision_advisory.jsonl"
DEFAULT_CHUNKS = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Ps/chunks.jsonl"
DEFAULT_WEB = ROOT / "data/canonical/translations/eng-web/translation_witnesses.jsonl"
DEFAULT_REPORT = ROOT / ".ai/handoffs/T544/psalms_child_decision_advisory_validation.json"
SCHEMA = "t544_psalms_child_decision_advisory.v1"
REQUIRED = {
    "decision_id", "span", "child_literary_form", "deciding_boundary_refs",
    "child_specific_rationale", "whole_parent_alternative",
    "rejected_alternative_merge_span", "alternative_disposition",
    "alternative_disposition_reason", "advisory", "exact_web_observation_refs",
    "authority", "authorizes_m7_change", "validation_scope",
    "bespoke_prose_approved", "copy_into_m7_final_fields_permitted",
}
ADVISORY_CONSTRUCTORS = {
    "middle_child_opening": re.compile(r"^This middle child has two observed edges\.", re.I),
    "last_child_endpoint_opening": re.compile(r"^The child begins after the ", re.I),
    "middle_opening_and_closure": re.compile(r"give the proposed .+ unit its own opening and closure", re.I),
    "replacement_child_alternative": re.compile(r"remains valid as parent context, but loses as a replacement child because it suppresses", re.I),
}
KNOWN_SHELLS = {
    "poem_specific_arc": re.compile(r"follows a poem-specific arc", re.I),
    "material_counterproposal": re.compile(r"material counterproposal assessed here is", re.I),
    "larger_child_wrapper": re.compile(r"strongest larger-child alternative", re.I),
    "audited_movement": re.compile(r"those lines frame the audited poem-specific movement", re.I),
    "tested_merger": re.compile(r"the tested merger is specific", re.I),
    "adjacent_span_answer": re.compile(r"adjacent-span alternative receives a concrete answer", re.I),
    "both_as_one_child": re.compile(r"treating both as one child was considered rather than assumed", re.I),
    "web_coordinates_stable": re.compile(r"the WEB coordinates for .+ are stable", re.I),
    "local_form_metadata_disclaimer": re.compile(r"the local form claim does not depend on treating", re.I),
    "peer_compared": re.compile(r"the peer compared", re.I),
}
SPAN_RE = re.compile(r"Ps\.(\d+)\.(\d+)(?:-Ps\.\1\.(\d+))?$")
EDGE_RE = re.compile(r"(Ps\.\d+\.\d+)\|(Ps\.\d+\.\d+)$")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows=[]
    with path.open(encoding="utf-8") as handle:
        for number,line in enumerate(handle,1):
            if not line.strip():
                continue
            try: row=json.loads(line)
            except json.JSONDecodeError as exc: raise ValueError(f"{path}:{number}: {exc}") from exc
            if not isinstance(row,dict): raise ValueError(f"{path}:{number}: expected object")
            rows.append(row)
    return rows


def bounds(span: str) -> tuple[str,str]:
    parts=span.split("-")
    return parts[0],parts[-1]


def verse(ref: str) -> int: return int(ref.rsplit(".",1)[1])
def psalm(ref: str) -> int: return int(ref.split(".")[1])


def normalized(text: str) -> str:
    value=text.lower()
    value=re.sub(r"m7_sol-ps-\d+", "<decision>", value)
    value=re.sub(r"ps\.\d+\.\d+(?:-ps\.\d+\.\d+)?", "<ref>", value)
    value=re.sub(r"\d+", "#", value)
    value=re.sub(r"\s+", " ", value)
    return value.strip()


def shingle_set(text: str, width: int=18) -> set[tuple[str,...]]:
    words=re.findall(r"[a-z0-9]+", text.lower())
    return {tuple(words[i:i+width]) for i in range(max(0,len(words)-width+1))}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger",type=Path,default=DEFAULT_LEDGER)
    parser.add_argument("--chunks",type=Path,default=DEFAULT_CHUNKS)
    parser.add_argument("--web",type=Path,default=DEFAULT_WEB)
    parser.add_argument("--report",type=Path,default=DEFAULT_REPORT)
    args=parser.parse_args()
    errors=[]
    try:
        ledger=read_jsonl(args.ledger)
        chunks=read_jsonl(args.chunks)
        web_rows=read_jsonl(args.web)
    except (OSError,ValueError) as exc:
        print(f"ERROR: {exc}",file=sys.stderr); return 1

    web={r.get("osis_ref") for r in web_rows if str(r.get("osis_ref","")).startswith("Ps.")}
    by_ps=defaultdict(list)
    for row in chunks:
        start,_=bounds(str(row.get("span","")))
        if start.startswith("Ps."):
            by_ps[psalm(start)].append(row)
    for rows in by_ps.values(): rows.sort(key=lambda r:verse(bounds(r["span"])[0]))
    split={p:rows for p,rows in by_ps.items() if len(rows)>1}
    expected=[r for p in sorted(split) for r in split[p]]
    expected_by_id={r["decision_id"]:r for r in expected}
    actual_by_id={r.get("decision_id"):r for r in ledger}

    if len(ledger)!=182: errors.append(f"row_count={len(ledger)} expected=182")
    if len(split)!=49: errors.append(f"split_psalm_count={len(split)} expected=49")
    duplicate_ids=[k for k,v in Counter(r.get("decision_id") for r in ledger).items() if v>1]
    if duplicate_ids: errors.append(f"duplicate IDs: {duplicate_ids[:12]}")
    missing=sorted(set(expected_by_id)-set(actual_by_id)); extra=sorted(set(actual_by_id)-set(expected_by_id))
    if missing: errors.append(f"missing IDs: {missing[:20]}")
    if extra: errors.append(f"extra IDs: {extra[:20]}")

    normalized_by_ps=defaultdict(dict)
    rationales={}
    shell_hits=defaultdict(list)
    advisory_constructor_hits=defaultdict(list)
    shingle_owners=defaultdict(list)
    advisory=Counter()
    for row in ledger:
        did=str(row.get("decision_id","")); current=expected_by_id.get(did)
        if current is None: continue
        absent=sorted(REQUIRED-set(row))
        if absent: errors.append(f"{did}: missing fields {absent}")
        if row.get("schema_version")!=SCHEMA: errors.append(f"{did}: bad schema_version")
        if row.get("span")!=current.get("span"): errors.append(f"{did}: span mismatch")
        if row.get("child_literary_form")!=current.get("literary_form"): errors.append(f"{did}: literary form mismatch")
        if row.get("authority")!="advisory_candidate_evidence_only" or row.get("authorizes_m7_change") is not False:
            errors.append(f"{did}: advisory/non-authorizing flags invalid")
        if row.get("validation_scope")!="structural_and_advisory_coverage_only":
            errors.append(f"{did}: validation_scope must remain structural/advisory only")
        if row.get("bespoke_prose_approved") is not False or row.get("copy_into_m7_final_fields_permitted") is not False:
            errors.append(f"{did}: prose-copy prohibition flags invalid")
        if row.get("advisory") not in {"R","H","RC"}: errors.append(f"{did}: invalid advisory")
        advisory[str(row.get("advisory"))]+=1
        rationale=str(row.get("child_specific_rationale","")).strip()
        reason=str(row.get("alternative_disposition_reason","")).strip()
        if len(rationale)<220: errors.append(f"{did}: rationale too short")
        if len(reason)<100: errors.append(f"{did}: alternative reason too short")
        if rationale.lower().strip()==str(row.get("child_literary_form","")).replace("_"," ").lower():
            errors.append(f"{did}: rationale merely restates literary form")
        for name,pattern in KNOWN_SHELLS.items():
            if pattern.search(rationale) or pattern.search(reason): shell_hits[name].append(did)
        for name,pattern in ADVISORY_CONSTRUCTORS.items():
            if pattern.search(rationale) or pattern.search(reason): advisory_constructor_hits[name].append(did)
        current_ps=psalm(bounds(current["span"])[0]); group=split[current_ps]
        idx=next(i for i,r in enumerate(group) if r["decision_id"]==did)
        expected_edges=[]
        if idx:
            expected_edges.append(f"{bounds(group[idx-1]["span"])[1]}|{bounds(current["span"])[0]}")
        if idx+1<len(group):
            expected_edges.append(f"{bounds(current["span"])[1]}|{bounds(group[idx+1]["span"])[0]}")
        edges=row.get("deciding_boundary_refs")
        if edges!=expected_edges: errors.append(f"{did}: boundary refs {edges!r} expected {expected_edges!r}")
        for edge in expected_edges:
            if edge not in rationale: errors.append(f"{did}: rationale omits boundary {edge}")
            match=EDGE_RE.fullmatch(edge)
            if not match: errors.append(f"{did}: malformed edge {edge}")
        obs=row.get("exact_web_observation_refs")
        if not isinstance(obs,list) or not obs: errors.append(f"{did}: observation refs missing")
        else:
            bad=[x for x in obs if x not in web]
            if bad: errors.append(f"{did}: non-WEB refs {bad[:6]}")
            needed=set(bounds(current["span"]))
            for edge in expected_edges: needed.update(edge.split("|"))
            if not needed.issubset(set(obs)): errors.append(f"{did}: observation refs omit {sorted(needed-set(obs))}")
        for field in ("whole_parent_alternative","rejected_alternative_merge_span"):
            span=str(row.get(field,"")); match=SPAN_RE.fullmatch(span)
            if not match: errors.append(f"{did}: malformed {field}={span!r}")
            elif int(match.group(1))!=current_ps: errors.append(f"{did}: cross-Psalm {field}")
        norm=normalized(rationale)
        prior=normalized_by_ps[current_ps].get(norm)
        if prior: errors.append(f"{did}: normalized same-Psalm duplicate of {prior}")
        normalized_by_ps[current_ps][norm]=did
        exact_prior=rationales.get(rationale)
        if exact_prior: errors.append(f"{did}: copied rationale from {exact_prior}")
        rationales[rationale]=did
        for shingle in shingle_set(rationale): shingle_owners[(current_ps,shingle)].append(did)
        if current_ps==119:
            if "heading" in rationale.lower(): errors.append(f"{did}: Psalm 119 heading claim is forbidden")
            start,end=bounds(current["span"])
            if len(obs)<8 or verse(end)-verse(start)!=7: errors.append(f"{did}: Psalm 119 octet evidence incomplete")

    for name,ids in shell_hits.items(): errors.append(f"known constructor shell {name}: {ids[:12]}")
    copied_shingles=[]
    for (p,shingle),ids in shingle_owners.items():
        unique=sorted(set(ids))
        if len(unique)>=3:
            copied_shingles.append((p," ".join(shingle),unique))
    if copied_shingles:
        for p,phrase,ids in copied_shingles[:12]:
            errors.append(f"Psalm {p}: copied 18-word prose across {ids}: {phrase}")

    report={
        "validator":"validate_psalms_child_decision_advisory.py",
        "status":"fail" if errors else "pass_structural_advisory_only",
        "pass_scope":"structural_and_advisory_coverage_only",
        "bespoke_prose_approved":False,
        "copy_into_m7_final_fields_permitted":False,
        "limitation":"Recurring generated sentences make this ledger an evidence-address and coverage artifact, not approved final rationale or review prose.",
        "non_authorizing":True,
        "ledger":{"path":args.ledger.as_posix(),"rows":len(ledger),"sha256":hashlib.sha256(args.ledger.read_bytes()).hexdigest()},
        "current_source":{"chunks_sha256":hashlib.sha256(args.chunks.read_bytes()).hexdigest(),"web_sha256":hashlib.sha256(args.web.read_bytes()).hexdigest()},
        "coverage":{"split_psalms":len(split),"expected_child_ids":len(expected_by_id),"missing_ids":len(missing),"extra_ids":len(extra)},
        "advisory_counts":dict(sorted(advisory.items())),
        "normalized_same_psalm_duplicates":0 if not errors else sum("normalized same-Psalm duplicate" in e for e in errors),
        "known_constructor_shell_hits":{k:len(v) for k,v in sorted(shell_hits.items())},
        "advisory_generated_constructor_counts":{k:len(v) for k,v in sorted(advisory_constructor_hits.items())},
        "copied_psalm_group_prose_hits":len(copied_shingles),
        "error_count":len(errors),
        "errors":errors,
    }
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    if errors:
        for error in errors[:30]: print(f"ERROR: {error}",file=sys.stderr)
        if len(errors)>30: print(f"ERROR: {len(errors)-30} more",file=sys.stderr)
        return 1
    print(json.dumps(report,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
