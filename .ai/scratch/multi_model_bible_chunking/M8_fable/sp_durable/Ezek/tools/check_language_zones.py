#!/usr/bin/env python3
"""Language-zone guard for Ezek (FLAGS member; API parity with the island-bearing books).

Ezek is Hebrew THROUGHOUT - byte-proven at Phase 0 from the OSHB morph codes (18,866 H-prefixed, 0 A-prefixed). There is no Aramaic island and no language zone, so:
 1. ARAMAIC LABEL ANYWHERE (flag, review candidate): an "Aramaic" or "Syrian(-language)"
    label within 100 chars of ANY Ezek ref - no verse of Ezekiel is in Aramaic.
    Aramaism / Aramaic-INFLUENCE discussion is legitimate (negative lookahead).
 2. (inert) no Hebrew-label-on-island arm - there is no island.
 3. (inert) no island-disclosure symmetry arm.
Output contract identical to the Jer member: flag_count / flags / status.
Usage: check_language_zones.py file1.json [more...]
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
REFPAT = re.compile(r"Ezek\.(\d+)\.(\d+)")
ARAMAIC = re.compile(r"\bAramaic\b(?!\s*(?:-influenced|influence|ism|izing|coloring|colouring|loan))|\bSyrian\b")
def iter_strings(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items(): yield from iter_strings(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from iter_strings(v, f"{path}[{i}]")
    elif isinstance(o, str): yield path, o
def load_any(p: Path):
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix == ".jsonl": return [json.loads(l) for l in text.splitlines() if l.strip()]
    return json.loads(text)
def main() -> int:
    flags = []
    for f in sys.argv[1:]:
        data = load_any(Path(f))
        for path, s in iter_strings(data):
            for m in REFPAT.finditer(s):
                ctx = s[max(0, m.start() - 100):m.end() + 100]
                if ARAMAIC.search(ctx):
                    flags.append({"file": Path(f).name, "path": path, "issue": "aramaic_label_in_ezek",
                                  "note": "review candidate - Ezek is Hebrew throughout (0 A-prefixed morph codes); no verse is Aramaic",
                                  "ref": m.group(0), "context": ctx[:160]})
    print(json.dumps({"flag_count": len(flags), "flags": flags, "status": "GREEN" if not flags else "FLAGS"}, ensure_ascii=False, indent=1))
    return 1 if flags else 0
if __name__ == "__main__":
    raise SystemExit(main())
