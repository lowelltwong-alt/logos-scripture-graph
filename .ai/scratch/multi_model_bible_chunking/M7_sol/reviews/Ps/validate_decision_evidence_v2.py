#!/usr/bin/env python3
"""Independently validate the M7_sol Psalm decision-evidence ledger."""
from __future__ import annotations

import ast
from collections import Counter, defaultdict
import hashlib
import importlib.util
import json
from pathlib import Path
import re
from typing import Any, Iterable

HERE = Path(__file__).resolve().parent
LEDGER = HERE / "decision_evidence_v2.jsonl"
REPORT = HERE / "decision_evidence_validation_v2.json"
GENERATOR = HERE / "corrective_re_review_v2.py"
spec = importlib.util.spec_from_file_location("psalms_corrective_validator", GENERATOR)
if spec is None or spec.loader is None:
    raise RuntimeError("unable to import Psalm boundary registry")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

CROSSWALK = g.ROOT / ".ai" / "handoffs" / "T544" / "psalms_web_mt_crosswalk.json"
CROSSWALK_SHA256 = "a83b101fe1ad3e36b3aa2282656afd88ba2fd5925b7f5a6e0511a7d5eb56975d"
SOURCE_AUDIT = g.ROOT / ".ai" / "handoffs" / "T544" / "psalms_hebrew_poetics_source_audit.md"
SOURCE_AUDIT_BASIS_END_MARKER = "## Fresh post-repair source-fidelity verdict — 2026-07-24"
SOURCE_AUDIT_PREFIX_BYTE_COUNT = 15570
SOURCE_AUDIT_PREFIX_SHA256 = "9424a48201ea4f643d2771bd71d5aa90a2424e74b7fba7990e82bf3f474a2c98"
SOURCE_AUTHORITY = "translation_versification_metadata_not_boundary_authority"
AUTHOR = HERE / "author_decision_evidence_v2.py"
CHILD_CASES = HERE / "child_decision_cases_v3.json"
CHILD_CASES_SHA256 = '17c073fa26847db172fd660e2fceaff7b26558d222b739e202418d43e1c2cef7'
CHILD_DOCKET = g.ROOT / ".ai" / "handoffs" / "T544" / "psalms_child_ledger_redteam.md"
CHILD_DOCKET_SHA256 = "59f0a82d546e260d1874b1b0e445ea8c7c989cb5882ae99aafe157043e599a08"
CONFIDENCE_DOCKET = g.ROOT / ".ai" / "handoffs" / "T544" / "psalms_confidence_hold_calibration.md"
CONFIDENCE_DOCKET_SHA256 = "0218f986dbc4fffbcb1e0867ac7bacd623e09e904f8c35acf0b8baec1eb0226d"
CHILD_STRUCTURAL_ADVISORY = g.ROOT / ".ai" / "handoffs" / "T544" / "psalms_child_decision_advisory.jsonl"
CHILD_STRUCTURAL_ADVISORY_SHA256 = "94322b5a27e3df1618ae0f168cbcc9e320f5c594174cec4c9571c06f728be5ef"
TRANSLATION_WITNESSES = g.ROOT / "data" / "canonical" / "translations" / "eng-web" / "translation_witnesses.jsonl"
EXPECTED_STATES = {"accepted_candidate":247,"held":36}
EXPECTED_CONFIDENCE = {'high':75,'medium':200,'medium_low':6,'low':2}
EXPECTED_CONFIDENCE_BY_STATE = {
    "accepted_candidate":{"high":75,"medium":172},
    'held':{'medium':28,'medium_low':6,'low':2},
}
EXPECTED_HEBREW = {"insufficient_evidence":248,"challenge":8,"supports":27}
NEW_HOLD_IDS = {"M7_sol-Ps-050","M7_sol-Ps-051","M7_sol-Ps-052","M7_sol-Ps-053","M7_sol-Ps-090","M7_sol-Ps-091"}
KNOWN_SHELLS = (
    "follows a poem-specific arc",
    "the material counterproposal assessed here",
    "the strongest larger-child alternative",
    "those lines frame the audited",
    "a different local job from both neighbors",
    "two transitions keep the span independently retrievable",
    "the local basis its rival remains explicit",
    "this terminal change bounds",
    "from that opening through",
    "those two observed turns bracket",
    "is the adjacent alternative to",
    "retaining only that merge would hide",
    "the decision selects only",
    "has directly inspectable web transition evidence",
    "covers the received web psalm",
    "covers the complete received web psalm",
)
CORRUPTION_MARKERS = ("\ufffd","doesnâ","â€™","â€œ","â€","Ã","Â","ï¿½")
NUMBERING_GAP_PSALMS = {9,10,114,115,116,147}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise AssertionError(message)


