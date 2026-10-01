#!/usr/bin/env python3
"""Replace reconcile.py's sentence-level position binding with ADJACENT binding, plus a regression fixture.

THE DEFECT. A position word ("verse-final", "mid-verse") was bound to EVERY verse reference in its sentence. Lane B's
P03-015 sentence "the utterance formula there is genuinely verse-final, unlike its four non-final recurrences
elsewhere in MT 18 (18:3, 18:23, 18:30, 18:32)" therefore bound "verse-final" to 18:3 and the rest, while lane A's
"mid-verse recurrences ... (18:3, ...)" bound "mid-verse" to them, and the reader reported four CONFLICTs where the two
lanes say the same thing.

THE RULE NOW. A position word binds to a verse only when the two are ADJACENT: the verse reference ends within 40
characters BEFORE the word with no other verse reference between, or the word is followed within 30 characters by
"at/in/on <verse>". "non-final" and "not verse-final" read as mid-verse. Everything else is UNBOUND - counted and
published, never guessed - because a wrong binding manufactures a conflict and a missing one only loses a comparison.
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "reconcile.py"
s = P.read_text(encoding="utf-8")

old = '''    positions = set()
    for s in SENT.split(t):
        vs = ["%s:%s" % (m.group(1), m.group(2)) for m in VERSE.finditer(s)]
        for p in POSITION.finditer(s):
            kind = "verse-final" if "final" in p.group(1).lower() else "mid-verse"
            for v in vs:
                positions.add((v, kind))'''
new = '''    # ADJACENT BINDING ONLY (see patch_position_arm.py): a position word binds to a verse reference that ends within
    # 40 characters before it with no other reference between, or to "at/in/on <verse>" within 30 characters after.
    positions, unbound = set(), 0
    refs = [(m.start(), m.end(), "%s:%s" % (m.group(1), m.group(2))) for m in VERSE.finditer(t)]
    for p in POSITION_ANY.finditer(t):
        word = p.group(0).lower()
        kind = "mid-verse" if ("mid" in word or "non" in word or "not" in word) else "verse-final"
        bound = None
        after = AFTER_REF.match(t, p.end())
        if after:
            bound = "%s:%s" % (after.group(1), after.group(2))
        else:
            before = [r for r in refs if r[1] <= p.start() and p.start() - r[1] <= 40]
            if before:
                last = before[-1]
                if not any(last[1] <= r[0] < p.start() for r in refs if r is not last):
                    bound = last[2]
        if bound:
            positions.add((bound, kind))
        else:
            unbound += 1'''
assert s.count(old) == 1, "position block not found exactly once"
s = s.replace(old, new)

old_ret = '''            "positions": positions, "hebrew": heb, "sentences": sentences, "grade": grade}'''
new_ret = '''            "positions": positions, "positions_unbound": unbound, "hebrew": heb, "sentences": sentences,
            "grade": grade}'''
assert s.count(old_ret) == 1
s = s.replace(old_ret, new_ret)

anchor = 'POSITION = re.compile(WB + "(verse-final|verse final|mid-verse|mid verse)" + WB, re.I)'
assert s.count(anchor) == 1
s = s.replace(anchor, anchor + '''
POSITION_ANY = re.compile(WB + "(?:not verse-final|non-final|verse-final|verse final|mid-verse|mid verse)" + WB, re.I)
AFTER_REF = re.compile(r"[^.;]{0,30}?" + WB + "(?:at|in|on)" + r"\\s+(?:oshb:|web:)?(?:Ezek\\.)?(\\d{1,2})[:.](\\d{1,3})")''')

old_fx = '''    cases = [("A vs A has no divergence", compare("t", base, same, same), "CONVERGENT"),'''
new_fx = '''    p15_a = dict(base, boundary_rationale=base["boundary_rationale"] + " The fused row was not taken because the "
                 "utterance formula there is genuinely verse-final, unlike its mid-verse recurrences elsewhere in MT 18 "
                 "(18:3, 18:23, 18:30, 18:32).")
    p15_b = dict(base, boundary_rationale=base["boundary_rationale"] + " The fused row was not taken because the "
                 "utterance formula there is genuinely verse-final, unlike its four non-final recurrences elsewhere in "
                 "MT 18 (18:3, 18:23, 18:30, 18:32).")
    cases = [("A vs A has no divergence", compare("t", base, same, same), "CONVERGENT"),
             ("REGRESSION P03-015: 'mid-verse recurrences' vs 'non-final recurrences' over one verse list is NOT a "
              "conflict", compare("t", base, p15_a, p15_b), "CONVERGENT"),'''
assert s.count(old_fx) == 1
s = s.replace(old_fx, new_fx)

P.write_text(s, encoding="utf-8", newline="\n")
print("patched; backspace bytes:", P.read_bytes().count(bytes([8])))
