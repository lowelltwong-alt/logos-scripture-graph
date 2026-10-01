#!/usr/bin/env python3
"""Rebuilds ../jer_device_inventory.json from bytes (orchestrator-run; agents
consume the JSON). Every count NAMES its object; all needles are
FINALS-NORMALIZED (E-11 discipline) and swept against the finals-normalized
skeleton index. MT keys throughout; use jer_lib crosswalk for WEB.

SECOND-PASS CORRECTED (probe _probe_devices2): the naive prefix-stripper ate
root-initial letters from the [vav-he-bet-lamed-kaf-mem-shin] class (it
mangled Shiloh and undercounted prefixed names) - prefix tolerance is now an
explicit per-length test. A FOURTH Nebuchadnezzar spelling surfaced
(plene nun-bet-vav-kaf-dalet-resh-aleph-tsadi-VAV-resh at 49:28, beside the
usual spelling in the SAME verse - the K/Q doubled-token signature); the
lone koh-amar-without-immediate-YHWH is the 7:20 adonai-YHWH stack (still
divine); hoy has a vav-prefixed shape at 34:5; all seven
neum-without-immediate-YHWH sites are divine-title stacks.

The Jeremiah frame spine this inventory serves:
 - WORD-EVENT formulas (the book's primary macro-seam device), by SHAPE.
 - KOH-AMAR census with the QUOTED-SPEECH ownership hazard (Hananiah speaks
   the full divine formula in ch 28; chs 27-29 quote formulas inside
   letters/confrontations) - machine output is shape counts + review lists.
 - NEUM-YHWH density (the OT's densest) + stack shapes + the 23:31 verb trap.
 - Date/reign header candidates (classified) and OAN headers.
 - hoy shapes (woe onsets vs funeral cries vs day-alas vs sword apostrophe).
 - Name spelling variants (Jeremiah 2; Nebuchadnezzar 4; Jehoiachin 3 name
   forms; Zedekiah/Jehoiakim/Gedaliah plene-defective pairs; Shiloh by site).
 - The 51:64 colophon + ch-52 appendix; the 10:11 Aramaic island; the
   1:11-12 shaqed/shoqed pun; chapter texture.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent
BOOK = "Jer"

POINTS = re.compile(r"[֑-ׇ]")
FINALS = str.maketrans("ךםןףץ", "כמנפצ")
PREFIX_LETTERS = set("והבלכמש")


def skel(s: str) -> str:
    return POINTS.sub("", unicodedata.normalize("NFD", s)).replace("־", " ").translate(FINALS)


oshb_raw: dict[str, str] = {}
for line in (SPBOOK / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").splitlines():
    if "\t" in line:
        ref, text = line.split("\t", 1)
        oshb_raw[ref.split(".", 1)[1]] = text          # "C.V" keys
SK = {k: skel(v) for k, v in oshb_raw.items()}
TOK = {k: v.split() for k, v in SK.items()}
KEY = lambda k: tuple(map(int, k.split(".")))


def token_matches(tok: str, base: str) -> bool:
    """tok equals base with 0-2 attached prefix letters. Explicit per-length
    test - never strips into the base itself (the second-pass bug fix)."""
    if tok == base:
        return True
    if len(tok) == len(base) + 1 and tok[0] in PREFIX_LETTERS and tok[1:] == base:
        return True
    if (len(tok) == len(base) + 2 and tok[0] in PREFIX_LETTERS
            and tok[1] in PREFIX_LETTERS and tok[2:] == base):
        return True
    return False


def verses_with_phrase(phrase: str) -> list[str]:
    p = phrase.translate(FINALS)
    return sorted((k for k in SK if f" {p} " in f" {SK[k]} "), key=KEY)


def verses_with_token(token: str, prefixes: bool = False) -> list[str]:
    t = token.translate(FINALS)
    if prefixes:
        return sorted((k for k in TOK if any(token_matches(x, t) for x in TOK[k])), key=KEY)
    return sorted((k for k in TOK if t in TOK[k]), key=KEY)


def initial(keys: list[str], phrase: str) -> list[str]:
    p = phrase.translate(FINALS)
    return [k for k in keys if SK[k].startswith(p)]


def main() -> int:
    pm = json.loads((SPBOOK / "pmarks_Jer.json").read_text(encoding="utf-8"))
    kq = pm["kq"]
    inv: dict = {"book": BOOK, "witness": "WLC (OSHB) single witness; MT keys",
                 "normalization": ("all needles finals-normalized (E-11); counts are VERSE "
                                   "counts unless stated; 'prefixed' = 0-2 attached "
                                   "[vav/he/bet/lamed/kaf/mem/shin] letters, tested "
                                   "per-length (never stripped into the base)")}

    # ---- word-event formulas, by shape ----
    vayehi = verses_with_phrase("ויהי דבר יהוה")
    vayehi_initial = initial(vayehi, "ויהי דבר יהוה")
    hadavar = verses_with_phrase("הדבר אשר היה אל ירמיהו")
    asher_hayah = verses_with_phrase("אשר היה דבר יהוה אל ירמיהו")
    inv["word_event_formula"] = {
        "debar_yhwh_phrase_verses": len(verses_with_phrase("דבר יהוה")),
        "vayehi_debar_yhwh": {"verses": vayehi, "count": len(vayehi),
                              "verse_initial_count": len(vayehi_initial),
                              "non_initial": sorted(set(vayehi) - set(vayehi_initial), key=KEY),
                              "non_initial_note": "42:7 - the ten-days wait: vayehi miqqets aseret yamim, THEN the formula"},
        "hadavar_asher_hayah_el_yirmeyahu": {"verses": hadavar, "count": len(hadavar),
                                             "note": "the prose-sermon superscription shape; all verse-initial"},
        "asher_hayah_debar_yhwh_el_yirmeyahu": {"verses": asher_hayah, "count": len(asher_hayah),
                                                "note": "the OAN/topical header shape (14:1 drought, 46:1 nations rubric, 47:1 Philistines, 49:34 Elam)"},
        "note": ("THREE shapes + the non-initial site - never blend; the shapes mark "
                 "DIFFERENT unit classes (narrative onset vs prose-sermon superscription vs "
                 "OAN/topical header)"),
    }

    # ---- koh-amar census ----
    koh_amar = verses_with_phrase("כה אמר")
    koh_amar_yhwh = verses_with_phrase("כה אמר יהוה")
    koh_amar_tsevaot = verses_with_phrase("כה אמר יהוה צבאות")
    koh_adonai = verses_with_phrase("כה אמר אדני יהוה")
    inv["koh_amar"] = {
        "total_verses": len(koh_amar),
        "with_yhwh_verses": len(koh_amar_yhwh),
        "with_yhwh_tsevaot_verses": len(koh_amar_tsevaot),
        "adonai_yhwh_stack": {"verses": koh_adonai,
                              "note": "7:20 - koh amar ADONAI YHWH: the one site where YHWH is not the immediately following word; still the divine formula (title stack)"},
        "quoted_speech_hazard": {
            "hananiah_full_formula_sites": [k for k in ("28.2", "28.11") if k in set(koh_amar)],
            "note": ("FRAME OWNERSHIP IS NOT MACHINE-DECIDABLE in Jer: HANANIAH speaks the "
                     "full divine formula (koh amar YHWH tsevaot) as a false prophet in ch "
                     "28; chs 27-29 letters/confrontations embed formulas inside quoted "
                     "speech. A koh-amar digit that does not name WHOSE mouth carries the "
                     "formula is meaningless (Isa i2 lesson, harder here)."),
        },
    }
    assert set(koh_amar) - set(koh_amar_yhwh) == set(koh_adonai), \
        "koh-amar shape accounting broken"

    # ---- neum ----
    neum_yhwh = verses_with_phrase("נאם יהוה")
    neum_tok = verses_with_token("נאם")
    neum_adonai = verses_with_phrase("נאם אדני יהוה")
    neum_melekh = verses_with_phrase("נאם המלך יהוה צבאות שמו")
    inv["neum"] = {
        "neum_yhwh_verses": len(neum_yhwh),
        "neum_token_verses": len(neum_tok),
        "adonai_yhwh_stacks": {"verses": neum_adonai,
                               "note": "ne'um adonai YHWH (tsevaot) - title-stack shape"},
        "melekh_signature": {"verses": neum_melekh,
                             "note": ("ne'um ha-melekh YHWH tsevaot shemo - 'says the King, "
                                      "whose name is YHWH of Armies': an OAN-zone signature "
                                      "(46:18, 48:15, 51:57)")},
        "verb_trap": ("23:31 carries BOTH the divine formula (ne'um-YHWH) AND the only "
                      "occurrence of the VERB na'am (vayin'amu ne'um) - of the false "
                      "prophets; a bare ne'um token sweep blends noun and verb THERE"),
        "verb_site_in_token_sweep": "23.31" in neum_tok,
    }
    assert set(neum_melekh) == {"46.18", "48.15", "51.57"}, "melekh-signature sites moved"

    # ---- date/reign header candidates (classified from bytes) ----
    date_rows = []
    for k in sorted(SK, key=KEY):
        hits = [t for t in TOK[k] if t in ("בשנת", "בשנה", "ובשנת", "ובשנה")]
        # bet+cardinal date shape (E-03-instance correction 2026-08-28): the year
        # word follows a bet-prefixed cardinal instead of carrying the bet itself
        # (byte-confirmed victims: 1:2 header-internal, 39:2 verse-initial).
        for _i, _t in enumerate(TOK[k]):
            if _t.startswith("ב") and "שנה" in TOK[k][_i + 1:_i + 3] and _t in ("בעשתי", "בשלש"):
                hits.append(_t)
        if not hits:
            continue
        opening = " ".join(TOK[k][:5])
        if k in ("17.8", "51.46"):
            cls = "not_a_date (17:8 year-of-drought simile; 51:46 year-by-year rumor)"
        elif k == "28.17":
            cls = "narrative_date (Hananiah death notice, same-year)"
        elif SK[k].startswith(("ויהי בשנה", "בשנה", "בשנת", "ויהי בשלשים", "בעשתי עשרה")):
            cls = "verse_initial_date_frame"
        else:
            cls = "header_internal_date (date inside a hadavar/asher-shape header or list row)"
        date_rows.append({"ref": k, "tokens": hits, "opening": opening, "class": cls})
    inv["date_headers"] = {
        "candidates": date_rows,
        "bereshit_mamlekhet": sorted(
            set(verses_with_phrase("בראשית ממלכת") + verses_with_phrase("בראשית ממלכות")),
            key=KEY),
        "bereshit_mamlekhet_note": ("TWO attested spellings of the construct, per-form "
                                    "(E-03-instance correction 2026-08-28, byte-verified): "
                                    "26:1 mamlekhut (vav plene), verse-initial; 27:1 "
                                    "mamlekhet, verse-initial; 28:1 mamlekhet, MID-VERSE "
                                    "after vayehi-bashanah-hahi"),
        "note": ("the reign-dated spine of chs 21-45 + 52; classification of non-initial "
                 "sites is per-site READ, recorded here from openings; writers argue "
                 "dated frames from their own verses"),
    }
    assert inv["date_headers"]["bereshit_mamlekhet"] == ["26.1", "27.1", "28.1"], \
        "bereshit-mamlekhet sites moved (expected the byte-verified 3-site set)"

    # ---- OAN headers (chs 46-51) ----
    inv["oan_headers"] = {
        "lamed_initial_headers": [
            {"ref": "46.2", "nation": "Egypt (topical: Pharaoh Neco's army)"},
            {"ref": "48.1", "nation": "Moab"},
            {"ref": "49.1", "nation": "Ammon (li-vnei Ammon)"},
            {"ref": "49.7", "nation": "Edom"},
            {"ref": "49.23", "nation": "Damascus"},
            {"ref": "49.28", "nation": "Kedar + kingdoms of Hazor"},
        ],
        "false_candidate_excluded": "51:16 le-qol (at-the-sound phrase, not a header)",
        "other_header_shapes": {
            "46.1": "asher-hayah rubric over the nations block",
            "47.1": "asher-hayah (Philistines, before-Pharaoh-struck-Gaza date)",
            "49.34": "asher-hayah (Elam, dated to Zedekiah's accession)",
            "50.1": "hadavar-asher-dibber shape (Babylon, be-yad Yirmeyahu)",
        },
        "note": "six lamed-initial nation headers + four non-lamed header shapes; per-site roles read from bytes",
    }
    assert SK["50.1"].startswith("הדבר אשר דבר יהוה אל בבל"), "50:1 Babylon header moved"

    # ---- hoy shapes ----
    hoy = verses_with_token("הוי")
    vhoy = verses_with_token("והוי")
    inv["hoy"] = {
        "bare_verses": hoy, "bare_count": len(hoy),
        "verse_initial": [k for k in hoy if TOK[k][0] == "הוי"],
        "vav_prefixed_verses": vhoy,
        "shapes": {
            "woe_oracle_onsets": ["22.13", "23.1"],
            "woe_inside_oan_header_verse": ["48.1"],
            "woe_after_battle_call": ["50.27"],
            "day_alas": ["30.7"],
            "funeral_cries": ["22.18 (fourfold: bare hoy AND vav-prefixed ve-hoy in one verse)",
                              "34.5 (vav-prefixed ve-hoy adon ONLY)"],
            "sword_apostrophe": ["47.6"],
        },
        "note": ("ROLE SPLIT REQUIRED before any digit: woe-onset vs funeral cry vs "
                 "day-alas vs sword apostrophe; the funeral cries carry the VAV-PREFIXED "
                 "shape (ve-hoy) - 34:5 has ONLY that shape and is invisible to a "
                 "bare-token sweep, 22:18 has BOTH shapes in one verse; oy (aleph) is a "
                 "different lexeme"),
    }
    assert set(hoy) == {"22.13", "22.18", "23.1", "30.7", "47.6", "48.1", "50.27"}, \
        f"hoy inventory moved: {hoy}"
    assert vhoy == ["22.18", "34.5"], f"vav-prefixed hoy moved: {vhoy}"
    inv["oy_distinct_lexeme"] = {"verses": verses_with_token("אוי")}

    # ---- names with spelling variants (prefix-tolerant, fixed matcher) ----
    def name_entry(**variants):
        out = {}
        allv = set()
        for name, tok in variants.items():
            vs = verses_with_token(tok, prefixes=True)
            out[name] = {"verses": len(vs), "sites": vs if len(vs) <= 15 else vs[:15] + ["..."]}
            allv |= set(vs)
        out["any_variant_verses"] = len(allv)
        return out

    inv["jeremiah_name"] = name_entry(yirmeyahu_long="ירמיהו", yirmeyah_short="ירמיה")
    inv["jeremiah_name"]["note"] = (
        "BOTH spellings attested. SWEEP HAZARD: the short form is a consonantal SUBSTRING "
        "of the long form - token-bound sweeps only. AND the noun remiyyah "
        "(deceit/slackness, 48:10) is a substring of BOTH (yod+resh-mem-yod-he+vav) - a "
        "bare substring sweep for the deceit-noun matches inside every occurrence of the "
        "prophet's name.")
    inv["nebuchadnezzar_name"] = name_entry(
        nevukhadretsar="נבוכדראצר", nevukhadretsar_plene_vav="נבוכדראצור",
        nevukhadnetsar="נבוכדנאצר", nevukhadnetsar_defective="נבכדנאצר")
    inv["nebuchadnezzar_name"]["note"] = (
        "FOUR live spellings. The resh-family dominates (chs 21-52 narrative + OAN); the "
        "nun-family clusters in chs 27-29; 28:11/28:14 carry the vav-less defective. THE "
        "49:28 TRAP: the plene nevukhadretsar-with-vav spelling stands BESIDE the usual "
        "one in the SAME verse (K/Q doubled token - check pmarks kq before slicing "
        "there). Name-form claims name their spelling.")
    inv["nebuchadnezzar_name"]["kq_at_49_28"] = bool(kq.get("Jer.49.28"))
    inv["zedekiah_name"] = name_entry(tsidqiyahu="צדקיהו", tsidqiyah="צדקיה")
    inv["jehoiakim_name"] = name_entry(yehoyaqim="יהויקים", yehoyaqim_defective="יהויקם")
    inv["jehoiakim_name"]["note"] = "27:1 carries the DEFECTIVE spelling (the famous Jehoiakim-vs-Zedekiah setting crux verse)"
    inv["jehoiachin_king"] = name_entry(yehoyakhin="יהויכין", yekhonyahu="יכניהו",
                                        khonyahu="כניהו", yekhonyah="יכניה")
    inv["jehoiachin_king"]["note"] = ("ONE king, THREE name forms (Jehoiachin 52:31 / "
                                      "Jeconiah 24:1, 27:20, 28:4, 29:2 / Coniah 22:24, "
                                      "22:28, 37:1) - name the form before any digit")
    inv["gedaliah_name"] = name_entry(gedalyahu="גדליהו", gedalyah="גדליה")
    inv["baruch"] = name_entry(barukh="ברוך")
    inv["baruch"]["note"] = ("Baruch ben-Neriah sites cluster in chs 32, 36, 43, 45 (the "
                             "scroll, the deed, the Egypt descent, the personal oracle); "
                             "the token also reads 'blessed' (barukh) - 17:7 and 20:14 "
                             "are the passive participle, NOT the scribe; per-site reading "
                             "before any digit")
    inv["hananiah"] = name_entry(chananyah="חנניה")
    inv["pashhur"] = name_entry(pashchur="פשחור")
    shilo_sites = {}
    for k in sorted(SK, key=KEY):
        for t in TOK[k]:
            for base in ("שלו", "שילו", "שלה", "שילה"):
                if token_matches(t, base):
                    shilo_sites.setdefault(k, []).append(t)
    inv["shiloh_place"] = {
        "candidate_tokens_by_verse": shilo_sites,
        "note": ("Shiloh spelling VARIES BY SITE in WLC Jer; the bases also collide with "
                 "unrelated words (shalu, mashal-forms, the relative she-lo) - the "
                 "temple-warning sites (chs 7, 26, 41:5) need per-site byte reading; "
                 "sweep per attested form only"),
    }
    inv["rachel"] = name_entry(rachel="רחל")

    # ---- divine names ----
    yhwh = verses_with_token("יהוה")
    tsevaot = verses_with_phrase("יהוה צבאות")
    stacked = verses_with_phrase("יהוה צבאות אלהי ישראל")
    adonai = verses_with_token("אדני")
    # POINT-AWARE partition (E-03-instance correction 2026-08-28, byte-verified):
    # the skeleton token is shared by the divine title (qamats under the nun) and
    # the human courtly address adoni (hiriq) - "my lord the king" to Zedekiah.
    import unicodedata as _ud
    from jer_lib import load_verse_maps as _lvm
    _, _oshb_pointed = _lvm()

    def _adonai_form(ref):
        for w in _oshb_pointed[f"Jer.{ref}"]["text"].split():
            skel = "".join(ch for ch in _ud.normalize("NFD", w)
                           if not _ud.combining(ch)).strip("־ ")
            if skel in ("אדני", "ואדני", "לאדני", "באדני"):
                tail = _ud.normalize("NFD", w)
                tail = tail[tail.rfind("נ") + 1:]
                if "ָ" in tail:
                    return "divine"
                if "ִ" in tail:
                    return "courtly"
        return "unclassified"

    adonai_divine = [r for r in adonai if _adonai_form(r) == "divine"]
    adonai_courtly = [r for r in adonai if _adonai_form(r) == "courtly"]
    assert len(adonai_divine) + len(adonai_courtly) == len(adonai) == 13, \
        "adonai point-aware partition broken (expected 11 divine + 2 courtly = 13 token sites)"
    assert adonai_courtly == ["37.20", "38.9"], "courtly adoni sites moved"
    # PREFIXED forms (E-03-instance correction 2026-08-28, writer-caught at 50:25;
    # sibling audit found 46:10 as well): la-adonai is a DIFFERENT token, outside
    # the bare-token object above; all attested prefixed tokens are divine (qamats).
    la_adonai = []
    for _k, _v in sorted(_oshb_pointed.items(),
                         key=lambda kv: tuple(map(int, kv[0].split(".")[1:]))):
        for _w in _v["text"].split():
            _skel = "".join(ch for ch in _ud.normalize("NFD", _w)
                            if not _ud.combining(ch)).strip("־ ")
            if _skel in ("לאדני", "ואדני", "באדני", "כאדני"):
                _ref = _k.split("Jer.")[1]
                if _ref not in la_adonai:
                    la_adonai.append(_ref)
    assert la_adonai == ["46.10", "50.25"], "prefixed la-adonai sites moved"
    assert all(_adonai_form(r) == "divine" for r in la_adonai), \
        "prefixed adonai form expected divine (qamats) at all attested sites"
    inv["divine_names"] = {
        "yhwh_verses": len(yhwh),
        "yhwh_tsevaot_verses": len(tsevaot),
        "yhwh_tsevaot_elohei_yisrael_verses": len(stacked),
        "stacked_form_note": ("the FULL title 'YHWH of Armies, the God of Israel' is a Jer "
                              "signature (32 verses) - its OWN object, never blended with "
                              "bare tsevaot"),
        "adonai_token_verses": len(adonai),
        "adonai_sites": adonai,
        "adonai_divine_title_sites": adonai_divine,
        "adoni_courtly_sites": adonai_courtly,
        "la_adonai_prefixed_sites": la_adonai,
        "la_adonai_note": ("PREFIXED la-adonai is its OWN token object (E-03-instance "
                           "correction 2026-08-28): 46:10 (twice in the verse) + 50:25, "
                           "both divine-title stacks (qamats), both in the OAN block; "
                           "never blended with the 13 bare-token sites"),
        "adonai_note": ("POINT-AWARE (E-03-instance correction 2026-08-28): of the 13 "
                        "skeleton-token sites, 11 are the divine title (qamats); 37:20 and "
                        "38:9 are the human courtly address adoni (hiriq, 'my lord the "
                        "king' to Zedekiah) - the courtly role-split IS live in Jer's "
                        "narrative zone, contra this note's earlier text"),
    }

    # ---- motif roots (sweep-hazard entries; counts name their object) ----
    shuv_bare = verses_with_token("שוב", prefixes=True)
    inv["motif_roots"] = {
        "shuv_bare_or_prefixed_token_verses": len(shuv_bare),
        "shuv_note": ("OBJECT: the bare/prefixed token form only. The shuv return/turn "
                      "root is Jer's signature wordplay (3:1-4:4 cluster: shuvu banim "
                      "shovavim; meshuvah faithlessness) but it INFLECTS far beyond any "
                      "single needle (shuvu, yashuv, meshuvah, shovav...) and the staged "
                      "tools carry NO morphology layer - every root-level claim needs its "
                      "own per-form sweep with the form named"),
        "meshuvah_faithlessness_verses": verses_with_token("משובה", prefixes=True) +
                                          verses_with_token("משבה", prefixes=True),
        "tsafon_north_verses": len(verses_with_token("צפון", prefixes=True)),
        "tsafon_note": "the foe-from-the-north motif carrier (mitstsafon); prefix-tolerant token count",
        "sheqer_falsehood_verses": len(verses_with_token("שקר", prefixes=True)),
        "sheqer_note": ("sheqer (falsehood) is a Jer keyword - DISTINCT from shaqed "
                        "(almond) / shoqed (watching): the 1:11-12 call-vision pun; a "
                        "2-letter-overlap sweep blends them"),
        "shaqed_shoqed_pun": {"almond_1_11": "שקד" in TOK["1.11"],
                              "watching_1_12": "שקד" in TOK["1.12"]},
    }
    assert inv["motif_roots"]["shaqed_shoqed_pun"] == {"almond_1_11": True, "watching_1_12": True}

    # ---- colophon + appendix ----
    inv["colophon_51_64"] = {
        "present": f" {skel('עד הנה דברי ירמיהו')} " in f" {SK['51.64']} ",
        "note": ("51:64 closes with 'Thus far are the words of Jeremiah' - the book's own "
                 "colophon BEFORE the ch-52 historical appendix (= 2 Kgs 24:18-25:30 "
                 "parallel: typed-relation metadata, NEVER boundary evidence - the Isa "
                 "chs 36-39 law carries)"),
    }
    assert inv["colophon_51_64"]["present"]

    # ---- Aramaic island ----
    inv["aramaic_island"] = {
        "verse": "10.11",
        "kidnah_initial": SK["10.11"].startswith("כדנה"),
        "note": "the single Aramaic verse (byte-proven from morph codes; see pmarks)",
    }
    assert inv["aramaic_island"]["kidnah_initial"]

    # ---- chapter texture table ----
    web = json.loads((TOOLS / "verse_map_web.json").read_text(encoding="utf-8"))
    ka_set, ny_set = set(koh_amar), set(neum_yhwh)
    we_set = set(vayehi) | set(hadavar) | set(asher_hayah)
    y_set = set(yhwh)
    texture = {}
    for ch in range(1, 53):
        keys = [k for k in SK if int(k.split(".")[0]) == ch]
        wkeys = [k for k in web if int(k.split(".")[1]) == ch]
        texture[str(ch)] = {
            "mt_verses": len(keys),
            "web_poetry_line_verses": sum(1 for k in wkeys if web[k]["poetry_lines"]),
            "koh_amar": sum(1 for k in keys if k in ka_set),
            "neum_yhwh": sum(1 for k in keys if k in ny_set),
            "word_event": sum(1 for k in keys if k in we_set),
            "yhwh": sum(1 for k in keys if k in y_set),
        }
    inv["chapter_texture"] = texture
    inv["chapter_texture_note"] = ("staging profile for the at-scale part plan; writers "
                                   "re-derive, never row evidence")

    (SPBOOK / "jer_device_inventory.json").write_text(
        json.dumps(inv, ensure_ascii=False, indent=1), encoding="utf-8")

    summary = {
        "word_event": {"vayehi": len(vayehi), "hadavar": len(hadavar),
                       "asher_hayah": len(asher_hayah)},
        "koh_amar": {"total": len(koh_amar), "yhwh": len(koh_amar_yhwh),
                     "tsevaot": len(koh_amar_tsevaot), "adonai_stack": len(koh_adonai)},
        "neum": {"yhwh": len(neum_yhwh), "token": len(neum_tok),
                 "adonai_stacks": len(neum_adonai), "melekh_signature": len(neum_melekh)},
        "date_candidates": len(date_rows),
        "hoy": {"bare": len(hoy), "vav_prefixed": vhoy},
        "jeremiah": {k: v["verses"] for k, v in inv["jeremiah_name"].items() if isinstance(v, dict)},
        "nebuchadnezzar": {k: v["verses"] for k, v in inv["nebuchadnezzar_name"].items() if isinstance(v, dict)},
        "kq_at_49_28": inv["nebuchadnezzar_name"]["kq_at_49_28"],
        "zedekiah": {k: v["verses"] for k, v in inv["zedekiah_name"].items() if isinstance(v, dict)},
        "jehoiakim": {k: v["verses"] for k, v in inv["jehoiakim_name"].items() if isinstance(v, dict)},
        "jehoiachin": {k: v["verses"] for k, v in inv["jehoiachin_king"].items() if isinstance(v, dict)},
        "gedaliah": {k: v["verses"] for k, v in inv["gedaliah_name"].items() if isinstance(v, dict)},
        "baruch": inv["baruch"]["barukh"]["verses"],
        "shiloh_sites": inv["shiloh_place"]["candidate_tokens_by_verse"],
        "divine": {"yhwh": len(yhwh), "tsevaot": len(tsevaot), "stacked": len(stacked),
                   "adonai_divine": len(adonai_divine), "adoni_courtly": len(adonai_courtly)},
        "motifs": {"shuv_bare": len(shuv_bare),
                   "meshuvah": len(inv["motif_roots"]["meshuvah_faithlessness_verses"]),
                   "tsafon": inv["motif_roots"]["tsafon_north_verses"],
                   "sheqer": inv["motif_roots"]["sheqer_falsehood_verses"]},
        "colophon_51_64": True, "aramaic_10_11": True,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
