"""Stage TOOLFIX-2 exactly as ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2 condition (b) states it, as ONE batch
(toolfix2_batch1) over the INSTALLED tools, which already carry TOOLFIX-1 (receipt ezek_tools_install_t4fix_batch2.json).
Session scratch only; nothing is installed. It supersedes the pre-ruling proposal toolfix2_batch2, which was never
installed.

CONTENT per (b):
  S1-07  ezek_lib.collate_hebrew gains a boundary rule that citation_sweep and the normalizer inherit.
         - Byte-class tiers (byte, nfd, accent_stripped): a match is neither preceded nor followed by a Hebrew letter or a
           combining mark.
         - Skeleton tier: a match is neither preceded nor followed by a Hebrew letter (a word boundary).
         - The normalizer never extends a run to a boundary; it reports a defect. Its book-wide Qere tier keeps its scope
           (R4-i), with the same boundary.
  S1-06  citation_sweep binds every Hebrew run inside a boundary_evidence_refs entry to that entry's own (first) ref,
         using walk()'s collate, raw-note Qere and in-sentence K/Q-keyword functions.
  S1-05  check_register gains the ruling's arms verbatim, with GREEN controls.
  S1-10  check_web_quotes flags a prose field whose curly DOUBLE quote counts differ.
  S1-22  check_marks Rules 1, 3 and 4:
         - claims read C:V, C.V, 'MT C:V' and dotted forms, bound to their own clause;
         - an absence phrase is scoped to the verse, range or chapter it names;
         - a negated K/Q token is an absence claim.
  S1-19  _cure_verification refuses (a) no author fields, (b) duplicate cure_ids, (c) an ordering id not bounded
         against '-', and (d) any digest that is not 64 hex; (e) is a recorded classification, never a refusal.
         --require-rulings serves gating runs.
  (e)    TOOLKIT.md and check_marks' docstring are edited in the same batch; the R6 sibling sweep's statements are
         recorded.

THE RUN:
  - regenerate the zone tools;
  - zone tests (section 10b), the ezek_lib selftest, the toolkit selfcheck, and the verifier selftest and real claims;
  - the suite over the chain head, compared with the post-TOOLFIX-1 installed report (suite_after_t4fix_batch2);
  - a corpus-impact report per (c): new HARD problems classed KNOWN (S1-06/S1-07 rows and runs) or NEW; removed and
    added FLAGS by rule and row against S1's TQ rows;
  - discrimination of the new vectors against the installed tools."""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
SCR = Path(__file__).resolve().parent
ROOT = SCR / "stage_tf2b"
ST = ROOT / "sp_durable"
T = ST / "Ezek" / "tools"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
applied = []


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(args, cwd=T):
    return subprocess.run([sys.executable] + [str(a) for a in args], capture_output=True, text=True, encoding="utf-8", env=ENV, cwd=str(cwd))


def sub(path, old, new, label, count=1):
    t = path.read_text(encoding="utf-8")
    n = t.count(old)
    if n != count:
        raise SystemExit("ABORT: %s: expected %d occurrence(s) in %s, found %d" % (label, count, path.name, n))
    path.write_text(t.replace(old, new), encoding="utf-8", newline="\n")
    applied.append(label)


# ------------------------------------------------------------------ stage
rec = json.loads((SP / "campaign" / "receipts" / "ezek_tools_install_t4fix_batch2.json").read_text(encoding="utf-8"))
for n, f in rec["files"].items():
    if sha(SP / "Ezek" / "tools" / n) != f["after"]:
        raise SystemExit("ABORT: SP tools/%s is not the TOOLFIX-1 installed digest" % n)
assert ROOT.parent == SCR and ROOT.name == "stage_tf2b"
if ROOT.exists():
    shutil.rmtree(ROOT)
ign = shutil.ignore_patterns("__pycache__", "*.pyc")
shutil.copytree(SP / "Ezek" / "tools", T, ignore=ign)
shutil.copytree(SP / "Jer" / "tools", ST / "Jer" / "tools", ignore=ign)
for f in (SP / "Ezek").iterdir():
    if f.is_file():
        shutil.copy2(f, ST / "Ezek" / f.name)
(ST / "campaign").mkdir(parents=True)
shutil.copy2(SP / "campaign" / "_cure_verification.py", ST / "campaign" / "_cure_verification.py")
SUITE = ST / "Ezek" / "repair" / "suite_tf2b"
SUITE.mkdir(parents=True)
shutil.copy2(SP / "Ezek" / "repair" / "rows_v3_cwo12.jsonl", SUITE / "rows.jsonl")
LIB, NORM, ADAPT = T / "ezek_lib.py", T / "normalize_hebrew_in_json.py", T / "_adapt_zone_tools_ezek.py"
REG, WQ, TK, TEST = T / "check_register.py", T / "check_web_quotes.py", T / "TOOLKIT.md", T / "_test_zone_tools_ezek.py"
VER = ST / "campaign" / "_cure_verification.py"

# ------------------------------------------------------------------ S1-07: ezek_lib
sub(LIB, "def collate_hebrew(quoted: str, source_text: str) -> str:\n", r'''HEB_LETTER = re.compile("[\u05d0-\u05ea\u05f0-\u05f2]")


def is_mark(ch: str) -> bool:
    """A combining mark (Unicode Mn): points, accents, dagesh, the shin and sin dots, U+05C4. Maqaf, paseq and sof pasuq
    are not marks."""
    return unicodedata.category(ch) == "Mn"


def is_letter(ch: str) -> bool:
    return bool(HEB_LETTER.match(ch))


def bounded_find(hay: str, needle: str, pos: int = 0, marks: bool = True) -> int:
    """The first index >= pos where needle occurs in hay on word boundaries (S1-07; ezek_controlling_rulings_a1#e4 ruling
    TOOLFIX-2 (b)). With marks=True (the byte, nfd and accent_stripped tiers) the match is neither preceded nor followed by a
    Hebrew letter or a combining mark; with marks=False (the skeleton tier) it is neither preceded nor followed by a Hebrew
    letter. -1 when there is none."""
    if not needle:
        return -1
    edge = (lambda ch: is_letter(ch) or is_mark(ch)) if marks else is_letter
    i = hay.find(needle, pos)
    while i != -1:
        j = i + len(needle)
        if (i == 0 or not edge(hay[i - 1])) and (j >= len(hay) or not edge(hay[j])):
            return i
        i = hay.find(needle, i + 1)
    return -1


def bounded_in(needle: str, hay: str, marks: bool = True) -> bool:
    return bounded_find(hay, needle, 0, marks) != -1


def collate_hebrew(quoted: str, source_text: str) -> str:
''', "S1-07 ezek_lib boundary helpers")
sub(LIB, 'checks.append(("collate_hebrew returns byte for a verbatim verse", collate_hebrew(oshb["Ezek.1.1"], joined) == "byte"))\n',
    'checks.append(("collate_hebrew returns byte for a verbatim verse",   # S1-07: verses joined as the tools join them; the old fixture\n'
    '                   collate_hebrew(oshb["Ezek.1.1"], " | ".join(oshb.values())) == "byte"))   # glued 1:1 to 1:2\'s first letter\n',
    "S1-07 selftest fixture: the verbatim-verse check joins verses with a separator (disclosed)")
sub(LIB, "    'byte' | 'nfd' | 'accent_stripped' | 'skeleton' | 'none'. Ellipsis-aware: fragments must match IN ORDER.\"\"\"\n",
    "    'byte' | 'nfd' | 'accent_stripped' | 'skeleton' | 'none'. Ellipsis-aware: fragments must match IN ORDER. Every fragment\n"
    "    matches on word boundaries (bounded_find): no Hebrew letter or combining mark beside it at the byte, nfd and\n"
    "    accent_stripped tiers, no Hebrew letter beside it at the skeleton tier (S1-07).\"\"\"\n", "S1-07 collate_hebrew docstring")
sub(LIB, "    def ordered(hay: str, needles: list[str]) -> bool:\n        pos = 0\n        for n in needles:\n            i = hay.find(n, pos)\n",
    "    def ordered(hay: str, needles: list[str], marks: bool) -> bool:\n        pos = 0\n        for n in needles:\n"
    "            i = bounded_find(hay, n, pos, marks)\n", "S1-07 ordered() bounded")
