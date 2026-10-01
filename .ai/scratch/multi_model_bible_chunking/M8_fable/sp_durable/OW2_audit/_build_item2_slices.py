#!/usr/bin/env python3
"""OW-2 item 2 frame + slice builder — the 213-row Ps/Job/Prov/Eccl/Song
semantic-adjudication scope (owner directive OW-2 item 2, 2026-08-31).

Reads the TYPED row list retro_scans/2026-08-31_owner_warning/
ow2_item2_scope.v1.json (hash-pinned), resolves every scope id to a SHIPPED
row in book_chunks/<Book>/chunks.jsonl (by decision_id, else by the row's
unique writer_decision_id — the retro scan keyed its flag records by writer
id where one exists), asserts the owner denominators EXACTLY at the scope-id
level (Ps 67 / Job 50 / Prov 56 / Eccl 28 / Song 12 = 213; a mismatch is
SURFACED, never substituted), records every identity collision (two scope
ids naming one shipped row) as a mapping, joins each target with its OW-1
retro-scan trigger evidence (report.v1.json, hash-pinned) and its book-order
neighbor rows, pins the five shipped-corpus hashes, and emits the frame +
per-book slices of <= 8 rows (balanced; rows never cross books).
Run from SP/OW2_audit.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
SCOPE = M8 / "retro_scans" / "2026-08-31_owner_warning" / "ow2_item2_scope.v1.json"
REPORT = M8 / "retro_scans" / "2026-08-31_owner_warning" / "report.v1.json"
BOOKS = ["Ps", "Job", "Prov", "Eccl", "Song"]
OWNER_DENOMINATORS = {"Ps": 67, "Job": 50, "Prov": 56, "Eccl": 28, "Song": 12}
OWNER_TOTAL = 213
MAX_ROWS = 8
# pinned at the OW-2 budget checkpoint (receipts/OW2_audit_budget_checkpoint.json)
SCOPE_SHA_EXPECTED = "401ebcd9b809d12ddbeb6834c6108b2d427529c9c944fb7abe3de5b29dceced8"
REPORT_SHA_EXPECTED = "512283b5b57490754c20e9c679066c142515e1d2be69a969ce9202ddfec430c5"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


scope_sha, report_sha = sha(SCOPE), sha(REPORT)
assert scope_sha == SCOPE_SHA_EXPECTED, f"scope file hash moved: {scope_sha}"
assert report_sha == REPORT_SHA_EXPECTED, f"retro report hash moved: {report_sha}"
scope = json.load(open(SCOPE, encoding="utf-8"))
report = json.load(open(REPORT, encoding="utf-8"))
assert scope["unique_rows_total"] == OWNER_TOTAL

frame = {"schema": "m8_ow2_item2_frame.v1", "built": "2026-09-03",
         "authorization": "owner directive OW-2 item 2 (2026-08-31) under the OW-2D sequencing ruling (audit first)",
         "selection_rule": scope["selection_rule"],
         "owner_denominators": {**OWNER_DENOMINATORS, "total": OWNER_TOTAL},
         "scope_id_counts": {}, "denominator_match": {}, "identity_resolution": {},
         "collisions": {}, "unique_targets": {}, "pinned": {
             "retro_scans/2026-08-31_owner_warning/ow2_item2_scope.v1.json": scope_sha,
             "retro_scans/2026-08-31_owner_warning/report.v1.json": report_sha},
         "books": {}}
mismatch = False
slice_report = []

for book in BOOKS:
    corpus = M8 / "book_chunks" / book / "chunks.jsonl"
    frame["pinned"][f"book_chunks/{book}/chunks.jsonl"] = sha(corpus)
    rows = [json.loads(l) for l in corpus.read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    by_dec = {r["decision_id"]: r for r in rows}
    wids = {}
    for r in rows:
        w = r.get("writer_decision_id")
        if w:
            wids.setdefault(w, []).append(r["decision_id"])
    by_idx = {r["chunk_index_in_book"]: r for r in rows}
    assert len(by_dec) == len(rows), f"{book}: duplicate decision ids"

    scope_rows = scope["books"][book]["rows"]           # scope_id -> [tags]
    n_scope = len(scope_rows)
    frame["scope_id_counts"][book] = n_scope
    ok = (n_scope == OWNER_DENOMINATORS[book] == scope["books"][book]["unique_rows"])
    frame["denominator_match"][book] = ok
    mismatch = mismatch or not ok

    resolution = {}
    unresolved = []
    for sid in scope_rows:
        if sid in by_dec:
            resolution[sid] = sid
        elif sid in wids and len(wids[sid]) == 1:
            resolution[sid] = wids[sid][0]
        else:
            unresolved.append(sid)
    if unresolved:
        mismatch = True
    frame["identity_resolution"][book] = {
        "by_decision_id": sum(1 for s, d in resolution.items() if s == d),
        "by_writer_decision_id": {s: d for s, d in resolution.items() if s != d},
        "unresolved": unresolved}

    # targets + triggers (union over colliding scope ids), book order
    targets: dict[str, dict] = {}
    for sid, tags in scope_rows.items():
        d = resolution.get(sid)
        if not d:
            continue
        t = targets.setdefault(d, {"row_id": d, "scope_ids": [], "triggers": []})
        t["scope_ids"].append(sid)
        for tag in tags:
            if tag not in t["triggers"]:
                t["triggers"].append(tag)
    collisions = [{"target": d, "scope_ids": t["scope_ids"]} for d, t in targets.items() if len(t["scope_ids"]) > 1]
    frame["collisions"][book] = collisions
    frame["unique_targets"][book] = len(targets)

    # trigger evidence from the retro report (flag records keyed by writer id where present)
    lanes = report["per_book"][book]
    evidence: dict[str, list] = {}
    for lane in ("REG", "PUNCT", "EXCL"):
        for f in lanes[lane]["flags"]:
            key = f["decision_id"]
            d = resolution.get(key) or (key if key in by_dec else None)
            if d is None and key in wids and len(wids[key]) == 1:
                d = wids[key][0]
            if d in targets:
                ev = {"lane": lane, **{k: v for k, v in f.items() if k != "decision_id"}}
                evidence.setdefault(d, []).append(ev)
    for d, t in targets.items():
        ev = list(evidence.get(d, []))
        row = by_dec[d]
        for tag in t["triggers"]:
            if tag.startswith("lowband:"):
                ev.append({"lane": "LOWBAND", "field": "confidence", "value": row.get("confidence"),
                           "tag": tag})
        t["trigger_evidence"] = ev
        # every non-lowband trigger must carry at least one flag record
        for tag in t["triggers"]:
            lane = tag.split(":")[0].upper()
            if lane != "LOWBAND" and not any(e["lane"] == lane for e in ev):
                t.setdefault("evidence_gaps", []).append(tag)

    ordered = sorted(targets.values(), key=lambda t: by_dec[t["row_id"]]["chunk_index_in_book"])
    n = len(ordered)
    k = -(-n // MAX_ROWS)                     # ceil
    base, extra = divmod(n, k)
    sizes = [base + 1 if i < extra else base for i in range(k)]
    assert sum(sizes) == n and max(sizes) <= MAX_ROWS
    slices = []
    pos = 0
    for i, sz in enumerate(sizes, 1):
        chunk = ordered[pos:pos + sz]
        pos += sz
        name = f"i2_{book}_{i:02d}"
        items = []
        for t in chunk:
            row = by_dec[t["row_id"]]
            idx = row["chunk_index_in_book"]
            item = {"row_id": t["row_id"], "scope_ids": t["scope_ids"], "triggers": t["triggers"],
                    "trigger_evidence": t["trigger_evidence"], "shipped_row": row}
            if t.get("evidence_gaps"):
                item["evidence_gaps"] = t["evidence_gaps"]
            if idx - 1 in by_idx:
                item["prev_row"] = by_idx[idx - 1]
            if idx + 1 in by_idx:
                item["next_row"] = by_idx[idx + 1]
            if len(t["scope_ids"]) > 1:
                item["frame_mapping_note"] = ("identity collision: the scope lists this shipped row under "
                                              f"{len(t['scope_ids'])} ids ({', '.join(t['scope_ids'])}) — audited ONCE, "
                                              "all its triggers dispositioned")
            items.append(item)
        doc = {"schema": "m8_ow2_i2_slice.v1", "batch": name, "book": book,
               "attempt_id": f"ow2i2_{book}_{i:02d}_a1",
               "output_file": f"reviews/ow2i2_{book}_{i:02d}.json",
               "row_ids": [t["row_id"] for t in chunk],
               "trigger_tags_by_row": {t["row_id"]: t["triggers"] for t in chunk},
               "items": items}
        (HERE / "slices").mkdir(exist_ok=True)
        out = HERE / "slices" / f"slice_{name}.json"
        out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        slices.append({"slice": name, "rows": len(chunk), "bytes": out.stat().st_size,
                       "sha256": sha(out)})
        slice_report.append({"book": book, **slices[-1]})
    frame["books"][book] = {"targets_in_book_order": [t["row_id"] for t in ordered],
                            "trigger_tag_counts": {},
                            "slices": slices}
    for t in ordered:
        for tag in t["triggers"]:
            frame["books"][book]["trigger_tag_counts"][tag] = frame["books"][book]["trigger_tag_counts"].get(tag, 0) + 1

frame["unique_targets"]["total"] = sum(frame["unique_targets"][b] for b in BOOKS)
frame["scope_id_counts"]["total"] = sum(frame["scope_id_counts"][b] for b in BOOKS)
frame["denominator_match"]["total"] = frame["scope_id_counts"]["total"] == OWNER_TOTAL
mismatch = mismatch or not frame["denominator_match"]["total"]
frame["status"] = "MISMATCH_SURFACED_DO_NOT_LAUNCH" if mismatch else "READY"
(HERE / "reviews").mkdir(exist_ok=True)
(HERE / "frame_item2.v1.json").write_text(json.dumps(frame, ensure_ascii=False, indent=1),
                                          encoding="utf-8", newline="\n")
print(json.dumps({"status": frame["status"],
                  "scope_id_counts": frame["scope_id_counts"],
                  "denominator_match": frame["denominator_match"],
                  "unique_targets": frame["unique_targets"],
                  "collisions": {b: [c["target"] for c in frame["collisions"][b]] for b in BOOKS},
                  "unresolved": {b: frame["identity_resolution"][b]["unresolved"] for b in BOOKS},
                  "writer_id_resolutions": {b: len(frame["identity_resolution"][b]["by_writer_decision_id"]) for b in BOOKS},
                  "slices": len(slice_report),
                  "slice_sizes": {b: [s["rows"] for s in frame["books"][b]["slices"]] for b in BOOKS},
                  "evidence_gaps": sum(1 for b in BOOKS for s in frame["books"][b]["slices"]
                                       for it in json.load(open(HERE / "slices" / f"slice_{s['slice']}.json", encoding="utf-8"))["items"]
                                       if it.get("evidence_gaps"))},
                 ensure_ascii=False, indent=1))
raise SystemExit(1 if mismatch else 0)
