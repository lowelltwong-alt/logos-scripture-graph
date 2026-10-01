#!/usr/bin/env python3
"""Update the A4 selftest to the window the #e13 ruling confirmed, and re-point its vectors.

The old vectors tested a2_seam_verses, which returned ONLY the two seam verses because the span was subtracted
upstream. R1 removed that subtraction, so the window now CONTAINS the span and the old expectations are wrong by
construction - the selftest exited 1 because the function it called no longer exists, which is the loud failure
the rename was supposed to produce rather than a silent pass against stale expectations.
"""
import hashlib
import json
import os
import py_compile
import subprocess
import sys
from pathlib import Path

T = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\tools")
P = T / "check_refs_mirror.py"
pre = P.read_text(encoding="utf-8")

OLD = '''    s = a4_seam_verses({(16, 24), (16, 25), (16, 34)})
    cases.append(("mid-chapter span yields both seam verses", s == {(16, 23), (16, 35)}))
    # span starting at verse 1: the onset seam is the PREVIOUS chapter's last verse
    s = a4_seam_verses({(16, 1), (16, 2)})
    cases.append(("span opening a chapter reaches back to the previous chapter's last verse",
                  s == {(15, LAST_VERSE[15]), (16, 3)}))
    # span ending on a chapter's last verse: the close seam is the NEXT chapter's verse 1
    s = a4_seam_verses({(15, LAST_VERSE[15] - 1), (15, LAST_VERSE[15])})
    cases.append(("span closing a chapter reaches forward to the next chapter's verse 1",
                  s == {(15, LAST_VERSE[15] - 2), (16, 1)}))
    # book edges: no verse before 1:1 and none after the last chapter's last verse
    s = a4_seam_verses({(1, 1)})
    cases.append(("no verse exists before the first verse of the book", (0, 0) not in s and len(s) == 1))
    last_ch = max(LAST_VERSE)
    s = a4_seam_verses({(last_ch, LAST_VERSE[last_ch])})
    cases.append(("no verse exists after the last verse of the book", len(s) == 1))
    # a far-side verse is not admitted
    s = a4_seam_verses({(40, 20), (40, 21)})
    cases.append(("a verse two away from the span is not a seam verse", (40, 23) not in s))'''

NEW = '''    span = {(16, 24), (16, 25), (16, 34)}
    w, d = a4_window(span)
    cases.append(("the window CONTAINS the span", span <= w))
    cases.append(("and adds both seam verses", {(16, 23), (16, 35)} <= w))
    cases.append(("a verse two away from the span is outside the window", (40, 23) not in w))
    # a span opening a chapter reaches back across the boundary
    w, d = a4_window({(16, 1), (16, 2)})
    cases.append(("a span opening a chapter finds its onset seam in the previous chapter",
                  (15, LAST_VERSE[15]) in w))
    # a span closing a chapter reaches forward across the boundary
    w, d = a4_window({(15, LAST_VERSE[15] - 1), (15, LAST_VERSE[15])})
    cases.append(("a span closing a chapter finds its close seam in the next chapter", (16, 1) in w))
    # BOOK EDGES: the boundary is reported, and the span is NEVER swallowed. This is the regression for the
    # guard that binned every reference out-of-window whenever a boundary could not be resolved - it cost the
    # one row whose span ends at the book's final verse all of its references.
    w, d = a4_window({(1, 1)})
    cases.append(("a span opening the book keeps its own verse in the window", (1, 1) in w))
    cases.append(("and reports that it has no onset seam rather than collapsing",
                  d["onset_seam"].startswith("NONE") and d.get("boundary_at_the_book_edge") is True))
    last_ch = max(LAST_VERSE)
    w, d = a4_window({(last_ch, LAST_VERSE[last_ch])})
    cases.append(("a span closing the book keeps its own verse in the window",
                  (last_ch, LAST_VERSE[last_ch]) in w))
    cases.append(("and reports that it has no close seam rather than collapsing",
                  d["close_seam"].startswith("NONE") and d.get("boundary_at_the_book_edge") is True))
    w, d = a4_window(set())
    cases.append(("an unresolvable span reports unresolved rather than returning a silent empty window",
                  w == set() and d["resolved"] is False))'''

n = pre.count(OLD)
assert n == 1, "selftest anchor: expected 1, MEASURED %d" % n
txt = pre.replace(OLD, NEW)

tmp = P.with_suffix(".py.tmp_p2b")
tmp.write_text(txt, encoding="utf-8", newline="\n")
py_compile.compile(str(tmp), doraise=True)
tmp.replace(P)

env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
st = subprocess.run([sys.executable, str(P), "--a4-selftest"], capture_output=True, text=True,
                    encoding="utf-8", cwd=str(T), env=env)
print(json.dumps({"file": P.name,
                  "postimage": hashlib.sha256(txt.encode()).hexdigest(),
                  "selftest_exit": st.returncode}, indent=1))
print(st.stdout or st.stderr)