def source_audit_prefix() -> bytes:
    raw = SOURCE_AUDIT.read_bytes()
    marker = SOURCE_AUDIT_BASIS_END_MARKER.encode("utf-8")
    offset = raw.find(marker)
    if offset < 0:
        fail("source-audit basis-end marker is missing")
    prefix = raw[:offset]
    if len(prefix) != SOURCE_AUDIT_PREFIX_BYTE_COUNT or hashlib.sha256(prefix).hexdigest() != SOURCE_AUDIT_PREFIX_SHA256:
        fail("source-audit immutable prefix changed")
    return prefix


def validate_author_source() -> dict[str,Any]:
    source = AUTHOR.read_text(encoding="utf-8")
    forbidden = (
        "This terminal change bounds","From that opening through","Those two observed turns bracket",
        "is the adjacent alternative to","retaining only that merge would hide","The decision selects only",
        "has directly inspectable WEB transition evidence","covers the received WEB Psalm","covers the complete received WEB Psalm",
    )
    hits = [phrase for phrase in forbidden if phrase in source]
    if hits:
        fail(f"author retains forbidden final-prose constructors: {hits}")
    tree = ast.parse(source)
    final_targets = {"rationale","rival","alternative","boundary_rationale","rejected_alternative","confidence","confidence_basis","response","responses","appeal","challenge_response"}
    def assigned_names(target: ast.AST) -> set[str]:
        if isinstance(target,ast.Name):
            return {target.id}
        if isinstance(target,(ast.Tuple,ast.List)):
            return set().union(*(assigned_names(item) for item in target.elts))
        return set()
    loop_fstrings: list[dict[str,Any]] = []
    for loop in (node for node in ast.walk(tree) if isinstance(node,(ast.For,ast.AsyncFor))):
        for node in ast.walk(loop):
            if not isinstance(node,(ast.Assign,ast.AnnAssign)):
                continue
            targets = node.targets if isinstance(node,ast.Assign) else [node.target]
            assigned = set().union(*(assigned_names(target) for target in targets))
            value = node.value
            final = assigned & final_targets
            if final and value is not None and any(isinstance(child,ast.JoinedStr) for child in ast.walk(value)):
                loop_fstrings.append({"line":node.lineno,"targets":sorted(final)})
    if loop_fstrings:
        fail(f"author loop-generates final-field f-strings: {loop_fstrings}")
    return {"forbidden_constructor_hits":0,"loop_generated_final_field_fstrings":0}


def case_tokens(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+",value.lower())


def masked_case_fingerprint(case: dict[str,Any], value: str) -> str:
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


def load_and_validate_child_cases() -> tuple[dict[str,dict[str,Any]],dict[str,Any]]:
    for path,expected in (
        (CHILD_CASES,CHILD_CASES_SHA256),(CHILD_DOCKET,CHILD_DOCKET_SHA256),
        (CONFIDENCE_DOCKET,CONFIDENCE_DOCKET_SHA256),(CHILD_STRUCTURAL_ADVISORY,CHILD_STRUCTURAL_ADVISORY_SHA256),
    ):
        if sha256(path) != expected:
            fail(f"pinned Psalm review artifact changed: {path}")
    cases = json.loads(CHILD_CASES.read_text(encoding="utf-8"))
    advisory = {row["decision_id"]:row for row in map(json.loads,CHILD_STRUCTURAL_ADVISORY.read_text(encoding="utf-8").splitlines())}
    if len(cases) != 182 or len(advisory) != 182:
        fail("child cases and structural advisory must each contain 182 rows")
    fields = {
        "boundary_rationale":lambda case:case["boundary_rationale"],
        "rejected_alternative":lambda case:case["rejected_alternative"],
        "confidence_basis.prose":lambda case:case["confidence_basis"]["prose"],
        "challenge_response.answer":lambda case:case["challenge_response"]["answer"],
    }
    seen = {field:{} for field in fields}
    flag_counts: Counter[str] = Counter()
    edge_count = 0
    for decision_id,case in cases.items():
        raw = advisory.get(decision_id)
        if raw is None or raw.get("authorizes_m7_change") is not False or raw.get("bespoke_prose_approved") is not False or raw.get("copy_into_m7_final_fields_permitted") is not False:
            fail(f"unsafe or missing structural advisory row: {decision_id}")
        provenance = case["provenance"]
        if any(provenance.get(key) is not False for key in ("structural_advisory_prose_used","advisory_bespoke_prose_approved","advisory_copy_into_m7_final_fields_permitted","advisory_authorizes_m7_change")):
            fail(f"child case provenance overclaims advisory prose: {decision_id}")
        if case["specialist_advisory_flag"] != raw["advisory"] or case["competing_span"] != raw["rejected_alternative_merge_span"]:
            fail(f"child case typed advisory mismatch: {decision_id}")
        expected_observations = list(raw['exact_web_observation_refs'])
        if decision_id == 'M7_sol-Ps-167':
            expected_observations.append('Ps.95.6')
        if case['structural_observation_refs'] != expected_observations:
            fail(f'child case observation refs differ from advisory: {decision_id}')
        flag_counts[case["specialist_advisory_flag"]] += 1
        edge_count += len(case["selected_adjacent_seams"])
        if case["boundary_rationale"] in case["rejected_alternative"]:
            fail(f"child alternative contains complete rationale: {decision_id}")
        confidence = case["confidence_basis"]
        if confidence["prose"] == case["boundary_rationale"] or confidence.get("status_not_used_as_input") is not True or any(not confidence.get(key) for key in ("marker","corroboration","alternative_strength","prose")):
            fail(f"child confidence basis is not evidence-independent: {decision_id}")
        response = case["challenge_response"]
        challenge = response.get("exact_challenge",{})
        if challenge != {"current_span":case["span"],"competing_span":case["competing_span"],"specialist_flag":case["specialist_advisory_flag"]} or not response.get("answer"):
            fail(f"child challenge response is not decision-local: {decision_id}")
        if case["specialist_advisory_flag"] in {"H","RC"} and (not response.get("question") or len(response.get("options",[])) < 2):
            fail(f"child H/RC case lacks exact question/options: {decision_id}")
        advisory_words = case_tokens(raw["child_specific_rationale"]+" "+raw["alternative_disposition_reason"])
        advisory_ngrams = {tuple(advisory_words[index:index+8]) for index in range(len(advisory_words)-7)}
        for field,get_value in fields.items():
            value = get_value(case)
            fingerprint = masked_case_fingerprint(case,value)
            prior = seen[field].get(fingerprint)
            if prior:
                fail(f"repeated masked child fingerprint in {field}: {prior}, {decision_id}")
            seen[field][fingerprint] = decision_id
            words_ = case_tokens(value)
            if any(tuple(words_[index:index+8]) in advisory_ngrams for index in range(len(words_)-7)):
                fail(f"child field copies advisory prose 8-gram in {field}: {decision_id}")
    if edge_count != 266 or dict(flag_counts) != {"R":157,"H":23,"RC":2}:
        fail(f"child case edge/flag counts changed: edges={edge_count}, flags={dict(flag_counts)}")
    return cases,{"rows":len(cases),"edges":edge_count,"flags":dict(flag_counts),"masked_fingerprint_duplicates":0,"advisory_prose_8gram_overlaps":0}

def load_rows() -> list[dict[str,Any]]:
    raw = LEDGER.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"ledger is not UTF-8: {exc}")
    rows = [json.loads(line) for line in text.splitlines() if line]
    return rows


