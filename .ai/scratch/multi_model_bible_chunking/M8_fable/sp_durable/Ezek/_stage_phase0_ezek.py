#!/usr/bin/env python3
"""EZEKIEL PHASE 0 STAGING — every input derived from source bytes, none carried from another book.

The source paths are PINNED CONSTANTS with digests, deliberately: the orchestrator had to search for them once,
and that search enumerated the sibling model lanes (recorded as a breach in
SP/campaign/finding_orchestrator_lane_dir_listing.v1.json). Pinning them means no later step ever searches again.

Produces, in SP/Ezek/:
  Ezek_web.usfm          the WEB USFM member, extracted verbatim from the zip (byte-identical, digest asserted)
  Ezek_web_clean.txt     the readable WEB extract in this campaign's established shape
  Ezek_oshb.txt          MT text, one `ref\\ttext` line per verse, from the OSHB XML
  verse_inventory.json   per-chapter WEB verse counts and the book total
  ezek_stage_report.json what was derived, with counts and digests, for the receipt

It asserts rather than assumes: WEB and MT verse counts are compared per chapter and any divergence is REPORTED,
never silently folded. Ezekiel's numbering is believed to be identity throughout, but this run proves it from the
bytes instead of inheriting Jeremiah's offset-zone habit of mind.
"""
import collections
import hashlib
import json
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

SP = Path(__file__).resolve().parent
REPO = Path(r"C:\wt\logos-t423-m8-fable")
BOOK = "Ezek"

OSHB_XML = REPO / "data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/files/Ezek.xml"
WEB_ZIP = REPO / "data/raw/bible/eng-web/usfm/eng-web_usfm.zip"
WEB_MEMBER = "27-EZKeng-web.usfm"
WEB_MEMBER_SHA = "e8e3bf3c4207c5da"  # first 16 hex, asserted below


def sha(b):
    return hashlib.sha256(b).hexdigest()


def extract_web():
    with zipfile.ZipFile(WEB_ZIP) as z:
        raw = z.read(WEB_MEMBER)
    d = sha(raw)
    assert d[:16] == WEB_MEMBER_SHA, "WEB member digest %s does not match the pin %s" % (d[:16], WEB_MEMBER_SHA)
    (SP / f"{BOOK}_web.usfm").write_bytes(raw)
    return raw.decode("utf-8"), d


W = re.compile(r'\\w ([^|\\]*)(?:\|[^\\]*)?\\w\*')
NOTE = re.compile(r"\\f .*?\\f\*", re.S)
CHAR = re.compile(r"\\\+?(?:add|nd|qt|tl|bk|wj|it|bd|sc|no|ord|pn|sig|sls|fig)\s*(.*?)\\\+?[a-z]+\*", re.S)


def strip_markup(s, fn_counter):
    n = len(NOTE.findall(s))
    if n:
        fn_counter[0] += n
        s = NOTE.sub("[fn]", s)
    s = W.sub(r"\1", s)
    for _ in range(3):
        s2 = CHAR.sub(r"\1", s)
        if s2 == s:
            break
        s = s2
    s = re.sub(r"\\\+?[a-z]+\d*\*?", "", s)
    return re.sub(r"[ \t]+", " ", s).strip()


def build_web_clean(usfm):
    """The established shape: a chapter banner, ¶ for a paragraph start, [v] N for a verse, and the poetry /
    structural markers carried through as ` |xx ` so a reviewer can see the line layout the translation used.
    Tier-4 metadata is VISIBLE here and never drives a boundary (E-23) - it is carried so it can be excluded
    knowingly rather than invisibly."""
    out, counts, fn = [], collections.Counter(), [0]
    cur_ch = None
    for line in usfm.splitlines():
        line = line.rstrip()
        if not line:
            continue
        m = re.match(r"\\c\s+(\d+)", line)
        if m:
            cur_ch = int(m.group(1))
            out.append("")
            out.append("===== %s %d =====" % (BOOK.upper(), cur_ch))
            continue
        if cur_ch is None:
            continue  # front matter: \id \ide \h \toc \mt - not scripture text
        tag = re.match(r"\\([a-z]+\d*)\s?(.*)$", line, re.S)
        if not tag:
            out.append(strip_markup(line, fn))
            continue
        t, rest = tag.group(1), tag.group(2)
        if t == "v":
            mv = re.match(r"(\d+(?:-\d+)?)\s*(.*)$", rest, re.S)
            counts[cur_ch] += 1
            out.append("[v] %s %s" % (mv.group(1), strip_markup(mv.group(2), fn)))
        elif t == "p":
            out.append("\u00b6" + (" " + strip_markup(rest, fn) if rest.strip() else ""))
        elif t == "b":
            out.append(" |b(blank poetry line)")
        elif t in ("id", "ide", "h", "toc1", "toc2", "toc3", "mt1", "mt2", "mt3", "rem"):
            continue
        else:
            out.append(" |%s %s" % (t, strip_markup(rest, fn)))
    (SP / f"{BOOK}_web_clean.txt").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    return counts, fn[0]


