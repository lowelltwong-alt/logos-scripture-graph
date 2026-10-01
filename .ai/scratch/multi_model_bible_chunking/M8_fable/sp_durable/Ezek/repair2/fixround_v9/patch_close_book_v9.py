#!/usr/bin/env python3
"""Amend Ezek/_close_book.py for the v9 fix round (OW-28). Exact-string edits, each anchor exactly once.

The tool is pinned at its expected-before digest and saved as .pre_<sha12>. It is compiled after the edit; a failure
restores it. The pin guard must be CLEAR. The tamper tests are run separately (_test_close_book_gates.py).
"""
import hashlib
import json
import os
import py_compile
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
EZ = HERE.parents[1]
SP = EZ.parent
T = EZ / "_close_book.py"
BEFORE = "dfeb34654dc4642c8d5945c55f29cf1d7804208958d463ad1eb6d94367dd81b5"
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731

DOC_OLD = "usage: _close_book.py [@usage.json] [--dry-report DIR] [--landing TEST_MANIFEST] [--close --acf {lam_pattern,item22}]\n" \
          "       --landing (dry only) points the lane gates at a landing set elsewhere, for adversarial tests\n"
DOC_NEW = '''AMENDED 2026-09-23 (v9 fix round, OW-28). Both v1 merged-close lanes returned not_fit over rows_v8_final, each on one
medium (A: P03-001 F-414; B: P06-015 SIGNAL_OUT_OF_SPAN). A bounded fix round built rows_v9_final: three rows changed and
the rest are byte-identical to v8, per rows_v9_final.manifest.json. Two blind delta lanes then re-checked THE DELTA over
v9. So:
- CORPUS is v9. The lineage gates prove that v9 differs from v8 only in the (row, field) pairs the manifest lists.
- The v1 lanes' final checks must be over the BASE (v8). Their verdicts stand as recorded (not_fit). Every v1 residual
  must be in the pinned docket, and every v1 high or medium must be judged cured by BOTH delta lanes.
- Items 20 and 21 come from the v1 lanes, because their records did not change. Items 22 and 23 come from the delta
  lanes.
- The Lam stray-gate filter is replaced by typed dispositions. Every unmet v1 close-gate entry must be keyed in the
  pinned dispositions file. Its type's text constraint is re-checked here, and both delta lanes must accept each one.
  DEFERRED_OW28_FABLE_END_REVIEW is DEFERRED, never MET: OW-28 defers claude-fable-5-1 to the campaign-end review.
- The book's Fable packet (its low and medium_low rows, their sidecars, the orchestrator's notes and the delta lanes'
  questions) must reproduce (--check MATCH) and carry THIS delta landing. The receipt names it as fable_end_review,
  DEFERRED (OW-28).
The earlier tool is kept as _close_book.py.pre_<sha12>.

usage: _close_book.py [@usage.json] [--dry-report DIR] [--landing M] [--delta-landing M] [--dispositions F]
                      [--close --acf {lam_pattern,item22}]
       --landing, --delta-landing and --dispositions are dry-only test hooks: they point the gates at copies
       elsewhere, for adversarial tests
'''
EDITS = [
    (DOC_OLD, DOC_NEW),
    ('CORPUS = "rows_v8_final.jsonl"\nCORPUS_PIN = "b2160ad6281184dc1dedf15a764bc058bc79a181928ed6323dbc332ec09cb0e7"\n',
     'CORPUS = "rows_v9_final.jsonl"\nCORPUS_PIN = "a80b6e6712aa43bf3d8652255b4655a934af08a9cd3e036f9b320a37bbd1098c"\n'
     'BASE = "rows_v8_final.jsonl"  # the corpus the v1 merged-close lanes reviewed in full\n'
     'BASE_PIN = "b2160ad6281184dc1dedf15a764bc058bc79a181928ed6323dbc332ec09cb0e7"\n'
     'DELTA_MANIFEST = EZ / "rows_v9_final.manifest.json"\n'
     'DELTA_MANIFEST_PIN = "91736024a4ac2ee44d37077a136355554f0bc27bdf012198f6c684adc3f5853c"\n'),
    ('              "final_message.md")\n',
     '              "final_message.md")\n'
     'FR = EZ / "repair2" / "fixround_v9"\n'
     'DOCKET, DOCKET_PIN = FR / "delta_docket_v9.v1.json", "9463a68183dd69e3b3f3caf6efa52655b86638be9030c0c3b2bff7e8ef015791"\n'
     'DISPOSITIONS = FR / "v1_unmet_gate_dispositions.v1.json"\n'
     'DISPOSITIONS_PIN = "3744b9cb21a7d2cfe94af72e607b82e0007437673243e91c9a4a9b5c6ec60725"\n'
     'DELTA_LANDING = EZ / "merged_close" / "delta_v9" / "landing_manifest.v1.json"\n'
     'DELTA_RECEIPTS = FR / "ezek_fixround_v9_attempt_receipts.jsonl"\n'
     'DELTA_LANES = (("A", "ezek_fixround_v9_delta_lane_a_a1"), ("B", "ezek_fixround_v9_delta_lane_b_a1"))\n'
     'DELTA_FILES = ("delta_check.json", "final_message.md")\n'
     'DERIVED = ("atlas_rows", "atlas_dimensions", "atlas_check", "sidecars", "proposals", "readme")\n'
     'FABLE_GEN = EZ / "fable_end_review" / "gen_fable_end_packet.py"\n'
     'FABLE_PACKET = EZ / "fable_end_review" / "Ezek_fable_end_packet.v1.json"\n'),
    ("def sidecar_gates(rows):\n", '''def lineage_gates():
    """v9 is v8 plus exactly the manifest's (row, field) changes: every other line is byte-identical (OW-28)."""
    gate("base corpus (v8) pinned", sha(EZ / BASE) == BASE_PIN, sha(EZ / BASE)[:16])
    gate("v8 -> v9 manifest pinned", sha(DELTA_MANIFEST) == DELTA_MANIFEST_PIN, sha(DELTA_MANIFEST)[:16])
    man = jload(DELTA_MANIFEST)
    gate("manifest built from the base, names this corpus", (man.get("built_from") or {}).get("sha256") == BASE_PIN
         and man.get("corpus_sha256") == CORPUS_PIN and man.get("corpus") == CORPUS)
    old = (EZ / BASE).read_bytes().decode("utf-8").splitlines()
    new = (EZ / CORPUS).read_bytes().decode("utf-8").splitlines()
    want, vals = collections.defaultdict(set), {}
    for c in man.get("changes") or []:
        want[c["row"]].add(c["field"])
        vals[(c["row"], c["field"])] = (c.get("before_sha256"), c.get("after_sha256"))
    same, bad = 0, []
    for i, (x, y) in enumerate(zip(old, new), 1):
        rx, ry = json.loads(x), json.loads(y)
        rid = rx.get("decision_id")
        if x == y:
            same += 1
            if rid in want:
                bad.append("%s unchanged but listed" % rid)
            continue
        diff = {k for k in set(rx) | set(ry) if rx.get(k) != ry.get(k)}
        if rid != ry.get("decision_id") or diff != want.get(rid):
            bad.append("%s line %d: %s" % (rid, i, sorted(diff)[:4]))
        for k in diff:
            h = (shab(json.dumps(rx.get(k), ensure_ascii=False).encode("utf-8")),
                 shab(json.dumps(ry.get(k), ensure_ascii=False).encode("utf-8")))
            if vals.get((rid, k)) != h:
                bad.append("%s.%s before/after sha" % (rid, k))
    gate("v9 differs from v8 only where the manifest says", len(old) == len(new) and not bad
         and same == len(old) - len(want) == man.get("unchanged_rows_byte_identical")
         and sorted(want) == sorted(man.get("rows_changed") or []), {"same": same, "bad": bad[:4]})
    return man


def sidecar_gates(rows):
'''),
    ('''        gate("lane %s: postcheck fit_to_assemble, no high/medium residual" % L,
             pc.get("verdict") == "fit_to_assemble" and not hi_med(pc.get("residual")) and not pc.get("blocking"),
''', '''        gate("lane %s: v1 postcheck verdict recorded (its high/medium go to the docket)" % L,
             pc.get("verdict") in ("fit_to_assemble", "not_fit"),
'''),
    ('''        gate("lane %s: final check fit_to_close over THIS corpus" % L, fc.get("verdict") == "fit_to_close"
             and fc.get("corpus_sha256") == CORPUS_PIN and not hi_med(fc.get("residual")),
''', '''        gate("lane %s: v1 final check over the base corpus (v8), verdict recorded" % L,
             fc.get("verdict") in ("fit_to_close", "not_fit") and fc.get("corpus_sha256") == BASE_PIN,
'''),
    ('''        stray = [str(g.get("gate") or g.get("name") or g)[:80] for g in unmet if "transcript" not in json.dumps(g).lower()]
        gate("lane %s: the only unmet Lam gate is the owed transcript audit" % L, cga and unmet and not stray,
             {"entries": len(cga), "unmet": len(unmet), "other_unmet": stray[:4]})
        gate("lane %s: items 20-23 fit_to_accept" % L,
             all((it.get("item_%d" % i) or {}).get("fit_to_accept") is True for i in range(20, 24)),
''', '''        gate("lane %s: close-gate assessment present (unmet entries go to the typed dispositions)" % L, bool(cga),
             {"entries": len(cga), "unmet": len(unmet)})
        gate("lane %s: items 20-21 fit_to_accept (22 and 23 are the delta lanes')" % L,
             all((it.get("item_%d" % i) or {}).get("fit_to_accept") is True for i in (20, 21)),
'''),
    ('"postcheck": pc, "final_check": fc, "items": it, "meta": meta}\n',
     '"postcheck": pc, "final_check": fc, "items": it, "meta": meta, "unmet": unmet}\n'),
    ("def target_gates():\n", '''def delta_lane_gates(model, fallback, landing):
    """The two blind v9 delta lanes (OW-28), read from their durable transcriptions. Paths resolve as in lane_gates."""
    out = {}
    land = jload(landing) if landing.is_file() else None
    if not gate("delta landing manifest present", land is not None, landing.name):
        return out, None
    recs = jl(DELTA_RECEIPTS)
    for L, att in DELTA_LANES:
        ent = (land.get("lanes") or {}).get(L) or {}
        files, ok = {}, True
        for fn in DELTA_FILES:
            f = (ent.get("files") or {}).get(fn) or {}
            p = landing.parent / str(f.get("durable", "")) if f.get("durable") else None
            good = p is not None and p.is_file() and sha(p) == f.get("sha256")
            ok &= good
            files[fn] = p if good else None
        gate("delta lane %s: durable outputs match the delta landing manifest" % L, ok and ent.get("attempt_id") == att,
             [k for k, v in files.items() if v is None])
        done = [r for r in recs if r.get("attempt_id") == att and r.get("record_kind") == "completion"]
        gate("delta lane %s: completion receipt COMPLETED on %s" % (L, model), len(done) == 1
             and done[0].get("outcome") == "COMPLETED" and done[0].get("model_actual") == model,
             [(d.get("outcome"), d.get("model_actual")) for d in done])
        if not ok:
            out[L] = None
            continue
        dc = jload(files["delta_check.json"])
        gate("delta lane %s: names the carrier's model" % L, dc.get("model") == model
             and (not fallback or "grader_fallback" in str(dc.get("grader_role", ""))),
             {"model": dc.get("model"), "role": dc.get("grader_role")})
        gate("delta lane %s: over v9, base v8, manifest pinned" % L, dc.get("corpus_sha256") == CORPUS_PIN
             and dc.get("base_corpus_sha256") == BASE_PIN and dc.get("manifest_sha256") == DELTA_MANIFEST_PIN,
             {k: str(dc.get(k))[:16] for k in ("corpus_sha256", "base_corpus_sha256", "manifest_sha256")})
        gate("delta lane %s: lineage confined to the manifest" % L,
             (dc.get("lineage") or {}).get("confined_to_manifest") is True)
        dr = dc.get("derived_records") or {}
        gate("delta lane %s: derived records fit" % L, all((dr.get(k) or {}).get("fit") is True for k in DERIVED),
             {k: (dr.get(k) or {}).get("fit") for k in DERIVED})
        items = dc.get("items") or {}
        gate("delta lane %s: items 22-23 fit_to_accept" % L,
             all((items.get("item_%d" % i) or {}).get("fit_to_accept") is True for i in (22, 23)),
             {i: (items.get("item_%d" % i) or {}).get("fit_to_accept") for i in (22, 23)})
        gate("delta lane %s: fit_to_assemble and fit_to_close, no high/medium residual" % L,
             dc.get("assembly_verdict") == "fit_to_assemble" and dc.get("verdict") == "fit_to_close"
             and not hi_med(dc.get("residual")),
             {"assembly": dc.get("assembly_verdict"), "verdict": dc.get("verdict"), "hi_med": len(hi_med(dc.get("residual"))),
              "bounded_fix": str(dc.get("bounded_fix"))[:160]})
        gate("delta lane %s: transcript audit stated OWED, e19 self-report, message digest" % L,
             "OWED" in str((dc.get("transcript_coverage") or {}).get("statement", "")).upper()
             and bool(dc.get("e19_selfreport")) and dc.get("output_sha256") == sha(files["final_message.md"]))
        out[L] = {"attempt_id": att, "check": dc,
                  "files": {k: ("sp_durable/Ezek/merged_close/" + str(v.relative_to(landing.parent.parent)).replace("\\\\", "/"),
                                sha(v)) for k, v in files.items()}}
    gate("two distinct blind delta lanes", all(out.get(L) for L, _ in DELTA_LANES))
    return out, land


def docket_gates(lanes, delta):
    """Every v1 residual is docketed, and every v1 high or medium is judged cured by BOTH delta lanes. The docket's
    claims are the orchestration's, not judgements (OW-19)."""
    gate("delta docket pinned", sha(DOCKET) == DOCKET_PIN, sha(DOCKET)[:16])
    doc = jload(DOCKET).get("entries") or {}
    v1 = {}
    for L, _ in LANES:
        for i, r in enumerate(((lanes.get(L) or {}).get("final_check") or {}).get("residual") or []):
            v1["%s%d" % (L, i)] = r
    gate("docket covers every v1 residual, severities verbatim", set(doc) == set(v1)
         and all(doc[k].get("v1_severity") == v1[k].get("severity") for k in v1),
         {"missing": sorted(set(v1) - set(doc))[:4], "extra": sorted(set(doc) - set(v1))[:4]})
    need = sorted(k for k, r in v1.items() if r.get("severity") in ("high", "medium"))
    ds = {L: ((delta.get(L) or {}).get("check") or {}).get("docket") or {} for L, _ in DELTA_LANES}
    judged = ("cured", "partly_cured", "not_cured", "carried")
    gate("docket: both delta lanes judged every key", all(set(ds[L]) >= set(doc) and all(
        (ds[L][k] or {}).get("judged") in judged for k in doc) for L in ds), {L: sorted(set(doc) - set(ds[L]))[:4] for L in ds})
    gate("docket: every v1 high/medium cured in both delta lanes", all(
        (ds[L].get(k) or {}).get("judged") == "cured" and (ds[L].get(k) or {}).get("severity_now") in ("none", "low")
        for L in ds for k in need), {L: {k: (ds[L].get(k) or {}).get("judged") for k in need} for L in ds})
    gate("docket: no key judged high/medium now", not [k for L in ds for k, v in ds[L].items()
                                                       if (v or {}).get("severity_now") in ("high", "medium")])
    pcs = [(L, r.get("row_id")) for L, _ in LANES for r in hi_med(((lanes.get(L) or {}).get("postcheck") or {}).get("residual"))]
    gate("v1 postcheck high/medium residuals are docketed high/medium", all(
        rid and any(k[0] == L and rid in str(doc.get(k, {}).get("row_or_artifact")) for k in need) for L, rid in pcs), pcs[:4])
    return doc, ds


def disposition_gates(lanes, delta, path):
    """The Lam stray-gate filter, replaced. Every unmet v1 close-gate entry carries a typed disposition whose text
    constraint is re-checked here, and both delta lanes accept every one. DEFERRED is never MET (OW-28)."""
    gate("gate dispositions pinned", sha(path) == DISPOSITIONS_PIN, sha(path)[:16])
    ent = jload(path).get("entries") or {}
    v1 = {"%s:%s" % (L, g.get("gate")): g for L, _ in LANES for g in ((lanes.get(L) or {}).get("unmet") or [])}
    gate("every unmet v1 gate has a disposition, evidence verbatim", set(ent) == set(v1)
         and all(ent[k].get("v1_evidence") == v1[k].get("evidence") for k in v1),
         {"missing": sorted(k[:50] for k in set(v1) - set(ent))[:3], "extra": sorted(k[:50] for k in set(ent) - set(v1))[:3]})
    bad = []
    for k, d in ent.items():
        g, e, t, st, cb = k.split(":", 1)[-1].lower(), str(d.get("v1_evidence") or "").lower(), d.get("type"), \\
            str(d.get("state")), d.get("cured_by")
        ok = {"DEFERRED_OW28_FABLE_END_REVIEW": "fable" in g and "stage-1" not in g and st.startswith("DEFERRED, NOT MET"),
              "OWED_OW26": any(w in g for w in ("transcript", "stage-1", "stage1", "reconcile"))
              and st.startswith("OWED, NOT MET"),
              "OWNER_ACT_OW11": "final-check packet" in g and "owner" in e,
              "CURED_BY_DELTA_VERDICT": (cb == "assembly_verdict" and "postcheck" in g)
              or (cb == "verdict" and ("verdict fit_to_close" in g or "no medium/high residual" in g))}.get(t, False)
        if not ok or (t != "CURED_BY_DELTA_VERDICT" and cb is not None) or " met" in st.lower().replace("not met", ""):
            bad.append(k[:70])
    gate("every disposition's type holds by its text (DEFERRED never MET)", not bad, bad[:4])
    want = {"assembly_verdict": "fit_to_assemble", "verdict": "fit_to_close"}
    cured = [k for k, d in ent.items() if d.get("type") == "CURED_BY_DELTA_VERDICT"]
    gate("verdict-cured gates: both delta lanes returned the named verdict", all(
        ((delta.get(L) or {}).get("check") or {}).get(ent[k].get("cured_by")) == want.get(ent[k].get("cured_by"))
        for L, _ in DELTA_LANES for k in cured), len(cured))
    acc = {L: ((delta.get(L) or {}).get("check") or {}).get("gate_dispositions") or {} for L, _ in DELTA_LANES}
    gate("dispositions: both delta lanes accept every one", all((acc[L].get(k) or {}).get("accept") is True
                                                                 for L in acc for k in ent),
         {L: sorted(k[:40] for k in ent if (acc[L].get(k) or {}).get("accept") is not True)[:3] for L in acc})
    return ent


def fable_gates(rows, delta_landing):
    """OW-28: Fable reviews every book's least-confident rows at the campaign's end. The packet must reproduce, be built
    over this corpus and THIS delta landing, and hold exactly the low and medium_low rows."""
    have = FABLE_PACKET.is_file() and FABLE_GEN.is_file()
    rc, tail = run([str(FABLE_GEN), "--check"]) if have else (1, ["absent"])
    gate("fable end packet reproduces (--check MATCH)", rc == 0 and tail[-1] == "MATCH", tail)
    pk = jload(FABLE_PACKET) if have else {}
    low = sorted(r["decision_id"] for r in rows if r["confidence"] in ("low", "medium_low"))
    gate("fable end packet over this corpus, rows == low/medium_low", pk.get("corpus_sha256") == CORPUS_PIN
         and sorted(pk.get("row_ids") or []) == low, {"rows": len(pk.get("row_ids") or []), "want": len(low)})
    gate("fable end packet carries THIS delta landing", bool(pk) and delta_landing.is_file()
         and pk.get("delta_landing_sha256") == sha(delta_landing))
    return pk


def target_gates():
'''),
    ('    ap.add_argument("--landing", help="dry-mode test hook: a landing manifest outside the real one")\n',
     '    ap.add_argument("--landing", help="dry-mode test hook: a landing manifest outside the real one")\n'
     '    ap.add_argument("--delta-landing", help="dry-mode test hook: a delta landing manifest outside the real one")\n'
     '    ap.add_argument("--dispositions", help="dry-mode test hook: a dispositions file outside the real one")\n'),
    ("    rows = corpus_gates()\n", "    rows = corpus_gates()\n    delta_man = lineage_gates()\n"),
    ('    lanes, land = lane_gates(model, carrier.get("fallback_in_force"), landing)\n',
     '    lanes, land = lane_gates(model, carrier.get("fallback_in_force"), landing)\n'
     '    if (a.delta_landing or a.dispositions) and a.close:\n'
     '        raise SystemExit("REFUSED: --delta-landing and --dispositions are dry-mode test hooks")\n'
     '    dlanding = Path(a.delta_landing).resolve() if a.delta_landing else DELTA_LANDING\n'
     '    delta, dland = delta_lane_gates(model, carrier.get("fallback_in_force"), dlanding)\n'
     '    doc, dsj = docket_gates(lanes, delta)\n'
     '    disp = disposition_gates(lanes, delta, Path(a.dispositions).resolve() if a.dispositions else DISPOSITIONS)\n'
     '    pk = fable_gates(rows, dlanding)\n'),
    ('"mesh_revision": "m8-mesh-r3 + OW-1..OW-26 as ruled; grader fallback OW-25; merged-verdict close OW-26",\n',
     '"mesh_revision": "m8-mesh-r3 + OW-1..OW-28 as ruled; grader fallback OW-25; merged-verdict close OW-26; "\n'
     '                         "v9 fix round with Fable deferred to the campaign-end review OW-28",\n'),
    ('"corpus_lineage_sha256": {"repair/rows_v7_cwo24.jsonl (pre-finalize)": sha(PRE_FINAL), CORPUS: sha(EZ / CORPUS)},\n',
     '"corpus_lineage_sha256": {"repair/rows_v7_cwo24.jsonl (pre-finalize)": sha(PRE_FINAL),\n'
     '                                  BASE + " (v1 merged-close base)": sha(EZ / BASE),\n'
     '                                  DELTA_MANIFEST.name + " (v8 -> v9)": sha(DELTA_MANIFEST), CORPUS: sha(EZ / CORPUS)},\n'),
    ('        "transcript_audit": "OWED, NOT MET",\n        "campaign_close_gate_evidence": {\n',
     '        "transcript_audit": "OWED, NOT MET",\n'
     '        "fable_end_review": {"status": "DEFERRED (OW-28)", "reviewer": "claude-fable-5-1, at the campaign\'s end",\n'
     '                             "packet": "sp_durable/Ezek/fable_end_review/" + FABLE_PACKET.name,\n'
     '                             "packet_sha256": sha(FABLE_PACKET) if FABLE_PACKET.is_file() else None,\n'
     '                             "rows": pk.get("row_ids"),\n'
     '                             "deferred_gate_keys": sorted(k for k, d in disp.items()\n'
     '                                                          if d.get("type") == "DEFERRED_OW28_FABLE_END_REVIEW")},\n'
     '        "v1_unmet_gate_dispositions": {"file": "sp_durable/Ezek/repair2/fixround_v9/" + DISPOSITIONS.name,\n'
     '                                       "sha256": sha(DISPOSITIONS),\n'
     '                                       "by_type": dict(collections.Counter(d.get("type") for d in disp.values()))},\n'
     '        "delta_docket": {"file": "sp_durable/Ezek/repair2/fixround_v9/" + DOCKET.name, "sha256": sha(DOCKET),\n'
     '                         "v1_high_medium_keys": sorted(k for k, v in doc.items() if v.get("v1_severity") in ("high", "medium")),\n'
     '                         "judged": {L: dict(collections.Counter((v or {}).get("judged") for v in dsj[L].values()))\n'
     '                                    for L in dsj}},\n'
     '        "campaign_close_gate_evidence": {\n'),
    ('''                "authority": "OW-6 as amended for Ezekiel by OW-25 (declared fallback grader) and OW-26 (merged-verdict "
                             "close; stage-1 transcript audit OWED, NOT MET)"},
        },
''', '''                "authority": "OW-6 as amended for Ezekiel by OW-25 (declared fallback grader) and OW-26 (merged-verdict "
                             "close; stage-1 transcript audit OWED, NOT MET). Both lanes reviewed the base, rows_v8_final, "
                             "and returned not_fit; their residuals are docketed and judged by item10_delta_v9 (OW-28)"},
            "item10_delta_v9": {
                "landing_manifest": "sp_durable/Ezek/merged_close/delta_v9/" + DELTA_LANDING.name,
                "landing_manifest_sha256": sha(dlanding) if dlanding.is_file() else None,
                "lanes": {L: {"attempt_id": v["attempt_id"], "files": v["files"], "model": v["check"].get("model"),
                              "assembly_verdict": v["check"].get("assembly_verdict"), "verdict": v["check"].get("verdict"),
                              "corpus_sha256_audited": v["check"].get("corpus_sha256"),
                              "items_22_23": {i: ((v["check"].get("items") or {}).get(i) or {}).get("fit_to_accept")
                                              for i in ("item_22", "item_23")}} for L, v in delta.items() if v},
                "authority": "OW-28 fix round: two blind delta lanes over rows_v9_final. The v1 lanes' full-book review "
                             "stands for every row the manifest proves byte-identical"},
        },
'''),
]
g = subprocess.run([sys.executable, "-B", str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek", "--target",
                    "Ezek/_close_book.py"], cwd=str(SP), capture_output=True, text=True, encoding="utf-8",
                   env=dict(os.environ, PYTHONUTF8="1"))
