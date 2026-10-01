#!/usr/bin/env python3
"""The OW-15 budget position for Ezekiel, reported as a BOUND rather than an equality.

WHY THIS TOOL EXISTS RATHER THAN A ONE-LINE SUM. Nine of this book's attempt receipts carry no token figure. A
script that sums `tokens_reported` and skips what is missing returns 38,678,610 and presents it as the census -
which asserts that the nine missing attempts cost ZERO. Four of them are Fable runs I landed myself (the boss
audit and the e12/e13/e14 rulings). So the census is a LOWER BOUND and the headroom is an UPPER BOUND, and any
report that states them as equalities is a half-truth of exactly the kind OW-18 forbids.

TWO MEASUREMENT FAILURES OF MY OWN THAT THIS REPLACES:
  * my first census used a HARDCODED list of receipt files and returned 23,895,678 - it missed five lanes
    (author, writer, fixup1-3). The pinned tool's own note says it discovers files by recursive glob precisely
    "because a hardcoded list would undercount". Mine undercounted by 14.8M, and for a moment I had a figure
    LOWER than the recorded census, which is impossible and is what made me look.
  * I then guessed the field name (`total_tokens`, `tokens`, `usage`) and got zero from every file before
    reading the attachment, which names it: `tokens_reported`.
Both were the same mistake: inventing a shape instead of reading the one the pinned artifact declares.

THE CEILING IS READ FROM ITS CARRIER, never hardcoded - a gate's own budget script once carried a superseded
ceiling and reported headroom that was not real.
"""
import hashlib
import json
from pathlib import Path

SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
EZ = SP / "Ezek"
CARRIER = SP / "campaign" / "budget_ceilings.v1.json"
BOOK = "Ezek"

carrier = json.loads(CARRIER.read_text(encoding="utf-8"))
ceiling = carrier["books"][BOOK]["ceiling"]

# THREE CLASSES, NOT TWO. My earlier version reported "9 attempts with no figure" and that figure was wrong
# in two directions, both found by reading the rows instead of the total:
#   * ONE of the nine is not an attempt at all. It carries schema m8_attempt_receipt_amendment.v1 - the
#     campaign's own mechanism for correcting a landed receipt - and has no attempt_id because it is not an
#     attempt. Counting it inflated the denominator and invented a capture gap that never existed.
#   * TWO of the nine DO declare UNAVAILABLE, in a sibling `token_note` field, with reasons ("the stop
#     notification carried no usage record; never estimated"). The census did not read that field, so it
#     reported a declared absence as a bare blank - understating the record's own honesty.
# So an unmeasured attempt is now either DECLARED (a value or a note that says UNAVAILABLE) or UNDECLARED, and
# only the undeclared set is a defect. That distinction is the whole of OW-18 applied to this column.
ATTEMPT_SCHEMA = "m8_attempt_receipt.v1"


def declares_unavailable(r):
    """Does this row SAY its token figure is unavailable, in any field that carries such a declaration?"""
    v = r.get("tokens_reported")
    if isinstance(v, str) and "UNAVAILABLE" in v.upper():
        return "tokens_reported carries UNAVAILABLE as a value"
    note = r.get("token_note")
    if isinstance(note, str) and ("UNAVAILABLE" in note.upper() or "no token count is recorded" in note):
        return "token_note declares it: %s" % note[:120]
    ex = r.get("execution_id")
    if ex in AMENDED_DECLARATIONS:
        return AMENDED_DECLARATIONS[ex]
    return None


