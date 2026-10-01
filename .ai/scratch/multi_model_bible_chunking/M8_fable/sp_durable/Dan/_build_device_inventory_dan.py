#!/usr/bin/env python3
"""DANIEL device inventory - the book's own structural signals, counted from MT bytes. Ported from
Ezekiel's _build_device_inventory_ezek.py; every difference beyond book tokens is listed in LOGIC_CHANGES.

WHAT THIS IS. It COUNTS datelines, year words that are not datelines, calendar dates without a year, and
recurring formulae, per language (Hebrew / Aramaic), and records where they stand. It decides no boundary.
The campaign rules stand: a refrain CLOSES a unit, and a seam is assessed from BOTH sides.

EVERY COUNT IS A CONSONANTAL-SKELETON MATCH over Dan_oshb.txt, counted in VERSES containing a form (not
occurrences). Points and accents are stripped after NFD; maqaf (none measured) would become a space.

TWO LANGUAGES. dan_language_zones.json assigns each verse H or A; MT 2:4 is mixed and is split by word
index (words before the switch are Hebrew, the rest Aramaic). Each pattern is written for one language and
is matched only against that language's text; its hits in the other language are reported, not counted.

REFS ARE MT (numbering_face "MT"). MT != WEB in chs 3-6 (four zones); every zone ref carries both faces.
Consumers must assert the face they expect: verse_inventory.json in the same directory is on the WEB face.

USAGE. Installed at SP/Dan it reads its sibling inputs and writes dan_device_inventory.json beside itself.
  --root DIR --out FILE   redirect the inputs and the output
  --selftest              run the synthetic self-test only (writes nothing)
It exits non-zero unless every self-assertion holds.
"""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOOK = "Dan"
INPUTS = ["Dan_oshb.txt", "Dan_web_clean.txt", "dan_language_zones.json", "web_mt_offset_map.json",
          "verse_inventory.json"]
POINTS = re.compile(r"[֑-ׇ]")
MAQAF = "־"
LANG = {"H": "Hebrew", "A": "Aramaic"}
PRODUCED_BY = {"attempt_id": "dan_p0_device_inventory_a1", "execution_id": "dan_p0_device_inventory_a1#e2",
               "model": "claude-opus-5-5", "grader_role": "grader_fallback (OW-25)",
               "statement": "a recorded downgrade, not an equivalence: this lane ran on claude-opus-5-5 under OW-25"}


def skel(s):
    return POINTS.sub("", unicodedata.normalize("NFD", s.replace(MAQAF, " ")))


def vkey(k):
    return (int(k.split(".")[1]), int(k.split(".")[2]))


# ---------------------------------------------------------------- numbering zones (MT -> WEB)
# (mt_chapter, mt_first, mt_last, web_chapter, web_first). Asserted against web_mt_offset_map.json zone_pairs.
ZONES = [(3, 31, 33, 4, 1), (4, 1, 34, 4, 4), (6, 1, 1, 5, 31), (6, 2, 29, 6, 1)]


def in_zone(c, v):
    return any(mc == c and lo <= v <= hi for mc, lo, hi, _, _ in ZONES)


def mt_to_web(c, v):
    for mc, lo, hi, wc, wlo in ZONES:
        if mc == c and lo <= v <= hi:
            return (wc, wlo + v - lo)
    return (c, v)


def web_ref(mt_key):
    c, v = mt_to_web(*vkey(mt_key))
    return f"{BOOK}.{c}.{v}"


# ---------------------------------------------------------------- date-family patterns, per language
# YEAR: SUBSTRING is the primary reading (as Ezekiel's), so artifacts are listed and labelled, not dropped;
# the word-ANCHORED reading (optional proclitics, no suffix) is reported beside it.
YEAR = {"H": {"substring": r"שנ(?:ה|ת|ים|ות)",
              "anchored": r"(?:^|\s)ו?[בלכמ]?ה?(?:שנה|שנת|שנים|שנות)(?=\s|$)"},
        "A": {"substring": r"שנ(?:ה|ת|ין)",
              "anchored": r"(?:^|\s)ו?[בלכ]?(?:שנה|שנת|שנין|שנתא)(?=\s|$)"}}
MONTH = {"H": {"substring": r"חדש", "anchored": r"(?:^|\s)ו?[בלכמ]?ה?חדש(?:ים|י|ו|יו)?(?=\s|$)"},
         "A": {"substring": r"ירח", "anchored": r"(?:^|\s)ו?[בלכ]?ירח(?:א|ין|יא)?(?=\s|$)"}}
# DAY: ANCHORED is the primary reading here, because the substring is dominated by חכימי 'wise men' (A) and
# catches ימינו 'his right hand' and מימי 'waters of' (H); substring-only hits are classified as artifacts.
DAY = {"H": {"substring": r"יום|ימים|ימי|יומ",
             "anchored": r"(?:^|\s)ו?[בלכמ]?ה?(?:יום|יומו|ימים|ימי|ימין)(?=\s|$)"},
       "A": {"substring": r"יום|יומ|ימי",
             "anchored": r"(?:^|\s)ו?[בלכ]?(?:יום|יומא|יומין|יומיא|יומי|יומיה|יומיהון)(?=\s|$)"}}
# DATELINE (Daniel): the ב-prefixed year construct, a numeral word, then a ל-prefixed regnal term.
# Ezekiel's rule (year word + month/day term) returns ZERO in Daniel; that reading is reported, not used.
DATELINE_RX = r"(?:^|\s)(ו?בשנת)\s+(\S+)\s+(ל\S+)(?:\s+(\S+))?"
DATELINE_READINGS = {
    "b_prefixed_year_construct_numeral_regnal (USED)": r"(?:^|\s)ו?בשנת\s+\S+\s+ל\S+",
    "b_prefixed_year_construct_alone": r"(?:^|\s)ו?בשנת(?=\s|$)",
    "any_year_construct_numeral_regnal (admits a terminus such as עד שנת)": r"(?:^|\s)\S*שנת\s+\S+\s+ל\S+",
}
# Ezekiel's own date patterns, verbatim, applied to Daniel's whole skeleton only to record that they find no dateline
EZEK_DATE = {"YEAR": r"ב?שנ[הת]", "MONTH": r"חדש", "DAY": r"בעשור|לחדש"}
# calendar date construction, word-anchored as Ezekiel's DATE_CONSTRUCTION
DATE_CONSTRUCTION = {"H": r"(?:^|\s)ו?[לב]חדש(?=\s|$)", "A": r"(?:^|\s)ו?[לב]ירח(?:א)?(?=\s|$)"}
WEB_YEAR = re.compile(r"(?:[Ii]n )?the [a-z-]+ year of (?:his reign|(?:the reign of )?(?:King )?(?P<name>[A-Z][a-z]+)"
                      r"(?: (?:the son of|king of) [A-Z][a-z]+| the Mede)?)")
