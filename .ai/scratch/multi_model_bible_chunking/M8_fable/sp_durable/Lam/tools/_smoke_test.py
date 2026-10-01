#!/usr/bin/env python3
"""Phase-0 toolkit smoke test for Lam (orchestrator only; artifacts removed after). TWO clean rows must
pass every validator (an acrostic-opening row with SAMEKH + paseq + acrostic disclosure; a K/Q row with
ketiv/qere disclosure and the front-seam mark disclosed) and TWO bad rows must be caught on EVERY
planted defect class: the legacy citation classes (X-X form, mark TYPE at a markless verse, range END,
cross-tradition ref, zero-verse, selah, false paseq, false K/Q, small/large letter fabrications, Hebrew
bound to the wrong ref), E-01 (NFD-degraded pointed Hebrew = HARD), E-15c (WEB text in straight
quotes), E-16 (exclusivity claim without a digit), the Aramaic-label arm, an unmirrored ref, a false
mark-absence claim, the register classes, and E-02 (a whole-chapter row at high without the cap).
Full 22-field schema on every row. Hebrew is byte-spliced from verse_map_oshb.json (never typed)."""
from __future__ import annotations
import json, re, subprocess, sys, unicodedata
from pathlib import Path
TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent
oshb = json.loads((TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))
web = json.loads((TOOLS / "verse_map_web.json").read_text(encoding="utf-8"))
pm = json.loads((SPBOOK / "pmarks_Lam.json").read_text(encoding="utf-8"))
def webtxt(ref): return re.sub(r"\[fn [^\]]*\]", " ", web[ref]["text"]).strip()
heb_1_1, heb_1_2, heb_1_6, heb_1_7, heb_1_5 = (oshb[f"Lam.1.{v}"]["text"] for v in (1, 2, 6, 7, 5))
web_1_1, web_1_6, web_2_4 = webtxt("Lam.1.1"), webtxt("Lam.1.6"), webtxt("Lam.2.4")
# preconditions (fail loudly if the data moves)
assert pm["marks"].get("Lam.1.1") == ["SAMEKH"] and pm["marks"].get("Lam.1.2") == ["SAMEKH"] and pm["marks"].get("Lam.1.5") == ["SAMEKH"]
assert pm["marks"].get("Lam.1.22") == ["PE"] and not pm["marks"].get("Lam.5.2") and not pm["marks"].get("Lam.5.3")
assert pm["paseq"].get("Lam.1.1") == 1 and not pm["paseq"].get("Lam.5.4")
assert pm["kq"].get("Lam.1.6") == 1 and not pm["kq"].get("Lam.1.1") and not pm["kq"].get("Lam.5.2")
assert pm["other_segs"] == {}
assert oshb["Lam.1.1"]["acrostic_letter"] == "\u05d0" and oshb["Lam.1.2"]["acrostic_letter"] == "\u05d1"
COMMON = {"book": "Lam", "model_id": "M8_fable", "non_authorizing": True, "literature_type_guess": "lament_poem",
          "confidence": "high", "strong_or_hebrew_tags_used": False, "wj_or_red_letter_considered": "not applicable in the OT substrate",
          "frontier_flag_considered": False, "review_status": "draft", "observed_substrate_signals": ["acrostic.smoke_fixture"]}
def row(did, idx, span, refs, rat, alt, notes, **over):
    r = {**COMMON, "decision_id": did, "chunk_index_in_book": idx, "span": span, "parent_collection": "SMOKE Lam.1.1-Lam.5.22",
         "unit_type": "smoke_stanza", "writer_part": "p00", "writer_decision_id": did, "writer_attempt_id": "smoke_lam_r1",
         "boundary_evidence_refs": refs, "boundary_rationale": rat, "strongest_rejected_alternative": alt, "device_notes": notes}
    r.update(over); return r
