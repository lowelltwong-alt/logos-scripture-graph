#!/usr/bin/env python3
"""Land the step-2 reconciliation ANALYSIS durably and bring the resume carriers current (E-37).

Nothing is decided and nothing is applied to the rows. Order: (1) artifacts with manifest, (2) handoff addendum,
(3) queue E13-100, (4) the resume prompt's two quoted values (handoff digest, queue range), then the checker.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

NOW = datetime.now(timezone.utc).isoformat()
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
EZ = M8 / "sp_durable" / "Ezek"
S2 = Path(__file__).resolve().parent / "ezek_step2"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
ROWS_SHA = "1238eb2443c2e2b02ffd15ccc26cd8bd6acef0aecd5646e24500ba8417799425"
if sha(EZ / "repair" / "rows_v7_cwo24.jsonl") != ROWS_SHA:
    raise SystemExit("REFUSED: rows moved")

rec = json.loads((S2 / "reconciliation.v1.json").read_text(encoding="utf-8"))
delta = json.loads((S2 / "suite_runs" / "suite_delta.json").read_text(encoding="utf-8"))
if rec["inputs"]["live_rows_sha256"] != ROWS_SHA:
    raise SystemExit("REFUSED: the reconciliation was computed on different rows")

# ---------------------------------------------------------------- (1) artifacts
DST = EZ / "repair2" / "step2_reconciliation"
DST.mkdir(parents=True, exist_ok=True)
files = {"reconciliation.v1.json": S2 / "reconciliation.v1.json",
         "suite_delta_lanes_a_b.json": S2 / "suite_runs" / "suite_delta.json",
         "reconcile.py": S2 / "reconcile.py",
         "suite_candidates.py": S2 / "suite_candidates.py",
         "patch_position_arm.py": S2 / "patch_position_arm.py",
         "land_step2_analysis.py": Path(__file__).resolve()}
man = {}
for name, src in files.items():
    shutil.copyfile(src, DST / name)
    if sha(DST / name) != sha(src):
        raise SystemExit("REFUSED: copy mismatch %s" % name)
    man[name] = sha(src)
(DST / "MANIFEST.json").write_text(json.dumps({
    "what": "REPAIR-2 step 2 reconciliation ANALYSIS - nothing decided, nothing applied",
    "rows_sha256": ROWS_SHA, "written_at": NOW, "sha256": man}, indent=1), encoding="utf-8", newline="\n")

ra, rb = delta["lane_a"], delta["lane_b"]
chg = lambda x, m: x["members_that_changed"].get(m, {})                        # noqa: E731
tally = rec["tally"]
divk, only_b, only_a, rem_a, rem_b = {}, 0, 0, 0, 0
for r in rec["per_row"]:
    for d in r["divergent"]:
        divk[d["kind"]] = divk.get(d["kind"], 0) + 1
        if d["kind"] == "verses named by one lane only":
            only_a += len(d["only_A"]); only_b += len(d["only_B"])
        if d["kind"].startswith("live sentences"):
            rem_a += len(d["only_A_removed"]); rem_b += len(d["only_B_removed"])
shared = [s["row"] for s in rec["shared_constraints_not_corroboration"]]

# ---------------------------------------------------------------- (2) handoff addendum
H = EZ / "EZEK_PAUSE_HANDOFF_REPAIR2.v1.md"
h_before = sha(H)
add = [
    "", "## Addendum (same session, after the pause) - step-2 reconciliation ANALYSIS: nothing decided, nothing applied", "",
    "Supersedes items 5 and 6 of the step-2 docket above. Artifacts: `repair2/step2_reconciliation/MANIFEST.json`. Rows unchanged at `1238eb24...`.", "",
    "**Pinned suite, item by item against the live baseline (PYTHONUTF8=1):**", "",
    "- Lane A: register 116 -> 105 (11 removed, 0 added); web_quotes 40 -> 39 (P08-012's single-curly quote cleared); refs_mirror stays GREEN (+6 far-side citations, no duty); universals 665 -> 680 (triage); ngram7 worst reuse is lane A's own 'is the shape this row's medium' in 9 rows against a gate of 10 - vary it. No hard member moved.",
    "- Lane B: register 116 -> 105 (11 removed, 0 added); **refs_mirror GREEN -> FLAGS with +13 worklist citations** - exactly the 13 uncovered argued citations lane B disclosed, so the PINNED member does enforce the A4 duty (the correction to E13-98 is confirmed from both sides); mark_symmetry 4 -> 5 (+1 at P02-008: 'chapter 10 carries no parashah mark' flagged false_mark_absence_claim because the span's 11:1 carries a PE - the claim is about chapter 10 and #e15 Q4 states it true, so this looks like a member false positive, INFERRED, needing a reader); universals 665 -> 686; web_quotes unchanged (lane B did not clear the P08-012 quote flag).",
    "", "**Claims-level reconciliation (`reconcile.py`, selftest 11/11):** %d rows, %d comparisons - %s. Every stated grade matches its row in both lanes; no verse is placed verse-final by one lane and mid-verse by the other; all quoted Hebrew is EXACT, an unpointed skeleton, or a labelled Qere." % (rec["rows"], rec["comparisons"], ", ".join("%s %d" % kv for kv in sorted(tally.items()))),
    "", "**Divergence shape (choices, not factual disagreement):** verses named only by B %d, only by A %d; device-word divergences %d; live sentences removed only by A %d, only by B %d. Shared gate constraint on %s - agreement there is the brief's wall, not corroboration." % (only_b, only_a, divk.get("devices named by one lane only", 0), rem_a, rem_b, ", ".join(shared)),
    "", "**Three reader defects in my own reconciler, fixed before the result was trusted, each with a regression fixture:** a mis-designed Qere fixture; position words bound to every verse in a sentence (a false P03-015 conflict over identical claims worded 'mid-verse recurrences' and 'non-final recurrences'); and position claims collapsed into a dict keyed by verse, so an assertion and a rejected hypothetical for the same verse survived arbitrarily per lane (a false P03-017 conflict at 18:23).",
    "", "**Decisions still owed at reconciliation - NOT taken here:**", "",
    "1. Per row, lane A's position-phrasing or lane B's numbered verses; if B's, install the matching refs entries in the SAME batch, each already carrying its ROLE token and face qualifier, or refs_mirror goes FLAGS.",
    "2. Vary lane A's templated phrase before it reaches the ngram7 gate.",
    "3. Read the P02-008 mark_symmetry flag against the bytes.",
    "4. Both lanes KEPT a live sentence at P03-015 rejecting the fused 18:5-20 row because 18:9's utterance is verse-final; under #e15's ch-18 class ruling a verse-final utterance followed by no fresh onset is paragraph-final, so that ground may be stale - reconciliation or #e16.",
    "5. The calls already listed in item 4 of the docket above.",
    "",
]
with H.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(add))
h_after = sha(H)

# ---------------------------------------------------------------- (3) queue
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
q = {"id": "E13-100", "opened_at": NOW, "severity": "MEDIUM", "tier": "MEASURED",
     "headline": ("STEP-2 RECONCILIATION ANALYSIS DONE (nothing decided, nothing applied): 0 CONFLICT in %d "
                  "comparisons - the two blind lanes agree on every checkable claim; lane B's 13 numbered citations "
                  "take the pinned refs_mirror GREEN -> FLAGS, confirming the A4 duty is enforced; three defects in my "
                  "own reconciler fixed first." % rec["comparisons"]),
     "raised_by": "orchestrator (claude-opus-5)", "status": "ANALYSIS - decisions owed at reconciliation",
     "blocks_close": True,
     "artifacts": {"dir": "Ezek/repair2/step2_reconciliation", "manifest_sha256": sha(DST / "MANIFEST.json")},
     "handoff": {"file": "Ezek/EZEK_PAUSE_HANDOFF_REPAIR2.v1.md", "sha256_before_addendum": h_before,
                 "sha256_after_addendum": h_after},
     "suite": {"lane_a_register": "116->105", "lane_b_register": "116->105",
               "lane_b_refs_mirror": "GREEN->FLAGS +13 worklist citations", "lane_b_mark_symmetry": "4->5 (P02-008)",
               "lane_a_web_quotes": "40->39", "lane_a_ngram7_worst": "9 rows vs gate 10"},
     "reconciliation": {"tally": tally, "comparisons": rec["comparisons"], "verses_only_B": only_b,
                        "verses_only_A": only_a, "shared_constraint_rows": shared},
     "reader_defects_fixed": ["Qere fixture design", "sentence-level position binding (false P03-015 conflict)",
                              "dict collapse of position claims (false P03-017 conflict at 18:23)"]}
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(q, ensure_ascii=False) + "\n")

# ---------------------------------------------------------------- (4) resume prompt: two quoted values only
P = M8 / "RESUME_PROMPT_CURRENT.md"
t = P.read_text(encoding="utf-8")
old_h = "EZEK_PAUSE_HANDOFF_REPAIR2.v1.md (sha256 %s…)" % h_before[:8]
old_q = "queue E13-01..E13-99"
if t.count(old_h) != 1 or t.count(old_q) != 1:
    raise SystemExit("REFUSED: prompt anchors not found exactly once (%d, %d)" % (t.count(old_h), t.count(old_q)))
t = t.replace(old_h, "EZEK_PAUSE_HANDOFF_REPAIR2.v1.md (sha256 %s…)" % h_after[:8]).replace(old_q, "queue E13-01..E13-100")
P.write_text(t, encoding="utf-8", newline="\n")
CHK = M8 / "sp_durable" / "Jer" / "_safe_to_clear_check.py"
env = dict(os.environ, PYTHONUTF8="1")
c1 = subprocess.run([sys.executable, str(CHK), str(P)], cwd=str(CHK.parent), capture_output=True, text=True,
                    encoding="utf-8", env=env).stdout.strip().splitlines()[-1]
c2 = subprocess.run([sys.executable, str(CHK), "--selftest"], cwd=str(CHK.parent), capture_output=True, text=True,
                    encoding="utf-8", env=env).stdout.strip().splitlines()[-1]
print(json.dumps({"artifacts": len(man), "handoff_sha256": h_after, "queue": "E13-100",
                  "prompt_sha256": sha(P), "check": c1[:60], "selftest": c2}, indent=1))
