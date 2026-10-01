#!/usr/bin/env python3
"""Fix two WRONG ASSUMPTIONS in my lane validator. Both flagged a lane for something the brief never required.

ASSUMPTION 1: that sweep == "a4" implies op == "append_ref". Lane 06 needed a `set` with a LIST value on two
rows, because an ordered quotation repair falls INSIDE an existing reference entry while citation entries must
also be added to the same field - so one edit legitimately rewrites the whole list. My validator read the list
as a string, found two role tokens in it, and called the edit malformed. It is not: it adds three entries, two
carrying a citation's ROLE token and one being the quotation repair, which is not a citation install and
correctly carries no token.

  The fix: check role tokens on append_ref values, and on the NEW entries of a set-on-refs edit. An entry
  without a token is reported as "no token - verify it is a quotation repair rather than a missed citation
  token", which is a question for a reader, not a verdict.

ASSUMPTION 2: that no annotation may repeat. My brief says "at least 4 distinct formulations per annotation
type, at most 6 words". Lane 06 has 8 distinct formulations across 11 paseq annotations, which MEETS that floor.
My validator invented an all-distinct rule the brief does not state and then reported the lane as non-compliant.

  The fix: measure the floor the brief actually sets, and report repeats as INFORMATION - with the 7-gram risk
  named, because a repeated annotation preceded by the same token can form a duplicated 7-word sequence and the
  validator suite's duplicate gate is the thing that can actually measure that. A risk worth measuring is not
  the same as a rule already broken.

THE PATTERN IN BOTH: a check stricter than its rule manufactures defects, and a manufactured defect costs the
same investigation as a real one. This is the mirror image of the under-collection that produced E-32, and it is
the second time this session that a check of mine reported disagreement where there was none.
"""
from pathlib import Path

p = Path("validate_lane.py")
t = p.read_text(encoding="utf-8")

OLD = '''    tok_re = re.compile(r"\\[([A-Za-z-]+)\\]")
    a4 = [e for e in edits if str(e.get("sweep")) == "a4"]
    bad_tokens, annotations = [], []
    for e in a4:
        v = str(e.get("value", ""))
        toks = tok_re.findall(v)
        if len(toks) != 1 or toks[0] not in ROLE_VOCABULARY:
            bad_tokens.append({"row": e.get("row_id"), "value": v[:90], "tokens_found": toks})
        else:
            tail = v.split("]", 1)[1].strip()
            annotations.append((e.get("row_id"), toks[0], tail))
    too_long = [(r, t, a) for r, t, a in annotations if len(a.split()) > 6]
    dupes = [a for a, n in Counter(a for _, _, a in annotations).items() if n > 1 and a]
    per_token = Counter(t for _, t, _ in annotations)'''

NEW = '''    tok_re = re.compile(r"\\[([A-Za-z-]+)\\]")
    a4 = [e for e in edits if str(e.get("sweep")) == "a4"]

    def new_entries(e):
        """The reference entries an edit ADDS. An append_ref adds one string; a set-on-refs replaces the whole
        list, so the additions are the entries not present in expected_before. A lane may need the latter when
        a quotation repair falls inside an existing entry while citation entries are also being added."""
        if e.get("op") == "append_ref":
            return [str(e.get("value", ""))]
        v = e.get("value")
        if isinstance(v, list):
            before = set(e.get("expected_before") or [])
            return [str(x) for x in v if str(x) not in before]
        return [str(v)]

    bad_tokens, untokened, annotations = [], [], []
    for e in a4:
        for v in new_entries(e):
            toks = tok_re.findall(v)
            if not toks:
                # NOT a verdict: a quotation repair carries no citation token and is legitimately untokened
                untokened.append({"row": e.get("row_id"), "entry": v[:110],
                                  "question": "no ROLE token - verify this is a quotation repair rather than a "
                                              "missed citation token"})
            elif len(toks) != 1 or toks[0] not in ROLE_VOCABULARY:
                bad_tokens.append({"row": e.get("row_id"), "entry": v[:110], "tokens_found": toks})
            else:
                annotations.append((e.get("row_id"), toks[0], v.split("]", 1)[1].strip()))
    too_long = [(r, t, a) for r, t, a in annotations if len(a.split()) > 6]
    per_token = Counter(t for _, t, _ in annotations)
    distinct_per_token = {tk: len({a for _, tt, a in annotations if tt == tk}) for tk in per_token}
    # THE FLOOR THE BRIEF ACTUALLY SETS: at least 4 distinct formulations per token where the token has 4 or
    # more entries. Repeats below that are not a breach, and an all-distinct rule is one my validator invented.
    floor_misses = {tk: distinct_per_token[tk] for tk, n in per_token.items()
                    if n >= 4 and distinct_per_token[tk] < 4}
    repeats = [a for a, n in Counter(a for _, _, a in annotations).items() if n > 1 and a]'''