clean = [
    row("SMOKE-A", 1, "Lam.1.1-Lam.1.2",
        ["web:Lam.1.1 = oshb:Lam.1.1", "oshb:Lam.1.1 (setumah, single-witness)", "oshb:Lam.1.2 (setumah, single-witness)", "oshb:Lam.1.1 (paseq, single-witness)", "web:Lam.1.2"],
        "The eikhah cry opens the book: \u201c" + web_1_1 + "\u201d (web:Lam.1.1). The Hebrew runs " + heb_1_1 + " (oshb:Lam.1.1). The alef line at oshb:Lam.1.1 and the bet line at oshb:Lam.1.2 open the acrostic of poem one (acrostic letters read from the verse-initial consonants; 22 letters over 22 verses in this chapter). A setumah stands at oshb:Lam.1.1 and at oshb:Lam.1.2 (both single-witness). The paseq count for oshb:Lam.1.1 is one (single-witness; the inventory records the count and no position inside the verse).",
        "A cut after web:Lam.1.1 by itself was rejected; the bet line at web:Lam.1.2 continues the widow figure without a fresh onset.",
        "Acrostic site recorded from the byte inventories."),
    row("SMOKE-B", 2, "Lam.1.6-Lam.1.7",
        ["web:Lam.1.6", "oshb:Lam.1.6 (ketiv/qere, single-witness)", "oshb:Lam.1.5 (setumah, single-witness)", "oshb:Lam.1.6 (setumah, single-witness)", "oshb:Lam.1.7 (setumah, single-witness)", "web:Lam.1.7"],
        "The vav line opens the stanza: \u201c" + web_1_6 + "\u201d (web:Lam.1.6). The Hebrew runs " + heb_1_6 + " (oshb:Lam.1.6; the verse carries one ketiv/qere note, single-witness, disclosed). A setumah stands at oshb:Lam.1.5 on the front seam and at oshb:Lam.1.6 and oshb:Lam.1.7 (all three single-witness). The zayin line at oshb:Lam.1.7 runs " + heb_1_7 + " (oshb:Lam.1.7).",
        "Joining web:Lam.1.7 to the following stanza was rejected; the remembrance line closes on the mocking of the foes.",
        "Two acrostic letters (vav, zayin) recorded from the verse-initial consonants."),
]
bad = [
    row("SMOKE-BAD", 3, "Lam.1.3",                                                   # (1) not X-X form
        ["oshb:Lam.5.2 (petuchah, single-witness)",                                  # (2) mark claim at a markless verse
         "web:Lam.1.1-Lam.1.99",                                                     # (3) range END out of range
         "LXX Lam 1:1 superscription (4QLam)",                                       # (4) cross-tradition in refs
         "web:Lam.5.0",                                                              # (5) zero-verse pseudo-ref
         "oshb:Lam.5.3 (selah)",                                                     # (6) selah fabrication
         "oshb:Lam.5.4 (paseq)",                                                     # (7) no paseq at 5:4 + no disclosure
         "oshb:Lam.5.2 (qere)",                                                      # (8) false K/Q claim
         "oshb:Lam.5.4 (small nun, single-witness)",                                 # (9) small-letter fabrication
         "oshb:Lam.5.3 (large mem, single-witness)"],                                # (10) large-letter fabrication
        "The book's only widow figure - no other chapter does this. There is no setumah anywhere in this span. Lam.2.4 echoes it. "   # (11) universal no digit; (12) false absence (SAMEKH at 1:3); (13) unmirrored ref
        "The quoted line " + heb_1_5 + " (oshb:Lam.1.10) proves it. "                 # (14) Hebrew bound to WRONG ref
        "The faded copy reads " + unicodedata.normalize("NFD", heb_1_2) + " (oshb:Lam.1.2) beside it. "   # (15) E-01 NFD-degraded pointed Hebrew
        "Only this seam matches at byte tier against oshb:Lam.1.2. "                 # (16) E-16 exclusivity + tier, no digit
        "Lam.1.3 is in Aramaic here. That row handles the cross-part seam.",          # (17) Aramaic label; (18) register classes
        "\u201c" + web_2_4 + "\u201d (web:Lam.1.4). Also \"" + web_2_4 + "\" sits near web:Lam.2.4 undelimited.",   # (19) WEB misquote wrong ref; (20) E-15c straight quotes
        "Notes."),
    row("SMOKE-CAP", 4, "Lam.5.1-Lam.5.22", ["web:Lam.5.1", "web:Lam.5.22", "oshb:Lam.5.18 (petuchah, single-witness)"],   # (21) E-02 whole-chapter row at high, no cap disclosure
        "The final prayer runs the whole chapter with a petuchah at oshb:Lam.5.18 (single-witness).", "None.", "Notes."),
]
def run(script, path):
    p = subprocess.run([sys.executable, str(TOOLS / script), str(path)], capture_output=True, text=True, encoding="utf-8")
    try: return json.loads(p.stdout)
    except json.JSONDecodeError: return {"status": "ERROR", "stdout": p.stdout[-800:], "stderr": p.stderr[-800:]}
