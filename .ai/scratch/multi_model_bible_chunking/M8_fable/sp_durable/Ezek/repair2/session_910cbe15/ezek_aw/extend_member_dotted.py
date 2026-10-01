#!/usr/bin/env python3
"""Extend the A4 member to read a DOTTED CONTINUATION of a citation list, under guarded mutation.

THE GAP (queue E13-77, ledger E-33): the member's patterns are an OSIS token, a bare C:V cite with a colon, an
"MT C:V" qualifier and a v./vv. expression. A dotted continuation - `20.14` in
"oshb:Ezek.20.9, 20.14 and 20.22" - matches none of them, so the member took the first member of such a list and
dropped the rest. Measured: 53 argued, in-window, unmirrored citations on 22 rows invisible to it. The
controlling agent's independent recount shares the blind spot, because both implementations read the same
enumeration of forms.

THE READING I AM IMPLEMENTING, and it is disclosed rather than assumed. DEF-A4-ARGUED clause 1 opens "Any verse
anchor a prose field carries" and then names four forms; clause 2 makes a comma/"and" list one citation PER
MEMBER. The governing phrase is the first, the four forms illustrate it, and a three-verse list is three
citations whatever the members' spelling. So this implements clause 1's rule rather than extending it. The
reading is routed to the controlling agent either way, because an incomplete Tier-0 gate is red at the close and
over-disclosing an interpretation is the cheaper error.

THE PREDICATE IS DELIBERATELY NARROW. A dotted pair is read as a citation ONLY where an OSIS-style token
appears EARLIER IN THE SAME STRING - that is what makes it a continuation of a list rather than a decimal, a
version number or a figure. Two fixtures pin both sides: the three-member list must yield three citations, and a
bare decimal in prose must yield none.
"""
import hashlib
import json
import py_compile
import shutil
import subprocess
import sys
from pathlib import Path

TOOLS = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable"
             r"\sp_durable\Ezek\tools")
SRC = TOOLS / "check_refs_mirror.py"
PIN = "343d03cbaa982357ebfe9c0d62c3537dd7c889a786e0a0e0469b88ebcff73a2e"
HERE = Path(__file__).resolve().parent

pre = SRC.read_bytes()
got = hashlib.sha256(pre).hexdigest()
if got != PIN:
    raise SystemExit("REFUSED: preimage is %s, expected %s" % (got, PIN))
text = pre.decode("utf-8")
(HERE / "check_refs_mirror.preimage_343d03cb.py").write_bytes(pre)

edits = []

# ---- 1. the pattern and its expander
ANCHOR = "def parse_verse_expr_groups(expr: str) -> list[tuple[frozenset, str]]:"
NEW_BLOCK = '''# A DOTTED CONTINUATION of an OSIS-style list: the "20.14" in "oshb:Ezek.20.9, 20.14 and 20.22".
# DEF-A4-ARGUED clause 1's governing phrase is "any verse anchor a prose field carries" and clause 2 makes a
# comma/"and" list one citation PER MEMBER, so a three-verse list is three citations whatever the members'
# spelling. The member could see only the first, which cost 53 in-window unmirrored citations on 22 rows
# (ledger E-33). NARROW BY DESIGN: a dotted pair counts only where an OSIS token stands EARLIER IN THE SAME
# STRING, which is what distinguishes a list continuation from a decimal, a version number or a figure.
DOTTED_CONT = re.compile(r"(?<![\\w.])(\\d{1,3})\\.(\\d{1,3})(?![\\d.])")
OSIS_EARLIER = re.compile(r"(?:oshb:|web:)?Ezek\\.\\d+\\.\\d+")


def dotted_continuation_refs(s: str) -> set[tuple[int, int]]:
    """WEB-space verses named by dotted continuations of an OSIS list in this string.

    The witness prefix of the list's LAST explicit OSIS token governs the continuation, exactly as it does
    inside one entry (the OL-c18 rule): "oshb:Ezek.20.9, 20.14" means MT 20:14, not WEB 20:14, and MT and WEB
    diverge in chs 20-21 - which is precisely where this corpus's longest such lists sit.
    """
    out: set[tuple[int, int]] = set()
    for m in DOTTED_CONT.finditer(s):
        before = s[:m.start()]
        toks = list(OSIS_EARLIER.finditer(before))
        if not toks:
            continue
        is_oshb = "oshb:" in before[max(0, toks[-1].start() - 6):toks[-1].end()]
        c, v = int(m.group(1)), int(m.group(2))
        space = MT_LAST_VERSE if is_oshb else LAST_VERSE
        if c not in space or not (1 <= v <= space[c]):
            continue
        out.update(mt_to_web_all(c, v) if is_oshb else [(c, v)])
    return out


def dotted_continuation_citations(s: str, field: str) -> list[dict]:
    """One citation per dotted continuation; each is its own list member under clause 2."""
    out = []
    for m in DOTTED_CONT.finditer(s):
        before = s[:m.start()]
        toks = list(OSIS_EARLIER.finditer(before))
        if not toks:
            continue
        is_oshb = "oshb:" in before[max(0, toks[-1].start() - 6):toks[-1].end()]
        c, v = int(m.group(1)), int(m.group(2))
        space = MT_LAST_VERSE if is_oshb else LAST_VERSE
        if c not in space or not (1 <= v <= space[c]):
            continue
        pairs = list(mt_to_web_all(c, v)) if is_oshb else [(c, v)]
        cit = _cite(pairs, m.group(0), field, "dotted_continuation")
        if cit:
            out.append(cit)
    return out


'''
edits.append(("the dotted-continuation pattern, expander and citation emitter", ANCHOR,
              NEW_BLOCK + ANCHOR, 1))

