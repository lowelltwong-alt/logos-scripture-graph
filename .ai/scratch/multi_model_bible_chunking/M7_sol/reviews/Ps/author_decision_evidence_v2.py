#!/usr/bin/env python3
"""Author source-pinned, decision-local Psalm evidence; write no derived sidecars."""
from __future__ import annotations

from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
from typing import Any
import unicodedata
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
GENERATOR = HERE / "corrective_re_review_v2.py"
OUTPUT = HERE / "decision_evidence_v2.jsonl"
spec = importlib.util.spec_from_file_location("psalms_corrective_v2", GENERATOR)
if spec is None or spec.loader is None:
    raise RuntimeError("unable to load Psalm corrective generator")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

CROSSWALK = g.ROOT / ".ai" / "handoffs" / "T544" / "psalms_web_mt_crosswalk.json"
CROSSWALK_SHA256 = "a83b101fe1ad3e36b3aa2282656afd88ba2fd5925b7f5a6e0511a7d5eb56975d"
SOURCE_AUDIT = g.ROOT / ".ai" / "handoffs" / "T544" / "psalms_hebrew_poetics_source_audit.md"
SOURCE_AUDIT_BASIS_END_MARKER = "## Fresh post-repair source-fidelity verdict — 2026-07-24"
SOURCE_AUDIT_PREFIX_BYTE_COUNT = 15570
SOURCE_AUDIT_PREFIX_SHA256 = "9424a48201ea4f643d2771bd71d5aa90a2424e74b7fba7990e82bf3f474a2c98"
SOURCE_AUTHORITY = "translation_versification_metadata_not_boundary_authority"
CHILD_DOCKET = g.ROOT / ".ai" / "handoffs" / "T544" / "psalms_child_ledger_redteam.md"
CHILD_DOCKET_SHA256 = "59f0a82d546e260d1874b1b0e445ea8c7c989cb5882ae99aafe157043e599a08"
CONFIDENCE_DOCKET = g.ROOT / ".ai" / "handoffs" / "T544" / "psalms_confidence_hold_calibration.md"
CONFIDENCE_DOCKET_SHA256 = "0218f986dbc4fffbcb1e0867ac7bacd623e09e904f8c35acf0b8baec1eb0226d"
CHILD_STRUCTURAL_ADVISORY = g.ROOT / ".ai" / "handoffs" / "T544" / "psalms_child_decision_advisory.jsonl"
CHILD_STRUCTURAL_ADVISORY_SHA256 = "94322b5a27e3df1618ae0f168cbcc9e320f5c594174cec4c9571c06f728be5ef"
TRANSLATION_WITNESSES = g.ROOT / "data" / "canonical" / "translations" / "eng-web" / "translation_witnesses.jsonl"
OSIS_NS = "{http://www.bibletechnologies.net/2003/OSIS/namespace}"

NEW_HOLD_IDS = {
    "M7_sol-Ps-050", "M7_sol-Ps-051", "M7_sol-Ps-052", "M7_sol-Ps-053",
    "M7_sol-Ps-090", "M7_sol-Ps-091",
}
NEW_HOLD_QUESTIONS = {
    "ps37_child_granularity": "Do the topical transitions at Ps 37:12, 21, and 32 warrant separately retrievable children under the alphabetic parent, or should the continuous acrostic wisdom poem remain the only stable unit?",
    "ps59_recurrence_architecture": "Should Psalm 59 be retained only as a whole parent, or should children follow the recurrent 1-5 / 6-13 / 14-17 cycle rather than the present 1-9 / 10-17 division?",
}
LITERARY_CHILD_CHALLENGES = {
    (18,20,30),(19,7,11),(24,3,6),(31,19,24),(35,11,18),(37,12,20),(40,11,17),(44,17,26),
    (49,5,12),(51,13,19),(55,9,15),(59,1,9),(62,5,8),(67,4,5),(68,19,27),(69,19,28),
    (71,14,24),(73,18,22),(74,12,17),(77,10,15),(78,32,39),(78,56,64),(80,8,19),(81,6,10),
    (83,9,18),(89,46,48),(90,7,12),(94,12,15),(99,4,5),(102,23,28),(104,19,23),(107,43,43),
    (109,6,20),(110,4,7),(118,19,29),(135,1,4),(136,26,26),(137,5,6),(139,19,22),(144,9,11),
    (145,14,21),(147,7,11),
}
CANONICAL_CHALLENGE_PSALMS = {2,9,10,22,41,42,43,45,72,82,89,95,102,106,108,110,114,115,116,118,132,145,147,148}
ACROSTIC_CANDIDATES = {9,10,25,34,37,111,112,119,145}
REFRAIN_REFS = {
    42:["WEB:Ps.42.5","WEB:Ps.42.11","WEB:Ps.43.5"],
    43:["WEB:Ps.42.5","WEB:Ps.42.11","WEB:Ps.43.5"],
    46:["WEB:Ps.46.7","WEB:Ps.46.11"],
    57:["WEB:Ps.57.5","WEB:Ps.57.11"],
    59:["WEB:Ps.59.9","WEB:Ps.59.16","WEB:Ps.59.17"],
    62:["WEB:Ps.62.1","WEB:Ps.62.2","WEB:Ps.62.5","WEB:Ps.62.6"],
    67:["WEB:Ps.67.3","WEB:Ps.67.5"],
    80:["WEB:Ps.80.3","WEB:Ps.80.7","WEB:Ps.80.19"],
    107:["WEB:Ps.107.6","WEB:Ps.107.13","WEB:Ps.107.19","WEB:Ps.107.28"],
    136:[f"WEB:Ps.136.{verse}" for verse in range(1,27)],
}
RELATION_CODES = {
    9:["PS09_PS10_IRREGULAR_ALPHABETIC_PRESSURE","LXX_WITNESS_GAP"],
    10:["PS09_PS10_IRREGULAR_ALPHABETIC_PRESSURE","LXX_WITNESS_GAP"],
    41:["CLOSING_BLESSING_DOUBLE_AMEN"],
    42:["PS42_PS43_VARIANT_REFRAIN"],
    43:["PS42_PS43_VARIANT_REFRAIN"],
    72:["BLESSING_DOUBLE_AMEN_DAVIDIC_PRAYERS_COLOPHON"],
    89:["CLOSING_BLESSING_AMEN"],
    95:["HEBREW_SYNTAX_CROSSES_WEB_95_7_8"],
    106:["CLOSING_BLESSING_AMEN"],
    108:["WEB_PS57_PS60_REUSE_RELATION"],
    110:["YHWH_OATH_AT_WEB_110_4"],
    114:["LXX_WITNESS_GAP"],
    115:["LXX_WITNESS_GAP"],
    116:["LXX_WITNESS_GAP"],
    118:["GATE_PROCESSION_MOVEMENT"],
    119:["EIGHT_VERSE_INITIAL_CONSONANT_BLOCK"],
    132:["DAVID_TO_YHWH_AND_YHWH_TO_DAVID_OATH_PAIR"],
    145:["INCOMPLETE_ACROSTIC_MISSING_NUN_LINE"],
    147:["RENEWED_PRAISE_SUMMONS","LXX_WITNESS_GAP"],
    148:["HEAVEN_TO_EARTH_SUMMONS_AT_WEB_148_7"],
}
HEBREW_LETTERS = list("אבגדהוזחטיכלמנסעפצקרשת")
CHILD_CASES = HERE / "child_decision_cases_v3.json"
CHILD_CASES_SHA256 = '17c073fa26847db172fd660e2fceaff7b26558d222b739e202418d43e1c2cef7'