def load_canonical_web_verses() -> dict[tuple[int,int],str]:
    verses: dict[tuple[int,int],str] = {}
    for line in TRANSLATION_WITNESSES.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        match = re.fullmatch(r"Ps\.(\d+)\.(\d+)", row.get("osis_ref",""))
        if match:
            verses[tuple(map(int,match.groups()))] = row["text"]
    if len(verses) != 2461:
        fail("canonical WEB witness must contain 2461 Psalm verses")
    return verses


def prose_items(row: dict[str,Any]) -> Iterable[tuple[str,str]]:
    yield "boundary_rationale",row["boundary_rationale"]
    yield "rejected_alternative",row["rejected_alternative"]
    confidence = row.get("confidence_basis",{}).get("prose") or row.get("confidence_basis",{}).get("rationale")
    if isinstance(confidence,str):
        yield "confidence_basis.prose",confidence
    response = row.get("redteam_resolution",{}).get("challenge_response",{}).get("answer")
    if isinstance(response,str):
        yield "redteam_resolution.challenge_response.answer",response
    claim = row["reviews"]["hebrew"].get("claim")
    if isinstance(claim,str):
        yield "reviews.hebrew.claim",claim
    if "hold" in row:
        yield "hold.question",row["hold"]["question"]
        for index,option in enumerate(row["hold"]["options"]):
            yield f"hold.options[{index}].argument",option["argument"]


def tokens(value: str) -> list[str]:
    return re.findall(r"[a-z0-9\u0590-\u05ff]+",value.lower())


def normalized(value: str) -> str:
    return " ".join(tokens(value))


def ngram_report(rows: list[dict[str,Any]], n: int = 7) -> dict[str,Any]:
    clusters: dict[str,set[str]] = defaultdict(set)
    exact: dict[str,set[str]] = defaultdict(set)
    for row in rows:
        for _,value in prose_items(row):
            exact[normalized(value)].add(row["decision_id"])
            words = tokens(value)
            for index in range(len(words)-n+1):
                clusters[" ".join(words[index:index+n])].add(row["decision_id"])
    ranked = sorted(((len(ids),phrase,sorted(ids)) for phrase,ids in clusters.items()),reverse=True)
    maximum = ranked[0][0] if ranked else 0
    offenders = [{"phrase":phrase,"decision_count":count,"decision_ids":ids} for count,phrase,ids in ranked if count >= 10]
    exact_max = max((len(ids) for ids in exact.values()),default=0)
    if offenders:
        fail(f"seven-word prose reuse reaches {offenders[0]['decision_count']}: {offenders[0]['phrase']}")
    return {
        "n":n,"threshold_decision_count":10,"max_decision_reuse":maximum,
        "offender_count":len(offenders),"max_normalized_exact_reuse":exact_max,
        "top_clusters":[{"phrase":phrase,"decision_count":count} for count,phrase,_ in ranked[:10]],
    }


