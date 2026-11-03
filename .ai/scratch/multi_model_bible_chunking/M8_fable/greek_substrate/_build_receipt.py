#!/usr/bin/env python3
"""Regenerate STAGING_RECEIPT.v1.json from the staged bytes (MEASURED) plus the fixed source specs below.

Sizes and sha256 are measured from disk on every run; the licence and provenance fields are EXTRACTED from the
source files named in each spec and were read before any byte was used. A set whose folder is absent is recorded as
awaiting the owner's per-file yes (OW-31 binding); a set whose folder holds a file that is not in its spec, or that
lacks a listed file, fails closed (exit 1) and the receipt is not written.

Usage: python _build_receipt.py            (writes STAGING_RECEIPT.v1.json, prints a one-line summary)
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

NT_BOOKS_RP = ("MAT MAR LUK JOH ACT ROM 1CO 2CO GAL EPH PHP COL 1TH 2TH 1TI 2TI TIT PHM HEB JAM 1PE 2PE "
               "1JO 2JO 3JO JUD REV").split()
NT_BOOKS_SBL = ("Matt Mark Luke John Acts Rom 1Cor 2Cor Gal Eph Phil Col 1Thess 2Thess 1Tim 2Tim Titus Phlm Heb "
                "Jas 1Pet 2Pet 1John 2John 3John Jude Rev").split()

GOVERNED = {"reused_from": {"archive_path": "data/raw/original_language/greek/sblgnt/raw/sblgnt-c4d241a9c1c4.zip",
    "archive_sha256": "4fc2659ce10ec6f57552f22e039de927ed3e417c7b5a757f34f05dae530e4c0f", "archive_size_bytes": 1414688,
    "manifest": "data/raw/original_language/greek/sblgnt/source_manifest.yaml", "manifest_status": "verified",
    "manifest_downloaded_at": "2026-07-04T21:19:41+00:00", "newly_downloaded": False,
    "correspondence_check": "_stage_and_verify.py: archive sha256 = manifest; every staged file git-blob-sha1 = upstream tree at commit"}}

SETS = [
    {
        "set": "A", "folder": "byzantine_rp_PRIMARY", "role": "PRIMARY Greek NT witness (OW-31)",
        "disposition": "newly_acquired",
        "owner_terms_2026-09-29": "independent comparison witness, not a preferred reading or textual authority",
        "witness": "Robinson-Pierpont Byzantine Textform, RP2018 text",
        "repository": "https://github.com/byztxt/byzantine-majority-text",
        "pin": {"tag": "v3.3.2", "commit": "27a45ff1b7be6c17ccbfeac414f3f55732ae8e28"},
        "raw_base": "https://raw.githubusercontent.com/byztxt/byzantine-majority-text/v3.3.2/",
        "files": {**{f"{b}.csv": f"csv-unicode/ccat/no-variants/{b}.csv" for b in NT_BOOKS_RP},
                  "PA.csv": "csv-unicode/ccat/no-variants/PA.csv",
                  "ACT24.csv": "csv-unicode/ccat/no-variants/ACT24.csv",
                  "LICENSE.txt": "LICENSE.txt", "README.md": "README.md",
                  "csv-unicode_README.md": "csv-unicode/README.md"},
        "licence": {"name": "The Unlicense (public-domain dedication)", "tier": "EXTRACTED",
                    "read_from": ["LICENSE.txt", "README.md section '## Copyright'"],
                    "quoted": "All the code and text contained in this folder is in the Public Domain.",
                    "owner_assumption_ow31": "public domain", "matches_assumption": True},
    },
    {
        "set": "B", "folder": "sblgnt_SECONDARY", "role": "SECONDARY Greek NT witness, critical-text disclosure (OW-31)",
        "disposition": "reuse_existing_governed_raw", **GOVERNED,
        "witness": "SBL Greek New Testament v1.2",
        "repository": "https://github.com/Faithlife/SBLGNT (LogosBible/SBLGNT redirects here)",
        "pin": {"tag": None, "commit": "c4d241a9c1c479a55b989ba35a4976c1d0b8052c"},
        "raw_base": "https://raw.githubusercontent.com/Faithlife/SBLGNT/c4d241a9c1c479a55b989ba35a4976c1d0b8052c/",
        "files": {**{f"{b}.txt": f"data/sblgnt/text/{b}.txt" for b in NT_BOOKS_SBL},
                  "LICENSE": "LICENSE", "README.md": "README.md"},
        "licence": {"name": "CC BY 4.0", "tier": "EXTRACTED", "read_from": ["LICENSE", "README.md section '## License'"],
                    "attribution": "Copyright 2010 by the Society of Biblical Literature and Logos Bible Software",
                    "owner_assumption_ow31": "CC BY 4.0", "matches_assumption": True},
    },
    {
        "set": "B2", "folder": "sblgnt_apparatus", "role": "SBLGNT apparatus, critical-text disclosure (optional)",
        "disposition": "reuse_existing_governed_raw", **GOVERNED,
        "owner_terms_2026-09-29": "logically distinct from the base text; comparison/apparatus evidence only; the "
            "canonical-source-view classification of sblgntapp as excluded/noncanonical is unchanged; no promotion to "
            "source-language text, no preferred readings, no textual-critical truth",
        "witness": "SBLGNT apparatus v1.2",
        "repository": "https://github.com/Faithlife/SBLGNT",
        "pin": {"tag": None, "commit": "c4d241a9c1c479a55b989ba35a4976c1d0b8052c"},
        "raw_base": "https://raw.githubusercontent.com/Faithlife/SBLGNT/c4d241a9c1c479a55b989ba35a4976c1d0b8052c/",
        "files": {f"{b}.txt": f"data/sblgntapp/text/{b}.txt" for b in NT_BOOKS_SBL},
        "licence": {"name": "CC BY 4.0 (repository LICENSE)", "tier": "EXTRACTED", "read_from": ["LICENSE"]},
    },
    {
        "set": "C", "folder": "swete_lxx_REFERENCE_ONLY", "role": "REFERENCE-ONLY Greek OT witness (OW-31); never primary",
        "witness": "Swete, The Old Testament in Greek, vol. 3 (Cambridge University Press, 1905), First1KGreek TEI",
        "repository": "https://github.com/OpenGreekAndLatin/First1KGreek",
        "pin": {"tag": None, "commit": "8ee111eb44ecef4120c844e10749178d95d1f30c"},
        "raw_base": "https://raw.githubusercontent.com/OpenGreekAndLatin/First1KGreek/8ee111eb44ecef4120c844e10749178d95d1f30c/",
        "files": {"tlg0527.tlg057.1st1K-grc1.xml": "data/tlg0527/tlg057/tlg0527.tlg057.1st1K-grc1.xml",
                  "tlg0527.tlg056.1st1K-grc1.xml": "data/tlg0527/tlg056/tlg0527.tlg056.1st1K-grc1.xml",
                  "tlg0527.tlg053.1st1K-grc1.xml": "data/tlg0527/tlg053/tlg0527.tlg053.1st1K-grc1.xml",
                  "tlg0527.tlg046.1st1K-grc1.xml": "data/tlg0527/tlg046/tlg0527.tlg046.1st1K-grc1.xml",
                  "license.md": "license.md"},
        "work_titles": {"tlg057": "Daniel (Theodotionis versio)", "tlg056": "Daniel (translatio Graeca)",
                        "tlg053": "Ezechiel", "tlg046": "Zacharias"},
        "licence": {"name": "CC BY-SA 4.0", "tier": "EXTRACTED",
                    "url": "https://creativecommons.org/licenses/by-sa/4.0/",
                    "read_from": ["license.md", "each XML teiHeader <availability>/<licence>"],
                    "quoted": "Available under a Creative Commons Attribution-ShareAlike 4.0 International License",
                    "attribution": "Open Greek and Latin Project, First1KGreek; source edition H. B. Swete, The Old "
                                   "Testament in Greek, vol. 3, Cambridge University Press 1905 (Internet Archive scan)",
                    "owner_assumption_ow31": "public domain", "matches_assumption": False,
                    "note": "The printed 1905 edition is INFERRED public domain by age; the DIGITAL transcription "
                            "staged here is CC BY-SA 4.0 as EXTRACTED from its own headers."},
        "handling_terms_owner_2026-09-29": [
            "Accepted as a reference-only witness under CC BY-SA 4.0; exact licence, attribution, source URL, "
            "version/hash and provenance are preserved in this receipt.",
            "Swete text bytes stay isolated from canonical Scripture, shipped derived datasets, graph/retrieval "
            "truth, embeddings, reviewed-gold text and redistributable alignment outputs.",
            "Derived observations may record non-textual facts/provenance where legally appropriate; no substantial "
            "Swete text is reproduced, and 'reference-only' is not treated as exempt from the licence.",
            "If a later feature needs to publish Swete wording or a derivative of the digital transcription, STOP "
            "for a separate licence/output review.",
            "A genuinely public-domain Greek OT witness may be researched later if a redistribution-friendly "
            "source is needed.",
        ],
    },
]

RETRIEVED = {"C": "2026-09-29T19:34:31Z", "A": "2026-09-29T19:50:50Z",   # UTC download time, from `date -u`
             "B": "2026-09-29 (extracted locally from the governed archive; no download)",
             "B2": "2026-09-29 (extracted locally from the governed archive; no download)"}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    out_sets, problems = [], []
    for spec in SETS:
        folder = HERE / spec["folder"]
        rec = {k: v for k, v in spec.items() if k != "files"}
        if not folder.is_dir():
            rec["status"] = "awaiting_owner_per_file_yes"
            rec["files"] = [{"name": n, "source_path": s} for n, s in spec["files"].items()]
            out_sets.append(rec)
            continue
        on_disk = {p.name for p in folder.iterdir() if p.is_file()}
        missing = sorted(set(spec["files"]) - on_disk)
        extra = sorted(on_disk - set(spec["files"]))
        if missing or extra:
            problems.append({"set": spec["set"], "missing": missing, "unexpected": extra})
        rec["status"] = "staged"
        rec["retrieved_utc"] = RETRIEVED.get(spec["set"])
        rec["files"] = [{"name": n, "source_url" if spec.get("disposition") != "reuse_existing_governed_raw" else "upstream_url_of_same_bytes": spec["raw_base"] + s, "bytes": (folder / n).stat().st_size,
                         "sha256": sha256(folder / n), "tier": "MEASURED"}
                        for n, s in spec["files"].items() if (folder / n).is_file()]
        rec["total_bytes"] = sum(f["bytes"] for f in rec["files"])
        out_sets.append(rec)
    if problems:
        print(json.dumps({"status": "RED", "problems": problems}))
        return 1
    receipt = {"receipt": "greek_substrate STAGING_RECEIPT", "version": 1, "owner_decision": "OW-31 (2026-09-29)",
               "generator": "_build_receipt.py",
               "web_reference": {"path": "data/raw/bible/eng-web/usfm/eng-web_usfm.zip (repo root)",
                                 "sha256": "a745365f53ab95570e9c39a60a7d245ba10bbf6c863832006876b01ea8654f8e",
                                 "tier": "MEASURED", "note": "matches SOURCE_TEXT_ATTRIBUTION.md; read-only"},
               "sets": out_sets}
    (HERE / "STAGING_RECEIPT.v1.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=1) + "\n",
                                                  encoding="utf-8")
    print(json.dumps({"status": "GREEN", "sets": {s["set"]: s["status"] for s in out_sets}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
