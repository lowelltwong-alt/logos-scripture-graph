#!/usr/bin/env python3
"""OW-1 retrospective deterministic re-scan (owner warning 2026-08-31).

Read-only over M8's OWN completed evidence; writes only report.v1.json +
REPORT.md beside itself. Flags are REVIEW TRIGGERS, never verdicts (E-12 law).

Lanes:
  REG    (E-18 residue)  register/positional/workflow language in row prose —
                         the class of Isa's lost corpus-wide order — over all
                         completed books' chunks.jsonl.
  PUNCT  (E-23)          translation-layer punctuation/paragraphing/
                         capitalization DRIVER language in boundary_rationale /
                         strongest_rejected_alternative only (driver fields;
                         device_notes disclosure talk deliberately out of scope
                         for this trigger queue).
  EXCL   (E-16/E-17 proxy) exclusivity tokens without a digit in the same
                         sentence (mandated-boilerplate shapes exempted).
  CARRIAGE (E-18 arm)    corpus-wide-order language in surviving review-layer
                         artifacts (sp_durable books only) + file inventory —
                         semantic carriage needs a model lane; this pass only
                         builds the trigger inventory.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
M8 = HERE.parent.parent
BOOKS_DIR = M8 / "book_chunks"
SPD = M8 / "sp_durable"

HEB = re.compile(r"[֐-׿ְ-ׇ]+(?:[ ־][֐-׿ְ-ׇ]+)*")
CURLY = re.compile(r"“[^”]*”")
PROSE = ("boundary_rationale", "strongest_rejected_alternative", "device_notes")
DRIVER_FIELDS = ("boundary_rationale", "strongest_rejected_alternative")

REG_CLASSES = {
    "positional_row_reference": re.compile(
        r"\bthat row\b|\bthe (?:previous|next|preceding|following|prior) row\b|"
        r"\brow (?:above|below)\b|\bneighbou?ring row\b|\bsibling row\b|"
        r"\b(?:previous|next|preceding|following) (?:decision|entry)\b", re.I),
    "cross_part_or_part_range": re.compile(
        r"\bcross-part\b|\bpart boundary\b|\bthis part\b|\bwriter part\b|"
        r"\bassigned range\b|\bpart['’]s\b|\bP\d{2}\b(?![-\d])", re.I),
    "decision_id_in_prose": re.compile(r"\bP\d{2}-\d{3}\b"),
    "governance_tooling": re.compile(
        r"\b\w+\.(?:py|jsonl|json|md)\b|\bvalidator\b|\bchecker\b|\btoolkit\b|"
        r"\bTier-0\b|\bthe suite\b|\borchestrator\b|\battempt id\b|"
        r"\bwork order\b|\b(?:writer|author|peer|primary|spot) brief\b", re.I),
    "review_actor": re.compile(
        r"\bboss\b|\bpeer review\w*\b|\bpeer remedy\b|\breviewer\b|"
        r"\bprimar(?:y|ies) (?:packet|review)\b", re.I),
    "erratum_repair_narration": re.compile(
        r"\berrat(?:um|a)\b|\bnow corrected\b|\bpreviously claimed\b|"
        r"\bthe earlier draft\b", re.I),
    "session_wave_reference": re.compile(
        r"\bthis (?:session|wave|cycle)\b|"
        r"\bthe (?:writer|author|peer|spot|micro) wave\b", re.I),
    "strategy_citation": re.compile(
        r"§\s*\d|\bbook_strategy\b|\bstrategy file\b|\bper the strategy\b|"
        r"\bgate ruling\b|\bowner gate\b", re.I),
}

PUNCT_CLASSES = {
    "punctuation_token": re.compile(r"\bpunctuation\b", re.I),
    "period_fullstop_driver": re.compile(
        r"\bfull stop\b|"
        r"\bperiod\b(?=[^.;]{0,50}\b(?:ends?|closes?|divides?|marks?|separates?|boundar)\b)|"
        r"\b(?:ends?|closes?|divides?|separates?)\b[^.;]{0,50}\bperiod\b", re.I),
    "question_exclamation_driver": re.compile(
        r"\bquestion mark\b|\bexclamation (?:mark|point)\b", re.I),
    "quotation_mark_structure": re.compile(
        r"\bquotation marks?\b[^.;]{0,60}\b(?:open|close|end|begin|onset|boundar)|"
        r"\b(?:open|close|end|begin)\w*\b[^.;]{0,60}\bquotation marks?\b", re.I),
    "paragraph_layer": re.compile(r"\bparagraph(?:ing|\s+break|\s+division)s?\b", re.I),
    "capitalization": re.compile(r"\bcapitali[sz](?:e|ed|ation)\b|\bcapital letter\b", re.I),
    "english_sentence_layer": re.compile(
        r"\b(?:WEB|English|translation)['’]?s?\b[^.;]{0,50}\bsentence\b|"
        r"\bsentence\b[^.;]{0,50}\b(?:WEB|English|translation)\b", re.I),
}

EXCL_TOKEN = re.compile(
    r"\b(?:only|sole|solely|unique(?:ly)?|never|exclusively|nowhere|no other)\b", re.I)
EXCL_EXEMPT = re.compile(
    r"absence[^.;]{0,60}never[^.;]{0,30}counter|never[^.;]{0,30}counter-?evidence|"
    r"never conflated|single-witness|count-only|no position (?:is )?assert", re.I)
CARRIAGE_PAT = re.compile(
    r"corpus[- ]wide|book[- ]wide|as its own sweep|"
    r"across (?:the|all) (?:book|corpus|rows|parts)|"
    r"every row (?:that|whose|carrying)|all rows (?:that|whose|carrying)|"
    r"one order should settle", re.I)


def mask(s: str) -> str:
    s = HEB.sub(" ", s)
    return CURLY.sub(lambda m: " " * len(m.group(0)), s)


def scan_book(path: Path):
    reg, punct, excl = [], [], []
    rows_n = 0
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        rows_n += 1
        did = row.get("writer_decision_id") or row.get("decision_id") or f"idx{row.get('chunk_index_in_book','?')}"
        for field in PROSE:
            s = row.get(field)
            if not isinstance(s, str):
                continue
            m = mask(s)
            for cls, pat in REG_CLASSES.items():
                for hit in pat.finditer(m):
                    reg.append({"decision_id": did, "field": field, "class": cls,
                                "match": hit.group(0)[:50],
                                "context": s[max(0, hit.start()-50):hit.start()+70]})
            if field in DRIVER_FIELDS:
                for cls, pat in PUNCT_CLASSES.items():
                    for hit in pat.finditer(m):
                        punct.append({"decision_id": did, "field": field, "class": cls,
                                      "match": hit.group(0)[:50],
                                      "context": s[max(0, hit.start()-60):hit.start()+90]})
            for sent in re.split(r"(?<=[.;])\s+", m):
                if EXCL_TOKEN.search(sent) and not re.search(r"\d", sent) \
                        and "(sweep:" not in sent and not EXCL_EXEMPT.search(sent):
                    excl.append({"decision_id": did, "field": field,
                                 "sentence": sent.strip()[:160]})
    return rows_n, reg, punct, excl


def scan_carriage(book: str):
    root = SPD / book
    if not root.is_dir():
        return None
    inv, hits = [], []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix not in (".json", ".jsonl", ".md"):
            continue
        rel = p.relative_to(root).as_posix()
        low = rel.lower()
        layer = ("review_layer" if any(k in low for k in
                 ("peer", "boss", "work_order", "docket", "consolidat", "review"))
                 else "other")
        inv.append({"file": rel, "layer": layer, "bytes": p.stat().st_size})
        if layer != "review_layer":
            continue
        try:
            text = p.read_text(encoding="utf-8-sig")
        except Exception as e:  # unreadable: record, never guess
            hits.append({"file": rel, "error": str(e)[:120]})
            continue
        found = [hit.group(0) for hit in CARRIAGE_PAT.finditer(text)]
        if found:
            counts = {}
            for f0 in found:
                counts[f0.lower()] = counts.get(f0.lower(), 0) + 1
            hits.append({"file": rel, "match_count": len(found), "by_phrase": counts})
    return {"review_layer_files": sum(1 for i in inv if i["layer"] == "review_layer"),
            "total_files": len(inv),
            "corpus_wide_language_hits": hits}


def main():
    books = sorted(d.name for d in BOOKS_DIR.iterdir() if (d / "chunks.jsonl").is_file())
    report = {"schema": "m8_ow1_retro_scan.v1", "ran": "2026-08-31",
              "activation": "owner warning OW-1 (chat, 2026-08-31)",
              "flags_are_review_triggers_not_verdicts": True,
              "books_scanned": books, "per_book": {}, "carriage": {},
              "limits": [
                  "PUNCT lane scans driver fields only (boundary_rationale, strongest_rejected_alternative); disclosure-position punctuation talk in device_notes is out of this queue by design",
                  "EXCL lane exempts the mandated-boilerplate shapes (absence-never-counterevidence, never-conflated, single-witness, count-only); residual flags include rhetorical uses - triage by content",
                  "CARRIAGE lane is a trigger inventory only: semantic carriage adjudication needs a model lane; books without surviving review-layer artifacts (18 of 23) are auditable at the corpus-pattern layer only",
              ]}
    tot = {"rows": 0, "REG": 0, "PUNCT": 0, "EXCL": 0}
    for b in books:
        rows_n, reg, punct, excl = scan_book(BOOKS_DIR / b / "chunks.jsonl")
        report["per_book"][b] = {
            "rows": rows_n,
            "REG": {"count": len(reg), "flags": reg},
            "PUNCT": {"count": len(punct), "flags": punct},
            "EXCL": {"count": len(excl), "flags": excl}}
        tot["rows"] += rows_n
        tot["REG"] += len(reg)
        tot["PUNCT"] += len(punct)
        tot["EXCL"] += len(excl)
    for b in ("Eccl", "Prov", "Ps", "Song", "Isa"):
        c = scan_carriage(b)
        if c is not None:
            report["carriage"][b] = c
    report["totals"] = tot
    out = HERE / "report.v1.json"
    json.dump(report, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    lines = ["# OW-1 retro scan — summary (2026-08-31)", "",
             f"Books scanned: {len(books)}; rows: {tot['rows']}.",
             f"Lane totals: REG {tot['REG']} / PUNCT {tot['PUNCT']} / EXCL {tot['EXCL']}"
             " (review triggers, not verdicts).", "",
             "| book | rows | REG | PUNCT | EXCL |", "|---|---|---|---|---|"]
    for b in books:
        pb = report["per_book"][b]
        lines.append(f"| {b} | {pb['rows']} | {pb['REG']['count']} | "
                     f"{pb['PUNCT']['count']} | {pb['EXCL']['count']} |")
    lines += ["", "## Carriage-arm trigger inventory (surviving review layers only)"]
    for b, c in report["carriage"].items():
        nhit = sum(h.get("match_count", 0) for h in c["corpus_wide_language_hits"])
        lines.append(f"- {b}: {c['review_layer_files']} review-layer files; "
                     f"{len(c['corpus_wide_language_hits'])} files with corpus-wide "
                     f"language ({nhit} phrase hits)")
    lines += ["", "## Limits", *[f"- {l}" for l in report["limits"]]]
    (HERE / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"books": len(books), **tot,
                      "carriage_books": list(report["carriage"])}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
