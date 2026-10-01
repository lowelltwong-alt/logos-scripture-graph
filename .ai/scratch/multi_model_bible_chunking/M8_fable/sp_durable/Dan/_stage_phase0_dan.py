#!/usr/bin/env python3
"""DANIEL PHASE 0 STAGING - every input derived from source bytes, none carried from another book.

Adapted from Ezek/_stage_phase0_ezek.py (sha256 fed64d8ce63c60d8…). The logic is unchanged apart from the book
constants, plus one addition: the LANGUAGE PASS. Daniel's Aramaic is located from the OSHB morph codes, never from
memory. The first character of each main-text <w> morph is its language (H Hebrew, A Aramaic).

The source paths are PINNED CONSTANTS with digests, so no later step ever searches for them. The WEB member digest
was MEASURED at this staging from the member itself, exactly as Ezekiel's was. There is no external registry of
member digests, so the pin guards later drift and does not prove first-read authenticity. The zip's own digest is
recorded in the report for that reason.

Produces, in SP/Dan/:
  Dan_web.usfm            the WEB USFM member, extracted verbatim from the zip (byte-identical, digest asserted)
  Dan_web_clean.txt       the readable WEB extract in this campaign's established shape
  Dan_oshb.txt            MT text, one `ref\\ttext` line per verse, from the OSHB XML
  verse_inventory.json    per-chapter WEB verse counts and the book total
  dan_language_zones.json per-verse language from the morph codes, word-level runs, and every mixed verse's switch
  dan_stage_report.json   what was derived, with counts and digests, for the receipt

It asserts rather than assumes. WEB and MT verse counts are compared per chapter, and any divergence is REPORTED,
never silently folded. The offset map (a separate builder) resolves a divergence; this script does not.
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
BOOK = "Dan"

OSHB_XML = REPO / "data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/files/Dan.xml"
OSHB_XML_SHA = "bc69d0fa9708dacb"  # first 16 hex, MEASURED 2026-09-23 at this staging
WEB_ZIP = REPO / "data/raw/bible/eng-web/usfm/eng-web_usfm.zip"
WEB_MEMBER = "28-DANeng-web.usfm"
WEB_MEMBER_SHA = "b5a967cabbfbec9b"  # first 16 hex, MEASURED 2026-09-23 at this staging


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
# starts with a stray ">". Caught on Ezekiel by reading the extracted MT text back, not by the regex looking right.
VERSE = re.compile(r'<verse[^>]*osisID="Dan\.(\d+)\.(\d+)"[^>]*>(.*?)(?=<verse|</chapter)', re.S)
TAGS = re.compile(r"<[^>]+>")
SEG = re.compile(r"<seg\b[^>]*>.*?</seg>", re.S)
NOTE_X = re.compile(r"<note.*?</note>", re.S)
WORD = re.compile(r"<w\b([^>]*)>(.*?)</w>", re.S)
MORPH = re.compile(r'morph="([^"]*)"')


def build_oshb():
    """The established convention (derived on Lamentations, reused unchanged on Ezekiel):

      - every <seg> is dropped WITH ITS CONTENT, so maqaf, sof pasuq, samekh, paseq and pe never enter the running
        text; they are inventoried separately by the pmarks builder, which is where boundary evidence reads them.
      - the OSHB morpheme separator "/" is removed.
      - <note> is apparatus, not scripture, and is dropped."""
    raw = OSHB_XML.read_bytes()
    d = sha(raw)
    assert d[:16] == OSHB_XML_SHA, "OSHB digest %s does not match the pin %s" % (d[:16], OSHB_XML_SHA)
    raw = raw.decode("utf-8")
    rows, counts, verses = [], collections.Counter(), []
    for c, v, body in VERSE.findall(raw):
        verses.append((int(c), int(v), body))
        b = NOTE_X.sub("", body)
        b = SEG.sub(" ", b)
        txt = TAGS.sub("", b).replace("/", "")
        txt = unicodedata.normalize("NFC", re.sub(r"\s+", " ", txt).strip())
        if not txt:
            continue
        rows.append("%s.%s.%s\t%s" % (BOOK, c, v, txt))
        counts[int(c)] += 1
    (SP / f"{BOOK}_oshb.txt").write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
    return counts, verses, d


def language_pass(verses, oshb_digest):
    """Per main-text word: the first character of its morph code. Words inside <note> (the qere apparatus) are
    counted apart and never enter the zone map, because they are not the running text the rows quote."""
    per_verse, mixed, runs, totals, note_totals = {}, [], [], collections.Counter(), collections.Counter()
    for c, v, body in verses:
        ref = "%s.%d.%d" % (BOOK, c, v)
        for n in NOTE_X.findall(body):
            for attrs, _ in WORD.findall(n):
                m = MORPH.search(attrs)
                note_totals[m.group(1)[:1] if m else "?"] += 1
        main = NOTE_X.sub("", body)
        seq = []
        for i, (attrs, _) in enumerate(WORD.findall(main), 1):
            m = MORPH.search(attrs)
            lang = m.group(1)[:1] if m else "?"
            seq.append(lang)
            totals[lang] += 1
            if runs and runs[-1]["lang"] == lang:
                runs[-1]["end"] = "%s w%d" % (ref, i)
                runs[-1]["words"] += 1
            else:
                runs.append({"lang": lang, "start": "%s w%d" % (ref, i), "end": "%s w%d" % (ref, i), "words": 1})
        kinds = sorted(set(seq))
        per_verse[ref] = kinds[0] if len(kinds) == 1 else "mixed"
        if len(kinds) > 1:
            switches = [i + 1 for i in range(1, len(seq)) if seq[i] != seq[i - 1]]
            mixed.append({"ref": ref, "words": len(seq), "sequence": "".join(seq),
                          "switch_before_word": switches})
    doc = {"schema": "m8_language_zones.v1", "book": BOOK,
           "source": {"path": str(OSHB_XML.relative_to(REPO)).replace("\\", "/"), "sha256": oshb_digest},
           "method": ("language = first character of each main-text <w> morph attribute (H Hebrew, A Aramaic); "
                      "<note> content is excluded from the zone map and counted apart; a run is a maximal sequence "
                      "of consecutive main-text words of one language, in document order"),
           "tier": "EXTRACTED from the OSHB morph codes by this script; no zone was typed by hand",
           "word_totals": dict(sorted(totals.items())), "note_word_totals": dict(sorted(note_totals.items())),
           "runs": runs, "mixed_verses": mixed,
           "verse_language": per_verse}
    (SP / "dan_language_zones.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                                encoding="utf-8", newline="\n")
    return doc


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    usfm, web_digest = extract_web()
    web_counts, fn_sites = build_web_clean(usfm)
    mt_counts, verses, oshb_digest = build_oshb()
    lz = language_pass(verses, oshb_digest)

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
                         "sha256": oshb_digest, "bytes": OSHB_XML.stat().st_size},
            "web_usfm": {"zip": str(WEB_ZIP.relative_to(REPO)).replace("\\", "/"), "zip_sha256": sha(WEB_ZIP.read_bytes()),
                         "member": WEB_MEMBER, "sha256": web_digest, "bytes": len(usfm.encode("utf-8"))},
        },
        "outputs": {p.name: {"sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
                    for p in sorted(list(SP.glob("Dan_*")) + [SP / "verse_inventory.json", SP / "dan_language_zones.json"])
                    if p.is_file()},
        "web": {"chapters": len(web_counts), "total_verses": sum(web_counts.values()),
                "per_chapter": {str(c): web_counts[c] for c in sorted(web_counts)}, "fn_sites": fn_sites},
        "mt": {"chapters": len(mt_counts), "total_verses": sum(mt_counts.values()),
               "per_chapter": {str(c): mt_counts[c] for c in sorted(mt_counts)}},
        "language": {"word_totals": lz["word_totals"], "note_word_totals": lz["note_word_totals"],
                     "runs": len(lz["runs"]), "mixed_verses": [m["ref"] for m in lz["mixed_verses"]]},
        "numbering": {
            "identity_throughout": not divergences,
            "divergences": divergences,
            "note": ("every chapter's WEB and MT verse counts were compared from the bytes. A divergence is "
                     "REPORTED here and resolved by an explicit offset map before any row is written; it is never "
                     "silently folded, and no other book's offset zone is assumed to recur here."),
        },
    }
    (SP / "dan_stage_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1),
                                              encoding="utf-8", newline="\n")
    print(json.dumps({"web_chapters": len(web_counts), "web_verses": sum(web_counts.values()),
                      "mt_chapters": len(mt_counts), "mt_verses": sum(mt_counts.values()),
                      "identity_numbering": not divergences, "divergences": divergences,
                      "fn_sites": fn_sites, "language_word_totals": lz["word_totals"],
                      "note_word_totals": lz["note_word_totals"],
                      "runs": [(r["lang"], r["start"], r["end"], r["words"]) for r in lz["runs"]],
                      "mixed_verses": [(m["ref"], m["sequence"], m["switch_before_word"]) for m in lz["mixed_verses"]],
                      "outputs": list(report["outputs"])}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
