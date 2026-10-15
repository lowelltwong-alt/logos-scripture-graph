#!/usr/bin/env python3
"""1 CORINTHIANS mark inventory (pmarks_1Cor.json) and identity offset map (web_greek_offset_map.json), read from the
files _stage_phase0_1cor.py staged and pinned in 1cor_stage_report.json. Every ref is WEB numbering, which the
staging measured equal to RP and SBLGNT in every verse.

Adapted in purpose, not code, from Dan/_build_pmarks_dan.py: an NT book has no OSHB segs, so the evidence layers are
  1. rp_paragraph_starts   the Byzantine RP edition's pilcrows. All sit at verse start (asserted), so each marks the
                           verse that BEGINS a paragraph in that edition.
  2. web_paragraph_starts  WEB \\p markers. Tier-4 translation formatting, carried VISIBLE so it can be excluded
                           knowingly; it never drives a boundary (E-23). A \\p that falls after text inside a verse is
                           recorded as mid-verse.
  3. sbl_variant_sites     SBLGNT's inline critical signs (U+2E00 block), per verse. A verse carrying one is a
                           TEXTUAL-VARIANT site in SBLGNT's own apparatus; a row spanning one discloses it.
  4. rp_sbl_differences    verses whose RP and SBL wording differ at the skeleton tier (greek_lib.skeleton: accents,
                           case, punctuation and sigla removed). MEASURED variant evidence between the two witnesses.
  5. web_footnote_verses   verses whose WEB text carries a footnote.

WHAT A MARK IS AND IS NOT. A paragraph mark is EVIDENCE of how one edition read the text: it informs a boundary and
never decides one alone. A variant site is a disclosure duty, not a boundary argument.
"""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

SP = Path(__file__).resolve().parent
M8 = SP.parent.parent
BOOK = "1Cor"
sys.path.insert(0, str(M8 / "greek_substrate" / "tools"))
import greek_lib  # noqa: E402