sub(LIB, "        if ordered(xf(source_text), [xf(f) for f in frags]):\n",
    "        if ordered(xf(source_text), [xf(f) for f in frags], tier != \"skeleton\"):\n", "S1-07 tier-appropriate boundary")
sub(LIB, "    failed = [n for n, ok in checks if not ok]\n", r'''    # S1-07 (#e4 ruling TOOLFIX-2 (b)): word boundaries. Every case is found in the bytes, never typed.
    def _cases():
        found = {}
        for key in sorted(oshb, key=lambda k: (int(k.split(".")[1]), int(k.split(".")[2]))):
            verse = oshb[key]
            for w in verse.split(" "):
                letters = [i for i, ch in enumerate(w) if is_letter(ch)]
                if len(letters) < 4:
                    continue
                if "end" not in found and is_mark(w[-1]):
                    k = len(w)
                    while k and is_mark(w[k - 1]):
                        k -= 1
                    if not bounded_in(w[:k], verse):
                        found["end"] = (verse, w, w[:k])
                if "shin" not in found and "\u05e9\u05c1" in w[-4:]:
                    k = w.rfind("\u05c1")
                    if not bounded_in(w[:k], verse) and w[:k]:
                        found["shin"] = (verse, w, w[:k])
                if "start" not in found:
                    rest = w[letters[1]:]
                    if not bounded_in(rest, verse):
                        found["start"] = (verse, w, rest)
                if "root" not in found:
                    sk = skeleton(w).replace(" ", "")
                    inner = sk[1:-1]
                    if len(inner) >= 3 and not bounded_in(inner, skeleton(verse), marks=False):
                        found["root"] = (verse, w, inner)
                if len(found) == 4:
                    return found
        return found
    cases = _cases()
    checks.append(("REGRESSION S1-07 a splice cut before its word's final marks is not byte; the whole word is",
                   "end" in cases and collate_hebrew(cases["end"][2], cases["end"][0]) != "byte"
                   and collate_hebrew(cases["end"][1], cases["end"][0]) == "byte"))
    checks.append(("REGRESSION S1-07 a shin written without its shin dot is not byte",
                   "shin" in cases and collate_hebrew(cases["shin"][2], cases["shin"][0]) != "byte"))
    checks.append(("S1-07 a quote that begins inside a word (its first letter dropped) is not byte",
                   "start" in cases and collate_hebrew(cases["start"][2], cases["start"][0]) != "byte"))
    checks.append(("S1-07 an unpointed root inside a longer word does not collate at skeleton tier",
                   "root" in cases and collate_hebrew(cases["root"][2], cases["root"][0]) == "none"))
    w11 = oshb["Ezek.1.1"].split(" ")
    checks.append(("S1-07 whole words, an ellipsis of whole words, and an unpointed whole word still collate",
                   collate_hebrew(w11[1], oshb["Ezek.1.1"]) == "byte"
                   and collate_hebrew(w11[1] + " … " + w11[3], oshb["Ezek.1.1"]) == "byte"
                   and collate_hebrew(skeleton(w11[1]), oshb["Ezek.1.1"]) == "skeleton"))
    checks.append(("S1-07 skeleton() keeps word spaces (the word boundary depends on it)", " " in skeleton(oshb["Ezek.1.1"])))

    failed = [n for n, ok in checks if not ok]
''', "S1-07 ezek_lib selftest vectors")

# ------------------------------------------------------------------ S1-07: normalizer
sub(NORM, "(letters/points + internal spaces/maqaf) must be a byte-identical substring of\nEzek_oshb.txt.",
    "(letters/points + internal spaces/maqaf) must be a byte-identical substring of\nEzek_oshb.txt standing on word "
    "boundaries (no Hebrew letter or combining mark beside it; S1-07).\nA run cut inside a word is a defect: the normalizer "
    "never extends a run to a boundary.", "S1-07 normalizer docstring")
sub(NORM, "MIN_LEN = 2   # lesson f (Ps close): the standard re-splice cure runs MIN_LEN=2\n",
    "MIN_LEN = 2   # lesson f (Ps close): the standard re-splice cure runs MIN_LEN=2\n"
    "sys.path.insert(0, str(FREEZE))\n"
    "from ezek_lib import bounded_in  # noqa: E402   S1-07: presence is word-bounded at every tier\n", "S1-07 normalizer import")
sub(NORM, "def find_source_bytes(run: str, src: str, verses: list[str]) -> str | None:\n    if run in src:\n        return run\n",
    "def find_source_bytes(run: str, src: str, verses: list[str]) -> str | None:\n    if bounded_in(run, src):\n        return run\n",
    "S1-07 find_source_bytes bounded")
sub(NORM, "        if run in src:\n            stats[\"ok\"] += 1\n", "        if bounded_in(run, src):\n            stats[\"ok\"] += 1\n",
    "S1-07 byte tier bounded")
sub(NORM, "        if run in KQ[\"qere\"]:\n", "        if bounded_in(run, KQ[\"qere\"]):\n", "S1-07 Qere tier bounded (scope unchanged, R4-i)")
sub(NORM, '            if POINTS.sub("", run) in skel_src or POINTS.sub("", nfd(run)) in KQ["skel"]:\n',
    '            if bounded_in(POINTS.sub("", run), skel_src, marks=False) or bounded_in(POINTS.sub("", nfd(run)), KQ["skel"], marks=False):\n',
    "S1-07 unpointed mention tier word-bounded")

# ------------------------------------------------------------------ S1-06: citation_sweep REF HEBREW arm (adapter)
sub(ADAPT, 'CS_CAL_ONSET = r"""', r'''CS_REF_HEBREW_ARM = r"""            # REF HEBREW arm (Ezek; S1-06, ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2 (b)) [CWO-EZ-16]: every Hebrew
            # run inside a ref entry binds to that entry's OWN (first) ref - every verse of its range - with walk()'s functions:
            # collate_hebrew (byte tier if pointed, any tier if unpointed), the verse's Qere from the raw note bytes, and a
            # ketiv/qere keyword in the run's own sentence within 160 characters.
            ref_runs_ = [r_ for r_ in HEB_RUN.findall(tail) if len(re.sub(r"[^א-ת]", "", r_)) >= 3]
            if ref_runs_:
                if oshb_texts is None:
                    oshb_texts = json.loads((TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))
                keys_, (c_, v_) = [], (ch, v)
                while (c_, v_) <= end_pair and c_ in space:
                    mk_ = web_to_mt(c_, v_) if kind == "web" else (c_, v_)
                    if mk_:
                        keys_.append(f"Ezek.{mk_[0]}.{mk_[1]}")
                    c_, v_ = (c_, v_ + 1) if v_ < space[c_] else (c_ + 1, 1)
                texts_ = " | ".join(oshb_texts.get(k_, {}).get("text", "") for k_ in keys_)
                qere_ = " | ".join(kq_split_bytes(n_, oshb_texts.get(k_, {}).get("text", ""))[1].replace("/", "")
                                   for k_ in keys_ for n_ in kq.get(k_, []))
                for r_ in ref_runs_:
                    pointed_ = bool(POINTED.search(r_))
                    t_ = collate_hebrew(r_, texts_)
                    if (t_ == "byte") if pointed_ else t_ != "none":
                        continue
                    tq_ = collate_hebrew(r_, qere_) if qere_.strip(" |") else "none"
                    if (tq_ == "byte") if pointed_ else tq_ != "none":
                        p_ = tail.find(r_)
                        s_lo_, s_hi_ = sentence_bounds(tail, p_, p_ + len(r_))
                        if KQ_WORD.search(tail[max(s_lo_, p_ - 160):min(s_hi_, p_ + len(r_) + 160)]):
                            continue
                        problems.append(f"{did}: Hebrew {r_[:25]!r}… in ref entry {ref!r} matches the Qere of its own ref "
                                        f"but its sentence carries no ketiv/qere disclosure [CWO-EZ-16]")
                        continue
                    problems.append(f"{did}: Hebrew {r_[:25]!r}… in ref entry {ref!r} does not collate against its own ref "
                                    f"(tier {t_}, qere tier {tq_}, {'pointed' if pointed_ else 'unpointed'}) [CWO-EZ-16]")
"""

CS_CAL_ONSET = r"""''', "S1-06 CS_REF_HEBREW_ARM defined")
sub(ADAPT, "CS_PUNCTA_ARM + CS_CAL_REF_ARM + kq_line_ezek", "CS_PUNCTA_ARM + CS_CAL_REF_ARM + CS_REF_HEBREW_ARM + kq_line_ezek",
    "S1-06 REF HEBREW arm wired into the ref loop")

