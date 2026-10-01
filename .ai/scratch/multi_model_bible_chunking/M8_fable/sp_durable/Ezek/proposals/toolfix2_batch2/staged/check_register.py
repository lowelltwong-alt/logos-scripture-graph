#!/usr/bin/env python3
"""Register sweep, Ezek - FLAGS suite member (E-06 + the E-18 residual arms).

Detects workflow/administrative language in ROW PROSE (the register-bleed
class every book has shipped some of; Isa's postcheck found a 53-occurrence
corpus-wide instance that survived three corpus versions because the sweep
was not Tier-0). Pattern list HARDENED per the Isa postcheck residuals:
"that row" and "cross-part" now have their own arms.

Scans the canonical prose fields (boundary_rationale,
strongest_rejected_alternative, device_notes) of row objects and, since S1-05, the
annotation of every boundary_evidence_refs entry (the text after its leading ref token); curly-quoted
WEB spans and Hebrew runs are masked first (source text is never charged).
EXEMPT by campaign law: self-reference ("this unit" / "this row"), and the
sanctioned "(sweep: N verses)" citation shorthand (not matched by any arm).
Flags are TRIAGE CANDIDATES (E-12 law: disposition by content, never
auto-suppress, never auto-fail) - the suite carries them as flags, not RED.
Usage: check_register.py rows.jsonl [more...]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ezek_lib import HEB_RUN

PROSE_FIELDS = ("boundary_rationale", "strongest_rejected_alternative", "device_notes")
REF_TOKEN = re.compile(r"^\s*(?:oshb|web):Ezek\.\d+\.\d+(?:-(?:Ezek\.)?\d+\.\d+)?")   # S1-05: annotations are read after it

CLASSES = {
    "positional_row_reference": re.compile(
        r"\bthat row\b|\bat that row\b|"
        r"\bthe (?:previous|next|preceding|following|prior) row\b|"
        r"\brow (?:above|below)\b|\bneighbou?ring row\b|\bsibling row\b|"
        r"\b(?:previous|next|preceding|following) (?:decision|entry)\b|"
        # S1-05: without 'the', possessive, before/after, and 'one/middle/last of N ... rows'
        r"\b(?:preceding|next|following|previous|prior) row(?:['’]s)?\b|\brow (?:before|after)\b|"
        r"\b(?:one|middle|last|first) of (?:the )?\w+\b[^.;]{0,20}?\brows\b", re.I),
    "cross_part_or_part_range": re.compile(
        r"\bcross-part\b|\bpart boundary\b|\bthis part\b|\bwriter part\b|"
        r"\bassigned range\b|\bpart['’]s\b|\bbatch\b|\bP\d{2}\b(?![-\d])", re.I),
    "decision_id_in_prose": re.compile(r"\bP\d{2}-\d{3}\b"),
    "governance_tooling": re.compile(
        r"\b\w+\.(?:py|jsonl|json|md)\b|\bvalidator\b|\bchecker\b|\btoolkit\b|"
        r"\bTier-0\b|\bthe suite\b|\borchestrator\b|\battempt id\b|"
        r"\bwork order\b|\b(?:writer|author|peer|primary|spot) brief\b|"
        r"\bper the brief\b", re.I),
    "review_actor": re.compile(
        r"\bboss\b|\bpeer review\w*\b|\bpeer remedy\b|\breviewer\b|"
        r"\bprimar(?:y|ies) (?:packet|review)\b", re.I),
    "erratum_repair_narration": re.compile(
        r"\berrat(?:um|a)\b|"
        r"\brepair(?:ed|s)?\b(?=[^.;]{0,60}\b(?:order|remedy|wave|install|defect|original|cure)\b)|"
        r"\b(?:order|remedy|wave|install|defect|original)\b[^.;]{0,60}\brepair(?:ed|s)?\b|"
        r"\bcured?\b(?=[^.;]{0,60}\b(?:order|remedy|wave|defect|class)\b)", re.I),
    "session_wave_reference": re.compile(
        r"\bthis (?:session|wave|cycle)\b|"
        r"\bthe (?:writer|author|peer|spot|micro) wave\b", re.I),
    "strategy_citation": re.compile(
        r"§\s*\d|\bbook_strategy\b|\bstrategy file\b|\bper the strategy\b|"
        r"\bgate ruling\b|\bowner gate\b|\bstrategy['’]s\b|\bthe strategy\b", re.I),   # S1-05
    # S1-05 (ezek_author_wave_spot_review_s1_a1#e1): repair history and governance posture the author wave added
    "row_history_narration": re.compile(
        r"\b(?:as )?originally drafted\b|\bformer (?:single )?(?:[\d.:-]+ )?(?:\w+-verse )?(?:span|row|reading|grouping)\b|"
        r"\bprior [\d.:-]+ reading\b|\bkeeping the prior\b|\bpreviously held\b|\bcorrection to an earlier\b|"
        r"\bearlier grouping\b", re.I),
    "governance_posture": re.compile(
        r"\bposture\b|\bofficially inventoried\b|\bthe (?:ruling|order)['’]s\b|\bends the part\b|\bthe part['’]s\b", re.I),
    "staged_file_stem": re.compile(
        r"\bverse_map\w*\b|\bpmarks\w*\b|\bdevice_inventory\b|\boffset_map\b|"
        r"\bconsonantal_index\b|\bTOOLKIT\b|\bezek_lib\b", re.I),
}


def rows_from(p: Path):
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix == ".jsonl":
        return [json.loads(l) for l in text.splitlines() if l.strip()]
    data = json.loads(text)
    if isinstance(data, dict):
        return data.get("decisions", [v for v in data.values() if isinstance(v, dict)])
    return data


def main() -> int:
    flags = []
    rows_n = 0
    for f in sys.argv[1:]:
        for row in rows_from(Path(f)):
            if not isinstance(row, dict):
                continue
            rows_n += 1
            did = row.get("writer_decision_id") or row.get("decision_id") or "?"
            for field in PROSE_FIELDS:
                s = row.get(field)
                if not isinstance(s, str):
                    continue
                masked = HEB_RUN.sub(" ", s)
                masked = re.sub(r"“[^”]*”", lambda m: " " * len(m.group(0)), masked)
                for cls, pat in CLASSES.items():
                    for m in pat.finditer(masked):
                        flags.append({"file": Path(f).name, "decision_id": did,
                                      "field": field, "class": cls,
                                      "match": m.group(0)[:60],
                                      "context": s[max(0, m.start() - 60):m.start() + 80]})
            # S1-05: the annotation of every ref entry is prose too (the text after its leading ref token)
            for i, ref in enumerate(row.get("boundary_evidence_refs") or []):
                if not isinstance(ref, str):
                    continue
                ann = REF_TOKEN.sub("", ref, count=1)
                masked = HEB_RUN.sub(" ", ann)
                masked = re.sub(r"“[^”]*”", lambda m: " " * len(m.group(0)), masked)
                for cls, pat in CLASSES.items():
                    for m in pat.finditer(masked):
                        flags.append({"file": Path(f).name, "decision_id": did,
                                      "field": "boundary_evidence_refs[%d]" % i, "class": cls,
                                      "match": m.group(0)[:60],
                                      "context": ann[max(0, m.start() - 60):m.start() + 80]})
    by_class = {}
    for fl in flags:
        by_class[fl["class"]] = by_class.get(fl["class"], 0) + 1
    print(json.dumps({"rows_checked": rows_n, "flag_count": len(flags),
                      "by_class": by_class, "flags": flags,
                      "status": "GREEN" if not flags else "FLAGS"},
                     ensure_ascii=False, indent=1))
    return 1 if flags else 0


if __name__ == "__main__":
    raise SystemExit(main())