# ---- 2. wire it into both arms
edits.append(("prose_refs reads dotted continuations",
              "            out.update(verse_word_refs(o, span_chapters))",
              "            out.update(verse_word_refs(o, span_chapters))\n"
              "            out.update(dotted_continuation_refs(o))", 1))
edits.append(("string_citations reads dotted continuations",
              """    if len(span_chapters) == 1:
        (ch,) = span_chapters
        for m in VERSE_WORD.finditer(s):""",
              """    out.extend(dotted_continuation_citations(s, field))
    if len(span_chapters) == 1:
        (ch,) = span_chapters
        for m in VERSE_WORD.finditer(s):""", 1))

# ---- 3. two fixtures, one per side
edits.append(("fixtures for the dotted continuation and the decimal that must NOT match",
              "    # ---- the regrouping invariant, on the expression parser directly",
              '''    # ---- the dotted continuation (ledger E-33), both sides
    row_g = {"decision_id": "FIXTURE-G", "span": "Ezek.20.1-Ezek.20.44",
             "boundary_evidence_refs": ["web:Ezek.20.9"],
             "rationale": "the for-my-name's-sake clauses at oshb:Ezek.20.9, 20.14 and 20.22"}
    rg = analyze_row(row_g, "fixture")
    cases.append(("E-33 a dotted continuation of an OSIS list is read as its own citation",
                  rg["citations_read"] == 3))
    cases.append(("E-33 and the two unmirrored members reach the worklist",
                  len([i for i in rg["items"] if i["kind"] == "single"]) >= 2))
    row_h = {"decision_id": "FIXTURE-H", "span": "Ezek.20.1-Ezek.20.44",
             "boundary_evidence_refs": [],
             "rationale": "the ratio is 20.14 percent and no verse is named here"}
    cases.append(("E-33 a bare decimal with NO OSIS token earlier in the string is NOT a citation",
                  analyze_row(row_h, "fixture")["citations_read"] == 0))

    # ---- the regrouping invariant, on the expression parser directly''', 1))

new = text
for desc, old, rep, want in edits:
    n = new.count(old)
    if n != want:
        raise SystemExit("REFUSED: %r occurs %d times, expected %d" % (desc, n, want))
    new = new.replace(old, rep, want)
    print("  edit OK  %s" % desc)

STAGE = HERE / "check_refs_mirror.candidate2.py"
STAGE.write_text(new, encoding="utf-8", newline="\n")
py_compile.compile(str(STAGE), doraise=True)
print("  py_compile OK")

tmp = SRC.with_suffix(".py.tmpE33")
shutil.copy2(STAGE, tmp)
tmp.replace(SRC)
post = hashlib.sha256(SRC.read_bytes()).hexdigest()
sel = subprocess.run([sys.executable, str(SRC), "--a4-selftest"], capture_output=True, text=True,
                     cwd=str(TOOLS), encoding="utf-8", errors="replace")
print(sel.stdout[-1400:])
print(json.dumps({"preimage": PIN, "postimage": post, "selftest_exit": sel.returncode,
                  "backup": "check_refs_mirror.preimage_343d03cb.py"}, indent=1))
if sel.returncode != 0:
    raise SystemExit("REFUSED: selftest failed; the preimage backup is beside this script")
