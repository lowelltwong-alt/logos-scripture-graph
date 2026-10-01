#!/usr/bin/env python3
"""Language-label guard for Isa (WARN-level heuristic).

Isa has NO Aramaic zones — all 1,291 MT verses are Hebrew (Phase 0 verified:
every OSHB morph code is H-prefixed, 16,988 codes; contrast Ezra/Daniel).
This checker therefore flags ANY "Aramaic" or "Syrian(-language)" label
within 100 chars of an Isa ref: there is no verse of Isaiah for which an
Aramaic grammar label is correct. ("Hebrew" labels are always fine.)
CAUTION, Isa-specific: the narrative zone DISCUSSES Aramaic — at Isa 36:11
(identity ref) the officials ask the Rabshakeh to speak "in the Syrian
language" (ארמית) so the people on the wall cannot understand: DISCUSSING
that request, quoting ארמית, or naming the Aramaic LANGUAGE as story
content is legitimate and will surface here only as a review candidate —
the flagged FAILURE MODE is labeling a VERSE as being IN Aramaic.
Aramaism/Aramaic-INFLUENCE discussion is likewise legitimate; flags are
review candidates, not auto-fails.
Usage: check_language_zones.py file1.json [more...]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REFPAT = re.compile(r"Isa\.(\d+)\.(\d+)")


def iter_strings(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from iter_strings(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from iter_strings(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o


def load_any(p: Path):
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix == ".jsonl":
        return [json.loads(l) for l in text.splitlines() if l.strip()]
    return json.loads(text)


def main() -> int:
    flags = []
    for f in sys.argv[1:]:
        for path, s in iter_strings(load_any(Path(f))):
            for m in REFPAT.finditer(s):
                ctx = s[max(0, m.start() - 100):m.end() + 100]
                if re.search(r"\bAramaic\b(?!\s*(?:-influenced|influence|ism|izing|"
                             r"coloring|colouring|loan))|\bSyrian\b", ctx):
                    flags.append({"file": Path(f).name, "path": path,
                                  "issue": "aramaic_label_in_isa_all_hebrew",
                                  "note": ("review candidate — the 36:11 Rabshakeh "
                                           "request DISCUSSES Aramaic legitimately; "
                                           "the failure mode is labeling a verse as "
                                           "being IN Aramaic"),
                                  "ref": m.group(0), "context": ctx[:160]})
    print(json.dumps({"flag_count": len(flags), "flags": flags,
                      "status": "GREEN" if not flags else "FLAGS"},
                     ensure_ascii=False, indent=1))
    return 1 if flags else 0


if __name__ == "__main__":
    raise SystemExit(main())
