"""Build 1Cor strategy candidate a2 from a1 by applying the blind checks C1 (13 defects) and C2 (6 defects).
Every find must occur exactly the stated number of times; plan edits are structural (one string field, one hit).
Every double-quoted string and opening-word cell in the result is re-checked against the WEB, RP and SBL bytes.
usage: make_a2.py --dry | --install     (dry writes to ./a2_dry; install writes new files, never overwriting)"""
import hashlib
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from web_lib import load_web  # noqa: E402

SP1 = Path("C:/wt/logos-t423-m8-fable/.ai/scratch/multi_model_bible_chunking/M8_fable/sp_durable/1Cor")
CAND = SP1 / "strategy_candidate"
A1_MD, A1_PL = CAND / "book_strategy_1Cor.a1.md", CAND / "strategy_plan_1Cor.a1.json"
sha = lambda b: hashlib.sha256(b).hexdigest()  # noqa: E731
mode = sys.argv[1]
assert mode in ("--dry", "--install")


def load_tsv(name):
    out = {}
    for l in (SP1 / name).read_text(encoding="utf-8").splitlines():
        if "\t" in l:
            r, t = l.split("\t", 1)
            out[r.split(".", 1)[1].replace(".", ":")] = t
    return out


rp, sbl, web = load_tsv("1Cor_rp.txt"), load_tsv("1Cor_sbl.txt"), load_web()
strip = lambda s: "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c)).lower()  # noqa

# --- measured facts this script asserts (named as MEASURED, make_a2.py in the text) ---
assert "Μαρὰν ἀθά." in rp["16:22"] and "⸂Μαράνα θά⸃." in sbl["16:22"], "maranatha slices"
assert rp["9:1"].index("ἀπόστολος") < rp["9:1"].index("ἐλεύθερος"), "RP 9:1 order"
assert web["9:1"].index("free") < web["9:1"].index("apostle"), "WEB 9:1 order"
assert "ἀπολογία" in rp["9:3"], "9:3 apologia"
s613, s614 = strip(rp["6:13"]), strip(rp["6:14"])
assert all(w in s613 for w in ("βρωμασιν", "ο δε θεος", "καταργησει")) and "εξεγερει" in s614, "6:13/6:14 words"

