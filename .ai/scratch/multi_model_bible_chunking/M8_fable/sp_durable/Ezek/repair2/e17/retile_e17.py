#!/usr/bin/env python3
"""#e17 RE-TILING: retire the 15 rows its seven re-tiling orders name and write the 8 new rows. A separately reviewed
mechanism, because the guarded harness refuses every identity and span field by design (it must stay that way).

WHAT A NEW ROW IS AT THIS STAGE. Its identity and decision fields are final; its prose is a SEED the final remediation
authors rewrite whole:
  - span, unit_type, parent_collection and confidence (the grade): from the ruling, verbatim;
  - decision_id / writer_decision_id: the next number in the part that NO rows file under Ezek/repair has ever used
    (retired ids included; the corpus convention of _apply_author_wave_ezek.py, widened from the chain to every file);
  - writer_part: the retired rows' part (all must agree); writer_attempt_id: the ruling's attempt, which decided the row;
  - boundary_rationale: the ruling's ground for the row (Fable-measured faces);
  - boundary_evidence_refs: the source rows' entries that still verify against the NEW span under the role-token member
    (an entry the member flags on the new span - a dissolved seam's onset/close token, a pair that is now an own seam - is
    left out and listed), then the ruling's required tokens that are written as refs entries (a conditional one goes to
    the authors, listed);
  - strongest_rejected_alternative, device_notes: the source rows' texts in the ruling's prose_from order, joined;
  - literature_type_guess: the first source row's; tag and signal lists: the ordered union; flags: the sources' (must agree).
Every surviving row keeps its bytes except chunk_index_in_book, renumbered 1..N in span order (the only field allowed to
differ, measured). The whole book must tile - every WEB verse exactly once (#e17 T-4) - and every new row must stay inside
its part's verses.

GUARDS: pinned pre-image and ruling digests; an exclusive lock; the full candidate built and checked in memory; written to a
temp file, re-read and compared, the pre-image backed up, then atomically replaced; a manifest with every input digest,
the id map, the chunk-index map, the dropped and conditional tokens. Refuses to overwrite a manifest with different bytes (E-41).

usage: python retile_e17.py --pre <rows sha> --ruling-sha <sha> [--apply] | --selftest
"""
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
R17 = EZ / "author" / "e17" / "ruling_e17.json"
MANIFEST = HERE / "retile_e17.manifest.json"
sys.path.insert(0, str(EZ / "tools"))
from ezek_lib import LAST_VERSE                                                 # noqa: E402
import check_role_tokens as RT                                                  # noqa: E402

FIELDS = ["decision_id", "book", "model_id", "chunk_index_in_book", "span", "boundary_rationale", "boundary_evidence_refs",
          "strongest_rejected_alternative", "literature_type_guess", "confidence", "strong_or_hebrew_tags_used",
          "wj_or_red_letter_considered", "frontier_flag_considered", "non_authorizing", "review_status", "parent_collection",
          "unit_type", "writer_part", "writer_decision_id", "writer_attempt_id", "observed_substrate_signals", "device_notes"]
SPAN = re.compile(r"^Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)$")
PID = re.compile(r"P\d\d-\d\d\d")
SCALE = {"low", "medium_low", "medium", "high"}
sha_b = lambda b: hashlib.sha256(b).hexdigest()                                 # noqa: E731
arg = lambda n: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else None      # noqa: E731


def verses(span):
    c1, v1, c2, v2 = map(int, SPAN.match(span).groups())
    out, c, v = [], c1, v1
    while (c, v) <= (c2, v2):
        out.append((c, v))
        c, v = (c, v + 1) if v < LAST_VERSE[c] else (c + 1, 1)
    return out


def dump(rows):
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows).encode("utf-8")