def words(value: str) -> str:
    return value.replace("_", " ")


def web_ref(psalm: int, verse: int) -> str:
    return f"WEB:Ps.{psalm}.{verse}"


def bare_ref(psalm: int, verse: int) -> str:
    return f"Ps.{psalm}.{verse}"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_prose(value: str) -> str:
    cleaned = value.translate(str.maketrans({"\"": "", "“": "", "”": ""}))
    return cleaned.replace("`", "").replace("**", "").strip()


def source_audit_prefix() -> bytes:
    raw = SOURCE_AUDIT.read_bytes()
    marker = SOURCE_AUDIT_BASIS_END_MARKER.encode("utf-8")
    offset = raw.find(marker)
    if offset < 0:
        raise RuntimeError("Psalm source-audit basis-end marker is missing")
    prefix = raw[:offset]
    if len(prefix) != SOURCE_AUDIT_PREFIX_BYTE_COUNT or hashlib.sha256(prefix).hexdigest() != SOURCE_AUDIT_PREFIX_SHA256:
        raise RuntimeError("Psalm source-audit immutable prefix changed")
    return prefix


def load_child_docket() -> dict[int,dict[str,Any]]:
    if file_sha256(CHILD_DOCKET) != CHILD_DOCKET_SHA256:
        raise RuntimeError("Psalm child red-team docket hash changed")
    rows: dict[int,dict[str,Any]] = {}
    pattern = re.compile(r"^\| (\d+) / `([0-9]{3})–([0-9]{3})` \| (.*?) \| (.*?) \|$", re.MULTILINE)
    for match in pattern.finditer(CHILD_DOCKET.read_text(encoding="utf-8")):
        psalm = int(match.group(1))
        rows[psalm] = {
            "decision_start": int(match.group(2)),
            "decision_end": int(match.group(3)),
            "evidence": audit_prose(match.group(4)),
            "advisory": audit_prose(match.group(5)),
        }
    if len(rows) != 49:
        raise RuntimeError(f"Psalm child docket must expose 49 split-Psalm rows, found {len(rows)}")
    return rows


def load_confidence_overrides() -> dict[str,dict[str,str]]:
    if file_sha256(CONFIDENCE_DOCKET) != CONFIDENCE_DOCKET_SHA256:
        raise RuntimeError("Psalm confidence docket hash changed")
    overrides: dict[str,dict[str,str]] = {}
    pattern = re.compile(
        r"^\| `(M7_sol-Ps-[0-9]{3})` \| .*? -> (high|medium_low|medium|low)(?: (?:held|accepted))? \| (.*?) \|$",
        re.MULTILINE,
    )
    for match in pattern.finditer(CONFIDENCE_DOCKET.read_text(encoding="utf-8")):
        overrides[match.group(1)] = {"tier": match.group(2), "basis": audit_prose(match.group(3))}
    if len(overrides) != 46:
        raise RuntimeError(f"Psalm confidence docket must expose 46 decision-local changes, found {len(overrides)}")
    return overrides


def load_child_structural_advisory() -> dict[str,dict[str,Any]]:
    if file_sha256(CHILD_STRUCTURAL_ADVISORY) != CHILD_STRUCTURAL_ADVISORY_SHA256:
        raise RuntimeError("Psalm child structural advisory hash changed")
    allowed_flags = {"R","H","RC"}
    sanitized: dict[str,dict[str,Any]] = {}
    for line in CHILD_STRUCTURAL_ADVISORY.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        raw = json.loads(line)
        decision_id = raw["decision_id"]
        selected = {
            "decision_id":decision_id,
            "span":raw["span"],
            "psalm":raw["psalm"],
            "child_literary_form":raw["child_literary_form"],
            "deciding_boundary_refs":raw["deciding_boundary_refs"],
            "exact_web_observation_refs":raw["exact_web_observation_refs"],
            "rejected_alternative_merge_span":raw["rejected_alternative_merge_span"],
            "advisory":raw["advisory"],
        }
        forbidden_approvals = (
            raw.get("authorizes_m7_change") is not False,
            raw.get("bespoke_prose_approved") is not False,
            raw.get("copy_into_m7_final_fields_permitted") is not False,
        )
        if raw["advisory"] not in allowed_flags or any(forbidden_approvals):
            raise RuntimeError(f"unsafe structural advisory row: {decision_id}")
        sanitized[decision_id] = selected
    if len(sanitized) != 182:
        raise RuntimeError(f"Psalm structural advisory must expose 182 rows, found {len(sanitized)}")
    return sanitized

def load_crosswalk() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    if file_sha256(CROSSWALK) != CROSSWALK_SHA256:
        raise RuntimeError("Psalm crosswalk hash changed")
    source_audit_prefix()
    data = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    if data["authority"] != SOURCE_AUTHORITY:
        raise RuntimeError("crosswalk authority changed")
    if data["summary"]["mapped_verse_count"] != 2461:
        raise RuntimeError("crosswalk coverage changed")
    by_ref = {row["web_ref"]: row for row in data["verse_mapping"]}
    if len(by_ref) != 2461:
        raise RuntimeError("crosswalk references are not unique")
    return data, by_ref


def load_canonical_web_verses() -> dict[tuple[int,int],str]:
    verses: dict[tuple[int,int],str] = {}
    for line in TRANSLATION_WITNESSES.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        match = re.fullmatch(r"Ps\.(\d+)\.(\d+)", row.get("osis_ref",""))
        if match:
            verses[tuple(map(int,match.groups()))] = row["text"]
    if len(verses) != 2461:
        raise RuntimeError("canonical WEB witness must contain 2461 Psalm verses")
    return verses