# NOTE the trailing `[^>]*>`: without it the remainder of the <verse> open tag lands in the body and every verse
# starts with a stray ">". Caught by reading the extracted MT text back, not by the regex looking right.
VERSE = re.compile(r'<verse[^>]*osisID="Ezek\.(\d+)\.(\d+)"[^>]*>(.*?)(?=<verse|</chapter)', re.S)
TAGS = re.compile(r"<[^>]+>")
SEG = re.compile(r"<seg\b[^>]*>.*?</seg>", re.S)


def build_oshb():
    """The established convention, derived by reading Lam.xml against the Lam extract rather than assumed:

      - every <seg> is dropped WITH ITS CONTENT. Lam.xml carries 165 x-maqqef, 154 x-sof-pasuq, 84 x-samekh,
        11 x-paseq and 5 x-pe segs, and Lam_oshb.txt contains zero of U+05BE, U+05C0 and U+05C3. Stripping the
        TAG but keeping the character would silently inject maqaf and sof-pasuq into the running text.
        Those marks are not lost - they are inventoried separately, which is where boundary evidence reads them.
      - the OSHB morpheme separator "/" is removed (ha/ir -> hair); Lam_oshb.txt contains no "/".
      - <note> is apparatus, not scripture, and is dropped."""
    raw = OSHB_XML.read_text(encoding="utf-8")
    rows, counts = [], collections.Counter()
    for c, v, body in VERSE.findall(raw):
        body = re.sub(r"<note.*?</note>", "", body, flags=re.S)
        body = SEG.sub(" ", body)
        txt = TAGS.sub("", body).replace("/", "")
        txt = unicodedata.normalize("NFC", re.sub(r"\s+", " ", txt).strip())
        if not txt:
            continue
        rows.append("%s.%s.%s\t%s" % (BOOK, c, v, txt))
        counts[int(c)] += 1
    (SP / f"{BOOK}_oshb.txt").write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
    return counts, raw


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    usfm, web_digest = extract_web()
    web_counts, fn_sites = build_web_clean(usfm)
    mt_counts, oshb_raw = build_oshb()

    chapters = sorted(set(web_counts) | set(mt_counts))
    divergences = [{"chapter": c, "web": web_counts.get(c, 0), "mt": mt_counts.get(c, 0)}
                   for c in chapters if web_counts.get(c, 0) != mt_counts.get(c, 0)]

    inv = {"book": BOOK, "total_verses": sum(web_counts.values()),
           "chapters": {str(c): web_counts[c] for c in sorted(web_counts)}}
    (SP / "verse_inventory.json").write_text(json.dumps(inv, ensure_ascii=False, indent=1),
                                             encoding="utf-8", newline="\n")

    report = {
        "schema": "m8_phase0_stage_report.v1",
        "book": BOOK,
        "derived_from_bytes_only": True,
        "sources": {
            "oshb_xml": {"path": str(OSHB_XML.relative_to(REPO)).replace("\\", "/"),
                         "sha256": sha(OSHB_XML.read_bytes()), "bytes": OSHB_XML.stat().st_size},
            "web_usfm": {"zip": str(WEB_ZIP.relative_to(REPO)).replace("\\", "/"), "member": WEB_MEMBER,
                         "sha256": web_digest, "bytes": len(usfm.encode("utf-8"))},
        },
        "outputs": {p.name: {"sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
                    for p in sorted(SP.glob("Ezek_*")) if p.is_file()},
        "web": {"chapters": len(web_counts), "total_verses": sum(web_counts.values()),
                "per_chapter": {str(c): web_counts[c] for c in sorted(web_counts)}, "fn_sites": fn_sites},
        "mt": {"chapters": len(mt_counts), "total_verses": sum(mt_counts.values()),
               "per_chapter": {str(c): mt_counts[c] for c in sorted(mt_counts)}},
        "numbering": {
            "identity_throughout": not divergences,
            "divergences": divergences,
            "note": ("every chapter's WEB and MT verse counts were compared from the bytes. A divergence is "
                     "REPORTED here and resolved by an explicit offset map before any row is written; it is never "
                     "silently folded, and Jeremiah's offset-zone is NOT assumed to recur here."),
        },
    }
    (SP / "ezek_stage_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1),
                                               encoding="utf-8", newline="\n")
    print(json.dumps({"web_chapters": len(web_counts), "web_verses": sum(web_counts.values()),
                      "mt_chapters": len(mt_counts), "mt_verses": sum(mt_counts.values()),
                      "identity_numbering": not divergences, "divergences": divergences,
                      "fn_sites": fn_sites,
                      "outputs": list(report["outputs"])}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
