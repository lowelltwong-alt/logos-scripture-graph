"""Stage TOOLFIX-2 (S1-05, S1-06, S1-07, S1-10, S1-19) on top of TOOLFIX-1, in session scratch only, and test it.

The stage is rebuilt from SP on every run, so nothing carries over between runs:
  - SP/Ezek/tools, SP/Jer/tools, the SP/Ezek top-level files and the chain head are copied, and so is
    SP/campaign/_cure_verification.py;
  - TOOLFIX-1's staged files are laid over them from SP/Ezek/proposals/t4fix_batch1/staged, each checked against its
    manifest digest.

Every replacement is exact and count-checked. The edits:
  A ezek_lib.py            S1-07  collate_hebrew's byte and nfd tiers become grapheme-bounded (bounded_find), with selftest
                                  vectors built from the bytes;
  B normalize_hebrew_*.py  S1-07  byte presence and the Qere tier become grapheme-bounded;
  C _adapt_zone_tools_*.py S1-06  a REF HEBREW arm binds Hebrew inside a ref entry to that entry's own ref (and regenerates
                                  citation_sweep.py);
  D check_register.py      S1-05  arms for repair history, positional row references, strategy citations and governance
                                  posture, and a scan of every ref annotation;
  E check_web_quotes.py    S1-10  every flag names its decision_id (the e15a pairing arm already fires on all 10 rows; S1's
                                  claim that it has no such arm is refuted by the tool's own output);
  F _cure_verification.py  S1-19  (a) author named, (b) one line per cure id, (c) an attempt-shaped ordering id plus
                                  --require-rulings and a warning, (d) a real output digest, (e) a warning when the
                                  ordering ruling does not name the retired cure;
  G TOOLKIT.md                    rows and a paragraph for the above;
  T _test_zone_tools_*.py         section 10, with vectors both ways (local helpers keep it runnable against older tools).
Then it regenerates the zone tools, runs the zone tests, the ezek_lib selftest, the toolkit selfcheck, and the verifier's
selftest and real claims, and runs the suite over the chain head, comparing it list by list with the installed tools' report.
Nothing is installed."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
SCR = Path(__file__).resolve().parent
ROOT = SCR / "stage_toolfix2"
ST = ROOT / "sp_durable"
T = ST / "Ezek" / "tools"
B1 = SP / "Ezek" / "proposals" / "t4fix_batch1"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
applied = []


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sub(path, old, new, label, count=1):
    t = path.read_text(encoding="utf-8")
    n = t.count(old)
    if n != count:
        raise SystemExit("ABORT: %s: expected %d occurrence(s) in %s, found %d" % (label, count, path.name, n))
    path.write_text(t.replace(old, new), encoding="utf-8", newline="\n")
    applied.append(label)


def run(args, cwd=T):
    return subprocess.run([sys.executable] + [str(a) for a in args], capture_output=True, text=True, encoding="utf-8",
                          env=ENV, cwd=str(cwd))


# ---------------------------------------------------------------- stage
man = json.loads((B1 / "manifest.json").read_text(encoding="utf-8"))
rec = json.loads((SP / "campaign" / "receipts" / "ezek_tools_install_r4ii_cal1.json").read_text(encoding="utf-8"))
for n, f in rec["files"].items():
    if sha(SP / "Ezek" / "tools" / n) != f["after"]:
        raise SystemExit("ABORT: SP tools/%s is not the installed digest" % n)
assert ROOT.parent == SCR and ROOT.name == "stage_toolfix2"
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
SUITE = ST / "Ezek" / "repair" / "suite_toolfix2"
SUITE.mkdir(parents=True)
shutil.copy2(SP / "Ezek" / "repair" / "rows_v3_cwo12.jsonl", SUITE / "rows.jsonl")
for n, f in man["files"].items():
    src = B1 / "staged" / n
    if sha(src) != f["staged_sha256"]:
        raise SystemExit("ABORT: batch1 staged %s does not match its manifest" % n)
    shutil.copyfile(src, T / n)
applied.append("TOOLFIX-1 staged files laid over the SP copy (manifest-checked)")

LIB, NORM, ADAPT = T / "ezek_lib.py", T / "normalize_hebrew_in_json.py", T / "_adapt_zone_tools_ezek.py"
REG, WQ, TK, TEST = T / "check_register.py", T / "check_web_quotes.py", T / "TOOLKIT.md", T / "_test_zone_tools_ezek.py"
VER = ST / "campaign" / "_cure_verification.py"

# ---------------------------------------------------------------- A  ezek_lib (S1-07)
sub(LIB, "def collate_hebrew(quoted: str, source_text: str) -> str:\n", r'''def is_mark(ch: str) -> bool:
    """A combining mark (Unicode category Mn): points, accents, dagesh, the shin and sin dots, U+05C4. Maqaf, paseq and sof
    pasuq are not marks."""
    return unicodedata.category(ch) == "Mn"


def bounded_find(hay: str, needle: str, pos: int = 0) -> int:
    """The first index >= pos where needle occurs in hay on grapheme boundaries: the needle may not begin with a combining
    mark, and the character after it may not be one. -1 when there is none (S1-07, ezek_author_wave_spot_review_s1_a1#e1:
    a splice cut inside a grapheme is not byte-true)."""
    if not needle or is_mark(needle[0]):
        return -1
    i = hay.find(needle, pos)
    while i != -1:
        j = i + len(needle)
        if j >= len(hay) or not is_mark(hay[j]):
            return i
        i = hay.find(needle, i + 1)
    return -1


def bounded_in(needle: str, hay: str) -> bool:
    return bounded_find(hay, needle) != -1


def collate_hebrew(quoted: str, source_text: str) -> str:
''', "A1 ezek_lib is_mark / bounded_find / bounded_in")
sub(LIB, "    'byte' | 'nfd' | 'accent_stripped' | 'skeleton' | 'none'. Ellipsis-aware: fragments must match IN ORDER.\"\"\"\n",
    "    'byte' | 'nfd' | 'accent_stripped' | 'skeleton' | 'none'. Ellipsis-aware: fragments must match IN ORDER. At the byte and\n"
    "    nfd tiers every fragment matches on grapheme boundaries (bounded_find), so a splice cut inside a grapheme is not\n"
    "    byte-true (S1-07).\"\"\"\n", "A2 collate_hebrew docstring")
sub(LIB, "    def ordered(hay: str, needles: list[str]) -> bool:\n        pos = 0\n        for n in needles:\n            i = hay.find(n, pos)\n",
    "    def ordered(hay: str, needles: list[str], bounded: bool) -> bool:\n        pos = 0\n        for n in needles:\n"
    "            i = bounded_find(hay, n, pos) if bounded else hay.find(n, pos)\n", "A3 ordered() bounded")
sub(LIB, "        if ordered(xf(source_text), [xf(f) for f in frags]):\n",
    "        if ordered(xf(source_text), [xf(f) for f in frags], tier in (\"byte\", \"nfd\")):\n", "A4 byte and nfd tiers bounded")
sub(LIB, "    failed = [n for n, ok in checks if not ok]\n", r'''    # S1-07 (ezek_author_wave_spot_review_s1_a1#e1): the byte tier is grapheme-bounded. The cases are found in the bytes.
    def _first_cut(want_shin_dot):
        for key in sorted(oshb, key=lambda k: (int(k.split(".")[1]), int(k.split(".")[2]))):
            verse = oshb[key]
            for w in verse.split(" "):
                if not w or not is_mark(w[-1]):
                    continue
                k = len(w)
                while k and is_mark(w[k - 1]):
                    k -= 1
                cut = w[:k]
                if want_shin_dot and not ("\u05e9" == cut[-1:] and "\u05c1" in w[k:]):
                    continue
                if len(re.sub("[^\u05d0-\u05ea]", "", cut)) >= 2 and not bounded_in(cut, verse):
                    return key, verse, w, cut
        return None
    case = _first_cut(False)
    checks.append(("REGRESSION S1-07 a splice cut before its word's final marks is not byte; the whole word is",
                   case is not None and collate_hebrew(case[3], case[1]) != "byte" and collate_hebrew(case[2], case[1]) == "byte"))
    case = _first_cut(True)
    checks.append(("REGRESSION S1-07 a shin written without its shin dot is not byte",
                   case is not None and collate_hebrew(case[3], case[1]) != "byte"))
    w11 = oshb["Ezek.1.1"].split(" ")
    checks.append(("S1-07 whole words, and an ellipsis of whole words, stay byte",
                   collate_hebrew(w11[1], oshb["Ezek.1.1"]) == "byte"
                   and collate_hebrew(w11[1] + " … " + w11[3], oshb["Ezek.1.1"]) == "byte"))
    checks.append(("S1-07 a quote that begins with a combining mark is never byte",
                   is_mark(w11[1][1]) and collate_hebrew(w11[1][1:], oshb["Ezek.1.1"]) != "byte"))

    failed = [n for n, ok in checks if not ok]
''', "A5 ezek_lib selftest vectors")

# ---------------------------------------------------------------- B  normalizer (S1-07)
sub(NORM, "(letters/points + internal spaces/maqaf) must be a byte-identical substring of\nEzek_oshb.txt.",
    "(letters/points + internal spaces/maqaf) must be a byte-identical substring of\nEzek_oshb.txt that ends on a grapheme "
    "boundary: a run the source continues with a combining mark is a\nsplice cut inside a grapheme and is a defect (S1-07; "
    "the same rule holds at the Qere tier).", "B1 normalizer docstring")
sub(NORM, "MIN_LEN = 2   # lesson f (Ps close): the standard re-splice cure runs MIN_LEN=2\n",
    "MIN_LEN = 2   # lesson f (Ps close): the standard re-splice cure runs MIN_LEN=2\n"
    "sys.path.insert(0, str(FREEZE))\n"
    "from ezek_lib import bounded_in  # noqa: E402   S1-07: byte presence is grapheme-bounded\n", "B2 normalizer import")
sub(NORM, "def find_source_bytes(run: str, src: str, verses: list[str]) -> str | None:\n    if run in src:\n        return run\n",
    "def find_source_bytes(run: str, src: str, verses: list[str]) -> str | None:\n    if bounded_in(run, src):\n        return run\n",
    "B3 find_source_bytes bounded")
sub(NORM, "        if run in src:\n            stats[\"ok\"] += 1\n", "        if bounded_in(run, src):\n            stats[\"ok\"] += 1\n",
    "B4 fix_string byte tier bounded")
sub(NORM, "        if run in KQ[\"qere\"]:\n", "        if bounded_in(run, KQ[\"qere\"]):\n", "B5 fix_string Qere tier bounded")

# ---------------------------------------------------------------- C  adapt script: REF HEBREW arm (S1-06)
sub(ADAPT, 'CS_CAL_ONSET = r"""', r'''CS_REF_HEBREW_ARM = r"""            # REF HEBREW arm (Ezek; S1-06, ezek_author_wave_spot_review_s1_a1#e1): Hebrew inside a ref entry binds to that
            # entry's own ref (every verse of its range) or to an oshb: ref or MT qualifier named inside the annotation. A
            # pointed run must collate at byte tier (grapheme-bounded), an unpointed run at any tier. A Qere of those
            # verses (raw note bytes) counts only when the entry itself carries a ketiv/qere word.
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
                keys_ += [f"Ezek.{a_ or c2_}.{b_ or d2_}"
                          for a_, b_, c2_, d2_ in re.findall(r"oshb:Ezek\.(\d+)\.(\d+)|\bMT\s+(\d+)[:.](\d+)", tail)]
                texts_ = " | ".join(oshb_texts.get(k_, {}).get("text", "") for k_ in keys_)
                qere_ = (" | ".join(kq_split_bytes(n_, oshb_texts.get(k_, {}).get("text", ""))[1].replace("/", "")
                                    for k_ in keys_ for n_ in kq.get(k_, []))
                         if KQ_WORD.search(tail) else "")
                for r_ in ref_runs_:
                    pointed_ = bool(POINTED.search(r_))
                    t_ = collate_hebrew(r_, texts_)
                    tq_ = collate_hebrew(r_, qere_) if qere_.strip(" |") else "none"
                    if not (("byte" in (t_, tq_)) if pointed_ else (t_ != "none" or tq_ != "none")):
                        problems.append(f"{did}: Hebrew {r_[:25]!r}… in ref entry {ref!r} does not collate against its "
                                        f"own ref or a ref it names (tier {t_}, qere tier {tq_}, "
                                        f"{'pointed' if pointed_ else 'unpointed'})")
"""

