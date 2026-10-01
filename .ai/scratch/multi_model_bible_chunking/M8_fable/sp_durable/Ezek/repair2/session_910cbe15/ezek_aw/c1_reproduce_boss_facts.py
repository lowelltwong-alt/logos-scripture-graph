#!/usr/bin/env python3
"""#e14 Q3 CONDITION C1: reproduce each of the four boss-measured facts from the pinned input at its digest.

WHAT C1 IS FOR, in the ruling's own logic. The four peers' shared defect was not opening the pinned input that
carried the answer - the class the audit named UNAVAILABLE-where-MEASURABLE. The ruling's remedy is therefore NOT
a fourth human reading (OW-19: a correlated re-derivation adds nothing) but MACHINE REPRODUCTION from the input.
This script is that second lens, and it is decorrelated from the audit because it reads the bytes rather than the
audit's report of them.

THE RULE C1 SETS, applied literally: "a fact that does not reproduce is a STOP for that row, NOT a fallback to
the peer's version." So a failure here does not quietly restore what the peer wrote; it halts the row. Each
check therefore records what it FOUND, not merely whether it agreed - a boolean cannot be audited.
"""
import hashlib
import json
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
STRAT = EZ / "book_strategy_Ezek.md"
PMARKS = EZ / "pmarks_Ezek.json"
PINS = {"book_strategy_Ezek.md": "4c7847535a29c046c160635936275177b696836019f8e6f7a368bceda38330f3",
        "pmarks_Ezek.json": "25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315"}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


pin_report = {}
for p in (STRAT, PMARKS):
    got = sha(p)
    pin_report[p.name] = {"measured": got, "pinned_by_the_audit": PINS[p.name], "equal": got == PINS[p.name]}
if not all(v["equal"] for v in pin_report.values()):
    raise SystemExit("REFUSED: an input moved since the audit read it:\n"
                     + json.dumps(pin_report, indent=1))

strat_lines = STRAT.read_text(encoding="utf-8").splitlines()
pm = json.loads(PMARKS.read_text(encoding="utf-8"))
checks = []


def record(row, claim, expected, found, ok, how, note=None):
    checks.append({"row": row, "audit_claim": claim, "expected": expected, "found": found,
                   "reproduces": bool(ok), "how": how, **({"note": note} if note else {})})


# ---------------------------------------------------------------- P06-009: strategy line 351
# The audit cites "strategy line 351 states 'a qinah-labelled unit is never split'". Line numbers are fragile,
# so the reproduction searches the WHOLE document for the claim and reports where it actually sits: a fact
# located by content survives an edit above it, and a fact located by line number does not.
needle_words = ("qinah", "never split")
hits = [(i + 1, l.strip()) for i, l in enumerate(strat_lines)
        if "qinah" in l.lower() and "split" in l.lower()]
line351 = strat_lines[350].strip() if len(strat_lines) > 350 else "<the file has fewer than 351 lines>"
ok = bool(hits) and any("never" in h[1].lower() and "split" in h[1].lower() for h in hits)
record("P06-009", "strategy line 351: a qinah-labelled unit is never split",
       "a strategy statement that a qinah-labelled unit is not to be split",
       {"matching_lines": hits[:6], "what_line_351_actually_holds": line351}, ok,
       "searched every line of book_strategy_Ezek.md for a qinah + split statement rather than trusting the "
       "line number; the line number is reported beside the content so a drift is visible")

# ---------------------------------------------------------------- P08-002: the sof pasuq arithmetic anomaly
node = (pm.get("arithmetic_anomalies_resolved") or {}).get("sof_pasuq_1272_for_1273_verses") or {}
found_verse = node.get("verse")
record("P08-002", "pmarks arithmetic_anomalies_resolved.sof_pasuq_1272_for_1273_verses.verse = 'Ezek.33.20'",
       "Ezek.33.20", {"verse": found_verse, "sibling_keys": sorted(node.keys())},
       found_verse == "Ezek.33.20",
       "read the exact key path in pmarks_Ezek.json; the sibling keys are listed so a renamed field would be "
       "visible rather than reading as an absent fact")

# ---------------------------------------------------------------- P08-011: K-Q separator counts
kq = pm.get("kq") or {}
e1, e2 = kq.get("Ezek.36.13"), kq.get("Ezek.36.14")


def sep_counts(entry):
    """The separator count of a K-Q entry, per member.

    MEASURED SHAPE, which the first version of this script got wrong: a kq entry is a LIST of two K-Q pair
    strings, and a "separator count" is the number of '/' morpheme separators in each. Ezek.36.13 is
    ["...", "gwy/k gwyyk/k"] -> [0, 2]. The first version looked for an integer-pair FIELD, found no dict at
    all, and reported that the fact did not reproduce - which under C1 would have STOPPED two rows on my own
    reader's bug and told the controlling agent its audit was unsupported.

    THE ONLY REASON THAT DID NOT HAPPEN is that this script records what it FOUND and not merely whether it
    agreed: the output said "_entry_shape: list", which is a wrong reader, not a wrong fact. A check that
    reports a boolean cannot tell "the claim is false" from "I read the wrong place", and those two demand
    opposite responses.
    """
    if not isinstance(entry, list):
        return {"_unexpected_shape": type(entry).__name__}
    return {"separator_counts": [m.count("/") for m in entry if isinstance(m, str)],
            "members": len(entry)}


