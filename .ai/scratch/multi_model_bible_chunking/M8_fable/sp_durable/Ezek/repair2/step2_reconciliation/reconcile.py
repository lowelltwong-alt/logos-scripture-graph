#!/usr/bin/env python3
"""Reconcile two BLIND step-2 lanes at the level of CLAIMS, not strings. Read-only; writes one report.

WHY CLAIMS. Two authors given the same orders will never write the same sentence, and they split the orders into
clauses differently, so neither prose nor order quotes can be aligned by string. What CAN be aligned is what each
row ends up asserting: which verses it names, which devices, what grade it states, which false sentences it
removed, which Hebrew it quotes, and where it says a formula stands verse-final or mid-verse. Agreement on those is
corroboration; disagreement is the reconciliation docket.

THREE SEVERITIES
  CONFLICT   - one lane's row asserts something that cannot be true together with the row or the witness: a
               grade stated that the row does not carry; a Hebrew run absent from the witness; the two lanes
               placing the same formula verse-final and mid-verse. Nothing is applied from a CONFLICT row until
               it is resolved.
  DIVERGENT  - the lanes chose differently where both choices may be sound: a verse or device only one names; a
               live sentence only one deleted. Read and chosen, with the choice recorded.
  CONVERGENT - no divergence on any claim this reader extracts.

A SHARED CONSTRAINT IS NOT CORROBORATION. Both lanes hold one brief, and that brief barred refs edits while the
gate requires a refs entry for every argued verse (E13-98). Where both lanes write around the same wall the same
way, their agreement is the wall's, not two readings' - E-33. The report lists those separately and never counts
them as agreement.

THE DENOMINATOR IS PUBLISHED AND A ZERO FAILS (E-36). A selftest with planted divergences runs first; if the
reader cannot find a divergence it was handed, no verdict is computed.

usage: python reconcile.py [--selftest]
"""
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
LIVE = EZ / "repair" / "rows_v7_cwo24.jsonl"
OSHB = EZ / "Ezek_oshb.txt"
PROSE = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess")
WB = chr(92) + "b"
sha = lambda b: hashlib.sha256(b).hexdigest()                                  # noqa: E731


def _alt(*alts):
    return re.compile("|".join(WB + "(?:" + a + ")" + WB for a in alts), re.I)


VERSE = re.compile(r"(?:Ezek\.)?(\d{1,2})[:.](\d{1,3})(?:\s*[-\u2013]\s*(\d{1,3}))?")
DEVICES = _alt("samekh", "setumah", "pe", "petuchah", "messenger(?: formula)?", "utterance", "recognition",
               "dateline", "word-event", "transport", "son of man", "ve'attah", "ketiv", "qere", "K/Q",
               "paseq", "qinah", "colophon", "hand of YHWH", "oath", "refrain", "sof pasuq", "hayah")
GRADE = re.compile(
    "(?:row's|row s|this row's|its|the row's|holds? at|held at|stands at|rests at|grade of|grade is|carries|"
    "sits at|kept at|at)" + r"\s+" + "(high|medium[_ -]low|medium|low)" + WB +
    r"(?!\s+(?:place|places|priest|mountain|mountains|tower|towers|wall|walls|gate|gates|point|ground|hill))",
    re.I)
GRADE2 = re.compile(WB + "(high|medium[_ -]low|medium|low)" + r"\s+" + "(?:confidence|grade)" + WB, re.I)
NEGATION = re.compile("(?:not|never|rather than|below|above|short of|instead of|than|from|beyond|over)" +
                      r"\s*$", re.I)
POSITION = re.compile(WB + "(verse-final|verse final|mid-verse|mid verse)" + WB, re.I)
POSITION_ANY = re.compile(WB + "(?:not verse-final|non-final|verse-final|verse final|mid-verse|mid verse)" + WB, re.I)
AFTER_REF = re.compile(r"[^.;]{0,30}?" + WB + "(?:at|in|on)" + r"\s+(?:oshb:|web:)?(?:Ezek\.)?(\d{1,2})[:.](\d{1,3})")
HEBREW = re.compile("[\u0590-\u05ff][\u0590-\u05ff\\s\u05be]*[\u0590-\u05ff]")
SENT = re.compile(r"(?<=[.;])\s+")


def norm_grade(g):
    return g.lower().replace("-", "_").replace(" ", "_")


def bare(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if not unicodedata.combining(c) and c not in "\u05be\u05c0\u05c3\u05c6")


def pointed(s):
    return any(unicodedata.combining(c) for c in unicodedata.normalize("NFD", s))


WITNESS = [t.split("\t", 1)[1] for t in OSHB.read_text(encoding="utf-8").splitlines() if "\t" in t]
WITNESS_NFC = [unicodedata.normalize("NFC", t) for t in WITNESS]
WITNESS_BARE = [bare(t) for t in WITNESS]