SIGLA = {"\u2e00": "single_word_variant", "\u2e01": "single_word_omission_or_addition", "\u2e02": "span_open",
         "\u2e03": "span_close", "\u2e04": "span2_open", "\u2e05": "span2_close"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read_tsv(name):
    out = {}
    for line in (SP / name).read_text(encoding="utf-8").splitlines():
        ref, txt = line.split("\t", 1)
        out[ref] = txt
    return out


def web_paragraphs(usfm):
    """A paragraph marker followed directly by \\v N starts verse N. A marker followed by text (on its own line or the
    next non-verse line) breaks the CURRENT verse mid-way, and is recorded as mid-verse."""
    starts, mid, ch, cur, pending = [], [], None, None, False
    for line in usfm.splitlines():
        m = re.match(r"\\c\s+(\d+)", line)
        if m:
            ch, cur = int(m.group(1)), None
            continue
        if ch is None or not line.strip():
            continue
        mv = re.match(r"\\v\s+(\d+)", line)
        if mv:
            cur = "%s.%d.%s" % (BOOK, ch, mv.group(1))
            if pending:
                starts.append(cur)
                pending = False
            continue
        mp = re.match(r"\\(?:p|m|nb|pi\d?)(?:\s+(.*))?$", line)
        if mp:
            if (mp.group(1) or "").strip() and cur is not None:
                mid.append(cur)
            else:
                pending = True
            continue
        if pending and cur is not None and not line.startswith("\\"):
            mid.append(cur)
            pending = False
    return starts, mid


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rep = json.loads((SP / "1cor_stage_report.json").read_text(encoding="utf-8"))
    for n, d in rep["outputs"].items():
        assert sha((SP / n).read_bytes()) == d["sha256"], "staged %s drifted from 1cor_stage_report.json" % n
    check = json.loads((SP / "web_greek_verse_check.json").read_text(encoding="utf-8"))
    assert not check["divergent_chapters"] and not check["verses_not_in_all_three"], "numbering is not identity"

    greek_lib.load_rp()
    rp_starts = ["%s.%d.%d" % (BOOK, c, v) for b, c, v in sorted(greek_lib.RP_PARAGRAPH) if b == BOOK]
    raw_rp = (M8 / rep["sources"]["rp_csv"]["path"]).read_text(encoding="utf-8-sig")
    assert raw_rp.count("\u00b6") == len(rp_starts), "a verse carries more than one pilcrow"
    for line in raw_rp.splitlines()[1:]:
        if "\u00b6" in line:
            body = line.split(",", 2)[2].lstrip('"')
            assert body.startswith("\u00b6"), "pilcrow not at verse start: %s" % line[:40]

    usfm = (SP / f"{BOOK}_web.usfm").read_text(encoding="utf-8")
    web_starts, web_mid = web_paragraphs(usfm)

    rp, sbl, clean = read_tsv(f"{BOOK}_rp.txt"), read_tsv(f"{BOOK}_sbl.txt"), {}
    sites = {}
    for ref, t in sbl.items():
        c = collections.Counter(SIGLA.get(ch, "U+%04X" % ord(ch)) for ch in t if 0x2E00 <= ord(ch) <= 0x2E7F)
        if c:
            sites[ref] = dict(sorted(c.items()))
    diffs = [ref for ref in rp if greek_lib.skeleton(rp[ref]) != greek_lib.skeleton(sbl[ref])]
    cur = None
    fn_verses = collections.Counter()
    for line in (SP / f"{BOOK}_web_clean.txt").read_text(encoding="utf-8").splitlines():
        mc = re.match(r"===== 1COR (\d+) =====", line)
        if mc:
            ch = int(mc.group(1))
            continue
        mv = re.match(r"\[v\] (\d+)", line)
        if mv:
            cur = "%s.%d.%s" % (BOOK, ch, mv.group(1))
        if cur and "[fn]" in line:
            fn_verses[cur] += line.count("[fn]")

    out = {
        "book": BOOK,
        "sources": {"stage_report": {"path": "1Cor/1cor_stage_report.json",
                                     "sha256": sha((SP / "1cor_stage_report.json").read_bytes())},
                    "rp_csv": rep["sources"]["rp_csv"], "sbl_txt": rep["sources"]["sbl_txt"],
                    "web_member": {k: rep["sources"]["web_usfm"][k] for k in ("member", "sha256")}},
        "numbering": "WEB = RP = SBLGNT in every verse (437), MEASURED in web_greek_verse_check.json. Every ref is WEB.",
        "rp_paragraph_starts": rp_starts,
        "rp_paragraph_note": ("Byzantine RP pilcrows, each at the start of the verse that begins a paragraph in that "
                              "edition. Edition paragraphing is evidence: it informs a boundary and never decides one "
                              "alone (E-23)."),
        "web_paragraph_starts": web_starts,
        "web_paragraph_midverse": web_mid,
        "web_paragraph_note": ("WEB \\p/\\m/\\nb/\\pi markers: tier-4 translation formatting, VISIBLE so it can be "
                               "excluded knowingly. It never drives a boundary (E-23)."),
        "sbl_variant_sites": sites,
        "sbl_variant_note": ("SBLGNT inline critical signs per verse. Each marks a textual-variant site in SBLGNT's own "
                             "apparatus (the apparatus itself, set B2, stays local and is not read here). A row "
                             "spanning one discloses it; a boundary is never argued from a variant alone."),
        "rp_sbl_differences": diffs,
        "rp_sbl_note": ("verses whose RP and SBLGNT wording differ after greek_lib.skeleton (accents, case, "
                        "punctuation and sigla removed). MEASURED; quote the RP primary and disclose the SBL reading "
                        "where a row's argument rests on the wording."),
        "web_footnote_verses": dict(fn_verses),
        "tally": {"rp_paragraph_starts": len(rp_starts), "web_paragraph_starts": len(web_starts),
                  "web_paragraph_midverse": len(web_mid), "sbl_variant_site_verses": len(sites),
                  "rp_sbl_difference_verses": len(diffs), "web_footnote_verses": len(fn_verses),
                  "rp_and_web_agree_on_start": len(set(rp_starts) & set(web_starts))},
    }
    (SP / f"pmarks_{BOOK}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                                            encoding="utf-8", newline="\n")
    om = {"schema": "m8_web_greek_offset_map.v1", "book": BOOK, "identity_throughout": True, "zones": [],
          "per_chapter": check["per_chapter"],
          "basis": ("MEASURED: web_greek_verse_check.json sha256 %s shows every verse printed by WEB, RP and SBLGNT "
                    "and no divergent chapter; greek_lib.crosswalk('1Cor') carries no flag. A WEB ref is the Greek ref."
                    % sha((SP / "web_greek_verse_check.json").read_bytes())),
          "obligation_on_consumers": ("a consumer that maps WEB to Greek refs must assert identity_throughout is true "
                                      "and fail closed otherwise; never assume identity for another book.")}
    (SP / "web_greek_offset_map.json").write_text(json.dumps(om, ensure_ascii=False, indent=1) + "\n",
                                                  encoding="utf-8", newline="\n")
    print(json.dumps(out["tally"], indent=1))
    print("web_mid:", web_mid[:20])
    return 0


if __name__ == "__main__":
    sys.exit(main())