WEB_DAY = re.compile(r"(?:[Ii]n )?the [a-z-]+ day of the [a-z-]+ month")

# curated reasons for every year-word verse that is not a dateline (substring reading). The builder asserts
# the key set equals the measured set, and slices each web_evidence from Dan_web_clean.txt by its keyword.
YEAR_NOTES = {
    "Dan.1.5": ("count_of_years", "a duration: the three-year training (שנים שלוש)", "three years"),
    "Dan.1.21": ("regnal_terminus", "a regnal year named as an END point, 'until the first year of Cyrus' "
                 "(עד שנת אחת לכורש); not ב-prefixed, so not a dateline under the rule used", "first year of King Cyrus"),
    "Dan.5.9": ("homograph", "שנין here is 'changed' (his countenance), not 'years'", "changed"),
    "Dan.6.1": ("age", "an age: Darius about sixty-two years old (כבר שנין שתין ותרתין)", "sixty-two years old"),
    "Dan.6.19": ("homograph", "ושנתה is 'his sleep', not 'year'", "sleep"),
    "Dan.7.3": ("homograph", "שנין here is 'different' (one from another), not 'years'", "different"),
    "Dan.7.7": ("homograph", "ושנין here is 'teeth', not 'years'", "teeth"),
    "Dan.7.23": ("substring_artifact", "שנה only inside ותדושנה 'and it will tread it down'", "tread"),
    "Dan.9.25": ("homograph", "ושנים here is 'and two' in 'sixty-two (weeks)'", "sixty-two"),
    "Dan.9.26": ("homograph", "ושנים here is 'and two' in 'sixty-two (weeks)'", "sixty-two"),
    "Dan.10.13": ("substring_artifact", "שנים only inside הראשנים 'the chief (princes)'", "chief princes"),
    "Dan.11.6": ("duration", "a duration: 'at the end of years' (ולקץ שנים)", "years"),
    "Dan.11.8": ("duration", "a duration: 'some years' (שנים)", "years"),
    "Dan.11.13": ("duration", "a duration: 'at the end of the times, years' (לקץ העתים שנים)", "years"),
    "Dan.11.29": ("substring_artifact", "שנה only inside כראשנה 'as at the first' (WEB 'as it was in the former')", "former"),
    "Dan.12.5": ("homograph", "שנים here is 'two' ('two others'), not 'years'", "two others"),
}

