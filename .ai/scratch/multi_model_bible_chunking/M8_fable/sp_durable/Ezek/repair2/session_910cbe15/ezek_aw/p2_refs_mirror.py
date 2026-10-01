#!/usr/bin/env python3
r"""Precondition P2 of the #e13 ruling: fix refs_mirror, then run it once.

THE RULING (R1): "CONFIRMED: the window contains the span; E13-02/19 withdrawn as inferences; own_span
subtraction removed; range = one citation; zone-aware MT face; guards fail LOUD; worklist = fixed member union
the peers' hand-named in-window verses."

THE DEFECT CHAIN THIS CLOSES, all of it found by peers:
  * The member computed missing = argued - covered - own_span. Subtracting the span made an argued-but-unmirrored
    verse INSIDE the span invisible BY CONSTRUCTION. Four peers measured that class independently - 9, 8, 7 and
    12 verses - and one of them traced a flagged mark gap to it: a row's own CLOSE verse was missing from its own
    reference list, so the mark had nothing to attach to.
  * Because everything left was outside the span, A4's window reduced to two seam verses which A4's own far-side
    clause then barred, which is why three peers reported the member yielding no per-row finding at all. I
    recorded that as "A4 can never yield a per-row finding" THREE TIMES, and it was true of the member and false
    of the rule. Removing the subtraction is what makes the rule operable.
  * My A4 filter admitted only the two seam verses, which was right while the span was subtracted and is wrong
    now. The window is the span PLUS both seams.
  * The guard binned every reference out-of-window whenever either boundary could not be resolved, so the one row
    whose span ends at the book's final verse lost all of its references silently. Guards now fail LOUD.

ZONE-AWARE FACE: verse_inventory.json now declares "numbering_face": "WEB" (precondition P1). This asserts that
declaration rather than inferring it, and the module already compares in WEB space with MT-side tokens converted
through the crosswalk, which is the zone-awareness the ruling asks for.
"""
import hashlib
import json
import os
import py_compile
import subprocess
import sys
from pathlib import Path

T = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\tools")
EZ = T.parent
P = T / "check_refs_mirror.py"

pre = P.read_text(encoding="utf-8")
txt = pre
edits = []


def sub(label, old, new, expect=1):
    global txt
    n = txt.count(old)
    assert n == expect, "%s: expected %d, MEASURED %d" % (label, expect, n)
    txt = txt.replace(old, new)
    edits.append({"edit": label, "expected": expect, "measured": n})


# ---- 1. the window is the span plus both seams, and a missing boundary is LOUD
OLD_W = '''def a4_seam_verses(own_span):
    """The two verses A4 admits as defect candidates: the onset seam and the close seam.

    The row's own span is already subtracted from `missing` upstream, so the window
    [first-1, last+1] reduces to exactly these two verses. Returns a set, possibly smaller
    than 2 at the book's edges, where the adjacent verse does not exist.
    """
    if not own_span:
        return set()
    ordered = sorted(own_span)
    out = set()
    for v in (_prev_verse(*ordered[0]), _next_verse(*ordered[-1])):
        if v is not None:
            out.add(v)
    return out'''
NEW_W = '''def a4_window(own_span):
    """A4's window: the row's whole span PLUS the onset-seam verse and the close-seam verse.

    #e13 R1 removed the own_span subtraction upstream, so the window is no longer reducible to the two
    seam verses - it CONTAINS the span, which is what makes an in-span argued-but-unmirrored verse a
    defect the member can see. Four peers measured that class by hand while the member could not reach it.

    Returns (window, diagnostics). A boundary that does not exist - the book's first or last verse has no
    neighbour - is reported in the diagnostics and NEVER silently collapses the window: the previous guard
    binned every reference out-of-window whenever either boundary was unresolvable, which cost the one row
    whose span ends at the book's final verse all of its references.
    """
    if not own_span:
        return set(), {"resolved": False, "why": "the row has no resolvable span"}
    ordered = sorted(own_span)
    lo, hi = _prev_verse(*ordered[0]), _next_verse(*ordered[-1])
    win = set(ordered)
    diag = {"resolved": True, "span_verses": len(ordered),
            "onset_seam": ("Ezek.%d.%d" % lo) if lo else "NONE - the span opens the book",
            "close_seam": ("Ezek.%d.%d" % hi) if hi else "NONE - the span closes the book"}
    if lo is not None:
        win.add(lo)
    if hi is not None:
        win.add(hi)
    if lo is None or hi is None:
        diag["boundary_at_the_book_edge"] = True
    return win, diag'''
sub("window contains the span, and a book-edge boundary is reported not swallowed", OLD_W, NEW_W)

# ---- 2. drop the own_span subtraction and classify against the new window
OLD_M = '''            missing = sorted(argued - covered(row) - own_span)
            # A4 (#e12 ruling): only a verse inside [first-1, last+1] is a defect. The row's own span is
            # already subtracted above, so that window reduces to the two seam verses. Range expansions
            # and comparison verses outside it are NOT defects and move to far_side_refs, where the
            # information survives without being scored.
            seams = a4_seam_verses(own_span)
            in_window = [p for p in missing if p in seams]
            far_side = [p for p in missing if p not in seams]'''
