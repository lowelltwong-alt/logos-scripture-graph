#!/usr/bin/env python3
"""Audit EVERY field my register substitution touched, rather than fixing only what agents named.

WHAT I DID WRONG TWICE OVER. My register repair rewrote 30 fields by regex. The remediation agent found five
broken sentences; I fixed those five and moved on. Spot lane 2 then found a SIXTH, worse than any of them - a
substitution that ran twice over one span, shipped in two fields of P06-009 - and a quick scan finds two more.

Fixing the instances someone hands me, instead of measuring the blast radius of my own edit, is the same shape
as everything else I have got wrong this session: acting on the part of the problem in front of me. The fix is
to compare the pre-substitution bytes with the current bytes for every field I touched and READ each one.

THE DETECTOR looks for the characteristic artifacts of phrase-for-label substitution, and then prints the
context so a human decision is made on the sentence rather than on a pattern:
  * a doubled determiner ("the pinned the section-mark record");
  * a replacement phrase occurring twice adjacently ("the division plan the division plan's held question");
  * a sentence beginning in lower case after a full stop;
  * a replacement phrase immediately followed by a stranded qualifier ("..., line 351") that the label used to
    govern;
  * two replacement phrases in one clause, which is how collisions happen.
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
# the preimage of the register substitution
BEFORE = EZ / "repair" / "rows_v7_cwo24.jsonl.pre_9da4b940834c"
CUR = EZ / "repair" / "rows_v7_cwo24.jsonl"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()          # noqa: E731

REPLACEMENTS = ["the pointed Hebrew witness", "the English witness", "the section-mark record",
                "the verse census", "the device census", "the numbering crosswalk", "the staged verse text",
                "the division plan", "the division plan's held question", "the list of repairs",
                "the coordinating process", "a delegated reader", "the closing checklist",
                "the mark-disclosure duty", "the reading of a mark as standing on the verse it follows",
                "reading each section mark as standing on the verse it follows",
                "a licensed text signal outranks a section mark",
                "the bar on a row under three verses that is not a complete word-event unit"]
FIELDS = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess")

before = {r["decision_id"]: r for r in
          (json.loads(l) for l in BEFORE.read_text(encoding="utf-8").splitlines() if l.strip())}
cur = {r["decision_id"]: r for r in
       (json.loads(l) for l in CUR.read_text(encoding="utf-8").splitlines() if l.strip())}

DET = [
    ("doubled determiner before a replacement",
     re.compile(r"\b(the|a|its|this)\s+(?:pinned\s+)?(?:the|a)\s+(?:" + "|".join(
         re.escape(r[4:] if r.startswith("the ") else r) for r in REPLACEMENTS) + r")", re.I)),
    ("a replacement phrase repeated adjacently",
     re.compile("|".join(re.escape(r) + r"\s+" + re.escape(r) for r in REPLACEMENTS), re.I)),
    ("two replacements colliding in one clause",
     re.compile(r"(?:" + "|".join(re.escape(r) for r in REPLACEMENTS) + r")[^.;]{0,24}?(?:" +
                "|".join(re.escape(r) for r in REPLACEMENTS) + r")", re.I)),
    ("a stranded qualifier a label used to govern",
     re.compile(r"(?:" + "|".join(re.escape(r) for r in REPLACEMENTS) + r")\s*,?\s*line\s+\d+", re.I)),
    ("a sentence beginning in lower case",
     re.compile(r"[.!?]\s+(?:" + "|".join(re.escape(r[4:]) for r in REPLACEMENTS if r.startswith("the "))
                + r")\b")),
]

hits, per_row = [], Counter()
for rid in sorted(cur):
    for f in FIELDS:
        b, c = before.get(rid, {}).get(f), cur[rid].get(f)
        if not isinstance(c, str) or b == c:
            continue                                  # only fields my substitution (or a later pass) changed
        for name, pat in DET:
            for m in pat.finditer(c):
                hits.append({"row": rid, "field": f, "detector": name,
                             "match": m.group(0)[:90],
                             "context": c[max(0, m.start() - 90):m.end() + 70].replace("\n", " ")})
                per_row[rid] += 1

out = {
    "schema": "ezek_substitution_audit.v1",
    "why": ("my register substitution rewrote 30 fields by regex; I then fixed only the five broken sentences "
            "an agent named. A sixth, worse, was found by a reviewer afterwards. This audits every field the "
            "substitution touched instead of waiting to be told."),
    "inputs": {"pre_substitution": BEFORE.name, "pre_substitution_sha256": sha(BEFORE),
               "current": CUR.name, "current_sha256": sha(CUR)},
    "fields_compared": sum(1 for rid in cur for f in FIELDS
                           if isinstance(cur[rid].get(f), str)
                           and before.get(rid, {}).get(f) != cur[rid].get(f)),
    "artifacts_found": len(hits),
    "rows_affected": sorted(per_row),
    "by_detector": dict(Counter(h["detector"] for h in hits)),
    "hits": hits,
}
(HERE / "substitution_audit.v1.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                                 encoding="utf-8", newline="\n")
print(json.dumps({k: out[k] for k in ("fields_compared", "artifacts_found", "rows_affected",
                                      "by_detector")}, indent=1))
print()
seen = set()
for h in hits:
    k = (h["row"], h["field"], h["match"][:40])
    if k in seen:
        continue
    seen.add(k)
    print("  %-9s %-30s [%s]" % (h["row"], h["field"], h["detector"][:38]))
    print("      ...%s..." % h["context"][:150])