# ---------------------------------------------------------------- formulae: (name, lang, pattern, gloss)
EZEK_FORMULAE = [  # Ezekiel's eleven, verbatim, run on Daniel's HEBREW text so the zero counts are recorded
    ("ezek_word_event_formula", r"ויהי\s+דבר\s+יהוה\s+אלי\s+לאמר", "Ezekiel's strict word-event onset"),
    ("ezek_word_event_vayehi_any", r"ויהי\s+דבר\s+יהוה\s+אלי\b", "Ezekiel's word-event onset, infix allowed"),
    ("ezek_word_event_hayah_any", r"היה\s+דבר\s+יהוה\s+אלי\b", "Ezekiel's perfect-form word-event onset"),
    ("ezek_son_of_man_address", r"בן\s+אדם", "Ezekiel's 'son of man' address"),
    ("ezek_recognition_formula", r"וידעו\s+כי\s+אני\s+יהוה", "Ezekiel's recognition formula"),
    ("ezek_recognition_formula_2ms", r"וידעת\s+כי\s+אני\s+יהוה", "Ezekiel's 2ms recognition formula"),
    ("ezek_thus_says_the_lord_yhwh", r"כה\s+אמר\s+אדני\s+יהוה", "Ezekiel's messenger formula"),
    ("ezek_utterance_of_the_lord_yhwh", r"נאם\s+אדני\s+יהוה", "Ezekiel's utterance formula"),
    ("ezek_hand_of_yhwh_upon_me", r"יד\s+יהוה|יד\s+אדני\s+יהוה", "Ezekiel's hand-of-YHWH marker"),
    ("ezek_set_your_face", r"שים\s+פני?ך", "Ezekiel's 'set your face'"),
    ("ezek_i_am_yhwh_spoken", r"אני\s+יהוה\s+דברתי", "Ezekiel's 'I YHWH have spoken'"),
]
FORMULAE = [
    # first-person report
    ("i_daniel_heb", "H", r"אני\s+דניאל", "first-person report 'I, Daniel' (Hebrew)"),
    ("and_i_daniel_heb", "H", r"ואני\s+דניאל", "'and I, Daniel' (Hebrew; a subset of i_daniel_heb)"),
    ("i_daniel_aram", "A", r"אנה\s+דניאל", "first-person report 'I, Daniel' (Aramaic)"),
    ("i_nebuchadnezzar_aram", "A", r"אנה\s+נבו?כדנצר", "first-person report 'I, Nebuchadnezzar' (Aramaic)"),
    # vision formulae
    ("i_saw_heb", "H", r"(?:^|\s)(?:וארא|ואראה|ראיתי|וראיתי)(?=\s|$)", "'and I saw' / 'I saw' (Hebrew)"),
    ("i_saw_in_the_vision_heb", "H", r"ו?אראה?\s+בחזון", "'and I saw in the vision' (Hebrew)"),
    ("vision_noun_hazon_heb", "H", r"חזון", "the vision noun חזון, any form (Hebrew; substring)"),
    ("vision_noun_mareh_heb", "H", r"מראה", "the vision/appearance noun מראה, any form (Hebrew; substring)"),
    ("lifted_eyes_and_saw_heb", "H", r"ואשא\s+(?:את\s+)?עיני", "'I lifted up my eyes (and saw)' (Hebrew)"),
    ("behold_heb", "H", r"(?:^|\s)והנה(?=\s|$)", "'and behold' (Hebrew)"),
    ("i_was_seeing_heb", "H", r"חזה\s+הוית|הייתי\s+ראה", "'I was seeing' (Hebrew rendering of the Aramaic form)"),
    ("i_was_seeing_aram", "A", r"חזה\s+הוית", "'I was seeing' (Aramaic)"),
    ("i_was_seeing_in_my_visions_aram", "A", r"חזה\s+הוית\s+בחזוי", "'I was seeing in my visions' (Aramaic)"),
    ("visions_of_my_head_aram", "A", r"חזוי\s+ראש", "'the visions of my/his head' (Aramaic)"),
    ("visions_of_the_night_aram", "A", r"חזו\S*\s+(?:די\s+|עם\s+)?ליליא", "'visions of/in the night' (Aramaic)"),
    ("lifted_eyes_aram", "A", r"עיני\s+לשמיא\s+נטלת", "'I lifted my eyes to heaven' (Aramaic)"),
    ("behold_aram", "A", r"(?:^|\s)ו?(?:אלו|ארו)(?=\s|$)", "'and behold' (Aramaic ואלו / וארו)"),
    # speech introductions
    ("answered_and_said_heb", "H", r"(?:^|\s)ויען\s+(?:\S+\s+){0,4}?ויאמר", "'answered ... and said' (Hebrew)"),
    ("and_he_said_heb", "H", r"(?:^|\s)ויאמר(?=\s|$)", "'and he said' (Hebrew)"),
    ("and_he_said_to_me_heb", "H", r"ויאמר\s+אלי", "'and he said to me' (Hebrew)"),
    ("answered_and_said_aram_loose", "A", r"(?:^|\s)ענ(?:ה|ו|ין|ת)\s+(?:\S+\s+){0,5}?ו?אמר",
     "'answered ... and said' (Aramaic; up to five words between)"),
    ("answered_and_said_aram_strict", "A", r"(?:^|\s)ענ(?:ה|ו)\s+\S+\s+ו?אמר",
     "'X answered and said' (Aramaic; exactly one word between)"),
    ("o_king_live_forever_aram", "A", r"מלכא\s+לעלמין\s+חיי", "court greeting 'O king, live forever' (Aramaic)"),
    ("to_all_peoples_nations_tongues_aram", "A", r"עממיא\s+אמיא\s+ולשניא", "'peoples, nations and languages' (Aramaic)"),
    ("peace_be_multiplied_aram", "A", r"שלמכון\s+ישגא", "epistolary greeting 'peace be multiplied to you' (Aramaic)"),
    ("decree_aram", "A", r"(?:מני|מן\s+קדמי)\s+שים\s+טעם", "decree formula 'a decree is made by me' (Aramaic)"),
    ("this_is_the_interpretation_aram", "A", r"דנה\s+(?:חלמא\s+ו)?פשר", "'this is the (dream and its) interpretation' (Aramaic)"),
    # doxologies and ascriptions
    ("blessed_heb", "H", r"(?:^|\s)ו?ברוך|יתברך", "'blessed' (Hebrew)"),
    ("ashre_heb", "H", r"(?:^|\s)אשרי(?=\s|$)", "beatitude 'blessed is' אשרי (Hebrew)"),
    ("great_and_awesome_god_heb", "H", r"האל\s+הגדול\s+והנורא", "ascription 'the great and awesome God' (Hebrew)"),
    ("to_you_lord_righteousness_heb", "H", r"לך\s+אדני\s+הצדקה", "ascription 'to you, Lord, righteousness' (Hebrew)"),
    ("yhwh_name_heb", "H", r"יהוה", "the divine name יהוה (Hebrew)"),
    ("blessed_aram", "A", r"(?:^|\s)[ול]?(?:בריך|מברך|ברך|ברכת)(?=\s|$)",
     "'blessed/bless' (Aramaic); ברך is also 'knelt' - see the homograph note"),
    ("everlasting_dominion_aram", "A", r"שלטן\s+עלם", "'an everlasting dominion' (Aramaic)"),
    ("everlasting_kingdom_aram", "A", r"מלכות\S*\s+מלכות\s+עלם", "'his kingdom is an everlasting kingdom' (Aramaic)"),
    ("generation_to_generation_aram", "A", r"עם\s+דר\s+ודר", "'from generation to generation' (Aramaic)"),
    ("praise_aram", "A", r"שבח", "praise root שבח, any form (Aramaic; substring; includes praise of idols)"),
    ("most_high_aram", "A", r"(?:^|\s)[ול]{0,2}(?:עליא|עלאה|עליאה|עליונין)(?=\s|$)", "'the Most High' (Aramaic)"),
    ("god_of_heaven_aram", "A", r"אלה\s+שמיא", "'the God of heaven' (Aramaic)"),
    ("living_god_aram", "A", r"אלהא\s+חיא", "'the living God' (Aramaic)"),
    ("recognition_most_high_rules_aram", "A", r"די\s+שליט\s+(?:אלהא\s+)?(?:עליא|עלאה|עליאה)|די\s+שלטן\s+שמיא",
     "recognition refrain '(until you know) that the Most High rules / that Heaven rules' (Aramaic)"),
    # transitions
    ("at_that_time_heb", "H", r"(?:^|\s)ו?בעת\s+ההיא", "'at that time' (Hebrew)"),
    ("in_those_days_heb", "H", r"בימים\s+ההם", "'in those days' (Hebrew)"),
    ("in_those_times_heb", "H", r"ובעתים\s+ההם", "'and in those times' (Hebrew)"),
    ("time_of_the_end_heb", "H", r"עת\s+קץ", "'the time of the end' (Hebrew)"),
    ("vayehi_heb", "H", r"(?:^|\s)ויהי(?=\s|$)", "narrative 'and it came to pass / and it was' (Hebrew)"),
    ("then_aram", "A", r"(?:^|\s)(?:ב)?אדין(?=\s|$)", "'then' באדין / אדין (Aramaic)"),
    ("at_that_moment_aram", "A", r"בה\s+שעת[אה]|כשעה\s+חדה", "'at that moment' (Aramaic; both spellings)"),
    ("at_that_time_aram", "A", r"בה\s+זמנא", "'at that time' (Aramaic)"),
    ("in_that_night_aram", "A", r"בה\s+בליליא", "'in that night' (Aramaic)"),
    ("after_this_aram", "A", r"באתר\s+דנה", "'after this' (Aramaic)"),
    ("because_of_this_aram", "A", r"כל\s+קבל\s+דנה", "'because of this' (Aramaic)"),
    ("in_the_days_of_aram", "A", r"(?:^|\s)ו?ביומי", "'in the days of' (Aramaic)"),
    # address and direction
    ("son_of_man_heb", "H", r"בן\s+אדם", "'son of man' (Hebrew)"),
    ("son_of_man_aram", "A", r"כבר\s+אנש", "'one like a son of man' (Aramaic)"),
    ("fear_not_heb", "H", r"אל\s+תירא", "'fear not' (Hebrew)"),
    ("set_face_heb", "H", r"(?:ואתנה|נתתי|וישם|וישב|ישם|ישב)\s+(?:את\s+)?פני", "'I/he set (my/his) face' (Hebrew)"),
]


# ---------------------------------------------------------------- the measuring core (used by selftest too)
def split_parts(sk, lang, switch):
    """{key: {'H'|'A': text}}; a mixed verse is split by word index (1-based switch = first word of the 2nd lang)."""
    parts = {}
    for k, t in sk.items():
        L = lang[k]
        if L == "mixed":
            first, second, idx = switch[k]
            w = t.split()
            parts[k] = {first: " ".join(w[:idx - 1]), second: " ".join(w[idx - 1:])}
        else:
            parts[k] = {L: t}
    return parts


def hits(parts, order, L, pat):
    rx = re.compile(pat)
    return [k for k in order if L in parts[k] and rx.search(parts[k][L])]