FABLE = "a working answer, listed for Fable's end review"
MD_EDITS = [  # (defect, find, replace, expected count)
    ("C1 DEF-01", "also at 7:5 and 14:26)", "also at 7:5, 14:23 and 14:26; SBL lacks 7:5)", 1),
    ("C1 DEF-02", "; a further verse-initial tois de stands at 1:24)", ")", 1),
    ("C1 DEF-03", "It occurs at 22 RP verses and 21 SBL verses (MEASURED, device inventory adelphoi).",
     "The form ἀδελφοί occurs at 22 RP verses and 21 SBL verses (EXTRACTED, device inventory adelphoi); 20 of the RP "
     "verses carry it without a preceding article, the articular 9:5 and 16:20 being nominative, not vocative.", 1),
    ("C1 DEF-04", "- the vocative adelphoi (22 RP verses);",
     "- the vocative adelphoi (20 RP verses without a preceding article; 22 counting the articular nominatives at 9:5 "
     "and 16:20);", 1),
    ("C1 DEF-06", "Now I beg you, brothers, through the name ...", "Now I beg you, brothers, ...", 1),
    ("C1 DEF-07", "But in giving you this command I don't ...", "But in giving you this command I don\u2019t ...", 1),
    ("C1 DEF-08", "Now concerning spiritual things, brothers, I don't want ...",
     "Now concerning spiritual things, brothers, I don\u2019t want ...", 1),
    # C1 DEF-09 option (a): WEB byte slices; ouk oidate and to teleion become labelled glosses
    ("C1 DEF-09", "Greek is quoted from RP and English from WEB, both sliced by script (gen_strategy.py, ledger in "
     "quote_ledger.json). Nothing here is typed from memory.",
     "Greek is quoted from RP and English from WEB, both sliced by script (gen_strategy.py, ledger in "
     "quote_ledger.json); the quotations added in version a2 were checked against the witness bytes by the "
     "orchestrator's make_a2.py and are not in that ledger. Transliterated Greek words (for example ouk oidate) are "
     "labelled glosses, not quotations. Nothing here is typed from memory.", 1),
    ("C1 DEF-09", "The \"do you not know\" question binds",
     "The question ouk oidate (transliterated gloss; WEB \"Don\u2019t you know\") binds", 1),
    ("C1 DEF-09", "- \"do you not know\" (ten hits);", "- the question ouk oidate (transliterated gloss; ten hits);", 1),
    ("C1 DEF-09", "- \"do you not know\" (ten);", "- the question ouk oidate (ten);", 1),
    ("C1 DEF-09", "14:37 opens a conditional \"if anyone thinks\"", "14:37 opens a conditional, \"If any man thinks\"", 1),
    ("C1 DEF-09", "readings of \"the perfect\" at 13:8-13:12",
     "readings of to teleion (transliterated gloss; WEB \"that which is complete\") at 13:8-13:12", 1),
    ("C1 DEF-09", "7:12 marks \"I, not the Lord\"", "7:12 marks \"I\u2014not the Lord\u2014\"", 1),
    ("C1 DEF-09", "1:17, \"for Christ did not send me to baptize\", hinges",
     "1:17, \"For Christ sent me not to baptize\", hinges", 1),
    ("C1 DEF-09", "a self-referential \"I write these things\"",
     "a self-referential statement about the writing, \"I don\u2019t write these things to shame you\"", 1),
    ("C1 DEF-09", "At 7:1 (\"it is good for a man...\")", "At 7:1 (\"it is good for a man not to touch a woman\")", 1),
    ("C1 DEF-09", "5. Every opening-word cell and every Greek or English quotation in this file was sliced by script. The "
     "ledger is in quote_ledger.json.",
     "5. Every opening-word cell and every Greek or English quotation in this file was sliced by script: the a1 "
     "quotations by gen_strategy.py (ledger quote_ledger.json); in version a2, make_a2.py re-checked every quoted string "
     "and opening-word cell against the WEB, RP and SBL bytes. Transliterations are labelled glosses.", 1),
    # C1 DEF-10 option (a)
    ("C1 DEF-10", "Calibration: RP has 5514 distinct 4-token runs, of which 72 recur in more than one verse (MEASURED, "
     "gen_strategy.py).",
     "Calibration: RP has 5513 distinct 4-token runs, of which 73 recur in more than one verse (MEASURED, check2_c1.py "
     "in blind check C1 and the orchestrator's spot_C1.py: NFD with combining marks stripped, lowercase, word tokens; "
     "the figure holds with or without final-sigma folding). The lane's gen_strategy.py figure, 5514 and 72, did not "
     "reproduce and is superseded.", 1),
    # C1 DEF-12 option (a), merged with C2 DEF-05 option A
    ("C1 DEF-12", "The row 14:34-14:36 (or a row through 14:40, if a writer finds no signal at 14:36/14:37) carries "
     "three disclosures:",
     "Both rows meeting at the 14:33/14:34 seam (the row ending at 14:33, and the row opening at 14:34, which runs to "
     "14:36 or, if a writer finds no signal at 14:36/14:37, through 14:40) carry three disclosures:", 1),
    ("C2 DEF-05", "- the 14:33b attachment and the transposition on the row holding 14:33-14:36;",
     "- the 14:33b attachment and the transposition on the row or rows covering 14:33b-14:36 (both rows meeting at the "
     "14:33/14:34 seam);", 1),
    ("C2 DEF-05", "- the backward reading on the row opening at 15:50;",
     "- the rival reading of 15:50 (closing 15:35-15:49, or opening 15:50-15:58) on the row at 15:50 or 15:51;", 1),
    ("C2 DEF-05", "Those rows must stand alone (§7).",
     "Rows in those parents are cut finely enough that the 14:33b-14:36 disclosures and the 15:50/15:51 question sit "
     "on the rows that carry them; which rows those are is the writer's choice under §7.", 1),
    ("C2 DEF-05", "the row discloses that 12:31b introduces chapter 13 (C).",
     "the row discloses that 12:31b introduces chapter 13 (C). This is " + FABLE + ".", 1),
    ("C2 DEF-05", "attaches backward (INFERRED).", "attaches backward (INFERRED; " + FABLE + ").", 1),
    ("C2 DEF-05", "because whether it digresses is itself a divided reading.",
     "because whether it digresses is itself a divided reading. The rival reading takes chapter 9 as a defence, on the "
     "word ἀπολογία at 9:3 (MEASURED, make_a2.py); a row in chapter 9 names it. The typing is " + FABLE + ".", 1),
    # C1 DEF-13 option (a): record readings re-tiered EXTRACTED; bare MEASURED tags given a script; line 383 REPORTED
    ("C1 DEF-13", "(MEASURED at staging, web_greek_offset_map.json:", "(EXTRACTED, web_greek_offset_map.json:", 1),
    ("C1 DEF-13", "(MEASURED, device inventory", "(EXTRACTED, device inventory", 10),
    ("C1 DEF-13", "(MEASURED, cor_lib docstring and pmarks rp_sbl_differences)",
     "(EXTRACTED, cor_lib docstring and pmarks rp_sbl_differences)", 1),
    ("C1 DEF-13", "θά⸃.\" (MEASURED).", "θά⸃.\" (MEASURED, make_a2.py slices RP and SBL 16:22).", 1),
    ("C1 DEF-13", "departing from RP at least once (MEASURED).",
     "departing from RP at least once (MEASURED, make_a2.py: in RP 9:1 ἀπόστολος precedes ἐλεύθερος; in the WEB "
     "\"free\" precedes \"apostle\").", 1),
    ("C1 DEF-13", "where a mark is recorded on the verse it follows.",
     "where a mark is recorded on the verse it follows (REPORTED: method record v7 §6, which is not a pinned input of "
     "the strategy lane; logged in CYCLE_STATE as a method-change candidate for the book-close proposal loop).", 1),
    # C2 exact corrections
    ("C2 DEF-01", "14. Carry both attribution lines (§3) with any quotation.",
     "14. Carry both Greek attribution lines with any Greek quotation: Robinson-Pierpont Byzantine Textform "
     "(Unlicense); SBLGNT (CC BY 4.0).", 1),
    ("C2 DEF-02", "15. Row prose must not reproduce an unquoted witness run (convention C2).",
     "15. Row prose must not reproduce an unquoted witness run: four or more consecutive tokens matching the RP or SBL "
     "text of the row's verses, or of one verse on either side, compared with accents, case and punctuation removed. "
     "A script-sliced quotation carrying its witness tag is exempt.", 1),
    ("C2 DEF-03", "read differently by Latter-day Saint and mainstream traditions",
     "read differently in Latter-day Saint practice and in Catholic, Orthodox and Protestant readings", 1),
    # C2 DEF-04 option A: the adopted shape argued from text links; the scorer record kept as corroboration only
    ("C2 DEF-04", "   - Against, for 12-14: the scorer's boundary-risk record says 1:10-4:21, 8:1-11:1 and 12:1-14:40 "
     "are each one argument and that a parent seam at 9:1 or 10:1 severs the idol-food argument (REPORTED, "
     "hardness_batch_03). For 12-14 the text gives a measured bracket:",
     "   - Against, for 8:1-11:1: the text ties chapters 8, 9 and 10 together. The idol-food word eidolothyt- "
     "(transliterated gloss) stands at 8:1, 8:4, 8:7 and 8:10 and returns at 10:19 and 10:28; syneidesis (conscience) "
     "stands at 8:7, 8:10 and 8:12 and returns at 10:25, 10:27, 10:28 and 10:29; exousia (right) at 8:9 is carried into "
     "chapter 9 at 9:4, 9:5, 9:6, 9:12 and 9:18; eleuther- (free) stands at 9:1, 9:19 and 10:29 (MEASURED, "
     "measure_a2.py: accent-stripped stems on RP, counted within 8:1-11:1; blind check C2's b_lex.py gives the same "
     "verses).\n"
     "   - Against, for separate parents at 2:1 and 3:1: the naming of Apollos at 1:12 resumes at 3:4, 3:5, 3:6, 3:22 "
     "and 4:6, and of Kephas at 1:12 resumes at 3:22 (MEASURED, measure_a2.py, counted within 1:10-4:21).\n"
     "   - Corroboration only: the scorer's boundary-risk record says 1:10-4:21, 8:1-11:1 and 12:1-14:40 are each one "
     "argument and that a parent seam at 9:1 or 10:1 severs the idol-food argument (REPORTED, hardness_batch_03). It "
     "is not the ground of the adoption.\n"
     "   - Against, for 12-14: the text gives a measured bracket:", 1),
    # C2 DEF-06 option A: 6:13 named as a contested extent
    ("C2 DEF-06", "  - at 6:13, \"Τὰ βρώματα τῇ κοιλίᾳ,\", the response begins with a contrasting clause.",
     "  - at 6:13, \"Τὰ βρώματα τῇ κοιλίᾳ,\", the extent of the second slogan is itself contested: it may end after "
     "the first pair (after tois bromasin, transliterated gloss) or run through katargesei. The text signals are the de "
     "of ho de theos, which may open the response, and the parallel future at 6:14 (ho de theos ... exegerei), which "
     "answers katargesei.", 1),
    ("C2 DEF-06", "- At 7:1 (", "- At 6:13 (the second slogan), at 7:1 (", 1),
    ("C2 DEF-06", "every row holding 7:1, 8:1, 8:4 or 8:8 carries", "every row holding 6:13, 7:1, 8:1, 8:4 or 8:8 carries",
     1),
]
VERSION_NOTE = ("\nVersion a2 (orchestrator reconciliation, 2026-10-15): applies blind strategy checks C1 (13 defects) "
                "and C2 (6 defects). Every changed passage is listed in a2_reconciliation.json. The seven judgement "
                "items were adjudicated by the orchestrator without a Fable call (OW-30) and are listed for Fable's end "
                "review.\n")