def write(rows, name):
    p = TOOLS / name; p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8"); return p
clean_p, bad_p = write(clean, "_smoke_clean.jsonl"), write(bad, "_smoke_bad.jsonl")
problems = []
suite_clean = run("run_validator_suite.py", clean_p)
if suite_clean.get("hard_status") != "GREEN" or suite_clean.get("triage_flags", 1) != 0:
    repc = json.loads(clean_p.with_suffix(clean_p.suffix + ".validator_report.json").read_text(encoding="utf-8-sig"))
    problems.append({"clean_rows_not_green": suite_clean.get("per_check"), "clean_flags": {k: repc[k].get("flags") for k in ("web_quotes", "refs_mirror", "mark_symmetry", "universals", "language_zones", "register") if repc[k].get("flag_count")}})
suite_bad = run("run_validator_suite.py", bad_p)
if suite_bad.get("hard_status") != "RED" or not suite_bad.get("nfd_hard_e01"):
    problems.append({"bad_rows_not_red": suite_bad})
rep = json.loads(bad_p.with_suffix(bad_p.suffix + ".validator_report.json").read_text(encoding="utf-8-sig"))
cit = "\n".join(rep["citation_sweep"].get("problems", []))
expect_cit = ["X-X form", "claims petuchah", "range END out of range", "cross-tradition", "Lam.5.0", "selah", "claims paseq", "ketiv/qere", "small letter", "large letter", "does not collate"]
for e in expect_cit:
    if e not in cit: problems.append({"citation_sweep_missed": e})
if not rep["citation_sweep"].get("nfd_degraded_count"): problems.append({"citation_sweep_missed": "nfd_degraded (E-01)"})
marks = json.dumps(rep["mark_symmetry"].get("flags", []))
for e in ("false_mark_absence_claim", "paragraph_mark_claim", "selah_claim", "small_letter_claim", "large_letter_claim"):
    if e not in marks: problems.append({"check_marks_missed": e})
if not any("Lam.2.4" in json.dumps(f) for f in rep["refs_mirror"].get("flags", [])): problems.append({"refs_mirror_missed": "unmirrored Lam.2.4"})
wq = json.dumps(rep["web_quotes"])
if rep["web_quotes"].get("flag_count", 0) < 2 or "e15c" not in wq: problems.append({"web_quotes_missed": "misquote / e15c", "report": rep["web_quotes"].get("flag_count")})
if rep["universals"].get("flag_count", 0) < 1 or not rep["universals"].get("e16_exclusivity_undampened", rep["universals"].get("flag_count")): problems.append({"universals_missed": rep["universals"]})
if rep["language_zones"].get("flag_count", 0) < 1: problems.append({"language_zones": rep["language_zones"].get("flag_count")})
if rep["register"].get("flag_count", 0) < 1: problems.append({"register_missed": rep["register"]})
if rep["cap_sweep"].get("status") != "RED": problems.append({"cap_sweep_not_red": rep["cap_sweep"]})
# collate CLI arm (identity): bare Lam.3.1 at byte tier
col = json.loads(subprocess.run([sys.executable, str(TOOLS / "collate.py"), "--ref", "Lam.3.1", "--quote", oshb["Lam.3.1"]["text"]], capture_output=True, text=True, encoding="utf-8").stdout)
if col.get("tier") != "byte" or col.get("language") != "Hebrew": problems.append({"collate_cli": col})
# tiling over the whole book with a synthetic tiling
til = subprocess.run([sys.executable, str(TOOLS / "check_tiling.py"), str(clean_p), "--range", "Lam.1.1-Lam.1.7"], capture_output=True, text=True, encoding="utf-8")
tiling_note = (til.stdout or til.stderr)[-300:]
for p in (clean_p, bad_p, clean_p.with_suffix(clean_p.suffix + ".validator_report.json"), bad_p.with_suffix(bad_p.suffix + ".validator_report.json")):
    if p.exists(): p.unlink()
print(json.dumps({"clean_suite": {k: suite_clean.get(k) for k in ("hard_status", "nfd_hard_e01", "triage_flags")}, "bad_suite": {k: suite_bad.get(k) for k in ("hard_status", "nfd_hard_e01", "triage_flags")},
                  "bad_per_check": suite_bad.get("per_check"), "collate_cli": col, "tiling_probe_1_1_to_1_7": tiling_note.strip()[:200], "problems": problems,
                  "verdict": "PASS" if not problems else "FAIL"}, ensure_ascii=False, indent=1))