# ------------------------------------------------------------------ S1-22: check_marks Rules 1, 3, 4 (adapter, on the Jer text)
sub(ADAPT, "def stage_check_marks():\n", r'''CHAPTER_NAMED_RE = r"""CHAPTER_NAMED = re.compile(r"\bch(?:apter|\.)?\s+(\d{1,2})\b", re.I)   # S1-22: 'chapter 10', 'ch 46'
"""

CM_RULE1_OLD = """                lo = max(0, m.start() - 120)
                ctx = text[lo:m.start() + 120]
                cands = list(VERSE_NEAR.finditer(ctx))
                if not cands:
                    continue
                rel = m.start() - lo
                cands.sort(key=lambda vm: abs(vm.start() - rel))
                if any(want_type in marks.get(f"Jer.{rc}.{rv}", [])
                       for vm in cands
                       for rc, rv in readings(int(vm.group(1)), int(vm.group(2)))):
                    continue
                if ABSENCE.search(ctx):
                    continue
                vm = cands[0]
                c, v = int(vm.group(1)), int(vm.group(2))
"""
CM_RULE1_NEW = """                # S1-22 (ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2 (b)): the claim binds to the verse numbers written in
                # its OWN clause - C:V, C.V, 'MT C:V' or a dotted ref alike - plus a parenthetical opening directly after it; a
                # claim naming no number in its clause is left to rule 2 (symmetry)
                c_lo_, c_hi_ = clause_bounds(text, m.start(), m.end(), NUM_CLAUSE_END)
                named_ = [p for pairs in puncta_claim_numbers(text, m.start(), m.end()) for p in pairs]
                if not named_:
                    continue
                if any(want_type in marks.get(f"Jer.{rc}.{rv}", [])
                       for c0, v0 in named_
                       for rc, rv in readings(c0, v0)):
                    continue
                if ABSENCE.search(text[c_lo_:c_hi_]):
                    continue
                c, v = named_[0]
"""
CM_RULE3_OLD = """            for am in ABSENCE.finditer(text):
                have = relevant(span_pairs(row), marks)
                if have:
                    flags.append({"decision_id": did, "rule": "false_mark_absence_claim",
                                  "claim_context": text[max(0, am.start() - 60):am.start() + 80],
                                  "span_relevant_marks_mt_keys": have})
                    break
"""
CM_RULE3_NEW = """            # S1-22 (#e4 ruling TOOLFIX-2 (b)): an absence phrase is scoped to the verse, range or chapter its own clause
            # names; an absence phrase naming none keeps the span-scoped check
            for am in ABSENCE.finditer(text):
                named_ = [p for pairs in puncta_claim_numbers(text, am.start(), am.end()) for p in pairs]
                c_lo_, c_hi_ = clause_bounds(text, am.start(), am.end(), NUM_CLAUSE_END)
                for chm_ in CHAPTER_NAMED.finditer(text, c_lo_, c_hi_):
                    ch_ = int(chm_.group(1))
                    named_ += [(ch_, vv_) for vv_ in range(1, MT_LAST_VERSE.get(ch_, 0) + 1)]
                if named_:
                    scope_ = "named"
                    have = {f"Jer.{rc}.{rv}": marks[f"Jer.{rc}.{rv}"] for c0, v0 in named_ for rc, rv in readings(c0, v0)
                            if marks.get(f"Jer.{rc}.{rv}")}
                else:
                    scope_ = "span"
                    have = relevant(span_pairs(row), marks)
                if have:
                    flags.append({"decision_id": did, "rule": "false_mark_absence_claim", "scope": scope_,
                                  "claim_context": text[max(0, am.start() - 60):am.start() + 80],
                                  "span_relevant_marks_mt_keys": have})
                    break
"""
CM_RULE4_OLD = """            for m in KQ.finditer(text):
                lo = max(0, m.start() - 120)
                ctx = text[lo:m.start() + 120]
                cands = list(VERSE_NEAR.finditer(ctx))
                if not cands:
                    continue
                rel = m.start() - lo
                cands.sort(key=lambda vm: abs(vm.start() - rel))
                if any(kq.get(f"Jer.{rc}.{rv}") or (f"Jer.{rc}.{rv}" in kq_note_keys and NOTE_WORD.search(ctx))
                       for vm in cands
                       for rc, rv in readings(int(vm.group(1)), int(vm.group(2)))):
                    continue
                vm = cands[0]
                c, v = int(vm.group(1)), int(vm.group(2))
"""
CM_RULE4_NEW = """            # S1-22 (#e4 ruling TOOLFIX-2 (b)): a K/Q claim binds to the verse numbers in its OWN clause (C:V, C.V, 'MT C:V'
            # or dotted); a NEGATED K/Q token is an absence claim, checked against the verses its clause names or, naming
            # none, the span's kq keys (rule false_kq_absence_claim)
            for m in KQ.finditer(text):
                lo = max(0, m.start() - 120)
                ctx = text[lo:m.start() + 120]
                named_ = [p for pairs in puncta_claim_numbers(text, m.start(), m.end()) for p in pairs]
                if puncta_negated(text, m.start(), m.end()):
                    if named_:
                        keys_ = {f"Jer.{rc}.{rv}" for c0, v0 in named_ for rc, rv in readings(c0, v0)}
                    else:
                        keys_ = {f"Jer.{mt_[0]}.{mt_[1]}" for c0, v0 in span_pairs(row) for mt_ in [web_to_mt(c0, v0)] if mt_}
                    present_ = sorted(k_ for k_ in keys_ if kq.get(k_))
                    if present_:
                        flags.append({"decision_id": did, "rule": "false_kq_absence_claim", "scope": "named" if named_ else "span",
                                      "kq_mt_keys": present_, "claim_context": text[max(0, m.start() - 60):m.start() + 80]})
                    continue
                if not named_:
                    continue
                if any(kq.get(f"Jer.{rc}.{rv}") or (f"Jer.{rc}.{rv}" in kq_note_keys and NOTE_WORD.search(ctx))
                       for c0, v0 in named_
                       for rc, rv in readings(c0, v0)):
                    continue
                c, v = named_[0]
"""


def stage_check_marks():
''', "S1-22 check_marks rule texts defined in the adapter")
sub(ADAPT, '"PUNCTA_SITES = {(41, 20), (46, 22)}   # MT; asserted by ezek_lib\'s selftest\\n",',
    '"PUNCTA_SITES = {(41, 20), (46, 22)}   # MT; asserted by ezek_lib\'s selftest\\n" + CHAPTER_NAMED_RE,', "S1-22 CHAPTER_NAMED constant wired")
sub(ADAPT, '    return "check_marks.py", join_doc(head, t, CM_DOC), t\n',
    '    t = sub_exact(t, CM_RULE1_OLD, CM_RULE1_NEW, 1, "cm S1-22 rule 1 own-clause binding")\n'
    '    t = sub_exact(t, CM_RULE3_OLD, CM_RULE3_NEW, 1, "cm S1-22 rule 3 scoped absence")\n'
    '    t = sub_exact(t, CM_RULE4_OLD, CM_RULE4_NEW, 1, "cm S1-22 rule 4 own-clause binding and negated K/Q")\n'
    '    return "check_marks.py", join_doc(head, t, CM_DOC), t\n', "S1-22 rule substitutions applied")
sub(ADAPT, " 1. Any petuchah/setumah claim naming a verse must match the marks inventory\n",
    " 1. Any petuchah/setumah claim naming a verse IN ITS OWN CLAUSE (C:V, C.V, 'MT C:V'\n"
    "    or a dotted ref; S1-22) must match the marks inventory\n", "S1-22 docstring rule 1")
