#!/usr/bin/env python3
"""The DISTINCT CHECK #e15 ordered for the mechanical face sweep - a SECOND, decorrelated derivation.

#e15 Q5: the retro-qualification "runs as a MECHANICAL sweep with a distinct check". A distinct check that
re-ran the same geometry would agree with itself and prove nothing. So this one reads a different signal: the
ANNOTATION'S OWN WORDS. The first derivation knows only (verse, span) and no English; this one knows only
English and never looks at the span. Where they agree the qualifier is corroborated by two independent readers;
where they disagree, the disagreement is the finding and goes to the author batch.

WHY THIS IS THE RIGHT SECOND READER. A sign error in the geometry's previous/next verse would flip every
qualifier at once and stay perfectly self-consistent. Only a reader that does not do the arithmetic can catch
that.

TWO CORRECTIONS TO THIS READER, both disclosed because both changed its result.

(1) ITS FIRST VERSION READ DEIXIS AS A FACE CLAIM and reported 7 disagreements, all 7 its own error. "messenger
names the addressee here", "priestly class changes at this verse" - "here" and "this verse" POINT AT the cited
verse and say nothing about which side of the seam it sits on. The decisive case was P08-012's "a fresh movement
begins past here" at Ezek.36.24, which the reader called near and the geometry called far; #e15 says of that row
"the FAR face, 36:24, carries nothing". The geometry was right. Two interpretation rules replaced the
vocabulary: deixis leaves the face UNSPOKEN, and a verb of starting is read against the seam the token names -
on an ONSET warrant the row's own unit starts at the verse (near), on a CLOSE warrant the NEXT unit starts across
the seam (far). The reader is told which token it reads, which is not a leak: a token name says onset or close
and never says near or far.

(2) ITS SECOND VERSION REPORTED GREEN WHILE MATCHING NOTHING AT ALL. Every word-boundary escape in its patterns
had been turned into a literal BACKSPACE byte by the shell heredoc that wrote the patch - 66 of them - so no
pattern could fire, all 111 entries came back UNSPOKEN, and the verdict line said "GREEN - no disagreement".
Zero disagreements because zero comparisons. That is the third time this campaign has lost a word boundary to a
heredoc, so the rule is now absolute: PATTERNS ARE NEVER WRITTEN THROUGH A SHELL HEREDOC. And because a rule I
have broken three times is not a control, two controls are built in below:
  * a SELFTEST with fixtures, so the patterns are proven to fire before any verdict is computed; and
  * a REFUSAL: a check that corroborates nothing cannot report GREEN. If the words assert a face nowhere, the
    reader is broken or the corpus's annotations are silent, and either way there is no corroboration to
    report. Silence is never a pass.
"""
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAN = HERE / "face_qualification_plan.v1.json"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731

WB = chr(92) + "b"          # a word boundary, built rather than typed, so no writer can mangle it silently


def _pat(*alts):
    """Compile alternatives, each wrapped in word boundaries built from an explicit escape."""
    return re.compile("|".join(WB + "(?:" + a + ")" + WB for a in alts), re.I)


FAR = _pat("far face", "far side", "beyond", "past", "behind", "across the seam",
           "next (?:unit|row|verse)", "following (?:unit|verse)", "the verse after", "the verse before")
NEAR = _pat("near face", "near side", "rests? here", "stands here", "the close rests",
            "opens this (?:unit|row)", "closes this (?:unit|row)", "first verse", "last verse")
INTERIOR = _pat("interior", "in[- ]span", "mid[- ]unit", "partner", "within the (?:unit|row)")
# a verb of starting: the cited verse begins something. Its face depends on WHICH seam the token names.
STARTS = _pat("opens?", "begins?", "resumes?", "changes?", "turn")
# pure pointing, which asserts nothing about a face
DEIXIS = _pat("here", "at this verse", "this verse")


def face_from_words(text, token):
    """Return (face, basis); face is None when the wording asserts no face."""
    if INTERIOR.search(text):
        return ":interior", "an explicit interior word"
    if FAR.search(text):
        return ":far", "an explicit far-side word"
    if NEAR.search(text):
        return ":near", "an explicit near-side word"
    if STARTS.search(text):
        if token == "WARRANT-onset":
            return ":near", "a verb of starting on an ONSET warrant: the row's own unit starts at this verse"
        return ":far", "a verb of starting on a CLOSE warrant: the NEXT unit starts, across the seam"
    if DEIXIS.search(text):
        return None, "deixis only - the wording points at the verse and asserts no face"
    return None, "no face word"


def strip_signals(entry):
    """Remove the role token and the verse reference, so this reader cannot see reader 1's signal."""
    t = re.sub(r"\[[^\]]*\]", " ", entry)
    return re.sub(r"(?:oshb|web):Ezek\.\d+\.\d+", " ", t)


FIXTURES = [
    # (annotation text, token, expected face) - the patterns must FIRE, which is the point of the selftest
    ("far face of the close seam", "WARRANT-close", ":far"),
    ("the close rests here", "WARRANT-close", ":near"),
    ("near face carries the dateline", "WARRANT-onset", ":near"),
    ("sub-onset beyond this close", "WARRANT-close", ":far"),
    ("next unit address opens here", "WARRANT-close", ":far"),
    ("unmarked doom-poem opens here", "WARRANT-onset", ":near"),
    ("a fresh movement begins past here", "WARRANT-close", ":far"),
    ("the tribal list resumes here", "WARRANT-close", ":far"),
    ("priestly class changes at this verse", "WARRANT-close", ":far"),
    ("messenger names the addressee here", "WARRANT-onset", None),
    ("mofet partner within the unit", "WARRANT-close", ":interior"),
    ("son of man address", "WARRANT-onset", None),
    ("opens this unit", "WARRANT-onset", ":near"),
    ("the verse before carries a samekh", "WARRANT-onset", ":far"),
]


