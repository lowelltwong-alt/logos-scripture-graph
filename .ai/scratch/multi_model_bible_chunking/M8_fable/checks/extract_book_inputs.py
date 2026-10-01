#!/usr/bin/env python3
"""Extract per-book working inputs for the M8_fable campaign (Tier-0, deterministic).

Outputs into <out-dir>/<Book>/: verse_inventory.json, chapter_profile.json,
span_features.jsonl, risk_signals.jsonl, book_observation.jsonl, <Book>_web.usfm,
<Book>_web_clean.txt, <Book>_oshb.txt (OT books), web_mt_verse_check.json.

Includes the mandatory raw-vs-clean token audit (lesson M8-LOG-0002): every verse's
alphabetic token count in the cleaned text must match the raw USFM after markup
removal; any mismatch fails the extraction.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[5]
PASSAGES = ROOT / "data" / "canonical" / "scripture" / "passages" / "passages.jsonl"
SUBSTRATE = ROOT / "build" / "observation_substrate" / "current"
WEB_ZIP = ROOT / "data" / "raw" / "bible" / "eng-web" / "usfm" / "eng-web_usfm.zip"
OSHB_DIR = ROOT / "data" / "candidate" / "original_language_evidence" / "canonical_source_views" / "openscriptures_oshb" / "files"

USFM_CODE = {
    "Gen": "GEN", "Exod": "EXO", "Lev": "LEV", "Num": "NUM", "Deut": "DEU",
    "Josh": "JOS", "Judg": "JDG", "Ruth": "RUT", "1Sam": "1SA", "2Sam": "2SA",
    "1Kgs": "1KI", "2Kgs": "2KI", "1Chr": "1CH", "2Chr": "2CH", "Ezra": "EZR",
    "Neh": "NEH", "Esth": "EST", "Job": "JOB", "Ps": "PSA", "Prov": "PRO",
    "Eccl": "ECC", "Song": "SNG", "Isa": "ISA", "Jer": "JER", "Lam": "LAM",
    "Ezek": "EZK", "Dan": "DAN", "Hos": "HOS", "Joel": "JOL", "Amos": "AMO",
    "Obad": "OBA", "Jonah": "JON", "Mic": "MIC", "Nah": "NAM", "Hab": "HAB",
    "Zeph": "ZEP", "Hag": "HAG", "Zech": "ZEC", "Mal": "MAL",
    "Matt": "MAT", "Mark": "MRK", "Luke": "LUK", "John": "JHN", "Acts": "ACT",
    "Rom": "ROM", "1Cor": "1CO", "2Cor": "2CO", "Gal": "GAL", "Eph": "EPH",
    "Phil": "PHP", "Col": "COL", "1Thess": "1TH", "2Thess": "2TH", "1Tim": "1TI",
    "2Tim": "2TI", "Titus": "TIT", "Phlm": "PHM", "Heb": "HEB", "Jas": "JAS",
    "1Pet": "1PE", "2Pet": "2PE", "1John": "1JN", "2John": "2JN", "3John": "3JN",
    "Jude": "JUD", "Rev": "REV",
}

BS = chr(92)


def strip_markup(text: str) -> str:
    text = re.sub(r'\\w ([^|\\]+)\|strong="[^"]*"\\w\*', r'\1', text)
    text = re.sub(r'\\\+?wh ([^\\]*)\\\+?wh\*', r'\1', text)

    def fn(match: re.Match) -> str:
        inner = match.group(1)
        inner = re.sub(r'\\fr ([^\\]+)', r'\1', inner)
        inner = re.sub(r'\\ft ', '', inner)
        inner = re.sub(r'\\fqa? ([^\\]+)', chr(0xAB) + r'\1' + chr(0xBB), inner)
        inner = re.sub(r'\\\+?[a-z]+\*?', '', inner)
        return '[fn ' + ' '.join(inner.split()) + ']'

    text = re.sub(r'\\f \+ (.*?)\\f\*', fn, text, flags=re.S)
    # inline Selah marker: symmetric readable form on both audit sides
    text = re.sub(r'\\\+?qs ([^\\]*)\\\+?qs\*', r'[qs \1]', text)
    return text


def clean_lines(text: str, book_upper: str) -> list[str]:
    out: list[str] = []
    for line in text.splitlines():
        line = line.rstrip()
        if not line:
            continue
        match = re.match(r'\\([a-z0-9]+)\s*(.*)', line)
        if not match:
            out.append(line)
            continue
        tag, rest = match.groups()
        if tag in ('id', 'ide', 'h', 'toc1', 'toc2', 'toc3', 'mt1', 'mt2', 'mt3', 'mt', 'cl'):
            continue
        if tag == 'c':
            out.append('\n===== ' + book_upper + ' ' + rest.strip() + ' =====')
        elif tag == 'p':
            out.append((chr(0xB6) + ' ' + rest).rstrip())
        elif tag == 'm':
            out.append((chr(0xB6) + '(m) ' + rest).rstrip())
        elif tag == 'nb':
            out.append((chr(0xB6) + '(nb no-break) ' + rest).rstrip())
        elif tag in ('q', 'q1'):
            out.append('  |q1 ' + rest)
        elif tag == 'q2':
            out.append('    |q2 ' + rest)
        elif tag == 'q3':
            out.append('      |q3 ' + rest)
        elif tag == 'qr':
            out.append('  |qr(refrain) ' + rest)
        elif tag == 'qs':
            out.append('  |qs(Selah) ' + rest)
        elif tag == 'qc':
            out.append('  |qc(centered) ' + rest)
        elif tag == 'b':
            out.append('  |b(blank poetry line)')
        elif tag in ('s', 's1', 's2', 'r'):
            out.append('[HEADING ' + tag + ': ' + rest + ']')
        elif tag == 'd':
            out.append('[SUPERSCRIPTION: ' + rest + ']')
        elif tag in ('li', 'li1', 'li2'):
            out.append('  ' + chr(0x2022) + ' ' + rest)
        elif tag in ('pi', 'pi1', 'pi2'):
            out.append(chr(0xB6) + chr(0xBB) + '(indented) ' + rest)
        elif tag == 'mi':
            out.append(chr(0xB6) + chr(0x203A) + '(margin) ' + rest)
        elif tag == 'sp':
            out.append('[SPEAKER: ' + rest + ']')
        elif tag in ('ms', 'ms1', 'mr'):
            out.append('[MAJOR-SECTION: ' + rest + ']')
        else:
            out.append('[' + tag + '] ' + rest)
    return out


def verse_tokens(text: str) -> dict[str, int]:
    """chapter.verse -> alphabetic token count, from any text with [vN]/\\v N markers removed of markup."""
    # drop whole heading/superscription/cross-ref lines on the raw side; the clean side
    # wraps these as [HEADING]/[SUPERSCRIPTION] annotations which are stripped below
    kept = []
    for line in text.splitlines():
        if re.match(r'\\(s\d?|r|d|sp|ms\d?|mr)\b', line):
            continue
        kept.append(line)
    text = "\n".join(kept)
    counts: dict[str, int] = {}
    chapter = None
    verse = None
    for token in re.split(r'(\n===== [A-Z0-9 ]+ =====|\[v\] \d+|\\c \d+|\\v \d+)', text):
        header = re.match(r'\n===== [A-Z0-9]+ (\d+) =====', token or '')
        if header:
            chapter = int(header.group(1)); verse = None; continue
        chap2 = re.match(r'\\c (\d+)', token or '')
        if chap2:
            chapter = int(chap2.group(1)); verse = None; continue
        vm = re.match(r'(?:\[v\] |\\v )(\d+)', token or '')
        if vm:
            verse = int(vm.group(1)); continue
        if chapter and verse:
            body = re.sub(r'\[fn [^\]]*\]', '', token)
            body = re.sub(r'\\\+?[a-z0-9]+\*?', ' ', body)
            # strip campaign structural annotations (clean-side) symmetrically
            body = re.sub(r'\|q[123rsc]?\([^)]*\)', ' ', body)
            body = re.sub(r'\|q[123]?', ' ', body)
            body = re.sub(r'\|b\([^)]*\)', ' ', body)
            body = body.replace(chr(0xB6) + '(m)', ' ').replace(chr(0xB6) + '(nb no-break)', ' ')
            body = body.replace(chr(0xB6) + chr(0xBB) + '(indented)', ' ').replace(chr(0xB6) + chr(0x203A) + '(margin)', ' ')
            body = body.replace(chr(0xB6), ' ')
            body = re.sub(r'\[HEADING [^\]]*\]', ' ', body)
            body = re.sub(r'\[SPEAKER: [^\]]*\]', ' ', body)
            body = re.sub(r'\[MAJOR-SECTION: [^\]]*\]', ' ', body)
            body = re.sub(r'\[SUPERSCRIPTION: [^\]]*\]', ' ', body)
            words = re.findall(r"[A-Za-z]+", body)
            key = f"{chapter}.{verse}"
            counts[key] = counts.get(key, 0) + len(words)
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    book = args.book
    out = args.out_dir / book
    out.mkdir(parents=True, exist_ok=True)

    refs = []
    with PASSAGES.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("book") == book:
                refs.append(row["osis_ref"])
    chapters: dict[int, int] = collections.OrderedDict()
    for ref in refs:
        _, ch, v = ref.split(".")
        chapters[int(ch)] = max(chapters.get(int(ch), 0), int(v))
    (out / "verse_inventory.json").write_text(
        json.dumps({"book": book, "total_verses": len(refs), "chapters": chapters}, indent=1),
        encoding="utf-8")

    def filter_jsonl(name: str, dst: str) -> int:
        rows = []
        with (SUBSTRATE / name).open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    row = json.loads(line)
                    if row.get("book_id") == book:
                        rows.append(row)
        with (out / dst).open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        return len(rows)

    n_span = filter_jsonl("span_observation_features.jsonl", "span_features.jsonl")
    filter_jsonl("risk_signal_index.jsonl", "risk_signals.jsonl")
    filter_jsonl("book_observations.jsonl", "book_observation.jsonl")

    profile = []
    with (out / "span_features.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            markers = {k: v for k, v in sorted(row.get("marker_counts", {}).items()) if v}
            profile.append({
                "span": f"{row.get('osis_start')}-{row.get('osis_end')}",
                "verses": row.get("verse_count"),
                "markers": markers,
                "risk_flags": row.get("risk_flags", []),
            })
    (out / "chapter_profile.json").write_text(json.dumps(profile, indent=1, ensure_ascii=False), encoding="utf-8")

    code = USFM_CODE[book]
    zf = zipfile.ZipFile(WEB_ZIP)
    names = [n for n in zf.namelist() if re.match(rf"\d+-{code}eng-web\.usfm$", n)]
    if len(names) != 1:
        raise SystemExit(f"USFM entry ambiguous/missing for {book}: {names}")
    raw = zf.read(names[0]).decode("utf-8")
    (out / f"{book}_web.usfm").write_text(raw, encoding="utf-8")

    stripped = strip_markup(raw)
    lines = clean_lines(stripped, book.upper())
    clean = "\n".join(lines)
    clean = re.sub(r'\\v (\d+)', r'[v] \1', clean)
    clean = re.sub(r'[ \t]+', ' ', clean)
    (out / f"{book}_web_clean.txt").write_text(clean, encoding="utf-8")

    raw_counts = verse_tokens(strip_markup(raw))
    clean_counts = verse_tokens(clean)
    mismatches = []
    for key, count in raw_counts.items():
        if clean_counts.get(key, 0) != count:
            mismatches.append({"verse": key, "raw_tokens": count, "clean_tokens": clean_counts.get(key, 0)})
    if mismatches:
        (out / "token_audit_failures.json").write_text(json.dumps(mismatches, indent=1), encoding="utf-8")
        raise SystemExit(f"TOKEN AUDIT FAIL: {len(mismatches)} verses lost content; see token_audit_failures.json")

    oshb_path = OSHB_DIR / f"{book}.xml"
    web_mt = {"book": book, "oshb_available": oshb_path.is_file()}
    if oshb_path.is_file():
        NS = "{http://www.bibletechnologies.net/2003/OSIS/namespace}"
        tree = ET.parse(oshb_path)
        heb_lines = []
        heb_chapters: dict[int, int] = {}
        for verse in tree.iter(NS + "verse"):
            osis_id = verse.get("osisID", "")
            words = ["".join(w.itertext()).replace("/", "") for w in verse.iter(NS + "w")]
            heb_lines.append(osis_id + "\t" + " ".join(words))
            _, ch, v = osis_id.split(".")
            heb_chapters[int(ch)] = max(heb_chapters.get(int(ch), 0), int(v))
        (out / f"{book}_oshb.txt").write_text("\n".join(heb_lines), encoding="utf-8")
        diffs = [
            {"chapter": ch, "web_last_verse": chapters.get(ch), "mt_last_verse": heb_chapters.get(ch)}
            for ch in sorted(set(chapters) | set(heb_chapters))
            if chapters.get(ch) != heb_chapters.get(ch)
        ]
        web_mt.update({
            "web_total": len(refs),
            "mt_total": len(heb_lines),
            "chapter_mismatches": diffs,
            "status": "identical" if not diffs and len(refs) == len(heb_lines) else "offsets_present_build_crosswalk",
        })
    (out / "web_mt_verse_check.json").write_text(json.dumps(web_mt, indent=1), encoding="utf-8")

    print(json.dumps({
        "book": book,
        "verses": len(refs),
        "chapters": len(chapters),
        "substrate_spans": n_span,
        "clean_chars": len(clean),
        "token_audit": "PASS",
        "web_mt": web_mt.get("status", "no_oshb"),
        "chapter_mismatches": web_mt.get("chapter_mismatches", []),
    }, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
