"""Stage TOOLFIX-2 as toolfix2_batch3 per ezek_controlling_rulings_a1#e5 ruling INSTALL-TF2-1 (1)-(3), over the INSTALLED tools
(receipt ezek_tools_install_t4fix_batch2.json). Session scratch only; nothing is installed.

CONTENT per INSTALL-TF2-1 (1):
  - batch1's content UNCHANGED (S1-07, S1-06, S1-10, S1-19, S1-05, S1-22, TOOLKIT.md, the selftest fixture). batch1's staged
    files are copied byte for byte from SP/Ezek/proposals/toolfix2_batch1/staged, each verified against batch1's manifest,
    and only then amended.
  - NEWCLASS-TF2-1: three citation_sweep vectors whose Hebrew is derived from the verse bytes at run time; no rule change.
  - FLAGS-TF2-1: W1, W2 as amended, W5 and W6 in check_marks (through the adapter), with its vectors, the check_marks
    docstring and TOOLKIT.md's check_marks row.
  - REG-TF2-1: check_register's four arms as amended, with its RED vectors and GREEN controls.
  The new vectors form section 10c; section 10b is not touched.

THE RUN (INSTALL-TF2-1 (2)-(3)):
  - regenerate the zone tools (pins: batch1's staged citation_sweep and check_marks digests);
  - tests, the ezek_lib selftest, the toolkit selfcheck, the verifier selftest, and the verifier over both real claims files
    with --rulings (#e2, #e3, #e4, #e5) and --require-rulings;
  - the batch3 test file run against the INSTALLED tools and against batch1's STAGED tools (discrimination);
  - condition (c) over the chain head 6ff71fa6, with the batch3 tools and with batch1's staged tools:
    - the HARD lists compared for equality with the set NEWCLASS-TF2-1 enumerates;
    - check_marks deltas against batch1 compared with FLAGS-TF2-1's expected set;
    - register deltas listed per row;
    - web_quotes e15d counted."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
EZ = SP / "Ezek"
SCR = Path(__file__).resolve().parent
ROOT = SCR / "stage_tf2c"
B1 = EZ / "proposals" / "toolfix2_batch1"
CHAIN_HEAD = EZ / "repair" / "rows_v3_cwo12.jsonl"
CHAIN_HEAD_SHA = "6ff71fa693763167819d9f7544e65914de7824465a21e1cf1df0ce7244a03d1e"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
TOOL_FILES = ("citation_sweep.py", "check_marks.py", "_adapt_zone_tools_ezek.py", "_test_zone_tools_ezek.py", "TOOLKIT.md",
              "ezek_lib.py", "normalize_hebrew_in_json.py", "check_register.py", "check_web_quotes.py")
RULINGS = [EZ / "ezek_controlling_agent_rulings.v1.json", EZ / "ezek_controlling_agent_rulings_e3.v1.json",
           EZ / "ezek_controlling_agent_rulings_e4.v1.json", EZ / "ezek_controlling_agent_rulings_e5.v1.json"]
applied = []


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(args, cwd):
    return subprocess.run([sys.executable] + [str(a) for a in args], capture_output=True, text=True, encoding="utf-8", env=ENV, cwd=str(cwd))


def sub(path, old, new, label, count=1):
    t = path.read_text(encoding="utf-8")
    n = t.count(old)
    if n != count:
        raise SystemExit("ABORT: %s: expected %d occurrence(s) in %s, found %d" % (label, count, path.name, n))
    path.write_text(t.replace(old, new), encoding="utf-8", newline="\n")
    applied.append(label)


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


# ------------------------------------------------------------------ preconditions
if sha(CHAIN_HEAD) != CHAIN_HEAD_SHA:
    raise SystemExit("ABORT: the chain head is not 6ff71fa6")
rec = json.loads((SP / "campaign" / "receipts" / "ezek_tools_install_t4fix_batch2.json").read_text(encoding="utf-8"))
for n, f in rec["files"].items():
    if sha(EZ / "tools" / n) != f["after"]:
        raise SystemExit("ABORT: SP tools/%s is not the t4fix_batch2 installed digest" % n)
b1 = json.loads((B1 / "manifest.json").read_text(encoding="utf-8"))
for name, f in b1["files"].items():
    inst = (SP / name) if name.startswith("campaign/") else (EZ / "tools" / name)
    if sha(inst) != f["installed_sha256"]:
        raise SystemExit("ABORT: installed %s is not the digest batch1 builds on" % name)
    if sha(B1 / "staged" / name) != f["staged_sha256"]:
        raise SystemExit("ABORT: batch1's staged %s does not carry its manifest digest" % name)
for p in RULINGS:
    if not p.is_file():
        raise SystemExit("ABORT: rulings file %s is absent" % p.name)


def build_tree(root, overlay_batch1):
    assert root.parent == SCR and root.name.startswith("stage_tf2c")
    if root.exists():
        shutil.rmtree(root)
    st = root / "sp_durable"
    ign = shutil.ignore_patterns("__pycache__", "*.pyc")
    shutil.copytree(EZ / "tools", st / "Ezek" / "tools", ignore=ign)
    shutil.copytree(SP / "Jer" / "tools", st / "Jer" / "tools", ignore=ign)
    for f in EZ.iterdir():
        if f.is_file():
            shutil.copy2(f, st / "Ezek" / f.name)
    (st / "campaign").mkdir(parents=True)
    shutil.copy2(SP / "campaign" / "_cure_verification.py", st / "campaign" / "_cure_verification.py")
    if overlay_batch1:
        for name in b1["files"]:
            shutil.copyfile(B1 / "staged" / name, (st / name) if name.startswith("campaign/") else (st / "Ezek" / "tools" / name))
    return st


ST = build_tree(ROOT, True)
T = ST / "Ezek" / "tools"
ADAPT, TEST, REG, TK = T / "_adapt_zone_tools_ezek.py", T / "_test_zone_tools_ezek.py", T / "check_register.py", T / "TOOLKIT.md"
VER, LIB = ST / "campaign" / "_cure_verification.py", T / "ezek_lib.py"
for name, f in b1["files"].items():
    if sha((ST / name) if name.startswith("campaign/") else (T / name)) != f["staged_sha256"]:
        raise SystemExit("ABORT: the stage tree does not start from batch1's staged %s" % name)

# ------------------------------------------------------------------ FLAGS-TF2-1: check_marks helpers (adapter)
CM_W_BLOCK = r"""CM_W_RE = r'''# W1, W2, W5 and W6 (ezek_controlling_rulings_a1#e5 ruling FLAGS-TF2-1), check_marks only; the PUNCTA arm is untouched.
KQ_EXCLUSIVE = re.compile(r"other|further|additional|second|more", re.I)   # W2: an exclusivity word keeps the negation
# W6: the letter-name absence form, admitted only in mark talk (a MARKISH_CTX word within 60 characters, PARAMARK_LETTER's gate)
ABSENCE_LETTER = re.compile(r"\b(?:no|without)\s+(?:(?:a|any)\s+)?(?:pe|samekh)\b(?:\s+(?:or|and|nor)\s+(?:pe|samekh)\b)?", re.I)
EDGE_PUNCT = "()[]{},;:!?\u201c\u201d\u2018\u2019" + chr(34) + chr(39)


def before_readings(c, v):
    # W1: both MT readings of a cited verse and the verse before each. Before a chapter's first verse stands the previous
    # chapter's last MT verse, as relevant() computes the front seam.
    out = []
    for rc, rv in readings(c, v):
        for p in ((rc, rv), (rc, rv - 1) if rv > 1 else (rc - 1, MT_LAST_VERSE.get(rc - 1, 0))):
            if p not in out and p[0] in MT_LAST_VERSE and 1 <= p[1] <= MT_LAST_VERSE[p[0]]:
                out.append(p)
    return out


def letter_absences(text, lo=0, hi=None):
    # W6: every letter-name absence phrase in text[lo:hi] that stands in mark talk
    return [m for m in ABSENCE_LETTER.finditer(text, lo, len(text) if hi is None else hi)
            if MARKISH_CTX.search(text[max(0, m.start() - 60):m.start() + 60])]


def kq_negation(text, start):
    # W2 and W5, rule 4 only. Returns None, "plain" or "exclusive".
    # W2: inside the token's comma-delimited clause, a negator (NEG_WORD) with at most one word between it and the token negates
    # it. Two negators standing together cancel (T1-03). An exclusivity word as that one word returns "exclusive".
    # W5: a negator distributes across a comma list when its own comma-delimited segment is the negator plus at most two words,
    # every intervening segment is at most two words and names no verse, and the token's segment begins with the token
    # (optionally after and/or/nor).
    lo, _ = clause_bounds(text, start, start, NEG_CLAUSE_END)
    words = [w for w in (x.strip(EDGE_PUNCT) for x in text[lo:start].split()) if w]
    for gap in (0, 1):
        k = len(words) - 1 - gap
        if k >= 0 and NEG_WORD.fullmatch(words[k]):
            if k >= 1 and NEG_WORD.fullmatch(words[k - 1]):
                return None
            return "exclusive" if gap == 1 and KQ_EXCLUSIVE.fullmatch(words[-1]) else "plain"
    if [w.lower() for w in words] not in ([], ["and"], ["or"], ["nor"]):
        return None
    f_lo = field_bounds(text, start, start)[0]
    cut = lo
    while cut - 1 >= f_lo and text[cut - 1] == ",":
        seg_lo, _ = clause_bounds(text, cut - 1, cut - 1, NEG_CLAUSE_END)
        seg = text[seg_lo:cut - 1]
        seg_words = [w for w in (x.strip(EDGE_PUNCT) for x in seg.split()) if w]
        if seg_words and NEG_WORD.fullmatch(seg_words[0]) and len(seg_words) <= 3:
            return "plain"
        if len(seg_words) > 2 or RANGE_NUM.search(seg):
            return None
        cut = seg_lo
    return None


def row_named_mt_keys(text):
    # W2's exclusivity scope: the MT keys, under both readings, of every verse number written anywhere in the row. That means
    # C:V, C.V, MT C:V or dotted, in any field, the refs included; a written range names its two ends.
    keys = set()
    for m in RANGE_NUM.finditer(text):
        ends = [(int(m.group(1)), int(m.group(2)))]
        if m.group(4):
            ends.append((int(m.group(3)) if m.group(3) else int(m.group(1)), int(m.group(4))))
        for c0, v0 in ends:
            keys |= {f"Jer.{rc}.{rv}" for rc, rv in readings(c0, v0)}
    return keys
'''


