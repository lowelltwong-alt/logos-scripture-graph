#!/usr/bin/env python3
"""Build Ezekiel's packet for the campaign-end Fable review (OW-28, 2026-09-23).

The owner deferred Fable to the end of the campaign. There it reviews each book's least-confident rows and the
orchestrator's notes on them, "because its job is to make the hardest decisions". This packet is that input for
Ezekiel. It holds every low and medium_low row of the final corpus with its sidecar. It also holds the docket entries
the v9 fix round did not cure, the v1 gates typed DEFERRED to this review, both v1 lanes' escalations verbatim, each
v9 delta lane's for_fable_end_review items, and the orchestrator's notes. No Fable judgement is recorded here. The
packet asserts nothing MET.

AMENDED 2026-09-23 (v10 hold round, OW-30): the corpus is rows_v10_final. Fable's one authorized ruling on the eight
atlas holds (atlas_hold_ruling.v1.json) is carried with its standing precedent. So are the row it kept held
(M8-Ezek-113, P10-016), the row it dropped from the feed (M8-Ezek-082, P07-003, graded high) with the class question
behind the drop, and both v10 delta lanes' verdicts, residuals and for_fable_end_review items. The v9 delta landing is
kept as delta_v9_landing; delta_landing is now the v10 one. The ruling is a record, not this review's judgement.

Every input is pinned by digest. The output is deterministic: no clock, and a fixed key order. --check rebuilds it in
memory and compares it byte for byte with the packet on disk. Nothing is written in that mode, and it prints MATCH or
MISMATCH last. _close_book.py runs this check. --write refuses before the real v9 and v10 delta landings exist. If a
different packet already exists, --write keeps it as <name>.pre_<sha12> (E-44). --delta-landing, --delta10-landing
and --out form a dry test hook: they build over fixture landings into a file outside M8.

usage: gen_fable_end_packet.py --check | --write | --delta-landing M --delta10-landing M --out F
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
EZ = HERE.parent
SP = EZ.parent
M8 = SP.parent
PACKET = HERE / "Ezek_fable_end_packet.v1.json"
DELTA_LANDING = EZ / "merged_close" / "delta_v9" / "landing_manifest.v1.json"
DELTA10_LANDING = EZ / "merged_close" / "delta_v10" / "landing_manifest.v1.json"
PINS = {"rows_v10_final.jsonl": "106f355324fb867055e4f1ec25cc30ced8607b69a7ce0489b9d953e30e18608b",
        "sidecar_src_ezek.jsonl": "3ad194a1077fb0a20c473666011148b1c02db21b5a889ef5a7b5b2571c900e2c",
        "repair2/fixround_v9/delta_docket_v9.v1.json": "9463a68183dd69e3b3f3caf6efa52655b86638be9030c0c3b2bff7e8ef015791",
        "repair2/fixround_v9/v1_unmet_gate_dispositions.v1.json":
            "3744b9cb21a7d2cfe94af72e607b82e0007437673243e91c9a4a9b5c6ec60725",
        "fable_end_review/atlas_hold_ruling.v1.json": "24f6f8b0f4b2c4527db95505c9cf44d7a547c68b725675d32aa437d8bc130e5c",
        "rows_v10_final.manifest.json": "f8bd078b70cee18a9e54e02d1d3a5a7ba6b8aab3d1b0c48aa2e91d0f536be040"}
V1_LANDING = EZ / "merged_close" / "landing_manifest.v1.json"
DELTA_LANES = (("A", "ezek_fixround_v9_delta_lane_a_a1"), ("B", "ezek_fixround_v9_delta_lane_b_a1"))
DELTA10_LANES = (("A", "ezek_fixround_v10_delta_lane_a_a1"), ("B", "ezek_fixround_v10_delta_lane_b_a1"))
HOLD_FIELDS = ("review_status", "candidate_hold_state", "candidate_hold_basis")
# The orchestrator's notes. Each names the record it rests on; the quoted values are EXTRACTED from the pinned inputs,
# and the "for Fable" sentence is the orchestrator's INFERRED framing of the decision, never a ruling.
NOTES = (
    ("A6", "The scholar-record generator (scholar_record/gen_scholar_record.py) still reads repair/rows_v7_cwo24 "
           "(MEASURED at the v10 packet build); it was re-pointed neither in v9 nor in v10. The atlas, sidecar and "
           "proposal generators were. For Fable: must the scholar record be rebuilt over rows_v10_final before "
           "publication, or is the v7 image acceptable as the recorded history?"),
    ("A9", "Fable's OW-30 ruling (atlas_hold_ruling, carried below) decided the 8 atlas holds: 6 released (P1/P2), "
           "M8-Ezek-082 dropped from the feed (P2, graded high), M8-Ezek-113 kept held (P3). v10 implements it: 113 is "
           "final_deferred_review in the corpus itself, and both v10 delta lanes judged every ruled id implemented as "
           "ruled. Under P3, 113 stays held until a corrected row is re-versioned and re-checked by two blind lanes. "
           "For Fable: nothing is re-opened on the 8 holds; the 113 correction is owed and is the orchestrator's work."),
    ("B7", "P03-001 keeps grade medium_low. v9 appended the ground the v1 lanes asked for (docket A0), but not whether "
           "the grade is right. For Fable: is medium_low the correct grade for P03-001?"),
    ("B19", "The utterance.mid_unit class question (final-wave trace F-494/F-495). The OW-30 ruling treated it as a class "
            "question, not a row defect: it released M8-Ezek-083 (medium_low) on it and dropped M8-Ezek-082 (graded "
            "high) from the feed on it. Both v10 lanes carried it unjudged, as the ruling directs. For Fable: rule the "
            "class, whether utterance.mid_unit is a signal that should lower a grade, which then settles 082 and 083."),
    ("B20", "MCP-Ezek-002 still reads as if 0.643 were four fifths. For Fable: rule the wording, and adjudicate every "
            "method-change proposal (the v1 lanes left the proposals' adjudication open)."),
    ("item_23", "Lane B's v1 escalation asked the owner to name item 23's adjudicator. Under OW-28 the campaign-end Fable "
                "review is the natural adjudicator, but naming it is the owner's act (OW-11)."),
    ("A3", "Both v9 delta lanes found, blind, the same low defect in P10-016 ref [12] ('the gate circuit is one list the "
           "plan never cuts inside'): the corpus cuts inside the gate sequence (lane A R1: at 40:27/28; lane B N1: at 40:16/17, "
           "40:19/20 and 40:27/28). Lane A judged A3 "
           "partly_cured, lane B cured with N1 new; both propose scoping the claim to the three inner gates 40:28-37. "
           "For Fable: carry it as a low, or order the one-sentence cure (a new corpus version) before publication. "
           "v10 (OW-30, P3): this row, M8-Ezek-113, is now held in the corpus; both v10 lanes report the defect still "
           "present (their for_fable_end_review items, carried verbatim under delta_v10). The cure is owed under P3."),
    ("disp:A:L60 final checker model == claude-fable-5-1",
     "Lane B's N4: part of this gate's v1 evidence (the OW-25 downgrade recorded in grader_models.v1.json) needs no "
     "Fable model and could be checked by a tool now; the disposition defers the whole gate. For Fable or the owner: "
     "split the tool-checkable part out, or keep the gate whole."),
)
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731


def read_pinned(rel):
    b = (EZ / rel).read_bytes()
    if sha(b) != PINS[rel]:
        raise SystemExit("REFUSED: %s is not at its pinned digest" % rel)
    return b


def jlb(b):
    return [json.loads(l) for l in b.decode("utf-8-sig").splitlines() if l.strip()]


def atlas_id(r):
    return "M8-Ezek-%03d" % r["chunk_index_in_book"]


def lanes(landing, lane_ids, tag):
    if not landing.is_file():
        raise SystemExit("REFUSED: the %s delta landing is absent; the packet is built only after it (%s)"
                         % (tag, landing.name))
    lb = landing.read_bytes()
    land = json.loads(lb.decode("utf-8-sig"))
    out = {}
    for L, att in lane_ids:
        ent = (land.get("lanes") or {}).get(L) or {}
        f = (ent.get("files") or {}).get("delta_check.json") or {}
        p = landing.parent / str(f.get("durable", ""))
        if ent.get("attempt_id") != att or not f.get("durable") or not p.is_file() or sha(p.read_bytes()) != f.get("sha256"):
            raise SystemExit("REFUSED: %s delta lane %s does not resolve from the landing manifest" % (tag, L))
        out[L] = (f["sha256"], json.loads(p.read_bytes().decode("utf-8-sig")))
    return lb, out


def build(delta_landing, delta10_landing):
    rows = jlb(read_pinned("rows_v10_final.jsonl"))
    side = {s["writer_decision_id"]: s for s in jlb(read_pinned("sidecar_src_ezek.jsonl"))}
    docket = json.loads(read_pinned("repair2/fixround_v9/delta_docket_v9.v1.json").decode("utf-8-sig"))["entries"]
    disp = json.loads(read_pinned("repair2/fixround_v9/v1_unmet_gate_dispositions.v1.json").decode("utf-8-sig"))["entries"]
    rb = read_pinned("fable_end_review/atlas_hold_ruling.v1.json")
    ruling = json.loads(rb.decode("utf-8-sig"))
    man10 = json.loads(read_pinned("rows_v10_final.manifest.json").decode("utf-8-sig"))
    low = [r for r in rows if r["confidence"] in ("low", "medium_low")]
    missing = [r["writer_decision_id"] for r in low if r["writer_decision_id"] not in side]
    if missing or len(side) != len(low):
        raise SystemExit("REFUSED: sidecars do not match the low/medium_low rows: %s" % missing[:4])
    by_atlas = {atlas_id(r): r for r in rows}
    rul = ruling.get("rulings") or {}
    kept = sorted(k for k, v in rul.items() if v.get("decision") == "keep_held")
    dropped = sorted(k for k, v in rul.items() if v.get("decision") == "drop_from_feed")
    if not kept or not dropped or any(k not in by_atlas for k in kept + dropped):
        raise SystemExit("REFUSED: the ruling's held or dropped ids do not resolve to corpus rows")
    if sorted(((man10.get("sources") or {}).get("ruling") or {}).get("keep_held") or []) != kept:
        raise SystemExit("REFUSED: the v10 manifest's keep_held differs from the ruling's")
    for k in kept:
        if by_atlas[k].get("review_status") == "candidate_review_complete" or by_atlas[k].get("candidate_hold_state") is None:
            raise SystemExit("REFUSED: the ruled hold %s is not held in the corpus" % k)

    lb, d9 = lanes(delta_landing, DELTA_LANES, "v9")
    lb10, d10 = lanes(delta10_landing, DELTA10_LANES, "v10")
    delta = {L: {"attempt_id": att, "delta_check_sha256": d9[L][0], "model": d9[L][1].get("model"),
                 "assembly_verdict": d9[L][1].get("assembly_verdict"), "verdict": d9[L][1].get("verdict"),
                 "for_fable_end_review": d9[L][1].get("for_fable_end_review") or [], "docket": d9[L][1].get("docket") or {},
                 "residual": d9[L][1].get("residual") or []} for L, att in DELTA_LANES}
    delta10 = {L: {"attempt_id": att, "delta_check_sha256": d10[L][0], "model": d10[L][1].get("model"),
                   "assembly_verdict": d10[L][1].get("assembly_verdict"), "verdict": d10[L][1].get("verdict"),
                   "ruling_implementation": d10[L][1].get("ruling_implementation") or {},
                   "residual": d10[L][1].get("residual") or [],
                   "for_fable_end_review": d10[L][1].get("for_fable_end_review") or []} for L, att in DELTA10_LANES}

    vl = json.loads(V1_LANDING.read_bytes().decode("utf-8-sig"))
    esc = {}
    for L in ("A", "B"):
        f = vl["lanes"][L]["files"]["final_check.json"]
        b = (V1_LANDING.parent / f["durable"]).read_bytes()
        if sha(b) != f["sha256"]:
            raise SystemExit("REFUSED: v1 lane %s final check does not match its landing manifest" % L)
        esc[L] = {"source": "merged_close/" + f["durable"], "sha256": f["sha256"],
                  "escalation": json.loads(b.decode("utf-8-sig")).get("escalation")}

    open_keys = [k for k, v in docket.items() if v.get("claim") not in ("cured_v9",)]
    notes = []
    for key, text in NOTES:
        if key in docket:
            on = docket[key]
        elif key == "item_23":
            on = esc["B"]["escalation"]
        elif key.startswith("disp:") and key[5:] in disp:
            on = disp[key[5:]]
        else:
            raise SystemExit("REFUSED: a note names %s, which no pinned record holds" % key)
        notes.append({"key": key, "note": text, "rests_on": on,
                      "tier": "INFERRED framing over EXTRACTED records; lane findings are REPORTED by the lanes"})
    pk = {
        "schema": "m8_fable_end_review_packet.v1", "book": "Ezek",
        "status": "DEFERRED (OW-28): awaiting the campaign-end Fable review. No Fable judgement is recorded here; "
                  "nothing in this packet is MET. The OW-30 atlas-hold ruling is carried as a record, not as this "
                  "review's judgement.",
        "reviewer": "Fable (claude-fable-5-1) at the campaign-end review, which makes the hardest decisions (OW-28)",
        "corpus": {"file": "sp_durable/Ezek/rows_v10_final.jsonl", "sha256": PINS["rows_v10_final.jsonl"]},
        "corpus_sha256": PINS["rows_v10_final.jsonl"],
        "row_ids": [r["decision_id"] for r in low],
        "rows_by_confidence": {c: sum(1 for r in low if r["confidence"] == c) for c in ("low", "medium_low")},
        "rows": [{"decision_id": r["decision_id"], "writer_decision_id": r["writer_decision_id"],
                  "confidence": r["confidence"], "row": r, "sidecar": side[r["writer_decision_id"]]} for r in low],
        "held_rows": {k: {"decision_id": by_atlas[k]["decision_id"], "confidence": by_atlas[k]["confidence"],
                          "hold": {f: by_atlas[k].get(f) for f in HOLD_FIELDS}, "ruling": rul[k]} for k in kept},
        "dropped_from_feed": {k: {"decision_id": by_atlas[k]["decision_id"], "confidence": by_atlas[k]["confidence"],
                                  "row": by_atlas[k], "ruling": rul[k], "class_question": "docket B19"} for k in dropped},
        "atlas_hold_ruling": {"file": "sp_durable/Ezek/fable_end_review/atlas_hold_ruling.v1.json", "sha256": sha(rb),
                              "rulings": rul, "precedent": ruling.get("precedent") or []},
        "docket_open": {k: {"v1": docket[k], "delta": {L: delta[L]["docket"].get(k) for L, _ in DELTA_LANES}}
                        for k in open_keys},
        "deferred_gates": {k: d for k, d in disp.items() if d.get("type") == "DEFERRED_OW28_FABLE_END_REVIEW"},
        "v1_escalations": esc,
        "delta_for_fable_end_review": {L: delta[L]["for_fable_end_review"] for L, _ in DELTA_LANES},
        "delta_residual": {L: delta[L]["residual"] for L, _ in DELTA_LANES},
        "delta_verdicts": {L: {k: delta[L][k] for k in ("attempt_id", "delta_check_sha256", "model", "assembly_verdict",
                                                           "verdict")} for L, _ in DELTA_LANES},
        "delta_v10": delta10,
        "delta_landing": "sp_durable/Ezek/merged_close/delta_v10/landing_manifest.v1.json",
        "delta_landing_sha256": sha(lb10),
        "delta_v9_landing": "sp_durable/Ezek/merged_close/delta_v9/landing_manifest.v1.json",
        "delta_v9_landing_sha256": sha(lb),
        "orchestrator_notes": notes,
        "inputs": {**{"sp_durable/Ezek/" + k: v for k, v in PINS.items()},
                   "sp_durable/Ezek/merged_close/landing_manifest.v1.json": sha(V1_LANDING.read_bytes())},
        "builder": "sp_durable/Ezek/fable_end_review/gen_fable_end_packet.py",
        "builder_sha256": sha(Path(__file__).read_bytes()),
    }
    return (json.dumps(pk, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--write", action="store_true")
    g.add_argument("--delta-landing")
    ap.add_argument("--delta10-landing")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.delta_landing:
        out = Path(a.out or "").resolve()
        if not a.out or not a.delta10_landing or out == M8 or M8 in out.parents:
            raise SystemExit("REFUSED: the test hook needs --delta10-landing and --out outside M8")
        b = build(Path(a.delta_landing).resolve(), Path(a.delta10_landing).resolve())
        out.write_bytes(b)
        print(json.dumps({"out": str(out), "sha256": sha(b), "bytes": len(b)}))
        return
    if a.delta10_landing or a.out:
        raise SystemExit("REFUSED: --delta10-landing and --out belong to the test hook")
    if a.check:
        b = build(DELTA_LANDING, DELTA10_LANDING)
        ok = PACKET.is_file() and PACKET.read_bytes() == b
        print(json.dumps({"packet": PACKET.name, "rebuilt_sha256": sha(b)}))
        print("MATCH" if ok else "MISMATCH")
        sys.exit(0 if ok else 1)
    gd = subprocess.run([sys.executable, "-B", str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek", "--target",
                         "Ezek/fable_end_review/" + PACKET.name], cwd=str(SP), capture_output=True, text=True,
                        encoding="utf-8", env=dict(os.environ, PYTHONUTF8="1"))
    if json.loads(gd.stdout)["verdict"] != "CLEAR":
        raise SystemExit("REFUSED by pin guard: " + gd.stdout[-300:])
    b = build(DELTA_LANDING, DELTA10_LANDING)
    kept = None
    if PACKET.is_file():
        old = PACKET.read_bytes()
        if old == b:
            print(json.dumps({"packet": PACKET.name, "sha256": sha(b), "unchanged": True}))
            return
        keep = PACKET.with_name(PACKET.name + ".pre_" + sha(old)[:12])
        if keep.exists() and keep.read_bytes() != old:
            raise SystemExit("REFUSED: %s exists with different bytes" % keep.name)
        keep.write_bytes(old)
        kept = keep.name
    tmp = PACKET.with_suffix(".tmp")
    tmp.write_bytes(b)
    os.replace(tmp, PACKET)
    if PACKET.read_bytes() != b:
        raise SystemExit("FAILED: post-write check")
    print(json.dumps({"packet": PACKET.name, "sha256": sha(b), "bytes": len(b), "kept": kept}))


if __name__ == "__main__":
    main()