def hebrew_in_witness(run):
    r = unicodedata.normalize("NFC", run.strip())
    if any(r in t for t in WITNESS_NFC):
        return "EXACT"
    if not pointed(r) and any(bare(r) in t for t in WITNESS_BARE):
        return "UNPOINTED_SKELETON"
    if any(bare(r) in t for t in WITNESS_BARE):
        return "HYBRID_OR_ALTERED - the consonants occur but the pointing does not match the witness"
    return "ABSENT"


def claims(text, grade):
    t = text or ""
    verses = set()
    for m in VERSE.finditer(t):
        c, v, v2 = int(m.group(1)), int(m.group(2)), m.group(3)
        if 1 <= c <= 48:
            verses.add("%d:%d%s" % (c, v, ("-" + v2) if v2 else ""))
    devices = {m.group(0).lower() for m in DEVICES.finditer(t)}
    stated, referenced = set(), set()
    for pat in (GRADE, GRADE2):
        for m in pat.finditer(t):
            g = norm_grade(m.group(1))
            (referenced if NEGATION.search(t[max(0, m.start() - 30):m.start()]) else stated).add(g)
    # ADJACENT BINDING ONLY (see patch_position_arm.py): a position word binds to a verse reference that ends within
    # 40 characters before it with no other reference between, or to "at/in/on <verse>" within 30 characters after.
    positions, unbound = set(), 0
    refs = [(m.start(), m.end(), "%s:%s" % (m.group(1), m.group(2))) for m in VERSE.finditer(t)]
    for p in POSITION_ANY.finditer(t):
        word = p.group(0).lower()
        kind = "mid-verse" if ("mid" in word or "non" in word or "not" in word) else "verse-final"
        bound = None
        after = AFTER_REF.match(t, p.end())
        if after:
            bound = "%s:%s" % (after.group(1), after.group(2))
        else:
            before = [r for r in refs if r[1] <= p.start() and p.start() - r[1] <= 40]
            if before:
                last = before[-1]
                if not any(last[1] <= r[0] < p.start() for r in refs if r is not last):
                    bound = last[2]
        if bound:
            positions.add((bound, kind))
        else:
            unbound += 1
    # A LABELLED QERE FORM IS NOT A VERSE-TEXT QUOTATION. The witness file carries the KETIV in the running text
    # (at 18:20 it is the bare unpointed רשע), and a row that says "the Qere <form>" is quoting the read form,
    # which collates against the K/Q note and not against the verse. The boss audit ruled labelled Qere forms
    # exempt from challenge. This reader cannot verify them against the note, so they are reported as
    # QERE_LABELLED - exempt and NOT verified here - rather than passed or failed. My first dry run reported
    # three such forms as CONFLICTs, and all three were in the live rows already.
    heb = {}
    for m in HEBREW.finditer(t):
        h = m.group(0).strip()
        if len(h) < 3:
            continue
        window = t[max(0, m.start() - 60):m.start()].lower()
        heb[h] = ("QERE_LABELLED - collates against the K/Q note, not the verse text; exempt by ruling; NOT "
                  "verified by this reader") if "qere" in window else hebrew_in_witness(h)
    sentences = {s.strip() for s in SENT.split(t) if len(s.strip()) > 12}
    return {"verses": verses, "devices": devices, "grades_stated": stated, "grades_referenced": referenced,
            "positions": positions, "positions_unbound": unbound, "hebrew": heb, "sentences": sentences,
            "grade": grade}


def row_claims(row):
    return claims("\n".join(row.get(f) or "" for f in PROSE), row.get("confidence"))