def ever_used_ids():
    """Every decision id any rows file under Ezek/repair has carried (numbers per part)."""
    ever = {}
    for p in sorted((EZ / "repair").glob("rows_*.jsonl*")):
        if p.suffix not in (".jsonl",) and ".pre_" not in p.name:
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                did = json.loads(line).get("decision_id", "")
                if PID.fullmatch(did):
                    ever.setdefault("p" + did[1:3], set()).add(int(did[4:]))
    return ever


def refs_valid_on(entry, span, rid):
    flags, _ = RT.check_rows([{"decision_id": rid, "span": span, "boundary_evidence_refs": [entry]}], "post")
    return not flags, [x["problem"] for x in flags]


def union(lists):
    out = []
    for lst in lists:
        for x in lst or []:
            if x not in out:
                out.append(x)
    return out


def build(rows, r17, ever):
    by = {r["decision_id"]: r for r in rows}
    retired, new_rows, dropped, conditional, id_map = [], [], [], [], {}
    for o in r17["retiling_orders"]:
        for rid in o["retire"]:
            if rid not in by:
                raise SystemExit("REFUSED: %s retires %s, which is not a live row" % (o["id"], rid))
            retired.append(rid)
        parts = {by[x]["writer_part"] for x in o["retire"]}
        if len(parts) != 1:
            raise SystemExit("REFUSED: %s retires rows from several parts %s" % (o["id"], parts))
        part = parts.pop()
        for n in o["new_rows"]:
            src = [by[x] for x in PID.findall(n["prose_from"])]
            if not src or any(s["decision_id"] not in o["retire"] for s in src):
                raise SystemExit("REFUSED: %s prose_from names a row this order does not retire: %r" % (n["provisional_label"], n["prose_from"]))
            if str(n["grade"]).lower() not in SCALE:
                raise SystemExit("REFUSED: %s grade %r is off the scale" % (n["provisional_label"], n["grade"]))
            for f in ("wj_or_red_letter_considered", "frontier_flag_considered", "non_authorizing"):
                if len({json.dumps(s[f]) for s in src}) != 1:
                    raise SystemExit("REFUSED: the source rows of %s disagree on %s" % (n["provisional_label"], f))
            k = max(ever[part]) + 1
            ever[part].add(k)
            did = "P%s-%03d" % (part[1:], k)
            id_map[n["provisional_label"]] = {"decision_id": did, "span": n["span"], "from": [s["decision_id"] for s in src]}
            refs = []
            for s in src:
                for e in s.get("boundary_evidence_refs") or []:
                    ok, why = refs_valid_on(e, n["span"], did)
                    if ok and e not in refs:
                        refs.append(e)
                    elif not ok:
                        dropped.append({"new_row": did, "from": s["decision_id"], "entry": e, "member_says": why})
            for t in n.get("tokens_required") or []:
                if re.match(r"^(oshb|web):Ezek\.", t):
                    if t not in refs:
                        refs.append(t)
                else:
                    conditional.append({"new_row": did, "token_order": t})
            row = {"decision_id": did, "book": "Ezek", "model_id": src[0]["model_id"], "chunk_index_in_book": 0,
                   "span": n["span"], "boundary_rationale": n["ground"], "boundary_evidence_refs": refs,
                   "strongest_rejected_alternative": " ".join(s["strongest_rejected_alternative"] for s in src if s.get("strongest_rejected_alternative")),
                   "literature_type_guess": src[0]["literature_type_guess"], "confidence": str(n["grade"]).lower(),
                   "strong_or_hebrew_tags_used": union(s.get("strong_or_hebrew_tags_used") for s in src),
                   "wj_or_red_letter_considered": src[0]["wj_or_red_letter_considered"],
                   "frontier_flag_considered": src[0]["frontier_flag_considered"], "non_authorizing": src[0]["non_authorizing"],
                   "review_status": "pending", "parent_collection": n.get("parent_collection") or src[0]["parent_collection"],
                   "unit_type": n.get("unit_type") or src[0]["unit_type"], "writer_part": part,
                   "writer_decision_id": "%s-%d" % (part, k), "writer_attempt_id": r17["attempt_id"],
                   "observed_substrate_signals": union(s.get("observed_substrate_signals") for s in src),
                   "device_notes": " ".join(s["device_notes"] for s in src if s.get("device_notes"))}
            new_rows.append({f: row[f] for f in FIELDS})
    if len(set(retired)) != len(retired):
        raise SystemExit("REFUSED: a row is retired twice")
    kept = [r for r in rows if r["decision_id"] not in set(retired)]
    result = sorted(kept + new_rows, key=lambda r: verses(r["span"])[0])
    book = [(c, v) for c in sorted(LAST_VERSE) for v in range(1, LAST_VERSE[c] + 1)]
    got = [v for r in result for v in verses(r["span"])]
    if got != book:
        raise SystemExit("REFUSED: the book does not tile after re-tiling (%d verses vs %d)" % (len(got), len(book)))
    part_verses = {}
    for r in rows:
        part_verses.setdefault(r["writer_part"], set()).update(verses(r["span"]))
    for r in new_rows:
        if not set(verses(r["span"])) <= part_verses[r["writer_part"]]:
            raise SystemExit("REFUSED: %s (%s) leaves its part's verses" % (r["decision_id"], r["span"]))
    ci_map = {}
    for i, r in enumerate(result, 1):
        if r["chunk_index_in_book"] != i and r not in new_rows:
            ci_map[r["decision_id"]] = [r["chunk_index_in_book"], i]
        r["chunk_index_in_book"] = i
    # measured: a surviving row differs from its live bytes in chunk_index_in_book only
    live = {r["decision_id"]: r for r in rows}
    for r in result:
        if r["decision_id"] in live:
            a = dict(live[r["decision_id"]], chunk_index_in_book=None)
            b = dict(r, chunk_index_in_book=None)
            if json.dumps(a, ensure_ascii=False) != json.dumps(b, ensure_ascii=False):
                raise SystemExit("REFUSED: surviving row %s changed outside chunk_index_in_book" % r["decision_id"])
    return result, {"retired": retired, "new_row_ids": id_map, "chunk_index_renumbered": ci_map,
                    "refs_left_out_as_invalid_on_the_new_span": dropped, "conditional_token_orders_for_authors": conditional,
                    "tiling": {"rows_before": len(rows), "rows_after": len(result), "verses": len(got), "exact": True}}