CS_CAL_ONSET = r"""''', "C1 CS_REF_HEBREW_ARM defined")
sub(ADAPT, "CS_PUNCTA_ARM + CS_CAL_REF_ARM + kq_line_ezek", "CS_PUNCTA_ARM + CS_CAL_REF_ARM + CS_REF_HEBREW_ARM + kq_line_ezek",
    "C2 REF HEBREW arm wired into the ref loop")

# ---------------------------------------------------------------- D  check_register (S1-05)
sub(REG, "Scans ONLY the canonical prose fields (boundary_rationale,\nstrongest_rejected_alternative, device_notes) of row objects;",
    "Scans the canonical prose fields (boundary_rationale,\nstrongest_rejected_alternative, device_notes) of row objects and, "
    "since S1-05, the\nannotation of every boundary_evidence_refs entry (the text after its leading ref token);", "D1 register docstring")
sub(REG, 'PROSE_FIELDS = ("boundary_rationale", "strongest_rejected_alternative", "device_notes")\n',
    'PROSE_FIELDS = ("boundary_rationale", "strongest_rejected_alternative", "device_notes")\n'
    'REF_TOKEN = re.compile(r"^\\s*(?:oshb|web):Ezek\\.\\d+\\.\\d+(?:-(?:Ezek\\.)?\\d+\\.\\d+)?")   # S1-05: annotations are read after it\n',
    "D2 REF_TOKEN")
sub(REG, '        r"\\b(?:previous|next|preceding|following) (?:decision|entry)\\b", re.I),\n',
    '        r"\\b(?:previous|next|preceding|following) (?:decision|entry)\\b|"\n'
    "        # S1-05: without 'the', possessive, before/after, and 'one/middle/last of N ... rows'\n"
    '        r"\\b(?:preceding|next|following|previous|prior) row(?:[\'’]s)?\\b|\\brow (?:before|after)\\b|"\n'
    '        r"\\b(?:one|middle|last|first) of (?:the )?\\w+\\b[^.;]{0,20}?\\brows\\b", re.I),\n', "D3 positional arm widened")
sub(REG, '        r"\\bgate ruling\\b|\\bowner gate\\b", re.I),\n',
    '        r"\\bgate ruling\\b|\\bowner gate\\b|\\bstrategy[\'’]s\\b|\\bthe strategy\\b", re.I),   # S1-05\n', "D4 strategy arm widened")
sub(REG, '    "staged_file_stem": re.compile(\n', r'''    # S1-05 (ezek_author_wave_spot_review_s1_a1#e1): repair history and governance posture the author wave added
    "row_history_narration": re.compile(
        r"\b(?:as )?originally drafted\b|\bformer (?:single )?(?:[\d.:-]+ )?(?:\w+-verse )?(?:span|row|reading|grouping)\b|"
        r"\bprior [\d.:-]+ reading\b|\bkeeping the prior\b|\bpreviously held\b|\bcorrection to an earlier\b|"
        r"\bearlier grouping\b", re.I),
    "governance_posture": re.compile(
        r"\bposture\b|\bofficially inventoried\b|\bthe (?:ruling|order)['’]s\b|\bends the part\b|\bthe part['’]s\b", re.I),
    "staged_file_stem": re.compile(
''', "D5 new register classes")
sub(REG, '                                      "context": s[max(0, m.start() - 60):m.start() + 80]})\n    by_class = {}\n',
    r'''                                      "context": s[max(0, m.start() - 60):m.start() + 80]})
            # S1-05: the annotation of every ref entry is prose too (the text after its leading ref token)
            for i, ref in enumerate(row.get("boundary_evidence_refs") or []):
                if not isinstance(ref, str):
                    continue
                ann = REF_TOKEN.sub("", ref, count=1)
                masked = HEB_RUN.sub(" ", ann)
                masked = re.sub(r"“[^”]*”", lambda m: " " * len(m.group(0)), masked)
                for cls, pat in CLASSES.items():
                    for m in pat.finditer(masked):
                        flags.append({"file": Path(f).name, "decision_id": did,
                                      "field": "boundary_evidence_refs[%d]" % i, "class": cls,
                                      "match": m.group(0)[:60],
                                      "context": ann[max(0, m.start() - 60):m.start() + 80]})
    by_class = {}
''', "D6 register scans ref annotations")

# ---------------------------------------------------------------- E  check_web_quotes (S1-10)
sub(WQ, "def curly_pairing_broken(s: str):\n", r'''def decision_id_for(data, path: str):
    """S1-10 (ezek_author_wave_spot_review_s1_a1#e1): the row a flag's path points into, named by its decision_id, so a
    row-keyed triage or coverage predicate cannot miss a flag whose path is only an array index."""
    rows = data.get("decisions") if isinstance(data, dict) else data
    m = re.match(r"^(?:decisions)?\[(\d+)\]", path or "")
    if not m or not isinstance(rows, list) or int(m.group(1)) >= len(rows) or not isinstance(rows[int(m.group(1))], dict):
        return None
    return rows[int(m.group(1))].get("decision_id") or rows[int(m.group(1))].get("writer_decision_id")


def curly_pairing_broken(s: str):
''', "E1 decision_id_for")
sub(WQ, "        data = load_any(Path(f))\n", "        data = load_any(Path(f))\n        n_before, w_before = len(flags), len(neighbor_only_warns)\n",
    "E2 per-file flag offsets")
sub(WQ, '                                  "quote": span[:90], "refs_nearby": near})\n    print(json.dumps({"quotes_checked": checked, "flag_count": len(flags),\n',
    '                                  "quote": span[:90], "refs_nearby": near})\n'
    '        for fl in flags[n_before:] + neighbor_only_warns[w_before:]:   # S1-10: every flag names its row\n'
    '            fl.setdefault("decision_id", decision_id_for(data, fl.get("path", "")))\n'
    '    print(json.dumps({"quotes_checked": checked, "flag_count": len(flags),\n', "E3 flags carry decision_id")

# ---------------------------------------------------------------- F  _cure_verification (S1-19)
sub(VER, '    reasons = []\n    cid = c.get("cure_id") or "(unnamed cure)"\n',
    '    reasons = []\n    cid = c.get("cure_id") or "(unnamed cure)"\n'
    '    if not (c.get("author_attempt_id") or c.get("author_execution_id")):\n'
    '        # S1-19(a): with no author named, the distinct-checker test below has nothing to compare and would pass vacuously\n'
    '        reasons.append("%s: names no author_attempt_id or author_execution_id, so the checker cannot be shown distinct"\n'
    '                       % cid)\n', "F1 (a) author required")
sub(VER, '        has_machine_result = (v.get("exit") is not None) or bool(v.get("output_sha256")) or bool(v.get("counts"))\n',
    '        osha = v.get("output_sha256")\n'
    '        osha_ok = isinstance(osha, str) and re.fullmatch(r"[0-9a-f]{64}", osha) is not None\n'
    '        if osha is not None and not osha_ok:\n'
    '            # S1-19(d): an output digest that is not a digest is no machine result\n'
    '            reasons.append("%s output_sha256 %r is not a 64-hex digest" % (tag, str(osha)[:20]))\n'
    '        has_machine_result = (v.get("exit") is not None) or osha_ok or bool(v.get("counts"))\n', "F2 (d) output digest shape")
sub(VER, 'ORDERED_BY = re.compile(r"\\b(?P<xid>[a-z0-9_]+#e\\d+)\\b.*?\\bruling\\s+(?P<rid>[A-Za-z0-9][A-Za-z0-9-]*)")\n',
    '# S1-19(c): an attempt-shaped id standing alone, never a hyphen-joined substring (\'test-adversarial#e1\' named \'adversarial#e1\')\n'
    'ORDERED_BY = re.compile(r"(?<![\\w-])(?P<xid>[a-z0-9_]+_a\\d+#e\\d+)(?![\\w-]).*?\\bruling\\s+(?P<rid>[A-Za-z0-9][A-Za-z0-9-]*)")\n',
    "F3 (c) ORDERED_BY attempt-shaped")
sub(VER, '''def load_rulings(paths):
    """{execution_id: {ruling_id: verb}} from controlling-rulings files, for the optional --rulings cross-check."""
    out = {}
    for p in paths or []:
        d = json.loads(Path(p).read_text(encoding="utf-8"))
        out.setdefault(d.get("execution_id"), {}).update({r.get("id"): r.get("ruling") for r in d.get("rulings", [])})
    return out
''', '''RULING_TEXT = {}   # S1-19(e): (execution_id, ruling_id) -> the ruling's full text, to see whether it names the retired cure


def load_rulings(paths):
    """{execution_id: {ruling_id: verb}} from controlling-rulings files, for the optional --rulings cross-check."""
    out = {}
    for p in paths or []:
        d = json.loads(Path(p).read_text(encoding="utf-8"))
        out.setdefault(d.get("execution_id"), {}).update({r.get("id"): r.get("ruling") for r in d.get("rulings", [])})
        RULING_TEXT.update({(d.get("execution_id"), r.get("id")): json.dumps(r, ensure_ascii=False) for r in d.get("rulings", [])})
    return out
''', "F4 (e) ruling text kept")
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
    warnings = [] if known is not None else ["supersession records were not cross-checked against any rulings file; a gating "
                                             "run passes --rulings (S1-19(c))"]
''', "F5 (b) duplicate ids and the warnings list")
sub(VER, '''                if verb not in SUPERSEDING_VERBS:
                    why.append("the rulings given do not show %s ruling %s as adopt, amend or close (found %r)"
                               % (m.group("xid"), m.group("rid"), verb))
''', '''                if verb not in SUPERSEDING_VERBS:
                    why.append("the rulings given do not show %s ruling %s as adopt, amend or close (found %r)"
                               % (m.group("xid"), m.group("rid"), verb))
                elif not re.search(r"(?<![\\w-])%s(?![\\w-])" % re.escape(target), RULING_TEXT.get((m.group("xid"), m.group("rid")), "")):
                    warnings.append("%s: ruling %s of %s does not name %s; it orders the retirement rule, not this "
                                    "retirement (S1-19(e))" % (target, m.group("rid"), m.group("xid"), target))
            if target in dup:
                why.append("the record retires %s, which appears on more than one claim line" % target)
''', "F6 (e) warning and (b) supersession of a duplicated id")
sub(VER, '''    for c in claims:
        if c.get("cure_id") in supers:
''', '''    for c in claims:
        if c.get("cure_id") in dup:
            refused += 1
            out.append({"cure_id": c.get("cure_id"), "verdict": "REFUSED",
                        "reasons": ["%s appears on more than one claim line; append-only claims carry one line per cure id, "
                                    "and a retired claim is superseded, never repeated (S1-19(b))" % c.get("cure_id")]})
            continue
        if c.get("cure_id") in supers:
''', "F7 (b) duplicate claim lines refused")
sub(VER, '            "results": out, "verdict": "GREEN" if not refused else "RED"}\n',
    '            "results": out, "warnings": warnings, "verdict": "GREEN" if not refused else "RED"}\n', "F8 warnings reported")
sub(VER, '    ap.add_argument("--selftest", action="store_true")\n',
    '    ap.add_argument("--selftest", action="store_true")\n'
    '    ap.add_argument("--require-rulings", action="store_true", help="S1-19(c): refuse a run given no --rulings")\n', "F9 --require-rulings flag")
sub(VER, '    d = run(a.claims, a.root, a.rulings)\n',
    '    if a.require_rulings and not a.rulings:\n'
    '        print(json.dumps({"status": "REFUSED", "why": "--require-rulings was given without --rulings"}))\n'
    '        return 1\n'
    '    d = run(a.claims, a.root, a.rulings)\n', "F10 --require-rulings enforced")
sub(VER, '                              "output_sha256": "abc"}],\n',
    '                              "output_sha256": "a" * 64}],   # S1-19(d): a real digest shape\n', "F11 selftest good vector carries a real digest shape")
sub(VER, '        ("artifact digest does not match disk", dict(good, artifact_sha256="1" * 64), "REFUSED"),\n',
    '        ("artifact digest does not match disk", dict(good, artifact_sha256="1" * 64), "REFUSED"),\n'
    '        ("S1-19(a) a claim naming no author", {k: v for k, v in good.items() if k != "author_attempt_id"}, "REFUSED"),\n'
    '        ("S1-19(d) an output digest that is not a digest is no machine result",\n'
    '         dict(good, verification=[{"tool": "t.py", "artifact_sha256_at_run": d, "output_sha256": "not-a-digest"}]), "REFUSED"),\n',
    "F12 (a) and (d) vectors")
sub(VER, '            ("T3-01 --rulings confirms the ordering ruling", genuine, [rf], ("SUPERSEDED", 0)),\n',
    '            ("S1-19(c) ordered_by with a hyphen-joined fabricated id is refused",\n'
    '             dict(genuine, ordered_by="test-adversarial#e1 ruling R5"), None, ("REFUSED", 2)),\n'
    '            ("T3-01 --rulings confirms the ordering ruling", genuine, [rf], ("SUPERSEDED", 0)),\n', "F13 (c) vector")
sub(VER, '''    return {"vectors": len(results), "failed": failed, "results": results,
            "verdict": "GREEN" if not failed else "RED"}
''', '''    cf = tmp / "claims_dup.jsonl"
    cf.write_text(json.dumps(dict(good, cure_id="DUP", artifact_sha256="4" * 64)) + "\\n" + json.dumps(dict(good, cure_id="DUP")) + "\\n",
                  encoding="utf-8")
    rep = run(cf, tmp, None)
    dv = [o["verdict"] for o in rep["results"] if o["cure_id"] == "DUP"]
    ok = dv == ["REFUSED", "REFUSED"] and rep["refused"] == 2
    failed += not ok
    results.append({"vector": "S1-19(b) two claim lines with one cure id are both refused", "expected": ["REFUSED", "REFUSED"],
                    "got": dv, "ok": ok})
    cf = tmp / "claims_warn.jsonl"
    cf.write_text(json.dumps(stale) + "\\n" + json.dumps(genuine) + "\\n", encoding="utf-8")
    rep = run(cf, tmp, [rf])
    ok = any("S1-19(e)" in w for w in rep["warnings"]) and rep["superseded"] == 1
    failed += not ok
    results.append({"vector": "S1-19(e) --rulings warns when the ordering ruling does not name the retired cure id",
                    "expected": "a warning", "got": rep["warnings"], "ok": ok})
    rep = run(cf, tmp, None)
    ok = any("S1-19(c)" in w for w in rep["warnings"])
    failed += not ok
    results.append({"vector": "S1-19(c) a run without --rulings says so", "expected": "a warning", "got": rep["warnings"], "ok": ok})
    return {"vectors": len(results), "failed": failed, "results": results,
            "verdict": "GREEN" if not failed else "RED"}
''', "F14 (b), (c), (e) file-level vectors")

# ---------------------------------------------------------------- G  TOOLKIT.md
sub(TK, "calendar-date onsets and dateline claims, Hebrew-quote binding |",
    "calendar-date onsets and dateline claims, Hebrew-quote binding in prose and, for Hebrew inside a ref entry, to that "
    "entry's own ref or a ref it names (S1-06) |", "G1 TOOLKIT citation_sweep row")
sub(TK, "| every Hebrew run byte-true to the verse text or to a Qere; NFD-only matches stay defects |",
    "| every Hebrew run byte-true to the verse text or to a Qere, ending on a grapheme boundary (a splice cut inside a "
    "grapheme is a defect: S1-07; `collate_hebrew` applies the same rule at its byte and nfd tiers); NFD-only matches stay "
    "defects |", "G2 TOOLKIT normalizer row")
sub(TK, "`check_atomic_isolation.py`, `_punct_boundary_sweep.py` — state their contracts in their\nown docstrings.\n",
    "`check_atomic_isolation.py`, `_punct_boundary_sweep.py` — state their contracts in their\nown docstrings.\n\n"
    "`check_register.py` also reads the annotation of every ref entry, and carries arms for repair history, positional row\n"
    "references, strategy citations and governance posture (S1-05). `check_web_quotes.py` names each flag's decision_id\n"
    "(S1-10).\n", "G3 TOOLKIT register and web_quotes paragraph")

# ---------------------------------------------------------------- T  tests, section 10
SECTION10 = r'''# 10. S1 FINDINGS - TOOLFIX-2, proposed to ezek_controlling_rulings_a1#e4 (installed only after its ruling, then a fresh
# distinct review).
#   S1-06: Hebrew inside a ref entry binds to that entry's own ref or a ref it names, at byte tier for a pointed run; a Qere
#          counts only with a ketiv/qere word in the entry.
#   S1-07: a splice cut inside a grapheme is not byte-true, in prose (citation_sweep) and for the normalizer.
#   S1-05: register arms for the author wave's phrasings, in prose and in ref annotations.
#   S1-10: web_quotes flags name their row.
# The helpers are local, so this file still runs against tools that predate the edit.
import unicodedata  # noqa: E402


def _mark10(ch):
    return unicodedata.category(ch) == "Mn"


def _bounded10(needle, hay):
    i = hay.find(needle)
    while i != -1:
        j = i + len(needle)
        if j >= len(hay) or not _mark10(hay[j]):
            return True
        i = hay.find(needle, i + 1)
    return False


JOINED10 = " | ".join(OSHB.values())


def _cut10():
    for key, verse in OSHB.items():
        for w in verse.split(" "):
            if w and _mark10(w[-1]):
                k = len(w)
                while k and _mark10(w[k - 1]):
                    k -= 1
                cut = w[:k]
                if len([ch for ch in cut if "\u05d0" <= ch <= "\u05ea"]) >= 3 and not _bounded10(cut, JOINED10):
                    return key, cut, w
    return None, None, None


CUT_KEY, CUT, CUT_WORD = _cut10()
Q72 = kq_split_bytes(PM["kq"]["Ezek.7.2"][0], OSHB["Ezek.7.2"])[1].replace("/", "")
W11 = OSHB["Ezek.1.1"].split(" ")
OTHER12 = next(w for w in OSHB["Ezek.1.2"].split(" ")
               if len([ch for ch in w if "\u05d0" <= ch <= "\u05ea"]) >= 3 and w not in OSHB["Ezek.1.1"])
check("fixture: a word whose final-mark cut occurs nowhere bounded in the book exists (%s)" % CUT_KEY,
      bool(CUT) and CUT != CUT_WORD, CUT_KEY)
check("fixture: the MT 7:2 Qere is pointed and absent from the verse bytes", bool(Q72) and Q72 not in OSHB["Ezek.7.2"], Q72)
S1_REFS = [
    ("cs_s1_06_accent_stripped_qere_in_ref",
     ["oshb:Ezek.7.2 (K/Q, checked before quoting: ketiv ארבעת / qere אַרְבַּע, 'the four corners')"],
     "does not collate against its own ref"),
    ("cs_s1_06_raw_qere_in_ref_ok", ["oshb:Ezek.7.2 (K/Q: qere %s)" % Q72], None),
    ("cs_s1_06_undisclosed_qere_in_ref", ["oshb:Ezek.7.2 (%s)" % Q72], "does not collate against its own ref"),
    ("cs_s1_06_own_verse_words_ok", ["oshb:Ezek.1.1 (%s %s)" % (W11[1], W11[2])], None),
    ("cs_s1_06_other_verse_words", ["oshb:Ezek.1.1 (%s)" % OTHER12], "does not collate against its own ref"),
    ("cs_s1_06_other_verse_named_ok", ["oshb:Ezek.1.1 (cf. oshb:Ezek.1.2 %s)" % OTHER12], None),
]
S1_PROSE = [
    ("cs_s1_07_cut_splice_in_prose", "the splice %s (oshb:%s) closes the unit" % (CUT, CUT_KEY),
     "does not collate against any nearby cited ref"),
    ("cs_s1_07_whole_word_in_prose_ok", "the splice %s (oshb:%s) closes the unit" % (CUT_WORD, CUT_KEY), None),
]
REG10 = [
    ("reg_s1_05_originally_drafted", {"strongest_rejected_alternative": "the span as originally drafted ran to 7:27"}, "row_history_narration"),
    ("reg_s1_05_former_span", {"device_notes": "the former single 48.1-29 span held one refrain"}, "row_history_narration"),
    ("reg_s1_05_preceding_row", {"boundary_rationale": "the preceding row's close stands at 30:12"}, "positional_row_reference"),
    ("reg_s1_05_row_before_after", {"boundary_rationale": "the row before and the row after this one close on the refrain"},
     "positional_row_reference"),
    ("reg_s1_05_last_of_three", {"device_notes": "the last of three land-allotment rows"}, "positional_row_reference"),
    ("reg_s1_05_strategy_s", {"device_notes": "matches the strategy's own naming"}, "strategy_citation"),
    ("reg_s1_05_posture", {"device_notes": "held at medium_low per the flagged-region posture"}, "governance_posture"),
    ("reg_s1_05_officially_inventoried_in_ref", {"boundary_evidence_refs": ["oshb:Ezek.40.24 (officially inventoried transport)"]},
     "governance_posture"),
    ("reg_s1_05_this_row_exempt_ok", {"boundary_rationale": "this row closes on the refrain (sweep: 6 verses)"}, None),
    ("reg_s1_05_quoted_web_masked_ok", {"boundary_rationale": "“the next row of chambers” (web:Ezek.42.3)"}, None),
]
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "s1_cs.jsonl"
    p.write_text("\n".join([json.dumps({"decision_id": d, "boundary_evidence_refs": refs}, ensure_ascii=False) for d, refs, _ in S1_REFS]
                           + [json.dumps({"decision_id": d, "boundary_rationale": prose}, ensure_ascii=False) for d, prose, _ in S1_PROSE]),
                 encoding="utf-8")
    rep = run("citation_sweep.py", p)
    for did, _, expect in S1_REFS + S1_PROSE:
        mine = [x for x in rep["problems"] if x.startswith(did + ":")]
        check("citation_sweep %s: %s" % (did, "no problem" if expect is None else repr(expect)),
              (not mine) if expect is None else any(expect in x for x in mine), mine)
    for label, payload, want in (("normalize S1-07: a splice cut inside a grapheme is a defect", {"c": "x %s y" % CUT}, 1),
                                 ("normalize S1-07: the whole word stays byte-true", {"w": "x %s y" % CUT_WORD}, 0)):
        fp = Path(td) / ("s1_norm_%d.json" % want)
        fp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.run([sys.executable, str(HERE / "normalize_hebrew_in_json.py"), str(fp)],
                              capture_output=True, text=True, encoding="utf-8", env=ENV)
        nrep = json.loads(proc.stdout.strip().splitlines()[-1])
        check(label, nrep["defect_count"] == want, nrep)
    p = Path(td) / "s1_reg.jsonl"
    p.write_text("\n".join(json.dumps(dict({"decision_id": d}, **fields), ensure_ascii=False) for d, fields, _ in REG10), encoding="utf-8")
    rep = run("check_register.py", p)
    for d, _, cls in REG10:
        mine = [fl for fl in rep["flags"] if fl.get("decision_id") == d]
        check("check_register %s: %s" % (d, cls or "no flag"), (not mine) if cls is None else any(fl.get("class") == cls for fl in mine), mine)
    p = Path(td) / "s1_wq.jsonl"
    p.write_text(json.dumps({"decision_id": "wq_s1_10_unclosed",
                             "boundary_rationale": "“Son of man, set your face toward Sidon (web:Ezek.28.21)."}, ensure_ascii=False),
                 encoding="utf-8")
    rep = run("check_web_quotes.py", p)
    mine = [fl for fl in rep["flags"] if "e15a" in str(fl.get("issue"))]
    check("check_web_quotes wq_s1_10_unclosed: the pairing flag names its decision_id",
          any(fl.get("decision_id") == "wq_s1_10_unclosed" for fl in mine), rep["flags"])

'''
sub(TEST, 'failed = [r for r in results if not r["ok"]]\n', SECTION10 + 'failed = [r for r in results if not r["ok"]]\n', "T section 10 vectors")

# ---------------------------------------------------------------- regenerate, test, compare
pins = ["citation_sweep.py=" + sha(T / "citation_sweep.py"), "check_marks.py=" + sha(T / "check_marks.py")]
g = run([ADAPT, "--replace"] + pins)
out = {"applied": applied, "regen_exit": g.returncode, "regen": g.stdout.strip().splitlines()[-4:], "regen_err": g.stderr[-800:]}
if g.returncode != 0:
    print(json.dumps(out, ensure_ascii=False, indent=1))
    raise SystemExit(1)
t = run([TEST])
try:
    td_ = json.loads(t.stdout)
    out["tests"] = {"checks": td_["checks"], "passed": td_["passed"], "verdict": td_["verdict"],
                    "failed": [{"check": f.get("check"), "detail": str(f.get("detail"))[:400]} for f in td_["failed"]]}
except json.JSONDecodeError:
    out["tests"] = {"exit": t.returncode, "stdout_tail": t.stdout[-1500:], "stderr_tail": t.stderr[-1500:]}
lib = run([LIB])
try:
    ld = json.loads(lib.stdout)
    out["ezek_lib_selftest"] = {"checks": ld["checks"], "passed": ld["passed"], "failed": ld["failed"], "verdict": ld["verdict"]}
except json.JSONDecodeError:
    out["ezek_lib_selftest"] = {"exit": lib.returncode, "stdout_tail": lib.stdout[-800:], "stderr_tail": lib.stderr[-800:]}
sc = run([T / "_toolkit_selfcheck.py"])
try:
    scd = json.loads(sc.stdout)
    out["toolkit_selfcheck"] = {"exit": sc.returncode, "checks": scd.get("checks"), "passed": scd.get("passed"), "verdict": scd.get("verdict")}
except json.JSONDecodeError:
    out["toolkit_selfcheck"] = {"exit": sc.returncode, "stdout_tail": sc.stdout[-600:]}
vs = run([VER, "--selftest"], cwd=ST / "campaign")
try:
    vsd = json.loads(vs.stdout)
    out["verifier_selftest"] = {"vectors": vsd["vectors"], "failed": vsd["failed"], "verdict": vsd["verdict"],
                                "failed_vectors": [r for r in vsd["results"] if not r["ok"]]}
except json.JSONDecodeError:
    out["verifier_selftest"] = {"exit": vs.returncode, "stdout_tail": vs.stdout[-800:], "stderr_tail": vs.stderr[-800:]}
rulings = [SP / "Ezek" / "ezek_controlling_agent_rulings.v1.json", SP / "Ezek" / "ezek_controlling_agent_rulings_e3.v1.json"]
out["verifier_real_claims"] = {}
for cf in ("ezek_cure_claims.v1.jsonl", "ezek_cure_claims_toolkit_repair.v1.jsonl"):
    vr = run([VER, "--claims", SP / "Ezek" / cf, "--root", SP / "Ezek", "--rulings"] + rulings, cwd=ST / "campaign")
    vrd = json.loads(vr.stdout)
    out["verifier_real_claims"][cf] = {k: vrd.get(k) for k in ("claims", "accepted", "refused", "superseded", "warnings", "verdict")}
s = run([T / "run_validator_suite.py", SUITE / "rows.jsonl"])
new = json.loads((SUITE / "rows.jsonl.validator_report.json").read_text(encoding="utf-8"))
old = json.loads((SP / "Ezek" / "repair" / "suite_v3_2acbc045" / "rows.jsonl.validator_report.json").read_text(encoding="utf-8"))
diff = {}
for k in sorted(set(old) | set(new)):
    a, b = old.get(k), new.get(k)
    if not (isinstance(a, dict) and isinstance(b, dict)):
        continue
    for kk in sorted(set(a) | set(b)):
        la, lb = a.get(kk), b.get(kk)
        if not (isinstance(la, list) and isinstance(lb, list)):
            continue
        drop = not any(isinstance(x, dict) and "decision_id" in x for x in la) and any(isinstance(x, dict) and "decision_id" in x for x in lb)
        norm = (lambda x: {q: w for q, w in x.items() if q != "decision_id"} if isinstance(x, dict) else x) if drop else (lambda x: x)
        sa = {json.dumps(x, sort_keys=True, ensure_ascii=False) for x in la}
        sb = {json.dumps(norm(x), sort_keys=True, ensure_ascii=False) for x in lb}
        if sa != sb or drop:
            entry = {"installed": len(la), "staged": len(lb), "added": len(sb - sa), "removed": len(sa - sb),
                     "added_sample": sorted(sb - sa)[:12], "removed_sample": sorted(sa - sb)[:6]}
            if drop:
                entry["decision_id_added_to_every_item"] = True
            if "register" in k:
                added = [json.loads(x) for x in sb - sa]
                by_cls, by_row = {}, {}
                for fl in added:
                    by_cls[fl.get("class")] = by_cls.get(fl.get("class"), 0) + 1
                    by_row[fl.get("decision_id")] = by_row.get(fl.get("decision_id"), 0) + 1
                entry["added_by_class"], entry["added_rows"] = by_cls, len(by_row)
            diff["%s.%s" % (k, kk)] = entry
out["suite_exit"] = s.returncode
out["suite_summary"] = {"installed": old.get("summary"), "staged": new.get("summary")}
out["suite_list_differences"] = diff or "NONE"
out["staged_digests"] = {n: sha(T / n) for n in ("citation_sweep.py", "check_marks.py", "_adapt_zone_tools_ezek.py", "_test_zone_tools_ezek.py",
                                                   "TOOLKIT.md", "ezek_lib.py", "normalize_hebrew_in_json.py", "check_register.py", "check_web_quotes.py")}
out["staged_digests"]["campaign/_cure_verification.py"] = sha(VER)
(ROOT / "stage_run.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps(out, ensure_ascii=False, indent=1))