def measure(sk, lang, switch):
    order = sorted(sk, key=vkey)
    parts = split_parts(sk, lang, switch)
    m = {"order": order, "parts": parts, "lang": {}}
    for fam, table in (("year", YEAR), ("month", MONTH), ("day", DAY)):
        for L in "HA":
            for rd in ("substring", "anchored"):
                m[(fam, L, rd)] = hits(parts, order, L, table[L][rd])
    for L in "HA":
        dl = hits(parts, order, L, DATELINE_RX)
        dc = hits(parts, order, L, DATE_CONSTRUCTION[L])
        ys = set(m[("year", L, "substring")])
        m[("dateline", L)] = dl
        m[("date_construction", L)] = dc
        m[("calendar", L)] = [k for k in dc if k not in ys]
        m[("year_not_dateline", L, "substring")] = [k for k in m[("year", L, "substring")] if k not in dl]
        m[("year_not_dateline", L, "anchored")] = [k for k in m[("year", L, "anchored")] if k not in dl]
        md_anc = set(m[("month", L, "anchored")]) | set(m[("day", L, "anchored")])
        md_sub = set(m[("month", L, "substring")]) | set(m[("day", L, "substring")])
        taken = set(dl) | set(m[("calendar", L)])
        m[("md_not_date", L)] = [k for k in order if k in md_anc and k not in taken]
        m[("md_artifact", L)] = [k for k in order if k in md_sub and k not in md_anc and k not in taken]
        for k in order:
            if L in parts[k]:
                m["lang"].setdefault(k, []).append(L)
    return m


def dateline_entry(k, L, text):
    g = re.search(DATELINE_RX, text)
    term, nxt = g.group(3), g.group(4)
    name = nxt if term == "למלכות" else (None if term == "למלכו" else term[1:])
    return {"year_form": g.group(1), "numeral": g.group(2), "regnal_term": term, "reign_named_mt": name}


# ---------------------------------------------------------------- selftest over synthetic lines
def selftest():
    pointed = lambda s: "".join(ch + ("ָ" if "א" <= ch <= "ת" else "") for ch in s)
    lines = {
        "Dan.1.1": pointed("בשנת שלוש למלכות יהויקים מלך יהודה"),
        "Dan.7.1": "בשנת חדה לבלאשצר מלך בבל",
        "Dan.1.5": "ולגדלם שנים שלוש",
        "Dan.10.4": "וביום עשרים וארבעה לחדש הראשון",
        "Dan.4.26": "לקצת ירחין תרי עשר",
        "Dan.2.4": "וידברו הכשדים למלך ארמית מלכא לעלמין חיי אמר חלמא לעבדיך ופשרא נחוא",
    }
    lang = {"Dan.1.1": "H", "Dan.7.1": "A", "Dan.1.5": "H", "Dan.10.4": "H", "Dan.4.26": "A", "Dan.2.4": "mixed"}
    sw = {"Dan.2.4": ("H", "A", 5)}
    sk = {k: skel(v) for k, v in lines.items()}
    m = measure(sk, lang, sw)
    fm = {n: (L, p) for n, L, p, _ in FORMULAE}
    res = [
        ("skeleton strips points", sk["Dan.1.1"] == "בשנת שלוש למלכות יהויקים מלך יהודה"),
        ("Hebrew dateline found", m[("dateline", "H")] == ["Dan.1.1"]),
        ("Hebrew dateline reign", dateline_entry("Dan.1.1", "H", sk["Dan.1.1"])["reign_named_mt"] == "יהויקים"),
        ("Aramaic dateline found", m[("dateline", "A")] == ["Dan.7.1"]),
        ("Aramaic dateline reign", dateline_entry("Dan.7.1", "A", sk["Dan.7.1"])["reign_named_mt"] == "בלאשצר"),
        ("year word not a dateline", m[("year_not_dateline", "H", "substring")] == ["Dan.1.5"]),
        ("calendar date without a year", m[("calendar", "H")] == ["Dan.10.4"]),
        ("calendar date is not a month/day residual", "Dan.10.4" not in m[("md_not_date", "H")]),
        ("Aramaic month word (duration) is a residual, not a date", m[("md_not_date", "A")] == ["Dan.4.26"]
         and m[("calendar", "A")] == []),
        ("zone verse MT 4:26 = WEB 4:29", mt_to_web(4, 26) == (4, 29) and in_zone(4, 26)),
        ("zone verse MT 6:1 = WEB 5:31", mt_to_web(6, 1) == (5, 31)),
        ("zone verse MT 3:31 = WEB 4:1; MT 6:2 = WEB 6:1", mt_to_web(3, 31) == (4, 1) and mt_to_web(6, 2) == (6, 1)),
        ("identity outside the zones", mt_to_web(7, 1) == (7, 1) and mt_to_web(3, 30) == (3, 30) and not in_zone(5, 30)),
        ("mixed verse split 4 + 8 words", len(m["parts"]["Dan.2.4"]["H"].split()) == 4
         and len(m["parts"]["Dan.2.4"]["A"].split()) == 8),
        ("mixed verse: Aramaic formula counted in its Aramaic part",
         hits(m["parts"], m["order"], "A", fm["o_king_live_forever_aram"][1]) == ["Dan.2.4"]),
        ("mixed verse: the Aramaic formula is not in its Hebrew part",
         hits(m["parts"], m["order"], "H", fm["o_king_live_forever_aram"][1]) == []),
    ]
    sk2 = dict(sk, **{"Dan.2.4": skel("וידברו הכשדים למלך ארמית אני דניאל חיי אמר חלמא לעבדיך ופשרא נחוא")})
    m2 = measure(sk2, lang, sw)
    res.append(("mixed verse: a Hebrew formula after the switch is not counted as Hebrew",
                hits(m2["parts"], m2["order"], "H", fm["i_daniel_heb"][1]) == []))
    return res


# ---------------------------------------------------------------- web text
def parse_web(raw):
    verses, cont, ch, cur = {}, 0, 0, None
    for line in raw.split("\n"):
        mh = re.match(r"^===== DAN (\d+) =====$", line)
        if mh:
            ch, cur = int(mh.group(1)), None
            continue
        mv = re.match(r"^\[v\] (\d+) (.*)$", line)
        if mv:
            cur = (ch, int(mv.group(1)))
            verses[cur] = [mv.group(2)]
            continue
        if line.strip() and line.strip() != "¶" and cur is not None:
            verses[cur].append(line)
            cont += 1
    return verses, cont


def web_slice(segments, kw, pad=25):
    for seg in segments:
        i = seg.find(kw)
        if i >= 0:
            lo = seg.rfind(" ", 0, max(0, i - pad)) + 1 if i > pad else 0
            hi = seg.find(" ", i + len(kw) + pad)
            return seg[lo:hi if hi >= 0 else len(seg)]
    return None


def zone_dual(keys):
    return {k: "web:" + web_ref(k) for k in keys if in_zone(*vkey(k))}


