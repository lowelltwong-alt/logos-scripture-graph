#!/usr/bin/env python3
"""Derive step 6's landing, merge and adjudication-brief tools from step 5's, by exact-count replacements.

A copy with a generic step5->step6 rename would silently point the gate at a file that does not exist in step6/ and
pin a rule-substance file step 6 does not have; those references are rewritten explicitly first, each asserted to
occur the expected number of times, and the renamed tool is refused if any 'step5' reference survives unintended.
"""
from pathlib import Path

S5 = Path(__file__).resolve().parent.parent / "step5"
S6 = Path(__file__).resolve().parent


def derive(name, specific, keep_step5_refs=()):
    s = (S5 / name).read_text(encoding="utf-8")
    for old, new, count in specific:
        n = s.count(old)
        if n != count:
            raise SystemExit("REFUSED: %s: %r occurs %d times, expected %d" % (name, old[:70], n, count))
        s = s.replace(old, new)
    # the keep marker must contain nothing the rename below rewrites (a first version used 'STEP5KEEP' and the rename
    # turned it into 'STEP6KEEP', leaving the marker's control bytes in the output)
    MARK = "@@KEEP_FIVE@@"
    for keep in keep_step5_refs:
        s = s.replace(keep, keep.replace("step5", MARK))
    s = s.replace("register_prose", "transport_and_routed").replace("STEP5", "STEP6").replace("step5", "step6") \
         .replace("step-5", "step-6").replace("Step 5", "Step 6").replace("STEP 5", "STEP 6")
    s = s.replace(MARK, "step5")
    if "\x00" in s or MARK in s:
        raise SystemExit("REFUSED: %s: marker residue in the derived tool" % name)
    out = S6 / name.replace("step5", "step6")
    out.write_text(s, encoding="utf-8", newline="\n")
    print("wrote", out.name)


derive("land_lane.py", [])
derive("land_adjudication.py", [])
derive("merge_halves.py", [])
derive("build_step5_adjudication_brief.py", [
    ('(HERE / "check_candidate_v5.py", "YOUR GATE (v5)"),',
     '(EZ / "repair2" / "step5" / "check_candidate_v5.py", "YOUR GATE (v5, run with the step-6 worklist)"),', 1),
    ('(HERE / "step5_rule_substance.v1.json", "the substance of every barred rule id, verbatim"),',
     '(HERE / "step6_substance.v1.json", "the substance this step applies, verbatim from the records that define it"),', 1),
    ('(EZ / "ezek_controlling_agent_ruling_e15.v1.json", "the ruling: q9_section8_register governs"),',
     '(EZ / "ezek_controlling_agent_ruling_e15.v1.json", "the ruling: q8_transport_class governs the transport items, q9 the register items"),', 1),
    ("`python -B <SP>\\Ezek\\repair2\\step5\\check_candidate_v5.py %(deliv)s\\proposal.json --work %(deliv)s\\gate_work --discharge %(deliv)s\\adjudication.json`",
     "`python -B <SP>\\Ezek\\repair2\\step5\\check_candidate_v5.py %(deliv)s\\proposal.json --work %(deliv)s\\gate_work --discharge %(deliv)s\\adjudication.json --worklist <SP>\\Ezek\\repair2\\step6\\step6_worklist.v1.json`", 1),
    ("OF TWO BLIND PROSE LANES", "OF TWO BLIND AUTHOR LANES", 1),
    ("the register prose pass on this half", "the transport batch, the routed repairs and the register items on this half", 1),
    ("Change no claim; no grade, span, identity, signals or refs change.",
     "Change no claim beyond an item's order; refs change only where an item names them, each entry passing the gate's form; no grade, span, identity or signals change. RE-MEASURE every routed claim before adopting a repair of it. No grade moves in this step.", 1),
], keep_step5_refs=('"repair2" / "step5" / "check_candidate_v5.py"', "\\repair2\\step5\\check_candidate_v5.py"))