def compare(rid, live_row, a_row, b_row):
    L, A, B = row_claims(live_row), row_claims(a_row), row_claims(b_row)
    conflicts, divergent, inherited, comparisons = [], [], [], 0
    for lane, X in (("A", A), ("B", B)):
        comparisons += 1
        bad = {g for g in X["grades_stated"] if g != X["grade"]}
        if bad:
            conflicts.append({"lane": lane, "kind": "states a grade the row does not carry",
                              "row_grade": X["grade"], "stated": sorted(bad)})
        for h, verdict in X["hebrew"].items():
            comparisons += 1
            if verdict in ("EXACT", "UNPOINTED_SKELETON") or verdict.startswith("QERE_LABELLED"):
                continue
            item = {"lane": lane, "kind": "Hebrew not found in the witness as quoted", "run": h,
                    "verdict": verdict}
            # INHERITED IS NOT INTRODUCED. A run the live row already carries is a corpus finding for the
            # measured-false step, not a defect of the lane that left it in place.
            if h in L["hebrew"]:
                inherited.append(dict(item, kind="inherited from the live row: " + item["kind"]))
            else:
                conflicts.append(item)
    # POSITIONS ARE COMPARED AS SETS PER VERSE. A row can legitimately hold both kinds for one verse - an assertion
    # ("sits mid-verse") beside a rejected hypothetical ("treating it as a verse-final close was not taken"). My
    # earlier version collapsed the pairs into a dict keyed by verse, so whichever pair iterated last won, arbitrarily
    # per lane, and it reported a P03-017 conflict at 18:23 where both lanes carried the identical pair of claims.
    # A conflict now needs the two lanes' claim sets for a verse to be DISJOINT.
    from collections import defaultdict
    fa, fb = defaultdict(set), defaultdict(set)
    for v, k in A["positions"]:
        fa[v].add(k)
    for v, k in B["positions"]:
        fb[v].add(k)
    for v in sorted(set(fa) & set(fb)):
        comparisons += 1
        if not (fa[v] & fb[v]):
            conflicts.append({"kind": "the lanes place the same verse's formula differently",
                              "verse": v, "A": sorted(fa[v]), "B": sorted(fb[v])})
    for key in ("verses", "devices"):
        comparisons += 1
        oa, ob = sorted(A[key] - B[key]), sorted(B[key] - A[key])
        if oa or ob:
            divergent.append({"kind": key + " named by one lane only", "only_A": oa, "only_B": ob})
    del_a, del_b = L["sentences"] - A["sentences"], L["sentences"] - B["sentences"]
    comparisons += 1
    if del_a != del_b:
        divergent.append({"kind": "live sentences removed by one lane only",
                          "only_A_removed": sorted(del_a - del_b)[:12], "only_B_removed": sorted(del_b - del_a)[:12]})
    status = "CONFLICT" if conflicts else ("DIVERGENT" if divergent else "CONVERGENT")
    return {"row": rid, "status": status, "comparisons": comparisons, "conflicts": conflicts,
            "inherited_corpus_findings": inherited,
            "divergent": divergent,
            "agreement": {"verses_both": sorted(A["verses"] & B["verses"]),
                          "devices_both": sorted(A["devices"] & B["devices"]),
                          "removed_by_both": len(del_a & del_b)}}


def selftest():
    base = {"confidence": "medium", "boundary_rationale": "The onset at 33:21 is a dateline. The close at 33:22 "
            "is verse-final. A samekh stands on 33:20 and was said to decide it.", "device_notes": ""}
    same = dict(base)
    wrong_grade = dict(base, boundary_rationale=base["boundary_rationale"] + " The row holds at high.")
    negated = dict(base, boundary_rationale=base["boundary_rationale"] + " HIGH was never available; not high.")
    flipped = dict(base, boundary_rationale=base["boundary_rationale"].replace("verse-final", "mid-verse"))
    dropped = dict(base, boundary_rationale="The onset at 33:21 is a dateline. The close at 33:22 is verse-final.")
    high_places = dict(base, boundary_rationale=base["boundary_rationale"] + " Its high places are named.")
    heb_bad = dict(base, boundary_rationale=base["boundary_rationale"] + " It quotes \u05dc\u05b9\u05d0 "
                   "\u05d6\u05d5\u05d6\u05d6\u05d5\u05d6.")
    qere = dict(base, boundary_rationale=base["boundary_rationale"] + " The running text reads the ketiv in "
                "place of the Qere זָזָזז.")
    inherited_base = dict(heb_bad)
    p15_a = dict(base, boundary_rationale=base["boundary_rationale"] + " The fused row was not taken because the "
                 "utterance formula there is genuinely verse-final, unlike its mid-verse recurrences elsewhere in MT 18 "
                 "(18:3, 18:23, 18:30, 18:32).")
    p15_b = dict(base, boundary_rationale=base["boundary_rationale"] + " The fused row was not taken because the "
                 "utterance formula there is genuinely verse-final, unlike its four non-final recurrences elsewhere in "
                 "MT 18 (18:3, 18:23, 18:30, 18:32).")
    both_kinds = dict(base, boundary_rationale=base["boundary_rationale"] + " The formula inside 18:23 is mid-verse. "
                      "Treating 18:23's formula as a verse-final close was weighed and not taken.")
    cases = [("A vs A has no divergence", compare("t", base, same, same), "CONVERGENT"),
             ("REGRESSION P03-017: identical assertion plus rejected hypothetical in both lanes is NOT a conflict",
              compare("t", base, both_kinds, both_kinds), "CONVERGENT"),
             ("REGRESSION P03-015: 'mid-verse recurrences' vs 'non-final recurrences' over one verse list is NOT a "
              "conflict", compare("t", base, p15_a, p15_b), "CONVERGENT"),
             ("a labelled Qere form absent from the verse text is exempt",
              # both lanes carry the Qere sentence: a fixture that gave it to ONE lane also planted a device-word
              # divergence, so the reader correctly said DIVERGENT and the FIXTURE was wrong, not the reader
              compare("t", base, qere, qere), "CONVERGENT"),
             ("a bad run the LIVE row already carries is inherited, not the lane's conflict",
              compare("t", inherited_base, heb_bad, heb_bad), "CONVERGENT"),
             ("a stated wrong grade is a CONFLICT", compare("t", base, same, wrong_grade), "CONFLICT"),
             ("a negated grade is not a statement", compare("t", base, same, negated), "CONVERGENT"),
             ("a verse-final/mid-verse flip is a CONFLICT", compare("t", base, same, flipped), "CONFLICT"),
             ("a sentence removed by one lane is DIVERGENT", compare("t", base, same, dropped), "DIVERGENT"),
             ("'high places' is not a grade", compare("t", base, same, high_places), "CONVERGENT"),
             ("Hebrew absent from the witness is a CONFLICT", compare("t", base, same, heb_bad), "CONFLICT")]
    bad = [(n, r["status"], want) for n, r, want in cases if r["status"] != want]
    zero = [n for n, r, _ in cases if r["comparisons"] == 0]
    print(json.dumps({"selftest_cases": len(cases), "failed": bad, "zero_denominator": zero}, indent=1))
    return 1 if (bad or zero) else 0