sub(ADAPT, ' 3. ABSENCE ARM, SPAN-SCOPED: "no petuchah/setumah" claims are checked\n    against the marks inventory WITHIN the span-relevant (MT-mapped) set.\n',
    ' 3. ABSENCE ARM: a "no petuchah/setumah" claim is checked against the verse,\n'
    '    range or chapter its own clause names (S1-22); one naming none is checked\n'
    '    WITHIN the span-relevant (MT-mapped) set.\n', "S1-22 docstring rule 3")
sub(ADAPT, "    OSHB note names ketib/qere (the notes_other layer).\n",
    "    OSHB note names ketib/qere (the notes_other layer). The claim binds to the\n"
    "    numbers in its own clause (S1-22). A NEGATED K/Q claim is an absence claim,\n"
    "    checked against the verses its clause names or the span's kq keys\n"
    "    (false_kq_absence_claim).\n", "S1-22 docstring rule 4")

# ------------------------------------------------------------------ S1-05: check_register
sub(REG, '    "staged_file_stem": re.compile(\n', r'''    # S1-05 (ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2 (b)): the ruling's phrasings, verbatim [CWO-EZ-14]
    "author_wave_register_s1_05": re.compile(
        r"\boriginally drafted\b|\bformer (?:span|row)\b|\bprior \w+(?: \w+)? reading\b|\bcorrection to an earlier\b|"
        r"\b(?:preceding|next|following) row\b|\brow (?:before|after)\b|\b(?:one|middle|last) of \w+ rows\b|"
        r"\bstrategy['’]s\b|\bthe (?:ruling|order)['’]s\b|\bposture\b|\bofficially inventoried\b|"
        r"\b(?:ends|opens|closes|begins) the part\b|\bthe part['’]s\b", re.I),
    "staged_file_stem": re.compile(
''', "S1-05 register arms")

# ------------------------------------------------------------------ S1-10: check_web_quotes
sub(WQ, "        data = load_any(Path(f))\n", r'''        data = load_any(Path(f))
        # S1-10 (ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2 (b)) [CWO-EZ-17]: a prose field whose curly DOUBLE quote counts
        # differ. Single curly quotes are not counted: they double as apostrophes.
        for i_, row_ in enumerate(data if isinstance(data, list) else (data.get("decisions") or [])):
            if not isinstance(row_, dict):
                continue
            for field_ in ("boundary_rationale", "strongest_rejected_alternative", "device_notes"):
                s_ = row_.get(field_)
                if isinstance(s_, str) and s_.count("“") != s_.count("”"):
                    flags.append({"file": Path(f).name, "path": "[%d].%s" % (i_, field_), "decision_id": row_.get("decision_id"),
                                  "field": field_, "issue": "e15d_unequal_curly_double_quotes: %d open, %d close [CWO-EZ-17]"
                                  % (s_.count("“"), s_.count("”"))})
''', "S1-10 unequal-count arm")

# ------------------------------------------------------------------ S1-19: _cure_verification
sub(VER, '    reasons = []\n    cid = c.get("cure_id") or "(unnamed cure)"\n',
    '    reasons = []\n    cid = c.get("cure_id") or "(unnamed cure)"\n'
    '    if not (c.get("author_attempt_id") or c.get("author_execution_id")):\n'
    '        # S1-19(a): with no author named, the distinct-checker test below has nothing to compare and would pass vacuously\n'
    '        reasons.append("%s: names no author_attempt_id or author_execution_id, so the checker cannot be shown distinct" % cid)\n'
    '    for label_, value_ in (("artifact_sha256", c.get("artifact_sha256")),\n'
    '                           ("distinct_checker.artifact_sha256_at_review", (c.get("distinct_checker") or {}).get("artifact_sha256_at_review")\n'
    '                            if isinstance(c.get("distinct_checker"), dict) else None)):\n'
    '        if value_ is not None and not HEX64.fullmatch(str(value_)):\n'
    '            reasons.append("%s: %s %r is not a 64-hex digest (S1-19(d))" % (cid, label_, str(value_)[:20]))\n',
    "S1-19 (a) author required and (d) claim-level digests")
sub(VER, 'BARE_WORDS = {', 'HEX64 = re.compile(r"[0-9a-f]{64}")   # S1-19(d)\nBARE_WORDS = {', "S1-19 HEX64")
sub(VER, '        has_machine_result = (v.get("exit") is not None) or bool(v.get("output_sha256")) or bool(v.get("counts"))\n',
    '        osha = v.get("output_sha256")\n'
    '        osha_ok = isinstance(osha, str) and HEX64.fullmatch(osha) is not None\n'
    '        for label_, value_ in (("output_sha256", osha), ("artifact_sha256_at_run", v.get("artifact_sha256_at_run"))):\n'
    '            if value_ is not None and not HEX64.fullmatch(str(value_)):\n'
    '                reasons.append("%s %s %r is not a 64-hex digest (S1-19(d))" % (tag, label_, str(value_)[:20]))\n'
    '        has_machine_result = (v.get("exit") is not None) or osha_ok or bool(v.get("counts"))\n', "S1-19 (d) verification digests")
sub(VER, 'ORDERED_BY = re.compile(r"\\b(?P<xid>[a-z0-9_]+#e\\d+)\\b.*?\\bruling\\s+(?P<rid>[A-Za-z0-9][A-Za-z0-9-]*)")\n',
    '# S1-19(c): the ordering id is bounded against a hyphen too (\'test-adversarial#e1\' once matched as \'adversarial#e1\')\n'
    'ORDERED_BY = re.compile(r"(?<![\\w-])(?P<xid>[a-z0-9_]+#e\\d+)(?![\\w-]).*?\\bruling\\s+(?P<rid>[A-Za-z0-9][A-Za-z0-9-]*)")\n',
    "S1-19 (c) ordering id bounded")