c13, c14 = sep_counts(e1), sep_counts(e2)
want13, want14 = [0, 2], [4, 0]
ok13 = c13.get("separator_counts") == want13
ok14 = c14.get("separator_counts") == want14
record("P08-011", "pmarks kq['Ezek.36.13'] separator counts [0, 2] and kq['Ezek.36.14'] [4, 0]",
       {"Ezek.36.13": want13, "Ezek.36.14": want14},
       {"Ezek.36.13": c13, "Ezek.36.14": c14}, ok13 and ok14,
       "counted the '/' morpheme separators in each member of each kq list entry - the measured shape of a kq "
       "entry is a two-member list of K-Q pair strings",
       note="the first version of this check assumed a dict of integer-pair fields and reported a false "
            "non-reproduction; corrected here")


# ---------------------------------------------------------------- P09-002: two read forms differing at one mark
# The audit's fact is precise and unusually checkable: the two read forms of Ezek.37.16 differ at U+0591
# (etnachta) against U+05BD (meteg). A codepoint claim is reproduced by DIFFING CODEPOINTS, not by eyeballing.
e = kq.get("Ezek.37.16")
# MEASURED SHAPE: a two-member list of K-Q pair strings, so the "two read forms" ARE the two members. The first
# version collected string FIELDS of a dict, found none, and reported a false non-reproduction.
forms = [(i, m) for i, m in enumerate(e)] if isinstance(e, list) else []
diff, pair_found = None, False
if len(forms) >= 2:
    a, b = forms[0][1], forms[1][1]
    only_a, only_b = set(a) - set(b), set(b) - set(a)
    names = lambda s: sorted("U+%04X (%s)" % (ord(c), unicodedata.name(c, "?")) for c in s)
    diff = {"member_0_codepoints_absent_from_member_1": names(only_a),
            "member_1_codepoints_absent_from_member_0": names(only_b),
            "identical_apart_from_those": (len(a) == len(b)
                                           and sum(1 for x, y in zip(a, b) if x != y) == len(only_a | only_b))}
    cps = {"U+%04X" % ord(c) for c in (only_a | only_b)}
    pair_found = cps == {"U+0591", "U+05BD"}
    diff["the_difference_is_exactly_U0591_vs_U05BD"] = pair_found
record("P09-002", "pmarks kq['Ezek.37.16'] two read forms differing at U+0591 vs U+05BD",
       "two read forms whose codepoint difference is exactly U+0591 (etnachta) against U+05BD (meteg)",
       {"members_found": len(forms), "codepoint_difference": diff},
       pair_found, "diffed the two members of the kq list at the CODEPOINT level; the differing codepoints "
                   "are named with their Unicode names so the claim is checkable and not merely asserted",
       note="the first version looked for string fields of a dict and reported a false non-reproduction; "
            "corrected here")

failed = [c["row"] for c in checks if not c["reproduces"]]
out = {
    "schema": "ezek_c1_boss_fact_reproduction.v1",
    "condition": ("#e14 Q3 C1: the orchestrator reproduces each of the four facts from the pinned input at its "
                  "recorded digest by a self-contained script, and records the reproduction in the worklist "
                  "item's source and tier. A fact that does not reproduce is a STOP for that row, never a "
                  "fallback to the peer's version."),
    "why_a_script_and_not_a_reading": ("OW-19. The four peers' defect was not opening the input that carried "
                                       "the answer; a fourth correlated reading is the least independent check "
                                       "available. Machine reproduction from the bytes is the decorrelated "
                                       "lens, and it is decorrelated from the AUDIT too, because it reads the "
                                       "input rather than the audit's report of it."),
    "input_digest_parity": pin_report,
    "reproductions": checks,
    "all_four_reproduce": not failed,
    "STOPPED_ROWS": failed,
    "what_this_does_not_establish": ("reproduction confirms the FACT, not the audit's judgement built on it. "
                                     "Each row's corrected wording is still the audit's work order and is "
                                     "installed as such."),
    "tier": "MEASURED over pinned inputs whose digests equal the values the audit recorded",
    "recorded_at": datetime.now(timezone.utc).isoformat(),
}
p = Path(__file__).resolve().parent / "c1_boss_fact_reproduction.v1.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"input_digest_parity": {k: v["equal"] for k, v in pin_report.items()},
                  "reproductions": [{"row": c["row"], "reproduces": c["reproduces"]} for c in checks],
                  "all_four_reproduce": not failed, "STOPPED_ROWS": failed},
                 indent=1, ensure_ascii=False))
for c in checks:
    print()
    print(c["row"], "->", "REPRODUCES" if c["reproduces"] else "DOES NOT REPRODUCE")
    print("  found:", json.dumps(c["found"], ensure_ascii=False)[:700])