# ---------------------------------------------------------------- main
def build(root):
    raw = {n: (root / n).read_bytes() for n in INPUTS}
    inputs = {n: hashlib.sha256(b).hexdigest() for n, b in raw.items()}
    otext = raw["Dan_oshb.txt"].decode("utf-8")
    wtext = raw["Dan_web_clean.txt"].decode("utf-8")
    zones = json.loads(raw["dan_language_zones.json"].decode("utf-8"))
    omap = json.loads(raw["web_mt_offset_map.json"].decode("utf-8"))
    vinv = json.loads(raw["verse_inventory.json"].decode("utf-8"))
    oshb = {}
    for line in otext.splitlines():
        r, t = line.split("\t", 1)
        oshb[r] = t
    sk = {k: skel(v) for k, v in oshb.items()}
    lang = dict(zones["verse_language"])
    sw = {}
    for mv in zones["mixed_verses"]:
        seq = mv["sequence"]
        idx = mv["switch_before_word"][0]
        sw[mv["ref"]] = (seq[0], seq[idx - 1], idx)
    m = measure(sk, lang, sw)
    order = m["order"]
    web, cont_lines = parse_web(wtext)
    A = []  # self-assertions

    # totals
    chapters = sorted({vkey(k)[0] for k in order})
    per_ch = {str(c): sum(1 for k in order if vkey(k)[0] == c) for c in chapters}
    by_lang = {"Hebrew": sum(1 for k in order if lang[k] == "H"), "Aramaic": sum(1 for k in order if lang[k] == "A"),
               "mixed": sum(1 for k in order if lang[k] == "mixed")}
    A.append(("12 chapters and 357 verses in the witness", len(chapters) == 12 and len(order) == 357))
    A.append(("language totals sum to 357 (H 157 + A 199 + mixed 1)",
              sum(by_lang.values()) == 357 and set(lang) == set(order)
              and (by_lang["Hebrew"], by_lang["Aramaic"], by_lang["mixed"]) == (157, 199, 1)))
    # zone table agrees with the pinned offset map; WEB file and verse_inventory agree; bijection
    zp_ok = all(mt_to_web(*vkey(p["mt"].split(":", 1)[1])) == vkey(p["web"].split(":", 1)[1]) for p in omap["zone_pairs"])
    A.append(("zone table agrees with every web_mt_offset_map zone_pairs endpoint", zp_ok and len(omap["zone_pairs"]) == 8))
    web_per_ch = {str(c): sum(1 for (cc, _) in web if cc == c) for c in sorted({c for c, _ in web})}
    A.append(("WEB file has 357 [v] lines whose per-chapter counts equal verse_inventory.json (WEB face)",
              len(web) == 357 and web_per_ch == {str(c): n for c, n in vinv["chapters"].items()}
              and vinv["numbering_face"] == "WEB"))
    A.append(("MT -> WEB is a bijection onto the WEB file's verses",
              sorted(mt_to_web(*vkey(k)) for k in order) == sorted(web)))
    maqaf = otext.count(MAQAF)
    # language runs: witness word counts equal the zones file's run word counts
    run_ok = True
    flat = [(k, i + 1) for k in order for i in range(len(sk[k].split()))]
    pos = {p: n for n, p in enumerate(flat)}
    for run in zones["runs"]:
        s = run["start"].split(" w")
        e = run["end"].split(" w")
        n = pos[(e[0], int(e[1]))] - pos[(s[0], int(s[1]))] + 1
        run_ok &= (n == run["words"])
    A.append(("witness word counts equal the three language runs (345 / 3599 / 1975 words)", run_ok))
    mix_ok = all(len(sk[k].split()) == zones_mv["words"] == len(zones_mv["sequence"])
                 for zones_mv in zones["mixed_verses"] for k in [zones_mv["ref"]])
    A.append(("mixed verse MT 2:4: 12 words, switch before word 5",
              mix_ok and sw == {"Dan.2.4": ("H", "A", 5)}))

    def lst(keys):
        return sorted(set(keys), key=vkey)

    # datelines
    dl_entries, quotes = [], []
    for L in "HA":
        for k in m[("dateline", L)]:
            e = dateline_entry(k, L, m["parts"][k][L])
            w = web[mt_to_web(*vkey(k))]
            g = WEB_YEAR.search(w[0])
            wt = g.group(0) if g else None
            quotes.append(wt)
            other = sorted({t for t in m["parts"][k][L].split() if re.search(YEAR[L]["substring"], t)} - {e["year_form"]})
            md = [t for t in m["parts"][k][L].split()
                  if re.search(MONTH[L]["anchored"], " " + t) or re.search(DATE_CONSTRUCTION[L], " " + t)]
            dl_entries.append({
                "mt": k, "web": web_ref(k), "language": LANG[L], "year_form": e["year_form"],
                "numeral": e["numeral"], "regnal_term": e["regnal_term"], "month_or_day": md[0] if md else None,
                "reign_named": ({"mt": e["reign_named_mt"], "web": g.group("name")} if e["reign_named_mt"] else None),
                "reign_note": (None if e["reign_named_mt"] else
                               "למלכו 'his reign': the king is not named on the face of this verse"),
                "web_text": wt, "other_year_tokens_in_verse": other})
    dl_entries.sort(key=lambda d: vkey(d["mt"]))
    dl_keys = [d["mt"] for d in dl_entries]
    readings = {}
    for name, pat in DATELINE_READINGS.items():
        rk = lst(hits(m["parts"], order, "H", pat) + hits(m["parts"], order, "A", pat))
        readings[name] = {"count": len(rk), "verses_mt": rk}
    ezek_rule = lst([k for k in order if re.search(EZEK_DATE["YEAR"], sk[k])
                     and (re.search(EZEK_DATE["MONTH"], sk[k]) or re.search(EZEK_DATE["DAY"], sk[k]))])
    readings["ezekiel_rule_year_word_plus_month_or_day (NOT USED)"] = {"count": len(ezek_rule), "verses_mt": ezek_rule}

    # year words that are not datelines
    ynd = lst(m[("year_not_dateline", "H", "substring")] + m[("year_not_dateline", "A", "substring")])
    ynd_anc = lst(m[("year_not_dateline", "H", "anchored")] + m[("year_not_dateline", "A", "anchored")])
    notes = {}
    for k in ynd:
        cls, why, kw = YEAR_NOTES.get(k, (None, None, None))
        ev = web_slice(web[mt_to_web(*vkey(k))], kw) if kw else None
        quotes.append(ev)
        notes[k] = {"web": web_ref(k), "language": LANG[m["lang"][k][0]], "reason_class": cls, "reason": why,
                    "web_evidence": ev,
                    "token": sorted({t for L in m["lang"][k] for t in m["parts"][k][L].split()
                                     if re.search(YEAR[L]["substring"], t)})}
    A.append(("every year-word non-dateline carries a curated reason, and no curated reason is stale",
              set(YEAR_NOTES) == set(ynd) and all(n["web_evidence"] for n in notes.values())))

    # calendar dates without a year
    cal = lst(m[("calendar", "H")] + m[("calendar", "A")])
    cal_entries = []
    for k in cal:
        L = m["lang"][k][0]
        w = web[mt_to_web(*vkey(k))]
        g = WEB_DAY.search(w[0])
        quotes.append(g.group(0) if g else None)
        cal_entries.append({"mt": k, "web": web_ref(k), "language": LANG[L],
                            "month_or_day": [t for t in m["parts"][k][L].split()
                                             if re.search(DATE_CONSTRUCTION[L], " " + t)
                                             or re.search(DAY[L]["anchored"], " " + t)],
                            "web_text": g.group(0) if g else None})
    md_nd = lst(m[("md_not_date", "H")] + m[("md_not_date", "A")])
    md_art = lst(m[("md_artifact", "H")] + m[("md_artifact", "A")])

    def md_tokens(k, rd):
        return sorted({t for L in m["lang"][k] for t in m["parts"][k][L].split()
                       if re.search(MONTH[L][rd], " " + t if rd == "anchored" else t)
                       or re.search(DAY[L][rd], " " + t if rd == "anchored" else t)})

    # classification exactly once, per family and language (hits of the primary readings)
    once = True
    for L in "HA":
        dl, calL = set(m[("dateline", L)]), set(m[("calendar", L)])
        ynL = set(m[("year_not_dateline", L, "substring")])
        mdL, artL = set(m[("md_not_date", L)]), set(m[("md_artifact", L)])
        for k in m[("year", L, "substring")]:
            once &= ((k in dl) + (k in ynL)) == 1
        for fam in ("month", "day"):
            for k in m[(fam, L, "substring")]:
                once &= ((k in dl) + (k in calL) + (k in mdL) + (k in artL)) == 1
        for k in set(m[("dateline", L)]) | set(m[("date_construction", L)]):
            once &= ((k in dl) + (k in calL) + (k in ynL)) == 1
        once &= set(m[("dateline", L)]) <= set(m[("year", L, "substring")])
    A.append(("every hit of the date, year, month and day patterns is classified exactly once", once))

    # formulae
    formulae = {}
    for name, pat, gloss in EZEK_FORMULAE:
        h = hits(m["parts"], order, "H", pat)
        formulae[name] = {"gloss": gloss + "; tried in Daniel so a later sweep does not try it again",
                          "language": "Hebrew", "pattern": pat, "count": len(h), "verses_mt": h,
                          "cross_language_hits": hits(m["parts"], order, "A", pat)}
    for name, L, pat, gloss in FORMULAE:
        h = hits(m["parts"], order, L, pat)
        formulae[name] = {"gloss": gloss, "language": LANG[L], "pattern": pat, "count": len(h), "verses_mt": h,
                          "cross_language_hits": hits(m["parts"], order, "A" if L == "H" else "H", pat)}
    formulae["blessed_aram"]["homograph_note"] = (
        "MT 6:11 matches on ברך 'he knelt' (ברך על ברכוהי 'kneeling on his knees'), not 'bless'; kept and labelled")
    for f in formulae.values():
        zd = zone_dual(f["verses_mt"])
        if zd:
            f["web_for_zone_refs"] = zd

    # language switches from the zones file
    switches = []
    runs = zones["runs"]
    for a, b in zip(runs, runs[1:]):
        ref, w = b["start"].split(" w")
        switches.append({"mt": ref, "web": web_ref(ref), "from": LANG[a["lang"]], "to": LANG[b["lang"]],
                         "word_index": int(w)})

    # face-safe lists
    def listing(gloss, keys, **extra):
        d = {"gloss": gloss, "count": len(keys), "verses_mt": keys}
        d.update(extra)
        zd = zone_dual(keys)
        if zd:
            d["web_for_zone_refs"] = zd
        return d

    dp = [list(vkey(k)) for k in dl_keys]
    cp = [list(vkey(k)) for k in cal]
    out = {
        "book": BOOK,
        "produced_by": PRODUCED_BY,
        "witness": "WLC (OSHB), Dan_oshb.txt, single witness; refs are MT",
        "numbering": ("MT != WEB in four zones: MT 3:31-33 = WEB 4:1-3; MT 4:1-34 = WEB 4:4-37; MT 6:1 = WEB 5:31; "
                      "MT 6:2-29 = WEB 6:1-28; identity elsewhere (web_mt_offset_map.json). Every ref in a zone "
                      "carries both faces: entries carry mt and web, and every list carries web_for_zone_refs."),
        "numbering_face": "MT",
        "numbering_face_obligation_on_consumers": (
            "this inventory is on the MT face; verse_inventory.json beside it declares the WEB face. A consumer "
            "must assert the face it expects before any verse arithmetic, and convert with web_mt_offset_map.json."),
        "method": ("consonantal-skeleton regex over Dan_oshb.txt (NFD, points and accents U+0591-U+05C7 stripped; "
                   f"maqaf measured {maqaf}, and would become a space). Counts are of VERSES containing a form. Each "
                   "pattern is written for one language and matched only on that language's text per "
                   "dan_language_zones.json; MT 2:4 is split by word index (words 1-4 Hebrew, 5-12 Aramaic)."),
        "inputs": inputs,
        "web_format": {"verse_lines": len(web), "continuation_lines": cont_lines,
                       "verses_with_continuation_lines": sum(1 for v in web.values() if len(v) > 1),
                       "note": ("Dan_web_clean.txt has one '[v] N' line per verse, plus poetry and paragraph "
                                "continuation lines; every WEB quotation here is sliced from a single line and "
                                "asserted byte-exact in the file")},
        "totals": {"verses": len(order), "chapters": len(chapters), "verses_by_language": by_lang,
                   "verses_per_chapter_mt": per_ch,
                   "words_by_language": zones["word_totals"]},
        "datelines": {
            "gloss": ("REGNAL DATELINES: the ב-prefixed year construct בשנת, a numeral word, then a ל-prefixed "
                      "regnal term (למלכות / למלכו / ל+king). Structural. Daniel dates by regnal year and no "
                      "dateline carries a month or day term, so Ezekiel's rule (year word + month/day) finds "
                      "none; every reading is reported under readings."),
            "count": len(dl_keys), "verses_mt": dl_keys, "entries": dl_entries, "readings": readings},
        "year_word_but_not_a_dateline": listing(
            ("year-word verses that are not datelines, under the SUBSTRING reading (as Ezekiel's). The count "
             f"depends on the match semantics: {len(ynd)} under substring, {len(ynd_anc)} under the word-anchored "
             "reading (which drops the suffixed and embedded forms). The dateline count is "
             f"{len(dl_keys)} under either."), ynd,
            anchored_reading=listing("the same list under the word-anchored reading", ynd_anc), notes=notes),
        "calendar_dates_not_datelines": listing(
            ("a month or day-of-month date construction (word-anchored [לב]חדש / [לב]ירח) in a verse with no "
             "year word. A fact, not an onset rule: no Daniel ruling restricts onsets at calendar dates."),
            cal, entries=cal_entries),
        "month_or_day_word_not_a_date": listing(
            ("verses where a month or day word (anchored reading) stands outside any dateline or calendar date: "
             "durations, day counts, 'the end of the days', 'as at this day'. Listed so a sweep does not "
             "rediscover them; the tokens are recorded."), md_nd,
            tokens={k: md_tokens(k, "anchored") for k in md_nd}),
        "month_or_day_substring_artifacts": listing(
            ("verses hit only by the month/day SUBSTRING reading, not the anchored one: חכימי 'wise men', "
             "ימינו 'his right hand', מימי 'waters of' and the like."), md_art,
            tokens={k: md_tokens(k, "substring") for k in md_art}),
        "date_family_patterns": {
            "year": YEAR, "month": MONTH, "day": DAY, "dateline": DATELINE_RX,
            "date_construction": DATE_CONSTRUCTION,
            "primary_reading": {"year": "substring", "month": "substring (both readings agree)",
                                "day": "anchored; substring-only hits are month_or_day_substring_artifacts"},
            "per_language_counts": {
                LANG[L]: {"datelines": len(m[("dateline", L)]),
                          "year_word_not_dateline_substring": len(m[("year_not_dateline", L, "substring")]),
                          "year_word_not_dateline_anchored": len(m[("year_not_dateline", L, "anchored")]),
                          "calendar_dates": len(m[("calendar", L)]),
                          "month_or_day_word_not_a_date": len(m[("md_not_date", L)]),
                          "month_or_day_substring_artifacts": len(m[("md_artifact", L)])} for L in "HA"}},
        "formulae": formulae,
        "language_switches": switches,
        "citation_sweep_constants": {
            "face": "MT",
            "face_basis": ("Ezekiel's citation_sweep.py states its calendar pairs are MT pairs and converts every "
                           "WEB span or ref with web_to_mt before comparing (lines 308-313, 398-400, 598)"),
            "DATELINE_PAIRS": dp,
            "CAL_DATE_PAIRS": cp,
            "CAL_NO_ONSET": [],
            "CAL_NO_ONSET_statement": (
                "empty: no Daniel ruling restricts onsets at calendar dates. Ezekiel's CAL_NO_ONSET came from that "
                "book's strategy section 10 as clarified by its ruling G12(d), and does not carry over. These "
                "constants record facts only."),
            "zone_note": ("no DATELINE_PAIRS or CAL_DATE_PAIRS entry falls in a numbering zone, so the WEB-face "
                          "pairs are identical" if not any(in_zone(*p) for p in dp + cp) else
                          "SOME PAIRS FALL IN A ZONE: convert before comparing"),
        },
        "how_these_are_used": [
            "RULE: these are EVIDENCE, not a verdict. No boundary is set by a count alone; translation punctuation "
            "and editorial headings never drive one (E-23).",
            "RULE: a refrain CLOSES a unit, so a doxology or recognition refrain belongs to the unit BEFORE it.",
            "RULE: a seam is assessed from BOTH sides; an onset-only diagnosis is incomplete until the adjacent "
            "unit's close is weighed from bytes.",
            "RULE: this inventory is on the MT face; assert the face before comparing, and cite zone refs on both "
            "faces.",
            "HYPOTHESIS to test: the regnal datelines mark major onsets; weigh each against the close of the unit "
            "before it, and weigh a dateline inside direct speech separately.",
            "HYPOTHESIS to test: the Aramaic doxologies (everlasting dominion / kingdom, generation to generation, "
            "blessed, the recognition refrain) close court-tale units rather than open them.",
            "HYPOTHESIS to test: 'I was seeing' and 'behold' step scenes WITHIN a vision rather than open units.",
            "HYPOTHESIS to test: the language switches (MT 2:4 word 5; MT 8:1 word 1) are not by themselves unit "
            "boundaries: the first falls inside a verse.",
            "HYPOTHESIS to test: 'then', 'answered and said' and 'because of this' are narrative connectives, "
            "weak as boundary signals because of their frequency.",
        ],
        "ezek_key_crosswalk": None,  # filled below
        "for_fable_end_review": None,  # filled below
        "attribution": {
            "hebrew_aramaic": ("Hebrew witness WLC/OSHB, single witness; the witness carries its own attribution "
                               "terms, which travel with any quotation"),
            "english": "World English Bible (WEB); its attribution terms travel with any quotation",
        },
    }
    fz = {k: v["count"] for k, v in formulae.items()}
    out["ezek_key_crosswalk"] = crosswalk(fz, len(dl_keys))
    out["for_fable_end_review"] = [
        {"item": "MT 1:21 regnal terminus",
         "measurement": ("עד שנת אחת לכורש is a regnal-year construct with a ל-king term but no ב prefix; the rule "
                         f"used gives {len(dl_keys)} datelines, the any-year-construct reading gives "
                         f"{readings['any_year_construct_numeral_regnal (admits a terminus such as עד שנת)']['count']}"),
         "question": "is a regnal year named as an end point a dateline (it would enter DATELINE_PAIRS)?"},
        {"item": "MT 11:1 dateline inside direct speech",
         "measurement": ("11:1 matches the dateline rule (בשנת אחת לדריוש) and its WEB line opens a quotation "
                         "('As for me'); 10:1 is the preceding dateline and 10:4 a calendar date"),
         "question": "does a dateline embedded in a speaker's discourse belong to the same class as a narrative one?"},
        {"item": "MT 10:4 calendar date after a dated vision",
         "measurement": "day 24 of the first month, no year word; 10:1 three verses earlier carries the year",
         "question": ("is a calendar date that continues an earlier dateline onset-restricted? CAL_NO_ONSET is "
                      "empty here because no Daniel ruling exists")},
        {"item": "time-interval clauses",
         "measurement": ("MT 4:26 (WEB 4:29) 'at the end of twelve months' and the day counts (1:12-15, 12:11, "
                         f"12:12) are classified month_or_day_word_not_a_date ({len(md_nd)} verses)"),
         "question": "are interval clauses a class of their own for the calendar arm, or plain evidence?"},
        {"item": "model downgrade",
         "measurement": "this inventory was built and self-checked on claude-opus-5-5 as grader_fallback (OW-25)",
         "question": "the Fable end review is the first non-Opus check of these constants"},
    ]

    # ---- remaining self-assertions over the finished output
    listed = set()

    def walk(o):
        ok = True
        if isinstance(o, dict):
            if "count" in o and "verses_mt" in o:
                ok &= o["count"] == len(o["verses_mt"]) and len(set(o["verses_mt"])) == len(o["verses_mt"])
                listed.update(o["verses_mt"])
                zd = o.get("web_for_zone_refs", {})
                for k in o["verses_mt"]:
                    if in_zone(*vkey(k)):
                        ok &= zd.get(k) == "web:" + web_ref(k)
            if "mt" in o and "web" in o and isinstance(o["mt"], str) and o["mt"].startswith(BOOK + "."):
                listed.add(o["mt"])
                ok &= o["web"] == web_ref(o["mt"])
            for v in o.values():
                ok &= walk(v)
        elif isinstance(o, list):
            for v in o:
                ok &= walk(v)
        return ok
    counts_ok = walk(out)
    A.append(("every count equals the length of its verse list (and no list repeats a verse)", counts_ok))
    A.append(("every zone ref carries both faces", counts_ok and all(
        ("web" in d) for d in dl_entries + cal_entries)))
    A.append(("every verse listed exists in the witness", listed <= set(order) and len(listed) > 0))
    A.append(("every WEB quotation is found byte-exact in Dan_web_clean.txt",
              all(q and q in wtext for q in quotes)
              and all(d["reign_named"] is None or d["reign_named"]["web"] in d["web_text"] for d in dl_entries)))
    A.append(("citation_sweep constants equal the lists they come from",
              [f"{BOOK}.{c}.{v}" for c, v in dp] == dl_keys and [f"{BOOK}.{c}.{v}" for c, v in cp] == cal
              and out["citation_sweep_constants"]["CAL_NO_ONSET"] == []))
    A.append(("every formula has a language and a pattern that compiles",
              all(f["language"] in ("Hebrew", "Aramaic") and re.compile(f["pattern"]) for f in formulae.values())))
    out["self_assertions"] = [{"assertion": n, "holds": bool(ok)} for n, ok in A]
    return out, A