def selftest():
    bad = []
    for text, token, want in FIXTURES:
        got, basis = face_from_words(strip_signals(text), token)
        if got != want:
            bad.append({"text": text, "token": token, "expected": want, "got": got, "basis": basis})
    fired = sum(1 for t, tok, w in FIXTURES if w is not None)
    print(json.dumps({"selftest_vectors": len(FIXTURES), "failed": len(bad),
                      "vectors_that_must_match_a_face": fired, "failures": bad}, indent=1))
    return 1 if bad else 0


if "--selftest" in sys.argv:
    raise SystemExit(selftest())
if selftest():
    raise SystemExit("REFUSED: the selftest failed, so the patterns cannot be trusted and no verdict is "
                     "computed. A reader that cannot match its own fixtures cannot corroborate anything.")

plan = json.loads(PLAN.read_text(encoding="utf-8"))
rows, tally = [], Counter()
for item in plan["derivable_now"]:
    words = strip_signals(item["entry_before"])
    said, basis = face_from_words(words, item["token"])
    derived = item["qualifier"]
    verdict = "UNSPOKEN" if said is None else ("AGREE" if said == derived else "DISAGREE")
    tally[verdict] += 1
    tally["%s|%s" % (derived, said or "-")] += 1
    if verdict != "UNSPOKEN":
        rows.append({"row": item["row"], "token": item["token"], "geometry_says": derived,
                     "the_words_say": said, "how_the_words_were_read": basis,
                     "verdict": verdict, "entry": item["entry_before"]})

dis = [r for r in rows if r["verdict"] == "DISAGREE"]
agree = sum(1 for r in rows if r["verdict"] == "AGREE")
spoke = len(rows)

# THE REFUSAL. A check that compared nothing has not passed; it has not run.
if spoke == 0:
    verdict = ("BROKEN - the words assert a face NOWHERE, so this reader corroborated nothing. Zero "
               "disagreements here means zero comparisons, not agreement, and it is reported as a failure.")
elif dis:
    verdict = ("FLAGS - %d entries where the geometry and the annotation's own words assert different faces; "
               "each goes to the author batch and none is installed mechanically" % len(dis))
else:
    verdict = ("GREEN - %d of %d qualifiers are corroborated by a second, decorrelated reader and none is "
               "contradicted; the remaining %d annotations name no face and corroborate nothing"
               % (agree, len(plan["derivable_now"]), tally["UNSPOKEN"]))

out = {
    "schema": "ezek_face_distinct_check.v1",
    "order": "#e15 Q5: the mechanical face sweep runs with a DISTINCT CHECK",
    "the_two_readers": {
        "reader_1_geometry": "knows (verse, span) and the carrier's verse counts; reads no English",
        "reader_2_the_words": ("reads the annotation's wording with the role token and the verse reference "
                               "stripped out first, so it cannot see reader 1's signal; knows no span"),
        "why_decorrelated": ("a sign error in the geometry's previous/next verse would flip every qualifier at "
                             "once and stay perfectly self-consistent; only a reader that does not do the "
                             "arithmetic can catch that"),
    },
    "inputs": {"plan": PLAN.name, "plan_sha256": sha(PLAN),
               "rows_sha256": plan["inputs"]["rows_sha256"]},
    "selftest": {"vectors": len(FIXTURES), "failed": 0,
                 "why_it_gates_the_verdict": ("this reader once reported GREEN while matching nothing at all - "
                                              "every word boundary in its patterns had become a literal "
                                              "backspace byte. The fixtures now run first and a failure "
                                              "refuses the run.")},
    "tally": dict(tally),
    "summary": {"qualifiers_proposed": len(plan["derivable_now"]),
                "the_words_assert_a_face": spoke, "AGREE": agree, "DISAGREE": len(dis),
                "UNSPOKEN": tally["UNSPOKEN"]},
    "two_corrections_to_this_reader_disclosed": [
        ("its first version read DEIXIS as a face claim and reported 7 disagreements, all 7 its own error. "
         "P08-012's 'begins past here' at Ezek.36.24 was decisive: the reader said near, the geometry said "
         "far, and #e15 says of that row 'the FAR face, 36:24, carries nothing'."),
        ("its second version reported GREEN while matching nothing: 66 word boundaries had been turned into "
         "literal backspace bytes by the shell heredoc that wrote the patch, so all 111 entries came back "
         "UNSPOKEN and 'no disagreement' was printed. Zero disagreements because zero comparisons."),
    ],
    "what_unspoken_means": ("the annotation names no face, so this reader corroborates nothing for it. It is "
                            "NOT an agreement and is not counted as one - counting a silence as a pass is the "
                            "same error as summing an absent token figure as zero."),
    "DISAGREEMENTS": dis,
    "verdict": verdict,
    "tier": "MEASURED by both readers over the same entries",
}
p = HERE / "face_distinct_check.v1.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({k: out[k] for k in ("summary", "verdict")}, ensure_ascii=False, indent=1))
print()
for d in dis[:16]:
    print("  %-9s %-14s geometry=%-10s words=%-10s %s" % (d["row"], d["token"], d["geometry_says"],
                                                          d["the_words_say"], d["entry"][:70]))
