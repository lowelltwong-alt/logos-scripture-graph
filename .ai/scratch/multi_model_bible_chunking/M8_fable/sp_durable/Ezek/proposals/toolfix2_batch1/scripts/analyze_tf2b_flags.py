"""Second-pass facts for the controlling agent on the staged TOOLFIX-2 (stage_tf2b). Read-only; writes stage_tf2b/flags_analysis.json.
  1. check_marks: removed and added flags paired by (row, rule).
     - shape_only: the flag persists but gained a key (scope);
     - real_removed / real_added.
  2. First-pass labels for real added flags:
     - false_kq_absence_claim: the words between the nearest negator and the K/Q token (a negator more than two words
       away, or governing another noun, is a likely false positive);
     - false_mark_absence_claim: 'between X and Y' phrasing, or the marked key being the span's front seam;
     - paragraph_mark_claim / kq_claim: the clause and the numbers it names.
  3. UNBOUND_NOW: whether the K/Q mention sits inside a boundary_evidence_refs entry, which citation_sweep's HARD K/Q ref
     arm checks against the entry's own ref.
  4. S1-05 coverage: the rows S1-05 names, each marked flagged / not flagged under the staged literal arms."""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
SCR = Path(__file__).resolve().parent
ROOT = SCR / "stage_tf2b"
ST_T = ROOT / "sp_durable" / "Ezek" / "tools"
impact = json.loads((ROOT / "corpus_impact.json").read_text(encoding="utf-8"))
mreview = json.loads((ROOT / "marks_review.json").read_text(encoding="utf-8"))
sys.path.insert(0, str(ST_T))
spec = importlib.util.spec_from_file_location("cm_staged", ST_T / "check_marks.py")
cm = importlib.util.module_from_spec(spec)
sys.argv = ["check_marks.py"]
spec.loader.exec_module(cm)
pm = cm.load_pmarks()
rows = {json.loads(l)["decision_id"]: json.loads(l) for l in (SP / "Ezek" / "repair" / "rows_v3_cwo12.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}

mv = impact["lists"].get("mark_symmetry.flags", {"added": [], "removed": []})
key = lambda f: (f.get("decision_id"), f.get("rule"))
removed_by, added_by = {}, {}
for f in mv["removed"]:
    removed_by.setdefault(key(f), []).append(f)
for f in mv["added"]:
    added_by.setdefault(key(f), []).append(f)
shape_only, real_removed, real_added = [], [], []
for k in sorted(set(removed_by) | set(added_by), key=lambda x: (str(x[0]), str(x[1]))):
    r, a = removed_by.get(k, []), added_by.get(k, [])
    n = min(len(r), len(a))
    stripped = lambda f: {q: w for q, w in f.items() if q != "scope"}
    pairs = 0
    ra, aa = list(r), list(a)
    for fr in list(ra):
        match = next((fa for fa in aa if stripped(fa) == fr or (fr.get("claim_context") and fa.get("claim_context") == fr.get("claim_context"))), None)
        if match is not None:
            shape_only.append({"row": k[0], "rule": k[1], "installed": fr, "staged": match})
            ra.remove(fr)
            aa.remove(match)
            pairs += 1
    real_removed += [{"row": k[0], "rule": k[1], "flag": f} for f in ra]
    real_added += [{"row": k[0], "rule": k[1], "flag": f} for f in aa]

NEGATOR = re.compile(r"\b(?:no|not|nor|never|without|absent|lacks?|lacking|none)\b", re.I)


def row_text(row):
    return cm.prose_of(row) + " " + " ".join(row.get("boundary_evidence_refs", []))


labels = []
for e in real_added:
    row, f, rule = rows.get(e["row"], {}), e["flag"], e["rule"]
    text = row_text(row)
    lab = {"row": e["row"], "rule": rule}
    if rule == "false_kq_absence_claim":
        ctx = f.get("claim_context") or ""
        idx = text.find(ctx[:60]) if ctx else -1
        best = None
        for m in cm.KQ.finditer(text):
            if idx != -1 and not (idx <= m.start() <= idx + len(ctx) + 60):
                continue
            if not cm.puncta_negated(text, m.start(), m.end()):
                continue
            lo, _ = cm.clause_bounds(text, m.start(), m.start(), cm.NEG_CLAUSE_END)
            negs = list(NEGATOR.finditer(text, lo, m.start()))
            if negs:
                between = text[negs[-1].end():m.start()]
                best = {"negator": negs[-1].group(0), "words_between": len(between.split()), "between": between[-80:],
                        "kq_token": m.group(0), "clause": text[lo:m.end() + 60][:240]}
                break
        lab.update({"kq_mt_keys": f.get("kq_mt_keys"), "scope": f.get("scope"), "negation": best,
                    "first_pass": ("likely_false_positive: the negator is more than two words from the K/Q token"
                                   if best and best["words_between"] > 2 else
                                   "adjacent negator: review against the inventory keys (a true positive if the span holds the note)")})
    elif rule == "false_mark_absence_claim":
        ctx = f.get("claim_context") or ""
        have = f.get("span_relevant_marks_mt_keys") or {}
        pairs = cm.span_pairs(row)
        front = None
        if pairs:
            c0, v0 = pairs[0]
            prev = (c0, v0 - 1) if v0 > 1 else (c0 - 1, cm.LAST_VERSE.get(c0 - 1, 0))
            mt = cm.web_to_mt(*prev)
            front = "Ezek.%d.%d" % mt if mt else None
        lab.update({"scope": f.get("scope"), "marked_keys": sorted(have), "front_seam_key": front,
                    "between_phrase": bool(re.search(r"\bbetween\b", ctx, re.I)), "claim_context": ctx[:220],
                    "first_pass": ("likely_false_positive: 'between X and Y' names its bounding verses" if re.search(r"\bbetween\b", ctx, re.I)
                                   else "likely_false_positive: the only marked key is the front seam, outside 'this span'" if have and set(have) == {front}
                                   else "review")})
    else:
        lab.update({k: f.get(k) for k in ("verse_cited", "claimed")})
        vc = f.get("verse_cited") or ""
        mnum = re.match(r"Ezek\.(\d+)\.(\d+)", vc)
        if mnum:
            c, v = mnum.group(1), mnum.group(2)
            pat = re.compile(r"(?<![A-Za-z\d])%s[:.]%s(?!\d)" % (c, v))
            hits = [text[max(0, m.start() - 140):m.end() + 60] for m in pat.finditer(text)][:2]
            lab["contexts"] = hits
            lab["inventory"] = {"marks": pm["marks"].get(vc), "kq": bool(pm["kq"].get(vc)),
                                "marks_prev_verse": pm["marks"].get("Ezek.%s.%d" % (c, int(v) - 1))}
        lab["first_pass"] = "review: a mark or K/Q claim bound to a verse its own clause names"
    labels.append(lab)

unbound = []
for e in mreview.get("unbound_now", []):
    row = rows.get(e["row"], {})
    in_refs = any(e.get("clause", "").strip()[:30] in r for r in row.get("boundary_evidence_refs", []))
    unbound.append({"row": e["row"], "rule": e["rule"], "clause": e.get("clause"), "inside_a_ref_entry": in_refs,
                    "covered_by": ("citation_sweep's HARD K/Q ref arm checks the entry's own ref" if in_refs and e["rule"] == "kq_claim"
                                   else "not covered by a HARD arm: hand review")})

S1_05_ROWS = ["P01-002", "P01-013", "P06-013", "P07-004", "P08-007", "P11-012", "P11-014", "P11-015", "P06-012", "P07-009", "P10-016", "P10-007",
              "P08-001", "P09-002", "P01-003", "P08-002", "P08-004", "P08-005", "P08-006", "P08-012", "P08-015", "P06-007", "P11-001", "P02-020"]
reg_added = impact["lists"].get("register.flags", {}).get("added", [])
flagged_rows = {}
# check_register keys a flag by the row's writer_decision_id when the row has one, so flags are mapped back to decision ids
writer_to_did = {str(r.get("writer_decision_id")): did for did, r in rows.items() if r.get("writer_decision_id")}
for f in reg_added:
    if f.get("class") == "author_wave_register_s1_05":
        did_ = writer_to_did.get(str(f.get("decision_id")), f.get("decision_id"))
        flagged_rows.setdefault(did_, []).append(f.get("match"))
coverage = {r: flagged_rows.get(r, "NOT FLAGGED by the literal arms") for r in S1_05_ROWS}
LITERAL_MISSES = {}
for r in S1_05_ROWS:
    row = rows.get(r, {})
    prose = " ".join(str(row.get(k) or "") for k in ("boundary_rationale", "strongest_rejected_alternative", "device_notes"))
    for name, pat in (("prior ... reading with digits", r"\bprior [\d:.\-–]+ reading\b"), ("former ... span", r"\bformer (?!span\b|row\b)[\w.\- ]{1,30}?\bspan\b"),
                      ("previously held", r"\bpreviously held\b"), ("of N ... rows", r"\b(?:one|middle|last|first) of \w+ [\w-]+ rows\b"),
                      ("strategy citation without an apostrophe", r"\b(?:the book's|per the|per its) strategy\b|\bstrategy (?:section|§)")):
        for m in re.finditer(pat, prose, re.I):
            LITERAL_MISSES.setdefault(r, []).append({"pattern": name, "text": prose[max(0, m.start() - 40):m.end() + 40]})
out = {"check_marks": {"removed_total": len(mv["removed"]), "added_total": len(mv["added"]), "shape_only_pairs": len(shape_only),
                       "real_removed": len(real_removed), "real_added": len(real_added)},
       "shape_only": [{"row": s["row"], "rule": s["rule"], "staged_scope": s["staged"].get("scope")} for s in shape_only],
       "real_added_first_pass": labels, "unbound_now": unbound,
       "s1_05_literal_coverage": coverage, "s1_05_literal_misses": LITERAL_MISSES}
(ROOT / "flags_analysis.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
summary = {"check_marks": out["check_marks"], "shape_only": out["shape_only"],
           "first_pass_counts": {}, "unbound_now": unbound, "s1_05_not_flagged": [r for r, v in coverage.items() if isinstance(v, str)],
           "s1_05_literal_misses": {r: [x["pattern"] for x in v] for r, v in LITERAL_MISSES.items()}}
for l in labels:
    fp = l["first_pass"].split(":")[0]
    summary["first_pass_counts"]["%s | %s" % (l["rule"], fp)] = summary["first_pass_counts"].get("%s | %s" % (l["rule"], fp), 0) + 1
summary["real_added_detail"] = labels
print(json.dumps(summary, ensure_ascii=False, indent=1))