sub(VER, '''def load_rulings(paths):
    """{execution_id: {ruling_id: verb}} from controlling-rulings files, for the optional --rulings cross-check."""
    out = {}
    for p in paths or []:
        d = json.loads(Path(p).read_text(encoding="utf-8"))
        out.setdefault(d.get("execution_id"), {}).update({r.get("id"): r.get("ruling") for r in d.get("rulings", [])})
    return out
''', '''RULING_TEXT = {}   # S1-19(e): (execution_id, ruling_id) -> the ruling's full text


def load_rulings(paths):
    """{execution_id: {ruling_id: verb}} from controlling-rulings files, for the optional --rulings cross-check."""
    out = {}
    for p in paths or []:
        d = json.loads(Path(p).read_text(encoding="utf-8"))
        out.setdefault(d.get("execution_id"), {}).update({r.get("id"): r.get("ruling") for r in d.get("rulings", [])})
        RULING_TEXT.update({(d.get("execution_id"), r.get("id")): json.dumps(r, ensure_ascii=False) for r in d.get("rulings", [])})
    return out


def classify_supersession(x):
    """S1-19(e), V3-W (#e4): which forward-rule form a supersession record takes. 'ruling_names_retired_cure' when the ordering
    ruling's text (from --rulings) names the retired cure id; 'r5_with_trigger' when it cites R5 and its why names an install
    receipt or a digest change; otherwise 'unclassified'. A classification only, never a refusal."""
    m = ORDERED_BY.search(str(x.get("ordered_by", "")))
    target = str(x.get("supersedes_cure_id", ""))
    if m and re.search(r"(?<![\\w-])%s(?![\\w-])" % re.escape(target), RULING_TEXT.get((m.group("xid"), m.group("rid")), "")):
        return "ruling_names_retired_cure"
    if m and m.group("rid") == "R5" and re.search(r"receipt|->|\\u2192", str(x.get("why", ""))):
        return "r5_with_trigger"
    return "unclassified"
''', "S1-19 (e) ruling text and classification")
sub(VER, '''    claims = [x for x in lines if x.get("record_type") != "supersession"]
    claim_digest = {c.get("cure_id"): c.get("artifact_sha256") for c in claims}
    known = load_rulings(rulings) if rulings else None
    supers, out, refused, superseded = {}, [], 0, 0
''', '''    claims = [x for x in lines if x.get("record_type") != "supersession"]
    claim_digest = {c.get("cure_id"): c.get("artifact_sha256") for c in claims}
    counts = {}
    for c in claims:
        counts[c.get("cure_id")] = counts.get(c.get("cure_id"), 0) + 1
    dup = {k for k, n in counts.items() if n > 1}   # S1-19(b): one cure id, one claim line
    known = load_rulings(rulings) if rulings else None
    supers, out, refused, superseded = {}, [], 0, 0
    classes = []
''', "S1-19 (b) duplicate ids counted")
sub(VER, '''            elif known is not None:
                verb = known.get(m.group("xid"), {}).get(m.group("rid"))
                if verb not in SUPERSEDING_VERBS:
                    why.append("the rulings given do not show %s ruling %s as adopt, amend or close (found %r)"
                               % (m.group("xid"), m.group("rid"), verb))
''', '''            elif known is not None:
                verb = known.get(m.group("xid"), {}).get(m.group("rid"))
                if verb not in SUPERSEDING_VERBS:
                    why.append("the rulings given do not show %s ruling %s as adopt, amend or close (found %r)"
                               % (m.group("xid"), m.group("rid"), verb))
            if not HEX64.fullmatch(str(x["old_artifact_sha256"])):
                why.append("old_artifact_sha256 %r is not a 64-hex digest (S1-19(d))" % str(x["old_artifact_sha256"])[:20])
            if target in dup:
                why.append("the record retires %s, which appears on more than one claim line (S1-19(b))" % target)
        classes.append({"supersedes_cure_id": target, "ordered_by": x.get("ordered_by"), "ordered_by_class": classify_supersession(x)})
''', "S1-19 (b)(d) supersession checks and (e) classification")
sub(VER, '''    for c in claims:
        if c.get("cure_id") in supers:
''', '''    for c in claims:
        if c.get("cure_id") in dup:
            refused += 1
            out.append({"cure_id": c.get("cure_id"), "verdict": "REFUSED",
                        "reasons": ["%s appears on more than one claim line; a retired claim is superseded, never repeated "
                                    "(S1-19(b))" % c.get("cure_id")]})
            continue
        if c.get("cure_id") in supers:
''', "S1-19 (b) duplicate claim lines refused")
sub(VER, '            "results": out, "verdict": "GREEN" if not refused else "RED"}\n',
    '            "results": out, "supersession_classes": classes, "rulings_checked": known is not None,\n'
    '            "verdict": "GREEN" if not refused else "RED"}\n', "S1-19 (e) classes reported")
sub(VER, '    ap.add_argument("--selftest", action="store_true")\n',
    '    ap.add_argument("--selftest", action="store_true")\n'
    '    ap.add_argument("--require-rulings", action="store_true", help="a gating run: refuse when no --rulings is given (S1-19)")\n',
    "S1-19 --require-rulings")
sub(VER, '    d = run(a.claims, a.root, a.rulings)\n',
    '    if a.require_rulings and not a.rulings:\n'
    '        print(json.dumps({"status": "REFUSED", "why": "--require-rulings was given without --rulings"}))\n'
    '        return 1\n'
    '    d = run(a.claims, a.root, a.rulings)\n', "S1-19 --require-rulings enforced")
sub(VER, '                              "output_sha256": "abc"}],\n', '                              "output_sha256": "a" * 64}],\n',
    "S1-19 selftest good vector carries a digest shape")
sub(VER, '        ("artifact digest does not match disk", dict(good, artifact_sha256="1" * 64), "REFUSED"),\n',
    '        ("artifact digest does not match disk", dict(good, artifact_sha256="1" * 64), "REFUSED"),\n'
    '        ("S1-19(a) a claim naming no author", {k: v for k, v in good.items() if k != "author_attempt_id"}, "REFUSED"),\n'
    '        ("S1-19(d) an output digest that is not a digest",\n'
    '         dict(good, verification=[{"tool": "t.py", "artifact_sha256_at_run": d, "output_sha256": "not-a-digest"}]), "REFUSED"),\n'
    '        ("S1-19(d) an artifact digest that is not a digest", dict(good, artifact_sha256="not-a-digest"), "REFUSED"),\n',
    "S1-19 (a)(d) vectors")
sub(VER, '            ("T3-01 --rulings confirms the ordering ruling", genuine, [rf], ("SUPERSEDED", 0)),\n',
    '            ("S1-19(c) an ordering id joined by a hyphen is refused",\n'
    '             dict(genuine, ordered_by="test-adversarial#e1 ruling R5"), None, ("REFUSED", 2)),\n'
    '            ("S1-19(d) a supersession whose old digest is not a digest is refused",\n'
    '             dict(genuine, old_artifact_sha256="3" * 63 + "z"), None, ("REFUSED", 2)),\n'
    '            ("T3-01 --rulings confirms the ordering ruling", genuine, [rf], ("SUPERSEDED", 0)),\n', "S1-19 (c)(d) file-level vectors")
sub(VER, '''    return {"vectors": len(results), "failed": failed, "results": results,
            "verdict": "GREEN" if not failed else "RED"}
''', '''    cf = tmp / "claims_dup.jsonl"
    cf.write_text(json.dumps(dict(good, cure_id="DUP", artifact_sha256="4" * 64)) + "\\n" + json.dumps(dict(good, cure_id="DUP")) + "\\n",
                  encoding="utf-8")
    rep = run(cf, tmp, None)
    dv = [o["verdict"] for o in rep["results"] if o["cure_id"] == "DUP"]
    ok = dv == ["REFUSED", "REFUSED"] and rep["refused"] == 2
    failed += not ok
    results.append({"vector": "S1-19(b) two claim lines with one cure id are both refused", "got": dv, "ok": ok})
    rf2 = tmp / "rulings_names.json"
    rf2.write_text(json.dumps({"execution_id": "test_rulings_a1#e3", "rulings": [{"id": "V9", "ruling": "adopt", "decision": "retire OLD"}]}),
                   encoding="utf-8")
    cf = tmp / "claims_cls.jsonl"
    for name, rec_, rulings_, want in (
            ("S1-19(e) a ruling that names the retired cure id", dict(genuine, ordered_by="test_rulings_a1#e3 ruling V9"), [rf2],
             "ruling_names_retired_cure"),
            ("S1-19(e) R5 with its install receipt named", dict(genuine, why="install receipt X.json replaced the file"), [rf],
             "r5_with_trigger"),
            ("S1-19(e) neither form is classified, never refused", dict(genuine, why="changed"), [rf], "unclassified")):
        cf.write_text(json.dumps(stale) + "\\n" + json.dumps(rec_) + "\\n", encoding="utf-8")
        rep = run(cf, tmp, rulings_)
        got = [c_["ordered_by_class"] for c_ in rep["supersession_classes"]]
        ok = got == [want] and rep["superseded"] == 1
        failed += not ok
        results.append({"vector": name, "expected": want, "got": got, "ok": ok})
    return {"vectors": len(results), "failed": failed, "results": results,
            "verdict": "GREEN" if not failed else "RED"}
''', "S1-19 (b)(e) file-level vectors")

# ------------------------------------------------------------------ TOOLKIT.md (e)
sub(TK, "calendar-date onsets and dateline claims, Hebrew-quote binding |",
    "calendar-date onsets and dateline claims, Hebrew-quote binding in prose, and Hebrew inside a ref entry bound to that "
    "entry's own ref (S1-06) |", "TOOLKIT citation_sweep row")
sub(TK, "| every Hebrew run byte-true to the verse text or to a Qere; NFD-only matches stay defects |",
    "| every Hebrew run byte-true to the verse text or to a Qere, standing on word boundaries: no Hebrew letter or combining "
    "mark beside a pointed run, no Hebrew letter beside an unpointed one (S1-07; `collate_hebrew` applies the same rule); "
    "NFD-only matches stay defects |", "TOOLKIT normalizer row")
sub(TK, "| mark, K/Q and puncta claims in prose; mark-disclosure symmetry (FLAGS) |",
    "| mark, K/Q and puncta claims in prose, each bound to the verse numbers of its own clause (C:V, C.V, `MT C:V` or dotted); "
    "absence phrases scoped to the verse, range or chapter they name; a negated K/Q is an absence claim (S1-22); "
    "mark-disclosure symmetry (FLAGS) |", "TOOLKIT check_marks row")