def expected_mapping_row(raw: dict[str,Any]) -> dict[str,Any]:
    return {
        "web_ref":f"WEB:{raw['web_ref']}",
        "verification_basis":raw["verification_basis"],
        "mt_oshb_ref":raw["mt_oshb_ref"],
        "oshb_segment_locator":f"OSHB:Ps.xml#{raw['oshb_segment_locator']}",
        "mt_uxlc_ref":raw["mt_uxlc_ref"],
        "uxlc_locator":f"UXLC:Ps.xml#{raw['mt_uxlc_ref']}",
        "mt_verse_offset":raw["mt_verse_offset"],
        "uxlc_target_exists":raw["uxlc_target_exists"],
    }


def expected_feature_segment(raw: dict[str,Any], role: str, start_word: int, end_word: int) -> dict[str,Any]:
    oshb_locator = f"OSHB:Ps.xml#{raw['mt_oshb_ref']}#w{start_word}-w{end_word}"
    uxlc_locator = f"UXLC:Ps.xml#{raw['mt_uxlc_ref']}#w{start_word}-w{end_word}"
    return {
        "role":role,
        "web_ref":f"WEB:{raw['web_ref']}",
        "mt_oshb_ref":raw["mt_oshb_ref"],
        "mt_uxlc_ref":raw["mt_uxlc_ref"],
        "oshb_segment_locator":oshb_locator,
        "uxlc_segment_locator":uxlc_locator,
        "witnesses":{
            "openscriptures_oshb":{"witness_name":"Open Scriptures Hebrew Bible","source_ref":raw["mt_oshb_ref"],"segment_locator":oshb_locator},
            "tanach_us_uxlc":{"witness_name":"Unicode/XML Leningrad Codex","source_ref":raw["mt_uxlc_ref"],"segment_locator":uxlc_locator},
        },
    }


def validate_feature_segment(decision_id: str, segment: dict[str,Any], expected: dict[str,Any]) -> None:
    for key in ("role","web_ref","mt_oshb_ref","mt_uxlc_ref","oshb_segment_locator","uxlc_segment_locator"):
        if segment.get(key) != expected[key]:
            fail(f"mapped Hebrew feature {key} mismatch in {decision_id}")
    witnesses = {item.get("witness_id"):item for item in segment.get("witnesses",[])}
    if set(witnesses) != set(expected["witnesses"]):
        fail(f"mapped Hebrew feature witness set mismatch in {decision_id}")
    for witness_id,expected_witness in expected["witnesses"].items():
        witness = witnesses[witness_id]
        for key,value in expected_witness.items():
            if witness.get(key) != value:
                fail(f"mapped Hebrew feature witness {key} mismatch in {decision_id}: {witness_id}")
        if not witness.get("observed_text") or not witness.get("normalized_consonants"):
            fail(f"mapped Hebrew feature lacks observed/normalized witness text in {decision_id}: {witness_id}")
    normalization = segment.get("normalization",{})
    expected_operations = [
        "remove Hebrew combining marks including vowel points and cantillation",
        "omit OSHB morpheme separators and non-Hebrew punctuation",
        "preserve consonant and word order",
    ]
    if normalization.get("unicode_form") != "NFD" or normalization.get("operations") != expected_operations or normalization.get("comparison_result") != "matching_consonant_sequence":
        fail(f"mapped Hebrew feature normalization audit failed in {decision_id}")
    if witnesses["openscriptures_oshb"]["normalized_consonants"] != witnesses["tanach_us_uxlc"]["normalized_consonants"]:
        fail(f"mapped Hebrew feature witnesses do not normalize identically in {decision_id}")


