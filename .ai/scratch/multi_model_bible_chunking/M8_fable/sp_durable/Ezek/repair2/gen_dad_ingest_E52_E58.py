#!/usr/bin/env python3
"""Build dad_ingest_E52_E58.py from the E-38..E-51 harness: the harness's logic is kept byte-for-byte, its records
block is replaced by dad_records_E52_E58.py, and six exact identifiers are re-pointed. Every replacement must match
exactly once, or nothing is written. Deterministic; --check compares instead of writing."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "dad_ingest_E38_E51.py"
RECS = HERE / "dad_records_E52_E58.py"
OUT = HERE / "dad_ingest_E52_E58.py"

REPL = [
    ('"""Route the M8 error-ledger delta E-38..E-51 + OW-21..OW-24 into the DAD lesson intake.',
     '"""Route the M8 error-ledger delta E-52..E-58 + OW-25..OW-30 into the DAD lesson intake.\n\n'
     'Built by gen_dad_ingest_E52_E58.py from dad_ingest_E38_E51.py: same logic, new records and identifiers.'),
    ('with_name("dad_ingest_E38_E51.result.json")', 'with_name("dad_ingest_E52_E58.result.json")'),
    ('with_name("dad_ingest_E38_E51.scan.json")', 'with_name("dad_ingest_E52_E58.scan.json")'),
    ('TASK = ("Route M8_fable error-ledger delta E-38..E-51 plus OW-21..OW-24 from ERROR_PATTERN_LEDGER.v1.md into the "',
     'TASK = ("Route M8_fable error-ledger delta E-52..E-58 plus OW-25..OW-30 from ERROR_PATTERN_LEDGER.v1.md into the "'),
    ('    new_ids = [f"E-{n}" for n in range(38, 52)] + ["OW-21", "OW-22", "OW-23", "OW-24"]',
     '    new_ids = [f"E-{n}" for n in range(52, 59)] + [f"OW-{n}" for n in range(25, 31)]'),
    ('result = dict(date="2026-09-22",', 'result = dict(date="2026-09-23",'),
]
HEAD_OLD_START = "HEADINGS = {\n"
HEAD_NEW = ('HEADINGS = {\n'
            '    **{f"E-{n}": f"## E-{n} (" for n in range(52, 59)},\n'
            '    **{f"OW-{n}": f"## OWNER DIRECTIVE OW-{n} " for n in range(25, 30)},\n'
            '    "OW-30": "## OW-30 (",\n'
            '}\n')


def build():
    t = SRC.read_text(encoding="utf-8")
    for old, new in REPL:
        if t.count(old) != 1:
            raise SystemExit("REFUSED: anchor found %d times: %r" % (t.count(old), old[:70]))
        t = t.replace(old, new)
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
        OUT.write_text(text, encoding="utf-8", newline="\n")
        print("written", OUT.name, len(text))
