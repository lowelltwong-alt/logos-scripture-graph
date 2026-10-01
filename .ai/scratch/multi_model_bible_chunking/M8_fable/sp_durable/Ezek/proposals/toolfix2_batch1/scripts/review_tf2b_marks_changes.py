"""Hand-review support for ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2 condition (c). Every check_marks flag that the
staged batch (stage_tf2b) REMOVES or ADDS over the chain head is classified by re-deriving the claim under both readings:
  - the installed tools' reading: the NEAREST dotted ref within +-120 characters;
  - the staged tools' reading: the numbers written in the claim's own clause, a directly-following parenthetical, and
    chapters named for absence phrases; a negated K/Q token is an absence claim.

REMOVED classes:
  rebound_true            the own clause names a verse that confirms the claim
  negated_absence_true    a negated K/Q claim whose named or span verses carry no K/Q
  scoped_absence_true     an absence phrase whose named verses or chapter carry no mark
  UNBOUND_NOW             the claim's clause names no number, so the staged tool no longer checks it (a possible lost true
                          positive; its context is listed for review)
  other                   anything else, listed with context
ADDED flags are listed with the claim context and the named verses.

Also prints the NEW HARD class items: the row sentence and the cited verse's bytes. Read-only; writes
stage_tf2b/marks_review.json."""
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
sys.path.insert(0, str(ST_T))
spec = importlib.util.spec_from_file_location("cm_staged", ST_T / "check_marks.py")
cm = importlib.util.module_from_spec(spec)
sys.argv = ["check_marks.py"]
spec.loader.exec_module(cm)
pm = cm.load_pmarks()
marks, kq = pm["marks"], pm["kq"]
kq_note_keys = {k for k, notes in pm.get("notes_other", {}).items() if any(cm.KQ_NOTE.search(n.get("text", "")) for n in notes)}
rows = {json.loads(l)["decision_id"]: json.loads(l) for l in (SP / "Ezek" / "repair" / "rows_v3_cwo12.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
oshb = dict(l.split("\t", 1) for l in (SP / "Ezek" / "Ezek_oshb.txt").read_text(encoding="utf-8").splitlines() if "\t" in l)


def row_text(row):
    return cm.prose_of(row) + " " + " ".join(row.get("boundary_evidence_refs", []))


def installed_nearest(text, m):
    lo = max(0, m.start() - 120)
    ctx = text[lo:m.start() + 120]
    cands = list(cm.VERSE_NEAR.finditer(ctx))
    if not cands:
        return None, ctx, []
    rel = m.start() - lo
    cands.sort(key=lambda vm: abs(vm.start() - rel))
    return "Ezek.%s.%s" % (cands[0].group(1), cands[0].group(2)), ctx, cands


def named(text, s, e, chapters=False):
    out = [p for pairs in cm.puncta_claim_numbers(text, s, e) for p in pairs]
    if chapters:
        lo, hi = cm.clause_bounds(text, s, e, cm.NUM_CLAUSE_END)
        for chm in cm.CHAPTER_NAMED.finditer(text, lo, hi):
            c = int(chm.group(1))
            out += [(c, v) for v in range(1, cm.MT_LAST_VERSE.get(c, 0) + 1)]
    return out


def clause_of(text, s, e):
    lo, hi = cm.clause_bounds(text, s, e, cm.NUM_CLAUSE_END)
    return text[lo:hi][:240]


review = {"removed": [], "added": []}
flags_moved = impact["lists"].get("mark_symmetry.flags", {"added": [], "removed": []})
for fl in flags_moved["removed"]:
    did, rule = fl.get("decision_id"), fl.get("rule")
    row = rows.get(did)
    entry = {"row": did, "rule": rule, "installed_flag": {k: fl.get(k) for k in ("verse_cited", "claimed", "claim_context") if fl.get(k)}}
    if not row:
        entry["class"] = "other"
        entry["why"] = "row not in the chain head"
        review["removed"].append(entry)
        continue
    text = row_text(row)
    if rule == "kq_claim":
        hit = None
        for m in cm.KQ.finditer(text):
            near, ctx, cands = installed_nearest(text, m)
            if near == fl.get("verse_cited") and not any(kq.get("Ezek.%d.%d" % rc) for vm in cands for rc in cm.readings(int(vm.group(1)), int(vm.group(2)))):
                hit = m
                break
        if hit is None:
            entry["class"] = "other"
            entry["why"] = "the flagged K/Q token could not be re-derived"
        else:
            nm = named(text, hit.start(), hit.end())
            neg = cm.puncta_negated(text, hit.start(), hit.end())
            entry["clause"] = clause_of(text, hit.start(), hit.end())
            entry["named"] = ["%d:%d" % p for p in nm]
            if neg:
                keys = {"Ezek.%d.%d" % rc for c, v in nm for rc in cm.readings(c, v)} if nm else {
                    "Ezek.%d.%d" % mt for c, v in cm.span_pairs(row) for mt in [cm.web_to_mt(c, v)] if mt}
                entry["class"] = "negated_absence_true" if not any(kq.get(k) for k in keys) else "moved_to_false_kq_absence_claim"
            elif not nm:
                entry["class"] = "UNBOUND_NOW"
            elif any(kq.get("Ezek.%d.%d" % rc) or ("Ezek.%d.%d" % rc in kq_note_keys) for c, v in nm for rc in cm.readings(c, v)):
                entry["class"] = "rebound_true"
            else:
                entry["class"] = "other"
                entry["why"] = "still unconfirmed under the staged binding but not flagged"
    elif rule == "paragraph_mark_claim":
        want = fl.get("claimed")
        hit = None
        markish = list(cm.PARAMARK.finditer(text)) + [m for m in cm.PARAMARK_LETTER.finditer(text)
                                                        if cm.MARKISH_CTX.search(text[max(0, m.start() - 60):m.start() + 60])]
        for m in markish:
            wt = "PE" if m.group(0).lower() in ("petuchah", "pe") else "SAMEKH"
            near, ctx, cands = installed_nearest(text, m)
            if wt == want and near == fl.get("verse_cited"):
                hit = m
                break
        if hit is None:
            entry["class"] = "other"
            entry["why"] = "the flagged mark mention could not be re-derived"
        else:
            nm = named(text, hit.start(), hit.end())
            entry["clause"] = clause_of(text, hit.start(), hit.end())
            entry["named"] = ["%d:%d" % p for p in nm]
            if not nm:
                entry["class"] = "UNBOUND_NOW"
            elif any(want in marks.get("Ezek.%d.%d" % rc, []) for c, v in nm for rc in cm.readings(c, v)):
                entry["class"] = "rebound_true"
            elif cm.ABSENCE.search(entry["clause"]):
                entry["class"] = "absence_clause_skip"
            else:
                entry["class"] = "other"
                entry["why"] = "still unconfirmed under the staged binding but not flagged"
    elif rule == "false_mark_absence_claim":
        hit = None
        for am in cm.ABSENCE.finditer(text):
            if (fl.get("claim_context") or "")[:40] in text[max(0, am.start() - 60):am.start() + 80]:
                hit = am
                break
        if hit is None:
            entry["class"] = "other"
            entry["why"] = "the flagged absence phrase could not be re-derived"
        else:
            nm = named(text, hit.start(), hit.end(), chapters=True)
            entry["clause"] = clause_of(text, hit.start(), hit.end())
            entry["named"] = sorted({"%d:%d" % p for p in nm})[:12]
            if nm and not any(marks.get("Ezek.%d.%d" % rc) for c, v in nm for rc in cm.readings(c, v)):
                entry["class"] = "scoped_absence_true"
            else:
                entry["class"] = "other"
                entry["why"] = "absence phrase names no verse, or names a marked verse, yet the flag was removed"
    else:
        entry["class"] = "other"
        entry["why"] = "a rule this review does not re-derive"
    review["removed"].append(entry)
for fl in flags_moved["added"]:
    did, rule = fl.get("decision_id"), fl.get("rule")
    review["added"].append({"row": did, "rule": rule, **{k: fl.get(k) for k in ("verse_cited", "claimed", "scope", "kq_mt_keys",
                                                                                 "span_relevant_marks_mt_keys", "claim_context") if fl.get(k) is not None}})
counts = {"removed": {}, "added": {}}
for e in review["removed"]:
    counts["removed"][e["class"]] = counts["removed"].get(e["class"], 0) + 1
for e in review["added"]:
    counts["added"][e["rule"]] = counts["added"].get(e["rule"], 0) + 1
new_hard = []
for item in impact["hard_classes"]["NEW_HARD_CLASS_ITEMS"]:
    did = str(item).split(":", 1)[0]
    row = rows.get(did, {})
    run_m = re.search(r"Hebrew quote '([^']+)'", str(item))
    ref_m = re.search(r"best oshb:(Ezek\.\d+\.\d+)", str(item))
    run = run_m.group(1) if run_m else None
    sentence = None
    for field in ("boundary_rationale", "strongest_rejected_alternative", "device_notes"):
        s = row.get(field) or ""
        if run and run in s:
            i = s.find(run)
            sentence = s[max(0, s.rfind(".", 0, i) + 1):s.find(".", i + len(run)) + 1 or None][:400]
            break
    verse = oshb.get(ref_m.group(1)) if ref_m else None
    containing = [w for w in (verse or "").split(" ") if run and run in "".join(ch for ch in w if not ("\u0591" <= ch <= "\u05c7"))]
    new_hard.append({"item": item, "run": run, "sentence": sentence, "cited_verse": ref_m.group(1) if ref_m else None,
                     "verse_words_containing_the_run": containing})
out = {"counts": counts, "unbound_now": [e for e in review["removed"] if e["class"] == "UNBOUND_NOW"],
       "other_removed": [e for e in review["removed"] if e["class"] == "other"], "added": review["added"], "new_hard_class": new_hard}
(ROOT / "marks_review.json").write_text(json.dumps({"review": review, **out}, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"counts": counts, "unbound_now": len(out["unbound_now"]), "other_removed": len(out["other_removed"]),
                  "unbound_now_sample": out["unbound_now"][:12], "other_removed_sample": out["other_removed"][:8],
                  "added_sample": out["added"][:14], "new_hard_class": new_hard}, ensure_ascii=False, indent=1))