sub(TK, "`check_atomic_isolation.py`, `_punct_boundary_sweep.py` — state their contracts in their\nown docstrings.\n",
    "`check_atomic_isolation.py`, `_punct_boundary_sweep.py` — state their contracts in their\nown docstrings. "
    "`check_register.py` carries the S1-05 arms (repair history, positional row references, strategy\n"
    "citations, governance posture), and `check_web_quotes.py` flags a prose field whose curly double\n"
    "quote counts differ (S1-10).\n", "TOOLKIT register and web_quotes sentence")

# ------------------------------------------------------------------ tests, section 10b
SECTION10B = r'''# 10b. TOOLFIX-2 per ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2 (b). Local helpers keep this file runnable against
# the tools that predate the edit, so its vectors can be shown to discriminate.
import unicodedata  # noqa: E402


def _mk10(ch):
    return unicodedata.category(ch) == "Mn"


def _lt10(ch):
    return "\u05d0" <= ch <= "\u05ea"


def _bnd10(needle, hay, marks=True):
    edge = (lambda ch: _lt10(ch) or _mk10(ch)) if marks else _lt10
    i = hay.find(needle)
    while i != -1:
        j = i + len(needle)
        if (i == 0 or not edge(hay[i - 1])) and (j >= len(hay) or not edge(hay[j])):
            return True
        i = hay.find(needle, i + 1)
    return False


def _skel10(s):
    return "".join(ch for ch in s if not _mk10(ch))


JOINED10 = " | ".join(OSHB.values())
SKEL10 = _skel10(JOINED10)


def _cases10():
    found = {}
    for key, verse in OSHB.items():
        for w in verse.split(" "):
            letters = [i for i, ch in enumerate(w) if _lt10(ch)]
            if len(letters) < 5:
                continue
            if "end" not in found and _mk10(w[-1]):
                k = len(w)
                while k and _mk10(w[k - 1]):
                    k -= 1
                if not _bnd10(w[:k], JOINED10):
                    found["end"] = (key, w, w[:k])
            if "start" not in found:
                rest = w[letters[1]:]
                if not _bnd10(rest, JOINED10):
                    found["start"] = (key, w, rest)
            if "root" not in found:
                sk = _skel10(w)
                inner = sk[1:-1]
                if len(inner) >= 3 and not _bnd10(inner, SKEL10, marks=False):
                    found["root"] = (key, w, inner)
            if len(found) == 3:
                return found
    return found


C10 = _cases10()
check("fixture: word-boundary cases found in the bytes (end, start, root)", set(C10) == {"end", "start", "root"}, sorted(C10))
Q72b = kq_split_bytes(PM["kq"]["Ezek.7.2"][0], OSHB["Ezek.7.2"])[1].replace("/", "")
W11b = OSHB["Ezek.1.1"].split(" ")
OTHER12b = next(w for w in OSHB["Ezek.1.2"].split(" ") if len([ch for ch in w if _lt10(ch)]) >= 3 and w not in OSHB["Ezek.1.1"])
UNMARKED1 = next(v for v in range(2, 28) if not PM["marks"].get("Ezek.1.%d" % v) and not PM["kq"].get("Ezek.1.%d" % v))
NOMARK_CH = next((c for c in range(1, 48) if not any(k.startswith("Ezek.%d." % c) for k in PM["marks"])), None)
NEXT_MARK = next(((int(k.split(".")[1]), int(k.split(".")[2])) for k in sorted(PM["marks"], key=lambda k: (int(k.split(".")[1]), int(k.split(".")[2])))
                  if NOMARK_CH and int(k.split(".")[1]) > NOMARK_CH), None)
check("fixture: MT 1:28 carries SAMEKH, MT 1:%d carries no mark and no K/Q" % UNMARKED1, "SAMEKH" in PM["marks"].get("Ezek.1.28", []), UNMARKED1)
check("fixture: a chapter with no parashah mark exists, followed by a marked verse", NOMARK_CH is not None and NEXT_MARK is not None,
      [NOMARK_CH, NEXT_MARK])
check("fixture: MT 33:16 carries a K/Q note and MT 40:1-4 carry none",
      bool(PM["kq"].get("Ezek.33.16")) and not any(PM["kq"].get("Ezek.40.%d" % v) for v in range(1, 5)))
S10B_CS_REFS = [
    ("cs_tf2b_s1_06_accent_stripped_qere_in_ref",
     ["oshb:Ezek.7.2 (K/Q, checked before quoting: ketiv ארבעת / qere אַרְבַּע, 'the four corners')"], "does not collate against its own ref"),
    ("cs_tf2b_s1_06_raw_qere_in_ref_ok", ["oshb:Ezek.7.2 (K/Q: qere %s)" % Q72b], None),
    ("cs_tf2b_s1_06_undisclosed_qere_in_ref", ["oshb:Ezek.7.2 (the reading %s)" % Q72b], "matches the Qere of its own ref"),
    ("cs_tf2b_s1_06_own_verse_words_ok", ["oshb:Ezek.1.1 (%s %s)" % (W11b[1], W11b[2])], None),
    ("cs_tf2b_s1_06_other_verse_words", ["oshb:Ezek.1.1 (%s)" % OTHER12b], "does not collate against its own ref"),
    ("cs_tf2b_s1_06_named_other_ref_does_not_rebind", ["oshb:Ezek.1.1 (cf. oshb:Ezek.1.2 %s)" % OTHER12b], "does not collate against its own ref"),
]
S10B_CS_PROSE = [
    ("cs_tf2b_s1_07_cut_at_word_end", "the splice %s (oshb:%s) closes the unit" % (C10["end"][2], C10["end"][0]), "does not collate against any nearby cited ref"),
    ("cs_tf2b_s1_07_cut_at_word_start", "the splice %s (oshb:%s) closes the unit" % (C10["start"][2], C10["start"][0]), "does not collate against any nearby cited ref"),
    ("cs_tf2b_s1_07_root_inside_word", "the root %s (oshb:%s) recurs" % (C10["root"][2], C10["root"][0]), "does not collate against any nearby cited ref"),
    ("cs_tf2b_s1_07_whole_word_ok", "the splice %s (oshb:%s) closes the unit" % (C10["end"][1], C10["end"][0]), None),
]
S10B_REG = [
    ("reg_tf2b_originally_drafted", {"strongest_rejected_alternative": "the span as originally drafted ran to 7:27"}, "author_wave_register_s1_05"),
    ("reg_tf2b_former_span", {"device_notes": "the former span held one refrain"}, "author_wave_register_s1_05"),
    ("reg_tf2b_prior_reading", {"device_notes": "keeping the prior paragraph reading"}, "author_wave_register_s1_05"),
    ("reg_tf2b_correction_earlier", {"device_notes": "a correction to an earlier grouping"}, "author_wave_register_s1_05"),
    ("reg_tf2b_next_row", {"boundary_rationale": "the onset of the next row's unit"}, "author_wave_register_s1_05"),
    ("reg_tf2b_row_after", {"boundary_rationale": "the row after this unit closes on the refrain"}, "author_wave_register_s1_05"),
    ("reg_tf2b_last_of_rows", {"device_notes": "the last of three rows"}, "author_wave_register_s1_05"),
    ("reg_tf2b_strategy_s", {"device_notes": "matches the strategy's own naming"}, "author_wave_register_s1_05"),
    ("reg_tf2b_order_s", {"device_notes": "rather than the order's own ceiling"}, "author_wave_register_s1_05"),
    ("reg_tf2b_posture", {"device_notes": "held under the flagged-region posture"}, "author_wave_register_s1_05"),
    ("reg_tf2b_officially_inventoried", {"device_notes": "a messenger formula, officially inventoried"}, "author_wave_register_s1_05"),
    ("reg_tf2b_ends_the_part", {"device_notes": "the utterance formula ends the part"}, "author_wave_register_s1_05"),
    ("reg_tf2b_the_part_s", {"device_notes": "the part's close"}, "author_wave_register_s1_05"),
    ("reg_tf2b_green_part_of_the_court_ok", {"boundary_rationale": "the measuring covers part of the court"}, None),
    ("reg_tf2b_green_order_of_the_gates_ok", {"boundary_rationale": "the order of the gates follows the court"}, None),
]
S10B_CM = [
    ("cm_tf2b_s1_22_cv_form_own_clause_ok",
     {"boundary_rationale": "a setumah is recorded after 1:28; the unit then turns at oshb:Ezek.1.%d" % UNMARKED1}, {"paragraph_mark_claim": False}),
    ("cm_tf2b_s1_22_mt_form_type_mismatch_flags", {"boundary_rationale": "a petuchah is recorded after MT 1:28"}, {"paragraph_mark_claim": True}),
    ("cm_tf2b_s1_22_absence_named_unmarked_verse_ok",
     {"boundary_rationale": "no setumah stands after 1:%d" % UNMARKED1, "span": "Ezek.1.1-Ezek.1.28"}, {"false_mark_absence_claim": False}),
    ("cm_tf2b_s1_22_absence_named_marked_verse_flags",
     {"boundary_rationale": "no setumah stands after 1:28", "span": "Ezek.1.1-Ezek.1.28"}, {"false_mark_absence_claim": True}),
    ("cm_tf2b_s1_22_absence_chapter_named_ok",
     {"boundary_rationale": "chapter %s carries no parashah mark" % NOMARK_CH,
      "span": "Ezek.%s.1-Ezek.%s.%s" % (NOMARK_CH, NEXT_MARK[0] if NEXT_MARK else 0, NEXT_MARK[1] if NEXT_MARK else 0)}, {"false_mark_absence_claim": False}),
    ("cm_tf2b_s1_22_negated_kq_near_dotted_ref_ok",
     {"boundary_rationale": "No K/Q or editorial note touches oshb:Ezek.40.1-4", "span": "Ezek.40.1-Ezek.40.4"},
     {"kq_claim": False, "false_kq_absence_claim": False}),
    ("cm_tf2b_s1_22_negated_kq_named_verse_flags", {"boundary_rationale": "no K/Q stands at 33:16"}, {"false_kq_absence_claim": True}),
    ("cm_tf2b_s1_22_kq_claim_cv_form_flags", {"boundary_rationale": "the qere at 1:%d is disclosed" % UNMARKED1}, {"kq_claim": True}),
]
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "tf2b_cs.jsonl"
    p.write_text("\n".join([json.dumps({"decision_id": d, "boundary_evidence_refs": refs}, ensure_ascii=False) for d, refs, _ in S10B_CS_REFS]
                           + [json.dumps({"decision_id": d, "boundary_rationale": prose}, ensure_ascii=False) for d, prose, _ in S10B_CS_PROSE]),
                 encoding="utf-8")
    rep = run("citation_sweep.py", p)
    for did, _, expect in S10B_CS_REFS + S10B_CS_PROSE:
        mine = [x for x in rep["problems"] if x.startswith(did + ":")]
        check("citation_sweep %s: %s" % (did, "no problem" if expect is None else repr(expect)),
              (not mine) if expect is None else any(expect in x for x in mine), mine)
    for label, payload, want in (("normalize tf2b S1-07: a run cut at its word's end is a defect", {"a": "x %s y" % C10["end"][2]}, 1),
                                 ("normalize tf2b S1-07: a run cut at its word's start is a defect", {"b": "x %s y" % C10["start"][2]}, 1),
                                 ("normalize tf2b S1-07: an unpointed root inside a word is a defect", {"c": "x %s y" % C10["root"][2]}, 1),
                                 ("normalize tf2b S1-07: the whole word stays byte-true", {"d": "x %s y" % C10["end"][1]}, 0)):
        fp = Path(td) / ("tf2b_norm_%s.json" % list(payload)[0])
        fp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.run([sys.executable, str(HERE / "normalize_hebrew_in_json.py"), str(fp)],
                              capture_output=True, text=True, encoding="utf-8", env=ENV)
        nrep = json.loads(proc.stdout.strip().splitlines()[-1])
        check(label, nrep["defect_count"] == want, nrep)
    p = Path(td) / "tf2b_reg.jsonl"
    p.write_text("\n".join(json.dumps(dict({"decision_id": d}, **fields), ensure_ascii=False) for d, fields, _ in S10B_REG), encoding="utf-8")
    rep = run("check_register.py", p)
    for d, _, cls in S10B_REG:
        mine = [fl for fl in rep["flags"] if fl.get("decision_id") == d]
        check("check_register %s: %s" % (d, cls or "no flag of any class"), (not mine) if cls is None else any(fl.get("class") == cls for fl in mine), mine)
    p = Path(td) / "tf2b_wq.jsonl"
    p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in (
        {"decision_id": "wq_tf2b_s1_10_unequal", "boundary_rationale": "“Son of man, set your face toward Sidon (web:Ezek.28.21)."},
        {"decision_id": "wq_tf2b_s1_10_balanced_ok", "boundary_rationale": "“Son of man, set your face toward Sidon” (web:Ezek.28.21)."},
        {"decision_id": "wq_tf2b_s1_10_apostrophes_ok", "boundary_rationale": "Yahweh’s word stands (web:Ezek.28.21)."})), encoding="utf-8")
    rep = run("check_web_quotes.py", p)
    for d, fires in (("wq_tf2b_s1_10_unequal", True), ("wq_tf2b_s1_10_balanced_ok", False), ("wq_tf2b_s1_10_apostrophes_ok", False)):
        mine = [fl for fl in rep["flags"] if "e15d" in str(fl.get("issue")) and fl.get("decision_id") == d]
        check("check_web_quotes %s: e15d %s" % (d, "fires" if fires else "silent"), bool(mine) == fires, rep["flags"])
    p = Path(td) / "tf2b_cm.jsonl"
    p.write_text("\n".join(json.dumps(dict({"decision_id": d}, **f), ensure_ascii=False) for d, f, _ in S10B_CM), encoding="utf-8")
    rep = run("check_marks.py", p)
    for d, _, expect in S10B_CM:
        for rule, fires in expect.items():
            mine = [fl for fl in rep["flags"] if fl.get("decision_id") == d and fl.get("rule") == rule]
            check("check_marks %s: %s %s" % (d, rule, "fires" if fires else "silent"), bool(mine) == fires, mine)

'''
sub(TEST, 'failed = [r for r in results if not r["ok"]]\n', SECTION10B + 'failed = [r for r in results if not r["ok"]]\n', "section 10b vectors")