PLAN_EDITS = [
    ("C1 DEF-05", "nominative or accusative uses (e.g. 16:12) carry no boundary weight",
     "non-vocative uses (e.g. the articular nominative at 9:5 and 16:20) carry no boundary weight"),
    ("C1 DEF-11", "Expected grades: parent A, 15:50 versus 15:51 C, others B.",
     "Expected grades: parent A, creed row 15:1-15:11 A, 15:57-15:58 close A, 15:50 versus 15:51 C, others B."),
    ("C1 DEF-12", "With 14:33 (the row ending at 14:33 discloses that 14:33b may be read with 14:34).",
     "Disclosed on both rows meeting at the 14:33/14:34 seam: the row ending at 14:33 discloses that 14:33b may be "
     "read with 14:34, and the row opening at 14:34 discloses that 14:33b may be read with it."),
    ("C1 DEF-13", "(MEASURED, device inventory year_word 0, month_word 0)",
     "(EXTRACTED, device inventory year_word 0, month_word 0)"),
    ("C2 DEF-06", "7:1, 8:1, 8:4, 8:8 flagged contested-extent.",
     "6:13 (second slogan), 7:1, 8:1, 8:4, 8:8 flagged contested-extent."),
]
NEW_FABLE = [
    {"question": "Does 12:31, whose second clause points forward, go with the chapter 12 row or open the chapter 13 row?",
     "working_answer": "With chapter 12; the row discloses that 12:31b introduces chapter 13.",
     "evidence": "zeloute at 12:31, 14:1 and 14:39 (MEASURED, gen_strategy.py). Raised by blind check C2 DEF-05; "
                 "orchestrator adjudication, option A, no Fable call (OW-30)."},
    {"question": "Does the rhetorical question at 14:36 attach backward to 14:34-14:35 or forward to 14:37-14:40?",
     "working_answer": "Backward (INFERRED); both rows meeting at the 14:33/14:34 seam carry the 14:33b disclosures.",
     "evidence": "14:37 opens a conditional with an RP pilcrow. Raised by blind check C2 DEF-05; orchestrator "
                 "adjudication, option A, no Fable call (OW-30)."},
    {"question": "Should chapter 9 be typed `example`, or does the rival reading as a defence (ἀπολογία, 9:3) govern its "
                 "unit_type?",
     "working_answer": "`example`, with the defence reading named in a chapter 9 row.",
     "evidence": "exousia at 8:9 carried into 9:4-9:18; eleuther- at 9:1, 9:19, 10:29 (MEASURED, measure_a2.py); "
                 "ἀπολογία at 9:3 (MEASURED, make_a2.py). Raised by blind check C2 DEF-05; orchestrator adjudication, "
                 "option A, no Fable call (OW-30)."},
    {"question": "Were the orchestrator's adjudications of the seven judgement defects from blind strategy checks C1 "
                 "(DEF-09, -10, -12, -13) and C2 (DEF-04, -05, -06) right?",
     "working_answer": "Options chosen: C1 DEF-09 (a), DEF-10 (a), DEF-12 (a), DEF-13 (a); C2 DEF-04 A, DEF-05 A, "
                       "DEF-06 A.",
     "evidence": "strategy_candidate/a2_reconciliation.json; the two check reports in the C1 and C2 landing rows."},
]

