#!/usr/bin/env python3
"""Validate a 1 Corinthians book strategy (book_strategy_1Cor.md plus strategy_plan_1Cor.json) against the staged inventories.

Ported 2026-10-15 by the orchestrator from Dan/_validate_strategy_dan.py, BEFORE the strategy lane launched, so the
author runs a check it cannot edit. Like Daniel's, it reads parents and parts from the plan and re-sums them from
verse_inventory.json, independent of the author's arithmetic. What changed from Daniel's, and why:
  - 1 Corinthians has no numbering zone: web_greek_offset_map.json declares identity_throughout with an empty zone list
    (MEASURED at staging), so a WEB ref is the RP and SBLGNT ref. The validator asserts that and refuses otherwise
    (the map's own consumer obligation). Daniel's zone-dual arms (MT duals on spans, oshb:Dan. tokens, verse_map_web)
    therefore have no 1 Corinthians object. They are replaced by two identity arms: a parent or part may carry no
    dual field, and no line may write an MT-face (oshb:/mt:) token for this book.
  - A new arm checks that every web:/rp:/sbl: 1Cor token in the markdown names a real verse.
  - The readiness record is SP/1Cor/1cor_start_readiness.v1.json (Daniel's was campaign/daniel_start_readiness.v2.json).

What it enforces:
  - FACE. verse_inventory.json must declare numbering_face "WEB" (assert, never infer), and the plan the same face.
  - IDENTITY. web_greek_offset_map.json must declare identity_throughout true with no zones; a plan entry carrying
    mt_dual or greek_dual, or a line carrying an oshb:1Cor. or mt:1Cor. token, is a failure.
  - TILING. Parents and parts each tile the book exactly, contiguous from the first verse to the last, every ref real.
  - PARENT-SEAM STRADDLES. A part may contain a parent seam (Ezekiel's ruled invariant, 2026-09-08: ROWS never
    straddle a parent seam; a part is a work assignment). Every such seam must be DECLARED in the plan and DISCLOSED in
    the markdown as "internal parent seam A:B/C:D", C:D being the parent start. An undisclosed straddle is a failure.
  - SPANS IN THE TEXT. Every parent and part span appears in the markdown as "C:V-C:V".
  - TOKEN REFS. Every web:1Cor.C.V, rp:1Cor.C.V or sbl:1Cor.C.V token names a verse of the inventory.
  - SECTIONS. The markdown has headings for sections 1 to 11 (section 11 is the OW-19 lens record).
  - LENS (OW-19). count >= 2 with a stated reason; a third lens names one of the decorrelating kinds the readiness
    record lists.
  - COVERAGE. Every prepared scrutiny target (1cor_start_readiness.v1.json) and every for_fable_end_review item of
    1cor_device_inventory.json is addressed exactly once, verbatim, with a section that exists.

It writes nothing. Usage:
  _validate_strategy_1cor.py --md FILE --plan FILE
  _validate_strategy_1cor.py --selftest
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INV = HERE / "verse_inventory.json"
DEV = HERE / "1cor_device_inventory.json"
READY = HERE / "1cor_start_readiness.v1.json"
OFFSET = HERE / "web_greek_offset_map.json"
SECTIONS = range(1, 12)
REF = re.compile(r"^(\d+):(\d+)$")
TOKEN = re.compile(r"\b(?:web|rp|sbl):1Cor\.(\d+)\.(\d+)\b")
OFF_FACE = re.compile(r"\b(?:oshb|mt):1Cor\.")
DUAL_KEYS = ("mt_dual", "greek_dual")


def assert_identity(offset):
    if offset.get("identity_throughout") is not True or offset.get("zones"):
        raise SystemExit("REFUSED: web_greek_offset_map.json does not declare identity_throughout with no zones; this "
                         "validator has no zone arms and must not run")


def load_inputs():
    inv = json.loads(INV.read_text(encoding="utf-8"))
    dev = json.loads(DEV.read_text(encoding="utf-8"))
    ready = json.loads(READY.read_text(encoding="utf-8"))["already_settled_for_1cor"]
    assert_identity(json.loads(OFFSET.read_text(encoding="utf-8")))
    return {"face": inv.get("numbering_face"), "declared_total": inv.get("total_verses"),
            "chapters": {int(k): int(v) for k, v in inv["chapters"].items()},
            "targets": list(ready["prepared_scrutiny_targets"]),
            "kinds": list(ready["lens_requirement_under_OW19"]["decorrelating_kinds"]),
            "items": [x["item"] for x in dev["for_fable_end_review"]]}


def check(md, plan, ctx):
    ch = ctx["chapters"]
    problems = []
    if ctx["face"] != "WEB":
        problems.append("verse_inventory declares face %r; this validator expects 'WEB'" % ctx["face"])
    if plan.get("face") != ctx["face"]:
        problems.append("plan face %r differs from the inventory face %r" % (plan.get("face"), ctx["face"]))
    total = sum(ch.values())
    if ctx["declared_total"] != total:
        problems.append("inventory total_verses %r differs from its chapter sum %d" % (ctx["declared_total"], total))
    order = [(c, v) for c in sorted(ch) for v in range(1, ch[c] + 1)]
    index = {cv: i for i, cv in enumerate(order)}

    def parse(s):
        m = REF.match(str(s))
        cv = (int(m.group(1)), int(m.group(2))) if m else None
        return cv if cv in index else None

    lines = md.splitlines()
    tiled = {}
    for kind in ("parents", "parts"):
        spans, bad = [], []
        for e in plan.get(kind) or []:
            a, b = parse(e.get("start")), parse(e.get("end"))
            if a is None or b is None or index[a] > index[b]:
                bad.append("%s %s: span %r-%r is not a real forward span" % (kind, e.get("id"), e.get("start"),
                                                                            e.get("end")))
                continue
            spans.append((e, a, b))
        problems += bad
        if not spans:
            problems.append("%s: none given" % kind)
            continue
        if spans[0][1] != order[0] or spans[-1][2] != order[-1]:
            problems.append("%s: do not run from %d:%d to %d:%d" % ((kind,) + order[0] + order[-1]))
        for (e1, _, b1), (e2, a2, _) in zip(spans, spans[1:]):
            if index[a2] != index[b1] + 1:
                problems.append("%s: after %s (%d:%d) expected %d:%d, got %d:%d" % (
                    (kind, e1.get("id")) + b1 + (order[min(index[b1] + 1, len(order) - 1)]) + a2))
        n = sum(index[b] - index[a] + 1 for _, a, b in spans)
        if n != total:
            problems.append("%s: sum to %d verses, the inventory has %d" % (kind, n, total))
        for e, a, b in spans:
            label = "%d:%d-%d:%d" % (a + b)
            if e.get("verses") != index[b] - index[a] + 1:
                problems.append("%s %s: verses %r, measured %d" % (kind, e.get("id"), e.get("verses"),
                                                                    index[b] - index[a] + 1))
            if not any(label in ln for ln in lines):
                problems.append("%s %s: span %s not found in the markdown" % (kind, e.get("id"), label))
            for k in DUAL_KEYS:
                if k in e:
                    problems.append("%s %s: carries %s, but 1 Corinthians numbering is identity (no dual applies)"
                                    % (kind, e.get("id"), k))
        tiled[kind] = spans

    straddles = []
    if tiled.get("parents") and tiled.get("parts"):
        starts = [a for _, a, _ in tiled["parents"][1:]]
        for e, a, b in tiled["parts"]:
            found = ["%d:%d/%d:%d" % (order[index[p] - 1] + p) for p in starts if index[a] < index[p] <= index[b]]
            declared = list(e.get("internal_parent_seams") or [])
            if sorted(found) != sorted(declared):
                problems.append("part %s: internal parent seams declared %s, measured %s" % (e.get("id"), declared,
                                                                                            found))
            for s in found:
                ok = ("internal parent seam " + s) in md
                straddles.append({"part": e.get("id"), "seam": s, "disclosed": ok})
                if not ok:
                    problems.append("part %s: contains parent seam %s and the markdown does not disclose it as "
                                    "'internal parent seam %s'" % (e.get("id"), s, s))

    off_face = [i for i, ln in enumerate(lines, 1) if OFF_FACE.search(ln)]
    if off_face:
        problems.append("MT-face 1Cor tokens (oshb:/mt:) on lines %s; 1 Corinthians refs are WEB = RP = SBLGNT"
                        % off_face[:10])
    unreal = sorted({m.group(0) for m in TOKEN.finditer(md) if (int(m.group(1)), int(m.group(2))) not in index})
    if unreal:
        problems.append("token refs that name no verse: %s" % unreal[:10])

    heads = {int(m.group(1)) for m in re.finditer(r"^##+\s*§(\d+)\b", md, re.M)}
    problems += ["section §%d missing" % n for n in SECTIONS if n not in heads]

    lens = plan.get("lens") or {}
    cnt = lens.get("count")
    if not isinstance(cnt, int) or cnt < 2:
        problems.append("lens.count must be an integer >= 2 (OW-19 floor), got %r" % cnt)
    if len(str(lens.get("reason") or "").strip()) < 40:
        problems.append("lens.reason must state why this count (OW-19: an unrecorded reason is a close-gate problem)")
    if isinstance(cnt, int) and cnt >= 3 and lens.get("third_lens_kind") not in ctx["kinds"]:
        problems.append("a third lens counts only if decorrelated: third_lens_kind %r is not one of %s"
                        % (lens.get("third_lens_kind"), ctx["kinds"]))

    for key, want, field in (("scrutiny_targets", ctx["targets"], "target"),
                             ("device_review_items", ctx["items"], "item")):
        got = [str(x.get(field)) for x in plan.get(key) or []]
        missing = [w for w in want if got.count(w) != 1]
        extra = [g for g in got if g not in want]
        if missing:
            problems.append("%s: not addressed exactly once: %s" % (key, missing))
        if extra:
            problems.append("%s: entries that match no source %s verbatim: %s" % (key, field, extra))
        for x in plan.get(key) or []:
            m = re.fullmatch(r"§(\d+)", str(x.get("section")))
            if not m or int(m.group(1)) not in heads:
                problems.append("%s %r: section %r is not a heading of the markdown" % (key, x.get(field),
                                                                                     x.get("section")))
            if not str(x.get("disposition") or "").strip():
                problems.append("%s %r: no disposition" % (key, x.get(field)))

    return {"face": ctx["face"], "inventory_total": total,
            "parents": {"count": len(tiled.get("parents") or [])},
            "parts": {"count": len(tiled.get("parts") or [])},
            "parent_seam_straddles": straddles,
            "straddle_rule": "allowed when declared and disclosed; rows never straddle a parent seam",
            "off_face_token_lines": len(off_face), "unreal_token_refs": len(unreal),
            "lens": {"count": cnt, "third_lens_kind": lens.get("third_lens_kind")},
            "predecessor_mentions": len(re.findall(r"\b(?:Ezek|Dan\b|Daniel)", md)),
            "problems": problems, "verdict": "GREEN" if not problems else "RED"}


def selftest():
    ctx = {"face": "WEB", "declared_total": 9, "chapters": {3: 3, 4: 3, 5: 3},
           "targets": ["t1"], "kinds": ["CROSS_BOOK"], "items": ["i1"]}
    head = "\n".join("## §%d s" % n for n in SECTIONS)
    md = head + ("\n| P1 | 3:1-4:2 | web:1Cor.4.2 |\n| P2 | 4:3-5:3 | rp:1Cor.4.3 |"
                 "\n| W1 | 3:1-5:3 | - |\ninternal parent seam 4:2/4:3\n")
    good = {"face": "WEB",
            "parents": [{"id": "P1", "start": "3:1", "end": "4:2", "verses": 5},
                        {"id": "P2", "start": "4:3", "end": "5:3", "verses": 4}],
            "parts": [{"id": "W1", "start": "3:1", "end": "5:3", "verses": 9, "internal_parent_seams": ["4:2/4:3"]}],
            "lens": {"count": 2, "reason": "x" * 40},
            "scrutiny_targets": [{"target": "t1", "section": "§7", "disposition": "d"}],
            "device_review_items": [{"item": "i1", "section": "§2", "disposition": "d"}]}

    def mut(f):
        p = json.loads(json.dumps(good))
        f(p)
        return p

    def refuses(offset):
        try:
            assert_identity(offset)
        except SystemExit:
            return True
        return False
    # each RED case names the problem it must raise, so a case cannot pass on some other failure
    cases = [
        ("green", md, good, ctx, None),
        ("gap", md, mut(lambda p: p["parents"][1].update(start="5:1", verses=3)), ctx, "expected 4:3, got 5:1"),
        ("overlap", md, mut(lambda p: p["parents"][0].update(end="4:3", verses=6)), ctx, "sum to 10 verses"),
        ("undeclared_straddle", md, mut(lambda p: p["parts"][0].update(internal_parent_seams=[])), ctx,
         "internal parent seams declared []"),
        ("undisclosed_straddle", md.replace("internal parent seam 4:2/4:3", ""), good, ctx, "does not disclose"),
        ("span_absent", md.replace("| P2 | 4:3-5:3 |", "| P2 | - |"), good, ctx, "span 4:3-5:3 not found"),
        ("dual_on_identity", md, mut(lambda p: p["parents"][0].update(mt_dual="oshb:1Cor.3.1-oshb:1Cor.4.2")), ctx,
         "carries mt_dual"),
        ("off_face_token", md + "oshb:1Cor.4.1 alone\n", good, ctx, "MT-face 1Cor tokens"),
        ("unreal_token", md + "web:1Cor.5.4\n", good, ctx, "token refs that name no verse"),
        ("section_missing", md.replace("## §11 s", ""), good, ctx, "section §11 missing"),
        ("lens_one", md, mut(lambda p: p["lens"].update(count=1)), ctx, "lens.count must be"),
        ("lens_no_reason", md, mut(lambda p: p["lens"].update(reason="short")), ctx, "lens.reason must"),
        ("lens_third_correlated", md, mut(lambda p: p["lens"].update(count=3, third_lens_kind="SAME_FAMILY")), ctx,
         "a third lens counts only"),
        ("target_missing", md, mut(lambda p: p.update(scrutiny_targets=[])), ctx, "scrutiny_targets: not addressed"),
        ("item_paraphrased", md, mut(lambda p: p["device_review_items"][0].update(item="I1")), ctx,
         "device_review_items: not addressed"),
        ("section_not_a_heading", md, mut(lambda p: p["scrutiny_targets"][0].update(section="§12")), ctx,
         "is not a heading"),
        ("no_disposition", md, mut(lambda p: p["device_review_items"][0].update(disposition="")), ctx,
         "no disposition"),
        ("plan_face_wrong", md, mut(lambda p: p.update(face="MT")), ctx, "plan face"),
        ("inventory_face_wrong", md, good, dict(ctx, face="MT"), "this validator expects 'WEB'"),
        ("bad_ref", md, mut(lambda p: p["parts"][0].update(end="5:4")), ctx, "not a real forward span"),
        ("verses_wrong", md, mut(lambda p: p["parts"][0].update(verses=8)), ctx, "verses 8, measured 9"),
    ]
    res = {}
    for name, m, p, c, want in cases:
        r = check(m, p, c)
        res[name] = (r["verdict"] == "GREEN") if want is None else any(want in x for x in r["problems"])
    res["identity_ok_accepted"] = not refuses({"identity_throughout": True, "zones": []})
    res["identity_false_refused"] = refuses({"identity_throughout": False, "zones": []})
    res["zones_present_refused"] = refuses({"identity_throughout": True, "zones": [{"web": "x"}]})
    print(json.dumps({"selftest": res, "passed": sum(res.values()), "of": len(res)}, indent=1))
    return 0 if all(res.values()) else 1


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--md")
    ap.add_argument("--plan")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.md and a.plan):
        ap.error("--md and --plan are required")
    md = Path(a.md).read_text(encoding="utf-8")
    plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
    out = check(md, plan, load_inputs())
    out = dict({"md": a.md, "plan": a.plan}, **out)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if out["verdict"] == "GREEN" else 1


if __name__ == "__main__":
    sys.exit(main())