if json.loads(g.stdout)["verdict"] != "CLEAR":
    raise SystemExit("REFUSED by pin guard: " + g.stdout[-300:])
before = T.read_bytes()
if sha(before) != BEFORE:
    raise SystemExit("REFUSED: _close_book.py is at %s, not its expected-before digest" % sha(before)[:12])
src = before.decode("utf-8")
for old, new in EDITS:
    if src.count(old) != 1:
        raise SystemExit("REFUSED: an anchor occurs %d times: %r" % (src.count(old), old[:70]))
    src = src.replace(old, new)
keep = T.with_name(T.name + ".pre_" + BEFORE[:12])
if keep.exists() and keep.read_bytes() != before:
    raise SystemExit("REFUSED: %s exists with different bytes" % keep.name)
keep.write_bytes(before)
T.write_bytes(src.encode("utf-8"))
try:
    py_compile.compile(str(T), doraise=True, cfile=str(HERE / "_pc_close_book.pyc"))
except py_compile.PyCompileError as e:
    T.write_bytes(before)
    raise SystemExit("ROLLED BACK: does not compile: %s" % str(e)[:300])
finally:
    (HERE / "_pc_close_book.pyc").unlink(missing_ok=True)
print(json.dumps({"tool": [BEFORE, sha(T.read_bytes())], "kept": keep.name, "edits": len(EDITS)}))