def validate_special_hebrew_features(row: dict[str,Any], mapping: dict[str,dict[str,Any]]) -> None:
    decision_id = row["decision_id"]
    psalm = row["psalm"]
    features = row["observed_poetic_features"]
    if psalm == 95:
        feature = next((item for item in features if item.get("kind") == "cross_verse_hebrew_syntax"),None)
        if not feature or feature.get("web_refs") != ["WEB:Ps.95.7","WEB:Ps.95.8"] or feature.get("supported_seam") != "WEB:Ps.95.6/WEB:Ps.95.7" or feature.get("rejected_seam") != "WEB:Ps.95.7/WEB:Ps.95.8":
            fail(f"Psalm 95 exact syntax feature mismatch in {decision_id}")
        expected = [
            expected_feature_segment(mapping["Ps.95.7"],"hearing_condition",9,12),
            expected_feature_segment(mapping["Ps.95.8"],"conditioned_prohibition",1,3),
        ]
        if len(feature.get("segments",[])) != 2:
            fail(f"Psalm 95 syntax feature segment count mismatch in {decision_id}")
        for segment,expected_segment in zip(feature["segments"],expected):
            validate_feature_segment(decision_id,segment,expected_segment)
        if feature.get("normalization_scope") != "consonantal comparison only; syntax is assessed on the named vocalized witnesses":
            fail(f"Psalm 95 normalization scope mismatch in {decision_id}")
    elif psalm == 110:
        feature = next((item for item in features if item.get("kind") == "mapped_boundary_oath_formula"),None)
        raw3,raw4 = mapping["Ps.110.3"],mapping["Ps.110.4"]
        expected = [
            expected_feature_segment(raw3,"left_boundary_context",int(raw3["oshb_word_start"]),int(raw3["oshb_word_end"])),
            expected_feature_segment(raw4,"oath_formula",1,2),
        ]
        if not feature or feature.get("web_refs") != ["WEB:Ps.110.3","WEB:Ps.110.4"] or len(feature.get("segments",[])) != 2:
            fail(f"Psalm 110 mapped oath feature mismatch in {decision_id}")
        for segment,expected_segment in zip(feature["segments"],expected):
            validate_feature_segment(decision_id,segment,expected_segment)
        context = feature.get("mapped_boundary_context",{})
        expected_outside = not (row["start_verse"] <= 4 <= row["end_verse"])
        if context != {"seam":"WEB:Ps.110.3/WEB:Ps.110.4","context_ref":"WEB:Ps.110.4","context_outside_chunk_alignment":expected_outside,"context_is_separately_mapped":True}:
            fail(f"Psalm 110 separately mapped context mismatch in {decision_id}")
    elif psalm == 132:
        feature = next((item for item in features if item.get("kind") == "mapped_directional_oath_pair"),None)
        expected = [
            expected_feature_segment(mapping["Ps.132.2"],"david_swears_to_yahweh",1,3),
            expected_feature_segment(mapping["Ps.132.11"],"yahweh_swears_to_david",1,3),
        ]
        if not feature or feature.get("web_refs") != ["WEB:Ps.132.2","WEB:Ps.132.11"] or len(feature.get("segments",[])) != 2:
            fail(f"Psalm 132 directional oath feature mismatch in {decision_id}")
        for segment,expected_segment in zip(feature["segments"],expected):
            validate_feature_segment(decision_id,segment,expected_segment)


