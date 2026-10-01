#!/usr/bin/env python3
"""Build dad_ingest_E66_E67.py from the E-59..E-65 harness: the harness's logic is kept byte-for-byte, its records
block is replaced by dad_records_E66_E67.py, and five exact identifiers are re-pointed. Every replacement must match
exactly once, or nothing is written. Deterministic; --check compares instead of writing."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "dad_ingest_E59_E65.py"
RECS = HERE / "dad_records_E66_E67.py"
OUT = HERE / "dad_ingest_E66_E67.py"

REPL = [
    ('"""Route the M8 error-ledger delta E-59..E-65 into the DAD lesson intake.\n\n'
     'Built by gen_dad_ingest_E59_E65.py from dad_ingest_E52_E58.py: same logic, new records and identifiers.',
     '"""Route the M8 error-ledger delta E-66..E-67 into the DAD lesson intake.\n\n'
     'Built by gen_dad_ingest_E66_E67.py from dad_ingest_E59_E65.py: same logic, new records and identifiers.'),
    ('with_name("dad_ingest_E59_E65.result.json")', 'with_name("dad_ingest_E66_E67.result.json")'),
    ('with_name("dad_ingest_E59_E65.scan.json")', 'with_name("dad_ingest_E66_E67.scan.json")'),
    ('TASK = ("Route M8_fable error-ledger delta E-59..E-65 from ERROR_PATTERN_LEDGER.v1.md into the "',
     'TASK = ("Route M8_fable error-ledger delta E-66..E-67 from ERROR_PATTERN_LEDGER.v1.md into the "'),
    ('    new_ids = [f"E-{n}" for n in range(59, 66)]',
     '    new_ids = [f"E-{n}" for n in range(66, 68)]'),
]
HEAD_OLD_START = "HEADINGS = {\n"
HEAD_NEW = ('HEADINGS = {\n'
            '    **{f"E-{n}": f"## E-{n} (" for n in range(66, 68)},\n'
            '}\n')


def build():
    t = SRC.read_text(encoding="utf-8")
    for old, new in REPL:
        if t.count(old) != 1:
            raise SystemExit("REFUSED: anchor found %d times: %r" % (t.count(old), old[:70]))
        t = t.replace(old, new)
    if t.count(HEAD_OLD_START) != 1:
        raise SystemExit("REFUSED: HEADINGS block found %d times" % t.count(HEAD_OLD_START))
    a = t.index(HEAD_OLD_START)
    b = t.index("\n}\n", a) + 3
    t = t[:a] + HEAD_NEW + t[b:]
    lines = t.split("\n")
    starts = [i for i, l in enumerate(lines) if l.startswith("rec(")]
    end = [i for i, l in enumerate(lines) if l.startswith("SPLIT = re.compile")]
    if not starts or len(end) != 1 or starts[-1] > end[0]:
        raise SystemExit("REFUSED: could not bound the records block")
    body = RECS.read_text(encoding="utf-8").rstrip("\n").split("\n")
    lines = lines[:starts[0]] + body + ["", ""] + lines[end[0]:]
    return "\n".join(lines)


if __name__ == "__main__":
    text = build()
    if "--check" in sys.argv:
        print("MATCH" if OUT.is_file() and OUT.read_text(encoding="utf-8") == text else "DIFFERS")
    else:
        if OUT.exists():
            raise SystemExit("REFUSED: %s exists; use --check" % OUT.name)
        OUT.write_text(text, encoding="utf-8", newline="\n")
        print("written", OUT.name, len(text))
