#!/usr/bin/env python3
"""Rebuilds ../eccl_device_inventory.json from bytes (orchestrator-run at
staging; agents consume the JSON). Every count NAMES its object. Eccl is a
NON-IDENTITY book (MT 4:17 = WEB 5:1; MT 5:1-19 = WEB 5:2-20): every ref in
this inventory is MT-KEYED unless the section says otherwise; web_ref
back-references are provided where the offset zone is touched.

Sections:
  frame_seams        — the tier-1 frame spine: divrei header, qohelet sites
                       (BOTH attested spellings), amar-qohelet formula sites,
                       first-person discourse markers, king self-IDs
  hevel_refrain      — attested hevel token forms, verse/token counts,
                       havel-havalim + hakol-hevel phrase sites, inclusio
  reut_ruach         — chasing-wind refrain phrase sites (both forms)
  under_the_sun      — tachat-hashemesh phrase sites + bare shemesh sites
  time_catalogue     — 3:1-8 et tokens per verse + et outside the poem
  tov_comparatives   — tov-min adjacency sites, tov openers, WEB better-than
  carpe_diem         — eat+drink co-occurrence sites (enjoyment refrain)
  allegory_zone      — 11:7-12:8: ad-asher-lo anaphora, remember/rejoice
                       imperact sites, youth tokens
  elohim_yhwh        — elohim family counts; YHWH ZERO (probative absence)
  sentence_zone_texture — per-chapter catchword adjacency + WEB ', but ' +
                       better-than density (granularity-gate staging signals)
  parashah_distribution / kq_distribution / paseq — from ../pmarks_Eccl.json
  continuation_folds — WEB verses folded across paragraph marks (LIVE here)
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eccl_lib import (BOOK, LAST_VERSE, MT_LAST_VERSE, SPBOOK, TOOLS,
                      load_pmarks, mt_to_web, skeleton)

STOP = {"לא", "אל", "את", "על", "כי", "מן", "אם", "גם", "כל", "אשר", "הוא",
        "היא", "יש", "אין", "או", "פן", "בל", "לו", "לך", "בו", "בה", "מה",
        "זה", "זאת", "עם", "עד", "אך", "רק", "כן", "כה", "אף"}


def mt_sort(refs):
    return sorted(refs, key=lambda x: (int(x.split(".")[1]), int(x.split(".")[2])))


def with_web(ref):
    _, c, v = ref.split(".")
    w = mt_to_web(int(c), int(v))
    wr = f"{BOOK}.{w[0]}.{w[1]}"
    return {"mt": ref, "web": wr} if wr != ref else {"mt": ref}


def main() -> int:
    oshb: dict[str, str] = {}
    for line in (SPBOOK / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            ref, text = line.split("\t", 1)
            oshb[ref] = text
    web = json.loads((TOOLS / "verse_map_web.json").read_text(encoding="utf-8"))
    sk = {ref: skeleton(t) for ref, t in oshb.items()}
    toks = {ref: s.split() for ref, s in sk.items()}

    # --- frame seams ---
    divrei_initial = [r for r, t in toks.items() if t and t[0] == "דברי"]
    qoh_forms = collections.defaultdict(list)     # attested token form -> refs
    for r, t in toks.items():
        for tok in t:
            if "קהלת" in tok or "קוהלת" in tok:
                qoh_forms[tok].append(r)
    qoh_refs = mt_sort({r for refs in qoh_forms.values() for r in refs})
    amar_qoh = [r for r, s in sk.items()
                if re.search(r"אמרה? ה?קו?הלת", s)]
    ani = [r for r, t in toks.items() if "אני" in t or "ואני" in t]
    shavti = [r for r, t in toks.items()
              if any(x in ("שבתי", "ושבתי") for x in t)]
    raiti = [r for r, t in toks.items()
             if any(x in ("ראיתי", "וראיתי") for x in t)]
    amarti = [r for r, t in toks.items() if any(x in ("אמרתי", "ואמרתי") for x in t)]
    dibbarti = [r for r, t in toks.items() if any(x in ("דברתי", "ודברתי") for x in t)]
    melekh = [r for r, t in toks.items()
              if any(x in ("מלך", "המלך", "למלך", "ומלך") for x in t)]
    frame_seams = {
        "note": "tier-1 frame spine; quotes are skeleton-tier here — writers re-collate pointed bytes via collate.py",
        "divrei_verse_initial": {"refs": divrei_initial,
                                 "count_object": "verses whose first skeleton token is דברי",
                                 "count": len(divrei_initial)},
        "qohelet_sites": {
            "refs": qoh_refs,
            "attested_forms": {f: mt_sort(rs) for f, rs in sorted(qoh_forms.items())},
            "count_object": "verses containing any token carrying the qohelet name — BOTH attested spellings (קהלת defective; קוהלת plene at the definite 12:8 form); sweep per attested spelling",
            "count": len(qoh_refs)},
        "amar_qohelet_formula": {
            "refs": mt_sort(amar_qoh),
            "count_object": "verses whose skeleton matches the said-qohelet formula (אמר/אמרה + optional article, either spelling) — the third-person frame intrusions",
            "count": len(amar_qoh)},
        "first_person_ani": {
            "refs": mt_sort(ani),
            "count_object": "verses containing the word-bound token אני or ואני (the monologue's pleonastic first person)",
            "count": len(ani),
            "by_chapter": dict(sorted(collections.Counter(int(r.split(".")[1]) for r in ani).items()))},
        "shavti_turns": {"refs": mt_sort(shavti),
                         "count_object": "verses containing token שבתי or ושבתי (the I-turned discourse pivot)",
                         "count": len(shavti)},
        "raiti_observations": {"refs": mt_sort(raiti),
                               "count_object": "verses containing token ראיתי or וראיתי (the I-saw observation frame)",
                               "count": len(raiti)},
        "amarti_speech": {"refs": mt_sort(amarti),
                          "count_object": "verses containing token אמרתי or ואמרתי (I-said self-address frame)",
                          "count": len(amarti)},
        "dibbarti_speech": {"refs": mt_sort(dibbarti),
                            "count_object": "verses containing token דברתי or ודברתי",
                            "count": len(dibbarti)},
        "melekh_sites": {"refs": mt_sort(melekh),
                         "count_object": "verses containing token מלך with article/prefix forms (המלך, למלך, ומלך) — noun/verb/name-object discipline applies before any count is cited",
                         "count": len(melekh)},
    }

    # --- hevel refrain ---
    hevel_forms = collections.defaultdict(list)
    for r, t in toks.items():
        for tok in t:
            base = tok
            if "הבל" in tok and "חבל" not in tok:
                hevel_forms[tok].append(r)
    hevel_refs = mt_sort({r for refs in hevel_forms.values() for r in refs})
    hevel_tokens = sum(len(v) for v in hevel_forms.values())
    havel_havalim = [r for r, s in sk.items() if re.search(r"הבל הבלים", s)]
    hh_token_count = sum(len(re.findall(r"הבל הבלים", sk[r])) for r in havel_havalim)
    hakol_hevel = [r for r, s in sk.items() if re.search(r"הכל הבל", s)]
    hevel = {
        "attested_forms": {f: mt_sort(rs) for f, rs in sorted(hevel_forms.items())},
        "verse_refs": hevel_refs,
        "count_object_verses": "verses containing any token whose skeleton contains הבל (het-bet-lamed חבל excluded — different consonant, different object)",
        "verse_count": len(hevel_refs),
        "count_object_tokens": "hevel-family TOKENS across the book",
        "token_count": hevel_tokens,
        "by_chapter": dict(sorted(collections.Counter(int(r.split(".")[1]) for r in hevel_refs).items())),
        "havel_havalim_phrase": {
            "refs": mt_sort(havel_havalim),
            "count_object": "verses containing the contiguous skeleton phrase הבל הבלים; token-count counts phrase OCCURRENCES",
            "verse_count": len(havel_havalim),
            "phrase_occurrences": hh_token_count},
        "hakol_hevel_phrase": {
            "refs": mt_sort(hakol_hevel),
            "count_object": "verses containing the contiguous skeleton phrase הכל הבל",
            "count": len(hakol_hevel)},
        "inclusio_note": "the superlative havel-havalim phrase brackets the monologue: first and last sites form the 1:2 <-> 12:8 inclusio (12:8 with the plene definite qohelet form); byte-derived above, argued by writers from bytes",
    }

    # --- reut/rayon ruach ---
    reut = [r for r, s in sk.items() if re.search(r"רעות רוח", s)]
    rayon = [r for r, s in sk.items() if re.search(r"רעיון רוח", s)]
    ruach = [r for r, t in toks.items()
             if any("רוח" in x and "ירוח" not in x for x in t)]

    # --- under the sun ---
    tachat_shemesh = [r for r, s in sk.items() if re.search(r"תחת השמש", s)]
    shemesh_all = [r for r, t in toks.items() if any("שמש" in x for x in t)]
    shemesh_bare = [r for r in shemesh_all if r not in set(tachat_shemesh)]

    # --- time catalogue ---
    def et_count(r):
        return sum(1 for x in toks[r] if x in ("עת", "ועת", "לעת", "בעת", "והעת", "העת"))
    poem = [f"{BOOK}.3.{v}" for v in range(1, 9)]
    et_poem = {r: et_count(r) for r in poem}
    et_elsewhere = [r for r in sk if r not in set(poem) and et_count(r)]
    zman = [r for r, t in toks.items() if any(x in ("זמן", "וזמן", "לזמן") for x in t)]
    time_catalogue = {
        "poem_span_mt": "Eccl.3.1-Eccl.3.8 (identity zone — WEB same)",
        "et_tokens_per_poem_verse": et_poem,
        "et_poem_total": sum(et_poem.values()),
        "count_object": "word-bound tokens עת with attested prefix forms (ועת/לעת/בעת); עתה (now) is a DIFFERENT token, never blended",
        "et_verses_outside_poem": {"refs": mt_sort(et_elsewhere),
                                   "count": len(et_elsewhere)},
        "zman_sites": {"refs": mt_sort(zman),
                       "count_object": "verses containing token זמן (the rare season loan-register noun)",
                       "count": len(zman)},
        "samekh_bracket_note": "SAMEKH segs stand at MT 3:1 and 3:8 — the catalogue's own seam verses (tier-3 weak, single witness; see pmarks)",
    }

    # --- tov comparatives ---
    tov_min = []
    for r, t in toks.items():
        for i, x in enumerate(t[:-1]):
            if x in ("טוב", "וטוב", "טובה", "וטובה") and t[i + 1].startswith("מ"):
                tov_min.append(r)
                break
    tov_openers = [r for r, t in toks.items() if t and t[0] in ("טוב", "טובה")]
    web_better = [ref for ref, d in web.items() if re.search(r"\bbetter\b", d["clean"], re.I)]
    tov = {
        "tov_min_adjacent": {
            "refs": mt_sort(tov_min),
            "count_object": "verses with a טוב/טובה token immediately followed by a מ-prefixed token (skeleton adjacency HEURISTIC for the better-than construction — the Prov phrase-extension trap is LIVE: a מ-prefix after tov is not always comparative; construction check required before citing)",
            "count": len(tov_min)},
        "tov_openers": {"refs": mt_sort(tov_openers),
                        "count_object": "verses whose first skeleton token is טוב/טובה",
                        "count": len(tov_openers)},
        "web_better_verses": {
            "count_object": "WEB verses containing the word better (ENGLISH-SIDE HEURISTIC texture, never evidence)",
            "count": len(web_better),
            "by_chapter": dict(sorted(collections.Counter(int(r.split(".")[1]) for r in web_better).items()))},
    }

    # --- carpe diem ---
    def has_root(r, prefixes):
        return any(any(x.startswith(p) or x[1:].startswith(p) for p in prefixes)
                   for x in toks[r])
    eat_drink = [r for r in sk
                 if any("אכל" in x or "אכול" in x for x in toks[r])
                 and any("שתה" in x or "שתו" in x or "לשתות" in x for x in toks[r])]

    # --- allegory zone 11:7-12:8 ---
    zone = [f"{BOOK}.11.{v}" for v in range(7, 11)] + [f"{BOOK}.12.{v}" for v in range(1, 9)]
    ad_asher_lo = [r for r in sk if re.search(r"עד אשר לא", sk[r])]
    zakhar = [r for r in zone if any("זכר" in x for x in toks[r])]
    samach = [r for r in zone if any("שמח" in x for x in toks[r])]
    youth = [r for r in sk if any(("בחור" in x and "בחורי" not in x) or "ילדות" in x or "שחרות" in x
                                  for x in toks[r])]
    allegory = {
        "zone_note": "11:7-12:8 (identity zone): the rejoice-then-remember bridge and the aging allegory; bounds are WRITER territory argued from bytes",
        "ad_asher_lo_anaphora": {
            "refs": mt_sort(ad_asher_lo),
            "count_object": "verses containing the contiguous skeleton phrase עד אשר לא (the before-clause anaphora spine of 12:1-7)",
            "count": len(ad_asher_lo)},
        "zakhar_remember_in_zone": {"refs": mt_sort(zakhar),
                                    "count_object": "zone verses containing a זכר-root token",
                                    "count": len(zakhar)},
        "samach_rejoice_in_zone": {"refs": mt_sort(samach),
                                   "count_object": "zone verses containing a שמח-root token",
                                   "count": len(samach)},
        "youth_terms": {"refs": mt_sort(youth),
                        "count_object": "verses containing youth-vocabulary tokens (בחור-family youth/prime, ילדות childhood, שחרות dawn-of-life)",
                        "count": len(youth)},
    }

    # --- elohim / yhwh ---
    elohim_exact = [r for r, t in toks.items() if "אלהים" in t]
    elohim_def = [r for r, t in toks.items() if "האלהים" in t]
    elohim_family = [r for r, t in toks.items() if any("אלהים" in x for x in t)]
    yhwh = [r for r, t in toks.items() if any("יהוה" in x for x in t)]
    elohim = {
        "elohim_bare_token": {"refs": mt_sort(elohim_exact),
                              "count_object": "verses containing the exact unprefixed token אלהים",
                              "count": len(elohim_exact)},
        "ha_elohim_token": {"refs": mt_sort(elohim_def),
                            "count_object": "verses containing the exact token האלהים (the definite the-God form Eccl favors)",
                            "count": len(elohim_def)},
        "elohim_any_form": {
            "count_object": "verses containing ANY token carrying אלהים (bare, definite, prefixed)",
            "count": len(elohim_family),
            "by_chapter": dict(sorted(collections.Counter(int(r.split(".")[1]) for r in elohim_family).items()))},
        "yhwh_absence": {
            "count_object": "verses containing any token carrying יהוה — swept, not assumed",
            "count": len(yhwh),
            "note": "ZERO byte-verified: the divine name never occurs in Eccl; every God-reference is Elohim. Any YHWH citation in an Eccl row is a fabrication. This absence is itself citable WITH this sweep digit."},
    }

    # --- sentence-zone texture (granularity-gate staging signals) ---
    adj_by_ch = {}
    pairs_by_ch = {}
    for c in sorted(MT_LAST_VERSE):
        shared = 0
        pairs = MT_LAST_VERSE[c] - 1
        for v in range(1, MT_LAST_VERSE[c]):
            a = {t for t in toks[f"{BOOK}.{c}.{v}"] if len(t) >= 2 and t not in STOP}
            b = {t for t in toks[f"{BOOK}.{c}.{v+1}"] if len(t) >= 2 and t not in STOP}
            if a & b:
                shared += 1
        adj_by_ch[str(c)] = shared
        pairs_by_ch[str(c)] = pairs
    but_by_ch = collections.Counter()
    for ref, d in web.items():
        if ", but " in d["clean"].lower() or d["clean"].lower().startswith("but "):
            but_by_ch[int(ref.split(".")[1])] += 1
    texture = {
        "catchword_adjacency": {
            "count_object": "adjacent-MT-verse pairs sharing >=1 content token (skeleton tier, len>=2, stoplist-filtered) per chapter — HEURISTIC staging signal for the granularity gate; writers re-derive specific chains from bytes",
            "shared_pairs_by_chapter": adj_by_ch,
            "total_pairs_by_chapter": pairs_by_ch},
        "web_but_texture": {
            "count_object": "WEB verses containing ', but ' (or opening 'But ') per WEB chapter — ENGLISH-SIDE HEURISTIC, never evidence",
            "by_chapter": dict(sorted(but_by_ch.items()))},
    }

    pm = load_pmarks()
    para_by_ch = collections.Counter()
    for ref, ms in pm["marks"].items():
        para_by_ch[int(ref.split(".")[1])] += len(ms)
    kq_sites = [with_web(r) for r in mt_sort(pm["kq"])]
    paseq_sites = [with_web(r) for r in mt_sort(pm["paseq"])]
    folds = [ref for ref, d in web.items() if d["continuation_paragraphs"]]

    out = {
        "book": BOOK,
        "built": "Phase 0, 2026-08-19, from staged bytes (orchestrator)",
        "numbering_note": "MT-keyed except where marked; NON-IDENTITY book — MT 4:17 = WEB 5:1, MT 5:1-19 = WEB 5:2-20; use eccl_lib crosswalk",
        "frame_seams": frame_seams,
        "hevel_refrain": hevel,
        "reut_ruach": {
            "reut_ruach_phrase": {"refs": mt_sort(reut),
                                  "count_object": "verses containing the contiguous skeleton phrase רעות רוח",
                                  "count": len(reut)},
            "rayon_ruach_phrase": {"refs": mt_sort(rayon),
                                   "count_object": "verses containing the contiguous skeleton phrase רעיון רוח — a DIFFERENT attested form, never blended with רעות רוח",
                                   "count": len(rayon)},
            "ruach_any": {"count_object": "verses containing any token carrying רוח (wind/breath/spirit — name the sense before counting)",
                          "count": len(ruach)},
        },
        "under_the_sun": {
            "tachat_hashemesh": {"refs": mt_sort(tachat_shemesh),
                                 "count_object": "verses containing the contiguous skeleton phrase תחת השמש",
                                 "count": len(tachat_shemesh),
                                 "by_chapter": dict(sorted(collections.Counter(int(r.split(".")[1]) for r in tachat_shemesh).items()))},
            "shemesh_outside_formula": {"refs": mt_sort(shemesh_bare),
                                        "count_object": "verses with a שמש-carrying token but WITHOUT the תחת השמש phrase",
                                        "count": len(shemesh_bare)},
        },
        "time_catalogue": time_catalogue,
        "tov_comparatives": tov,
        "carpe_diem": {
            "refs": mt_sort(eat_drink),
            "count_object": "verses containing both an אכל-family token and a שתה-family token (eat+drink co-occurrence — the enjoyment-refrain staging signal; writers argue each passage's bounds from bytes)",
            "count": len(eat_drink)},
        "allegory_zone": allegory,
        "elohim_yhwh": elohim,
        "sentence_zone_texture": texture,
        "parashah_distribution": {
            "count_object": "PE/SAMEKH segs per MT chapter (WLC single witness; tier-3 weak in Writings)",
            "by_chapter": dict(sorted(para_by_ch.items())),
            "sites": {r: pm["marks"][r] for r in mt_sort(pm["marks"])}},
        "kq_distribution": {
            "count_object": "ketiv/qere variant notes (MT-keyed, with WEB back-ref where the offset zone is touched)",
            "sites": kq_sites, "total_notes": sum(pm["kq"].values())},
        "paseq_sites": {"count_object": "paseq segs (COUNT-ONLY layer; MT-keyed with WEB back-ref where offset)",
                        "sites": paseq_sites},
        "continuation_folds": {
            "web_refs": folds,
            "count_object": "WEB verses whose text folds across a paragraph mark (the M8-LOG-0002 folding class — LIVE in this prose book)",
            "count": len(folds)},
    }
    (SPBOOK / "eccl_device_inventory.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({
        "divrei_initial": divrei_initial,
        "qohelet_sites": qoh_refs,
        "qohelet_forms": {f: len(rs) for f, rs in sorted(qoh_forms.items())},
        "amar_qohelet": mt_sort(amar_qoh),
        "ani_verses": len(ani), "shavti": mt_sort(shavti), "raiti": len(raiti),
        "hevel_verses": len(hevel_refs), "hevel_tokens": hevel_tokens,
        "havel_havalim": mt_sort(havel_havalim), "hh_occurrences": hh_token_count,
        "hakol_hevel": mt_sort(hakol_hevel),
        "reut_ruach": mt_sort(reut), "rayon_ruach": mt_sort(rayon),
        "tachat_hashemesh": len(tachat_shemesh), "shemesh_bare": mt_sort(shemesh_bare),
        "et_poem_total": sum(et_poem.values()), "et_outside": mt_sort(et_elsewhere),
        "zman": mt_sort(zman),
        "tov_min": len(tov_min), "tov_openers": mt_sort(tov_openers),
        "better_by_ch": dict(sorted(collections.Counter(int(r.split(".")[1]) for r in web_better).items())),
        "eat_drink": mt_sort(eat_drink),
        "ad_asher_lo": mt_sort(ad_asher_lo), "youth": mt_sort(youth),
        "elohim_any": len(elohim_family), "yhwh": len(yhwh),
        "catchword_shared": adj_by_ch, "but_by_ch": dict(sorted(but_by_ch.items())),
        "folds": folds,
    }, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