if "--selftest" in sys.argv:
    raise SystemExit(selftest())
if selftest():
    raise SystemExit("REFUSED: the reconciler cannot find divergences it was handed; no verdict computed")

live_b = LIVE.read_bytes()
live = {r["decision_id"]: r for r in (json.loads(l) for l in live_b.decode("utf-8").splitlines() if l.strip())}
props = {x: json.loads((HERE / ("lane_%s" % x) / "proposal.json").read_text(encoding="utf-8")) for x in "ab"}


def apply(rid, lane):
    r = dict(live[rid])
    r.update(props[lane].get(rid, {}))
    return r


rows = sorted(set(props["a"]) | set(props["b"]))
results = [compare(rid, live[rid], apply(rid, "a"), apply(rid, "b")) for rid in rows]
disc = {x: json.loads((HERE / ("lane_%s" % x) / "discharge.json").read_text(encoding="utf-8")) for x in "ab"}
shared = []
for rid in rows:
    da = disc["a"]["rows"].get(rid, {}).get("disagreements", [])
    db = disc["b"]["rows"].get(rid, {}).get("disagreements", [])
    ga = [d for d in da if "gate" in str(d.get("with", "")).lower()]
    gb = [d for d in db if "gate" in str(d.get("with", "")).lower()]
    if ga and gb:
        shared.append({"row": rid, "A": [d.get("what") for d in ga], "B": [d.get("what") for d in gb],
                       "reading": "both lanes met the gate on this row: a SHARED CONSTRAINT, not corroboration"})
false_stops = {x: [{"row": rid, "order": s.get("order"), "why": s.get("why_its_ground_is_false")}
                   for rid, v in disc[x]["rows"].items() for s in v.get("stops", [])
                   if not str(s.get("why_its_ground_is_false", "")).upper().startswith("NOT FALSE")]
               for x in "ab"}
tally = Counter(r["status"] for r in results)
total_comparisons = sum(r["comparisons"] for r in results)
if total_comparisons == 0:
    raise SystemExit("REFUSED: zero comparisons (E-36)")
out = {
    "schema": "ezek_repair2_step2_reconciliation.v1",
    "inputs": {"live_rows_sha256": sha(live_b),
               "lane_a_proposal_sha256": sha((HERE / "lane_a" / "proposal.json").read_bytes()),
               "lane_b_proposal_sha256": sha((HERE / "lane_b" / "proposal.json").read_bytes())},
    "rows": len(rows), "comparisons": total_comparisons, "tally": dict(tally),
    "rows_proposed_by_only_one_lane": sorted(set(props["a"]) ^ set(props["b"])),
    "shared_constraints_not_corroboration": shared,
    "stops_claiming_a_false_ground": false_stops,
    "per_row": results,
    "tier": "MEASURED claim extraction over both candidates; what counts as a claim is this reader's, stated above",
}
(HERE / "reconciliation.v1.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=sorted),
                                             encoding="utf-8", newline="\n")
print(json.dumps({k: out[k] for k in ("rows", "comparisons", "tally", "rows_proposed_by_only_one_lane")},
                 indent=1))
for r in results:
    if r["status"] != "CONVERGENT":
        print("  %-9s %-10s conflicts=%d divergent=%d" % (r["row"], r["status"], len(r["conflicts"]),
                                                          len(r["divergent"])))
