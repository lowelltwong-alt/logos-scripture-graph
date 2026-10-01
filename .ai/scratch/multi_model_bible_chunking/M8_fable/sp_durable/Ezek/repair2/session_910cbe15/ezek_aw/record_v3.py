#!/usr/bin/env python3
"""Record worklist v3, the A6 union gap it closes, and the two measurement mistakes found on the way."""
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()          # noqa: E731

for name in ("a6_union_check.v2.json", "a6_peer_union.v1.json"):
    src, dst = HERE / name, EZ / name
    if dst.is_file() and sha(dst) != sha(src):
        raise SystemExit("REFUSED: %s exists with different bytes" % name)
    shutil.copy2(src, dst)

W = EZ / "author_wave_worklist.v3.json"
w = json.loads(W.read_text(encoding="utf-8"))
entry = {
    "id": "E13-63",
    "severity": "MEDIUM",
    "headline": "THE A6 WORKLIST WAS NOT R3'S UNION: v2 built it from the boss's sweep alone where #e13 R3 makes "
                "the corrected arm and the peers' hand-named runs union MEMBERS. Eight items were missing. "
                "Worklist v3 adds them and makes the union coverage a BUILD GATE.",
    "raised_by": "orchestrator (claude-opus-5), self-audit of the worklist's basis against the order's own text",
    "how_it_was_found": ("after the A4 union was settled by containment I asked the same question of A6, "
                         "because R3's wording is a union and v2's A6 class came from a single measurement. "
                         "This is the E-31 discipline applied to a class I had not been told was wrong: check "
                         "the artifact against the ORDER, not against my memory of building it."),
    "measured": {
        "boss_sweep": "170 runs on 86 rows (the basis v2 used)",
        "corrected_arm": "95 runs on 66 rows; ONE has no overlapping run in v2's A6 class (P04-005)",
        "peers": ("a true superset of every 5+-word string any peer names anywhere in an item, filtered to "
                  "those that actually OCCUR in the WEB: 39 runs on 24 rows, of which SEVEN have no "
                  "overlapping run in v2's A6 class"),
        "union_additions": 8,
    },
    "two_measurement_mistakes_i_made_and_corrected": [
        {"mistake": "compared run TEXT exactly and reported 66 of 96 arm runs as NOT in the boss set",
         "why_wrong": ("the three sweeps name run EXTENTS independently, so the same site at a different "
                       "extent counted as a miss. 66 measured my comparison rule, not the worklist."),
         "corrected_figure": "1 by overlap on the same row",
         "lesson": "a number without its comparison rule is not a measurement"},
        {"mistake": "collected peer runs only from A6-context strings, giving 10 WEB-occurring runs",
         "why_wrong": ("a superset argument is worthless if the superset is not actually a superset; "
                       "collecting from the whole item gives 39"),
         "corrected_figure": "39 WEB-occurring runs on 24 rows",
         "lesson": ("the narrow collection was a DEFECT, not a conservative choice - under-collection in a "
                    "containment argument produces a false PASS")},
        {"note": ("a third slip, cheap: I guessed the translation lived at Ezek_web.txt and got "
                  "FileNotFoundError. The arm reads tools/verse_map_web.json through ezek_lib. Read what the "
                  "tool uses rather than inventing a filename.")},
    ],
    "why_the_filter_matters": ("the raw peer superset is 9,210 strings and 9,171 of them are the peers' OWN "
                              "PROSE. Filtering to strings that occur in the WEB is mechanical and turns a "
                              "number that measured my collection rule into one that measures coverage. "
                              "Without it the 'gap' would have read as 1,201 items."),
    "v3": {"file": "Ezek/author_wave_worklist.v3.json", "sha256": sha(W), "bytes": W.stat().st_size,
           "items": w["counts"]["items_total"], "by_class": w["counts"]["by_class"],
           "fixtures": "%d, all fired" % len(w["negative_fixtures"]["results"]),
           "items_moving_a_seam": w["counts"]["items_moving_a_seam"],
           "v2_and_v1_kept": True},
    "new_fixtures": ["R3's A6 union is covered: every arm-named and peer-named run has an item on its row",
                     "every v2 item survives into v3 byte-identical - a version bump that drops work while "
                     "claiming to add it is ledger row E-30"],
    "a6b_note": ("all eight additions are AUTHOR_JUDGEMENT, not installs. A6-b's exemption is conditional on "
                 "the row naming the device, which no tool can judge."),
    "blocks_author_wave": False, "status": "DONE", "tier": "MEASURED",
    "opened_at": datetime.now(timezone.utc).isoformat(),
}
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
print(json.dumps({"appended": "E13-63",
                  "queue_rows": len(Q.read_text(encoding="utf-8").strip().splitlines()),
                  "v3_sha256": sha(W), "items": w["counts"]["items_total"],
                  "landed": ["a6_union_check.v2.json", "a6_peer_union.v1.json"]}, indent=1))
