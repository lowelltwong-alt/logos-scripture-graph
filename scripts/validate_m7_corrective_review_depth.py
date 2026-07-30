#!/usr/bin/env python3
"""Reject thin M7 book reviews without pretending to judge Bible boundaries.

This validator is an opt-in corrective-depth gate for books re-reviewed after
the T544 thin-pass diagnosis.  It checks observable review discipline: bespoke
rationales, real form labels, decision-local attempts and evidence, honest
support/challenge mix, calibrated confidence, and specific holds.  Human and
external-model convergence remain separate, non-fabricable gates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODEL_ROOT = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
WEB_TRANSLATION_WITNESSES = (
    ROOT / "data" / "canonical" / "translations" / "eng-web" / "translation_witnesses.jsonl"
)
ACCEPTED = "accepted_candidate"
HELD = {"held_lower_confidence", "deferred_human_or_external_ai"}
MEDIUM_HIGH = {"medium", "high"}
VALID_VERDICTS = {"support", "supports", "challenge", "insufficient_evidence", "frontier_defer"}
MAX_ATTEMPT_REUSE = 8
PACKET_SCHEMA = "m7_corrective_review_packet.v2"
REVIEW_REVISION = "m7-corrective-rereview-v2"

TEMPLATE_RATIONALE_PATTERNS = (
    re.compile(r"^prefer (?:the )?complete\b", re.I),
    re.compile(r"^prefer complete larger\b", re.I),
    re.compile(r"selected clean literary\s*=", re.I),
    re.compile(r"preserved exact competing evidence", re.I),
    re.compile(r"^[A-Za-z0-9.:-]+ is retained as an? .+ candidate because", re.I),
    re.compile(r"counterevidence is explicit", re.I),
    re.compile(r"WEB wording governs the coordinate decision", re.I),
    re.compile(r"follows a poem-specific arc", re.I),
    re.compile(r"the material counterproposal assessed here is", re.I),
    re.compile(r"the strongest larger-child alternative", re.I),
)
GENERIC_FORM_PATTERNS = (
    re.compile(r"narrative[-_ ]discourse episode", re.I),
    re.compile(r"teaching discourse or saying sequence", re.I),
    re.compile(r"larger prophetic[-_ ]literary unit", re.I),
    re.compile(r"complete canonical psalm poem", re.I),
    re.compile(r"^(?:larger|smaller|complete|generic|general)?[_ -]*(?:passage|section|episode|unit)$", re.I),
)
SOURCE_ANCHOR_RE = re.compile(
    r"(?:^|[/\s])(?:WEB|OSHB|UXLC|SBLGNT|UGNT|CNTR|USFM|canonical_text|direct_read):",
    re.I,
)
OT_BOOKS = {
    "Gen", "Exod", "Lev", "Num", "Deut", "Josh", "Judg", "Ruth",
    "1Sam", "2Sam", "1Kgs", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh",
    "Esth", "Job", "Ps", "Prov", "Eccl", "Song", "Isa", "Jer", "Lam",
    "Ezek", "Dan", "Hos", "Joel", "Amos", "Obad", "Jonah", "Mic",
    "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal",
}
NT_BOOKS = {
    "Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor",
    "Gal", "Eph", "Phil", "Col", "1Thess", "2Thess", "1Tim", "2Tim",
    "Titus", "Phlm", "Heb", "Jas", "1Pet", "2Pet", "1John", "2John",
    "3John", "Jude", "Rev",
}
ORIGINAL_LANGUAGE_ROLE_RE = re.compile(
    r"(?:hebrew|aramaic|greek|original[_ -]?language|textual[_ -]?witness)",
    re.I,
)
QUESTION_MARK_AS_OPENING_PUNCTUATION_RE = re.compile(r"\?[A-Za-z0-9]")
DOUBLE_TERMINAL_PUNCTUATION_RE = re.compile(r"[?!](?:[.,]|[\"?][.,])")
TRUNCATED_QUOTE_RE = re.compile(
    r"[\"?][^\"?]{2,180}\b(?:the|of|in|to|and|for|with|from|on|at|by|a|an)[\"?]",
    re.I,
)
PACKET_BATCH_PROSE_SHELL_PATTERNS = {
    "web_coordinates_are_stable": re.compile(r"the WEB coordinates for .+ are stable", re.I),
    "local_form_not_metadata_authority": re.compile(r"the local form claim does not depend on treating", re.I),
    "hebrew_evidence_may_weight_recorded_alternative": re.compile(r"Hebrew-poetic or versification evidence may give additional weight", re.I),
    "neighboring_movement_plausibly_attached": re.compile(r"the neighboring movement can plausibly remain attached", re.I),
    "explicit_whole_psalm_parent": re.compile(r"remains inside an explicit whole-Psalm parent", re.I),
    "retrieval_could_overstate_child": re.compile(r"retrieval could overstate the child or conceal", re.I),
    "peer_compared": re.compile(r"the peer compared", re.I),
}
PROSE_FIELD_NAMES = {
    'confidence_basis',
    'confidence_rationale',
    'convergence_defense_rationale',
    'convergence_rationale',
    "boundary_rationale",
    "deciding_marker_or_seam",
    "rejected_alternative",
    "defensible_basis",
    "support",
    "counterevidence",
    "rationale",
    "claim",
    "proposed_remedy",
}
BATCH_PROSE_SHELL_PATTERNS = {
    "poem_specific_arc": re.compile(r"follows a poem-specific arc", re.I),
    "material_counterproposal_assessed": re.compile(r"the material counterproposal assessed here is", re.I),
    "strongest_larger_child_alternative": re.compile(r"the strongest larger-child alternative", re.I),
    "audited_poem_specific_movement": re.compile(r"those lines frame the audited poem-specific movement", re.I),
    "tested_merger_is_specific": re.compile(r"the tested merger is specific", re.I),
    "adjacent_span_concrete_answer": re.compile(r"the adjacent-span alternative receives a concrete answer", re.I),
    "treating_both_as_one_child": re.compile(r"treating both as one child was considered rather than assumed", re.I),
    "web_completes_initiates_retain": re.compile(
        r"^WEB:[^;]+ completes .+;\s*WEB:[^;]+ initiates .+\.\s*Retain\b",
        re.I,
    ),
    "web_closes_initiates_preserve": re.compile(
        r"^WEB:[^;]+ closes .+;\s*WEB:[^;]+ initiates .+\.\s*Preserve\b",
        re.I,
    ),
    "web_leaves_then_opens_keep": re.compile(
        r"^WEB:[^;]+ leaves .+;\s*WEB:[^;]+ then opens .+\.\s*Keep\b",
        re.I,
    ),
    "merge_cost_constructor": re.compile(r"^Merge .+;\s*cost:", re.I),
    "absorb_cost_constructor": re.compile(r"^Absorb .+;\s*cost:", re.I),
    'terminal_change_bounds_constructor': re.compile(r'\bthis terminal change bounds\b', re.I),
    'opening_through_close_constructor': re.compile(r'\bfrom that opening through\b', re.I),
    'two_observed_turns_bracket_constructor': re.compile(r'\bthose two observed turns bracket\b', re.I),
    'middle_child_two_edges_constructor': re.compile(r'\bthis middle child has two observed edges\b', re.I),
    'adjacent_alternative_constructor': re.compile(r'\bis the adjacent alternative\b', re.I),
    'directly_inspectable_web_transition_constructor': re.compile(
        r'\bhas directly inspectable WEB transition evidence\b', re.I,
    ),
    'received_web_psalm_constructor': re.compile(
        r'\bcovers the (?:complete )?received WEB Psalm\b', re.I,
    ),
    'proposed_unit_opening_closure_constructor': re.compile(
        r'\bgive the proposed .+ unit its own opening and closure\b', re.I,
    ),
    'parent_context_loses_constructor': re.compile(
        r'\bremains valid as parent context, but loses as a replacement child because it suppresses\b', re.I,
    ),
    'eight_verse_acrostic_confidence_constructor': re.compile(
        r'\bis an eight-verse\b.{0,120}\bacrostic\b', re.I,
    ),
    'enumerated_fields_resolution_constructor': re.compile(
        r'\bselects only \d+ seams?, retains .+ parent, (?:and )?tests (?:the )?alternative\b', re.I,
    ),
}
ZERO_TOLERANCE_BATCH_PROSE_SHELLS = {
    'terminal_change_bounds_constructor',
    'opening_through_close_constructor',
    'two_observed_turns_bracket_constructor',
    'middle_child_two_edges_constructor',
    'adjacent_alternative_constructor',
    'directly_inspectable_web_transition_constructor',
    'received_web_psalm_constructor',
    'proposed_unit_opening_closure_constructor',
    'parent_context_loses_constructor',
    'eight_verse_acrostic_confidence_constructor',
    'enumerated_fields_resolution_constructor',
    "web_completes_initiates_retain",
    "web_closes_initiates_preserve",
    "web_leaves_then_opens_keep",
    "merge_cost_constructor",
    "absorb_cost_constructor",
}

_SEMANTIC_SLOT_EXACT_KEYS = {
    'decision_id', 'span', 'web_span', 'source_span', 'retrieval_choice',
    'parent_retained', 'adjacent_span', 'rejected_alternative_merge_span',
    'literary_form', 'literature_type_guess', 'local_function', 'parent_literary_form',
    'child_literary_form', 'form', 'parent_form', 'advisory',
    'specialist_advisory_flag',
}
_SEMANTIC_SLOT_CONTEXT_KEYS = {
    'deciding_marker_or_seam', 'source_observations',
    'observed_poetic_features', 'original_language_alignment',
    'evidence_refs', 'source_refs', 'deciding_boundary_refs',
    'structural_observation_refs',
}


_HEBREW_LABEL_RE = re.compile(
    r'\b(?:aleph|beth|gimel|daleth|he|waw|zayin|heth|teth|yodh|kaph|lamedh|mem|nun|samekh|ayin|pe|tsadhe|qoph|resh|shin|taw)\b|[\u05d0-\u05ea]',
    re.I,
)
_OSIS_LOCATOR_RE = re.compile(
    r'\b(?:WEB|OSHB|UXLC|SBLGNT|UGNT|CNTR|USFM):[1-4]?[A-Za-z]+\.\d+\.\d+(?:-[1-4]?[A-Za-z]+\.\d+\.\d+)?(?:#[^\s,;)\]}]+)?',
    re.I,
)


_OSIS_SPAN_RE = re.compile(
    r'\b[1-4]?[A-Za-z]+\.\d+\.\d+(?:-[1-4]?[A-Za-z]+\.\d+\.\d+)?\b', re.I,
)


_HUMAN_LOCATOR_RE = re.compile(r'\b(?:[1-4]?[A-Za-z]+\s+)?\d+:\d+(?:-\d+)?\b', re.I)
_VERSE_LOCATOR_RE = re.compile(r'\b(?:verses?|vv?\.)\s*\d+(?:-\d+)?\b', re.I)


_QUOTED_TEXT_RE = re.compile(chr(34) + r'[^\r\n]{3,}' + chr(34))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ValueError(f"missing {path.as_posix()}")
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path.as_posix()}:{line_no}: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path.as_posix()}:{line_no}: expected object")
            rows.append(row)
    return rows


@lru_cache(maxsize=1)
def _load_web_translation_witnesses(
    path: Path = WEB_TRANSLATION_WITNESSES,
) -> dict[str, str]:
    witnesses: dict[str, str] = {}
    for row in _read_jsonl(path):
        osis_ref = row.get("osis_ref")
        text = row.get("text")
        if isinstance(osis_ref, str) and isinstance(text, str):
            witnesses[f"WEB:{osis_ref}"] = text
    if not witnesses:
        raise ValueError(f"{path.as_posix()}: no WEB translation witnesses found")
    return witnesses


def _strip_excerpt_ellipses(text: str) -> str | None:
    value = text.strip()
    has_ellipsis = False
    if value.startswith("..."):
        value = value[3:]
        has_ellipsis = True
    elif value.startswith("…"):
        value = value[1:]
        has_ellipsis = True
    if value.endswith("..."):
        value = value[:-3]
        has_ellipsis = True
    elif value.endswith("…"):
        value = value[:-1]
        has_ellipsis = True
    if not has_ellipsis:
        return None
    core = value.strip()
    return core or None


def _validate_structured_web_quote_fidelity(
    value: Any,
    canonical_witnesses: Mapping[str, str],
    *,
    path: str = "$",
) -> tuple[list[str], int]:
    """Recursively validate structured WEB observations without mutating input."""
    errors: list[str] = []
    checked = 0
    if isinstance(value, dict):
        ref = value.get("ref")
        quote_candidate = isinstance(ref, str) and ref.startswith("WEB:")

        if quote_candidate:
            checked += 1
            if not all(field in value for field in ("ref", "text", "extent")):
                errors.append(f"{path}: structured WEB quote requires ref, text, and extent")
            elif not isinstance(ref, str) or ref not in canonical_witnesses:
                errors.append(f"{path}: missing canonical WEB ref {ref!r}")
            elif not isinstance(value["text"], str) or not isinstance(value["extent"], str):
                errors.append(f"{path}: structured WEB quote text and extent must be strings")
            else:
                quote_text = value["text"]
                extent = value["extent"]
                canonical = canonical_witnesses[ref]
                if extent == "complete_verse":
                    if quote_text != canonical:
                        errors.append(f"{path}: complete_verse text must equal canonical WEB exactly")
                elif "excerpt" in extent.lower():
                    core = _strip_excerpt_ellipses(quote_text)
                    if core is None:
                        errors.append(f"{path}: excerpt text must have at least one explicit ellipsis")
                    elif core not in canonical:
                        errors.append(f"{path}: excerpt core is not an exact canonical WEB substring")
                else:
                    errors.append(f"{path}: unsupported structured WEB quote extent {extent!r}")
        for key, child in value.items():
            child_errors, child_checked = _validate_structured_web_quote_fidelity(
                child,
                canonical_witnesses,
                path=f"{path}.{key}",
            )
            errors.extend(child_errors)
            checked += child_checked
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_errors, child_checked = _validate_structured_web_quote_fidelity(
                child,
                canonical_witnesses,
                path=f"{path}[{index}]",
            )
            errors.extend(child_errors)
            checked += child_checked
    return errors, checked


def _present(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, tuple, set)):
        return bool(value)
    return value is not None


def _iter_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from _iter_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_strings(child)


def _has_question_mark_encoding_corruption(value: Any) -> bool:
    return any(
        QUESTION_MARK_AS_OPENING_PUNCTUATION_RE.search(text)
        or DOUBLE_TERMINAL_PUNCTUATION_RE.search(text)
        for text in _iter_strings(value)
    )


def _collect_prose_strings(value: Any):
    if not isinstance(value, dict):
        return
    for key, child in value.items():
        if key in PROSE_FIELD_NAMES and isinstance(child, str):
            yield child
        elif isinstance(child, dict):
            yield from _collect_prose_strings(child)
        elif isinstance(child, list):
            for item in child:
                if isinstance(item, dict):
                    yield from _collect_prose_strings(item)


def _pervasive_prose_ngrams(
    rows: list[dict[str, Any]],
    *,
    ngram_size: int = 7,
    min_decisions: int = 10,
) -> list[tuple[int, str, list[str]]]:
    uses: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        decision_id = str(row.get("decision_id", ""))
        decision_ngrams: set[str] = set()
        for prose in _collect_prose_strings(row):
            tokens = re.findall(r"[a-z0-9]+(?:'[a-z]+)?", prose.lower())
            decision_ngrams.update(
                " ".join(tokens[index : index + ngram_size])
                for index in range(max(0, len(tokens) - ngram_size + 1))
            )
        for ngram in decision_ngrams:
            uses[ngram].add(decision_id)
    return sorted(
        (
            (len(decision_ids), ngram, sorted(decision_ids)[:5])
            for ngram, decision_ids in uses.items()
            if len(decision_ids) >= min_decisions
        ),
        key=lambda row: (-row[0], row[1]),
    )


def _collect_prose_field_entries(value: Any, *, path: str = '$'):
    if not isinstance(value, dict):
        return
    for key, child in value.items():
        child_path = f'{path}.{key}'
        if key in PROSE_FIELD_NAMES and isinstance(child, str):
            yield key, child_path, child
        elif isinstance(child, dict):
            yield from _collect_prose_field_entries(child, path=child_path)
        elif isinstance(child, list):
            for index, item in enumerate(child):
                if isinstance(item, dict):
                    yield from _collect_prose_field_entries(item, path=f'{child_path}[{index}]')


def _semantic_slot_values(row: Mapping[str, Any]) -> set[str]:
    values: set[str] = set()

    def visit(value: Any, *, key: str = '', slot_context: bool = False) -> None:
        context = slot_context or key in _SEMANTIC_SLOT_CONTEXT_KEYS
        if isinstance(value, str):
            text = value.strip()
            if text and (context or key in _SEMANTIC_SLOT_EXACT_KEYS or key.endswith('_ref')):
                values.add(text)
                if 'form' in key:
                    spaced = re.sub(r'[_-]+', ' ', text).strip()
                    if spaced:
                        values.add(spaced)
        elif isinstance(value, dict):
            for child_key, child in value.items():
                visit(child, key=str(child_key), slot_context=context)
        elif isinstance(value, list):
            for child in value:
                visit(child, key=key, slot_context=context)

    visit(row)
    return values


def _mask_semantic_slots(text: str, row: Mapping[str, Any]) -> str:
    value = _QUOTED_TEXT_RE.sub(' <slot> ', text)
    for slot in sorted(_semantic_slot_values(row), key=len, reverse=True):
        pattern = rf'(?<!\w){re.escape(slot)}(?!\w)' if len(slot) < 2 else re.escape(slot)
        value = re.sub(pattern, ' <slot> ', value, flags=re.I)
    value = _OSIS_LOCATOR_RE.sub(' <slot> ', value)
    value = _OSIS_SPAN_RE.sub(' <slot> ', value)
    value = _HUMAN_LOCATOR_RE.sub(' <slot> ', value)
    value = _VERSE_LOCATOR_RE.sub(' <slot> ', value)
    value = _HEBREW_LABEL_RE.sub(' <slot> ', value)
    value = re.sub(r'\bM7_sol-[A-Za-z0-9_-]+\b', ' <slot> ', value, flags=re.I)
    return re.sub(r'\s+', ' ', value).strip()


def _residual_fingerprint(text: str, row: Mapping[str, Any]) -> str:
    masked = _mask_semantic_slots(text, row).lower()
    tokens = re.findall(r'<slot>|[a-z0-9]+(?:\x27[a-z]+)?', masked)
    return ' '.join('<number>' if token.isdigit() else token for token in tokens)


def _semantic_constructor_fingerprints(
    rows: list[dict[str, Any]],
    *,
    min_decisions: int = 10,
    min_residual_words: int = 5,
) -> list[tuple[int, str, str, str, list[str]]]:
    uses: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    for row in rows:
        decision_id = str(row.get('decision_id', ''))
        seen: set[tuple[str, str, str]] = set()
        for field, _path, prose in _collect_prose_field_entries(row):
            field_fingerprint = _residual_fingerprint(prose, row)
            form = str(row.get('literary_form') or row.get('local_function') or '').lower()
            formal_acrostic_claim = (
                'oshb uxlc initials' in field_fingerprint
                or (
                    'both hebrew witnesses verify eight' in field_fingerprint
                    and 'no heading element is asserted' in field_fingerprint
                )
            )
            if field == 'claim' and 'alphabetic' in form and formal_acrostic_claim:
                continue
            candidates = [('field', field, field_fingerprint)]
            masked = _mask_semantic_slots(prose, row)
            candidates.extend(
                ('sentence', field, _residual_fingerprint(sentence, row))
                for sentence in re.split(r'(?<=[.!?;])\s+', masked)
            )
            for kind, field_name, fingerprint in candidates:
                tokens = fingerprint.split()
                residual_words = [token for token in tokens if token not in {'<slot>', '<number>'}]
                signature = (kind, field_name, fingerprint)
                if len(residual_words) >= min_residual_words and signature not in seen:
                    uses[signature].add(decision_id)
                    seen.add(signature)
    return sorted(
        (
            (len(decision_ids), kind, field, fingerprint, sorted(decision_ids)[:5])
            for (kind, field, fingerprint), decision_ids in uses.items()
            if len(decision_ids) >= min_decisions
        ),
        key=lambda item: (-item[0], item[1], item[2], item[3]),
    )


def _alias_tokens(text: str) -> str:
    return ' '.join(re.findall(r'[a-z0-9]+(?:\x27[a-z]+)?', text.lower()))


def _embeds_full_prose(candidate: str, source: str, *, min_source_words: int = 10) -> bool:
    candidate_norm = _alias_tokens(candidate)
    source_norm = _alias_tokens(source)
    return len(source_norm.split()) >= min_source_words and source_norm in candidate_norm


def _chunk_prose_aliases(chunk: Mapping[str, Any]) -> list[str]:
    rationale = str(chunk.get('boundary_rationale') or '').strip()
    if not rationale:
        return []
    violations: list[str] = []
    alternative = chunk.get('rejected_alternative')
    if isinstance(alternative, str) and _embeds_full_prose(alternative, rationale):
        violations.append('rejected_alternative embeds the full boundary_rationale')
    for field in (
        'confidence_basis', 'confidence_rationale', 'defensible_basis',
        'convergence_defense_rationale', 'convergence_rationale',
    ):
        value = chunk.get(field)
        if value is None:
            continue
        for candidate in _iter_strings(value):
            if _embeds_full_prose(candidate, rationale) and _embeds_full_prose(rationale, candidate):
                violations.append(f'{field} aliases boundary_rationale')
                break
    return violations


def _normalized_rationale(text: str) -> str:
    value = text.lower()
    value = re.sub(r"[1-4]?[a-z]+\.\d+\.\d+(?:-[1-4]?[a-z]+\.\d+\.\d+)?", "<span>", value)
    value = re.sub(r"m7_sol-[a-z0-9]+-\d+", "<decision>", value)
    value = re.sub(r"\d+", "#", value)
    return re.sub(r"\s+", " ", value).strip()


def _human_question(chunk: dict[str, Any], packet: dict[str, Any]) -> str:
    candidates: list[Any] = [
        packet.get("human_review_question"),
        chunk.get("human_review_question"),
    ]
    candidates.extend(chunk.get("review_holds", []) or [])
    for candidate in candidates:
        if isinstance(candidate, str) and "?" in candidate and len(candidate.strip()) >= 30:
            return candidate.strip()
    return ""


def _chunk_sha256(chunk: dict[str, Any]) -> str:
    payload = json.dumps(chunk, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _source_anchored(refs: Any, span: str) -> bool:
    if not isinstance(refs, list):
        return False
    allowed_sources = {"eng-web", "oshb", "uxlc", "sblgnt", "ugnt", "cntr", "usfm"}
    for ref in refs:
        if isinstance(ref, str):
            direct_parts = ref.split(":", 2)
            if (
                len(direct_parts) == 3
                and direct_parts[0] == "direct_read"
                and direct_parts[1] in allowed_sources
                and direct_parts[2] == span
            ):
                return True
            source_parts = ref.split(":", 1)
            if len(source_parts) == 2:
                source_name, locator = source_parts
                if source_name == "WEB" and locator == span:
                    return True
                if source_name in {"OSHB", "UXLC", "SBLGNT", "UGNT", "CNTR", "USFM"} and locator.endswith(f"#{span}"):
                    return True
        elif isinstance(ref, dict):
            if (
                ref.get("source_id") in allowed_sources
                and ref.get("span") == span
                and _present(ref.get("observation"))
            ):
                return True
    return False


def _wlc_ref_for_web_ref(ref: str) -> str:
    book, chapter_text, verse_text = ref.split(".")
    chapter = int(chapter_text)
    verse = int(verse_text)
    if book == "Dan":
        if chapter == 4 and verse <= 3:
            chapter, verse = 3, verse + 30
        elif chapter == 4:
            verse -= 3
        elif chapter == 5 and verse == 31:
            chapter, verse = 6, 1
        elif chapter == 6:
            verse += 1
    elif book == "Hos":
        if chapter == 1 and verse >= 10:
            chapter, verse = 2, verse - 9
        elif chapter == 2:
            verse += 2
        elif chapter == 11 and verse == 12:
            chapter, verse = 12, 1
        elif chapter == 12:
            verse += 1
        elif chapter == 13 and verse == 16:
            chapter, verse = 14, 1
        elif chapter == 14:
            verse += 1
    else:
        raise ValueError(f"unexpected WEB-to-MT/WLC coordinate {ref!r}")
    return f"{book}.{chapter}.{verse}"


def _wlc_span_for_web_span(span: str) -> str:
    parts = span.split("-")
    if len(parts) != 2:
        raise ValueError(f"invalid full WEB span {span!r}")
    books = {ref.split(".", 1)[0] for ref in parts}
    if len(books) != 1:
        raise ValueError(f"cross-book WEB span is not supported {span!r}")
    return "-".join(_wlc_ref_for_web_ref(ref) for ref in parts)

def _language_source_status(refs: Any, span: str, book: str, verdict: str = "") -> str | None:
    """Classify original-language evidence without manufacturing certainty.

    Psalms, Daniel, and Hosea require explicit WEB-to-MT crosswalks where numbering
    differs. A documented unverified mapping may support only an
    ``insufficient_evidence`` verdict and makes no boundary claim. Other books
    retain exact-span source-family checks.
    """
    if not isinstance(refs, list):
        return None
    required_ids = (
        {"oshb", "uxlc"}
        if book in OT_BOOKS
        else {"sblgnt", "ugnt", "cntr"}
        if book in NT_BOOKS
        else set()
    )
    if not required_ids:
        return "not_applicable"
    if book == "Ps":
        for ref in refs:
            if not isinstance(ref, dict):
                continue
            common = (
                str(ref.get("source_id", "")).lower() in required_ids
                and ref.get("web_span") == span
                and _present(ref.get("observation"))
                and ref.get("source_metadata_boundary_authority") is False
            )
            if (
                common
                and _present(ref.get("source_span"))
                and ref.get("crosswalk_status") == "validated_web_mt_verse_mapping"
            ):
                return "validated_original_language"
            if (
                common
                and verdict == "insufficient_evidence"
                and not _present(ref.get("source_span"))
                and ref.get("crosswalk_status") == "unverified_web_mt_verse_mapping"
                and ref.get("evidence_status") == "source_gap_no_boundary_claim"
            ):
                return "documented_source_gap"
        return None
    if book in {"Dan", "Hos"}:
        expected_source_span = _wlc_span_for_web_span(span)
        validated_ids: set[str] = set()
        for ref in refs:
            if not isinstance(ref, dict):
                continue
            source_id = str(ref.get("source_id", "")).lower()
            if (
                source_id in required_ids
                and ref.get("web_span") == span
                and ref.get("span") == expected_source_span
                and ref.get("source_span") == expected_source_span
                and ref.get("coordinate_system") == "MT_WLC"
                and ref.get("crosswalk_status")
                == "validated_web_mt_verse_mapping"
                and ref.get("source_metadata_boundary_authority") is False
                and _present(ref.get("observation"))
            ):
                validated_ids.add(source_id)
        return (
            "validated_original_language"
            if validated_ids == required_ids
            else None
        )
    required_labels = {source_id.upper() for source_id in required_ids}
    for ref in refs:
        if isinstance(ref, str):
            direct_parts = ref.split(":", 2)
            if (
                len(direct_parts) == 3
                and direct_parts[0] == "direct_read"
                and direct_parts[1].lower() in required_ids
                and direct_parts[2] == span
            ):
                return "validated_original_language"
            source_parts = ref.split(":", 1)
            if (
                len(source_parts) == 2
                and source_parts[0].upper() in required_labels
                and source_parts[1].endswith(f"#{span}")
            ):
                return "validated_original_language"
        elif isinstance(ref, dict):
            if (
                str(ref.get("source_id", "")).lower() in required_ids
                and ref.get("span") == span
                and _present(ref.get("observation"))
            ):
                return "validated_original_language"
    return None


def _has_language_appropriate_source(refs: Any, span: str, book: str, verdict: str = "") -> bool:
    return _language_source_status(refs, span, book, verdict) is not None


def validate(
    model_root: Path,
    book: str,
    *,
    max_attempt_reuse: int = MAX_ATTEMPT_REUSE,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    chunk_path = model_root / "book_chunks" / book / "chunks.jsonl"
    packet_path = model_root / "reviews" / book / "review_packets.jsonl"
    try:
        chunks = _read_jsonl(chunk_path)
        packets = _read_jsonl(packet_path)
        canonical_web_witnesses = _load_web_translation_witnesses()
    except ValueError as exc:
        return [str(exc)], {}

    chunk_by_id = {str(row.get("decision_id", "")): row for row in chunks}
    packet_by_id = {str(row.get("decision_id", "")): row for row in packets}
    if "" in chunk_by_id or len(chunk_by_id) != len(chunks):
        errors.append(f"{book}: chunk decision IDs must be unique and non-empty")
    if "" in packet_by_id or len(packet_by_id) != len(packets):
        errors.append(f"{book}: packet decision IDs must be unique and non-empty")
    if set(chunk_by_id) != set(packet_by_id):
        errors.append(f"{book}: chunk/packet decision sets differ")

    rationale_groups: dict[str, list[str]] = defaultdict(list)
    confidences: Counter[str] = Counter()
    final_states: Counter[str] = Counter()
    verdicts: Counter[str] = Counter()
    role_verdicts: dict[str, Counter[str]] = defaultdict(Counter)
    role_documented_source_gaps: Counter[str] = Counter()
    attempt_uses: Counter[str] = Counter()
    chapter_forms: dict[str, list[str]] = defaultdict(list)
    generic_forms: list[str] = []
    templated_rationales: list[str] = []
    encoding_corrupt_chunks: list[str] = []
    encoding_corrupt_packets: list[str] = []
    truncated_quote_chunks: list[str] = []
    batch_shell_decisions: dict[str, list[str]] = defaultdict(list)
    packet_batch_shell_decisions: dict[str, list[str]] = defaultdict(list)
    midpoint_alternative_count = 0
    exact_midpoint_alternative_count = 0
    structured_web_quotes_checked = 0
    structured_web_quote_failures = 0

    for decision_id, chunk in chunk_by_id.items():
        prefix = f"{book} {decision_id}"
        quote_errors, quote_count = _validate_structured_web_quote_fidelity(
            chunk,
            canonical_web_witnesses,
        )
        structured_web_quotes_checked += quote_count
        structured_web_quote_failures += len(quote_errors)
        errors.extend(f"{prefix}: {error}" for error in quote_errors)
        if _has_question_mark_encoding_corruption(chunk):
            encoding_corrupt_chunks.append(decision_id)
        chunk_strings = list(_iter_strings(chunk))
        if any(TRUNCATED_QUOTE_RE.search(value) for value in chunk_strings):
            truncated_quote_chunks.append(decision_id)
        for shell_name, shell_pattern in BATCH_PROSE_SHELL_PATTERNS.items():
            if any(shell_pattern.search(value) for value in chunk_strings):
                batch_shell_decisions[shell_name].append(decision_id)
        form = str(chunk.get("literary_form") or chunk.get("literature_type_guess") or "").strip()
        if not form:
            errors.append(f"{prefix}: real literary form is required")
        elif any(pattern.search(form) for pattern in GENERIC_FORM_PATTERNS):
            generic_forms.append(decision_id)
        span_chapter_match = re.match(r"[1-4]?[A-Za-z]+\.(\d+)\.", str(chunk.get("span", "")))
        if span_chapter_match:
            chapter_forms[span_chapter_match.group(1)].append(form)
        if book == "Ps" and str(chunk.get("span", "")).startswith("Ps.119.") and not ({"acrostic", "alphabetic"} & set(re.split(r"[_ -]+", form.lower()))):
            errors.append(f"{prefix}: Psalm 119 stanza form must name the acrostic evidence")

        rationale = str(chunk.get("boundary_rationale") or "").strip()
        if len(rationale) < 80:
            errors.append(f"{prefix}: boundary_rationale is too thin to be decision-specific")
        if any(pattern.search(rationale) for pattern in TEMPLATE_RATIONALE_PATTERNS):
            templated_rationales.append(decision_id)
        if rationale:
            rationale_groups[_normalized_rationale(rationale)].append(decision_id)
        for alias_error in _chunk_prose_aliases(chunk):
            errors.append(f'{prefix}: {alias_error}')
        for field in ("deciding_marker_or_seam", "rejected_alternative", "defensible_basis"):
            if not _present(chunk.get(field)):
                errors.append(f"{prefix}: missing convergence-defense field {field}")
        span_match = re.fullmatch(r"[1-4]?[A-Za-z]+\.(\d+)\.(\d+)-[1-4]?[A-Za-z]+\.\1\.(\d+)", str(chunk.get("span", "")))
        alternative_match = re.search(
            r"rejected subdividing .*? at verse (\d+)\b",
            str(chunk.get("rejected_alternative", "")),
            re.I,
        )
        if span_match and alternative_match:
            midpoint_alternative_count += 1
            start_verse = int(span_match.group(2))
            end_verse = int(span_match.group(3))
            if int(alternative_match.group(1)) == (start_verse + end_verse) // 2:
                exact_midpoint_alternative_count += 1
        confidences[str(chunk.get("confidence", ""))] += 1

    if encoding_corrupt_chunks:
        errors.append(
            f"{book}: probable quote/Unicode or doubled-terminal punctuation corruption in chunks: "
            f"{encoding_corrupt_chunks[:12]}"
        )
    if truncated_quote_chunks:
        errors.append(
            f"{book}: probable clipped source quotation ends on a stopword in chunks: "
            f"{truncated_quote_chunks[:12]}"
        )
    pervasive_shells = {
        name: ids
        for name, ids in batch_shell_decisions.items()
        if name in ZERO_TOLERANCE_BATCH_PROSE_SHELLS or len(ids) >= 10
    }
    if pervasive_shells:
        errors.append(
            f"{book}: repeated prose-shell substitution signature remains: "
            f"{[(name, len(ids), ids[:5]) for name, ids in sorted(pervasive_shells.items())]}"
        )
    chunk_prose_ngrams = _pervasive_prose_ngrams(chunks)
    if chunk_prose_ngrams:
        errors.append(
            f"{book}: repeated seven-word chunk-prose n-grams remain across >=10 decisions: "
            f"{chunk_prose_ngrams[:12]}"
        )
    chunk_semantic_fingerprints = _semantic_constructor_fingerprints(chunks)
    if chunk_semantic_fingerprints:
        errors.append(
            f'{book}: repeated slot-masked semantic chunk constructors remain across >=10 decisions: '
            f'{chunk_semantic_fingerprints[:12]}'
        )
    if generic_forms:
        errors.append(f"{book}: generic literary form labels remain: {generic_forms[:12]}")
    if templated_rationales:
        errors.append(f"{book}: templated boundary rationales remain: {templated_rationales[:12]}")
    duplicate_groups = [ids for ids in rationale_groups.values() if len(ids) > 1]
    if duplicate_groups:
        errors.append(f"{book}: normalized duplicate rationales remain: {duplicate_groups[:5]}")
    if (
        midpoint_alternative_count >= 10
        and exact_midpoint_alternative_count * 5 >= midpoint_alternative_count * 4
    ):
        errors.append(
            f"{book}: rejected alternatives show a mechanical midpoint batch signature: "
            f"exact_midpoint={exact_midpoint_alternative_count}/{midpoint_alternative_count}"
        )
    segmented_chapters = {chapter: forms for chapter, forms in chapter_forms.items() if len(forms) > 1}
    uniform_segmented_chapters = {
        chapter: forms[0]
        for chapter, forms in segmented_chapters.items()
        if len(set(forms)) == 1
    }
    if (
        len(segmented_chapters) >= 5
        and len(uniform_segmented_chapters) * 5 >= len(segmented_chapters) * 4
    ):
        errors.append(
            f"{book}: segmented units show a copied parent-form batch signature: "
            f"uniform={len(uniform_segmented_chapters)}/{len(segmented_chapters)}"
        )

    for decision_id, packet in packet_by_id.items():
        chunk = chunk_by_id.get(decision_id, {})
        prefix = f"{book} {decision_id}"
        quote_errors, quote_count = _validate_structured_web_quote_fidelity(
            packet,
            canonical_web_witnesses,
        )
        structured_web_quotes_checked += quote_count
        structured_web_quote_failures += len(quote_errors)
        errors.extend(f"{prefix}: {error}" for error in quote_errors)
        if _has_question_mark_encoding_corruption(packet):
            encoding_corrupt_packets.append(decision_id)
        packet_strings = list(_iter_strings(packet))
        for shell_name, shell_pattern in PACKET_BATCH_PROSE_SHELL_PATTERNS.items():
            if any(shell_pattern.search(value) for value in packet_strings):
                packet_batch_shell_decisions[shell_name].append(decision_id)
        for shell_name in ZERO_TOLERANCE_BATCH_PROSE_SHELLS:
            shell_pattern = BATCH_PROSE_SHELL_PATTERNS[shell_name]
            if any(shell_pattern.search(value) for value in packet_strings):
                packet_batch_shell_decisions[f'known_constructor:{shell_name}'].append(decision_id)
        span = str(chunk.get("span", ""))
        expected_chunk_sha = _chunk_sha256(chunk)
        if packet.get("schema_version") != PACKET_SCHEMA:
            errors.append(f"{prefix}: packet schema_version must be {PACKET_SCHEMA}")
        if packet.get("book") != book or packet.get("span") != span:
            errors.append(f"{prefix}: packet book/span must match the current chunk")
        if packet.get("review_revision") != REVIEW_REVISION:
            errors.append(f"{prefix}: packet review_revision must be {REVIEW_REVISION}")
        if packet.get("chunk_content_sha256") != expected_chunk_sha:
            errors.append(f"{prefix}: packet chunk_content_sha256 is stale or missing")

        final_state = str(packet.get("final_state", ""))
        final_states[final_state] += 1
        reviews = packet.get("primary_reviews")
        if not isinstance(reviews, list) or len(reviews) < 2:
            errors.append(f"{prefix}: at least two primary reviews are required")
            reviews = []
        packet_attempts: set[str] = set()
        packet_roles: set[str] = set()
        challenge_ids: list[str] = []
        for index, review in enumerate(reviews, 1):
            if not isinstance(review, dict):
                errors.append(f"{prefix}: primary review {index} is not an object")
                continue
            attempt_id = str(review.get("reviewer_attempt_id", "")).strip()
            role = str(review.get("reviewer_role") or review.get("role") or "").strip()
            if not attempt_id or attempt_id in packet_attempts:
                errors.append(f"{prefix}: primary attempt IDs must be non-empty and distinct")
            if not role or role in packet_roles:
                errors.append(f"{prefix}: primary roles must be non-empty and distinct")
            packet_attempts.add(attempt_id)
            packet_roles.add(role)
            attempt_uses[attempt_id] += 1
            verdict = str(review.get("verdict", ""))
            verdicts[verdict] += 1
            role_verdicts[role][verdict] += 1
            if verdict not in VALID_VERDICTS:
                errors.append(f"{prefix}: invalid primary verdict {verdict!r}")
            review_refs = review.get("source_refs") or review.get("evidence_refs")
            if not _source_anchored(review_refs, span):
                errors.append(f"{prefix}: primary review {attempt_id} lacks a resolved exact-span source reference")
            if ORIGINAL_LANGUAGE_ROLE_RE.search(role):
                language_status = _language_source_status(review_refs, span, book, verdict)
                if language_status is None:
                    errors.append(
                        f"{prefix}: original-language primary {attempt_id} lacks a language-appropriate source or structured source-gap record"
                    )
                elif language_status == "documented_source_gap":
                    role_documented_source_gaps[role] += 1
            if review.get("blind_to_other_primary_reviews") is not True:
                errors.append(f"{prefix}: primary review {attempt_id} must attest blind_to_other_primary_reviews=true")
            if review.get("evidence_only") is not True:
                errors.append(f"{prefix}: primary review {attempt_id} must attest evidence_only=true")
            if not _present(review.get("counterevidence")):
                errors.append(f"{prefix}: primary review {attempt_id} lacks explicit counterevidence")
            challenges = review.get("challenges", [])
            if not isinstance(challenges, list):
                errors.append(f"{prefix}: primary review {attempt_id} challenges must be a list")
                challenges = []
            for challenge in challenges:
                if not isinstance(challenge, dict):
                    errors.append(f"{prefix}: primary review {attempt_id} has a non-object challenge")
                    continue
                challenge_id = str(challenge.get("challenge_id", "")).strip()
                if not challenge_id or challenge_id in challenge_ids:
                    errors.append(f"{prefix}: challenge IDs must be non-empty and unique")
                challenge_ids.append(challenge_id)
                for field in ("claim", "proposed_remedy", "counterevidence"):
                    if not _present(challenge.get(field)):
                        errors.append(f"{prefix}: challenge {challenge_id!r} missing {field}")
                if not _source_anchored(challenge.get("source_refs") or challenge.get("evidence_refs"), span):
                    errors.append(f"{prefix}: challenge {challenge_id!r} lacks exact-span source evidence")

        independence = packet.get("independence_scope")
        required_independence = {
            "independent_from_sibling_model_maps": True,
            "primaries_blind_to_each_other_artifacts": True,
            "roles_separated": True,
            "shared_model_substrate": True,
            "counts_as_cross_model_independent_votes": False,
            "independent_model_or_human_evidence_required_at_convergence": True,
            "reviewer_count_is_not_authority": True,
        }
        if not isinstance(independence, dict):
            errors.append(f"{prefix}: independence_scope disclosure is required")
        else:
            for field, expected in required_independence.items():
                if independence.get(field) is not expected:
                    errors.append(f"{prefix}: independence_scope {field} must be {str(expected).lower()}")

        mesh_identity_ids = set(packet_attempts)
        peer = packet.get("peer_crosscheck")
        if not isinstance(peer, dict):
            errors.append(f"{prefix}: peer_crosscheck is required")
        else:
            peer_id = str(peer.get("reviewer_attempt_id", "")).strip()
            peer_role = str(peer.get("reviewer_role") or peer.get("role") or "").strip()
            peer_rationale = peer.get("rationale") or peer.get("support")
            if not peer_id or not peer_role or not _present(peer_rationale) or not _present(peer.get("counterevidence")):
                errors.append(f"{prefix}: peer_crosscheck needs an attempt ID, role, rationale, and counterevidence")
            else:
                if peer_id in mesh_identity_ids:
                    errors.append(f"{prefix}: peer attempt identity must be distinct from the primaries")
                mesh_identity_ids.add(peer_id)
                attempt_uses[peer_id] += 1
            if not _source_anchored(peer.get("source_refs") or peer.get("evidence_refs"), span):
                errors.append(f"{prefix}: peer_crosscheck lacks exact-span source evidence")

        post = packet.get("post_resolution_check")
        if not isinstance(post, dict):
            errors.append(f"{prefix}: post_resolution_check is required")
        else:
            post_id = str(post.get("checker_attempt_id", "")).strip()
            if not post_id or not _present(post.get("status")):
                errors.append(f"{prefix}: post_resolution_check needs a checker ID and status")
            else:
                if post_id in mesh_identity_ids:
                    errors.append(f"{prefix}: post-resolution checker identity must be distinct from primaries and peer")
                mesh_identity_ids.add(post_id)
                attempt_uses[post_id] += 1
            if post.get("chunk_content_sha256") != expected_chunk_sha:
                errors.append(f"{prefix}: post-resolution chunk hash is stale or missing")

        resolution = packet.get("sol_resolution")
        if not isinstance(resolution, dict):
            errors.append(f"{prefix}: sol_resolution must be an object")
            resolution = {}
        author_attempt_id = str(resolution.get("author_attempt_id", "")).strip()
        if not author_attempt_id:
            errors.append(f"{prefix}: sol_resolution author_attempt_id is required")
        elif author_attempt_id in mesh_identity_ids:
            errors.append(f"{prefix}: author/boss identity must be distinct from primaries, peer, and postchecker")
        responses = resolution.get("challenge_responses", [])
        if not isinstance(responses, list):
            errors.append(f"{prefix}: challenge_responses must be a list")
            responses = []
        response_ids: list[str] = []
        for response in responses:
            if not isinstance(response, dict):
                errors.append(f"{prefix}: challenge response is not an object")
                continue
            response_id = str(response.get("challenge_id", "")).strip()
            response_ids.append(response_id)
            for field in ("disposition", "rationale", "rejected_alternative"):
                if not _present(response.get(field)):
                    errors.append(f"{prefix}: response to {response_id!r} missing {field}")
        if Counter(challenge_ids) != Counter(response_ids):
            errors.append(f"{prefix}: every primary challenge needs exactly one author response")

        boss = packet.get("boss_ruling")
        if not isinstance(boss, dict):
            errors.append(f"{prefix}: decision-local boss_ruling is required")
        else:
            ruling_id = str(boss.get("ruling_id", "")).strip()
            if not ruling_id:
                errors.append(f"{prefix}: boss_ruling ruling_id is required")
            elif ruling_id != author_attempt_id and ruling_id in mesh_identity_ids:
                errors.append(f"{prefix}: boss identity must be distinct from primaries, peer, and postchecker")
            for field in ("rationale", "counterevidence", "rejected_alternative"):
                if not _present(boss.get(field)):
                    errors.append(f"{prefix}: boss_ruling missing {field}")
            if not _present(boss.get("outcome") or boss.get("ruling")):
                errors.append(f"{prefix}: boss_ruling missing outcome")

        unresolved = resolution.get("unresolved_claim_ids", [])
        if not isinstance(unresolved, list):
            errors.append(f"{prefix}: unresolved_claim_ids must be a list")
            unresolved = []
        appeals = packet.get("appeals", [])
        if not isinstance(appeals, list):
            errors.append(f"{prefix}: appeals must be a list")
            appeals = []
        chunk_held = chunk.get("candidate_hold_state") == "deferred_human_or_external_ai"
        if final_state == ACCEPTED:
            if unresolved or appeals:
                errors.append(f"{prefix}: accepted decision retains unresolved claims or appeals")
            if chunk_held:
                errors.append(f"{prefix}: accepted packet conflicts with chunk candidate_hold_state")
            if not any(isinstance(r, dict) and r.get("verdict") in {"support", "supports"} for r in reviews):
                errors.append(f"{prefix}: accepted decision has no supporting primary verdict")
        elif final_state in HELD:
            if not chunk_held or not _present(chunk.get("candidate_hold_basis")):
                errors.append(f"{prefix}: held packet needs matching chunk hold state and basis")
            if not _human_question(chunk, packet):
                errors.append(f"{prefix}: held decision lacks a specific answerable human question")
            if not _present(packet.get("human_review_route") or packet.get("requested_reviewer")):
                errors.append(f"{prefix}: held decision lacks a routed human/external reviewer")
            if not unresolved and not appeals:
                errors.append(f"{prefix}: held decision needs a specific unresolved claim or preserved appeal")
        else:
            errors.append(f"{prefix}: invalid final_state {final_state!r}")
    if encoding_corrupt_packets:
        errors.append(
            f"{book}: probable quote/Unicode or doubled-terminal punctuation corruption in review packets: "
            f"{encoding_corrupt_packets[:12]}"
        )
    pervasive_packet_shells = {
        name: ids
        for name, ids in packet_batch_shell_decisions.items()
        if ids
    }
    if pervasive_packet_shells:
        errors.append(
            f"{book}: repeated review-prose substitution signature remains: "
            f"{[(name, len(ids), ids[:5]) for name, ids in sorted(pervasive_packet_shells.items())]}"
        )
    packet_prose_ngrams = _pervasive_prose_ngrams(packets)
    if packet_prose_ngrams:
        errors.append(
            f"{book}: repeated seven-word review-prose n-grams remain across >=10 decisions: "
            f"{packet_prose_ngrams[:12]}"
        )
    packet_semantic_fingerprints = _semantic_constructor_fingerprints(packets)
    if packet_semantic_fingerprints:
        errors.append(
            f'{book}: repeated slot-masked semantic review constructors remain across >=10 decisions: '
            f'{packet_semantic_fingerprints[:12]}'
        )
    overused = {attempt: count for attempt, count in attempt_uses.items() if count > max_attempt_reuse}
    if overused:
        sample = sorted(overused.items(), key=lambda item: (-item[1], item[0]))[:12]
        errors.append(f"{book}: reviewer/checker attempt IDs exceed passage-cluster ceiling {max_attempt_reuse}: {sample}")
    deterministic_roles = {
        role: dict(counts)
        for role, counts in role_verdicts.items()
        if (
            sum(counts.values()) >= 10
            and len([count for count in counts.values() if count]) == 1
            and not (
                set(counts) == {"insufficient_evidence"}
                and role_documented_source_gaps[role] == sum(counts.values())
            )
        )
    }
    if deterministic_roles:
        errors.append(f"{book}: primary role verdicts are mechanically uniform: {deterministic_roles}")

    accepted = final_states[ACCEPTED]
    held = sum(final_states[state] for state in HELD)
    medium_high = sum(confidences[level] for level in MEDIUM_HIGH)
    if accepted <= held:
        errors.append(f"{book}: accepted decisions must be the defensible majority; accepted={accepted} held={held}")
    if medium_high * 2 <= len(chunks):
        errors.append(f"{book}: medium/high confidence must be the majority; medium_high={medium_high} total={len(chunks)}")
    if len([level for level, count in confidences.items() if count]) < 2:
        errors.append(f"{book}: uniform confidence is a corrective-review smell: {dict(confidences)}")
    if verdicts["support"] + verdicts["supports"] == 0 or verdicts["challenge"] == 0:
        errors.append(f"{book}: primary review needs a real supports/challenge mix: {dict(verdicts)}")

    summary = {
        "book": book,
        "chunks": len(chunks),
        "accepted": accepted,
        "held": held,
        "confidence": dict(sorted(confidences.items())),
        "primary_verdicts": dict(sorted(verdicts.items())),
        "unique_attempt_ids": len(attempt_uses),
        "max_attempt_reuse": max(attempt_uses.values(), default=0),
        "templated_rationales": len(templated_rationales),
        "generic_forms": len(generic_forms),
        "encoding_corrupt_chunks": len(encoding_corrupt_chunks),
        "encoding_corrupt_packets": len(encoding_corrupt_packets),
        "truncated_quote_chunks": len(truncated_quote_chunks),
        "structured_web_quotes_checked": structured_web_quotes_checked,
        "structured_web_quote_failures": structured_web_quote_failures,
        "pervasive_batch_shells": {name: len(ids) for name, ids in sorted(pervasive_shells.items())},
        "pervasive_review_batch_shells": {name: len(ids) for name, ids in sorted(pervasive_packet_shells.items())},
        "chunk_prose_ngram_violations": len(chunk_prose_ngrams),
        "review_prose_ngram_violations": len(packet_prose_ngrams),
        "max_chunk_prose_ngram_reuse": chunk_prose_ngrams[0][0] if chunk_prose_ngrams else 0,
        "max_review_prose_ngram_reuse": packet_prose_ngrams[0][0] if packet_prose_ngrams else 0,
        "midpoint_alternatives": midpoint_alternative_count,
        "exact_midpoint_alternatives": exact_midpoint_alternative_count,
        "segmented_chapters": len(segmented_chapters),
        "uniform_segmented_chapter_forms": len(uniform_segmented_chapters),
        "role_verdicts": {role: dict(sorted(counts.items())) for role, counts in sorted(role_verdicts.items())},
        "role_documented_source_gaps": dict(sorted(role_documented_source_gaps.items())),
        "candidate_only": True,
        "non_authorizing": True,
        'semantic_chunk_constructor_count': len(chunk_semantic_fingerprints),
        'semantic_review_constructor_count': len(packet_semantic_fingerprints),
    }
    return errors, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-root", type=Path, default=DEFAULT_MODEL_ROOT)
    parser.add_argument("--book", required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-errors", type=int, default=100)
    args = parser.parse_args()
    errors, summary = validate(args.model_root, args.book)
    if errors:
        visible_errors = errors[: max(args.max_errors, 0)]
        for error in visible_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        hidden_count = len(errors) - len(visible_errors)
        if hidden_count:
            print(f"ERROR: ... {hidden_count} additional error(s) omitted", file=sys.stderr)
        if args.json:
            print(
                json.dumps(
                    {
                        "status": "fail",
                        "summary": summary,
                        "errors": visible_errors,
                        "omitted_error_count": hidden_count,
                    },
                    indent=2,
                )
            )
        return 1
    if args.json:
        print(json.dumps({"status": "pass", "summary": summary}, indent=2))
    else:
        print(f"OK: {args.book} corrective review depth")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