NEW_M = '''            # #e13 R1: own_span is NOT subtracted. An argued verse the reference list omits is a candidate
            # defect whether it lies inside the span or at either seam; only verses OUTSIDE the window are
            # discharged. This is the change that makes the in-span class visible at all.
            missing = sorted(argued - covered(row))
            window, win_diag = a4_window(own_span)
            in_window = [p for p in missing if p in window]
            far_side = [p for p in missing if p not in window]
            in_span = [p for p in in_window if p in own_span]
            at_seam = [p for p in in_window if p not in own_span]'''
sub("own_span subtraction removed; classify in-span and at-seam separately", OLD_M, NEW_M)

# ---- 3. the flag carries the new classification
OLD_F = '''            if in_window:
                flags.append({"file": Path(f).name,
                              "decision_id": row.get("decision_id", "?"),
                              "argued_but_unmirrored": [f"Ezek.{c}.{v}" for c, v in in_window],
                              "window": {"onset_seam": (f"Ezek.{sorted(seams)[0][0]}.{sorted(seams)[0][1]}"
                                                        if seams else None),
                                         "rule": "A4: a defect only inside [first-1, last+1]"}})'''
NEW_F = '''            if in_window:
                flags.append({"file": Path(f).name,
                              "decision_id": row.get("decision_id", "?"),
                              "argued_but_unmirrored": [f"Ezek.{c}.{v}" for c, v in in_window],
                              "in_span": [f"Ezek.{c}.{v}" for c, v in in_span],
                              "at_a_seam": [f"Ezek.{c}.{v}" for c, v in at_seam],
                              "window": dict(win_diag,
                                             rule="A4 as ruled in #e13 R1: the window is the span plus both "
                                                  "seam verses; own_span is not subtracted")})'''
sub("flag carries in-span and at-seam", OLD_F, NEW_F)

# ---- 4. assert the declared face rather than inferring it
OLD_I = "from ezek_lib import (LAST_VERSE, MT_LAST_VERSE, PSALM_RULES, expand_ref_token,"
NEW_I = ('''# #e13 R2: every arithmetic consumer ASSERTS the numbering face it expects. LAST_VERSE is built from
# verse_inventory.json, which previously carried a face and declared none - the silence broke four separate
# adjacency computations in a consumer and could not be detected from inside one.
def _assert_declared_face(expected="WEB"):
    import json as _json
    from pathlib import Path as _P
    inv = _json.loads((_P(__file__).resolve().parent.parent / "verse_inventory.json")
                      .read_text(encoding="utf-8"))
    got = inv.get("numbering_face")
    if got != expected:
        raise SystemExit("REFUSED: this tool does verse arithmetic on the %s face and verse_inventory.json "
                         "declares %r. A face mismatch is the wrong verse, not a rounding error." % (expected, got))


from ezek_lib import (LAST_VERSE, MT_LAST_VERSE, PSALM_RULES, expand_ref_token,''')
sub("declared-face assertion", OLD_I, NEW_I)

sub("call the face assertion at startup", "def main() -> int:\n", "def main() -> int:\n    _assert_declared_face(\"WEB\")\n")

tmp = P.with_suffix(".py.tmp_p2")
tmp.write_text(txt, encoding="utf-8", newline="\n")
py_compile.compile(str(tmp), doraise=True)
tmp.replace(P)

env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
st = subprocess.run([sys.executable, str(P), "--a4-selftest"], capture_output=True, text=True,
                    encoding="utf-8", cwd=str(T), env=env)
run = subprocess.run([sys.executable, str(P), "../repair/rows_v7_cwo24.jsonl"], capture_output=True,
                     text=True, encoding="utf-8", cwd=str(T), env=env)
try:
    rep = json.loads(run.stdout)
    n_in_span = sum(len(f.get("in_span") or []) for f in rep["flags"])
    n_seam = sum(len(f.get("at_a_seam") or []) for f in rep["flags"])
    summary = {"rows_checked": rep.get("rows_checked"), "flag_count": rep.get("flag_count"),
               "in_span_verses": n_in_span, "at_seam_verses": n_seam,
               "far_side_rows": rep.get("far_side_ref_rows"), "far_side_verses": rep.get("far_side_ref_count"),
               "rows_with_an_in_span_defect": sorted({f["decision_id"] for f in rep["flags"] if f.get("in_span")})}
except Exception:
    summary = {"raw": ((run.stdout or "") + (run.stderr or ""))[-700:]}

print(json.dumps({"precondition": "P2", "file": P.name,
                  "preimage": hashlib.sha256(pre.encode()).hexdigest(),
                  "postimage": hashlib.sha256(txt.encode()).hexdigest(),
                  "edits": edits, "compiles": True,
                  "a4_selftest_exit": st.returncode,
                  "fixed_member_run": summary}, indent=1, ensure_ascii=False))