def load_hebrew_words() -> tuple[dict[str,list[str]], dict[str,list[str]]]:
    oshb: dict[str,list[str]] = {}
    for verse in ET.parse(g.OSH).getroot().iter(OSIS_NS + "verse"):
        oshb[verse.attrib["osisID"]] = [
            "".join(word.itertext()).strip()
            for word in verse.iter(OSIS_NS + "w")
            if "".join(word.itertext()).strip()
        ]
    uxlc: dict[str,list[str]] = {}
    for chapter in ET.parse(g.UXLC).getroot().iter("c"):
        psalm = int(chapter.attrib["n"])
        for verse in chapter.findall("v"):
            uxlc[f"Ps.{psalm}.{int(verse.attrib['n'])}"] = [
                "".join(word.itertext()).strip()
                for word in verse.iter("w")
                if "".join(word.itertext()).strip()
            ]
    return oshb, uxlc


def consonants(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value)
    return "".join(ch for ch in normalized if "\u05d0" <= ch <= "\u05ea")


def first_consonant(value: str) -> str:
    chars = consonants(value)
    return chars[0] if chars else ""


def mapped_rows(psalm: int, start: int, end: int, crosswalk: dict[str,dict[str,Any]]) -> list[dict[str,Any]]:
    rows = []
    for verse in range(start,end+1):
        raw = crosswalk[bare_ref(psalm,verse)]
        rows.append({
            "web_ref": web_ref(psalm,verse),
            "verification_basis": raw["verification_basis"],
            "mt_oshb_ref": raw["mt_oshb_ref"],
            "oshb_segment_locator": f"OSHB:Ps.xml#{raw['oshb_segment_locator']}",
            "mt_uxlc_ref": raw["mt_uxlc_ref"],
            "uxlc_locator": f"UXLC:Ps.xml#{raw['mt_uxlc_ref']}",
            "mt_verse_offset": raw["mt_verse_offset"],
            "uxlc_target_exists": raw["uxlc_target_exists"],
        })
    return rows


def alignment_for(psalm: int, start: int, end: int, crosswalk: dict[str,dict[str,Any]]) -> dict[str,Any]:
    rows = mapped_rows(psalm,start,end,crosswalk)
    return {
        "web_mt_crosswalk_status":"verified_candidate_mapping",
        "crosswalk_artifact_id":"T544_PS_WEB_MT_V1",
        "crosswalk_sha256":CROSSWALK_SHA256,
        "source_audit_lineage":{
            "path":SOURCE_AUDIT.relative_to(g.ROOT).as_posix(),
            "basis_end_marker":SOURCE_AUDIT_BASIS_END_MARKER,
            "prefix_byte_count":SOURCE_AUDIT_PREFIX_BYTE_COUNT,
            "prefix_sha256":SOURCE_AUDIT_PREFIX_SHA256,
            "appended_verdict_treated_separately":True,
        },
        "authority":SOURCE_AUTHORITY,
        "basis_counts":dict(Counter(row["verification_basis"] for row in rows)),
        "mt_verse_offsets":sorted({row["mt_verse_offset"] for row in rows}),
        "ordered_verse_mapping":rows,
        "greek_lxx_source_available":False,
        "selah_boundary_authority":False,
        "locator_existence_is_not_boundary_evidence":True,
    }


def neighbor_facts(psalm: int, start: int, end: int, form: str) -> dict[str,Any]:
    units = g.SPLITS.get(psalm)
    if not units:
        return {"decision_kind":"whole_psalm","left":None,"right":None}
    position = units.index((start,end))
    left = None
    right = None
    if position:
        ls,le = units[position-1]
        left = {"span":g.span(psalm,ls,le),"form":g.CHILD_FORMS[(psalm,ls,le)],"terminal_ref":web_ref(psalm,le)}
    if position + 1 < len(units):
        rs,re_ = units[position+1]
        right = {"span":g.span(psalm,rs,re_),"form":g.CHILD_FORMS[(psalm,rs,re_)],"opening_ref":web_ref(psalm,rs)}
    return {"decision_kind":"child_unit","left":left,"right":right}


