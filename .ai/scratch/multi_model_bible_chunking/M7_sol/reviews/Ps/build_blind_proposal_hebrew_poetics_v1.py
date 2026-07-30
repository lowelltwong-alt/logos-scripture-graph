"""Build the blind Hebrew/textual/poetics primary proposal for Psalms.

Candidate-only. This builder reads the local WEB Psalm USFM only to prove exact
ordered verse coverage. It does not read any M7 Psalm chunk map or peer proposal.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
WEB = ROOT / "data/processed/bible/eng-web/usfm/extracted/20-PSAeng-web.usfm"
OUT = Path(__file__).with_name("blind_proposal_hebrew_poetics_v1.json")


# Whole psalms are genuine outer literary units. Only these extended or strongly
# multipart psalms receive internal proposed units.
SPLITS: dict[int, tuple[list[tuple[int, int]], str]] = {
    18: ([(1, 3), (4, 19), (20, 30), (31, 45), (46, 50)],
         "opening invocation; distress/theophanic rescue; evaluated deliverance; victory recital; closing praise"),
    22: ([(1, 11), (12, 21), (22, 31)],
         "lament and remembered trust; intensified petition; assembly thanksgiving and widening praise"),
    31: ([(1, 8), (9, 18), (19, 24)],
         "refuge petition and trust; distress and enemy pressure; praise/exhortation"),
    35: ([(1, 10), (11, 18), (19, 28)],
         "three renewed complaint-petition-vow movements"),
    37: ([(1, 11), (12, 22), (23, 31), (32, 40)],
         "alphabetic wisdom movements: fret/exhortation; wicked/righteous contrast; ordered way; final contrast and refuge"),
    42: ([(1, 5), (6, 11)],
         "two lament cycles closed by the repeated self-address refrain"),
    44: ([(1, 8), (9, 16), (17, 22), (23, 26)],
         "ancestral recital/confession; present reversal; protest of fidelity; urgent communal petition"),
    45: ([(1, 9), (10, 15), (16, 17)],
         "royal address; bride/procession address; dynastic closing blessing"),
    46: ([(1, 3), (4, 7), (8, 11)],
         "three strophes articulated by Selah/refrain evidence"),
    49: ([(1, 4), (5, 12), (13, 20)],
         "wisdom summons; first mortality exposition; second folly/mortality exposition"),
    50: ([(1, 6), (7, 15), (16, 23)],
         "divine appearance/court summons; address concerning sacrifice; address to the wicked and closure"),
    51: ([(1, 6), (7, 12), (13, 17), (18, 19)],
         "confession; cleansing/renewal petition; teaching/praise vow; Zion-sacrifice coda"),
    55: ([(1, 8), (9, 15), (16, 23)],
         "distress and escape wish; city/betrayal complaint; prayer-confidence-exhortation"),
    57: ([(1, 5), (6, 11)],
         "two movements closed by the repeated exaltation refrain"),
    59: ([(1, 9), (10, 17)],
         "two enemy-petition/confidence cycles with related fortress refrains"),
    62: ([(1, 4), (5, 8), (9, 12)],
         "quiet-confidence refrain cycle; renewed self-address and communal exhortation; human transience and divine recompense"),
    66: ([(1, 7), (8, 12), (13, 20)],
         "worldwide praise; communal testing/deliverance; individual vow/testimony"),
    68: ([(1, 6), (7, 18), (19, 27), (28, 35)],
         "opening summons; wilderness/Sinai/procession recital; daily deliverance and liturgical procession; kingdoms summons and closing praise"),
    69: ([(1, 12), (13, 18), (19, 29), (30, 36)],
         "distress/alienation complaint; petition for rescue; reproach/imprecation petition; praise and Zion closure"),
    71: ([(1, 8), (9, 16), (17, 24)],
         "refuge from youth; old-age petition; lifelong praise vow"),
    73: ([(1, 12), (13, 17), (18, 28)],
         "problem of the prosperous wicked; speaker crisis and sanctuary turn; reassessment and confession"),
    74: ([(1, 11), (12, 17), (18, 23)],
         "communal ruin complaint; creation-kingship remembrance; covenant petition"),
    77: ([(1, 9), (10, 15), (16, 20)],
         "lament and unanswered questions; remembrance turn; waters/exodus theophany"),
    78: ([(1, 8), (9, 31), (32, 39), (40, 55), (56, 64), (65, 72)],
         "didactic prologue; Ephraim/wilderness rebellion; failed response and compassion; exodus-to-land recital; renewed rebellion/judgment; final election/pastoral close"),
    80: ([(1, 7), (8, 14), (15, 19)],
         "communal plea/refrain; vine recital; renewed vine petition and final refrain"),
    81: ([(1, 7), (8, 16)],
         "festival summons and deliverance remembrance; divine oracle of admonition and unrealized blessing"),
    83: ([(1, 8), (9, 18)],
         "coalition complaint; historical analogy and petition"),
    89: ([(1, 18), (19, 37), (38, 45), (46, 51), (52, 52)],
         "hymnic covenant frame; oracle recital; present royal reversal; lament-petition; Book III doxology"),
    90: ([(1, 6), (7, 12), (13, 17)],
         "eternal refuge/human transience; wrath and wisdom petition; compassion/work petition"),
    94: ([(1, 7), (8, 15), (16, 23)],
         "appeal against oppressors; wisdom rebuke and assurance; personal testimony and judgment close"),
    95: ([(1, 7), (8, 11)],
         "worship summons; divine warning oracle"),
    102: ([(1, 11), (12, 22), (23, 28)],
          "individual affliction; Zion/nations confidence; shortened-life petition and enduring creator close"),
    104: ([(1, 9), (10, 18), (19, 26), (27, 35)],
          "cosmic ordering; habitats/provision; times/sea creatures; dependence, renewal, and praise"),
    105: ([(1, 15), (16, 25), (26, 36), (37, 45)],
          "praise and patriarchal promise; Joseph movement; Moses/plagues movement; exodus-land-law close"),
    106: ([(1, 5), (6, 12), (13, 23), (24, 33), (34, 46), (47, 48)],
          "praise/confession frame; sea rebellion; wilderness/idol rebellion; land/refusal/Meribah; Canaan apostasy and compassion; restoration petition and Book IV doxology"),
    107: ([(1, 9), (10, 16), (17, 22), (23, 32), (33, 43)],
          "desert wanderers; prisoners; sick sufferers; sailors; providential reversal and wisdom close"),
    109: ([(1, 5), (6, 20), (21, 31)],
          "complaint; extended imprecation; personal petition and praise vow"),
    118: ([(1, 4), (5, 18), (19, 27), (28, 29)],
          "responsive thanksgiving summons; distress/deliverance testimony; gate/procession liturgy; personal thanksgiving and repeated close"),
    119: ([(1 + 8*i, 8 + 8*i) for i in range(22)],
          "twenty-two explicit alphabetic octets: Aleph through Tav"),
    135: ([(1, 4), (5, 14), (15, 21)],
          "praise summons/election; creation/exodus/land recital; idol contrast and responsive blessing"),
    136: ([(1, 3), (4, 9), (10, 16), (17, 22), (23, 26)],
          "opening thanksgiving; creation; exodus/wilderness; kings/land; remembered provision and closing thanks, each line carrying the recurring response"),
    137: ([(1, 4), (5, 6), (7, 9)],
          "Babylon remembrance/refusal; Jerusalem self-imprecation; Edom/Babylon imprecation"),
    139: ([(1, 6), (7, 12), (13, 18), (19, 24)],
          "divine knowledge; inescapable presence; embodied formation; enemies and self-examination"),
    144: ([(1, 8), (9, 11), (12, 15)],
          "warrior-deliverance petition; new-song vow and renewed rescue; communal flourishing beatitude"),
    145: ([(1, 7), (8, 13), (14, 21)],
          "alphabetic praise of greatness; gracious kingdom; sustaining nearness and universal close"),
    147: ([(1, 6), (7, 11), (12, 20)],
          "restoration/creation praise; provision praise; Jerusalem/word/Torah praise, with LXX split-numbering hold"),
}

ACROSTIC_WHOLE = {9, 10, 25, 34, 111, 112}
REFRAIN_WHOLE = {43, 67, 99}
COLLECTION_DOXOLOGIES = {41, 72, 89, 106, 150}


def web_verses() -> dict[int, list[int]]:
    text = WEB.read_text(encoding="utf-8")
    out: dict[int, list[int]] = {}
    chapter: int | None = None
    for line in text.splitlines():
        cm = re.match(r"\\c\s+(\d+)", line)
        if cm:
            chapter = int(cm.group(1))
            out[chapter] = []
        vm = re.match(r"\\v\s+(\d+)", line)
        if vm and chapter is not None:
            out[chapter].append(int(vm.group(1)))
    return out


def make_chunks(verses: dict[int, list[int]]) -> list[dict[str, object]]:
    chunks: list[dict[str, object]] = []
    index = 0
    letters = [
        "Aleph", "Beth", "Gimel", "Daleth", "He", "Vav", "Zayin", "Heth",
        "Teth", "Yodh", "Kaph", "Lamedh", "Mem", "Nun", "Samekh", "Ayin",
        "Pe", "Tsadhe", "Qoph", "Resh", "Shin", "Tav",
    ]
    for psalm in range(1, 151):
        last = max(verses[psalm])
        units = SPLITS.get(psalm, ([(1, last)], "complete psalm poem"))[0]
        profile = SPLITS.get(psalm, ([], "complete psalm poem"))[1]
        for movement, (start, end) in enumerate(units, 1):
            index += 1
            whole = f"{psalm}:1-{psalm}:{last}"
            span = f"{psalm}:{start}-{psalm}:{end}"
            internally_split = len(units) > 1
            if psalm == 119:
                letter = letters[movement - 1]
                form = f"alphabetic Torah-poem stanza ({letter})"
                marker = (
                    f"explicit {letter} acrostic octet, eight consecutive WEB verses "
                    f"{span}; each Hebrew line begins with the stanza letter"
                )
                confidence = "HIGH"
                risk = "alphabetic_stanza_translation_and_mt_superscription_numbering"
            elif internally_split:
                form = f"extended psalm movement {movement} of {len(units)}"
                marker = (
                    f"{span} is movement {movement} in the independently visible sequence: "
                    f"{profile}; preserve {whole} as the governing parent"
                )
                confidence = "LOW"
                risk = "poetic_strophe_refrain_speaker_or_liturgical_seam_disputed"
            else:
                if psalm in ACROSTIC_WHOLE:
                    form = "complete alphabetic/acrostic wisdom or praise psalm"
                    risk = "acrostic_irregularity_and_psalm_9_10_numbering_relation"
                elif psalm in REFRAIN_WHOLE:
                    form = "complete refrain-shaped psalm"
                    risk = "refrain_evidence_without_mandatory_internal_split"
                elif psalm in COLLECTION_DOXOLOGIES:
                    form = "complete psalm with collection-closing doxological function"
                    risk = "collection_doxology_attachment"
                else:
                    form = "complete canonical psalm poem"
                    risk = "superscription_speaker_genre_and_versification_hold"
                marker = (
                    f"canonical Psalm {psalm} incipit through its closure ({whole}); "
                    "no internal marker was judged strong enough to outweigh whole-poem context"
                )
                confidence = "MEDIUM" if risk != "superscription_speaker_genre_and_versification_hold" else "HIGH"
            rejected = (
                f"{whole} as one larger coherent parent"
                if internally_split
                else f"any smaller stanza division within {whole}; retain the complete psalm"
            )
            chunks.append({
                "index": index,
                "span": span,
                "literary_form": form,
                "deciding_marker": marker,
                "rejected_alternative": rejected,
                "confidence": confidence,
                "risk": risk,
            })
    return chunks


def verify(chunks: list[dict[str, object]], verses: dict[int, list[int]]) -> None:
    expected = [(p, v) for p in range(1, 151) for v in verses[p]]
    actual: list[tuple[int, int]] = []
    for row in chunks:
        m = re.fullmatch(r"(\d+):(\d+)-(\d+):(\d+)", str(row["span"]))
        assert m and m.group(1) == m.group(3)
        psalm, start, end = int(m.group(1)), int(m.group(2)), int(m.group(4))
        actual.extend((psalm, v) for v in range(start, end + 1))
    assert actual == expected, (len(actual), len(expected))
    assert [row["index"] for row in chunks] == list(range(1, len(chunks) + 1))


def main() -> None:
    verses = web_verses()
    chunks = make_chunks(verses)
    verify(chunks, verses)
    proposal = {
        "schema_version": "m7_blind_primary_review.v1",
        "proposal_id": "M7-sol-Ps-hebrew-poetics-primary-20260723-v1",
        "book": "Ps",
        "model_id": "M7_sol",
        "role": "hebrew_textual_poetics_specialist",
        "artifact_class": "candidate_only_non_authorizing",
        "review_status": "blind_primary_complete",
        "independence_declaration": {
            "read_only": True,
            "read": [
                "book_strategy/Ps.md",
                "review_contract.yaml and local chunking/context policies",
                "direct canonical WEB Psalms USFM",
                "direct OSHB Psalms",
                "direct UXLC Psalms",
            ],
            "not_read": [
                "current or fallback M7_sol Psalm chunk map",
                "other Psalm primary proposals",
                "M1-M6 maps",
                "comparison/",
                "T417 layers",
            ],
            "shared_model_substrate": True,
            "counts_as_cross_model_independent_vote": False,
        },
        "non_authorizations": [
            "reviewed_gold",
            "chunk_output_promotion",
            "theology_or_canon",
            "authorship_or_superscription_historicity",
            "speaker_identity",
            "performance_or_liturgical_reconstruction",
            "preferred_translation_reading_or_source_tradition",
            "forced_messianic_or_christological_identification",
            "psalm_pair_merger",
        ],
        "coverage_assertion": {
            "coordinate_system": "WEB",
            "canonical_psalms_expected": 150,
            "canonical_verses_expected": 2461,
            "canonical_verses_covered": 2461,
            "exactly_once": True,
            "ordered": True,
            "gaps": 0,
            "overlaps": 0,
            "chunk_count": len(chunks),
        },
        "boundary_principle": {
            "default": "A complete psalm is a genuine outer literary unit, not a chapter fallback.",
            "internal_split_gate": (
                "Split only long or clearly multipart psalms at refrain cycles, alphabetic stanzas, "
                "extended recital episodes, speaker/addressee or liturgical-role changes, while "
                "preserving the whole psalm as the exact rejected larger alternative."
            ),
            "unresolved_rule": "keep_larger_unit_lower_confidence_and_queue",
        },
        "web_mt_lxx_versification_holds": [
            "WEB canonical coverage excludes unnumbered USFM headings and must not manufacture verse 0.",
            "Many MT/OSHB psalms count one or two superscription lines as verses; map per psalm rather than applying a blanket offset.",
            "Greek/LXX numbering commonly combines MT Psalms 9-10, combines MT 114-115, splits MT 116, and splits MT 147; relation is evidence only.",
            "LXX Psalm 151 lies outside this 66-book WEB coordinate scope and is not imported.",
            "Psalms 42 and 43 share refrain/lexical pressure, but remain separate canonical psalms with an evidence-only relation.",
        ],
        "oshb_mt_qere_ketiv_evidence_only": [
            "MT/OSHB 5:9", "6:4", "9:13", "9:19", "10:5", "10:10", "10:12",
            "11:1", "17:11", "17:14", "18:51", "21:2", "24:6", "26:2", "30:4",
            "39:1", "41:3", "42:9", "49:15", "51:4", "54:7", "55:16", "56:7",
            "58:8", "59:11", "74:6", "74:11", "77:1", "77:12", "77:20",
            "85:2", "89:18", "89:29", "90:8", "92:16", "100:3", "101:5",
            "102:24", "105:18", "105:28", "106:45", "119:79", "119:147",
            "119:161", "126:4", "129:3", "139:6", "139:16", "140:10", "140:11",
        ],
        "global_translation_poetics_holds": [
            "superscription terms mizmor, maskil, miktam, musical directions, names, and settings",
            "Selah placement and translation; never an automatic seam",
            "Masoretic accent hierarchy versus English lineation",
            "rare Hebrew, ellipsis, parallelism, wordplay, and divine names/titles",
            "acrostic irregularities in Psalms 9-10, 25, 34, 37, 111, 112, 119, and 145",
            "refrain variants in Psalms 42-43, 46, 49, 57, 59, 62, 67, 80, 99, 107, and 136",
            "textual and later-reuse pressure in Psalms 22, 45, 69, 82, 89, 110, and 118",
            "Psalm 68 obscurity; Psalm 119 Torah-term variation; Psalm 137 violent imprecation",
            "collection doxologies and the five-book arrangement are evidence, not authority to detach or merge units",
        ],
        "proposed_chunks": chunks,
        "exact_low_holds": [
            {
                "span": f"{psalm}:1-{psalm}:{max(verses[psalm])}",
                "competing_internal_units": [
                    f"{psalm}:{start}-{psalm}:{end}" for start, end in SPLITS[psalm][0]
                ],
                "hold": (
                    f"All internal seams in Psalm {psalm} remain contestable against the exact "
                    "whole-psalm parent; retain LOW unless the alphabetic octets of Psalm 119."
                ),
            }
            for psalm in SPLITS
            if psalm != 119
        ],
        "expertise_gaps": [
            "Masoretic Psalms accentuation and versification specialist",
            "Biblical Hebrew poetry and discourse specialist",
            "Septuagint Psalms textual and numbering specialist",
            "Dead Sea Psalms manuscript specialist",
            "chronologically labeled ancient Jewish and rabbinic Psalms reception specialist",
            "Temple and synagogue liturgical-history specialist",
        ],
        "unresolved_action": "keep_larger_unit_lower_confidence_and_queue",
        "agreement_is_not_authority": True,
    }
    payload = json.dumps(proposal, indent=2, ensure_ascii=False) + "\n"
    OUT.write_text(payload, encoding="utf-8")
    print(json.dumps({
        "path": str(OUT),
        "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "chunks": len(chunks),
        "verses": 2461,
    }))


if __name__ == "__main__":
    main()
