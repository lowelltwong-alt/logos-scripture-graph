#!/usr/bin/env python3
"""Stage SBLGNT B/B2 from the existing governed raw archive (NO download) and verify A, B, B2 against upstream.

Owner decision 2026-09-29: B and B2 are reused from data/raw/original_language/greek/sblgnt/ (disposition
reuse_existing_governed_raw). Fail closed (exit 1, nothing further written) when:
  - the archive's sha256 or size differs from its source_manifest.yaml;
  - a required member is absent from the archive, or appears twice;
  - any staged file's git blob sha1 differs from the upstream tree entry at the pinned commit (A, B, B2);
  - a staged folder holds a file that the upstream listing does not.
Upstream listings are read with `gh api` (metadata only; no file bytes are fetched here).

Usage: python _stage_and_verify.py [--stage]     (--stage extracts B/B2 when their folders are absent)
Prints one JSON line.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]                     # .../logos-t423-m8-fable
RAW = REPO / "data/raw/original_language/greek/sblgnt"
SBL_COMMIT = "c4d241a9c1c479a55b989ba35a4976c1d0b8052c"
RP_TAG = "v3.3.2"

# (set, folder, repo, ref, upstream dir, extra upstream files {local name: upstream path})
CHECKS = [
    ("A", "byzantine_rp_PRIMARY", "byztxt/byzantine-majority-text", RP_TAG, "csv-unicode/ccat/no-variants",
     {"LICENSE.txt": "LICENSE.txt", "README.md": "README.md", "csv-unicode_README.md": "csv-unicode/README.md"}),
    ("B", "sblgnt_SECONDARY", "Faithlife/SBLGNT", SBL_COMMIT, "data/sblgnt/text",
     {"LICENSE": "LICENSE", "README.md": "README.md"}),
    ("B2", "sblgnt_apparatus", "Faithlife/SBLGNT", SBL_COMMIT, "data/sblgntapp/text", {}),
]


def gh(path: str):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        raise RuntimeError(f"gh api {path}: {r.stderr.strip()[:200]}")
    return json.loads(r.stdout)


def blob_sha(b: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def manifest_value(key: str) -> str:
    m = re.search(rf"^{key}:\s*'?([^'\n]+)'?\s*$", (RAW / "source_manifest.yaml").read_text(encoding="utf-8"), re.M)
    return m.group(1).strip() if m else ""


def upstream(repo: str, ref: str, d: str, extra: dict[str, str]) -> dict[str, tuple[str, int]]:
    out = {e["name"]: (e["sha"], e["size"]) for e in gh(f"repos/{repo}/contents/{d}?ref={ref}") if e["type"] == "file"}
    for local, p in extra.items():
        e = gh(f"repos/{repo}/contents/{p}?ref={ref}")
        out[local] = (e["sha"], e["size"])
    return out


def main() -> int:
    stage = "--stage" in sys.argv
    problems: list[str] = []
    arch = RAW / manifest_value("archive_path").split("sblgnt/", 1)[-1]
    data = arch.read_bytes()
    arch_ok = (hashlib.sha256(data).hexdigest() == manifest_value("sha256")
               and len(data) == int(manifest_value("size_bytes") or -1)
               and manifest_value("resolved_commit") == SBL_COMMIT)
    if not arch_ok:
        print(json.dumps({"status": "RED", "problems": ["governed SBLGNT archive differs from source_manifest.yaml"]}))
        return 1
    result = {"archive": {"path": str(arch.relative_to(REPO)).replace("\\", "/"), "sha256_matches_manifest": True}}
    for s, folder, repo, ref, d, extra in CHECKS:
        want = upstream(repo, ref, d, extra)
        dest = HERE / folder
        if s in ("B", "B2") and not dest.exists():
            if not stage:
                problems.append(f"{s}: not staged (run with --stage)")
                continue
            with zipfile.ZipFile(arch) as z:
                names = z.namelist()
                dest.mkdir()
                for local in want:
                    up = f"{d}/{local}" if local not in extra else extra[local]
                    hits = [n for n in names if n.endswith("/" + up) and n.count("/") == up.count("/") + 1]
                    if len(hits) != 1:
                        problems.append(f"{s}: archive member for {up!r} found {len(hits)} times")
                        continue
                    (dest / local).write_bytes(z.read(hits[0]))
        have = {p.name for p in dest.iterdir() if p.is_file()} if dest.exists() else set()
        bad = [n for n in sorted(want) if n not in have or blob_sha((dest / n).read_bytes()) != want[n][0]]
        extra_local = sorted(have - set(want))
        if bad or extra_local:
            problems.append(f"{s}: blob mismatch or missing {bad[:5]}; unexpected {extra_local[:5]}")
        result[s] = {"files": len(want), "blob_sha1_match": not bad and not extra_local,
                     "bytes": sum(v[1] for v in want.values())}
    status = "GREEN" if not problems else "RED"
    print(json.dumps({"status": status, **result, "problems": problems}))
    return 0 if status == "GREEN" else 1


if __name__ == "__main__":
    sys.exit(main())
