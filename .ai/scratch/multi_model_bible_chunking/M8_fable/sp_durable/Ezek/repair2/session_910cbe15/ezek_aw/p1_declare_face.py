#!/usr/bin/env python3
"""Precondition P1 of the #e13 ruling: verse_inventory.json declares its numbering face.

THE RULING (R2): "recomputed once by the fixed member after verse_inventory.json declares 'numbering_face':
'WEB'; every arithmetic consumer asserts the face; Daniel inherits it."

WHY. The file carried a face and declared none. MEASURED before this change: its only top-level keys were book,
total_verses and chapters, and its chapter 20 is 49 verses against MT 44, its chapter 21 is 32 against MT 37 -
the WEB face exactly. Four separate defects in one orchestrator-built consumer trace to that silence, and Daniel
carries TWO numbering zones instead of one.

GUARDED: the preimage digest is pinned, the expected-before state is asserted key by key, the per-chapter counts
are proved equal to the WEB side of the crosswalk before the label is written, no existing key is altered, and the
postimage is read back and re-validated.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
INV = EZ / "verse_inventory.json"
CHECK = EZ / "web_mt_verse_check.json"

PIN = "cf48cac0132d0d06a1b5f7c3cb1e7fb437aebfcaa33a6272a2c8894129067a99"

pre_bytes = INV.read_bytes()
pre_sha = hashlib.sha256(pre_bytes).hexdigest()
assert pre_sha == PIN, "verse_inventory.json moved: %s" % pre_sha

inv = json.loads(pre_bytes.decode("utf-8"))
assert sorted(inv.keys()) == ["book", "chapters", "total_verses"], \
    "unexpected keys before the change: %s" % sorted(inv.keys())
assert "numbering_face" not in inv, "a face is already declared"

# PROVE the face before labelling it, rather than asserting it from the defect report
chk = json.loads(CHECK.read_text(encoding="utf-8"))["per_chapter"]
web_side = {int(k): v["web"] for k, v in chk.items()}
mt_side = {int(k): v["mt"] for k, v in chk.items()}
have = {int(k): v for k, v in inv["chapters"].items()}
matches_web = all(have[c] == web_side[c] for c in have)
matches_mt = all(have[c] == mt_side[c] for c in have)
divergent = sorted(c for c in have if web_side[c] != mt_side[c])
assert matches_web and not matches_mt, \
    "the face is not provable: matches_web=%s matches_mt=%s" % (matches_web, matches_mt)
assert divergent, "no chapter diverges, so the label would be untestable"

inv["numbering_face"] = "WEB"
inv["numbering_face_basis"] = (
    "MEASURED, not asserted: every per-chapter count in this file equals the WEB side of "
    "web_mt_verse_check.json and the chapters where the two witnesses diverge (%s) carry the WEB figure, not the "
    "MT one. Declared under #e13 ruling R2 because this file previously carried a face and named none, which "
    "silently broke four separate adjacency computations in a consumer." % ", ".join(str(c) for c in divergent))
inv["numbering_face_obligation_on_consumers"] = (
    "Any tool that does verse arithmetic from these counts MUST assert the face it expects rather than infer it. "
    "Adjacency near a divergent chapter computed on the wrong face is simply the wrong verse, and the consumer "
    "cannot detect it.")
inv["declared_at"] = datetime.now(timezone.utc).isoformat()

tmp = INV.with_suffix(".json.tmp_p1")
tmp.write_text(json.dumps(inv, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
tmp.replace(INV)

post = json.loads(INV.read_text(encoding="utf-8"))
assert post["numbering_face"] == "WEB"
assert post["chapters"] == inv["chapters"], "the per-chapter counts changed, which they must not"
assert post["total_verses"] == 1273 and post["book"] == "Ezek"

print(json.dumps({
    "precondition": "P1",
    "file": INV.name,
    "preimage": pre_sha,
    "postimage_measured": hashlib.sha256(INV.read_bytes()).hexdigest(),
    "face_declared": post["numbering_face"],
    "face_proved_before_labelling": {"matches_web_side": matches_web, "matches_mt_side": matches_mt,
                                     "divergent_chapters": divergent},
    "keys_before": ["book", "chapters", "total_verses"],
    "keys_after": sorted(post.keys()),
    "per_chapter_counts_unchanged": post["chapters"] == inv["chapters"],
    "note": ("every brief that pinned the old digest is now stale for this file by design; the author-wave brief "
             "pins the new one, and no lane is currently running against the old pin"),
}, indent=1))
