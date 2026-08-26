#!/usr/bin/env python3
"""Phase-0 Tier-0: build ../song_device_inventory.json from bytes (orchestrator-run;
agents consume the JSON). Every count NAMES ITS OBJECT (semantic-class count
discipline): spelling vs term vs formula vs construction, verse counts vs
token counts, always labeled.

NON-IDENTITY book (MT 7:1 = WEB 6:13; MT 7:2-14 = WEB 7:1-13): every ref in
this inventory is MT-KEYED; WEB back-references are provided where the
offset zone is touched (MT ch 7).

Voice spine per LESSONS-FOR-Song lesson j: the inventories below carry the
text's own address/gender signals (dodi, rayati, kallah, achoti, the
daughters-addresses, the adjuration + mutual-belonging refrains, wasf
body-part density) — NOT the WEB [SPEAKER] headings (tier-4, cataloged
separately in ../speaker_headings_web.json for audit only).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from song_lib import BOOK, MT_LAST_VERSE, SPBOOK, mt_to_web, skeleton

OUT = SPBOOK / "song_device_inventory.json"

oshb: dict[str, str] = {}
for line in (SPBOOK / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").splitlines():
    if "\t" in line:
        ref, text = line.split("\t", 1)
        oshb[ref.split(".", 1)[1]] = text          # "C.V" -> pointed text

skel = {k: skeleton(v) for k, v in oshb.items()}
toks = {k: v.split() for k, v in skel.items()}


def mtref(k: str) -> str:
    return f"{BOOK}.{k.replace('.', ':')}"


def webback(k: str) -> str:
    """MT key -> 'MT c:v' + WEB back-ref where the offset zone is touched."""
    c, v = (int(x) for x in k.split("."))
    w = mt_to_web(c, v)
    if (c, v) != w:
        return f"MT {c}:{v} (= WEB {w[0]}:{w[1]})"
    return f"{c}:{v}"


def sweep_token(pred) -> dict[str, list[str]]:
    """MT verses whose token list satisfies pred(token) — returns {key: [hits]}."""
    out = {}
    for k, tt in toks.items():
        hits = [t for t in tt if pred(t)]
        if hits:
            out[k] = hits
    return out


def keys_sorted(d) -> list[str]:
    return sorted(d, key=lambda k: (int(k.split(".")[0]), int(k.split(".")[1])))


def vlist(d) -> list[str]:
    return [webback(k) for k in keys_sorted(d)]


def exact(*forms):
    fs = set(forms)
    return lambda t: t in fs


# ---- frame / superscription ----
assert "שיר השירים אשר לשלמה" in skel["1.1"], "1:1 superscription bytes moved"
shelomo = sweep_token(lambda t: "שלמה" in t)
melek_hamelek = sweep_token(exact("המלך", "מלך", "למלך", "והמלך", "שהמלך", "במלך"))
malkot = sweep_token(lambda t: t in ("מלכות", "המלכות"))

# ---- address / voice vocabulary (attested-form discipline) ----
dodi = sweep_token(exact("דודי", "ודודי", "לדודי"))                    # her beloved (m.)
dod_family = sweep_token(lambda t: re.fullmatch(r"[ולמב]?דוד(י|ך|ים|ה)?", t) is not None)
dadeikha_defective = sweep_token(exact("דדיך", "דדי"))                  # dodekha 'your loves', DEFECTIVE spelling — escapes dod sweeps
dudaim = sweep_token(lambda t: "דודאים" in t)                           # mandrakes 7:14 — dod-adjacent homograph
rayati = sweep_token(lambda t: re.fullmatch(r"רעיתי", t) is not None)
rea_shepherd = sweep_token(exact("הרעה", "רעה", "לרעות", "ירעה", "הרעים"))  # graze/pasture family (resh-ayin)
kallah = sweep_token(exact("כלה", "וכלה"))
achoti = sweep_token(lambda t: t in ("אחתי", "אחות", "ואחות"))
yonah = sweep_token(lambda t: re.fullmatch(r"[וכל]?יונ(ה|תי|ים)", t) is not None)
ahavah_noun = sweep_token(lambda t: re.fullmatch(r"[והבכ]{0,2}אהבה", t) is not None)  # noun forms ONLY — she-ahavah (relative + qal verb) is a DIFFERENT object, censused below
sheahavah_nafshi = {k: v for k, v in sweep_token(lambda t: t == "שאהבה").items()
                    if "נפשי" in toks[k]}
raayah_yafah = sweep_token(exact("יפה", "היפה", "יפתי", "הנך", "יפית"))

# ---- daughters addresses ----
banot_yerushalaim = {k: t for k, t in toks.items()
                     if any(a == "בנות" and b.endswith("ירושלם")
                            for a, b in zip(t, t[1:]))}
banot_tsiyon = {k: t for k, t in toks.items()
                if any(a == "בנות" and b == "ציון" for a, b in zip(t, t[1:]))}
banot_other = {k: [x for x in t if x in ("בנות", "הבנות", "כבנות", "מבנות")]
               for k, t in toks.items()
               if any(x in ("בנות", "הבנות", "כבנות", "מבנות") for x in t)}

# ---- the adjuration refrain (hishba'ti sites + formula variation) ----
adjuration = sweep_token(exact("השבעתי"))
adjuration_detail = {}
for k in keys_sorted(adjuration):
    t = " ".join(toks[k])
    adjuration_detail[webback(k)] = {
        "has_banot_yerushalaim": "בנות ירושלם" in t,
        "has_gazelles_does": ("בצבאות" in toks[k]) and any("אילות" in x for x in toks[k]),
        "opens_im_tairu_im_teoreru": "אם תעירו ואם תעוררו" in t,
        "mah_variant": ("מה תעירו" in t) or ("מה תגידו" in t),
        "im_timtseu_variant": "אם תמצאו" in t,
    }

# ---- mutual-belonging refrain ----
mutual = {}
for k, t in skel.items():
    if "דודי לי ואני לו" in t:
        mutual[k] = "dodi li va-ani lo (his-mine order)"
    elif "אני לדודי ודודי לי" in t:
        mutual[k] = "ani le-dodi ve-dodi li (mine-his order)"
    elif "אני לדודי ועלי תשוקתו" in t:
        mutual[k] = "ani le-dodi ve-alai teshuqato (desire variant)"

# ---- gazelle / stag / foxes refrains ----
tsvi = sweep_token(lambda t: re.fullmatch(r"[ולכב]?צבי(ה|ם)?", t) is not None or t == "בצבאות")
foxes = sweep_token(lambda t: "שעלים" in t or "שועלים" in t)
qol_dodi = {k: True for k, t in skel.items() if "קול דודי" in t}
ad_sheyafuach = {k: True for k, t in skel.items() if "עד שיפוח היום" in t}
mi_zot = {k: True for k, t in skel.items() if "מי זאת" in t}
semadar = sweep_token(lambda t: "סמדר" in t)
henetsu_rimmonim = {k: True for k, t in skel.items()
                    if re.search(r"הנצו הרמ[ו]?נים", t)}

# ---- wasf (descriptive-poem) signal: suffixed body-part density ----
BODY = ("עיני", "שער", "שני", "שפת", "שפתות", "צואר", "שדי", "לחי", "ראש",
        "אף", "אפ", "בטנ", "ירכ", "שרר", "פעמי", "ידי", "מעי", "חכ", "קומת",
        "רקת", "קוצות", "עפעפ", "טבור", "גרון", "זרוע", "לב", "רגל")


def body_hits(t: str) -> list[str]:
    hits = []
    for tok in t.split():
        core = tok
        if len(core) >= 3 and (core.endswith("ך") or core.endswith("ו") or core.endswith("יו")):
            stem = core.rstrip("ךו")
            if any(stem.startswith(b) or (len(core) > 1 and core[1:].startswith(b))
                   for b in BODY):
                hits.append(tok)
    return hits


wasf_tokens = {k: body_hits(t) for k, t in skel.items() if body_hits(t)}
# maximal runs of >=3 consecutive body-part-bearing verses = wasf zones
runs = []
cur = []
for c in sorted(MT_LAST_VERSE):
    for v in range(1, MT_LAST_VERSE[c] + 1):
        k = f"{c}.{v}"
        if k in wasf_tokens:
            if cur and (cur[-1][0] == c and v == cur[-1][1] + 1):
                cur.append((c, v))
            else:
                if len(cur) >= 3:
                    runs.append(cur)
                cur = [(c, v)]
        else:
            if len(cur) >= 3:
                runs.append(cur)
            cur = []
if len(cur) >= 3:
    runs.append(cur)
wasf_zones = [f"MT {r[0][0]}:{r[0][1]}-{r[-1][0]}:{r[-1][1]}"
              + ("" if r[0][0] != 7 else f" (= WEB {mt_to_web(r[0][0], r[0][1])[0]}:{mt_to_web(r[0][0], r[0][1])[1]}-{mt_to_web(r[-1][0], r[-1][1])[0]}:{mt_to_web(r[-1][0], r[-1][1])[1]})")
              for r in runs]

# ---- divine names (byte facts) ----
yhwh = sweep_token(lambda t: t == "יהוה")
elohim = sweep_token(lambda t: "אלהים" in t)
# WLC 8:6 writes ONE word (shalhevetyah); OSHB divides it into שלהבת + יה
# for exegesis (its note says so) and tags יה as lemma 3050 Yah (HNp) — so
# the STAGED EXTRACT carries an adjacent token pair, and a naive standalone
# יה sweep hits here.
shalhevet_yah = {k: True for k, t in toks.items()
                 if any(a.endswith("שלהבת") and b == "יה" for a, b in zip(t, t[1:]))}
yah_standalone = sweep_token(lambda t: t == "יה")

# ---- shin-bet-ayin homograph census ----
shin_bet_ayin = sweep_token(lambda t: re.search(r"שבע", t) is not None)

# ---- misc lexicon hazards ----
kerem_family = sweep_token(lambda t: (re.fullmatch(r"[ובלמה]{0,2}כרמ(י|ים|נו)", t) is not None
                                      or re.fullmatch(r"[ובלמה]{0,2}כרם", t) is not None)
                           and "כרמל" not in t)  # final-mem bare form AND suffixed medial forms — allography-split
karmel = sweep_token(lambda t: "כרמל" in t)
ayin_gedi = {k: True for k, t in skel.items() if "עין גדי" in t}
pardes = sweep_token(lambda t: "פרדס" in t)
yayin = sweep_token(lambda t: re.fullmatch(r"[ומכבהל]{0,2}יין", t) is not None or t == "ייני")  # bare/prefixed final-nun forms + suffixed medial yeini (5:1)
mor = sweep_token(lambda t: re.fullmatch(r"[וה]?מ[ו]?ר(י|ו)?", t) is not None)

# ---- first-person + gender texture (staging signal) ----
ani = sweep_token(exact("אני", "ואני"))
nafshi = sweep_token(lambda t: "נפשי" in t)

# ---- catchword adjacency per chapter (skeleton shared-content-token pairs;
#      staging signal for the granularity gate — writers re-derive) ----
STOP = {"לא", "אל", "את", "על", "כי", "מן", "אם", "גם", "כל", "אשר", "הוא",
        "היא", "יש", "אין", "או", "פן", "בל", "לו", "לך", "בו", "בה", "מה",
        "זה", "זאת", "עם", "עד", "אך", "רק", "כן", "כה", "אף", "לי", "מי"}
adjacency = {}
for c in sorted(MT_LAST_VERSE):
    pairs = 0
    shared = 0
    for v in range(1, MT_LAST_VERSE[c]):
        a = {t for t in toks.get(f"{c}.{v}", []) if len(t) >= 2 and t not in STOP}
        b = {t for t in toks.get(f"{c}.{v+1}", []) if len(t) >= 2 and t not in STOP}
        pairs += 1
        if a & b:
            shared += 1
    adjacency[str(c)] = f"{shared}/{pairs}"


def block(d, count_object, note=""):
    out = {"count_object": count_object,
           "verse_count": len(d), "verses": vlist(d)}
    if note:
        out["note"] = note
    return out


inv = {
    "book": BOOK,
    "numbering_note": "MT-keyed except where marked; NON-IDENTITY book — MT 7:1 = WEB 6:13, MT 7:2-14 = WEB 7:1-13; use song_lib crosswalk",
    "frame": {
        "superscription": "MT 1:1 shir ha-shirim asher li-shlomo — the book's only header (byte-asserted)",
        "shelomo_sites": block(shelomo, "verses bearing a shelomo-containing token (incl. li-shlomo 1:1, she-li-shlomo 3:7)"),
        "melek_sites": block(melek_hamelek, "verses bearing a melek-lexeme token (המלך/מלך forms; the noun 'king')",
                             "distinguish from melakhot 'queens' (below) before counting any king-digit"),
        "melakhot_queens": block(malkot, "verses bearing melakhot 'queens' tokens (6:8, 6:9)"),
    },
    "voice_address": {
        "dodi_exact": block(dodi, "verses bearing דודי/ודודי/לדודי exact tokens (her word for the man)"),
        "dod_family": block(dod_family, "verses bearing dod-family tokens (letter-prefix tolerant)",
                            "family sweep ≠ dodi count ≠ token count: name the object before any digit"),
        "dadeikha_defective": block(dadeikha_defective, "verses bearing the DEFECTIVE dodekha spelling דדיך/דדי ('your loves', 1:2, 1:4, 4:10, 7:13)",
                                    "escapes every dod-sweep (no vav) — the Song digit-blending hazard's sharpest arm"),
        "dudaim_mandrakes": block(dudaim, "verses bearing duda'im 'mandrakes' (MT 7:14 = WEB 7:13)",
                                  "dod-adjacent homograph; never blend with beloved-counts"),
        "rayati": block(rayati, "verses bearing רעיתי 'my love [f.]' (his word for the woman)"),
        "rea_shepherd_family": block(rea_shepherd, "verses bearing graze/pasture ro'eh-family tokens",
                                     "resh-ayin family: ra'yati (address) / ro'eh (graze) / ra' (evil, absent) — name the object"),
        "kallah": block(kallah, "verses bearing kallah 'bride' tokens"),
        "achoti": block(achoti, "verses bearing achoti/achot 'my sister/sister' tokens",
                        "8:8 achot is the brothers' little sister — NOT the bride epithet; role-split before counting"),
        "yonah_family": block(yonah, "verses bearing dove-family tokens (yonati/yonim/ka-yonim)"),
        "ahavah_noun": block(ahavah_noun, "verses bearing the noun ahavah (letter-prefix tolerant)"),
        "sheahavah_nafshi": block(sheahavah_nafshi, "verses bearing the she-ahavah nafshi relative formula ('whom my soul loves')"),
        "ani": block(ani, "verses bearing אני/ואני exact tokens (first-person pronoun)"),
        "nafshi": block(nafshi, "verses bearing nafshi-containing tokens"),
    },
    "daughters_addresses": {
        "banot_yerushalaim": block(banot_yerushalaim, "verses bearing the adjacent pair בנות ירושלם"),
        "banot_tsiyon": block(banot_tsiyon, "verses bearing the adjacent pair בנות ציון (3:11 only)"),
        "banot_any": block(banot_other, "verses bearing any banot token (incl. the two address formulas above)"),
    },
    "adjuration_refrain": {
        "count_object": "verses bearing hishba'ti 'I adjure' (hiphil, shin) — the adjuration sites",
        "verse_count": len(adjuration),
        "verses": vlist(adjuration),
        "formula_variation_byte_derived": adjuration_detail,
        "note": ("2:7 and 3:5 carry the FULL form (daughters + gazelles/does + im-ta'iru); "
                 "5:8 is the im-timtse'u / mah-tagidu variant WITHOUT the gazelles; "
                 "8:4 uses mah-ta'iru WITHOUT the gazelles — three attested shapes, never conflated"),
    },
    "mutual_belonging_refrain": {
        "count_object": "verses bearing one of the three attested mutual-belonging formulas (byte-matched skeleton phrases)",
        "verse_count": len(mutual),
        "sites": {webback(k): mutual[k] for k in keys_sorted(mutual)},
        "note": "the three shapes DIFFER (order flip 2:16 vs 6:3; the 7:11 desire-variant sits in the OFFSET ZONE = WEB 7:10) — quote the attested shape, never a harmonized one",
    },
    "gazelle_stag_foxes": {
        "tsvi_family": block(tsvi, "verses bearing gazelle-family tokens (tsvi/tsviyah/bi-tseva'ot)",
                             "bi-tseva'ot in the adjurations = 'by the gazelles' — homograph with tseva'ot 'hosts'; the divine-name reading is NOT in these bytes"),
        "foxes": block(foxes, "verses bearing fox-tokens (2:15: shu'alim twice — 'foxes, little foxes')"),
        "qol_dodi": block(qol_dodi, "verses opening/bearing the qol dodi phrase (2:8, 5:2)"),
        "ad_sheyafuach": block(ad_sheyafuach, "verses bearing the ad-she-yafuach ha-yom refrain (2:17, 4:6)"),
        "mi_zot": block(mi_zot, "verses bearing the mi-zot ascending-question formula (3:6, 6:10, 8:5)"),
        "semadar": block(semadar, "verses bearing semadar 'vine blossom' (2:13, 2:15, 7:13)"),
        "henetsu_rimmonim": block(henetsu_rimmonim, "verses bearing the henetsu ha-rimmonim clause (6:11, 7:13 — both spellings)"),
    },
    "wasf_signal": {
        "count_object": "suffixed body-part tokens per MT verse (2fs -kh / 3ms -o classes; heuristic stem list)",
        "verses_with_tokens": {webback(k): v for k, v in ((k, wasf_tokens[k]) for k in keys_sorted(wasf_tokens))},
        "derived_zones_runs_of_3plus": wasf_zones,
        "note": ("STAGING SIGNAL ONLY (writers re-derive; heuristic, never row evidence): "
                 "maximal runs of >=3 consecutive body-part-bearing verses. The derived zones "
                 "are the byte-grounded wasf candidates; exact wasf BOUNDS are writer territory "
                 "argued from bytes (openers, closures, addressee shifts)."),
    },
    "divine_names": {
        "yhwh_tetragrammaton": {"count_object": "standalone YHWH tokens", "verse_count": len(yhwh),
                                "verses": vlist(yhwh),
                                "note": "ZERO (byte-swept). ANY tetragrammaton citation in Song is a fabrication."},
        "elohim": {"count_object": "elohim-containing tokens", "verse_count": len(elohim),
                   "verses": vlist(elohim),
                   "note": "ZERO (byte-swept). Song carries no elohim/YHWH at all — cite the absence WITH this sweep; the sole Yah-form surface is the 8:6 crux below."},
        "shalhevet_yah_8_6": {"count_object": "the adjacent staged-token pair shalhevet + yah (MT 8:6)",
                              "verse_count": len(shalhevet_yah),
                              "verses": vlist(shalhevet_yah),
                              "standalone_yah_tokens_in_staged_extract": vlist(yah_standalone),
                              "note": ("The underlying WLC text writes ONE word (OSHB's own 8:6 note: "
                                       "'A single word in the text has been divided for exegesis'); OSHB "
                                       "divides it into שלהבת + יה and TAGS the second element as lemma "
                                       "3050 Yah (HNp) — single-witness TAGGING metadata, not text bytes. "
                                       "So the staged extract carries a standalone יה token at MT 8:6 that "
                                       "a naive divine-name sweep hits. The construal (intensive suffix "
                                       "'mighty flame' vs divine element 'flame of Yah') is a CLASSIC "
                                       "CRUX: hold, never decide; never cite as a divine-name occurrence "
                                       "without the crux AND the one-word/divided-token disclosure.")},
    },
    "shin_bet_ayin_census": {
        "count_object": "verses bearing ANY token containing the שבע letter sequence (blind contiguous sweep — for the hazard catalog)",
        "verse_count": len(shin_bet_ayin),
        "verses_with_tokens": {webback(k): v for k, v in ((k, shin_bet_ayin[k]) for k in keys_sorted(shin_bet_ayin))},
        "note": ("EVERY Song hit is the OATH root: hishba'ti at 2:7/3:5/5:8/8:4 PLUS the daughters' "
                 "quoted-back shehishba'tanu at 5:9 (which the adjuration-site count rightly EXCLUDES — "
                 "it reports the oath, it does not swear one) — no 'seven' and no 'sated' tokens exist "
                 "in Song: a blended שבע digit is meaningless here; name the root AND the speech role "
                 "before counting"),
    },
    "lexicon_hazards": {
        "kerem_family": block(kerem_family, "verses bearing vineyard kerem-family tokens (karmel EXCLUDED)"),
        "karmel": block(karmel, "verses bearing Carmel (MT 7:6 = WEB 7:5 only)",
                        "כרם is CONTAINED in כרמל — word-bind or byte-check every vineyard sweep"),
        "ayin_gedi": block(ayin_gedi, "verses bearing the En-Gedi pair (1:14)",
                           "עין = eye AND spring: the En-Gedi ayin is not an eye-token; role-split eye-counts"),
        "pardes": block(pardes, "verses bearing the Persian loan pardes (4:13)"),
        "yayin_family": block(yayin, "verses bearing wine yayin-family tokens (incl. suffixed yeini 5:1 — final/medial nun allography)"),
        "mor_family": block(mor, "verses bearing myrrh mor-family tokens BOTH spellings (plene מור; DEFECTIVE מר at 1:13, 4:14)",
                            "the defective spelling collides with mar 'bitter' (absent in Song) and escapes plene sweeps"),
    },
    "texture_staging_signals": {
        "catchword_adjacency_per_chapter": adjacency,
        "note": ("skeleton-tier shared-content-token adjacent-verse pairs per MT chapter — "
                 "staging signal for the granularity gate; writers re-derive; heuristic, never row evidence"),
    },
}

OUT.write_text(json.dumps(inv, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({
    "shelomo": len(shelomo), "melek": len(melek_hamelek),
    "dodi": len(dodi), "dod_family": len(dod_family),
    "dadeikha_defective": len(dadeikha_defective),
    "rayati": len(rayati), "kallah": len(kallah), "achoti": len(achoti),
    "ahavah_noun": len(ahavah_noun), "sheahavah_nafshi": len(sheahavah_nafshi),
    "banot_yerushalaim": len(banot_yerushalaim), "banot_tsiyon": len(banot_tsiyon),
    "adjuration": vlist(adjuration),
    "mutual_belonging": {webback(k): mutual[k] for k in keys_sorted(mutual)},
    "tsvi_family": len(tsvi), "foxes": vlist(foxes),
    "mi_zot": vlist(mi_zot), "ad_sheyafuach": vlist(ad_sheyafuach),
    "wasf_zones": wasf_zones,
    "yhwh": len(yhwh), "elohim": len(elohim),
    "shalhevet_yah": vlist(shalhevet_yah), "yah_standalone": vlist(yah_standalone),
    "shin_bet_ayin_verses": vlist(shin_bet_ayin),
    "adjacency": adjacency,
    "out": OUT.name,
}, ensure_ascii=False, indent=1))
