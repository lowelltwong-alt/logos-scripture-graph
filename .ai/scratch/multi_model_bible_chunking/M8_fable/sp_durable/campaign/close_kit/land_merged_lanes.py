#!/usr/bin/env python3
"""Land the two blind merged-close lanes into the durable shape the close gates read (TE-1, TE-7).

Both lanes must already be landed as ordinary review lanes by _land_lane.py. This reads their rows in the book's review
receipts, checks each of the six files against the digests the lane's result lists, and writes:
  {B}/merged_close/lane_{a,b}_e1/<the six files>
  {B}/merged_close/landing_manifest.v1.json
  {B}/{b}_merged_close_attempt_receipts.jsonl
Every target is write-once: an existing target with other bytes is refused, and nothing is written unless all items pass.
Book-agnostic: the book's names come from merged_params.v1.json.

usage (from SP): python -B campaign/close_kit/land_merged_lanes.py --params {B}/close/merged_params.v1.json [--dry-run]
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(__file__).resolve().parents[2]
FILES = ["postcheck.json", "final_check.json", "items_20_23.json", "named_questions.json", "lane_meta.json", "final_message.md"]
MODEL_BASIS = ("the lane's final_check.json and lane_meta.json both name this model; the runtime's completion "
               "notification carries no model field, so the tier is REPORTED, not MEASURED")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sha_lf_json(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def rows_of(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def one(rows, attempt, kind):
    hit = [r for r in rows if r.get("attempt_id") == attempt and r.get("record_kind") == kind]
    if len(hit) != 1:
        raise SystemExit("REFUSED: %s has %d %s rows, wanted 1" % (attempt, len(hit), kind))
    return hit[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    params = json.loads((SP / a.params).read_text(encoding="utf-8"))
    book, b, prefix = params["book"], params["book_lower"], params["attempt_prefix"]
    source_rel = "%s/review/%s_review_attempt_receipts.jsonl" % (book, b)
    source_bytes = (SP / source_rel).read_bytes()
    source = rows_of(SP / source_rel)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    plan, launches, completions, lanes = [], [], [], {}
    # Same suffix rule as make_merged_lanes.py: a reissue "a2" reads MERGED_A2_result.json and lands lane_a_e2.
    sfx = params.get("attempt_suffix", "a1")
    key_sfx, ex = ("" if sfx == "a1" else sfx[1:]), "e" + sfx[1:]
    for lane in ("A", "B"):
        low = lane.lower()
        attempt = "%s_merged_close_lane_%s_%s" % (prefix, low, sfx)
        launch = one(source, attempt, "launch")
        done = one(source, attempt, "completion")
        out = Path(launch["output_dir"])
        result = json.loads((SP / book / "review" / ("MERGED_%s%s_result.json" % (lane, key_sfx))).read_text(encoding="utf-8"))
        listed = {(d.get("name") or d.get("file")): d["sha256"] for d in result["deliverables"]}
        files = {}
        durable = "%s/merged_close/lane_%s_%s" % (book, low, ex)
        for name in FILES:
            data = (out / name).read_bytes()
            if listed.get(name) != digest(data):
                raise SystemExit("REFUSED: %s of lane %s does not match the digest the lane reported" % (name, lane))
            plan.append((SP / durable / name, data))
            files[name] = {"durable": "lane_%s_%s/%s" % (low, ex, name), "sha256": digest(data)}
        final = json.loads((out / "final_check.json").read_text(encoding="utf-8"))
        meta = json.loads((out / "lane_meta.json").read_text(encoding="utf-8"))
        model = launch["model"]
        if final.get("model") != model or meta.get("model") != model:
            raise SystemExit("REFUSED: lane %s names a model other than the one ordered" % lane)
        row = dict(launch)
        row["lane"] = "merged_close_lane_%s" % low
        launches.append(row)
        completions.append({
            "schema": "m8_attempt_receipt.v1", "record_kind": "completion", "attempt_id": attempt,
            "execution_id": launch["execution_id"], "book": book, "lane": row["lane"], "outcome": "COMPLETED",
            "outcome_in_review_receipts": done["outcome"], "model": model, "model_actual": model,
            "model_actual_tier": "REPORTED", "model_actual_basis": MODEL_BASIS,
            "model_actual_in_review_receipts": done["model_actual"],
            "tokens_reported": done["tokens_notification_unit"], "tool_uses_reported": done["tool_uses"],
            "tokens_tier": "REPORTED (the runtime's completion notification)",
            "deliverables": {k: v["sha256"] for k, v in files.items()}, "durable_dir": "sp_durable/" + durable,
            "weakness_disclosed": str(meta["e19_selfreport"]),
            "source_receipts": "sp_durable/" + source_rel, "source_receipts_sha256": digest(source_bytes),
            "recorded_at": stamp, "recorded_by": "land_merged_lanes.py"})
        lanes[lane] = {"attempt_id": attempt, "execution_id": launch["execution_id"], "files": files}
    manifest = {"schema": "%s_merged_close_landing.v1" % b, "written_at": stamp, "lanes": lanes}
    plan.append((SP / book / "merged_close" / "landing_manifest.v1.json",
                 (json.dumps(manifest, ensure_ascii=False, indent=1) + "\n").encode("utf-8")))
    plan.append((SP / book / ("%s_merged_close_attempt_receipts.jsonl" % b),
                 "".join(sha_lf_json(r) + "\n" for r in launches + completions).encode("utf-8")))
    for target, _data in plan:
        if target.exists():
            raise SystemExit("REFUSED: %s already exists" % target)
    if not a.dry_run:
        for target, data in plan:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    print(json.dumps({"dry_run": a.dry_run, "written": len(plan), "lanes": sorted(lanes)}))


if __name__ == "__main__":
    main()
