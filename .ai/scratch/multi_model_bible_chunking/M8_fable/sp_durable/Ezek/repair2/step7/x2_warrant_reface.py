#!/usr/bin/env python3
"""X2 for WARRANT entries: re-face web: -> oshb: where a warrant RESTS ON an MT-borne device, outside the zone.

Step 4a's mechanical X2 sweep (repair2/step4/x2_reface_plan.py) re-faced DISCLOSURE-* entries only. Four of six step-7
readers found the WARRANT entries resting on MT formulae, datelines, transport verbs and marks still on web: - about
45 corpus-wide. #e15 Q5: "an MT-borne device ... is cited on the oshb: face; a WEB quotation on the web: face".

TWO DERIVATIONS MUST AGREE before an entry is re-faced (a mechanical sweep with a distinct check, as step 4a):
  (A) the ANNOTATION names an MT device class (word-event, messenger, utterance, recognition, dateline, transport,
      set-your-face, hand-of-YHWH, son-of-man/ve'attah, I-YHWH-have-spoken, or a section mark), and carries no curly
      quotation (an English quotation ground stays on web:);
  (B) the CENSUS (inventory v2) or the MARK RECORD shows that class at the entry's verse.
Only single-verse entries outside the zone with identity numbering (web_to_mt) qualify. A class named but not found
at the verse, a range entry, or a zone entry is ROUTED to an author with its reason - re-facing an unsupported claim
would dress it in the authoritative face. Nothing but the prefix changes.

usage: python x2_warrant_reface.py [--out-dir <dir>]   (writes plan.json and proposal.json; never touches the rows)
"""
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
sys.path.insert(0, str(EZ / "tools"))
import ezek_lib as LIB                                                         # noqa: E402

OUT = Path(sys.argv[sys.argv.index("--out-dir") + 1]) if "--out-dir" in sys.argv else HERE / "x2_warrant"
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
pm = json.loads((EZ / "pmarks_Ezek.json").read_text(encoding="utf-8"))
inv = json.loads((EZ / "ezek_device_inventory.v2.json").read_text(encoding="utf-8"))
F = inv["formulae"]


def vs(*lists):
    out = set()
    for l in lists:
        out |= set(l)
    return out


CLASS = {  # annotation keyword pattern -> census verse set (MT refs "Ezek.C.V")
    "word-event": (re.compile(r"word[- ]event", re.I), vs(F["word_event_formula"]["verses_mt"], F["word_event_vayehi_any"]["verses_mt"], F["word_event_hayah_any"]["verses_mt"])),
    "messenger": (re.compile(r"messenger|thus says", re.I), set(F["thus_says_the_lord_yhwh"]["verses_mt"])),
    "utterance": (re.compile(r"utterance", re.I), vs(F["utterance_of_the_lord_yhwh"]["verses_mt"], F["utterance_short_yhwh"]["verses_mt"])),
    "recognition": (re.compile(r"recognition", re.I), vs(F["recognition_family_64"]["verses_mt"], F["recognition_formula"]["verses_mt"], F["recognition_formula_2s"]["verses_mt"],
                                                        F["recognition_formula_2mp"]["verses_mt"], F["recognition_formula_2fp"]["verses_mt"], F["recognition_formula_adonai_variant"]["verses_mt"])),
    "dateline": (re.compile(r"dateline", re.I), set(inv["dated_oracles"]["verses_mt"])),
    "transport": (re.compile(r"transport|guided[- ]motion", re.I), set(inv["vision_transport"]["verses_mt"])),
    "set-your-face": (re.compile(r"set[- ]your[- ]face|set-face", re.I), set(F["set_your_face"]["verses_mt"])),
    "hand-of-YHWH": (re.compile(r"hand[- ]of[- ]YHWH|hand of the Lord", re.I), set(F["hand_of_yhwh_upon_me"]["verses_mt"])),
    "son-of-man": (re.compile(r"son[- ]of[- ]man|ve'attah|we-attah", re.I), set(F["son_of_man_address"]["verses_mt"])),
    "spoken": (re.compile(r"have spoken|I YHWH spoke|spoken formula", re.I), set(F["i_am_yhwh_spoken"]["verses_mt"])),
    "mark": (re.compile(r"\b(?:samekh|pe|petuchah|setumah|parashah|section mark|mark(?:-only)?)\b", re.I), set(pm["marks"].keys())),
}
ENTRY = re.compile(r"^web:Ezek\.(\d{1,2})\.(\d{1,3})(-Ezek\.\d{1,2}\.\d{1,3})? (\[WARRANT-(?:onset|close|rival)(?::(?:near|far|interior))?\]) (.*)$")
ZONE_WEB = {(20, v) for v in range(45, 50)} | {(21, v) for v in range(1, 33)}

rows = [json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]
plan, routed, tally, proposal = [], [], Counter(), {}
for r in rows:
    refs = list(r.get("boundary_evidence_refs") or [])
    new = list(refs)
    for i, e in enumerate(refs):
        m = ENTRY.match(e)
        if not m:
            continue
        c, v, rng, tok, note = int(m.group(1)), int(m.group(2)), m.group(3), m.group(4), m.group(5)
        named = [k for k, (pat, _) in CLASS.items() if pat.search(note)]
        if not named:
            continue                                  # a content or structure warrant: web: is its face
        tally["candidates_naming_a_device"] += 1
        why = None
        if "“" in note or "”" in note:
            why = "the annotation carries an English quotation; its face is an author's call"
        elif (c, v) in ZONE_WEB or c in (20, 21):
            why = "chapters 20-21: dual writing is author work"
        elif rng:
            why = "a range entry: the device's own verse is an author's call"
        elif tuple(LIB.web_to_mt(c, v) or ()) != (c, v):
            why = "identity numbering does not hold here by web_to_mt"
        else:
            key = "Ezek.%d.%d" % (c, v)
            found = [k for k in named if key in CLASS[k][1]]
            if not found:
                why = "the annotation names %s but the census/mark record shows none at MT %d:%d" % ("/".join(named), c, v)
        if why:
            routed.append({"row": r["decision_id"], "index": i, "entry": e, "classes_named": named, "why": why})
            tally["routed"] += 1
            continue
        new[i] = "oshb:" + e[len("web:"):]
        plan.append({"row": r["decision_id"], "index": i, "before": e, "after": new[i], "classes_named": named, "found_in_record": found})
        tally["re_faced"] += 1
    if new != refs:
        proposal[r["decision_id"]] = {"boundary_evidence_refs": new}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "proposal.json").write_text(json.dumps(proposal, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
(OUT / "plan.json").write_text(json.dumps({"schema": "ezek_x2_warrant_reface_plan.v1", "rows_sha256": sha(ROWS), "tally": dict(tally),
                                           "plan": plan, "routed": routed}, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"rows_sha256": sha(ROWS), "tally": dict(tally), "rows_in_proposal": len(proposal),
                  "proposal_sha256": sha(OUT / "proposal.json"), "plan_sha256": sha(OUT / "plan.json"),
                  "routed_reasons": dict(Counter(x["why"].split(":")[0][:60] for x in routed))}, indent=1))