def selftest():
    rows = [json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]
    r17 = json.loads(R17.read_text(encoding="utf-8-sig"))
    cases = []
    res, man = build(rows, r17, ever_used_ids())
    cases.append(("138 rows after, 145 before", man["tiling"]["rows_before"] == 145 and man["tiling"]["rows_after"] == 138))
    ids = [r["decision_id"] for r in res]
    cases.append(("ids unique", len(ids) == len(set(ids))))
    ever = ever_used_ids()
    newids = [v["decision_id"] for v in man["new_row_ids"].values()]
    cases.append(("no new id was ever used before", all(int(i[4:]) not in ever["p" + i[1:3]] for i in newids)))
    bad = json.loads(json.dumps(r17))
    bad["retiling_orders"][0]["new_rows"][0]["span"] = "Ezek.18.21-Ezek.18.31"
    try:
        build(rows, bad, ever_used_ids())
        cases.append(("a one-verse gap is refused", False))
    except SystemExit as e:
        cases.append(("a one-verse gap is refused", "does not tile" in str(e)))
    bad = json.loads(json.dumps(r17))
    bad["retiling_orders"][1]["new_rows"][0]["prose_from"] = "P03-020 for everything"
    try:
        build(rows, bad, ever_used_ids())
        cases.append(("prose from a row the order does not retire is refused", False))
    except SystemExit as e:
        cases.append(("prose from a row the order does not retire is refused", "prose_from" in str(e)))
    ok, _ = refs_valid_on("oshb:Ezek.16.50 [WARRANT-close:near] ends on the utterance", "Ezek.16.44-Ezek.16.58", "PX")
    cases.append(("a dissolved seam's close token is invalid on the merged span", not ok))
    ok, _ = refs_valid_on("oshb:Ezek.16.51 [WARRANT-rival:near] 16.50/16.51 comparison turn after a samekh", "Ezek.16.44-Ezek.16.58", "PX")
    cases.append(("an interior rival stays valid", ok))
    cases.append(("every new row's grade is on the scale", all(r["confidence"] in SCALE for r in res)))
    failed = [n for n, ok in cases if not ok]
    print(json.dumps({"selftest_cases": len(cases), "failed": failed}, indent=1))
    return 1 if failed else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    pre, rsha = arg("--pre"), arg("--ruling-sha")
    live_b = ROWS.read_bytes()
    if sha_b(live_b) != pre:
        raise SystemExit("REFUSED: live rows %s are not the pinned pre-image %s" % (sha_b(live_b), pre))
    if sha_b(R17.read_bytes()) != rsha:
        raise SystemExit("REFUSED: the ruling is not the pinned bytes")
    if selftest():
        raise SystemExit("REFUSED: selftest failed (E-36)")
    rows = [json.loads(l) for l in live_b.decode("utf-8").splitlines() if l.strip()]
    result, man = build(rows, json.loads(R17.read_text(encoding="utf-8-sig")), ever_used_ids())
    out = dump(result)
    manifest = dict({"schema": "ezek_retile_e17.v1", "ruling": {"file": "Ezek/author/e17/ruling_e17.json", "sha256": rsha},
                     "preimage_sha256": pre, "postimage_sha256_computed": sha_b(out), "applied": "--apply" in sys.argv}, **man)
    print(json.dumps({k: manifest[k] for k in ("preimage_sha256", "postimage_sha256_computed", "new_row_ids", "tiling", "applied")}
                     | {"retired": len(man["retired"]), "chunk_index_renumbered": len(man["chunk_index_renumbered"]),
                        "refs_left_out": len(man["refs_left_out_as_invalid_on_the_new_span"]),
                        "conditional_token_orders": len(man["conditional_token_orders_for_authors"])}, ensure_ascii=False, indent=1))
    if "--apply" not in sys.argv:
        return 0
    lock = ROWS.with_suffix(ROWS.suffix + ".lock")
    fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        if sha_b(ROWS.read_bytes()) != pre:
            raise SystemExit("REFUSED: the rows moved while the candidate was built")
        tmp = ROWS.with_suffix(ROWS.suffix + ".tmpRT")
        tmp.write_bytes(out)
        if tmp.read_bytes() != out or [json.loads(l) for l in tmp.read_text(encoding="utf-8").splitlines() if l.strip()] != result:
            tmp.unlink()
            raise SystemExit("REFUSED: the temp file does not re-read to the candidate; nothing replaced")
        backup = ROWS.with_suffix(ROWS.suffix + ".pre_" + pre[:12])
        if not backup.exists():
            backup.write_bytes(live_b)
        os.replace(tmp, ROWS)
        manifest["postimage_sha256_measured_from_disk"] = sha_b(ROWS.read_bytes())
        manifest["preimage_backup"] = backup.name
        manifest["at"] = datetime.now(timezone.utc).isoformat()
        if manifest["postimage_sha256_measured_from_disk"] != manifest["postimage_sha256_computed"]:
            raise SystemExit("POSTCHECK FAILED: the disk bytes differ from the candidate")
        data = json.dumps(manifest, ensure_ascii=False, indent=1).encode("utf-8")
        if MANIFEST.exists() and MANIFEST.read_bytes() != data:
            raise SystemExit("REFUSED to overwrite %s (E-41); the rows ARE written - record from stdout" % MANIFEST.name)
        MANIFEST.write_bytes(data)
    finally:
        os.close(fd)
        lock.unlink()
    print(json.dumps({"postimage_sha256_measured_from_disk": manifest["postimage_sha256_measured_from_disk"], "manifest": MANIFEST.name}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
