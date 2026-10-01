#!/usr/bin/env python3
"""EZEKIEL device inventory — the book's own structural signals, counted from MT bytes.

WHAT THIS IS FOR. Ezekiel is unusually formulaic, and its formulae are the honest boundary evidence: dated oracles
open units, the word-event formula opens oracles, the recognition formula closes them. This file COUNTS them and
records where they stand. It does not decide a single boundary — the writer and reviewers do that, and the
campaign's rule stands that a refrain CLOSES a unit and that a seam is assessed from BOTH sides.

EVERY COUNT IS A CONSONANTAL-SKELETON MATCH over Ezek_oshb.txt, which carries no maqaf, no paseq and no
sof-pasuq (see _build_pmarks_ezek.py). Matching on the pointed text would miss forms that differ only in
vocalisation, so the text is stripped to consonants first and the pattern is written in consonants.

REFS ARE MT. The ch 20/21 zone means MT != WEB there; web_mt_offset_map.json converts, and a row citing anything
in that zone carries a dual reference.
"""
import collections
import json
import re
import sys
import unicodedata
from pathlib import Path

SP = Path(__file__).resolve().parent
BOOK = "Ezek"
POINTS = re.compile(r"[֑-ׇ]")


def skel(s):
    return POINTS.sub("", unicodedata.normalize("NFD", s))


# consonantal patterns, written as skeletons
FORMULAE = {
    # Three nested counts, reported SEPARATELY and never blended (see word_event_family below). The strict form
    # alone missed MT 24:1, where the DATE is infixed between אלי and לאמר - and 24:1 is also a dateline, so the
    # strict word-event pattern and the cardinal-numeral dateline pattern failed at the SAME verse for two
    # unrelated reasons, making it invisible twice. Found by the Fable strategy author, verified from bytes.
    "word_event_formula": (r"ויהי\s+דבר\s+יהוה\s+אלי\s+לאמר",
                           "'and the word of YHWH came to me, saying' - STRICT form, אלי and לאמר adjacent; "
                           "the standard oracle ONSET"),
    "word_event_vayehi_any": (r"ויהי\s+דבר\s+יהוה\s+אלי\b",
                              "the ויהי word-event onset allowing an INFIXED temporal phrase (MT 12:8 'in the "
                              "morning'; MT 24:1 the ninth-year dateline). THE INFIX MUST NOT BE THE PERFECT "
                              "VERB היה: an unbounded infix returns 47, not 41, by swallowing the six "
                              "'ויהי [date] היה דבר יהוה' datelines (MT 26:1, 29:17, 30:20, 31:1, 32:1, 32:17) "
                              "that belong to the SEPARATE perfect-form count. This pattern is anchored on אלי "
                              "so it cannot; a rebuilt sweep that drops the anchor silently blends the two "
                              "families this split exists to keep apart"),
    "word_event_hayah_any": (r"היה\s+דבר\s+יהוה\s+אלי\b",
                             "the PERFECT היה form of the word-event onset; it is the form the dated oracles "
                             "systematically use AFTER their dateline (MT 26:1, 29:1, 29:17, 30:20, 31:1, 32:1, "
                             "32:17)"),
    "son_of_man_address": (r"בן\s+אדם",
                           "'son of man' - the divine address to the prophet; near-universal oracle opener"),
    "recognition_formula": (r"וידעו\s+כי\s+אני\s+יהוה",
                            "'and they shall know that I am YHWH' - the characteristic CLOSING refrain"),
    "recognition_formula_2ms": (r"וידעת\s+כי\s+אני\s+יהוה",
                                "'and you shall know that I am YHWH' - second-person variant of the close"),
    "thus_says_the_lord_yhwh": (r"כה\s+אמר\s+אדני\s+יהוה",
                                "'thus says the Lord YHWH' - the messenger formula"),
    "utterance_of_the_lord_yhwh": (r"נאם\s+אדני\s+יהוה",
                                   "'utterance of the Lord YHWH' - oracle-final signature"),
    # NOT `יד יהוה על[יו]`: that fixed order returned 1, because the motif also stands as
    # `היתה עלי יד יהוה` and `ותהי עלי שם יד יהוה` with the prepositional phrase BEFORE the construct.
    # An undercount in an inventory is worse than no inventory, because it reads as evidence of absence.
    "hand_of_yhwh_upon_me": (r"יד\s+יהוה|יד\s+אדני\s+יהוה",
                             "'the hand of YHWH' - vision ONSET marker; matched on the construct alone because "
                             "the prepositional phrase precedes it as often as it follows"),
    "set_your_face": (r"שים\s+פני?ך", "'set your face toward' - sign-act / oracle direction opener"),
    "i_am_yhwh_spoken": (r"אני\s+יהוה\s+דברתי", "'I YHWH have spoken' - emphatic close"),
}

