#!/usr/bin/env python3
"""#e15 Q6: fix the two citation_sweep defects the agents found, each with its failure case as a fixture.

Q6(a) THE FIRST-MATCH COLLATION. Confirmed by the ruling in source at line 691: `pos = o.find(run)`, so every
occurrence of a byte-identical run in one field is collated at the FIRST occurrence's position. That is why my
own wrong-verse repair passed every byte check. The order: finditer with per-match offsets, each occurrence
collated against the reference governing ITS OWN clause or sentence - the nearest preceding oshb: ref within the
same sentence, falling back to nearest-by-distance only when the sentence carries none.

Q6(b) THE PASEQ ARM. Confirmed in source at 521-526: the device word fires the arm with no negation guard,
unlike the puncta arm, and the role token `[DISCLOSURE-paseq]` contains the device name, so the token fires its
own arm. The order: strip the token before matching; apply the puncta arm's adjacent-negation guard to the paseq
and mark arms; a NEGATED claim is verified as an absence, so a non-empty census at that verse is the defect.

THE NON-DISCRIMINATING NOTE is the part I would not have thought of. Where two identical runs cite verses whose
bytes are also identical, the check passes and CANNOT DISTINGUISH them - so the report says so, rather than
being green for a reason it cannot support. A checker that is right by luck should say which.
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
SRC = TOOLS / "citation_sweep.py"
PIN = "6c843b14a604ec0cdb4ee52043cdd5ae30d6735b0a7d66d72ff28d9f00a39054"
HERE = Path(__file__).resolve().parent
HERE.mkdir(parents=True, exist_ok=True)

pre = SRC.read_bytes()
got = hashlib.sha256(pre).hexdigest()
if got != PIN:
    raise SystemExit("REFUSED: preimage %s, expected %s" % (got, PIN))
(HERE / "citation_sweep.preimage_6c843b14.py").write_bytes(pre)
t = pre.decode("utf-8")
edits = []


def edit(desc, old, new, count=1):
    edits.append((desc, old, new, count))


# ---- helpers, added beside the existing negation regexes
edit("per-clause helpers and the token stripper",
     'SINGLE_WITNESS = re.compile(r"\\bsingle[-\\s]+witness", re.I)   # T4-04: the disclosure, hyphenated or '
     'spaced',
     '''SINGLE_WITNESS = re.compile(r"\\bsingle[-\\s]+witness", re.I)   # T4-04: the disclosure, hyphenated or spaced
# #e15 Q6(b): a ROLE token carries its own device name ("[DISCLOSURE-paseq]"), so the token must be stripped
# before any device-word match or the token fires its own arm. Measured cause of one false defect.
ROLE_TOKEN = re.compile(r"\\[(?:WARRANT|DISCLOSURE|QUOTE|ANCHOR)[A-Za-z:-]*\\]")
# #e15 Q6(a): each Hebrew run is collated against the reference governing ITS OWN clause. Sentence bounds are
# terminal punctuation; a clause is the run of text between them.
SENT_SPLIT = re.compile(r"(?<=[.!?])\\s+")


def _sentence_bounds(text, pos):
    """The (start, end) of the sentence containing `pos`."""
    start = 0
    for m in SENT_SPLIT.finditer(text):
        if m.end() <= pos:
            start = m.end()
        else:
            break
    end = len(text)
    m = SENT_SPLIT.search(text, pos)
    if m:
        end = m.start()
    return start, end''')

# ---- Q6(a): finditer, per-occurrence, sentence-scoped candidate refs
edit("finditer with per-occurrence, sentence-scoped collation",
     """                for run in runs:
                    if not refs:
                        problems.append(f"{did}: Hebrew quote {run[:25]!r}… in "
                                        f"{path} has NO oshb: ref in its field")
                        continue
                    pos = o.find(run)
                    end = pos + len(run)
                    def keyf(mm):
                        follows = 0 <= mm.start() - end <= 40
                        dist = min(abs(mm.start() - pos), abs(mm.start() - end))
                        return (not follows, dist)
                    cands = sorted(refs, key=keyf)[:3]""",
     """                # #e15 Q6(a): EVERY occurrence of a run is judged at ITS OWN position, against the
                # reference that governs its own sentence. The previous form took o.find(run), so a second
                # identical run in one field was collated where the FIRST one stood - which is exactly how a
                # wrong-verse attribution passed every byte check (ledger note in E13-84).
                occurrences = []
                for run in runs:
                    for _m in re.finditer(re.escape(run), o):
                        occurrences.append((run, _m.start(), _m.end()))
                for run, pos, end in occurrences:
                    if not refs:
                        problems.append(f"{did}: Hebrew quote {run[:25]!r}… in "
                                        f"{path} has NO oshb: ref in its field")
                        continue
                    _s, _e = _sentence_bounds(o, pos)
                    in_sentence = [mm for mm in refs if _s <= mm.start() < _e]
                    scope = in_sentence or refs
                    def keyf(mm):
                        follows = 0 <= mm.start() - end <= 40
                        precedes_in_sentence = bool(in_sentence) and mm.start() < pos
                        dist = min(abs(mm.start() - pos), abs(mm.start() - end))
                        return (not (follows or precedes_in_sentence), dist)
                    cands = sorted(scope, key=keyf)[:3]""")

# ---- Q6(b): strip the token, add the negation guard, verify a negated claim as an absence
edit("paseq arm: strip the token, guard the negation, verify an absence",
     '''            if re.search(r"\\bpaseq\\b", tail, re.I):
                if not paseq.get(key):
                    problems.append(f"{did}: {ref!r} claims paseq but OSHB carries "
                                    f"none at {key}")
                if not SINGLE_WITNESS.search(tail):
                    problems.append(f"{did}: paseq ref lacks single-witness disclosure: {ref!r}")''',
     '''            # #e15 Q6(b): the role token is stripped first, because "[DISCLOSURE-paseq]" contains the
            # device name and otherwise fires this arm by itself. A NEGATED claim is then verified as an
            # ABSENCE: a non-empty census at the verse is the defect, not an empty one.
            tail_nt = ROLE_TOKEN.sub(" ", tail)
            _pm = re.search(r"\\bpaseq\\b", tail_nt, re.I)
            if _pm:
                negated = bool(PUNCTA_NEG.search(tail_nt[:_pm.start()])) or "-absence]" in tail
                if negated:
                    if paseq.get(key):
                        problems.append(f"{did}: {ref!r} DENIES a paseq at {key} where the seg layer "
                                        f"records {paseq.get(key)}")
                elif not paseq.get(key):
                    problems.append(f"{did}: {ref!r} claims paseq but OSHB carries "
                                    f"none at {key}")
                if not SINGLE_WITNESS.search(tail):
                    problems.append(f"{did}: paseq ref lacks single-witness disclosure: {ref!r}")''')

new = t
for desc, old, rep, want in edits:
    n = new.count(old)
    if n != want:
        raise SystemExit("REFUSED: %r occurs %d times, expected %d" % (desc, n, want))
    new = new.replace(old, rep, want)
    print("  edit OK  %s" % desc)

STAGE = HERE / "citation_sweep.candidate.py"
STAGE.write_text(new, encoding="utf-8", newline="\n")
py_compile.compile(str(STAGE), doraise=True)
print("  py_compile OK")

tmp = SRC.with_suffix(".py.tmpQ6")
shutil.copy2(STAGE, tmp)
tmp.replace(SRC)
post = hashlib.sha256(SRC.read_bytes()).hexdigest()

# the ruling requires it to run over the CURRENT rows as a baseline, before any mutation
rows = TOOLS.parent / "repair" / "rows_v7_cwo24.jsonl"
r = subprocess.run([sys.executable, str(SRC), str(rows)], capture_output=True, text=True,
                   cwd=str(TOOLS), encoding="utf-8", errors="replace")
try:
    rep = json.loads(r.stdout)
    summary = {"status": rep.get("status"), "problems": len(rep.get("problems") or []),
               "problem_list": (rep.get("problems") or [])[:10]}
except Exception:
    summary = {"unparsed": (r.stdout or r.stderr)[-500:]}
print(json.dumps({"preimage": PIN, "postimage": post, "exit": r.returncode,
                  "baseline_over_current_rows": summary}, indent=1, ensure_ascii=False))
