#!/usr/bin/env python3
"""Build Ezekiel's atlas candidate rows, and the three-dimension sidecar the shared feed cannot hold.

CLOSE-GATE ITEM 22. Two outputs, from pinned inputs only:

  atlas_candidate_feed_rows.jsonl   the 16 canonical fields of M8_fable/atlas_candidate_feed.jsonl, nothing added,
                                    for the owner to merge. Merging is the owner's act (OW-11); this tool never
                                    touches the shared feed.
  Ezek_atlas_dimensions.v1.jsonl    method record v6 s15 requires MEASURED, DEPENDENCY and JUDGED to be recorded and
                                    NEVER MERGED. The shared feed has no fields for that separation, and widening a
                                    shared registry's schema is not this tool's authority, so the separation lives in
                                    a sidecar keyed by the same chunk_decision_id.

SELECTION IS MEASURED, not chosen: every shipped row whose RECORDED confidence is low or medium_low - the same rule
the 384 existing feed rows follow (confidence low 59, medium_low 324, medium 1) - PLUS every row the second,
independent reading refused to act on or whose recorded grade it questioned, whatever that grade says. The addition
is not cosmetic: Ezek.29.17-21 is recorded at HIGH confidence and the reconciling reader still declined to act there,
so a confidence-only rule would have dropped the one row whose own grade is in dispute. Ezekiel: 11 low + 90
medium_low + 1 refused-at-high = 102.
AMENDED 2026-09-23 (v10 hold round, OW-30): the widened rule above is retired. Fable's one authorized ruling
(Ezek/fable_end_review/atlas_hold_ruling.v1.json) resolved every referred row against the corpus: six holds
released, the refused-at-high row dropped from the feed, one row kept held in the corpus (rows_v10_final). The
selection is now low/medium_low only, and a row is held exactly when its corpus row is held: 11 + 90 = 101.
The judged score still counts the second reading's refusal or grade question, as its rule text says.

PROSE IS TRANSCRIBED, not re-written: why_low_confidence carries the row's own recorded words, filtered to sentences
that quote no witness bytes (no Hebrew codepoints, no quoted translation), so this deliverable carries no quotation
and therefore no licence obligation of its own - see README.md. possible_downstream_risk is COMPOSED from measured
dependency facts and is labelled as composed in the sidecar.

Usage: gen_atlas_rows.py [--check]     --check rebuilds and compares digests only, writing nothing.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent
ROWS = EZ / "rows_v10_final.jsonl"  # v10 hold round 2026-09-23 (OW-30); was rows_v9_final.jsonl (a80b6e67),
# and before that repair/rows_v7_cwo24.jsonl (the preimage)
FINAL = EZ / "author" / "final"
FEED = EZ.parent.parent / "atlas_candidate_feed.jsonl"
OUT_ROWS = HERE / "atlas_candidate_feed_rows.jsonl"
OUT_DIM = HERE / "Ezek_atlas_dimensions.v1.jsonl"

FEED_KEYS = ["model_id", "book", "span", "chunk_decision_id", "confidence", "observed_substrate_signals",
             "review_packet_final_state", "chunk_review_status", "candidate_hold_state", "non_authorizing",
             "concern_type", "why_low_confidence", "possible_downstream_risk", "suggested_reviewer",
             "proposed_atlas_action", "atlas_promotion_authority"]
SELECT = {"low", "medium_low"}
HEB = re.compile(r"[֐-׿]")
TOKEN = re.compile(r"\[WARRANT[^\]]*\]|\btier-\d\b|\bP\d{2}-\d{3}\b|\bS[1-6]-\d{3}\b|\bK\d\b")
SENT = re.compile(r"(?<=[.;])\s+")
# MT 21:1-5 = WEB 20:45-49 and MT 21:6-37 = WEB 21:1-32; identical elsewhere (method record s8).
ZONE_CH = 21
ZONE_EDGE = ((20, 44), (22, 1))


def vref(s):
    m = re.match(r"Ezek\.(\d+)\.(\d+)$", s or "")
    return (int(m.group(1)), int(m.group(2))) if m else None


def span_ends(span):
    a, _, b = (span or "").partition("-")
    return vref(a), vref(b)


def clean_sentences(text, limit):
    """Sentences of the row's own prose that quote no witness bytes and carry no internal code.

    Returns (kept, filtered, capped), counted SEPARATELY on purpose: 'filtered' means a sentence carried witness
    bytes or an internal code and could not travel, while 'capped' means it was usable but fell past this field's
    sentence limit. Reporting one total would let a reader think the whole remainder was unquotable, when most of it
    is simply not carried. A silent filter would also let this deliverable look fully derived when most of a row's
    reason had in fact been dropped."""
    out, filtered, capped = [], 0, 0
    for s in SENT.split((text or "").replace("\n", " ")):
        s = s.strip()
        if not s:
            continue
        if HEB.search(s) or '"' in s or "“" in s or TOKEN.search(s):
            filtered += 1
            continue
        if len(out) >= limit:
            capped += 1
            continue
        out.append(s if s[-1] in ".;" else s + ".")
    return out, filtered, capped


def concern_of(feat):
    for name, ok in (("numbering_zone_seam", feat["zone"]),
                     ("formula_absent_onset", feat["no_formula"]),
                     ("mark_layer_absence", feat["mark_absence"]),
                     ("scope_hinge", feat["hinge"]),
                     ("compression_zone", feat["dense"]),
                     ("frame_edge", feat["frame"])):
        if ok:
            return name
    return "reading_rests_on_prose"


def build():
    rows = [json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]
    stop, gq, nodef, touched = set(), set(), {}, set()
    for k in range(1, 7):
        d = json.loads((FINAL / ("s%d_adjudication" % k) / "adjudication.json").read_text(encoding="utf-8"))
        for _iid, it in sorted((d.get("items") or {}).items()):
            if not isinstance(it, dict):
                continue
            s, r = str(it.get("status", "")).split()[0] if it.get("status") else "", it.get("row") or ""
            touched.add(r)
            if s == "STOP":
                stop.add(r)
            elif s == "GRADE_QUESTION":
                gq.add(r)
            elif s == "NO_DEFECT":
                nodef[r] = nodef.get(r, 0) + 1
    by_span = {r["span"]: r for r in rows}
    ends = {r["decision_id"]: span_ends(r["span"]) for r in rows}
    order = sorted(rows, key=lambda r: r.get("chunk_index_in_book") or 0)
    neighbour = {}
    for i, r in enumerate(order):
        neighbour[r["decision_id"]] = (order[i - 1]["span"] if i else None,
                                       order[i + 1]["span"] if i + 1 < len(order) else None)
    parent_n = {}
    for r in rows:
        parent_n[r.get("parent_collection")] = parent_n.get(r.get("parent_collection"), 0) + 1

    feed, dims = [], []
    for r in order:
        rid, span = r["decision_id"], r["span"]
        if str(r.get("confidence")) not in SELECT:  # OW-30: low/medium_low only (was: OR referred)
            continue
        notes, alt = r.get("device_notes") or "", r.get("strongest_rejected_alternative") or ""
        low = " ".join([notes, alt]).lower()
        (c1, _v1), (c2, v2) = ends[rid]
        feat = {
            "zone": ZONE_CH in (c1, c2) or (c1, _v1) in ZONE_EDGE or (c2, v2) in ZONE_EDGE,
            "no_formula": "no formula" in low or "no counted formula" in low,
            "mark_absence": "no parashah" in low or "chapter-wide absence" in low,
            "hinge": any(w in low for w in ("fold", "merge", "as its own row", "larger", "rival")),
            "dense": str(r.get("unit_type")) in ("temple_measurement", "temple_law"),
            "frame": any(str(s).startswith(("dateline", "messenger", "wordevent")) for s in
                         (r.get("observed_substrate_signals") or [])),
        }
        held = r.get("candidate_hold_state") is not None  # OW-30: held exactly when the corpus row is held
        referred = rid in stop or rid in gq  # the second reading's own act; it feeds the judged score only
        classes = []
        if feat["zone"]:
            classes.append("numbering_divergence_zone")
        if parent_n.get(r.get("parent_collection"), 0) > 1:
            classes.append("shared_frame")
        if neighbour[rid][0] or neighbour[rid][1]:
            classes.append("shared_seam")
        if feat["mark_absence"] or feat["no_formula"]:
            classes.append("convention_reach")
        risk = []
        if "numbering_divergence_zone" in classes:
            risk.append("This unit lies in the numbering-divergence zone, so every reference into it must carry both "
                        "witnesses' numbers.")
        nb = [s for s in neighbour[rid] if s]
        if "shared_seam" in classes:
            risk.append("It shares a seam with the adjacent unit at %s, so moving that boundary moves two units."
                        % nb[0] if len(nb) == 1 else
                        "It shares seams with the adjacent units at %s, so moving either boundary moves two units."
                        % " and ".join(nb))
        if "convention_reach" in classes:
            risk.append("The reading depends on a convention about an absent mark or an absent formula, and that "
                        "convention's reach is book-wide.")
        if "shared_frame" in classes:
            n_sib = parent_n.get(r.get("parent_collection"), 0) - 1
            risk.append("It sits inside a frame shared with %d other unit%s of this book."
                        % (n_sib, "" if n_sib == 1 else "s"))
        if held:
            risk.append("The second, independent reading declined to act here and referred the question onward.")
        parts, filt_notes, cap_notes = clean_sentences(notes, 2)
        n_from_notes = len(parts)
        alt_s, filt_alt, cap_alt = clean_sentences(alt, 1)
        if alt_s and alt_s[0] not in parts:
            parts.append("Recorded alternative: " + alt_s[0])
        why = " ".join(parts).strip()
        fallback = not why
        if fallback:
            why = ("Recorded at %s confidence; the row's own reason is stated in terms of witness bytes, which this "
                   "deliverable does not transcribe." % r["confidence"])
        feed.append({
            "model_id": "M8_fable", "book": "Ezek", "span": span,
            "chunk_decision_id": "M8-Ezek-%03d" % (r.get("chunk_index_in_book") or 0),
            "confidence": r["confidence"],
            "observed_substrate_signals": list(r.get("observed_substrate_signals") or []),
            "review_packet_final_state": "held_lower_confidence" if held else "accepted_candidate",
            "chunk_review_status": "final_deferred_review" if held else "candidate_review_complete",
            "candidate_hold_state": "deferred_human_or_external_ai" if held else None,
            "non_authorizing": True,
            "concern_type": concern_of(feat),
            "why_low_confidence": why,
            "possible_downstream_risk": " ".join(risk) or None,
            "suggested_reviewer": ("human_owner" if (feat["zone"] or held) else
                                   "convergence" if feat["hinge"] else "literary_form_reviewer"),
            "proposed_atlas_action": "consider_only",
            "atlas_promotion_authority": "none",
        })
        score = ((2 if r["confidence"] == "low" else 1) + (2 if feat["zone"] else 0) + (2 if referred else 0)
                 + (1 if feat["no_formula"] else 0) + (1 if nodef.get(rid) else 0))
        dims.append({
            "schema": "ezek_atlas_dimensions.v1",
            "chunk_decision_id": "M8-Ezek-%03d" % (r.get("chunk_index_in_book") or 0),
            "internal_decision_id": rid, "span": span,
            "measured": {
                "confidence_recorded": r["confidence"], "unit_type": r.get("unit_type"),
                "parent_collection": r.get("parent_collection"),
                "signals": list(r.get("observed_substrate_signals") or []),
                "in_numbering_divergence_zone": feat["zone"],
                "own_notes_state_no_onset_formula": feat["no_formula"],
                "own_notes_disclose_mark_absence": feat["mark_absence"],
                "second_reading": {"addressed_in_final_wave": rid in touched,
                                   "items_where_measurement_found_nothing_to_repair": nodef.get(rid, 0),
                                   "reader_refused_to_act": rid in stop,
                                   "question_about_recorded_grade": rid in gq},
            },
            "derivation": {
                "why_low_confidence_source_fields": [f for f, n in (("device_notes", n_from_notes),
                                                                    ("strongest_rejected_alternative",
                                                                     len(parts) - n_from_notes)) if n],
                "sentences_kept": len(parts),
                "sentences_unquotable_filtered": filt_notes + filt_alt,
                "sentences_usable_but_over_cap": cap_notes + cap_alt,
                "composed_not_derived": fallback,
                "filter": "unquotable means the sentence carries Hebrew codepoints, a double quotation mark, or an "
                          "internal campaign token; over-cap means it was usable but past this field's limit, which "
                          "is 2 sentences from device_notes and 1 from strongest_rejected_alternative",
                "note": "composed_not_derived true means the filter left nothing usable and the field carries a "
                        "sentence written here instead of the row's own words",
            },
            "dependency": {"classes": classes, "neighbour_spans": [s for s in neighbour[rid] if s],
                           "units_sharing_this_frame": parent_n.get(r.get("parent_collection"), 0),
                           "composed_sentence_in_feed": " ".join(risk) or None},
            "judged": {"tier": "JUDGED_BY_RULE", "atlas_hardness": "high" if score >= 4 else
                       "medium" if score >= 2 else "low", "score": score,
                       "rule": "low confidence 2, medium_low 1, numbering zone 2, second reading refused or "
                               "questioned the grade 2, own notes state no onset formula 1, at least one repair item "
                               "the second reading found nothing to repair 1; high at 4, medium at 2",
                       "not_a_measurement": "This rating is assigned by the stated rule over measured inputs. No one "
                                            "re-read the passage to produce it."},
        })
    return feed, dims, rows


def dump(objs):
    return "".join(json.dumps(o, ensure_ascii=False) + "\n" for o in objs).encode("utf-8")


def main():
    feed, dims, rows = build()
    a, b = dump(feed), dump(dims)
    if "--check" in sys.argv:
        ok = True
        for p, data in ((OUT_ROWS, a), (OUT_DIM, b)):
            on = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else "ABSENT"
            new = hashlib.sha256(data).hexdigest()
            ok = ok and on == new
            print("%-34s on_disk %s  rebuilt %s" % (p.name, on[:12], new[:12]))
        print("DETERMINISTIC: MATCH" if ok else "MISMATCH")
        sys.exit(0 if ok else 1)
    OUT_ROWS.write_bytes(a)
    OUT_DIM.write_bytes(b)
    print("rows selected        %d of %d shipped units (confidence low or medium_low; held exactly "
          "when the corpus row is held, OW-30)" % (len(feed), len(rows)))
    print("held for referral    %d" % sum(1 for f in feed if f["candidate_hold_state"]))
    print("concern types        %s" % json.dumps({c: sum(1 for f in feed if f["concern_type"] == c)
                                                  for c in sorted({f["concern_type"] for f in feed})}))
    print("hardness (judged)    %s" % json.dumps({h: sum(1 for d in dims if d["judged"]["atlas_hardness"] == h)
                                                  for h in ("high", "medium", "low")}))
    print("%-34s %d bytes  sha256 %s" % (OUT_ROWS.name, len(a), hashlib.sha256(a).hexdigest()))
    print("%-34s %d bytes  sha256 %s" % (OUT_DIM.name, len(b), hashlib.sha256(b).hexdigest()))
    print("rows input           sha256 %s" % hashlib.sha256(ROWS.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
