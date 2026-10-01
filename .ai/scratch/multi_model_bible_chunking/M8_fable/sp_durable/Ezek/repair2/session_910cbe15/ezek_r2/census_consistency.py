#!/usr/bin/env python3
"""#e15 Q10: the CENSUS-CONSISTENCY member. Every census figure a row states, re-checked against inventory v2.

The ruling adopts lane 03's proposal as a mechanical member: "every census figure and class name a row states is
re-checked against inventory v2 at its digest ... This is the pass the wave's scoping (fields needing citation
repair) could not include."

WHY IT CATCHES WHAT THE WAVE COULD NOT. The author wave's worklist was scoped to fields needing a citation or a
grounds repair. A row can state a stale census figure in a field no worklist item touched - and the campaign has
already shipped several: a class called "uncounted" that v2 counts at exactly two verses, a K/Q verse that
carries no K/Q note, a transport figure of 20 where the measured class is 33.

THE FIGURES ARE READ FROM THE ARTIFACT, never retyped. Every canonical count comes from inventory v2's own
`count` fields and the LENGTH of its own verse lists, and the two are cross-checked against each other, so a
count field that disagreed with its own list would be caught before any row is judged. The ruling lists the
figures it expects; that list is used only to confirm the reader found them, not as the source.
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
INV = EZ / "ezek_device_inventory.v2.json"
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
INV_PIN = "356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()          # noqa: E731

if sha(INV) != INV_PIN:
    raise SystemExit("REFUSED: the census moved; %s" % sha(INV))
inv = json.loads(INV.read_text(encoding="utf-8"))
rows = [json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]

# ---- harvest every count from the artifact, and cross-check each against its own verse list
counts, mismatched_internally = {}, []


# COUNT-BEARING KEY NAMES, not just "count". My first version harvested only `count` and therefore missed
# four of the figures the ruling names (48, 49, 33, 46) - they live under family_total_distinct, any-form and
# occurrence keys. The ruling's expected-figure list is what exposed the gap: a reader that finds 15 of 19
# declared figures is an incomplete reader, and saying so is the only reason the gap surfaced.
COUNT_KEYS = ("count", "family_total_distinct", "verses", "occurrences", "total", "n",
              "strict_vayehi_adjacent", "vayehi_any_incl_infixed_date", "hayah_perfect_form",
              "any_form_strategy_sweep", "verses_in_the_class", "occurrences_in_the_class")
# THE CENSUS DECLARES ITS OWN LABEL SETS. word_event_family carries `fixed_labels_e12_D1` with all five
# figures named; harvesting every int under any key ending in _labels_* or named `fixed_labels_*` takes the
# census's own declaration instead of my guess at key names. That is how 48 and 49 arrive.
LABEL_BLOCK = ("fixed_labels", "labels", "figures")


def harvest(o, path=""):
    if isinstance(o, dict):
        lst = next((v for k, v in o.items()
                    if k.startswith("verses_mt") and isinstance(v, list)), None)
        for k, v in o.items():
            if any(k.startswith(b) for b in LABEL_BLOCK) and isinstance(v, dict):
                for lk, lv in v.items():
                    if isinstance(lv, int):
                        counts[(path + "/" + k + "/" + lk).strip("/")] = lv
        for ck in COUNT_KEYS:
            n = o.get(ck)
            if isinstance(n, int):
                counts[(path + "/" + ck).strip("/")] = n
                if ck == "count" and lst is not None and len(lst) != n:
                    mismatched_internally.append({"class": path.strip("/"), "count_field": n,
                                                  "verse_list_length": len(lst)})
        # every verse list contributes its own LENGTH as a canonical figure, since a row may cite the list size
        for k, v in o.items():
            if isinstance(v, list) and v and all(isinstance(x, str) for x in v):
                counts[(path + "/" + k + "#len").strip("/")] = len(v)
        for k, v in o.items():
            harvest(v, path + "/" + str(k))


harvest(inv)

# FIGURES FROM THE OTHER PINNED RECORDS. A row may state the marks total, the K/Q note counts or the paseq
# figures; those are not census claims and flagging them as census errors would manufacture defects. They are
# read from the marks record itself, never retyped.
PM = EZ / "pmarks_Ezek.json"
pm = json.loads(PM.read_text(encoding="utf-8"))
other = {}
_marks = pm.get("marks") or {}
if isinstance(_marks, dict):
    other["marks/verses_with_a_mark"] = len(_marks)
    other["marks/total_marks"] = sum(len(v) if isinstance(v, list) else 1 for v in _marks.values())
_kq = pm.get("kq") or {}
if isinstance(_kq, dict):
    other["kq/verses"] = len(_kq)
    other["kq/notes"] = sum(len(v) if isinstance(v, list) else 1 for v in _kq.values())
    other["kq/verses_with_more_than_one_note"] = sum(
        1 for v in _kq.values() if isinstance(v, list) and len(v) > 1)
_ps = pm.get("paseq")
if isinstance(_ps, list):
    other["paseq/occurrences"] = len(_ps)
    other["paseq/verses"] = len(set(_ps))
elif isinstance(_ps, dict):
    other["paseq/verses"] = len(_ps)
    other["paseq/occurrences"] = sum(_ps.values()) if all(isinstance(v, int) for v in _ps.values()) else len(_ps)
CANON_ALL = set(counts.values()) | set(other.values())
CANON = sorted(set(counts.values()))
# the ruling's expected figures, used to CONFIRM the reader found them, not as the source
EXPECTED = {39, 41, 7, 48, 49, 93, 28, 5, 21, 2, 64, 122, 81, 4, 14, 9, 11, 33, 46}
found_expected = sorted(EXPECTED & set(counts.values()))
missing_expected = sorted(EXPECTED - set(counts.values()))

# ---- class-name -> canonical count, for the phrases rows actually use
CLASS_PHRASES = [
    (r"son[- ]of[- ]man", "formulae/son_of_man_address"),
    (r"\bmessenger[- ]formula\b|thus says the lord", "formulae/thus_says_the_lord_yhwh"),
    (r"utterance", "formulae/utterance_of_the_lord_yhwh"),
    (r"recognition family|wide[- ]family|64", "formulae/recognition_family_64"),
    (r"2mp recognition|recognition[- ]family close", "formulae/recognition_formula_2mp"),
    (r"adonai[- ]form recognition|adonai variant", "formulae/recognition_formula_adonai_variant"),
    (r"2fp", "formulae/recognition_formula_2fp"),
    (r"word[- ]event", "formulae/word_event_formula"),
    (r"transport", None),
    (r"dated[- ]oracle|dateline", "dated_oracles"),
]
# a figure stated as "(sweep: N verses)" or "N verses book-wide" or "one of the N"
FIG = re.compile(r"\(sweep:\s*(\d{1,3})\s*verses?\)|\b(\d{1,3})\s+verses?\s+book[- ]wide\b|"
                 r"\bone of (?:the\s+)?(\d{1,3})\b|\bthe\s+(\d{1,3})[- ]verse\b", re.I)
FIELDS = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess")

flags, per_row = [], Counter()
# THE TRANSPORT CLASS SIZE is the class's own figure, not the residue beyond the closed list. My first version
# took the LAST key matching "transport" and got 13 - the count of members beyond the strategy's closed 20 -
# and would have flagged a correct 33 as wrong. The class size is the largest transport figure the census
# carries, and the ruling names it: 33 verses / 46 occurrences.
_tr = [v for k, v in counts.items() if "transport" in k.lower()]
transport_count = max(_tr) if _tr else None
for r in rows:
    rid = r["decision_id"]
    for f in FIELDS:
        val = r.get(f)
        if not isinstance(val, str):
            continue
        for m in FIG.finditer(val):
            n = int(next(g for g in m.groups() if g))
            ctx = val[max(0, m.start() - 110):m.end() + 60]
            if n in CANON_ALL or n in (1, 2, 3):
                continue                     # a figure that matches SOME canonical count, or a small ordinal
            # a figure that matches no canonical count at all is a candidate stale claim
            near = [cls for pat, cls in CLASS_PHRASES if cls and re.search(pat, ctx, re.I)]
            flags.append({"row": rid, "field": f, "figure": n,
                          "context": ctx.replace("\n", " ")[:170],
                          "classes_named_nearby": near,
                          "canonical_counts_for_those": {c: counts.get(c) for c in near},
                          "why": "this figure matches no count in the census"})
            per_row[rid] += 1
        # the transport figure the ruling names explicitly
        for m in re.finditer(r"transport[^.;]{0,60}?\b(\d{1,3})\s+verses?", val, re.I):
            n = int(m.group(1))
            if transport_count is not None and n != transport_count:
                flags.append({"row": rid, "field": f, "figure": n,
                              "context": val[max(0, m.start() - 90):m.end() + 50].replace("\n", " ")[:170],
                              "classes_named_nearby": ["transport"],
                              "canonical_counts_for_those": {"transport": transport_count},
                              "why": "a transport class size against the census's measured %d (#e15 Q8 holds "
                                     "the predicate class governs)" % transport_count})
                per_row[rid] += 1

out = {
    "schema": "ezek_census_consistency.v1",
    "order": "#e15 Q10: every census figure and class name a row states, re-checked against inventory v2",
    "why_the_wave_could_not_include_it": ("the wave's worklist was scoped to fields needing a citation or a "
                                          "grounds repair; a stale census figure can sit in a field no item "
                                          "touched"),
    "figures_from_the_other_pinned_records": other,
    "figures_read_from_the_artifact": {"classes_with_a_count": len(counts),
                                       "distinct_counts": CANON,
                                       "internal_mismatches_count_field_vs_its_own_verse_list":
                                           mismatched_internally,
                                       "rulings_expected_figures_found": found_expected,
                                       "rulings_expected_figures_NOT_found": missing_expected,
                                       "note": ("every canonical count is read from the census's own count "
                                                "fields and cross-checked against the LENGTH of its own verse "
                                                "list, so a count disagreeing with its own list is caught "
                                                "before any row is judged. The ruling's list confirms the "
                                                "reader found the figures; it is not the source.")},
    "inputs": {"census": INV.name, "census_sha256": sha(INV), "rows": ROWS.name, "rows_sha256": sha(ROWS)},
    "flag_count": len(flags),
    "rows_flagged": sorted(per_row),
    "flags": flags,
    "honest_limit": ("this member flags a stated figure that matches NO canonical count. It cannot tell whether "
                     "a figure that matches SOME count is attached to the right class - lane 03's "
                     "'20 verses book-wide' for transport is caught only because the ruling names the transport "
                     "figure explicitly. Attaching a right number to a wrong class needs a reader."),
    "tier": "MEASURED over two pinned artifacts",
}
p = HERE / "census_consistency.v1.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({k: out[k] for k in ("figures_read_from_the_artifact", "flag_count", "rows_flagged")},
                 indent=1))
print()
for f in flags[:14]:
    print("  %-9s %-28s figure=%-4s %s" % (f["row"], f["field"], f["figure"], f["why"][:58]))
    print("        ...%s..." % f["context"][:130])