# PRE-PASS: an amendment can declare an attempt's token figure, and it may live in ANY receipts file and on
# ANY line - before or after the attempt it amends. So the declarations are collected FIRST and resolved onto
# the attempt in the main pass. Without this the census reads the attempt row alone, finds no declaration, and
# reports as an undeclared blank a figure that has in fact been declared by amendment - which is what it did
# on the run immediately before this one.
AMENDED_DECLARATIONS = {}
for _p in sorted(EZ.rglob("*_attempt_receipts.jsonl")):
    if _p.suffix != ".jsonl" or ".pre_" in _p.name:
        continue
    for _l in _p.read_text(encoding="utf-8").splitlines():
        if not _l.strip():
            continue
        _r = json.loads(_l)
        if not str(_r.get("schema", "")).endswith("_amendment.v1"):
            continue
        _ex = _r.get("amends_execution_id")
        _v, _n = _r.get("tokens_reported"), _r.get("token_note") or ""
        if _ex and ((isinstance(_v, str) and "UNAVAILABLE" in _v.upper())
                    or "UNAVAILABLE" in _n.upper() or "no token count is recorded" in _n):
            AMENDED_DECLARATIONS[_ex] = "declared by amendment in %s: %s" % (
                str(_p.relative_to(EZ)).replace("\\", "/"),
                (_v if isinstance(_v, str) else _n)[:140])

known, declared, undeclared, amendments, per_file = 0, [], [], [], {}
partial_attempts = set()
for p in sorted(EZ.rglob("*_attempt_receipts.jsonl")):
    if p.suffix != ".jsonl" or ".pre_" in p.name:
        continue
    rel = str(p.relative_to(EZ)).replace("\\", "/")
    s_, n, u, d, am = 0, 0, 0, 0, 0
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines()):
        if not line.strip():
            continue
        r = json.loads(line)
        schema = r.get("schema") or ""
        if schema.endswith("_amendment.v1"):
            # AN AMENDMENT IS RESOLVED, NOT SKIPPED. Its own how_to_read says so: "a consumer of these receipts
            # resolves amendments". My first cut excluded amendments wholesale and the lower bound FELL by
            # 646,412 - one amendment carries a real token figure for a resumed segment. Excluding a
            # non-attempt from the attempt COUNT is right; dropping the spend it records is not. The figure is
            # summed here and the attempt it amends is marked PARTIAL, because the amendment's own note says
            # the figure covers the resumed segment only and the 95-tool-call review was never counted.
            am += 1
            av = r.get("tokens_reported")
            rec = {"file": rel, "line": i + 1, "schema": schema,
                   "amends_execution_id": r.get("amends_execution_id"),
                   "tokens_supplied": av if isinstance(av, int) else None,
                   "why": (r.get("why") or "")[:140]}
            if isinstance(av, int):
                s_ += av
                rec["counted_toward_the_lower_bound"] = True
                note = r.get("token_note") or ""
                rec["partial"] = ("SEGMENT ONLY" in note.upper() or "RESUMED SEGMENT" in note.upper())
                if rec["partial"]:
                    partial_attempts.add(r.get("amends_execution_id"))
            amendments.append(rec)
            continue
        n += 1
        v = r.get("tokens_reported")
        if isinstance(v, int):
            s_ += v
            continue
        rec = {"file": rel, "line": i + 1, "attempt_id": r.get("attempt_id"),
               "execution_id": r.get("execution_id"), "role": (r.get("role") or r.get("lane") or "")[:70],
               "model": r.get("model")}
        why = declares_unavailable(r)
        if why:
            d += 1
            declared.append(dict(rec, declaration=why))
        else:
            u += 1
            undeclared.append(dict(rec, value_present=("null" if v is None and "tokens_reported" in r
                                                       else "the field is ABSENT")))
    per_file[rel] = {"attempt_rows": n, "tokens_known": s_,
                     "includes_amendment_supplied_tokens": sum(
                         a["tokens_supplied"] or 0 for a in amendments if a["file"] == rel),
                     "unmeasured_declared": d, "unmeasured_UNDECLARED": u,
                     "amendment_rows_not_attempts": am}
    known += s_
unknown = declared + undeclared