def _case_tokens(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+",value.lower())


def _masked_case_fingerprint(case: dict[str,Any], value: str) -> str:
    masked = value.lower()
    slots = [
        case["decision_id"],case["span"],case["competing_span"],case["parent_span"],
        case["local_function"].replace("_"," "),case["specialist_advisory_flag"],
        *[item["claim"] for item in case["selected_adjacent_seams"]],
    ]
    for slot in sorted(slots,key=len,reverse=True):
        masked = masked.replace(slot.lower()," <slot> ")
    masked = re.sub(r"(?:web:)?ps\.\d+(?:\.\d+)?(?:-ps\.\d+\.\d+)?"," <ref> ",masked)
    masked = re.sub(r"\b(?:aleph|beth|gimel|daleth|he|waw|zayin|heth|teth|yodh|kaph|lamedh|mem|nun|samekh|ayin|pe|tsadhe|qoph|resh|shin|taw)\b"," <letter> ",masked)
    masked = re.sub(r"[`\"“”][^`\"“”]*[`\"“”]"," <quote> ",masked)
    return " ".join(re.findall(r"[a-z<>]+",masked))


def load_child_decision_cases() -> dict[str,dict[str,Any]]:
    if file_sha256(CHILD_CASES) != CHILD_CASES_SHA256:
        raise RuntimeError("Psalm child decision-case artifact hash changed")
    cases = json.loads(CHILD_CASES.read_text(encoding="utf-8"))
    if len(cases) != 182 or set(cases) != {key for key in cases if re.fullmatch(r"M7_sol-Ps-[0-9]{3}",key)}:
        raise RuntimeError("Psalm child decision-case artifact must contain 182 keyed rows")
    structural = load_child_structural_advisory()
    advisory_raw = {
        row["decision_id"]:row
        for row in map(json.loads,CHILD_STRUCTURAL_ADVISORY.read_text(encoding="utf-8").splitlines())
    }
    fingerprint_fields = {
        "boundary_rationale":lambda case:case["boundary_rationale"],
        "rejected_alternative":lambda case:case["rejected_alternative"],
        "confidence_basis.prose":lambda case:case["confidence_basis"]["prose"],
        "challenge_response.answer":lambda case:case["challenge_response"]["answer"],
    }
    fingerprints: dict[str,dict[str,str]] = {field:{} for field in fingerprint_fields}
    for decision_id,case in cases.items():
        if case["decision_id"] != decision_id or case["schema_version"] != "m7_psalms_child_decision_case.v3":
            raise RuntimeError(f"Psalm child decision-case identity mismatch: {decision_id}")
        provenance = case["provenance"]
        required_false = (
            "structural_advisory_prose_used",
            "advisory_bespoke_prose_approved",
            "advisory_copy_into_m7_final_fields_permitted",
            "advisory_authorizes_m7_change",
        )
        if any(provenance.get(field) is not False for field in required_false):
            raise RuntimeError(f"Psalm child decision case imports unauthorized advisory prose: {decision_id}")
        raw = structural[decision_id]
        if case["specialist_advisory_flag"] != raw["advisory"] or case["competing_span"] != raw["rejected_alternative_merge_span"]:
            raise RuntimeError(f"Psalm child structural flag/merge mismatch: {decision_id}")
        expected_observations = list(raw['exact_web_observation_refs'])
        if decision_id == 'M7_sol-Ps-167':
            expected_observations.append('Ps.95.6')
        if case['structural_observation_refs'] != expected_observations:
            raise RuntimeError(f'Psalm child structural observation mismatch: {decision_id}')
        if case["structural_advisory_original_span"] != raw["span"] or case["structural_advisory_original_boundary_refs"] != raw["deciding_boundary_refs"]:
            raise RuntimeError(f"Psalm child advisory-original context mismatch: {decision_id}")
        current_refs = [item["refs"] for item in case["selected_adjacent_seams"]]
        if decision_id not in {"M7_sol-Ps-166","M7_sol-Ps-167"} and current_refs != raw["deciding_boundary_refs"]:
            raise RuntimeError(f"Psalm child current edge mismatch: {decision_id}")
        if case["boundary_rationale"] in case["rejected_alternative"]:
            raise RuntimeError(f"Psalm child alternative contains full rationale: {decision_id}")
        confidence = case["confidence_basis"]
        if confidence["prose"] == case["boundary_rationale"] or confidence.get("status_not_used_as_input") is not True:
            raise RuntimeError(f"Psalm child confidence is not independent: {decision_id}")
        if any(not confidence.get(field) for field in ("marker","corroboration","alternative_strength","prose")):
            raise RuntimeError(f"Psalm child confidence dimensions incomplete: {decision_id}")
        response = case["challenge_response"]
        challenge = response.get("exact_challenge",{})
        if challenge.get("current_span") != case["span"] or challenge.get("competing_span") != case["competing_span"] or challenge.get("specialist_flag") != case["specialist_advisory_flag"] or not response.get("answer"):
            raise RuntimeError(f"Psalm child challenge response incomplete: {decision_id}")
        if case["specialist_advisory_flag"] in {"H","RC"} and (not response.get("question") or len(response.get("options",[])) < 2):
            raise RuntimeError(f"Psalm child H/RC response lacks exact question/options: {decision_id}")
        advisory_words = _case_tokens(advisory_raw[decision_id]["child_specific_rationale"]+" "+advisory_raw[decision_id]["alternative_disposition_reason"])
        advisory_ngrams = {tuple(advisory_words[index:index+8]) for index in range(len(advisory_words)-7)}
        for field,get_value in fingerprint_fields.items():
            value = get_value(case)
            fingerprint = _masked_case_fingerprint(case,value)
            if fingerprint in fingerprints[field]:
                raise RuntimeError(f"Psalm child repeated semantic fingerprint in {field}: {fingerprints[field][fingerprint]} and {decision_id}")
            fingerprints[field][fingerprint] = decision_id
            words_ = _case_tokens(value)
            if any(tuple(words_[index:index+8]) in advisory_ngrams for index in range(len(words_)-7)):
                raise RuntimeError(f"Psalm child copies an advisory prose 8-gram in {field}: {decision_id}")
    return cases


CHILD_DECISION_CASES = load_child_decision_cases()

def local_case(
    decision_id: str,
    psalm: int,
    start: int,
    end: int,
    form: str,
    parent: str,
    lengths: dict[int,int],
    child_docket: dict[int,dict[str,Any]],
) -> tuple[dict[str,Any],str,str,dict[str,Any]]:
    span = g.span(psalm,start,end)
    facts = neighbor_facts(psalm,start,end,form)
    marker = {
        "span":span,"form":form,"parent_form":parent,
        "opening_ref":web_ref(psalm,start),"closing_ref":web_ref(psalm,end),
        "left_neighbor":facts["left"],"right_neighbor":facts["right"],
    }
    if facts["decision_kind"] == "whole_psalm":
        rationale,rival = g.WHOLE_AUDITS[psalm]
        rationale,rival = audit_prose(rationale),audit_prose(rival)
        if psalm == 115:
            rival = "Verse 9 starts the trust litany and verse 12 starts blessing. A proposed combined-numbering relation lacks a scoped Greek/LXX witness and cannot decide the WEB boundary."
        elif psalm == 116:
            rival = "Verse 12 starts the testimony-to-vow alternative. A proposed alternate-numbering split lacks a scoped Greek/LXX witness and remains evidence-only."
        basis = {"decision_kind":"whole_psalm","retrieval_choice":span,"tested_internal_alternative":True}
        return marker,rationale,rival,basis

    case = CHILD_DECISION_CASES[decision_id]
    docket = child_docket[psalm]
    basis = {
        "decision_kind":"child_unit",
        "retrieval_choice":span,
        "parent_retained":case["parent_span"],
        "form_transition":facts,
        "selected_adjacent_seams":case["selected_adjacent_seams"],
        "competing_span":case["competing_span"],
        "decision_case_registry":"CHILD_DECISION_CASES",
        "decision_case_artifact":{
            "path":CHILD_CASES.relative_to(g.ROOT).as_posix(),
            "sha256":CHILD_CASES_SHA256,
            "final_fields_copied_verbatim":["boundary_rationale","rejected_alternative","confidence_basis","challenge_response"],
        },
        "independent_structural_advisory":{
            "path":CHILD_STRUCTURAL_ADVISORY.relative_to(g.ROOT).as_posix(),
            "sha256":CHILD_STRUCTURAL_ADVISORY_SHA256,
            "current_deciding_boundary_refs":[item["refs"] for item in case["selected_adjacent_seams"]],
            "advisory_original_span":case["structural_advisory_original_span"],
            "advisory_original_boundary_refs":case["structural_advisory_original_boundary_refs"],
            "exact_web_observation_refs":case["structural_observation_refs"],
            "rejected_alternative_merge_span":case["competing_span"],
            "advisory":case["specialist_advisory_flag"],
            "prose_imported":False,
            "bespoke_prose_approved":False,
            "copy_into_m7_final_fields_permitted":False,
            "authorizes_m7_change":False,
        },
        "redteam_docket":{
            "path":CHILD_DOCKET.relative_to(g.ROOT).as_posix(),
            "sha256":CHILD_DOCKET_SHA256,
            "decision_range":[docket["decision_start"],docket["decision_end"]],
            "use":"provenance_only_not_copied_as_decision_prose",
        },
    }
    return marker,case["boundary_rationale"],case["rejected_alternative"],basis

def source_observations(psalm: int, start: int, end: int, length: int, verses: dict[tuple[int,int],str]) -> list[dict[str,str]]:
    refs: list[tuple[int,str]] = [(start,"opening_witness")]
    if end != start:
        refs.append((end,"closing_witness"))
    if start > 1:
        refs.append((start-1,"left_context"))
    if end < length:
        refs.append((end+1,"right_context"))
    seen: set[int] = set()
    result = []
    for verse,use in refs:
        if verse in seen:
            continue
        seen.add(verse)
        result.append({"ref":web_ref(psalm,verse),"text":verses[(psalm,verse)],"extent":"complete_verse","use":use})
    return result


def segment_initial(psalm: int, verse: int, crosswalk: dict[str,dict[str,Any]], oshb: dict[str,list[str]]) -> str:
    row = crosswalk[bare_ref(psalm,verse)]
    index = int(row["oshb_word_start"]) - 1
    return first_consonant(oshb[row["mt_oshb_ref"]][index])


def mapped_feature_segment(
    psalm: int,
    verse: int,
    crosswalk: dict[str,dict[str,Any]],
    oshb: dict[str,list[str]],
    uxlc: dict[str,list[str]],
    *,
    role: str,
    word_start: int | None = None,
    word_end: int | None = None,
) -> dict[str,Any]:
    row = crosswalk[bare_ref(psalm,verse)]
    start_word = int(row["oshb_word_start"]) if word_start is None else word_start
    end_word = int(row["oshb_word_end"]) if word_end is None else word_end
    oshb_words = oshb[row["mt_oshb_ref"]][start_word-1:end_word]
    uxlc_words = uxlc[row["mt_uxlc_ref"]][start_word-1:end_word]
    oshb_text = " ".join(oshb_words)
    uxlc_text = " ".join(uxlc_words)
    locator_suffix = f"{row['mt_oshb_ref']}#w{start_word}-w{end_word}"
    normalized_oshb = consonants(oshb_text)
    normalized_uxlc = consonants(uxlc_text)
    return {
        "role":role,
        "web_ref":web_ref(psalm,verse),
        "mt_oshb_ref":row["mt_oshb_ref"],
        "mt_uxlc_ref":row["mt_uxlc_ref"],
        "oshb_segment_locator":f"OSHB:Ps.xml#{locator_suffix}",
        "uxlc_segment_locator":f"UXLC:Ps.xml#{row['mt_uxlc_ref']}#w{start_word}-w{end_word}",
        "witnesses":[
            {"witness_id":"openscriptures_oshb","witness_name":"Open Scriptures Hebrew Bible","source_ref":row["mt_oshb_ref"],"segment_locator":f"OSHB:Ps.xml#{locator_suffix}","observed_text":oshb_text,"normalized_consonants":normalized_oshb},
            {"witness_id":"tanach_us_uxlc","witness_name":"Unicode/XML Leningrad Codex","source_ref":row["mt_uxlc_ref"],"segment_locator":f"UXLC:Ps.xml#{row['mt_uxlc_ref']}#w{start_word}-w{end_word}","observed_text":uxlc_text,"normalized_consonants":normalized_uxlc},
        ],
        "normalization":{
            "unicode_form":"NFD",
            "operations":["remove Hebrew combining marks including vowel points and cantillation","omit OSHB morpheme separators and non-Hebrew punctuation","preserve consonant and word order"],
            "comparison_result":"matching_consonant_sequence" if normalized_oshb == normalized_uxlc else "variant_consonant_sequence",
        },
    }

def poetic_features(psalm: int, start: int, end: int, verses: dict[tuple[int,int],str], crosswalk: dict[str,dict[str,Any]], oshb: dict[str,list[str]], uxlc: dict[str,list[str]]) -> list[dict[str,Any]]:
    features: list[dict[str,Any]] = []
    if psalm == 119:
        index = (start-1)//8
        expected = HEBREW_LETTERS[index]
        oshb_initials = [segment_initial(psalm,verse,crosswalk,oshb) for verse in range(start,end+1)]
        uxlc_initials = [first_consonant(uxlc[crosswalk[bare_ref(psalm,verse)]["mt_uxlc_ref"]][0]) for verse in range(start,end+1)]
        if oshb_initials != [expected]*8 or uxlc_initials != [expected]*8:
            raise RuntimeError(f"Psalm 119 initial verification failed at {start}-{end}")
        features.append({
            "kind":"eight_verse_initial_consonant_block","letter_name":g.HEBREW_LETTERS[index],"consonant":expected,
            "oshb_initials":oshb_initials,"uxlc_initials":uxlc_initials,"heading_element_claimed":False,
            "web_refs":[web_ref(psalm,verse) for verse in range(start,end+1)],
        })
    elif psalm in {9,10}:
        features.append({
            "kind":"irregular_alphabetic_pressure","observed_mapped_oshb_initials":[segment_initial(psalm,verse,crosswalk,oshb) for verse in range(start,end+1)],
            "paired_coordinate":"Ps.10" if psalm == 9 else "Ps.9","regular_complete_sequence_claimed":False,
        })
    elif psalm == 145:
        initials = [segment_initial(psalm,verse,crosswalk,oshb) for verse in range(start,end+1)]
        features.append({
            "kind":"incomplete_alphabetic_praise","mapped_oshb_initials":initials,
            "nun_line_present":False,"greek_repair_claimed":False,
            "title_prefix_excluded_by_segment_mapping":start == 1,
        })
    elif psalm in ACROSTIC_CANDIDATES:
        features.append({"kind":"acrostic_candidate","verification_status":"decision_local_pattern_not_adjudicated"})
    if psalm in {42,43}:
        mapped = [crosswalk[ref_.replace("WEB:","")] for ref_ in REFRAIN_REFS[psalm]]
        texts = {f"OSHB:{row['mt_oshb_ref']}":" ".join(oshb[row["mt_oshb_ref"]]) for row in mapped}
        normalized = [consonants(text) for text in texts.values()]
        features.append({
            "kind":"variant_refrain","web_refs":REFRAIN_REFS[psalm],
            "mapped_oshb_segments":[f"OSHB:Ps.xml#{row['oshb_segment_locator']}" for row in mapped],
            "oshb_text":texts,"comparison":["variant" if normalized[0] != normalized[1] else "matching","matching" if normalized[1] == normalized[2] else "variant"],
        })
    elif psalm in REFRAIN_REFS:
        features.append({"kind":"refrain_pattern","web_refs":REFRAIN_REFS[psalm],"verification_scope":"WEB_complete_verses"})
    selah_refs = [web_ref(psalm,verse) for verse in range(start,end+1) if "Selah" in verses[(psalm,verse)]]
    if selah_refs:
        features.append({"kind":"selah_lexical_token","web_refs":selah_refs,"boundary_authority":False})
    if psalm == 95:
        features.append({
            "kind":"cross_verse_hebrew_syntax",
            "web_refs":[web_ref(95,7),web_ref(95,8)],
            "segments":[
                mapped_feature_segment(95,7,crosswalk,oshb,uxlc,role="hearing_condition",word_start=9,word_end=12),
                mapped_feature_segment(95,8,crosswalk,oshb,uxlc,role="conditioned_prohibition",word_start=1,word_end=3),
            ],
            "syntactic_observation":"The verse-7 hearing condition is completed by the verse-8 prohibition; the auditable seam is 6/7, not 7/8.",
            "supported_seam":"WEB:Ps.95.6/WEB:Ps.95.7",
            "rejected_seam":"WEB:Ps.95.7/WEB:Ps.95.8",
            "normalization_scope":"consonantal comparison only; syntax is assessed on the named vocalized witnesses",
        })
    if psalm == 110:
        features.append({
            "kind":"mapped_boundary_oath_formula",
            "web_refs":[web_ref(110,3),web_ref(110,4)],
            "chunk_web_refs":[web_ref(110,verse) for verse in range(start,end+1)],
            "segments":[
                mapped_feature_segment(110,3,crosswalk,oshb,uxlc,role="left_boundary_context"),
                mapped_feature_segment(110,4,crosswalk,oshb,uxlc,role="oath_formula",word_start=1,word_end=2),
            ],
            "mapped_boundary_context":{"seam":"WEB:Ps.110.3/WEB:Ps.110.4","context_ref":web_ref(110,4),"context_outside_chunk_alignment":not (start <= 4 <= end),"context_is_separately_mapped":True},
            "lexical_observation":"The mapped verse-4 opening is the Yahweh oath formula and follows the verse-3 royal oracle context.",
            "normalization_scope":"dual-witness vocalized text retained; consonantal equivalence checked after declared normalization",
        })
    if psalm == 132:
        features.append({
            "kind":"mapped_directional_oath_pair",
            "web_refs":[web_ref(132,2),web_ref(132,11)],
            "segments":[
                mapped_feature_segment(132,2,crosswalk,oshb,uxlc,role="david_swears_to_yahweh",word_start=1,word_end=3),
                mapped_feature_segment(132,11,crosswalk,oshb,uxlc,role="yahweh_swears_to_david",word_start=1,word_end=3),
            ],
            "lexical_observation":"The two mapped oath segments reverse the oath direction from David-to-Yahweh to Yahweh-to-David within the covenant prayer.",
            "normalization_scope":"dual-witness vocalized text retained; consonantal equivalence checked after declared normalization",
        })
    if psalm in {9,10,114,115,116,147}:
        features.append({"kind":"numbering_metadata_pressure","source_status":"unresolved_no_scoped_greek_lxx_witness"})
    return features


def hebrew_review(psalm: int, start: int, end: int, features: list[dict[str,Any]], alignment: dict[str,Any]) -> dict[str,Any]:
    span = g.span(psalm,start,end)
    if psalm == 119:
        feature = next(item for item in features if item["kind"] == "eight_verse_initial_consonant_block")
        claim = f"{span}: both Hebrew witnesses verify eight {feature['letter_name']} initials ({feature['consonant'] * 8}); no heading element is asserted."
        return {"verdict":"supports","signal_code":"PS119_VERSE_INITIALS","claim":claim,"feature_kind":feature["kind"],"counterevidence_code":"WHOLE_PSALM_PARENT_REMAINS"}
    if psalm == 95:
        claim = (
            f"{span}: mapped MT 95:7-8 continues the hearing condition into the prohibition; the 6/7 seam survives, while 7/8 does not."
        )
        return {"verdict":"supports","signal_code":"PS95_CROSS_VERSE_SYNTAX","claim":claim,"feature_kind":"cross_verse_hebrew_syntax","counterevidence_code":"WHOLE_HYMN_ORACLE_CONTINUITY"}
    if psalm in {42,43}:
        claim = f"{span}: the mapped refrain recurs across WEB 42:5, 42:11, and 43:5 with variation; linked-parent pressure challenges isolated treatment."
        return {"verdict":"challenge","signal_code":"PS42_43_VARIANT_REFRAIN","claim":claim,"feature_kind":"variant_refrain","counterevidence_code":"WEB_COORDINATES_REMAIN_DISTINCT"}
    if psalm in {9,10}:
        claim = f"{span}: mapped initials show irregular alphabetic pressure across Psalms 9-10, but neither a complete sequence nor a required merger is established."
        return {"verdict":"challenge","signal_code":"PS09_10_IRREGULAR_ACROSTIC","claim":claim,"feature_kind":"irregular_alphabetic_pressure","counterevidence_code":"IRREGULAR_PATTERN_AND_LXX_GAP"}
    if psalm == 145:
        claim = f"{span}: mapped content initials continue an incomplete acrostic and skip nun before samekh; the alphabetic parent challenges child independence."
        return {"verdict":"challenge","signal_code":"PS145_INCOMPLETE_ACROSTIC","claim":claim,"feature_kind":"incomplete_alphabetic_praise","counterevidence_code":"FUNCTIONAL_MOVEMENTS_REMAIN_RETRIEVABLE"}
    if psalm == 110:
        feature = next(item for item in features if item["kind"] == "mapped_boundary_oath_formula")
        claim = f"{span}: the named OSHB and UXLC segments bind the WEB 110:3/4 boundary context to the verse-4 Yahweh oath opening; context outside a child is separately mapped rather than borrowed from its alignment."
        return {"verdict":"supports","signal_code":"PS110_YHWH_OATH","claim":claim,"feature_kind":feature["kind"],"counterevidence_code":"COMPLETE_PSALM_PARENT_REMAINS"}
    if psalm == 132:
        feature = next(item for item in features if item["kind"] == "mapped_directional_oath_pair")
        claim = f"{span}: named OSHB and UXLC segments map the verse-2 David-to-Yahweh oath and verse-11 Yahweh-to-David oath as a directional response pair."
        return {"verdict":"supports","signal_code":"PS132_PAIRED_OATHS","claim":claim,"feature_kind":feature["kind"],"counterevidence_code":"COVENANT_PRAYER_REMAINS_ONE_PARENT"}
    return {
        "verdict":"insufficient_evidence","signal_code":"NO_ADJUDICATED_HEBREW_BOUNDARY_SIGNAL",
        "claim":None,"feature_kind":None,
        "gap":{
            "locator_status":alignment["web_mt_crosswalk_status"],
            "observation_status":"decision_local_hebrew_poetics_not_adjudicated",
            "locator_alone_is_evidence":False,
        },
    }


def confidence_for(
    decision_id: str,
    psalm: int,
    start: int,
    end: int,
    length: int,
    evidence_rationale: str,
    alternative_rationale: str,
    overrides: dict[str,dict[str,str]],
) -> tuple[str,dict[str,Any]]:
    whole = start == 1 and end == length
    override = overrides.get(decision_id)
    if override:
        tier = override["tier"]
        rationale = override["basis"]
        tier_rule = "explicit_decision_local_calibration"
        marker_strength = "calibrated_from_named_WEB_or_mapped_feature"
        directness = "decision_specific_calibration_observation"
    elif psalm == 119:
        tier = "high"
        rationale = evidence_rationale
        tier_rule = "dual_witness_formal_sequence"
        marker_strength = "eight_matching_initials_in_each_named_witness"
        directness = "exact_verse_initial_observation"
    elif not whole:
        tier = "medium"
        rationale = evidence_rationale
        tier_rule = "source_local_child_seam"
        marker_strength = "one_or_two_observed_adjacent_transitions"
        directness = "canonical_WEB_boundary_observation"
    elif psalm in g.MEDIUM_WHOLE_PSALMS:
        tier = "medium"
        rationale = alternative_rationale
        tier_rule = "whole_unit_with_live_scoped_alternative"
        marker_strength = "complete_received_unit_and_explicit_counterproposal"
        directness = "canonical_WEB_whole_psalm_observation"
    else:
        tier = "high"
        rationale = alternative_rationale
        tier_rule = "complete_received_unit_without_stronger_scoped_rival"
        marker_strength = "complete_received_unit"
        directness = "canonical_WEB_whole_psalm_observation"
    basis = {
        "tier":tier,
        "tier_rule":tier_rule,
        "marker_strength":marker_strength,
        "directness":directness,
        "corroboration":"named_source_feature_when_available_otherwise_canonical_WEB",
        "alternative_strength":"explicitly_assessed_in_rejected_alternative",
        "status_not_used_as_input":True,
        "rationale":rationale,
        "calibration_docket":{
            "path":CONFIDENCE_DOCKET.relative_to(g.ROOT).as_posix(),
            "sha256":CONFIDENCE_DOCKET_SHA256,
            "decision_local_override":override is not None,
        },
    }
    return tier,basis

def hold_record(decision_id: str, psalm: int, start: int, end: int) -> dict[str,Any]:
    static_case = CHILD_DECISION_CASES.get(decision_id)
    static_appeal = (
        static_case.get("challenge_response", {}).get("append_only_appeal")
        if static_case
        else None
    )
    if static_appeal is not None:
        return {
            "kind":"child_specialist_open_appeal",
            "question":static_appeal["question"],
            "options":static_appeal["options"],
            "route":static_appeal["route"],
        }
    if decision_id in {"M7_sol-Ps-050","M7_sol-Ps-051","M7_sol-Ps-052","M7_sol-Ps-053"}:
        return {
            "kind":"ps37_child_granularity",
            "question":NEW_HOLD_QUESTIONS["ps37_child_granularity"],
            "options":[
                {"option":"retain_current_nested_children","argument":"Keep 1-11, 12-20, 21-31, and 32-40 only if the local topical turns outweigh continuous alphabetic wisdom alternation."},
                {"option":"prefer_larger_acrostic_units","argument":"Use the whole Psalm, or test 1-20 and 21-40, because righteous-wicked instruction continues across all three current seams."},
            ],
            "route":"PSALMS_SPECIALIST_HUMAN_OR_EXTERNAL_AI",
        }
    if decision_id in {"M7_sol-Ps-090","M7_sol-Ps-091"}:
        return {
            "kind":"ps59_recurrence_architecture",
            "question":NEW_HOLD_QUESTIONS["ps59_recurrence_architecture"],
            "options":[
                {"option":"retain_current_1_9_10_17","argument":"Keep the current split only if the verse-10 perspective shift outweighs the recurrence architecture."},
                {"option":"prefer_recurrent_cycles_or_whole","argument":"Test 1-5, 6-13, and 14-17, or retain only the whole, because dog, Selah, and strength motifs recur at those edges."},
            ],
            "route":"PSALMS_SPECIALIST_HUMAN_OR_EXTERNAL_AI",
        }
    kind = g.hold_kind(psalm,start,end)
    question,options = g.human_question(psalm,start,end)
    if kind == "linked_acrostic_and_alternate_numbering_parent":
        question = (
            "Given that alternate-numbering evidence is unavailable in the scoped sources, should observed "
            "irregular alphabetic pressure link Psalms 9-10 while retaining both WEB units?"
        )
        options = [
            {"option":"separate_web_units","argument":"Preserve the two WEB coordinates and record the irregular initials as evidence metadata."},
            {"option":"linked_parent","argument":"Expose a non-merging parent for alphabetic pressure; require external evidence before adding any numbering relation."},
        ]
    elif kind == "linked_refrain_parent":
        question = "Should the variant refrain link Psalms 42-43 while both WEB poems remain explicit?"
        options = [
            {"option":"separate_web_units","argument":"Keep chapter-local retrieval and attach the mapped variant-refrain relation as metadata."},
            {"option":"linked_refrain_parent","argument":"Expose the recurring but non-identical refrain through a parent without deleting either WEB child."},
        ]
    elif kind == "web_mt_lxx_alternate_numbering":
        question = f"Should {g.span(psalm,start,end)} remain governed by WEB coordinates while an externally proposed numbering relation awaits a scoped witness?"
        options = [
            {"option":options[0]["option"],"argument":"Retain declared WEB coordinates and record the current Greek/LXX source gap."},
            {"option":options[1]["option"],"argument":"Add the relation only after an exact external witness or versification table is supplied."},
        ]
    return {"kind":kind,"question":question,"options":options,"route":"PSALMS_SPECIALIST_HUMAN_OR_EXTERNAL_AI"}


def redteam_resolution(decision_id: str, held: bool, basis: dict[str,Any]) -> dict[str,Any] | None:
    if basis["decision_kind"] != "child_unit":
        return None
    case = CHILD_DECISION_CASES[decision_id]
    resolution: dict[str,Any] = {
        "specialist_challenge":{
            "docket_path":CHILD_DOCKET.relative_to(g.ROOT).as_posix(),
            "docket_sha256":CHILD_DOCKET_SHA256,
            "structural_advisory_path":CHILD_STRUCTURAL_ADVISORY.relative_to(g.ROOT).as_posix(),
            "structural_advisory_sha256":CHILD_STRUCTURAL_ADVISORY_SHA256,
            "specialist_flag":case["specialist_advisory_flag"],
            "exact_current_context":case["selected_adjacent_seams"],
            "typed_competing_span":case["competing_span"],
        },
        "challenge_response":case["challenge_response"],
        "boss_ruling":{
            "outcome":"held" if held else "accepted_candidate",
            "basis":"literal_decision_case_artifact_and_confidence_calibration",
            "non_authorizing":True,
        },
        "same_model_correlation":"role_separated_same_model_not_cross_model_convergence",
    }
    appeal = case["challenge_response"].get("append_only_appeal")
    if appeal is not None:
        resolution["append_only_appeal"] = appeal
    return resolution

def make_record(number: int, psalm: int, start: int, end: int, lengths: dict[int,int], verses: dict[tuple[int,int],str], crosswalk: dict[str,dict[str,Any]], oshb: dict[str,list[str]], uxlc: dict[str,list[str]], child_docket: dict[int,dict[str,Any]], confidence_overrides: dict[str,dict[str,str]]) -> dict[str,Any]:
    span = g.span(psalm,start,end)
    decision_id = f"M7_sol-Ps-{number:03d}"
    form = g.CHILD_FORMS.get((psalm,start,end),g.FORM_BY_PSALM[psalm])
    parent = g.FORM_BY_PSALM[psalm]
    static_case = CHILD_DECISION_CASES.get(decision_id)
    static_open_appeal = bool(
        static_case
        and static_case.get("challenge_response", {}).get("append_only_appeal")
    )
    held = g.is_held(psalm,start,end) or decision_id in NEW_HOLD_IDS or static_open_appeal
    whole = start == 1 and end == lengths[psalm]
    marker,rationale,rival,basis = local_case(decision_id,psalm,start,end,form,parent,lengths,child_docket)
    if decision_id in CHILD_DECISION_CASES:
        confidence_basis = CHILD_DECISION_CASES[decision_id]["confidence_basis"]
        confidence = confidence_basis["tier"]
    else:
        confidence,confidence_basis = confidence_for(
            decision_id, psalm, start, end, lengths[psalm], rationale, rival, confidence_overrides
        )
    features = poetic_features(psalm,start,end,verses,crosswalk,oshb,uxlc)
    alignment = alignment_for(psalm,start,end,crosswalk)
    hebrew = hebrew_review(psalm,start,end,features,alignment)
    key = (psalm,start,end)
    literary_challenge = key in LITERARY_CHILD_CHALLENGES or decision_id in NEW_HOLD_IDS or (whole and psalm in g.MEDIUM_WHOLE_PSALMS and psalm not in {45,82})
    canonical_challenge = (
        psalm in CANONICAL_CHALLENGE_PSALMS
        and (held or start == 1 or key in {(89,49,52),(118,19,29),(145,14,21)})
        and not (psalm == 2 and whole)
    )
    literary = {
        "verdict":"challenge" if literary_challenge else "supports",
        "basis_field_refs":["boundary_rationale","source_observations"],
        "counterevidence_field_ref":"rejected_alternative",
        "decision_key":f"LIT:{decision_id}:{form}",
    }
    canonical = {
        "verdict":"challenge" if canonical_challenge else "supports",
        "basis_field_refs":["defensible_basis.parent_retained","relation_codes"],
        "counterevidence_field_ref":"rejected_alternative",
        "decision_key":f"CAN:{decision_id}:{parent}",
    }
    verdicts = {"hebrew":hebrew["verdict"],"literary":literary["verdict"],"canonical":canonical["verdict"]}
    challenged = [role for role,value in verdicts.items() if value == "challenge"]
    review_refs = {"hebrew":"reviews.hebrew","literary":"reviews.literary","canonical":"reviews.canonical"}
    static_response = CHILD_DECISION_CASES.get(decision_id,{}).get("challenge_response",{})
    decision_local_answer = static_response.get("answer",rationale)
    responses = [{
        "role":role,
        "status":"unresolved_human_choice" if held else "answered_with_local_evidence",
        "basis_field_ref":review_refs[role],
        "counterproposal_field_ref":"rejected_alternative",
        "decision_local_answer":decision_local_answer,
    } for role in challenged]
    record: dict[str,Any] = {
        "schema_version":"m7_psalms_decision_evidence.v2","book":"Ps","decision_id":decision_id,"span":span,
        "psalm":psalm,"start_verse":start,"end_verse":end,"literary_form":form,"parent_literary_form":parent,
        "candidate_state":"held" if held else "accepted_candidate","confidence":confidence,"confidence_basis":confidence_basis,
        "deciding_marker_or_seam":marker,"boundary_rationale":rationale,"rejected_alternative":rival,
        "defensible_basis":basis,"source_observations":source_observations(psalm,start,end,lengths[psalm],verses),
        "observed_poetic_features":features,"relation_codes":RELATION_CODES.get(psalm,[]),
        "original_language_alignment":alignment,
        "reviews":{
            "hebrew":hebrew,"literary":literary,"canonical":canonical,
            "peer":{"verdict":"hold" if held else "pass","role_verdicts":verdicts,"challenge_count":len(challenged),"basis_fields":["boundary_rationale","rejected_alternative","reviews"]},
        },
        "challenge_responses":responses,"non_authorizing":True,
    }
    resolution = redteam_resolution(decision_id,held,basis)
    if resolution is not None:
        record["redteam_resolution"] = resolution
    if held:
        record["hold"] = hold_record(decision_id,psalm,start,end)
    return record


def main() -> int:
    _, crosswalk = load_crosswalk()
    oshb,uxlc = load_hebrew_words()
    lengths = g.load_lengths()
    verses = load_canonical_web_verses()
    boundaries = g.make_boundaries(lengths)
    child_docket = load_child_docket()
    confidence_overrides = load_confidence_overrides()
    records = [make_record(i,p,s,e,lengths,verses,crosswalk,oshb,uxlc,child_docket,confidence_overrides) for i,(p,s,e) in enumerate(boundaries,1)]
    if len(records) != 283 or len({row["decision_id"] for row in records}) != 283:
        raise RuntimeError("decision evidence must cover 283 unique decisions")
    payload = b"".join((json.dumps(row,ensure_ascii=False,separators=(",",":"))+"\n").encode("utf-8") for row in records)
    OUTPUT.write_bytes(payload)
    states = dict(Counter(row["candidate_state"] for row in records))
    hebrew = dict(Counter(row["reviews"]["hebrew"]["verdict"] for row in records))
    basis = Counter()
    for row in records:
        basis.update(row["original_language_alignment"]["basis_counts"])
    print(json.dumps({"records":len(records),"states":states,"hebrew_verdicts":hebrew,"mapped_verse_basis_totals":dict(basis),"crosswalk_sha256":CROSSWALK_SHA256,"output":OUTPUT.as_posix()},indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