assert t.count(OLD) == 1, "the role-token block did not match exactly"
t = t.replace(OLD, NEW, 1)

OLD2 = '''        "role_tokens": {"a4_edits": len(a4), "malformed": bad_tokens,
                        "distribution": dict(per_token)},
        "rotation_rule": {"annotations": len(annotations), "over_six_words": too_long,
                          "duplicated": dupes,
                          "distinct_formulations_per_token": {t: len({a for _, tt, a in annotations if tt == t})
                                                              for t in per_token}},'''
NEW2 = '''        "role_tokens": {"a4_edits": len(a4), "reference_entries_added": len(annotations) + len(untokened),
                        "malformed": bad_tokens,
                        "untokened_entries_to_verify": untokened,
                        "distribution": dict(per_token)},
        "rotation_rule": {"annotations": len(annotations), "over_six_words": too_long,
                          "distinct_formulations_per_token": distinct_per_token,
                          "tokens_below_the_four_formulation_floor": floor_misses,
                          "repeated_formulations": repeats,
                          "repeats_are_not_a_breach": ("the brief requires at least 4 distinct formulations per "
                                                       "token where the token has 4 or more entries, not that "
                                                       "every formulation be unique. Repeats are reported "
                                                       "because a repeated annotation preceded by the same "
                                                       "token can form a duplicated seven-word sequence; the "
                                                       "validator suite's duplicate gate is what measures "
                                                       "that, and it runs after the apply.")},'''
assert t.count(OLD2) == 1, "the report block did not match exactly"
t = t.replace(OLD2, NEW2, 1)

OLD3 = '''    if bad_tokens:
        problems.append("%d A4 appends carry a malformed or unknown ROLE token" % len(bad_tokens))
    if too_long:
        problems.append("%d annotations exceed six words" % len(too_long))
    if dupes:
        problems.append("%d annotations are duplicated" % len(dupes))'''
NEW3 = '''    if bad_tokens:
        problems.append("%d reference entries carry a malformed or unknown ROLE token" % len(bad_tokens))
    if too_long:
        problems.append("%d annotations exceed six words" % len(too_long))
    if floor_misses:
        problems.append("%d token classes fall below the four-formulation floor with four or more entries: %r"
                        % (len(floor_misses), floor_misses))'''
assert t.count(OLD3) == 1, "the problem block did not match exactly"
t = t.replace(OLD3, NEW3, 1)

# the item_identification block is not universal; accept any mapping-shaped key
t = t.replace('"has_item_identification_block": "item_identification" in d,',
              '"mapping_block_present": [k for k in d if "item_identification" in k or "item_id" in k] or '
              '"NONE - the per-item trace relies on this lane\'s own id scheme, which is my worklist\'s defect '
              'and not the lane\'s",')
p.write_text(t, encoding="utf-8", newline="\n")
print("validator patched: 3 asserted edits, each at exactly one occurrence")