def crosswalk(fz, n_dl):
    c = lambda n: fz.get(n)
    top = [
        ("book", "book", "same role; value 'Dan'"),
        ("witness", "witness", "same role; single witness WLC/OSHB"),
        ("numbering", "numbering", "same role; Daniel has four zones in chs 3-6, not Ezekiel's ch 20/21 zone"),
        ("method", "method", "same role; adds the per-language matching and the 2:4 word-index split"),
        ("totals", "totals", "same role; adds verses_by_language and words_by_language"),
        ("verses_per_chapter_mt", "totals.verses_per_chapter_mt", "moved inside totals; still MT face"),
        ("formulae", "formulae", "same shape plus language, pattern and cross_language_hits"),
        ("dated_oracles", "datelines", f"renamed: Daniel's {n_dl} datelines are regnal (year + ל-king), not "
                                       "Ezekiel's year + month/day oracle datelines; a consumer reading "
                                       "dev['dated_oracles'] must be re-pointed"),
        ("year_word_but_not_a_dateline", "year_word_but_not_a_dateline", "same role; notes carry reason_class, "
                                                                          "reason and a WEB evidence slice"),
        ("word_event_family", None, "Daniel has no word-event formula: the three Ezekiel patterns measure "
                                    f"{c('ezek_word_event_formula')}, {c('ezek_word_event_vayehi_any')}, "
                                    f"{c('ezek_word_event_hayah_any')} verses and are kept under formulae as ezek_*"),
        ("calendar_dates_not_datelines", "calendar_dates_not_datelines", "same role and anchored rule; adds entries"),
        ("how_these_are_used", "how_these_are_used", "same role; rules separated from hypotheses to test"),
        ("known_hard_regions_to_flag_for_raised_coverage", None,
         "not produced: the brief does not ask for it, and choosing coverage regions is a planning step "
         "beyond an inventory; the measured inputs to it are numbering and language_switches"),
    ]
    frm = [
        ("word_event_formula", None, f"measured {c('ezek_word_event_formula')} in Daniel (kept as ezek_word_event_formula)"),
        ("word_event_vayehi_any", None, f"measured {c('ezek_word_event_vayehi_any')} (kept as ezek_word_event_vayehi_any)"),
        ("word_event_hayah_any", None, f"measured {c('ezek_word_event_hayah_any')} (kept as ezek_word_event_hayah_any)"),
        ("son_of_man_address", "son_of_man_heb / son_of_man_aram",
         f"measured {c('son_of_man_heb')} Hebrew and {c('son_of_man_aram')} Aramaic verses; not a recurring address in Daniel"),
        ("recognition_formula", "recognition_most_high_rules_aram",
         f"an analog, not an equivalent: Ezekiel's pattern measures {c('ezek_recognition_formula')}; the Aramaic "
         f"'that the Most High rules' refrain measures {c('recognition_most_high_rules_aram')}"),
        ("recognition_formula_2ms", "recognition_most_high_rules_aram",
         f"Ezekiel's 2ms pattern measures {c('ezek_recognition_formula_2ms')}; the Aramaic refrain includes its 2ms 'until you know' forms"),
        ("thus_says_the_lord_yhwh", None, f"measured {c('ezek_thus_says_the_lord_yhwh')}"),
        ("utterance_of_the_lord_yhwh", None, f"measured {c('ezek_utterance_of_the_lord_yhwh')}"),
        ("hand_of_yhwh_upon_me", None, f"measured {c('ezek_hand_of_yhwh_upon_me')}"),
        ("set_your_face", "set_face_heb", f"Ezekiel's pattern measures {c('ezek_set_your_face')}; Daniel's first-/third-person "
                                          f"'set (my/his) face' measures {c('set_face_heb')}"),
        ("i_am_yhwh_spoken", None, f"measured {c('ezek_i_am_yhwh_spoken')}"),
    ]
    return {"top_level": [{"ezek_key": a, "dan_key": b, "reason": r} for a, b, r in top],
            "formulae": [{"ezek_key": a, "dan_key": b, "reason": r} for a, b, r in frm]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(HERE))
    ap.add_argument("--out", default=str(HERE / "dan_device_inventory.json"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if a.selftest:
        res = selftest()
        for n, ok in res:
            print(("PASS " if ok else "FAIL ") + n)
        return 0 if all(ok for _, ok in res) else 1
    out, A = build(Path(a.root))
    data = json.dumps(out, ensure_ascii=False, indent=1) + "\n"
    Path(a.out).write_bytes(data.encode("utf-8"))
    for n, ok in A:
        print(("PASS " if ok else "FAIL ") + n)
    print(json.dumps({"datelines": out["datelines"]["verses_mt"],
                      "year_word_not_dateline": out["year_word_but_not_a_dateline"]["count"],
                      "calendar": out["calendar_dates_not_datelines"]["verses_mt"],
                      "sha256": hashlib.sha256(data.encode("utf-8")).hexdigest()}, ensure_ascii=False))
    return 0 if all(ok for _, ok in A) else 1


if __name__ == "__main__":
    sys.exit(main())