# ------------------------------------------------------------------ regenerate
pins = ["citation_sweep.py=" + sha(T / "citation_sweep.py"), "check_marks.py=" + sha(T / "check_marks.py")]
g = run([ADAPT, "--replace"] + pins)
out = {"applied": applied, "regen_exit": g.returncode, "regen": g.stdout.strip().splitlines()[-6:], "regen_err": g.stderr[-1500:]}
if g.returncode != 0:
    print(json.dumps(out, ensure_ascii=False, indent=1))
    raise SystemExit(1)


def json_or_tail(p):
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"error": True, "exit": p.returncode, "stdout_tail": p.stdout[-1500:], "stderr_tail": p.stderr[-1500:]}


def test_summary(d):
    if d.get("error"):
        return d
    return {"checks": d["checks"], "passed": d["passed"], "verdict": d["verdict"], "failed": [f.get("check", "") for f in d["failed"]],
            "failed_detail": [{"check": f.get("check"), "detail": str(f.get("detail"))[:300]} for f in d["failed"]]}


staged_tests = test_summary(json_or_tail(run([TEST])))
out["tests"] = staged_tests
lib = json_or_tail(run([LIB]))
out["ezek_lib_selftest"] = {k: lib.get(k) for k in ("checks", "passed", "failed", "verdict", "error", "stdout_tail", "stderr_tail") if k in lib}
out["toolkit_selfcheck"] = {k: v for k, v in json_or_tail(run([T / "_toolkit_selfcheck.py"])).items() if k in ("checks", "passed", "verdict", "error", "stdout_tail")}
vs = json_or_tail(run([VER, "--selftest"], ST / "campaign"))
out["verifier_selftest"] = {"vectors": vs.get("vectors"), "failed": vs.get("failed"), "verdict": vs.get("verdict"),
                            "failed_vectors": [r for r in vs.get("results", []) if not r.get("ok")], **({"error": vs} if vs.get("error") else {})}
