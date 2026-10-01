#!/usr/bin/env python3
"""Amend the atlas deliverable's README for the v10 hold round, OW-30 (E-44: amend, never edit). Earlier text stays as history.

One section is inserted before the v9 amendment's heading (the anchor must occur exactly once), so the newest amendment
is read first. It gives the ruling, the new input and the new digests, measured here from disk against pins. The README
is saved as .pre_<sha12>. The atlas mirror check is then re-run: its record must still reproduce the shipped one byte
for byte, or the README is restored. The README is LF (measured); a CRLF or mixed file is refused.
usage: amend_atlas_readme_v10.py --dest <scratch dir outside M8>
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
EZ = HERE.parents[1]
SP, D = EZ.parent, EZ / "deliverables"
R = D / "README.md"
R_PIN = "28f14d5d71722e64fb302121ec7678c4a69566a82ba2fd53c5baf6a793c1882a"
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731
ap = argparse.ArgumentParser()
ap.add_argument("--dest", required=True)
a = ap.parse_args()
env = dict(os.environ, PYTHONUTF8="1")
g = subprocess.run([sys.executable, "-B", str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek",
                    "--target", "Ezek/deliverables/README.md"], cwd=str(SP), capture_output=True, text=True,
                   encoding="utf-8", env=env)
if json.loads(g.stdout)["verdict"] != "CLEAR":
    raise SystemExit("REFUSED by pin guard")
before = R.read_bytes()
if sha(before) != R_PIN:
    raise SystemExit("REFUSED: README.md is not at its expected-before digest")
if b"\r" in before:
    raise SystemExit("REFUSED: README.md carries CR bytes; this tool writes LF only")
files = [(D / "atlas_candidate_feed_rows.jsonl", "15bcea3730bfc39a1214a5dbaf293342e0175c5f43b8a6e553b8de908bb32081"),
         (D / "Ezek_atlas_dimensions.v1.jsonl", "2060bd5a965a5a602079ad80ad5ff29e8261eb82023fc88160fb245a2669b7fc"),
         (D / "gen_atlas_rows.py", "b8fa0ea08b8c939fb3630bccd608ba7ad07dd9274015f44d67e4fb927917965e"),
         (D / "check_atlas_rows.py", "2ed2e31786a8a019ca9d26f86bad84751d9d7960aba82600321d9dd9837522c3"),
         (D / "atlas_rows_check.v1.json", "59b38fb385a013b2307e85c5c4e82fb5da4aa07f87886d09335f4db0d68059e6"),
         (D / "gen_sidecars.py", "21ca02dd72fe3f27d4024d58c01a0f1c9a6494e65ea3db648de7f98fbe959923"),
         (EZ / "sidecar_src_ezek.jsonl", "3ad194a1077fb0a20c473666011148b1c02db21b5a889ef5a7b5b2571c900e2c"),
         (EZ / "rows_v10_final.jsonl", "106f355324fb867055e4f1ec25cc30ced8607b69a7ce0489b9d953e30e18608b"),
         (EZ / "rows_v10_final.manifest.json", "f8bd078b70cee18a9e54e02d1d3a5a7ba6b8aab3d1b0c48aa2e91d0f536be040"),
         (EZ / "fable_end_review" / "atlas_hold_ruling.v1.json",
          "24f6f8b0f4b2c4527db95505c9cf44d7a547c68b725675d32aa437d8bc130e5c")]
rows = []
for p, pin in files:
    b = p.read_bytes()
    if sha(b) != pin:
        raise SystemExit("REFUSED: %s is not at its pinned digest" % p.name)
    name = p.name if p.parent == D else str(p.relative_to(SP)).replace("\\", "/")
    rows.append("| `%s` | %s | `%s` |" % (name, format(len(b), ","), pin))

# the shape the section asserts, measured from the pinned bytes before a word of it is written
feed = [json.loads(l) for l in (D / "atlas_candidate_feed_rows.jsonl").read_text(encoding="utf-8").splitlines()]
corpus = [json.loads(l) for l in (EZ / "rows_v10_final.jsonl").read_text(encoding="utf-8").splitlines()]
held = sorted(r["chunk_decision_id"] for r in feed if r.get("candidate_hold_state") is not None)
ids = {r["chunk_decision_id"] for r in feed}
r082, r113 = corpus[81], corpus[112]
facts = {"feed_rows": len(feed), "held": held, "082_in_feed": "M8-Ezek-082" in ids,
         "grades": sorted({str(r["confidence"]) for r in feed}),
         "grade_counts": [sum(str(r["confidence"]) == g for r in feed) for g in ("low", "medium_low")],
         "082": (r082["decision_id"], r082["span"], r082["confidence"]),
         "113": (r113["decision_id"], r113["span"], r113["review_status"], r113.get("candidate_hold_state"))}
want = {"feed_rows": 101, "held": ["M8-Ezek-113"], "082_in_feed": False, "grades": ["low", "medium_low"], "grade_counts": [11, 90],
        "082": ("P07-003", "Ezek.29.17-Ezek.29.21", "high"),
        "113": ("P10-016", "Ezek.40.28-Ezek.40.37", "final_deferred_review", "deferred_human_or_external_ai")}
if facts != want:
    raise SystemExit("REFUSED: the measured shape is not the one this section states: %s" % json.dumps(facts))

sec = ("## AMENDED 2026-09-23 - v10 hold round, OW-30 (read this first; it supersedes the counts below)\n\n"
       "The final corpus is now `Ezek/rows_v10_final.jsonl`. The v9 final review wave held eight rows; Fable's one\n"
       "authorized ruling on them (`Ezek/fable_end_review/atlas_hold_ruling.v1.json`, owner ruling OW-30) resolved\n"
       "them under its standing three-rule precedent, recorded in the ledger:\n\n"
       "- **release** (P1 or P2): `M8-Ezek-035`, `-037`, `-038`, `-039`, `-049`, `-083`. Their feed rows now read\n"
       "  `accepted_candidate` / `candidate_review_complete` with no hold. No corpus row changed for them.\n"
       "- **drop_from_feed** (P2): `M8-Ezek-082` (writer row P07-003, Ezek.29.17-Ezek.29.21) is graded `high`, above\n"
       "  medium_low, so it leaves the feed. Its class question goes to Ezekiel's Fable end packet.\n"
       "- **keep_held** (P3): `M8-Ezek-113` (writer row P10-016, Ezek.40.28-Ezek.40.37). The corpus row is re-versioned\n"
       "  to `final_deferred_review` / `deferred_human_or_external_ai` / `specialist_or_external_review`\n"
       "  (manifest `Ezek/rows_v10_final.manifest.json`), and its feed row mirrors it as `held_lower_confidence`.\n\n"
       "**The selection rule changed with it.** The feed now follows the corpus: a row is in the feed only if it is\n"
       "graded `low` or `medium_low`, and it is held exactly when its corpus row carries `candidate_hold_state`.\n"
       "A referral by the final review wave (STOP or GRADE_QUESTION) no longer adds or holds a row; it only raises\n"
       "the row's score. The checker gained `feed_mirrors_the_corpus_hold` and the tamper `tamper_packet_state`, and\n"
       "passes 16 of 16. The feed has 101 rows (11 low, 90 medium_low), 1 held. Where the sections below say 102 rows,\n"
       "8 held rows or a referral-based selection, they describe the earlier builds and are kept as history.\n"
       "These are the current bytes:\n\n"
       "| File | Bytes | sha256 |\n|---|---|---|\n" + "\n".join(rows) + "\n\n"
       "The earlier files are kept beside these as `<name>.pre_<sha12>`. Re-pointing tool:\n"
       "`repair2/fixround_v10/repoint_generators_v10.py`; corpus builder `repair2/fixround_v10/build_rows_v10.py`.\n\n")
src = before.decode("utf-8")
anchor = "\n## AMENDED 2026-09-23 - v9 fix round"
if src.count(anchor) != 1 or "AMENDED 2026-09-23 - v10" in src:
    raise SystemExit("REFUSED: anchor count %d or already amended" % src.count(anchor))
new = src.replace(anchor, "\n" + sec + anchor[1:])
keep = R.with_name(R.name + ".pre_" + sha(before)[:12])
if keep.exists() and keep.read_bytes() != before:
    raise SystemExit("REFUSED: %s exists with different bytes" % keep.name)
keep.write_bytes(before)
tmp = R.with_name(R.name + ".tmp_v10")
tmp.write_bytes(new.encode("utf-8"))
os.replace(tmp, R)
m = subprocess.run([sys.executable, "-B", str(EZ / "repair2" / "close_check_mirror.py"), "--dest", a.dest, "--check",
                    "atlas"], capture_output=True, text=True, encoding="utf-8", env=env)
out = json.loads(m.stdout) if m.stdout.strip().startswith("{") else {}
if not out.get("bytes_equal_to_shipped") or out.get("exit"):
    R.write_bytes(before)
    raise SystemExit("ROLLED BACK: the atlas check record no longer reproduces: %s" % json.dumps(out)[:500])
print(json.dumps({"README": [sha(before), sha(R.read_bytes())], "kept": keep.name, "facts": facts,
                  "atlas_mirror": {"exit": out.get("exit"), "bytes_equal": out.get("bytes_equal_to_shipped")}}, indent=1))