md = A1_MD.read_bytes().decode("utf-8")
assert "\r" not in md
log = []
for did, f, r, n in MD_EDITS:
    c = md.count(f)
    assert c == n, "%s: find count %d != %d: %r" % (did, c, n, f[:80])
    md = md.replace(f, r)
    log.append({"defect": did, "file": "md", "find": f, "replace": r, "count": n})
first_nl = md.index("\n", md.index("Nothing here is typed from memory."))
md = md[:first_nl + 1] + VERSION_NOTE + md[first_nl + 1:]
assert "(MEASURED, device inventory" not in md and "(MEASURED)." not in md

plan = json.loads(A1_PL.read_bytes().decode("utf-8"))


def fields(o, path=()):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from fields(v, path + (k,))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from fields(v, path + (i,))
    elif isinstance(o, str):
        yield path, o


def setp(o, path, v):
    for p in path[:-1]:
        o = o[p]
    o[path[-1]] = v


for did, f, r in PLAN_EDITS:
    hits = [(p, s) for p, s in fields(plan) if f in s]
    assert len(hits) == 1 and hits[0][1].count(f) == 1, "%s plan hits %d" % (did, len(hits))
    setp(plan, hits[0][0], hits[0][1].replace(f, r))
    log.append({"defect": did, "file": "plan", "path": list(hits[0][0]), "find": f, "replace": r, "count": 1})