"""
sub(ADAPT, 'CM_RULE1_OLD = """', CM_W_BLOCK + 'CM_RULE1_OLD = """', "FLAGS-TF2-1 W helpers defined in the adapter")
sub(ADAPT, '+ CHAPTER_NAMED_RE,\n                  1, "cm puncta constants")', '+ CHAPTER_NAMED_RE + CM_W_RE,\n                  1, "cm puncta constants")',
    "FLAGS-TF2-1 W helpers wired into check_marks")

# ------------------------------------------------------------------ FLAGS-TF2-1: rules 1, 3 and 4 (adapter rule texts)
sub(ADAPT, r'''                if any(want_type in marks.get(f"Jer.{rc}.{rv}", [])
                       for c0, v0 in named_
                       for rc, rv in readings(c0, v0)):
                    continue
                if ABSENCE.search(text[c_lo_:c_hi_]):
                    continue
''', r'''                # W1 (ezek_controlling_rulings_a1#e5 ruling FLAGS-TF2-1): a mark of the claimed TYPE after N or after N-1 satisfies
                # the claim; the type test is untouched, and an absence claim never takes the N-1 acceptance (rule 3 reads N)
                if any(want_type in marks.get(f"Jer.{rc}.{rv}", [])
                       for c0, v0 in named_
                       for rc, rv in before_readings(c0, v0)):
                    continue
                # W6 (#e5 FLAGS-TF2-1): the letter-name absence form is an absence phrase, so rule 1 skips its clause
                if ABSENCE.search(text[c_lo_:c_hi_]) or letter_absences(text, c_lo_, c_hi_):
                    continue
''', "FLAGS-TF2-1 W1 and W6 in rule 1")
sub(ADAPT, '            for am in ABSENCE.finditer(text):\n                named_ = [p for pairs in puncta_claim_numbers(text, am.start(), am.end()) for p in pairs]\n',
    '            for am in sorted(list(ABSENCE.finditer(text)) + letter_absences(text), key=lambda x: x.start()):   # W6 (#e5 FLAGS-TF2-1)\n'
    '                named_ = [p for pairs in puncta_claim_numbers(text, am.start(), am.end()) for p in pairs]\n', "FLAGS-TF2-1 W6 in rule 3")
sub(ADAPT, r'''                if puncta_negated(text, m.start(), m.end()):
                    if named_:
                        keys_ = {f"Jer.{rc}.{rv}" for c0, v0 in named_ for rc, rv in readings(c0, v0)}
                    else:
                        keys_ = {f"Jer.{mt_[0]}.{mt_[1]}" for c0, v0 in span_pairs(row) for mt_ in [web_to_mt(c0, v0)] if mt_}
                    present_ = sorted(k_ for k_ in keys_ if kq.get(k_))
                    if present_:
                        flags.append({"decision_id": did, "rule": "false_kq_absence_claim", "scope": "named" if named_ else "span",
                                      "kq_mt_keys": present_, "claim_context": text[max(0, m.start() - 60):m.start() + 80]})
                    continue
''', r'''                # W2 and W5 (ezek_controlling_rulings_a1#e5 ruling FLAGS-TF2-1): kq_negation reads the negation (a negator at most
                # one word before the token, or heading a short comma list); T4-03's closed-set denial after the token still
                # denies. An exclusivity word ('no other K/Q') narrows the scope to the span's kq keys the row names nowhere.
                neg_ = kq_negation(text, m.start()) or ("plain" if denied_after(text, m.end()) else None)
                if neg_:
                    if neg_ == "exclusive":
                        scope_ = "span_unnamed"
                        keys_ = {f"Jer.{mt_[0]}.{mt_[1]}" for c0, v0 in span_pairs(row) for mt_ in [web_to_mt(c0, v0)] if mt_} - row_named_mt_keys(text)
                    elif named_:
                        scope_ = "named"
                        keys_ = {f"Jer.{rc}.{rv}" for c0, v0 in named_ for rc, rv in readings(c0, v0)}
                    else:
                        scope_ = "span"
                        keys_ = {f"Jer.{mt_[0]}.{mt_[1]}" for c0, v0 in span_pairs(row) for mt_ in [web_to_mt(c0, v0)] if mt_}
                    present_ = sorted(k_ for k_ in keys_ if kq.get(k_))
                    if present_:
                        flags.append({"decision_id": did, "rule": "false_kq_absence_claim", "scope": scope_,
                                      "kq_mt_keys": present_, "claim_context": text[max(0, m.start() - 60):m.start() + 80]})
                    continue
''', "FLAGS-TF2-1 W2 and W5 in rule 4")

# ------------------------------------------------------------------ FLAGS-TF2-1: check_marks docstring (adapter CM_DOC)
sub(ADAPT, "    reports whether MT V±1 carries a mark - the off-by-one signature.\n",
    "    reports whether MT V±1 carries a mark - the off-by-one signature.\n"
    "    W1 (#e5 FLAGS-TF2-1): a mark of the claimed type after the verse BEFORE\n"
    "    the named one also satisfies the claim (a mark closes the unit before an\n"
    "    onset); the type test is untouched and absence claims never take it.\n", "FLAGS-TF2-1 docstring rule 1")
sub(ADAPT, "    WITHIN the span-relevant (MT-mapped) set.\n",
    "    WITHIN the span-relevant (MT-mapped) set. W6 (#e5): the letter-name form\n"
    "    'no pe or samekh' is an absence phrase too, in mark talk only.\n", "FLAGS-TF2-1 docstring rule 3")
sub(ADAPT, "    checked against the verses its clause names or the span's kq keys\n    (false_kq_absence_claim).\n",
    "    checked against the verses its clause names or the span's kq keys\n    (false_kq_absence_claim).\n"
    "    W2/W5 (#e5): a K/Q is negated only by a negator at most one word before it\n"
    "    (two negators together cancel) or heading a comma list of short segments\n"
    "    ('No parashah, K/Q or editorial note ...'); T4-03's closed-set denial\n"
    "    after it still denies. 'no other K/Q' is checked against the span's K/Q\n"
    "    verses that the row names nowhere.\n", "FLAGS-TF2-1 docstring rule 4")

# ------------------------------------------------------------------ REG-TF2-1: check_register
sub(REG, r'''        r"\boriginally drafted\b|\bformer (?:span|row)\b|\bprior \w+(?: \w+)? reading\b|\bcorrection to an earlier\b|"
        r"\b(?:preceding|next|following) row\b|\brow (?:before|after)\b|\b(?:one|middle|last) of \w+ rows\b|"
''', r'''        # REG-TF2-1 (ezek_controlling_rulings_a1#e5): the 'former ... span', 'prior ... reading' and rows arms widened to S1's
        # own phrasings, 'rows of' refused, and 'previously held|drafted|spanned|read as' added
        r"\boriginally drafted\b|\bformer (?:[\w.\-–]+ ){0,2}(?:span|row)\b|\bprior [\w:.\-–]+(?: [\w:.\-–]+)? reading\b|"
        r"\bcorrection to an earlier\b|\bpreviously (?:held|drafted|spanned|read) as\b|"
        r"\b(?:preceding|next|following) row\b|\brow (?:before|after)\b|\b(?:one|middle|last) of \w+(?: [\w-]+)? rows\b(?!\s+of\b)|"
''', "REG-TF2-1 four arms as amended")

# ------------------------------------------------------------------ TOOLKIT.md
sub(TK, "a negated K/Q is an absence claim (S1-22); mark-disclosure symmetry (FLAGS) |",
    "a negated K/Q is an absence claim (S1-22); a mark claim is also met by a mark of its type after the verse before (W1); a K/Q is "
    "negated only by a negator at most one word before it or heading a short comma list, and `no other K/Q` is checked against the "
    "span's K/Q verses the row names nowhere (W2, W5); `no pe or samekh` is an absence phrase (W6); mark-disclosure symmetry (FLAGS) |",
    "TOOLKIT check_marks row (FLAGS-TF2-1)")
sub(TK, "`check_register.py` carries the S1-05 arms (repair history",
    "`check_register.py` carries the S1-05 arms, widened by REG-TF2-1 (repair history", "TOOLKIT register sentence (REG-TF2-1)")

# ------------------------------------------------------------------ tests, section 10c
SECTION10C = r'''# 10c. TOOLFIX-2 re-stage per ezek_controlling_rulings_a1#e5 (NEWCLASS-TF2-1, FLAGS-TF2-1, REG-TF2-1). Every Hebrew form
# is derived from the verse bytes at run time and never typed.


def _let10c(s):
    return "".join(ch for ch in s if _lt10(ch))


W1220C = [w for w in OSHB["Ezek.12.20"].split(" ")
          if len(_let10c(w)) >= 5 and any(_let10c(w)[1:] == _let10c(x) for x in OSHB["Ezek.17.12"].split(" "))]
check("fixture 10c: exactly one MT 12:20 word is a whole MT 17:12 word plus one leading letter", len(W1220C) == 1, W1220C)
WHOLE10C = _let10c(W1220C[0]) if W1220C else ""
BARE10C = WHOLE10C[1:]
S10C_CS_PROSE = [
    ("cs_e5_nc_proclitic_stripped_label_refused", "the %s recognition family (oshb:Ezek.12.20)" % BARE10C,
     "does not collate against any nearby cited ref"),
    ("cs_e5_nc_whole_word_label_ok", "the %s recognition family (oshb:Ezek.12.20)" % WHOLE10C, None),
    ("cs_e5_nc_bare_form_at_bare_verse_ok", "the %s form (oshb:Ezek.17.12)" % BARE10C, None),
]
S10C_REG = [
    ("reg_e5_prior_range_reading", {"device_notes": "keeping the prior 28:24-26 reading"}, "author_wave_register_s1_05"),
    ("reg_e5_former_hyphenated_span", {"device_notes": "its former nineteen-verse span"}, "author_wave_register_s1_05"),
    ("reg_e5_former_two_words_span", {"device_notes": "the former single 48.1-29 span"}, "author_wave_register_s1_05"),
    ("reg_e5_last_of_underscored_rows", {"device_notes": "the last of three land_allotment rows"}, "author_wave_register_s1_05"),
    ("reg_e5_previously_held_as", {"device_notes": "ground previously held as one 29-verse row"}, "author_wave_register_s1_05"),
    ("reg_e5_green_former_kings_ok", {"device_notes": "the former kings"}, None),
    ("reg_e5_green_last_of_the_gates_ok", {"device_notes": "the last of the gates"}, None),
    ("reg_e5_green_rows_of_chambers_ok", {"device_notes": "one of three rows of chambers"}, None),
    ("reg_e5_green_previously_held_by_ok", {"device_notes": "the land previously held by Judah"}, None),
    ("reg_e5_green_prior_verse_ok", {"device_notes": "the prior verse"}, None),
]
S10C_CM = [
    ("cm_e5_w1_mark_before_onset_ok", {"boundary_rationale": "a petuchah closes the row immediately before the fresh word-event at oshb:Ezek.12.21",
                                       "span": "Ezek.12.17-Ezek.12.20"}, [("paragraph_mark_claim", False)]),
    ("cm_e5_w1_no_mark_at_n_or_n_minus_1_flags", {"boundary_rationale": "a petuchah follows oshb:Ezek.8.13"}, [("paragraph_mark_claim", True)]),
    ("cm_e5_w1_type_never_conflated_flags", {"boundary_rationale": "a setumah closes the row immediately before oshb:Ezek.12.21"},
     [("paragraph_mark_claim", True)]),
    ("cm_e5_w1_chapter_crossing_ok", {"boundary_rationale": "a petuchah closes the preceding row immediately before the fresh word-event at oshb:Ezek.35.1"},
     [("paragraph_mark_claim", False)]),
    ("cm_e5_w2_adjacent_negator_flags", {"device_notes": "No K/Q note touches this span", "span": "Ezek.16.44-Ezek.16.50"},
     [("false_kq_absence_claim", ("keys", ["Ezek.16.47"]))]),
    ("cm_e5_w2_distant_negator_silent", {"boundary_rationale": "a boundary is never argued from any of these Qere readings", "span": "Ezek.37.15-Ezek.37.28"},
     [("false_kq_absence_claim", False), ("kq_claim", False)]),
    ("cm_e5_w2_two_words_between_silent", {"boundary_rationale": "not the whole-verse ketiv/qere concatenation", "span": "Ezek.7.10-Ezek.7.27"},
     [("false_kq_absence_claim", False), ("kq_claim", False)]),
    ("cm_e5_w2_no_other_undisclosed_flags", {"device_notes": "no other K/Q note touches this row", "span": "Ezek.41.12-Ezek.41.26"},
     [("false_kq_absence_claim", ("keys", ["Ezek.41.15"]))]),
    ("cm_e5_w2_no_other_disclosed_silent", {"boundary_rationale": "the K/Q at 41:15 is a form variant", "device_notes": "no other K/Q note touches this row",
                                            "span": "Ezek.41.12-Ezek.41.26"}, [("false_kq_absence_claim", False), ("kq_claim", False)]),
    ("cm_e5_w5_negator_heads_list_ok", {"boundary_rationale": "No parashah, K/Q or editorial note touches 40:17-40:19", "span": "Ezek.40.17-Ezek.40.19"},
     [("kq_claim", False), ("false_kq_absence_claim", False)]),
    ("cm_e5_w5_negator_heads_list_flags", {"boundary_rationale": "No parashah, K/Q or editorial note touches 16:44-16:50", "span": "Ezek.16.44-Ezek.16.50"},
     [("false_kq_absence_claim", True)]),
    ("cm_e5_w5_clause_not_a_list_flags", {"boundary_rationale": "No parashah stands here, K/Q at 1:%d is disclosed" % UNMARKED1}, [("kq_claim", True)]),
    ("cm_e5_w6_no_pe_or_samekh_true_silent", {"boundary_rationale": "the close has no Masoretic mark at all (no pe or samekh follows 8:13)",
                                              "span": "Ezek.8.7-Ezek.8.13"},
     [("paragraph_mark_claim", False), ("false_mark_absence_claim", ("no_scope", "named"))]),
    ("cm_e5_w6_no_samekh_false_flags", {"boundary_rationale": "no samekh mark follows 1:28"}, [("false_mark_absence_claim", ("scope", "named"))]),
]


def _cm10c_ok(mine, want):
    if want is True:
        return bool(mine)
    if want is False:
        return not mine
    kind, val = want
    if kind == "keys":
        return any(fl.get("kq_mt_keys") == val for fl in mine)
    if kind == "scope":
        return any(fl.get("scope") == val for fl in mine)
    return not any(fl.get("scope") == val for fl in mine)


with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "tf2c_cs.jsonl"
    p.write_text("\n".join(json.dumps({"decision_id": d, "boundary_rationale": prose}, ensure_ascii=False) for d, prose, _ in S10C_CS_PROSE),
                 encoding="utf-8")
    rep = run("citation_sweep.py", p)
    for did, _, expect in S10C_CS_PROSE:
        mine = [x for x in rep["problems"] if x.startswith(did + ":")]
        check("citation_sweep %s: %s" % (did, "no problem" if expect is None else repr(expect)),
              (not mine) if expect is None else any(expect in x for x in mine), mine)
    p = Path(td) / "tf2c_reg.jsonl"
    p.write_text("\n".join(json.dumps(dict({"decision_id": d}, **fields), ensure_ascii=False) for d, fields, _ in S10C_REG), encoding="utf-8")
    rep = run("check_register.py", p)
    for d, _, cls in S10C_REG:
        mine = [fl for fl in rep["flags"] if fl.get("decision_id") == d]
        check("check_register %s: %s" % (d, cls or "no flag of any class"), (not mine) if cls is None else any(fl.get("class") == cls for fl in mine), mine)
    p = Path(td) / "tf2c_cm.jsonl"
    p.write_text("\n".join(json.dumps(dict({"decision_id": d}, **f), ensure_ascii=False) for d, f, _ in S10C_CM), encoding="utf-8")
    rep = run("check_marks.py", p)
    for d, _, expects in S10C_CM:
        for rule, want in expects:
            mine = [fl for fl in rep["flags"] if fl.get("decision_id") == d and fl.get("rule") == rule]
            check("check_marks %s: %s %s" % (d, rule, ("fires" if want else "silent") if isinstance(want, bool) else "%s=%s" % want),
                  _cm10c_ok(mine, want), mine)

'''
sub(TEST, 'failed = [r for r in results if not r["ok"]]\n', SECTION10C + 'failed = [r for r in results if not r["ok"]]\n', "section 10c vectors")

# ------------------------------------------------------------------ regenerate
pins = ["citation_sweep.py=" + sha(T / "citation_sweep.py"), "check_marks.py=" + sha(T / "check_marks.py")]
g = run([ADAPT, "--replace"] + pins, T)
out = {"applied": applied, "regen_exit": g.returncode, "regen": g.stdout.strip().splitlines()[-6:], "regen_err": g.stderr[-1500:]}
if g.returncode != 0:
    print(json.dumps(out, ensure_ascii=False, indent=1))
    raise SystemExit(1)
out["citation_sweep_unchanged_from_batch1"] = sha(T / "citation_sweep.py") == b1["files"]["citation_sweep.py"]["staged_sha256"]

out["tests"] = test_summary(json_or_tail(run([TEST], T)))
lib = json_or_tail(run([LIB], T))
out["ezek_lib_selftest"] = {k: lib.get(k) for k in ("checks", "passed", "failed", "verdict", "error", "stdout_tail", "stderr_tail") if k in lib}
out["toolkit_selfcheck"] = {k: v for k, v in json_or_tail(run([T / "_toolkit_selfcheck.py"], T)).items() if k in ("checks", "passed", "verdict", "error", "stdout_tail")}
vs = json_or_tail(run([VER, "--selftest"], ST / "campaign"))
out["verifier_selftest"] = {"vectors": vs.get("vectors"), "failed": vs.get("failed"), "verdict": vs.get("verdict"),
                            "failed_vectors": [r for r in vs.get("results", []) if not r.get("ok")], **({"error": vs} if vs.get("error") else {})}
out["verifier_real_claims"] = {}
for cf in ("ezek_cure_claims.v1.jsonl", "ezek_cure_claims_toolkit_repair.v1.jsonl"):
    vr = json_or_tail(run([VER, "--claims", EZ / cf, "--root", EZ, "--rulings"] + RULINGS + ["--require-rulings"], ST / "campaign"))
    out["verifier_real_claims"][cf] = {k: vr.get(k) for k in ("claims", "accepted", "refused", "superseded", "supersession_classes", "verdict", "error")}

# ------------------------------------------------------------------ discrimination: installed tools and batch1's staged tools
out["discrimination"] = {}
for label, overlay in (("installed", False), ("batch1_staged", True)):
    base = build_tree(SCR / ("stage_tf2c_base_" + label), overlay)
    shutil.copyfile(TEST, base / "Ezek" / "tools" / "_test_zone_tools_ezek.py")
    bt = test_summary(json_or_tail(run([base / "Ezek" / "tools" / "_test_zone_tools_ezek.py"], base / "Ezek" / "tools")))
    out["discrimination"][label] = {"checks": bt.get("checks"), "passed": bt.get("passed"), "failed": bt.get("failed"),
                                    "failed_outside_10b_10c": [c for c in bt.get("failed") or [] if "tf2b" not in c and "_e5_" not in c and "10c" not in c],
                                    "error": bt.get("error")}
NAMED_DISCRIMINATING = {"cs_e5_nc_proclitic_stripped_label_refused": "installed", "cm_e5_w1_mark_before_onset_ok": "installed and batch1_staged",
                        "cm_e5_w2_distant_negator_silent": "batch1_staged", "cm_e5_w5_negator_heads_list_ok": "batch1_staged",
                        "cm_e5_w6_no_pe_or_samekh_true_silent": "batch1_staged"}
ids10c = [l.split('("', 1)[1].split('"', 1)[0] for l in SECTION10C.splitlines() if l.strip().startswith('("') and "_e5_" in l]
vec = {}
for vid in ids10c:
    vec[vid] = {base: any(vid in c for c in out["discrimination"][base]["failed"] or []) for base in ("installed", "batch1_staged")}
out["vectors_10c"] = {vid: {"fails_on_installed": v["installed"], "fails_on_batch1_staged": v["batch1_staged"],
                            "ruling_names_discriminating_against": NAMED_DISCRIMINATING.get(vid)} for vid, v in vec.items()}
out["named_discrimination_holds"] = all(all(vec.get(vid, {}).get(b) for b in want.split(" and ")) for vid, want in NAMED_DISCRIMINATING.items())

# ------------------------------------------------------------------ condition (c)
def suite(tree, label):
    d = tree / "Ezek" / "repair" / ("suite_" + label)
    d.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CHAIN_HEAD, d / "rows.jsonl")
    assert sha(d / "rows.jsonl") == CHAIN_HEAD_SHA
    run([tree / "Ezek" / "tools" / "run_validator_suite.py", d / "rows.jsonl"], tree / "Ezek" / "tools")
    return json.loads((d / "rows.jsonl.validator_report.json").read_text(encoding="utf-8"))


R3 = suite(ST, "tf2c")
R1 = suite(SCR / "stage_tf2c_base_batch1_staged" / "sp_durable", "b1")
b1_impact = json.loads((B1 / "corpus_impact.json").read_text(encoding="utf-8"))
exp_cs = b1_impact["lists"]["citation_sweep.problems"]["added"]
exp_norm = b1_impact["lists"]["hebrew_normalize_dryrun.defects"]["added"]


def ms(xs):
    return Counter(json.dumps(x, sort_keys=True, ensure_ascii=False) for x in xs)


cs3, cs1 = R3["citation_sweep"].get("problems", []), R1["citation_sweep"].get("problems", [])
n3, n1 = R3["hebrew_normalize_dryrun"].get("defects", []), R1["hebrew_normalize_dryrun"].get("defects", [])
hard = {"citation_sweep_equals_enumerated_10": ms(cs3) == ms(exp_cs) and len(exp_cs) == 10,
        "citation_sweep_batch1_base_reproduces": ms(cs1) == ms(exp_cs),
        "normalizer_equals_enumerated": ms(n3) == ms(exp_norm), "normalizer_distinct": len({json.dumps(x, ensure_ascii=False) for x in n3}),
        "normalizer_batch1_base_reproduces": ms(n1) == ms(exp_norm),
        "other_hard_members_unchanged": all(R3[k].get("status") == R1[k].get("status") for k in ("ngram7", "cap_sweep")),
        "summary_tf2c": R3.get("summary"), "summary_batch1": R1.get("summary"),
        "outside_the_set": {"citation_sweep": [x for x in cs3 if x not in exp_cs], "normalizer": [x for x in n3 if x not in exp_norm]}}


def key_counter(rep, member, idkeys=("decision_id",)):
    return Counter((next((fl.get(k) for k in idkeys if fl.get(k)), None), fl.get("rule") or fl.get("class")) for fl in rep[member].get("flags", []))


m3, m1 = key_counter(R3, "mark_symmetry"), key_counter(R1, "mark_symmetry")
EXPECT_REMOVED = Counter({("P01-003", "paragraph_mark_claim"): 1, ("P02-013", "paragraph_mark_claim"): 1, ("P08-007", "paragraph_mark_claim"): 1,
                          ("P08-010", "paragraph_mark_claim"): 1, ("P08-014", "paragraph_mark_claim"): 1, ("P08-015", "paragraph_mark_claim"): 1,
                          ("P09-002", "paragraph_mark_claim"): 1, ("P09-003", "paragraph_mark_claim"): 1, ("P09-011", "paragraph_mark_claim"): 1,
                          ("P01-014", "false_kq_absence_claim"): 2, ("P02-020", "false_kq_absence_claim"): 1, ("P09-002", "false_kq_absence_claim"): 1,
                          ("P10-008", "false_kq_absence_claim"): 1, ("P10-014", "false_kq_absence_claim"): 1,
                          ("P10-003", "kq_claim"): 1, ("P10-005", "kq_claim"): 1, ("P10-006", "kq_claim"): 1,
                          ("P02-002", "paragraph_mark_claim"): 2})
KEEPS = [("P03-007", "false_kq_absence_claim"), ("P03-016", "false_kq_absence_claim"), ("P11-012", "paragraph_mark_claim")]
removed, added = m1 - m3, m3 - m1
flags3, flags1 = ms(R3["mark_symmetry"].get("flags", [])), ms(R1["mark_symmetry"].get("flags", []))
shape_changed = sorted({k for k in (m1 & m3)
                        if Counter(x for x in (flags1 - flags3).elements() if (json.loads(x).get("decision_id"), json.loads(x).get("rule")) == k)})
marks = {"removed": sorted([list(k) + [n] for k, n in removed.items()]), "added": sorted([list(k) + [n] for k, n in added.items()]),
         "removed_equals_expected": removed == EXPECT_REMOVED,
         "expected_not_removed": sorted([list(k) + [n] for k, n in (EXPECT_REMOVED - removed).items()]),
         "removed_not_expected": sorted([list(k) + [n] for k, n in (removed - EXPECT_REMOVED).items()]),
         "keeps_hold": all(m3.get(k, 0) >= 1 for k in KEEPS), "shape_or_context_changed_same_row_rule": [list(k) for k in shape_changed],
         "added_items": [json.loads(x) for x in (flags3 - flags1).elements() if (json.loads(x).get("decision_id"), json.loads(x).get("rule")) in added],
         "removed_unexpected_items": [json.loads(x) for x in (flags1 - flags3).elements()
                                      if (json.loads(x).get("decision_id"), json.loads(x).get("rule")) in (removed - EXPECT_REMOVED)]}
g3 = key_counter(R3, "register", ("writer_decision_id", "decision_id"))
g1 = key_counter(R1, "register", ("writer_decision_id", "decision_id"))
register = {"batch1_flags": sum(g1.values()), "tf2c_flags": sum(g3.values()),
            "added_per_row": sorted([list(k) + [n] for k, n in (g3 - g1).items()]), "removed_per_row": sorted([list(k) + [n] for k, n in (g1 - g3).items()]),
            "added_items": [json.loads(x) for x in (ms(R3["register"].get("flags", [])) - ms(R1["register"].get("flags", []))).elements()]}
e15d = lambda rep: sum(1 for fl in rep["web_quotes"].get("flags", []) if "e15d" in str(fl.get("issue")))
web_quotes = {"e15d_tf2c": e15d(R3), "e15d_batch1": e15d(R1), "stays_at_10": e15d(R3) == 10 == e15d(R1),
              "all_web_quotes_flags_unchanged": ms(R3["web_quotes"].get("flags", [])) == ms(R1["web_quotes"].get("flags", []))}
moved = {}
for k in sorted(set(R1) | set(R3)):
    a_, b_ = R1.get(k), R3.get(k)
    if isinstance(a_, dict) and isinstance(b_, dict):
        for kk in sorted(set(a_) | set(b_)):
            if isinstance(a_.get(kk), list) and isinstance(b_.get(kk), list) and ms(a_[kk]) != ms(b_[kk]):
                moved["%s.%s" % (k, kk)] = {"batch1": len(a_[kk]), "tf2c": len(b_[kk])}
impact = {"against": "batch1's staged tools over the chain head 6ff71fa6 (run here from their digest-bound bytes)",
          "hard": hard, "check_marks": marks, "register": register, "web_quotes": web_quotes, "lists_moved_vs_batch1": moved}
(ROOT / "corpus_impact.json").write_text(json.dumps(impact, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
out["condition_c"] = {"hard": {k: v for k, v in hard.items() if k not in ("summary_tf2c", "summary_batch1")}, "summaries": [hard["summary_batch1"], hard["summary_tf2c"]],
                      "check_marks": {k: marks[k] for k in ("removed_equals_expected", "expected_not_removed", "removed_not_expected", "added", "keeps_hold",
                                                            "shape_or_context_changed_same_row_rule")},
                      "register": {k: register[k] for k in ("batch1_flags", "tf2c_flags", "added_per_row", "removed_per_row")},
                      "web_quotes": web_quotes, "lists_moved_vs_batch1": moved}
out["staged_digests"] = {n: sha(T / n) for n in TOOL_FILES}
out["staged_digests"]["campaign/_cure_verification.py"] = sha(VER)
(ROOT / "stage_run.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({k: out[k] for k in ("applied", "regen_exit", "citation_sweep_unchanged_from_batch1", "tests", "ezek_lib_selftest", "toolkit_selfcheck",
                                      "verifier_selftest", "verifier_real_claims", "discrimination", "vectors_10c", "named_discrimination_holds", "condition_c")},
                 ensure_ascii=False, indent=1)[:28000])
