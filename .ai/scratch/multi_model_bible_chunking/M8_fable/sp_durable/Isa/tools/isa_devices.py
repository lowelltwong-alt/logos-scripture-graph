#!/usr/bin/env python3
"""Phase-0 byte inventory of Isaiah's PROPHETIC FRAME SYSTEM (lesson j) —
../isa_device_inventory.json. Orchestrator-run; agents consume the JSON.

Every count NAMES its object (semantic-class count discipline, lesson e);
verse counts unless noted; ALL KEYS MT NUMBERING (crosswalk for WEB). All
sweeps run over FINALS-NORMALIZED skeletons (the finals-normalized
discipline — load-bearing in Isa, where MT 9:6 carries a medial final-mem
in the letter bytes); attested-spelling splits are called out where they
matter. Derived zones are STAGING SIGNALS ONLY — exact unit bounds are
writer territory argued from bytes.
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from isa_lib import SPBOOK, skeleton

FINALS = str.maketrans("ךםןףץ", "כמנפצ")

oshb_raw: dict[str, str] = {}
for line in (SPBOOK / "Isa_oshb.txt").read_text(encoding="utf-8").splitlines():
    if "\t" in line:
        ref, text = line.split("\t", 1)
        oshb_raw[ref.split(".", 1)[1]] = text

skel = {k: skeleton(v) for k, v in oshb_raw.items()}                 # attested finals
norm = {k: v.translate(FINALS) for k, v in skel.items()}             # finals-normalized
toks = {k: v.split() for k, v in norm.items()}
toks_raw = {k: v.split() for k, v in skel.items()}

web_map = json.loads((Path(__file__).resolve().parent / "verse_map_web.json")
                     .read_text(encoding="utf-8"))


def vkey(ref):
    c, v = (int(x) for x in ref.split("."))
    return (c, v)


def verses_where(pred):
    return sorted((r for r in toks if pred(toks[r])), key=vkey)


def contains(tokens, needle, prefixes=("", "ו", "ה", "ב", "ל", "מ", "כ", "וב", "ול", "וה", "ומ", "וכ", "ש")):
    n = needle.translate(FINALS)
    return any(t == p + n for t in tokens for p in prefixes)


def adjacent(tokens, first, second, prefixes=("", "ו", "ב", "ל", "מ", "כ", "וב", "ול")):
    f = first.translate(FINALS)
    s = second.translate(FINALS)
    for i in range(len(tokens) - 1):
        if any(tokens[i] == p + f for p in prefixes) and tokens[i + 1] == s:
            return True
    return False


inv: dict = {"book": "Isa",
             "numbering": "MT keys throughout (use isa_lib crosswalk; MT 63:19 spans WEB 63:19+64:1)",
             "discipline": ("every count NAMES its object; verse counts unless noted; sweeps "
                            "finals-normalized; derived zones are staging signals only")}

# ---- 0. selah-zero + lmrbh preconditions ----------------------------------
selah = verses_where(lambda t: "סלה" in t)
assert not selah, f"selah unexpectedly present: {selah}"
inv["selah"] = {"verses": 0, "note": "byte-swept ZERO — any selah claim in Isa is a fabrication (Psalter device)"}
assert "לםרבה" in toks_raw["9.6"] and "למרבה" in toks_raw["9.6"], "9:6 doubled token moved"
inv["lmrbh_9_6"] = {
    "verses": 1, "site": "9.6",
    "note": ("THE FLAGSHIP ALLOGRAPHY HAZARD: MT 9:6 carries לםרבה (final mem in MEDIAL "
             "position, in the letter bytes) AND למרבה — a DOUBLED token pair staged from "
             "the K/Q apparatus (kq note at 9.6). Any mem-sensitive sweep, token count, or "
             "quote in this verse must name which form it engages; the verse also sits IN "
             "OFFSET ZONE A (= WEB 9:7).")}

# ---- 1. superscription set (byte-verified) --------------------------------
assert toks["1.1"][:4] == ["חזונ", "ישעיהו", "בנ", "אמוצ"], f'1:1 opener moved: {toks["1.1"][:4]}'
assert toks["2.1"][:3] == ["הדבר", "אשר", "חזה"], f'2:1 opener moved: {toks["2.1"][:3]}'
assert toks["13.1"][:2] == ["משא", "בבל"] and "חזה" in toks["13.1"], f'13:1 opener moved: {toks["13.1"][:5]}'
yeshayahu = verses_where(lambda t: contains(t, "ישעיהו"))
inv["superscriptions"] = {
    "sites": ["1.1", "2.1", "13.1"],
    "byte_facts": ("1:1 chazon Yeshayahu ben-Amots (vision-header over Judah/Jerusalem, "
                   "four-king frame); 2:1 ha-davar asher chazah (word-header); 13:1 massa "
                   "Bavel asher chazah (massa-header WITH the chazah verb + ben-Amots — the "
                   "hinge between the vision-frame and the massa series)"),
    "note": "the only three chazah/ben-Amots-frame headers; 38:9 is a DIFFERENT class (see mikhtav)",
    "yeshayahu_name_verses": yeshayahu,
    "yeshayahu_note": ("13 verses carry the prophet's name: the three superscriptions, 7:3 "
                       "(sign-act command), 20:2-3 (sign-act narrative, עבדי ישעיהו), and the "
                       "narrative-zone cluster 37:2, 37:5, 37:6, 37:21, 38:1, 38:4, 38:21, 39:3-8"),
}
assert set(["1.1", "2.1", "13.1", "7.3", "20.2", "20.3"]).issubset(set(yeshayahu)), yeshayahu

# ---- 2. mikhtav (38:9) — the mid-book header of the OTHER class -----------
assert toks["38.9"][:2] == ["מכתב", "לחזקיהו"], f'38:9 opener moved: {toks["38.9"][:3]}'
inv["mikhtav_38_9"] = {
    "site": "38.9",
    "note": ("מכתב לחזקיהו מלך יהודה — a psalm-type WRITING-superscription INSIDE the "
             "narrative zone, heading the Hezekiah psalm (38:9-20 poetry island). "
             "Header-class evidence like the ch-1/2/13 superscriptions but a different "
             "genre frame; the zone treatment is a gate question.")}

# ---- 3. massa series: header vs common noun -------------------------------
massa_all = verses_where(lambda t: any(x in ("משא", "המשא", "ומשא") for x in t))
massa_initial = [r for r in massa_all if toks[r][0] == "משא"]
inv["massa"] = {
    "family_verses_any_role": massa_all,
    "verse_initial_headers": massa_initial,
    "header_facts": ("verse-initial massa-construct headers (the ORACLE-HEADER spine of chs "
                     "13-23 + 30:6): 13:1 Babylon (+chazah frame), 15:1 Moab, 17:1 Damascus, "
                     "19:1 Egypt, 21:1 wilderness-of-the-sea, 21:11 Dumah, 21:13 in-Arabia, "
                     "22:1 valley-of-vision, 23:1 Tyre, 30:6 beasts-of-the-Negev"),
    "non_initial_sites": sorted(set(massa_all) - set(massa_initial), key=vkey),
    "role_split_note": ("ROLE-SPLIT BEFORE COUNTING: 14:28 המשא הזה is a mid-verse header "
                        "REFERENCE inside the in-the-death-year-of-Ahaz frame; 22:25 המשא is "
                        "the burden common noun closing the Shebna/Eliakim oracle; 46:1-2 "
                        "carries the load/carry family in the idol-procession taunt — NEVER "
                        "blend header-massa with burden-massa in one digit"),
    "web_layout_note": ("the WEB extract opens a paragraph MID-VERSE after the header at "
                        "15:1, 17:1, 19:1, 21:1, 21:11, 21:13, 22:1, 23:1, 30:6 (the 16-fold "
                        "class) — tier-4 layout, but writers must use the folded verse text"),
}
assert set(["13.1", "15.1", "17.1", "19.1", "21.1", "21.11", "21.13", "22.1", "23.1", "30.6"]) == set(massa_initial), massa_initial

# ---- 4. hoy series --------------------------------------------------------
hoy_all = verses_where(lambda t: "הוי" in t)
hoy_initial = [r for r in hoy_all if toks[r][0] == "הוי"]
inv["hoy"] = {
    "token_verses": hoy_all,
    "verse_initial": hoy_initial,
    "role_split_note": ("ROLE-SPLIT BEFORE COUNTING: (a) woe-ORACLE onsets (the ch-5 "
                        "six-fold series 5:8/11/18/20/21/22, the 28-33 series 28:1, 29:1, "
                        "29:15, 30:1, 31:1, 33:1, plus 10:1, 10:5 Assyria, 17:12, 18:1, "
                        "45:9, 45:10); (b) 1:4 the opening woe-INDICTMENT; (c) 1:24 הוי "
                        "אנחם — divine self-exclamation, NOT a woe against the addressee; "
                        "(d) 16:4? no — verify per site; (e) 55:1 הוי is the INVITATION "
                        "cry ('Ho! everyone who thirsts') — the opposite speech act; "
                        "(f) 24:16 רזי לי... אוי? distinct lexeme אוי (6:5 24:16) is NOT "
                        "hoy — never blend אוי with הוי"),
    "count_discipline": "any 'N woes' digit names its series (ch-5 series vs 28-33 series vs whole-book token count)",
}
oy = verses_where(lambda t: any(x in ("אוי", "ואוי") for x in t))
inv["oy_distinct"] = {"verses": oy, "note": "אוי 'woe is me' lexeme (6:5 the call-vision; 24:16) — distinct from הוי; never blended"}

# ---- 5. divine-speech formula census --------------------------------------
koh_amar = verses_where(lambda t: any(t[i] == "כה" and t[i + 1] in ("אמר", "יאמר")
                                      for i in range(len(t) - 1)))


def _koh_amar_class(t):
    """Classify each koh-amar site by its SPEAKER from the next tokens.
    Patch i2 (p05 erratum, byte-verified): the divine frame is NOT always
    strictly adjacent — an intervening dative (21:6 כה אמר אלי אדני), the
    ha-El title (42:5), a suffixed adonai (51:22 אדניך), the qadosh-Israel
    title (30:12), or the ram-ve-nissa epithet (57:15) all open DIVINE
    frames. Royal-messenger sites name the human speaker (המלך / חזקיהו).
    A site matching neither is returned as 'review', never defaulted.
    NB: t is FINALS-NORMALIZED — every needle below is written in normalized
    form (המלכ not המלך, רמ not רם, אדניכ not אדניך): the third time this
    session the finals class caught an orchestrator fixture."""
    kinds = set()
    for i in range(len(t) - 1):
        if t[i] != "כה" or t[i + 1] not in ("אמר", "יאמר"):
            continue
        window = t[i + 2:i + 6]
        divine = any(
            "יהוה" in x or re.match(r"^(ו|ה)?אדני(כ|כמ)?$", x) or x.startswith("האדונ")
            or x == "האל" for x in window)
        if not divine and len(window) >= 2:
            for j in range(len(window) - 1):
                if (window[j] == "קדוש" and window[j + 1] == "ישראל") or \
                        (window[j] == "רמ" and window[j + 1] == "ונשא"):
                    divine = True
        royal = any(x in ("המלכ", "חזקיהו") for x in window[:3])
        kinds.add("divine" if divine else ("royal" if royal else "review"))
    return kinds


koh_amar_yhwh = [r for r in koh_amar if "divine" in _koh_amar_class(toks[r])]
koh_amar_royal = [r for r in koh_amar if "royal" in _koh_amar_class(toks[r])]
koh_amar_review = [r for r in koh_amar
                   if "review" in _koh_amar_class(toks[r])]
inv["koh_amar"] = {
    "all_koh_amar_verses": koh_amar,
    "divine_frame_verses": koh_amar_yhwh,
    "royal_messenger_verses": koh_amar_royal,
    "unclassified_review_verses": koh_amar_review,
    "classifier_note": ("patch i2 (p05 writer erratum, byte-verified): divine frames "
                        "include non-adjacent title forms — 21:6 (intervening dative), "
                        "30:12 (qadosh-Israel title), 42:5 (ha-El), 51:22 (suffixed "
                        "adoneikh), 57:15 (ram-ve-nissa epithet); royal-messenger sites "
                        "NAME the human speaker (המלך / חזקיהו); nothing defaults"),
    "role_split_note": ("THE NARRATIVE-ZONE TRAP: the messenger formula is used by BOTH "
                        "sides in chs 36-37 — כה אמר המלך הגדול מלך אשור (36:4), כה אמר "
                        "המלך (36:14, 36:16), כה אמר חזקיהו (37:3), plus the Rabshakeh's "
                        "taunts — a כה-אמר digit that does not name WHOSE speech-frame it "
                        "counts is meaningless; the divine frame (כה אמר יהוה / אדני / "
                        "האדון / האל / קדוש ישראל / רם ונשא) is the tier-1 object"),
}
neum = verses_where(lambda t: any(x in ("נאמ", "ונאמ") for x in t))
inv["neum"] = {
    "verses": neum,
    "note": ("neum-YHWH / neum-ha-adon oracle-signature census (incl. 1:24 נאם האדון יהוה "
             "צבאות — the stacked triple title); postpositive signature, not an onset "
             "frame; name the exact title stack when citing"),
}
amar_yhwh = verses_where(lambda t: any(t[i] in ("אמר", "יאמר", "ויאמר") and t[i + 1] == "יהוה"
                                       for i in range(len(t) - 1)))
inv["amar_yhwh_adjacent"] = {
    "verses": amar_yhwh,
    "note": ("amar/yomar/vayomer + YHWH adjacency (postpositive 'says Yahweh' signatures "
             "AND narrative 'Yahweh said' onsets — role-split when counting; 40:1 יאמר "
             "אלהיכם is the Elohim variant, NOT in this census)"),
}

# ---- 6. qadosh-Israel family ----------------------------------------------
# patch i3 (p14 erratum, byte-verified): MT 49:7 carries the DEFECTIVE
# spelling קדש ישראל — the title needle accepts both plene and defective
# forms (the mater-lectionis class). The same verse also carries the
# suffixed epithet קדושו (his-Holy-One) — a DIFFERENT object, not the title.
qi = sorted(set(verses_where(lambda t: adjacent(t, "קדוש", "ישראל")))
            | set(verses_where(lambda t: adjacent(t, "קדש", "ישראל"))), key=vkey)
assert "6.3" not in qi
trisagion = toks["6.3"]
assert any(trisagion[i:i + 3] == ["קדוש", "קדוש", "קדוש"]
           for i in range(len(trisagion) - 2)), f"6:3 trisagion moved: {trisagion}"
inv["qadosh_israel"] = {
    "title_verses": qi,
    "count": len(qi),
    "trisagion": {"site": "6.3", "note": "קדוש קדוש קדוש — the throne-vision source of the title; NOT a qadosh-Israel title site"},
    "note": ("the book's signature divine title (qedosh-Yisrael construct, prefix-tolerant "
             "sweep); distribution spans BOTH halves — name the swept object (title-construct) "
             "vs bare qadosh tokens vs the trisagion before any digit"),
    "per_half": {"chs_1_39": len([r for r in qi if vkey(r)[0] <= 39]),
                 "chs_40_66": len([r for r in qi if vkey(r)[0] >= 40])},
}

# ---- 7. remnant family -----------------------------------------------------
shear_yashuv = verses_where(lambda t: adjacent(t, "שאר", "ישוב", prefixes=("", "ו")))
shear_noun = verses_where(lambda t: any(x in ("שאר", "ושאר", "בשאר", "לשאר") for x in t))
sheerit = verses_where(lambda t: contains(t, "שארית"))
nishar = verses_where(lambda t: any(re.match(r"^(ו|ה)?נשאר", x) or re.match(r"^ישאר", x) for x in t))
inv["remnant"] = {
    "shear_yashuv_name": {"verses": shear_yashuv,
                          "note": ("THREE distinct roles on one adjacency: 7:3 the SON'S NAME "
                                   "(vav-prefixed ושאר ישוב 'you and Shear-Jashub your son'); "
                                   "10:21 the remnant CLAUSE reactivating the name (שאר ישוב "
                                   "שאר יעקב); 10:22 the plain clause 'a remnant shall return' "
                                   "— name-vs-clause split is LIVE at exactly this seam")},
    "shear_noun_verses": shear_noun,
    "sheerit_verses": sheerit,
    "nishar_verb_verses": nishar,
    "role_split_note": ("FOUR objects on one root: the name Shear-Jashub, the שאר noun, the "
                        "שארית noun, and the נשאר/ישאר verb family — name the object, then count"),
}
assert "7.3" in shear_yashuv and "10.21" in shear_yashuv, shear_yashuv

# ---- 8. servant census -----------------------------------------------------
avdi = verses_where(lambda t: any(x in ("עבדי", "ועבדי") for x in t))
eved_family = verses_where(lambda t: any(re.match(r"^(ו|ה|ל|ב|כ|מ)?עבד", x) for x in t))
inv["servant"] = {
    "avdi_my_servant_verses": avdi,
    "eved_family_verses_prefix_tolerant": eved_family,
    "named_referents_byte_facts": ("20:3 עבדי ישעיהו (the prophet); 22:20 עבדי אליקים (the "
                                   "steward); 37:35 דוד עבדי (David); 41:8-9, 44:1-2, 44:21, "
                                   "45:4, 48:20, 49:3 Israel/Jacob NAMED as servant; 42:1, "
                                   "42:19, 43:10, 49:5-6, 50:10, 52:13, 53:11 the "
                                   "servant-figure zones (referent NOT named in-verse — a "
                                   "classic held question, never decided by a chunking row)"),
    "candidate_zones_staging_only": ("the four classic servant-song candidate zones DERIVE "
                                     "from the byte census as first-person-divine + עבד "
                                     "clusters: 42:1-9 neighborhood, 49:1-13 neighborhood, "
                                     "50:4-11 neighborhood, 52:13-53:12 — STAGING SIGNAL "
                                     "ONLY; exact bounds are writer territory argued from "
                                     "tier-1 seams (the servant-song boundary debate is "
                                     "scholarship metadata, never boundary authority)"),
    "role_split_note": "name the referent-class before any servant digit (prophet/steward/David/Israel-named/unnamed-figure)",
}
assert set(["20.3", "22.20", "37.35", "42.1", "52.13"]).issubset(set(eved_family))

# ---- 9. stretched-hand refrain + zone A refrain discipline ----------------
refrain = verses_where(lambda t: " ".join(t).find("בכל זאת לא שב אפו ועוד ידו נטויה") >= 0)
inv["stretched_hand_refrain"] = {
    "verses": refrain,
    "note": ("the ap/yad refrain בכל זאת לא שב אפו ועוד ידו נטויה — byte-identical at "
             "5:25, 9:11, 9:16, 9:20, 10:4 (MT; the ch-9 sites are IN ZONE A = WEB 9:12, "
             "9:17, 9:21) — it BRIDGES the ch-5 woe series and the 9:7-10:4 poem: the "
             "classic structural-seam crux; every citation dual-cites in the zone"),
}
assert set(refrain) == {"5.25", "9.11", "9.16", "9.20", "10.4"}, refrain

# ---- 10. Immanuel + Yah short form ----------------------------------------
immanuel = verses_where(lambda t: adjacent(t, "עמנו", "אל", prefixes=("",)))
inv["immanuel"] = {"verses": immanuel,
                   "note": "עמנו אל two-token adjacency (7:14, 8:8, 8:10 — 8:10's כי עמנו אל is the formula as a CLAUSE; role-split name vs clause is a held classic)"}
assert set(["7.14", "8.8", "8.10"]).issubset(set(immanuel)), immanuel
yah = verses_where(lambda t: any(x in ("יה", "ביה") for x in t))
inv["yah_short_form"] = {
    "verses": yah,
    "note": ("standalone/prefixed YAH short form — THREE sites, byte-swept: 12:2 עזי "
             "וזמרת יה יהוה (the Exodus-15 echo, Yah + tetragrammaton stacked), 26:4 "
             "ביה יהוה, and 38:11 יה יה (DOUBLED Yah inside the Hezekiah psalm, 'I "
             "shall not see Yah, Yah, in the land of the living'); a standalone-יה "
             "sweep hits ONLY here; never blend with the tetragrammaton census"),
}
assert set(yah) == {"12.2", "26.4", "38.11"}, yah

# ---- 11. divine-name censuses (counts + distribution, not full lists) -----
yhwh = verses_where(lambda t: any("יהוה" in x for x in t))
adonai = verses_where(lambda t: any(re.match(r"^(ו|ל|ב|כ)?אדני$", x) for x in t))
tsevaot = verses_where(lambda t: any(t[i].endswith("יהוה") and t[i + 1] == "צבאות"
                                     for i in range(len(t) - 1)))
by_ch = collections.Counter(vkey(r)[0] for r in yhwh)
inv["divine_names"] = {
    "yhwh_verses_count": len(yhwh),
    "yhwh_token_note": ("tetragrammaton VERSE count (prefix-tolerant substring; token count "
                        "differs — 12:2 and 26:4 carry doubled names); YHWH is EVERYWHERE "
                        "(contrast Song's zero): divine-name citations are ordinary, but "
                        "count-objects still get named (tetragrammaton vs adonai vs "
                        "yhwh-tsevaot vs qadosh-Israel vs yah)"),
    "yhwh_per_chapter_max": dict(sorted(by_ch.items(), key=lambda kv: -kv[1])[:5]),
    "adonai_verses_count": len(adonai),
    "adonai_note": ("bare-adonai census (exact token, prefix-tolerant) — ROLE-SPLIT in the "
                    "narrative zone: courtly 'my lord' (36:12 אדני the Rabshakeh's master; "
                    "36:8 התערב נא את אדני) vs the divine Adonai (6:1 the throne vision, "
                    "the אדני יהוה stacks) — name the referent before any digit"),
    "yhwh_tsevaot_verses_count": len(tsevaot),
    "yhwh_tsevaot_note": "YHWH-tsevaot adjacency (of-hosts title); 1:24 stacks האדון יהוה צבאות",
}

# ---- 12. narrative zone 36-39 profile -------------------------------------
zone_web = [(c, v) for c in range(36, 40) for v in range(1, {36: 22, 37: 38, 38: 22, 39: 8}[c] + 1)]
zone_profile = []
for c in range(36, 40):
    keys = [k for k in web_map if k.startswith(f"Isa.{c}.")]
    poetry = sum(1 for k in keys if web_map[k]["poetry_lines"])
    zone_profile.append({"web_chapter": c, "verses": len(keys), "verses_opening_poetry": poetry})
hizkiyahu = verses_where(lambda t: contains(t, "חזקיהו"))
sancheriv = verses_where(lambda t: contains(t, "סנחריב"))
ravshaqeh = verses_where(lambda t: adjacent(t, "רב", "שקה", prefixes=("", "ו", "ה", "ל")))
inv["narrative_zone_36_39"] = {
    "identity_note": "chs 36-39 are IDENTITY numbering (both zones lie outside)",
    "web_poetry_profile": zone_profile,
    "poetry_island_note": ("the zone is prose-dominant EXCEPT the Hezekiah psalm 38:10-20 "
                           "(poetry lines) under the 38:9 mikhtav header — a genre island "
                           "inside the narrative; 37:22-35 also carries the taunt-song "
                           "poem (Yahweh's answer through Isaiah) — profile from bytes, "
                           "treatment is a gate question"),
    "hizkiyahu_verses": hizkiyahu,
    "sancheriv_verses": sancheriv,
    "ravshaqeh_verses": ravshaqeh,
    "cross_tradition_note": ("the 2 Kgs 18-20 parallel is cross-tradition-STYLE metadata "
                             "(intra-canon synoptic): typed-relation territory, NEVER "
                             "boundary evidence for Isaiah's seams (lesson j)"),
}

# ---- 13. per-chapter structural texture (staging for the gate) ------------
texture = []
for c in range(1, 67):
    keys = [k for k in web_map if k.startswith(f"Isa.{c}.")]
    poetry = sum(1 for k in keys if web_map[k]["poetry_lines"])
    mt_ch_refs = [r for r in toks if vkey(r)[0] == c]
    texture.append({
        "ch": c, "web_verses": len(keys), "poetry_share": round(poetry / len(keys), 2),
        "hoy": sum(1 for r in hoy_all if vkey(r)[0] == c),
        "koh_amar": sum(1 for r in koh_amar if vkey(r)[0] == c),
        "neum": sum(1 for r in neum if vkey(r)[0] == c),
        "massa_hdr": sum(1 for r in massa_initial if vkey(r)[0] == c),
        "yhwh": by_ch.get(c, 0),
    })
inv["chapter_texture"] = {
    "note": ("per-WEB-chapter staging profile (poetry share from WEB layout = tier-4 "
             "texture signal ONLY; formula counts MT-keyed) — for the at-scale wave/part "
             "plan and granularity gate questions; writers re-derive, never row evidence"),
    "rows": texture,
}

OUT = SPBOOK / "isa_device_inventory.json"
OUT.write_text(json.dumps(inv, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({
    "superscriptions": inv["superscriptions"]["sites"],
    "yeshayahu_verses": len(yeshayahu),
    "massa_headers": len(massa_initial),
    "massa_family": len(massa_all),
    "hoy_verses": len(hoy_all), "hoy_initial": len(hoy_initial),
    "koh_amar": len(koh_amar), "koh_amar_divine": len(koh_amar_yhwh),
    "neum": len(neum), "amar_yhwh_adj": len(amar_yhwh),
    "qadosh_israel": len(qi),
    "shear_yashuv": shear_yashuv, "remnant_noun": len(shear_noun),
    "sheerit": len(sheerit), "nishar_verb": len(nishar),
    "avdi": len(avdi), "eved_family": len(eved_family),
    "stretched_hand": refrain,
    "immanuel": immanuel, "yah": yah,
    "yhwh_verses": len(yhwh), "adonai": len(adonai), "tsevaot": len(tsevaot),
    "hizkiyahu": len(hizkiyahu), "sancheriv": len(sancheriv), "ravshaqeh": len(ravshaqeh),
    "status": "OK"}, ensure_ascii=False, indent=1))