n0 = len(plan["for_fable_end_review"])
plan["for_fable_end_review"].extend(NEW_FABLE)
log.append({"defect": "C2 DEF-05 + adjudication record", "file": "plan", "path": ["for_fable_end_review"],
            "appended": len(NEW_FABLE), "before": n0, "after": len(plan["for_fable_end_review"])})

# --- quotation re-check on the result ---
greek = re.compile(r"[\u0370-\u03ff\u1f00-\u1fff]")
rp_all, sbl_all, web_all = "\n".join(rp.values()), "\n".join(sbl.values()), "\n".join(web.values())
LABELS = {"digression", "slogan extent contested", "SBL reads"}  # terms and disclosure phrases, not quotations
bad = []
for q in re.findall(r"\"([^\"\n]+)\"", md):
    core = q.rstrip(". ").rstrip()
    core = core[:-3].rstrip() if core.endswith("...") else core
    pool = (rp_all + sbl_all) if greek.search(q) else web_all
    if q not in LABELS and q not in pool and core not in pool:
        bad.append(q)
cells = 0
for l in md.split("\n"):
    m = re.match(r"^\| (P\d\d) \| (\d+:\d+)-\d+:\d+ \| \d+ \| (.*?) \.\.\. \|", l)
    if m:
        cells += 1
        if not web[m.group(2)].startswith(m.group(3)):
            bad.append("CELL %s %r" % (m.group(1), m.group(3)))
print("md edits", len(MD_EDITS), "| plan edits", len(PLAN_EDITS), "| fable items", n0, "->",
      len(plan["for_fable_end_review"]), "| cells checked", cells)
print("quotes not found in witness bytes:", bad)

md_b = md.encode("utf-8")
pl_b = (json.dumps(plan, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
rec = {"from": {"md": A1_MD.name, "md_sha256": sha(A1_MD.read_bytes()), "plan": A1_PL.name,
                "plan_sha256": sha(A1_PL.read_bytes())},
       "to": {"md_sha256": sha(md_b), "plan_sha256": sha(pl_b)},
       "adjudication": "orchestrator, claude-opus-5-5 (OW-25), no Fable call (OW-30); every judgement item listed "
                       "for Fable's end review",
       "measurements": ["measure_a2.py (C2 DEF-04 stems)", "measure_a2b.py (WEB slices)", "spot_C1.py (DEF-01, "
                        "DEF-10)", "make_a2.py asserts (16:22, 9:1, 9:3, 6:13-6:14)"],
       "unresolved_quote_checks": bad, "edits": log}
rc_b = (json.dumps(rec, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
out = Path(__file__).resolve().parent / "a2_dry" if mode == "--dry" else CAND
out.mkdir(exist_ok=True)
for name, b in (("book_strategy_1Cor.a2.md", md_b), ("strategy_plan_1Cor.a2.json", pl_b),
                ("a2_reconciliation.json", rc_b)):
    p = out / name
    if mode == "--install":
        assert not bad, "refusing install with unresolved quotes"
        assert not p.exists(), "REFUSED: %s exists" % p
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_bytes(b)
    os.replace(tmp, p)
    print(mode, name, sha(b)[:12], len(b), "CR", b.count(b"\r"))
