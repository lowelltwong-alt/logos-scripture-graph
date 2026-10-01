#!/usr/bin/env python3
"""Validate a Daniel book strategy (book_strategy_Dan.md plus strategy_plan_Dan.json) against the staged inventories.

Written by the orchestrator BEFORE the strategy lane launched (2026-09-24), so the author runs a check it cannot edit.
Ezekiel's validator hardcoded its parents and parts after the fact; this one reads them from the plan and re-sums them
from verse_inventory.json, independent of the author's arithmetic.

What it enforces:
  - FACE. verse_inventory.json must declare numbering_face "WEB" (its consumer obligation: assert, never infer), and
    the plan must declare the same face.
  - TILING. Parents and parts each tile the book exactly, contiguous from the first verse to the last, every ref real.
  - PARENT-SEAM STRADDLES. A part may contain a parent seam (Ezekiel's ruled invariant, 2026-09-08: ROWS never
    straddle a parent seam; a part is a work assignment). Every such seam must be DECLARED in the plan and DISCLOSED in
    the markdown as "internal parent seam A:B/C:D", C:D being the parent start. An undisclosed straddle is a failure.
  - SPANS IN THE TEXT. Every parent and part span appears in the markdown as "C:V-C:V". A span that starts or ends on a
    WEB/MT zone verse must carry its MT dual (an oshb:Dan. token) on the same line.
  - MT DUAL IN THE PLAN. A parent or part whose start or end is a zone verse carries "mt_dual":
    "oshb:Dan.C.V-oshb:Dan.C.V", equal to its span mapped through tools/verse_map_web.json (whose zone rows must agree
    with every zone_pairs anchor of web_mt_offset_map.json). Any mt_dual given elsewhere must also equal the mapping.
    Added 2026-09-28 after strategy check C1's D9 (pre-image .pre_7e2bbbd67d3d).
  - ZONE DUALS. A line with a web:Dan. token in a zone carries an oshb:Dan. token, and the reverse.
  - SECTIONS. The markdown has headings for sections 1 to 11 (section 11 is the OW-19 lens record).
  - LENS (OW-19). count >= 2 with a stated reason; a third lens names one of the decorrelating kinds the readiness
    file indicates.
  - COVERAGE. Every prepared scrutiny target (daniel_start_readiness.v2.json) and every for_fable_end_review item of
    dan_device_inventory.json is addressed exactly once, verbatim, with a section that exists.

It writes nothing. Usage:
  _validate_strategy_dan.py --md FILE --plan FILE
  _validate_strategy_dan.py --selftest
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SP = HERE.parent
INV = HERE / "verse_inventory.json"
DEV = HERE / "dan_device_inventory.json"
READY = SP / "campaign" / "daniel_start_readiness.v2.json"
VMAP = HERE / "tools" / "verse_map_web.json"
OFFSET = HERE / "web_mt_offset_map.json"
SECTIONS = range(1, 12)
REF = re.compile(r"^(\d+):(\d+)$")
WEB_ZONE = re.compile(r"web:Dan\.(?:4\.\d+|5\.31|6\.\d+)\b")
MT_ZONE = re.compile(r"oshb:Dan\.(?:3\.3[1-3]|4\.\d+|6\.\d+)\b")


def load_inputs():
    inv = json.loads(INV.read_text(encoding="utf-8"))
    dev = json.loads(DEV.read_text(encoding="utf-8"))
    ready = json.loads(READY.read_text(encoding="utf-8"))["already_settled_for_daniel"]
    vmap = json.loads(VMAP.read_text(encoding="utf-8"))
    web_to_mt = {k[len("Dan."):].replace(".", ":"): v["mt"][len("Dan."):].replace(".", ":") for k, v in vmap.items()}
    for pair in json.loads(OFFSET.read_text(encoding="utf-8"))["zone_pairs"]:
        w, m = pair["web"][len("web:Dan."):].replace(".", ":"), pair["mt"][len("oshb:Dan."):].replace(".", ":")
        if web_to_mt.get(w) != m:
            raise SystemExit("REFUSED: verse_map_web.json maps %s to %r; web_mt_offset_map.json anchors it at %s"
                             % (w, web_to_mt.get(w), m))
    return {"face": inv.get("numbering_face"), "declared_total": inv.get("total_verses"), "web_to_mt": web_to_mt,
            "chapters": {int(k): int(v) for k, v in inv["chapters"].items()},
            "targets": list(ready["prepared_scrutiny_targets"]),
            "kinds": list(ready["lens_requirement_under_OW19"]["decorrelating_kinds_indicated_by_its_severe_axes"]),
            "items": [x["item"] for x in dev["for_fable_end_review"]]}


def zone_verse(c, v):
    return c == 4 or c == 6 or (c, v) == (5, 31)


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
            hits = [ln for ln in lines if label in ln]
            if not hits:
                problems.append("%s %s: span %s not found in the markdown" % (kind, e.get("id"), label))
            elif (zone_verse(*a) or zone_verse(*b)) and not any("oshb:Dan." in ln for ln in hits):
                problems.append("%s %s: span %s touches a WEB/MT zone and no line carrying it has an oshb:Dan. dual"
                                % (kind, e.get("id"), label))
            if zone_verse(*a) or zone_verse(*b) or "mt_dual" in e:
                mt = [ctx["web_to_mt"].get("%d:%d" % cv) for cv in (a, b)]
                if None in mt:
                    problems.append("%s %s: span %s has no MT mapping for an endpoint" % (kind, e.get("id"), label))
                    continue
                want = "-".join("oshb:Dan." + x.replace(":", ".") for x in mt)
                if e.get("mt_dual") != want:
                    problems.append("%s %s: mt_dual %r, expected %r" % (kind, e.get("id"), e.get("mt_dual"), want))
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

    zone_bad = [i for i, ln in enumerate(lines, 1)
                if (WEB_ZONE.search(ln) and "oshb:Dan." not in ln) or (MT_ZONE.search(ln) and "web:Dan." not in ln)]
    if zone_bad:
        problems.append("zone refs without their dual on lines %s" % zone_bad[:10])

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
            "zone_lines_missing_dual": len(zone_bad),
            "lens": {"count": cnt, "third_lens_kind": lens.get("third_lens_kind")},
            "ezek_mentions": len(re.findall(r"\bEzek", md)),
            "problems": problems, "verdict": "GREEN" if not problems else "RED"}


def selftest():
    w2m = {"%d:%d" % (c, v): "%d:%d" % (c, v) for c in (3, 5) for v in (1, 2, 3)}
    w2m.update({"4:1": "3:31", "4:2": "3:32", "4:3": "3:33"})
    ctx = {"face": "WEB", "declared_total": 9, "chapters": {3: 3, 4: 3, 5: 3}, "web_to_mt": w2m,
           "targets": ["t1"], "kinds": ["CROSS_BOOK"], "items": ["i1"]}
    head = "\n".join("## §%d s" % n for n in SECTIONS)
    md = head + ("\n| P1 | 3:1-4:2 | web:Dan.4.2 = oshb:Dan.3.32 |\n| P2 | 4:3-5:3 | web:Dan.4.3 = oshb:Dan.3.33 |"
                 "\n| W1 | 3:1-5:3 | - |\ninternal parent seam 4:2/4:3\n")
    good = {"face": "WEB",
            "parents": [{"id": "P1", "start": "3:1", "end": "4:2", "verses": 5,
                         "mt_dual": "oshb:Dan.3.1-oshb:Dan.3.32"},
                        {"id": "P2", "start": "4:3", "end": "5:3", "verses": 4,
                         "mt_dual": "oshb:Dan.3.33-oshb:Dan.5.3"}],
            "parts": [{"id": "W1", "start": "3:1", "end": "5:3", "verses": 9, "internal_parent_seams": ["4:2/4:3"]}],
            "lens": {"count": 2, "reason": "x" * 40},
            "scrutiny_targets": [{"target": "t1", "section": "§7", "disposition": "d"}],
            "device_review_items": [{"item": "i1", "section": "§2", "disposition": "d"}]}

    def mut(f):
        p = json.loads(json.dumps(good))
        f(p)
        return p
    # each RED case names the problem it must raise, so a case cannot pass on some other failure
    cases = [
        ("green", md, good, ctx, None),
        ("gap", md, mut(lambda p: p["parents"][1].update(start="5:1", verses=3)), ctx, "expected 4:3, got 5:1"),
        ("overlap", md, mut(lambda p: p["parents"][0].update(end="4:3", verses=6)), ctx, "sum to 10 verses"),
        ("undeclared_straddle", md, mut(lambda p: p["parts"][0].update(internal_parent_seams=[])), ctx,
         "internal parent seams declared []"),
        ("undisclosed_straddle", md.replace("internal parent seam 4:2/4:3", ""), good, ctx, "does not disclose"),
        ("zone_span_no_dual", md.replace("| web:Dan.4.2 = oshb:Dan.3.32 |", "|"), good, ctx,
         "touches a WEB/MT zone"),
        ("zone_token_no_dual", md + "web:Dan.4.1 alone\n", good, ctx, "zone refs without their dual"),
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
        ("dual_missing", md, mut(lambda p: p["parents"][0].pop("mt_dual")), ctx,
         "mt_dual None, expected 'oshb:Dan.3.1-oshb:Dan.3.32'"),
        ("dual_wrong", md, mut(lambda p: p["parents"][1].update(mt_dual="oshb:Dan.4.3-oshb:Dan.5.3")), ctx,
         "expected 'oshb:Dan.3.33-oshb:Dan.5.3'"),
        ("dual_wrong_off_zone", md, mut(lambda p: p["parts"][0].update(mt_dual="oshb:Dan.3.1-oshb:Dan.5.4")), ctx,
         "expected 'oshb:Dan.3.1-oshb:Dan.5.3'"),
        ("dual_unmapped", md, good, dict(ctx, web_to_mt={k: v for k, v in w2m.items() if k != "4:3"}),
         "has no MT mapping"),
    ]
    res = {}
    for name, m, p, c, want in cases:
        r = check(m, p, c)
        res[name] = (r["verdict"] == "GREEN") if want is None else any(want in x for x in r["problems"])
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
