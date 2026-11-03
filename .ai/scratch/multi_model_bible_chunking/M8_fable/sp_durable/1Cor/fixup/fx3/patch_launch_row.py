"""One-shot: adds the FIXUP-3 lanes to review/append_review_launch_row.py before its --lane argument. Refuses a second run."""
from pathlib import Path

p = Path(__file__).resolve().parents[2] / "review/append_review_launch_row.py"
s = p.read_bytes().decode("utf-8")
anchor = 'ap.add_argument("--lane", dest="part", required=True, choices=sorted(PARTS))'
if s.count(anchor) != 1 or "FX3_W" in s:
    raise SystemExit("REFUSED: anchor count %d" % s.count(anchor))
add = '''for _n in ("W1", "W2", "W3", "W4", "W5", "W6"):
    _p = "FX3_" + _n
    PARTS[_p] = ("cor_fixup3_%s_a1" % _n, "fixup3:" + _n,
                 "1 Corinthians FIXUP-3 author for part %s: carries out the round-4 rulings' orders to that part, CWO-1COR-06 and "
                 "-07 and, for W4, S3-01 (claude-opus-5-5 on grader_fallback, OW-25). Writes in OUT only" % _n)
    OUTDIR[_p] = "cor_fx3\\\\" + _n
    BRIEFNAME[_p] = "FIXUP3_BRIEF_" + _n
    PRODUCER[_p] = "this lane (1 Corinthians FIXUP-3 author, part %s, claude-opus-5-5 on grader_fallback, OW-25)" % _n
    CATCHER[_p] = ("the orchestrator's landing check (fixup/fx3/land_fixup3.py: changed fields against the licence, suite, ngram7, "
                   "tiling and sweep on the applied copy), then S5, a fresh agent on the applied rows")
'''
s = s.replace(anchor, add + anchor)
p.write_bytes(s.encode("utf-8"))
print("patched")