rulings = [SP / "Ezek" / "ezek_controlling_agent_rulings.v1.json", SP / "Ezek" / "ezek_controlling_agent_rulings_e3.v1.json",
           SP / "Ezek" / "ezek_controlling_agent_rulings_e4.v1.json"]
out["verifier_real_claims"] = {}
for cf in ("ezek_cure_claims.v1.jsonl", "ezek_cure_claims_toolkit_repair.v1.jsonl"):
    vr = json_or_tail(run([VER, "--claims", SP / "Ezek" / cf, "--root", SP / "Ezek", "--rulings"] + rulings + ["--require-rulings"], ST / "campaign"))
    out["verifier_real_claims"][cf] = {k: vr.get(k) for k in ("claims", "accepted", "refused", "superseded", "supersession_classes", "verdict", "error")}

# ------------------------------------------------------------------ corpus impact (condition (c))
s = run([T / "run_validator_suite.py", SUITE / "rows.jsonl"])
new = json.loads((SUITE / "rows.jsonl.validator_report.json").read_text(encoding="utf-8"))
old = json.loads((SP / "Ezek" / "repair" / "suite_after_t4fix_batch2" / "rows.jsonl.validator_report.json").read_text(encoding="utf-8"))
KNOWN_S1_07_ROWS = {"P03-004", "P03-005", "P03-006", "P03-010", "P03-012", "P03-017", "P03-019"}
KNOWN_S1_06_ROWS = {"P01-012"}
KNOWN_NORMALIZER_RUNS = {"אַרְבַּע", "וְהָרָשָׁ֗ע כִּ֤י יָשׁוּב", "וְהָשִׁ֖יבוּ וִֽחְיֽו", "וַתְּהִ֥י לְהֶֽפֶך", "וַתִּקְחִ֞י אֶת בָּנַ֤יִךְ וְאֶת בְּנוֹתַ֨יִך",
                         "לָכֵ֞ן כֹּה אָמַ֨ר אֲדֹנָ֣י יְהוִה֮ חַי אָנִי", "עַ֖ל כָּל תּוֹעֲבֹתָֽיִך", "תִּיבַ֣שׁ יָבֹ֔ש"}
TQ_REMOVAL_ROWS = {"paragraph_mark_claim": {"P01-001", "P01-011", "P01-013", "P02-013", "P05-001", "P05-002", "P05-003", "P05-004"},
                   "false_mark_absence_claim": {"P02-005", "P02-018", "P02-019", "P04-002", "P10-001", "P10-013"},
                   "kq_claim": {"P08-001", "P08-007", "P10-001", "P10-014"}}


def jset(xs):
    return {json.dumps(x, sort_keys=True, ensure_ascii=False) for x in xs}


def list_of(rep, path):
    cur = rep
    for p in path.split("."):
        cur = (cur or {}).get(p) if isinstance(cur, dict) else None
    return cur if isinstance(cur, list) else []


impact = {"summaries": {"installed": old.get("summary"), "staged": new.get("summary")}, "lists": {}}
for k in sorted(set(old) | set(new)):
    oa, nb = old.get(k), new.get(k)
    if isinstance(oa, dict) and isinstance(nb, dict):
        for kk in sorted(set(oa) | set(nb)):
            la, lb = oa.get(kk), nb.get(kk)
            if isinstance(la, list) and isinstance(lb, list):
                sa, sb = jset(la), jset(lb)
                if sa != sb:
                    impact["lists"]["%s.%s" % (k, kk)] = {"installed": len(la), "staged": len(lb),
                                                          "added": [json.loads(x) for x in sorted(sb - sa)],
                                                          "removed": [json.loads(x) for x in sorted(sa - sb)]}
cs_added = impact["lists"].get("citation_sweep.problems", {}).get("added", [])
norm_added = impact["lists"].get("hebrew_normalize_dryrun.defects", {}).get("added", [])
cs_classes = {"S1-07_known": [], "S1-06_known": [], "NEW_CLASS": []}
for pr in cs_added:
    row = str(pr).split(":", 1)[0]
    if "[CWO-EZ-16]" in str(pr) and row in KNOWN_S1_06_ROWS:
        cs_classes["S1-06_known"].append(pr)
    elif "does not collate against any nearby cited ref" in str(pr) and row in KNOWN_S1_07_ROWS:
        cs_classes["S1-07_known"].append(pr)
    else:
        cs_classes["NEW_CLASS"].append(pr)
norm_classes = {"known": [r for r in norm_added if str(r) in KNOWN_NORMALIZER_RUNS], "NEW_CLASS": [r for r in norm_added if str(r) not in KNOWN_NORMALIZER_RUNS]}
marks_changes = {}
for key, v in impact["lists"].items():
    if key.startswith("mark_symmetry") or "check_marks" in key or key.endswith("marks.flags"):
        for direction in ("removed", "added"):
            for fl in v[direction]:
                if isinstance(fl, dict):
                    rule, row = fl.get("rule"), fl.get("decision_id")
                    tq = row in TQ_REMOVAL_ROWS.get(rule, set())
                    marks_changes.setdefault(direction, []).append({"rule": rule, "row": row, "tq_named_row": tq})
impact["hard_classes"] = {"citation_sweep": {k: len(v) for k, v in cs_classes.items()}, "normalizer": {k: len(v) for k, v in norm_classes.items()},
                          "NEW_HARD_CLASS_ITEMS": cs_classes["NEW_CLASS"] + norm_classes["NEW_CLASS"]}
impact["flags_changes_check_marks"] = marks_changes
impact["removed_flags_outside_tq_rows"] = [c for c in marks_changes.get("removed", []) if not c["tq_named_row"]]
out["suite_exit"] = s.returncode
out["corpus_impact_summary"] = {"lists_moved": {k: {"installed": v["installed"], "staged": v["staged"], "added": len(v["added"]), "removed": len(v["removed"])}
                                                for k, v in impact["lists"].items()},
                                "hard_classes": impact["hard_classes"], "removed_flags_outside_tq_rows": impact["removed_flags_outside_tq_rows"][:40],
                                "summaries": impact["summaries"]}
(ROOT / "corpus_impact.json").write_text(json.dumps(impact, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")

# ------------------------------------------------------------------ discrimination against the installed tools
BASE = SCR / "stage_tf2b_base_installed"
if BASE.exists():
    shutil.rmtree(BASE)
shutil.copytree(SP / "Ezek" / "tools", BASE / "sp_durable" / "Ezek" / "tools", ignore=ign)
shutil.copytree(SP / "Jer" / "tools", BASE / "sp_durable" / "Jer" / "tools", ignore=ign)
for f in (SP / "Ezek").iterdir():
    if f.is_file():
        shutil.copy2(f, BASE / "sp_durable" / "Ezek" / f.name)
shutil.copyfile(TEST, BASE / "sp_durable" / "Ezek" / "tools" / "_test_zone_tools_ezek.py")
base_tests = test_summary(json_or_tail(run([BASE / "sp_durable" / "Ezek" / "tools" / "_test_zone_tools_ezek.py"], BASE / "sp_durable" / "Ezek" / "tools")))
new_ids = [d for d, _, _ in S10B_CS_REFS_IDS] if False else None
out["discrimination_installed"] = {"checks": base_tests.get("checks"), "passed_on_installed": base_tests.get("passed"),
                                   "failed_on_installed": base_tests.get("failed"), "error": base_tests.get("error")}
out["staged_digests"] = {n: sha(T / n) for n in ("citation_sweep.py", "check_marks.py", "_adapt_zone_tools_ezek.py", "_test_zone_tools_ezek.py", "TOOLKIT.md",
                                                   "ezek_lib.py", "normalize_hebrew_in_json.py", "check_register.py", "check_web_quotes.py")}
out["staged_digests"]["campaign/_cure_verification.py"] = sha(VER)
(ROOT / "stage_run.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps(out, ensure_ascii=False, indent=1))