# a dated oracle opens with 'in the Nth year / Nth month / Nth day'
DATE = re.compile(r"בשנת|בחדש|לחדש")
NUMERAL_WORDS = r"(אחת|שתי|שלש|רבע|חמש|שש|שבע|שמנ|תשע|עשר|עשרים|שלשים)"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    oshb = {}
    for line in (SP / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").splitlines():
        r, t = line.split("\t", 1)
        oshb[r] = t
    order = sorted(oshb, key=lambda k: (int(k.split(".")[1]), int(k.split(".")[2])))
    sk = {k: skel(v) for k, v in oshb.items()}

    found = {}
    for name, (pat, gloss) in FORMULAE.items():
        rx = re.compile(pat)
        hits = [k for k in order if rx.search(sk[k])]
        found[name] = {"gloss": gloss, "count": len(hits), "verses_mt": hits}

    # A DATELINE IS DEFINED STRUCTURALLY, not by a numeral vocabulary. Two earlier attempts failed:
    #   - requiring a CARDINAL stem (תשע, עשר, ...) missed every ordinal dateline, because Ezekiel writes
    #     התשיעית / העשירי / בעשור, which share no substring with the cardinals. MT 24:1 vanished this way.
    #   - requiring the construct בשנת alone returned ZERO datelines in a book famous for them.
    # A dateline is a YEAR word together with a MONTH or DAY term. That is what a dateline IS, and it needs no
    # numeral list at all. It also self-corrects a false positive the year regex alone produces: MT 26:10 matches
    # שנה only as a substring of תרעשנה ("they shall shake"), and is excluded because it carries no month or day.
    # SUBSTRING match, deliberately, and the docs must say so. A prefix-anchored reading of "prefix optional"
    # would miss שנתו at MT 46:13 (year + 3ms suffix) and change the non-dateline count from 7 to 5. The
    # DATELINE count is 14 either way, because the verses that separate the two readings carry no month or day
    # term - but a later sweep implementing the rule as loosely worded would appear to disagree for no real
    # reason, so the semantics are pinned here. The cost of the loose match is one substring artifact (MT 26:10,
    # תרעשנה), which is listed and labelled rather than silently dropped.
    YEAR = re.compile(r"ב?שנ[הת]")
    MONTH = re.compile(r"חדש")
    DAY = re.compile(r"בעשור|לחדש")
    datelines = [k for k in order if YEAR.search(sk[k]) and (MONTH.search(sk[k]) or DAY.search(sk[k]))]
    # Festival-calendar dates carry a month/day but NO year. This list is a WARNING list - "these look like
    # dates and open nothing" - so UNDER-inclusion is the dangerous error and it happened: the first rule reused
    # the cardinal NUMERAL_WORDS vocabulary and so missed MT 45:18, whose "בראשון באחד לחדש" is a FULLER date
    # formula than 45:20's day-only "בשבעה בחדש", and which carries the messenger formula as well - making it
    # the single verse in ch 45 most likely to be misread as a unit onset. Found by the distinct checker
    # (ezek_p0_recheck_a1#e1). Same root cause as the dateline miss: an ordinal slipping past a cardinal list.
    #
    # The rule is now structural and WORD-ANCHORED on the singular date construction לחדש / בחדש. The anchor is
    # what separates a date from the חדש homographs. None of these is a date:
    #   ובחדשים  "at the new moons"      MT 45:17, 46:3
    #   לחדשיו   "its months"            MT 47:12
    #   החדש     "the new moon" (day of) MT 46:1, 46:6  - the closest genuine near-miss: calendrical, in the
    #            same temple-law section, and excluded only because it carries no day number
    #   חדשים    "months" (duration)     MT 39:12, 39:14
    #   לב חדש   "a new heart"           MT 18:31, 36:26 - the same three letters meaning something else
    # NOT MT 11:19. An earlier draft of this comment listed 11:19 among the לב חדש verses and that was a
    # FABRICATED READING: 11:19 reads לֵב אֶחָד ("ONE heart") with רוּחַ חֲדָשָׁה ("a new spirit"); only the
    # spirit is new there. Caught by the distinct checker (ezek_p0_delta_a1#e1), which refused the whole repair
    # over it - correctly, since a false byte claim inside a note about byte fidelity is the exact error class
    # this round was opened to fix. Many manuscripts and versions do read חדש at 11:19, which is why the English
    # tradition says "a new heart"; WLC/OSHB, this campaign's declared source, does not.
    DATE_CONSTRUCTION = re.compile(r"(?:^|\s)[לב]חדש(?:\s|$)")
    calendar_only = [k for k in order if DATE_CONSTRUCTION.search(sk[k]) and not YEAR.search(sk[k])]
    year_word_not_dateline = [k for k in order if YEAR.search(sk[k]) and k not in datelines]
    per_ch = collections.Counter(int(k.split(".")[1]) for k in order)

    out = {
        "book": BOOK,
        "witness": "WLC (OSHB); refs are MT",
        "numbering": ("MT != WEB in the ch 20/21 zone (MT 21:1-5 = WEB 20:45-49; MT 21:6-37 = WEB 21:1-32); "
                      "identity elsewhere. Convert with web_mt_offset_map.json; a row in the zone carries a dual "
                      "reference."),
        "method": ("consonantal-skeleton regex over Ezek_oshb.txt, which carries no maqaf, paseq or sof-pasuq. "
                   "Counts are of VERSES containing the form, not of occurrences within a verse."),
        "totals": {"verses": len(oshb), "chapters": len(per_ch)},
        "verses_per_chapter_mt": {str(c): per_ch[c] for c in sorted(per_ch)},
        "formulae": found,
        "dated_oracles": {
            "gloss": ("ORACLE DATELINES: a YEAR word together with a MONTH or DAY term. Structural, not a numeral "
                      "vocabulary. These open major units and are the strongest onset evidence in the book."),
            "count": len(datelines), "verses_mt": datelines,
            "correction_2026_09_08": ("this list was 13 and is now 14. MT 24:1, the siege dateline, was missing "
                                      "because the earlier rule required a CARDINAL numeral stem and 24:1 uses "
                                      "ordinals. Found by the Fable strategy author (ezek_strategy_a1#e1), "
                                      "verified from bytes by the orchestrator, ruled: 14 is the count."),
        },
        "year_word_but_not_a_dateline": {
            "gloss": ("the LOOSE year regex's residue: 6 genuine year words that are not datelines - durations "
                      "and cultic years - plus 1 substring artifact. Listed so a later sweep does not rediscover "
                      "them as candidates. NOTE the count depends on the match semantics: 7 under the substring "
                      "match this tool uses, 5 under a prefix-anchored reading (which would drop שנתו at 46:13 "
                      "and the 26:10 artifact). The DATELINE count is 14 under either."),
            "count": len(year_word_not_dateline), "verses_mt": year_word_not_dateline,
            "notes": {"Ezek.4.6": "a day for a year - sign-act, not a date",
                      "Ezek.26.10": "FALSE POSITIVE of the year regex alone: שנה appears only inside תרעשנה "
                                    "(they shall shake). The structural rule excludes it; a year-word sweep "
                                    "alone would not.",
                      "Ezek.29.11": "forty years - duration", "Ezek.29.12": "forty years - duration",
                      "Ezek.29.13": "forty years - duration",
                      "Ezek.46.13": "a lamb of its first year - cultic",
                      "Ezek.46.17": "the year of liberty - cultic"},
        },
        "word_event_family": {
            "gloss": ("THREE NESTED COUNTS, REPORTED SEPARATELY AND NEVER BLENDED. Quoting one where another is "
                      "meant is the error class this split exists to prevent."),
            "strict_vayehi_adjacent": len(found["word_event_formula"]["verses_mt"]),
            "vayehi_any_incl_infixed_date": len(found["word_event_vayehi_any"]["verses_mt"]),
            "hayah_perfect_form": len(found["word_event_hayah_any"]["verses_mt"]),
            "family_total_distinct": len(set(found["word_event_vayehi_any"]["verses_mt"])
                                         | set(found["word_event_hayah_any"]["verses_mt"])),
            "infixed_date_verses_the_strict_form_misses": [
                k for k in found["word_event_vayehi_any"]["verses_mt"]
                if k not in found["word_event_formula"]["verses_mt"]],
            "note": ("the היה perfect form is what the dated oracles use AFTER their dateline, so the dateline "
                     "verses and the strict-form verses are largely disjoint sets - which is why the strict count "
                     "alone understates onset evidence exactly in the dated blocks."),
        },
        "calendar_dates_not_datelines": {
            "gloss": ("date formulae WITHOUT a year - festival-calendar dates in the temple-law section. They "
                      "open no oracle and must not be read as unit onsets; counted separately so the dateline "
                      "figure stays usable. MT 45:18 is the one to watch: it carries a full month+day formula "
                      "AND the messenger formula, which is exactly the combination that reads like an onset."),
            "correction_2026_09_08": ("this list was 3 and is now 4. MT 45:18 was missing because the earlier "
                                      "rule reused the cardinal numeral vocabulary. Found by the distinct "
                                      "checker (ezek_p0_recheck_a1#e1); rule replaced with a word-anchored "
                                      "date construction, which also correctly excludes the חדש homographs "
                                      "(ובחדשים 'at the new moons' 45:17/46:3, החדש 'the new moon' 46:1/46:6, "
                                      "לחדשיו 'its months' 47:12, חדשים 'months' 39:12/39:14, and לב חדש "
                                      "'a new heart' 18:31/36:26 - NOT 11:19, which reads לב אחד 'one heart'; "
                                      "an earlier draft's claim otherwise was a fabricated reading)."),
            "count": len(calendar_only), "verses_mt": calendar_only,
        },
        "how_these_are_used": [
            "the word-event formula and 'son of man' typically ONSET a unit; the recognition formula and "
            "'utterance of the Lord YHWH' typically CLOSE one",
            "a refrain CLOSES a unit - the standing campaign rule - so a recognition formula belongs to the unit "
            "BEFORE it, not the one after",
            "a seam is assessed from BOTH sides: an onset-only diagnosis is incomplete until the adjacent unit's "
            "close is weighed from bytes",
            "these are EVIDENCE, not a verdict. No boundary is set by a formula count alone, and translation "
            "punctuation or editorial headings never drive one at all (E-23)",
        ],
        "known_hard_regions_to_flag_for_raised_coverage": {
            "note": ("recorded from the structural counts above as candidates for the hard-track raised peer and "
                     "spot coverage; NOT a segmentation decision, and the writer re-derives every boundary"),
            "candidates": [
                "chs 1-3 the inaugural vision and commissioning (vision-cycle seams; hand-of-YHWH onsets)",
                "chs 8-11 the temple vision (a single transported vision across four chapters)",
                "ch 20/21 the NUMBERING ZONE - every ref dual-qualified",
                "chs 25-32 the oracles against the nations (a formula-dense block where onset and close collide)",
                "chs 38-39 Gog (recapitulation-versus-sequence)",
                "chs 40-48 the temple vision and land allotment (long measured description, few formulae)",
            ],
        },
    }
    (SP / "ezek_device_inventory.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                                   encoding="utf-8", newline="\n")
    print(json.dumps({"verses": len(oshb),
                      "formulae": {k: v["count"] for k, v in found.items()},
                      "dated_oracle_datelines": len(datelines), "dateline_verses": datelines,
                      "calendar_dates_not_datelines": calendar_only,
                      "year_word_not_dateline": year_word_not_dateline,
                      "word_event_strict": len(found["word_event_formula"]["verses_mt"]),
                      "word_event_vayehi_any": len(found["word_event_vayehi_any"]["verses_mt"]),
                      "word_event_hayah": len(found["word_event_hayah_any"]["verses_mt"])},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
