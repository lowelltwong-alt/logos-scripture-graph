#!/usr/bin/env python3
"""Register sweep, Ezek - FLAGS suite member (E-06 + the E-18 residual arms).

Detects workflow/administrative language in ROW PROSE (the register-bleed
class every book has shipped some of; Isa's postcheck found a 53-occurrence
corpus-wide instance that survived three corpus versions because the sweep
was not Tier-0). Pattern list HARDENED per the Isa postcheck residuals:
"that row" and "cross-part" now have their own arms.

TOOLFIX-5 (ezek_controlling_rulings_a1#e10 ruling TOOLFIX-5): scans the CONTENT
fields of row objects - boundary_rationale,
strongest_rejected_alternative, device_notes, literature_type_guess, and every
element of boundary_evidence_refs, observed_substrate_signals and
strong_or_hebrew_tags_used. Identity fields (decision_id, writer_decision_id,
writer_part, writer_attempt_id, parent_collection, span, unit_type,
confidence, chunk_index_in_book) are never scanned. Curly-quoted WEB spans
and Hebrew runs are masked first (source text is never charged).
EXEMPT by campaign law: self-reference ("this unit" / "this row"), and the
sanctioned "(sweep: N verses)" citation shorthand (not matched by any arm).
Flags are TRIAGE CANDIDATES (E-12 law: disposition by content, never
auto-suppress, never auto-fail) - the suite carries them as flags, not RED.
Usage: check_register.py rows.jsonl [more...]   |   check_register.py --selftest
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ezek_lib import HEB_RUN

PROSE_FIELDS = ("boundary_rationale", "strongest_rejected_alternative", "device_notes")
# TOOLFIX-5 (ezek_controlling_rulings_a1#e10 ruling TOOLFIX-5 (1)): the content-field scope and the identity exemptions
CONTENT_STR_FIELDS = PROSE_FIELDS + ("literature_type_guess",)
CONTENT_LIST_FIELDS = ("boundary_evidence_refs", "observed_substrate_signals", "strong_or_hebrew_tags_used")
IDENTITY_FIELDS = ("decision_id", "writer_decision_id", "writer_part", "writer_attempt_id", "parent_collection", "span",
                   "unit_type", "confidence", "chunk_index_in_book")   # never scanned; --selftest proves each exemption

CLASSES = {
    "positional_row_reference": re.compile(
        r"\bthat row\b|\bat that row\b|"
        r"\bthe (?:previous|next|preceding|following|prior) row\b|"
        r"\brow (?:above|below)\b|\bneighbou?ring row\b|\bsibling row\b|"
        r"\b(?:previous|next|preceding|following) (?:decision|entry)\b", re.I),
    "cross_part_or_part_range": re.compile(
        r"\bcross-part\b|\bpart boundary\b|\bthis part\b|\bwriter part\b|"
        r"\bassigned range\b|\bpart['’]s\b|\bbatch\b|\bP\d{2}\b(?![-\d])", re.I),
    "decision_id_in_prose": re.compile(r"\bP\d{2}-\d{3}\b"),
    "governance_tooling": re.compile(
        r"\b\w+\.(?:py|jsonl|json|md|txt)\b|\bvalidator\b|\bchecker\b|\btoolkit\b|"
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
        r"\bgate ruling\b|\bowner gate\b", re.I),
    # S1-05 (ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2 (b)): the ruling's phrasings, verbatim [CWO-EZ-14]
    "author_wave_register_s1_05": re.compile(
        # REG-TF2-1 (ezek_controlling_rulings_a1#e5): the 'former ... span', 'prior ... reading' and rows arms widened to S1's
        # own phrasings, 'rows of' refused, and 'previously held|drafted|spanned|read as' added
        r"\boriginally drafted\b|\bformer (?:[\w.\-–]+ ){0,2}(?:span|row)\b|\bprior [\w:.\-–]+(?: [\w:.\-–]+)? reading\b|"
        r"\bcorrection to an earlier\b|\bpreviously (?:held|drafted|spanned|read) as\b|"
        r"\b(?:preceding|next|following) row\b|\brow (?:before|after)\b|\b(?:one|middle|last) of \w+(?: [\w-]+)? rows\b(?!\s+of\b)|"
        r"\bstrategy['’]s\b|\bthe (?:ruling|order)['’]s\b|\bposture\b|\bofficially[- ]inventoried\b|"
        r"\b(?:ends|opens|closes|begins) the part\b|\bthe part['’]s\b", re.I),
    "staged_file_stem": re.compile(
        r"\bverse_map\w*\b|\bpmarks\w*\b|\bdevice_inventory\b|\boffset_map\b|"
        r"\bconsonantal_index\b|\bTOOLKIT\b|\bezek_lib\b|\bEzek_oshb\w*|\bEzek_web\w*", re.I),
    # TOOLFIX-5 (2): #e9 S2-15 (3)'s arms - a guarded non-possessive 'the strategy' and the CWO-EZ-21 arms
    "strategy_noun": re.compile(r"\bthe strategy\b(?!['’]s)(?!\s+(?:of|to|for|by)\b)", re.I),
    "ledger_id": re.compile(r"\bE-\d{2}\b"),
    "campaign_talk": re.compile(r"\bcampaign\b", re.I),
    # TOOLFIX-5 (2): the six CWO-EZ-22 arms, copied from ezek_controlling_rulings_a1#e10 corpus_wide_orders
    "rule_as_authority": re.compile("\\b(?:per|under|by|within|against) (?:the|a|this|its|that|the same|the book['’]s own) (?:[\\w'’/-]+ ){0,3}?(?:rule|guard|instruction|list-guard|exception|convention)s?\\b", re.I),
    "rule_verb": re.compile("\\b(?:the|a|this|its) (?:[\\w'’/-]+ ){0,3}?rules? (?:requires?|holds?|treats?|bars?|forbids?|applies|fixes|names?|says?|is absolute|admits?|allows?|licen[cs]es?|reserves?|places?|puts?|keeps?|makes?)\\b", re.I),
    "named_rule_or_guard": re.compile("\\b(?:the|a|this|its) (?:standing|governing|granularity|frame-spine(?:['’]s own)?|closed-vocabulary|list-guard|chapter-division|cross-seam|qinah-never-split|refrain-closes-a-unit|operative-category deviation-with-disclosure|structural dateline|cutting|book['’]s own|over-split|under-three-verse|under-3-verse|whole-chapter|complete-unit) (?:rule|guard|cap guard|default|instruction|list-guard|list|exception|allowance|floor)s?\\b", re.I),
    "flagged_guard_talk": re.compile('\\bflagged (?:region|zone|ch\\b|for\\b|in the|doubled-note|\\d)\\w*|\\bregion is flagged\\b|\\bfrontier-flagged\\b|\\bcap guard\\b|\\bzone review\\b|\\blow confidence is expected\\b', re.I),
    "disguised_strategy": re.compile("\\bauthori[sz]ed (?:as an? |exception)|\\bthe (?:one )?authori[sz]ed\\b|\\bexception (?:named|recorded)\\b|\\bnamed exception\\b|\\bover-split guard['’]s\\b|\\bclosed vocabulary\\b|\\bsometimes described as\\b|\\bdisclosed exception\\b", re.I),
    "launch_assignment_staged_actor": re.compile("\\blaunch(?:ed|ing)? (?:message|brief|order)s?\\b|\\bthe assignment\\b|\\bassigned (?:parent )?seam\\b|\\bstaged (?:inventory|extract|file|tools?|map|formula inventory|book-wide sweep)\\b|\\bstaged extract['’]s\\b|\\bdisclosure inventory\\b|\\bdenominator reconciliation\\b|\\bpaseq_tally\\b|\\bthe writer\\b|\\bruled seam\\b|\\bstanding instruction\\b|\\bcap_sweep\\b", re.I),
}
# TOOLFIX-5 (2): the oss arm, applied to observed_substrate_signals elements only
OSS_CLASSES = {"oss_parashah_key": re.compile(r"closure\.(?:parashah_\w+|pe|samekh)\b")}


def rows_from(p: Path):
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix == ".jsonl":
        return [json.loads(l) for l in text.splitlines() if l.strip()]
    data = json.loads(text)
    if isinstance(data, dict):
        return data.get("decisions", [v for v in data.values() if isinstance(v, dict)])
    return data


def content_leaves(row):
    """(field, text) for every content leaf; identity fields are never yielded (#e10 TOOLFIX-5 (1))."""
    for field in CONTENT_STR_FIELDS:
        s = row.get(field)
        if isinstance(s, str):
            yield field, s
    for field in CONTENT_LIST_FIELDS:
        for i, s in enumerate(row.get(field) or []):
            if isinstance(s, str):
                yield "%s[%d]" % (field, i), s


def scan_row(row, fname):
    flags = []
    did = row.get("writer_decision_id") or row.get("decision_id") or "?"
    for field, s in content_leaves(row):
        masked = HEB_RUN.sub(" ", s)
        masked = re.sub(r"“[^”]*”", lambda m: " " * len(m.group(0)), masked)
        classes = dict(CLASSES, **OSS_CLASSES) if field.startswith("observed_substrate_signals[") else CLASSES
        for cls, pat in classes.items():
            for m in pat.finditer(masked):
                flags.append({"file": fname, "decision_id": did,
                              "field": field, "class": cls,
                              "match": m.group(0)[:60],
                              "context": s[max(0, m.start() - 60):m.start() + 80]})
    return flags


def selftest() -> int:
    """TOOLFIX-5 (#e10 ruling TOOLFIX-5 (4)): each new arm fires on a ruled shape and in each widened field; each sanctioned
    form and each identity exemption stays GREEN; the unchanged classes still fire."""
    base = {"decision_id": "P01-001", "writer_decision_id": "P01-001", "writer_part": "p01", "writer_attempt_id": "a",
            "parent_collection": "P1", "span": "Ezek.1.1-Ezek.1.3", "unit_type": "oracle", "confidence": "high",
            "chunk_index_in_book": 1, "boundary_rationale": "", "strongest_rejected_alternative": "", "device_notes": "",
            "literature_type_guess": "", "boundary_evidence_refs": [], "observed_substrate_signals": [],
            "strong_or_hebrew_tags_used": []}

    def row(**kw):
        r = dict(base)
        r.update(kw)
        return r

    fire = [
        ("rule_as_authority", row(device_notes="a close held per the standing rule that a refrain closes the unit")),
        ("rule_verb", row(boundary_rationale="the granularity rule requires a formula-marked seam")),
        ("named_rule_or_guard", row(strongest_rejected_alternative="a two-verse row was rejected as the over-split guard")),
        ("flagged_guard_talk", row(device_notes="this region is flagged for the open question")),
        ("disguised_strategy", row(device_notes="the closed vocabulary names this type")),
        ("launch_assignment_staged_actor", row(boundary_rationale="this seam carries the least formula evidence of the assignment")),
        ("governance_tooling", row(device_notes="the byte text in Ezek_oshb.txt reads so")),
        ("staged_file_stem", row(device_notes="the Ezek_web_clean extract reads so")),
        ("author_wave_register_s1_05", row(device_notes="the officially-inventoried utterance formula")),
        ("strategy_noun", row(boundary_rationale="as the strategy holds, the seam stands")),
        ("ledger_id", row(device_notes="a cap disclosed (E-02)")),
        ("campaign_talk", row(device_notes="the campaign convention is followed")),
        ("oss_parashah_key", row(observed_substrate_signals=["closure.pe"])),
        ("rule_as_authority", row(boundary_evidence_refs=["oshb:Ezek.1.3 (held per the standing rule)"])),
        ("launch_assignment_staged_actor", row(literature_type_guess="oracle, as the writer held")),
        ("staged_file_stem", row(strong_or_hebrew_tags_used=["TOOLKIT"])),
        ("positional_row_reference", row(device_notes="as that row shows")),
        ("strategy_citation", row(device_notes="cited per the strategy file")),
    ]
    green = [
        ("sanctioned: a rule restated as the row's premise", row(boundary_rationale="because a refrain closes the unit before it, both 25:5 and 25:7 are treated as closes")),
        ("sanctioned: the text's own rule", row(boundary_rationale="the prohibition on seizing the people's inheritance (18)")),
        ("sanctioned: default continuation onset", row(device_notes="a default continuation onset stands at 12:1")),
        ("sanctioned: the witness's count layer", row(device_notes="the bytes are unsourceable from this extract")),
        ("sanctioned: a condition in content", row(strongest_rejected_alternative="a messenger formula counts as a row seam only after an addressee change, and none stands here")),
        ("guarded: a descriptive 'the strategy of'", row(boundary_rationale="the strategy of the besieger is narrated at 4:2")),
        ("sanctioned: the inventory's layer", row(device_notes="the inventory does not carry intra-verse position")),
        ("exempt: decision_id and writer_decision_id", row(decision_id="P01-001 per the standing rule", writer_decision_id="P01-001 campaign")),
        ("exempt: writer_part", row(writer_part="p01 the assignment")),
        ("exempt: writer_attempt_id", row(writer_attempt_id="ezek_lib.py E-02")),
        ("exempt: parent_collection", row(parent_collection="P1 this region is flagged")),
        ("exempt: span", row(span="Ezek.1.1-Ezek.1.3 TOOLKIT")),
        ("exempt: unit_type", row(unit_type="the closed vocabulary")),
        ("exempt: confidence", row(confidence="per the standing rule")),
        ("exempt: chunk_index_in_book", row(chunk_index_in_book="the campaign convention")),
    ]
    results = []
    for cls, r in fire:
        got = sorted({f["class"] for f in scan_row(r, "selftest")})
        results.append({"vector": "fires: %s" % cls, "classes": got, "ok": cls in got})
    for name, r in green:
        got = sorted({f["class"] for f in scan_row(r, "selftest")})
        results.append({"vector": "GREEN: %s" % name, "classes": got, "ok": not got})
    failed = [x["vector"] for x in results if not x["ok"]]
    print(json.dumps({"selftest": "check_register TOOLFIX-5", "vectors": len(results), "failed": failed, "results": results,
                      "verdict": "GREEN" if not failed else "RED"}, ensure_ascii=False, indent=1))
    return 0 if not failed else 1


def main() -> int:
    if "--selftest" in sys.argv[1:]:
        return selftest()
    flags = []
    rows_n = 0
    for f in sys.argv[1:]:
        for row in rows_from(Path(f)):
            if not isinstance(row, dict):
                continue
            rows_n += 1
            flags.extend(scan_row(row, Path(f).name))
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