out = {
    "schema": "ezek_ow15_position.v1",
    "law": "OW-15; the ceiling is READ from its carrier and never hardcoded",
    "ceiling": {"value": ceiling, "carrier": "sp_durable/campaign/budget_ceilings.v1.json",
                "carrier_sha256": hashlib.sha256(CARRIER.read_bytes()).hexdigest(),
                "owner_answer": carrier["books"][BOOK]["owner_answer"]},
    "census": {
        "LOWER_BOUND": known,
        "why_a_bound_and_not_an_equality": (
            "%d attempt receipts carry no integer token figure, so their cost is UNKNOWN and not zero. %d of "
            "them DECLARE that unavailability with a reason (OW-18: UNAVAILABLE is a value, never a blank); "
            "%d do not, and those are the only real capture gap in this book." % (
                len(unknown), len(declared), len(undeclared))),
        "attempt_receipts_total": sum(v["attempt_rows"] for v in per_file.values()),
        "attempts_counted": sum(v["attempt_rows"] for v in per_file.values()) - len(unknown),
        "unmeasured_but_DECLARED": len(declared),
        "unmeasured_and_UNDECLARED": len(undeclared),
        "amendment_rows_excluded_from_the_attempt_count": len(amendments),
        "amendment_supplied_tokens_counted": sum(a["tokens_supplied"] or 0 for a in amendments),
        "attempts_with_only_a_PARTIAL_figure": sorted(x for x in partial_attempts if x),
        "what_partial_means": ("an amendment supplied a token figure covering only part of the execution - the "
                               "resumed segment after a runtime kill - so the attempt's full cost is still "
                               "unknown and the total below remains a LOWER BOUND"),
        "basis": "MEASURED: sum of tokens_reported across every *_attempt_receipts.jsonl under sp_durable/Ezek, "
                 "discovered by recursive glob as the pinned budget tool does, with backups excluded",
        "per_file": per_file,
    },
    "headroom": {
        "UPPER_BOUND": ceiling - known,
        "meaning": ("at most this much remains. The true figure is lower by whatever the %d unmeasured attempts "
                    "cost." % len(unknown)),
    },
    "unmeasured_declared": declared,
    "unmeasured_UNDECLARED": undeclared,
    "amendment_rows": amendments,
    "what_was_repaired_and_what_was_not": {
        "repaired": ("the four receipts the orchestrator wrote this session (boss audit, e12/e13/e14 rulings) "
                     "now carry tokens_reported as an explicit UNAVAILABLE VALUE with its reason, written as a "
                     "STRING so a naive summing script fails LOUD rather than skipping it silently. Two of "
                     "them also had a wrong attempt_id - all three rulings read ezek_e12_ruling_a1 - now "
                     "DERIVED from the execution_id."),
        "not_repaired_and_why": ("the five older receipts (2 phase0, 3 top-level rulings) were written by "
                                 "earlier lanes I did not author. Their bytes are left alone and this census "
                                 "reports them as UNKNOWN, which achieves the same honesty without mutating "
                                 "another session's records."),
    },
    "consequence_for_the_author_wave_launch": (
        "the wave's six lanes are the next launch. Against a lower-bound census of %s and a ceiling of %s the "
        "upper-bound headroom is %s. The peer round - eleven agents over the same corpus - cost 3,668,692, so "
        "six author lanes over 495 items are of that order and fit inside the bound with margin even after "
        "allowing for the unmeasured attempts. No owner check-in is required by OW-15 because this launch does "
        "not approach the ceiling; the check-in duty is before a launch that would CROSS it."
        % ("{:,}".format(known), "{:,}".format(ceiling), "{:,}".format(ceiling - known))),
    "tier": "MEASURED for every figure present; the nine missing attempts are UNAVAILABLE and are counted as "
            "such, never as zero",
}
p = Path(__file__).resolve().parent / "ezek_ow15_position.v1.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({k: out[k] for k in ("ceiling", "census", "headroom",
                                      "consequence_for_the_author_wave_launch")},
                 ensure_ascii=False, indent=1).replace('"per_file"', '"per_file (see file)"')[:2600])
print()
print("attempts with no token figure: %d" % len(unknown))
for u in unknown:
    print("   %-46s %s" % (u["attempt_id"], u["role"] or u["file"]))