def validate() -> dict[str,Any]:
    if sha256(CROSSWALK) != CROSSWALK_SHA256:
        fail("crosswalk SHA-256 mismatch")
    source_prefix = source_audit_prefix()
    author_source_audit = validate_author_source()
    child_cases,child_case_audit = load_and_validate_child_cases()
    crosswalk = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    if crosswalk["authority"] != SOURCE_AUTHORITY:
        fail("crosswalk authority mismatch")
    expected_source_hashes = crosswalk["source_sha256"]
    source_paths = crosswalk["source_paths"]
    for key,relative in source_paths.items():
        source_path = g.ROOT / relative
        if sha256(source_path) != expected_source_hashes[key]:
            fail(f"crosswalk source hash mismatch: {key}")
    mapping = {row["web_ref"]:row for row in crosswalk["verse_mapping"]}
    if len(mapping) != 2461:
        fail("crosswalk must map 2461 unique WEB refs")

    rows = load_rows()
    if len(rows) != 283 or len({row["decision_id"] for row in rows}) != 283:
        fail("ledger must contain 283 unique decisions")
    lengths = g.load_lengths()
    verses = load_canonical_web_verses()
    expected_boundaries = g.make_boundaries(lengths)
    actual_boundaries = [(row["psalm"],row["start_verse"],row["end_verse"]) for row in rows]
    if actual_boundaries != expected_boundaries:
        fail("decision order/boundaries differ from the Psalm registry")
    expected_ids = [f"M7_sol-Ps-{index:03d}" for index in range(1,284)]
    if [row["decision_id"] for row in rows] != expected_ids:
        fail("decision IDs are not sequential")

    states = dict(Counter(row["candidate_state"] for row in rows))
    confidence = dict(Counter(row["confidence"] for row in rows))
    hebrew = dict(Counter(row["reviews"]["hebrew"]["verdict"] for row in rows))
    if states != EXPECTED_STATES:
        fail(f"state counts changed: {states}")
    if confidence != EXPECTED_CONFIDENCE:
        fail(f"confidence counts changed: {confidence}")
    confidence_by_state = {
        state:dict(Counter(row["confidence"] for row in rows if row["candidate_state"] == state))
        for state in EXPECTED_STATES
    }
    if confidence_by_state != EXPECTED_CONFIDENCE_BY_STATE:
        fail(f"confidence/state cross-tab changed: {confidence_by_state}")
    if hebrew != EXPECTED_HEBREW:
        fail(f"Hebrew verdict counts changed: {hebrew}")

    coverage: Counter[str] = Counter()
    observed_basis: Counter[str] = Counter()
    role_counts = {role:Counter() for role in ("hebrew","literary","canonical","peer")}
    challenge_response_count = 0
    for row in rows:
        if row["schema_version"] != "m7_psalms_decision_evidence.v2" or row["book"] != "Ps":
            fail(f"schema/book mismatch in {row['decision_id']}")
        if row["non_authorizing"] is not True:
            fail(f"authorizing record found: {row['decision_id']}")
        psalm,start,end = row["psalm"],row["start_verse"],row["end_verse"]
        expected_span = g.span(psalm,start,end)
        if row["span"] != expected_span:
            fail(f"span mismatch in {row['decision_id']}")
        if row["literary_form"] != g.CHILD_FORMS.get((psalm,start,end),g.FORM_BY_PSALM[psalm]):
            fail(f"local form mismatch in {row['decision_id']}")
        if row["parent_literary_form"] != g.FORM_BY_PSALM[psalm]:
            fail(f"parent form mismatch in {row['decision_id']}")
        decision_id = row["decision_id"]
        case = child_cases.get(decision_id)
        confidence_basis = row.get("confidence_basis",{})
        if confidence_basis.get("tier") != row["confidence"] or confidence_basis.get("status_not_used_as_input") is not True:
            fail(f"confidence basis/status coupling guard failed in {decision_id}")
        if case is not None:
            if row["boundary_rationale"] != case["boundary_rationale"] or row["rejected_alternative"] != case["rejected_alternative"]:
                fail(f"child final prose differs from static decision case in {decision_id}")
            if confidence_basis != case["confidence_basis"]:
                fail(f"child confidence basis differs from static decision case in {decision_id}")
            basis = row.get("defensible_basis",{})
            artifact = basis.get("decision_case_artifact",{})
            expected_artifact = {
                "path":CHILD_CASES.relative_to(g.ROOT).as_posix(),
                "sha256":CHILD_CASES_SHA256,
                "final_fields_copied_verbatim":["boundary_rationale","rejected_alternative","confidence_basis","challenge_response"],
            }
            if artifact != expected_artifact:
                fail(f"child decision-case artifact pin mismatch in {decision_id}")
            structural = basis.get("independent_structural_advisory",{})
            expected_structural = {
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
            }
            if structural != expected_structural:
                fail(f"child typed structural advisory mismatch in {decision_id}")
            resolution = row.get("redteam_resolution",{})
            if resolution.get("challenge_response") != case["challenge_response"]:
                fail(f"child challenge response differs from static decision case in {decision_id}")
            specialist = resolution.get("specialist_challenge",{})
            if specialist.get("specialist_flag") != case["specialist_advisory_flag"] or specialist.get("exact_current_context") != case["selected_adjacent_seams"] or specialist.get("typed_competing_span") != case["competing_span"]:
                fail(f"child specialist challenge provenance mismatch in {decision_id}")
            appeal = case["challenge_response"].get("append_only_appeal")
            if resolution.get("append_only_appeal") != appeal:
                fail(f"child append-only appeal mismatch in {decision_id}")
            if any(response.get("decision_local_answer") != case["challenge_response"]["answer"] for response in row["challenge_responses"]):
                fail(f"child role response does not use the static decision-local answer in {decision_id}")
        else:
            required_confidence = ("tier_rule","marker_strength","directness","corroboration","alternative_strength","rationale")
            if any(not confidence_basis.get(field) for field in required_confidence):
                fail(f"whole-Psalm confidence basis is incomplete in {decision_id}")
            docket = confidence_basis.get("calibration_docket",{})
            if docket.get("path") != CONFIDENCE_DOCKET.relative_to(g.ROOT).as_posix() or docket.get("sha256") != CONFIDENCE_DOCKET_SHA256:
                fail(f"whole-Psalm confidence docket pin mismatch in {decision_id}")
        static_open_appeal = bool(
            case
            and case.get("challenge_response", {}).get("append_only_appeal")
        )
        expected_held = g.is_held(psalm,start,end) or decision_id in NEW_HOLD_IDS or static_open_appeal
        if (row["candidate_state"] == "held") != expected_held:
            fail(f"hold mismatch in {row['decision_id']}")
        if ("hold" in row) != (row["candidate_state"] == "held"):
            fail(f"hold payload mismatch in {row['decision_id']}")
        for verse in range(start,end+1):
            coverage[f"Ps.{psalm}.{verse}"] += 1

        observations = row["source_observations"]
        if not observations:
            fail(f"no source observations in {row['decision_id']}")
        for observation in observations:
            match = re.fullmatch(r"WEB:Ps\.(\d+)\.(\d+)",observation["ref"])
            if not match:
                fail(f"invalid WEB observation ref in {row['decision_id']}")
            key = tuple(map(int,match.groups()))
            if observation["extent"] != "complete_verse" or observation["text"] != verses[key]:
                fail(f"non-exact WEB observation in {row['decision_id']}: {observation['ref']}")

        alignment = row["original_language_alignment"]
        if alignment["web_mt_crosswalk_status"] != "verified_candidate_mapping":
            fail(f"crosswalk status mismatch in {row['decision_id']}")
        if alignment["crosswalk_artifact_id"] != "T544_PS_WEB_MT_V1" or alignment["crosswalk_sha256"] != CROSSWALK_SHA256:
            fail(f"crosswalk pin mismatch in {row['decision_id']}")
        expected_lineage = {
            "path":SOURCE_AUDIT.relative_to(g.ROOT).as_posix(),
            "basis_end_marker":SOURCE_AUDIT_BASIS_END_MARKER,
            "prefix_byte_count":SOURCE_AUDIT_PREFIX_BYTE_COUNT,
            "prefix_sha256":SOURCE_AUDIT_PREFIX_SHA256,
            "appended_verdict_treated_separately":True,
        }
        if alignment.get("source_audit_lineage") != expected_lineage or alignment["authority"] != SOURCE_AUTHORITY:
            fail(f"source authority lineage mismatch in {row['decision_id']}")
        expected_rows = [expected_mapping_row(mapping[f"Ps.{psalm}.{verse}"]) for verse in range(start,end+1)]
        if alignment["ordered_verse_mapping"] != expected_rows:
            fail(f"ordered mapped segments mismatch in {row['decision_id']}")
        expected_basis = dict(Counter(item["verification_basis"] for item in expected_rows))
        if alignment["basis_counts"] != expected_basis:
            fail(f"mapping basis mismatch in {row['decision_id']}")
        if alignment["mt_verse_offsets"] != sorted({item["mt_verse_offset"] for item in expected_rows}):
            fail(f"offset summary mismatch in {row['decision_id']}")
        if alignment["greek_lxx_source_available"] is not False or alignment["selah_boundary_authority"] is not False:
            fail(f"source authority overclaimed in {row['decision_id']}")
        observed_basis.update(alignment["basis_counts"])
        validate_special_hebrew_features(row,mapping)

        for role in role_counts:
            role_counts[role][row["reviews"][role]["verdict"]] += 1
        challenged = [role for role in ("hebrew","literary","canonical") if row["reviews"][role]["verdict"] == "challenge"]
        response_roles = [item["role"] for item in row["challenge_responses"]]
        if sorted(challenged) != sorted(response_roles):
            fail(f"challenge response coverage mismatch in {row['decision_id']}")
        challenge_response_count += len(response_roles)

        prose_blob = " ".join(value for _,value in prose_items(row))
        prose_lower = prose_blob.lower()
        if any(marker.lower() in prose_lower for marker in KNOWN_SHELLS):
            fail(f"known shell phrase in {row['decision_id']}")
        if any(marker in prose_blob for marker in CORRUPTION_MARKERS):
            fail(f"encoding corruption in {row['decision_id']}")
        if re.search(r"[?!][.,]",prose_blob) or re.search(r"[?!][\"”][.,]",prose_blob):
            fail(f"duplicate terminal punctuation in {row['decision_id']}")
        if any(mark in prose_blob for mark in ('"','“','”')):
            fail(f"unverified quotation marks in prose for {row['decision_id']}")
        if psalm in NUMBERING_GAP_PSALMS:
            if alignment["greek_lxx_source_available"] is not False:
                fail(f"Greek/LXX source incorrectly available in {row['decision_id']}")
            if "LXX_WITNESS_GAP" not in row["relation_codes"]:
                fail(f"numbering gap code missing in {row['decision_id']}")
            if psalm in {114,115,116,147} and "witness" not in prose_lower and row["candidate_state"] == "held":
                fail(f"numbering hold lacks witness limitation in {row['decision_id']}")

    if len(coverage) != 2461 or any(count != 1 for count in coverage.values()):
        fail("chunk coverage is not exactly 2461 WEB verses once each")
    if dict(observed_basis) != {"structural_identity_no_explicit_note":1419,"explicit_oshb_kjv_note":1042}:
        fail(f"crosswalk aggregate changed: {dict(observed_basis)}")

    ps13 = next(row for row in rows if row["psalm"] == 13)
    ps13_map = {item["web_ref"]:item["oshb_segment_locator"] for item in ps13["original_language_alignment"]["ordered_verse_mapping"]}
    if ps13_map["WEB:Ps.13.5"] != "OSHB:Ps.xml#Ps.13.6#w1-w6" or ps13_map["WEB:Ps.13.6"] != "OSHB:Ps.xml#Ps.13.6#w7-w11":
        fail("Psalm 13 disjoint segments were collapsed")

    ps95_spans = [(row["start_verse"],row["end_verse"]) for row in rows if row["psalm"] == 95]
    if ps95_spans != [(1,6),(7,11)]:
        fail(f"Psalm 95 seam regression: {ps95_spans}")
    for row in rows:
        if row["psalm"] == 95:
            kinds = {item["kind"] for item in row["observed_poetic_features"]}
            if "cross_verse_hebrew_syntax" not in kinds or row["reviews"]["hebrew"]["verdict"] != "supports":
                fail(f"Psalm 95 syntax evidence missing in {row['decision_id']}")
        if row["psalm"] == 119:
            feature = next((item for item in row["observed_poetic_features"] if item["kind"] == "eight_verse_initial_consonant_block"),None)
            if not feature or feature["heading_element_claimed"] is not False or len(set(feature["oshb_initials"])) != 1 or len(set(feature["uxlc_initials"])) != 1:
                fail(f"Psalm 119 initials invalid in {row['decision_id']}")
        if row["psalm"] in {42,43}:
            feature = next((item for item in row["observed_poetic_features"] if item["kind"] == "variant_refrain"),None)
            if not feature or feature["comparison"][0] != "variant":
                fail(f"Psalm 42-43 variant refrain invalid in {row['decision_id']}")
        if row["psalm"] == 145:
            feature = next((item for item in row["observed_poetic_features"] if item["kind"] == "incomplete_alphabetic_praise"),None)
            if not feature or feature["nun_line_present"] is not False or feature["greek_repair_claimed"] is not False:
                fail(f"Psalm 145 incomplete acrostic invalid in {row['decision_id']}")

    prose = ngram_report(rows)
    schema = {
        "reviews":{
            "hebrew":sorted({key for row in rows for key in row["reviews"]["hebrew"]}),
            "literary":sorted(rows[0]["reviews"]["literary"]),
            "canonical":sorted(rows[0]["reviews"]["canonical"]),
            "peer":sorted(rows[0]["reviews"]["peer"]),
        },
        "original_language_alignment":sorted(rows[0]["original_language_alignment"]),
        "ordered_verse_mapping":sorted(rows[0]["original_language_alignment"]["ordered_verse_mapping"][0]),
    }
    report = {
        "validator":"validate_decision_evidence_v2.py",
        "verdict":"pass","non_authorizing":True,
        "ledger":{"path":LEDGER.relative_to(g.ROOT).as_posix(),"sha256":sha256(LEDGER),"records":len(rows)},
        "crosswalk":{
            "path":CROSSWALK.relative_to(g.ROOT).as_posix(),"sha256":sha256(CROSSWALK),
            "source_audit_lineage":{
                "path":SOURCE_AUDIT.relative_to(g.ROOT).as_posix(),
                "basis_end_marker":SOURCE_AUDIT_BASIS_END_MARKER,
                "prefix_byte_count":len(source_prefix),
                "prefix_sha256":hashlib.sha256(source_prefix).hexdigest(),
                "current_whole_file_sha256":sha256(SOURCE_AUDIT),
                "current_whole_file_is_not_pinned_authority":True,
            },
            "authority":SOURCE_AUTHORITY,"aggregate_basis":dict(observed_basis),
        },
        "counts":{"states":states,"confidence":confidence,"confidence_by_state":confidence_by_state,"hebrew_verdicts":hebrew,"role_verdicts":{role:dict(counts) for role,counts in role_counts.items()},"challenge_responses":challenge_response_count,"covered_web_verses":len(coverage)},
        "boundaries":{"decision_count":len(rows),"psalm_95":["Ps.95.1-Ps.95.6","Ps.95.7-Ps.95.11"],"holds":states["held"]},
        "prose_reuse":prose,"quote_fidelity":{"unverified_quote_mark_count":0,"source_observations_are_complete_verses":True,"duplicate_terminal_punctuation_count":0},
        "author_source_audit":author_source_audit,
        "child_decision_case_audit":{
            **child_case_audit,
            "path":CHILD_CASES.relative_to(g.ROOT).as_posix(),
            "sha256":sha256(CHILD_CASES),
            "final_fields_matched_verbatim":True,
            "confidence_status_independence_checked":True,
            "challenge_responses_matched_verbatim":True,
        },
        "schema":schema,
        "hard_passages":{"ps13_disjoint_segments":True,"ps42_43_variant_refrain":True,"ps95_syntax_reaudited":True,"ps110_oath_context_separately_mapped":True,"ps119_initials_not_headings":True,"ps132_directional_oaths_mapped":True,"ps145_incomplete_acrostic":True,"lxx_numbering_source_gaps":True},
    }
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return report


def main() -> int:
    print(json.dumps(validate(),ensure_ascii=False,indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
