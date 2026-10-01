#!/usr/bin/env python3
"""REPAIR-2 step-6 WORKLIST: the A8 transport batch (#e15 Q8), with its distinct checks run BEFORE any author sees it.

#e15's sequence: "6_a8_transport: Q8: the eight released items after distinct checks; the seven A16 weighings of
interior members; the five onset rows may name their driver."

DISTINCT CHECKS, each class two ways, both required before an item is issued:
  transport (33 verses): (A) the inventory v2 list; (D) this builder's own scan of the witness bytes with the
      predicate the inventory STATES (three forms), written here from the predicate text, not from its token lists.
  recognition memberships behind peer_03's held findings: (A) the inventory v2 lists (family 64, 2mp 21, 2fp 2);
      (D) a scan for a yd'-root token plus the contiguous phrase 'ki ani YHWH' (family), and the 2mp/2fp skeletons.
A book-wide disagreement between A and D is REPORTED; an item whose own verse disagrees is REFUSED.

THE RULING'S COUNTS ARE CHECKED, not trusted (E-35): Q8 names seven A16 weighings but lists eight interior verses;
37:2 is carried by the ruling to Q4 as a disclosure (a one-verse remainder), which leaves seven - the builder asserts
that arithmetic and records the mapping as INFERRED. Every verse-to-row mapping is checked by span containment, and
every onset verse against the row's first verse.

THE HELD ITEMS WERE NEVER LISTED BY ID in any record. They are identified here from the peers' own words:
peer_10's unresolved_uncertainty names its four rows and verses; peer_03's names the memberships its four findings
rest on (13:14, 13:21, 13:23, 14:8, 15:7), mapped to rows by span containment and required to come to four rows.

usage: python build_step6_worklist.py [--probe]
"""
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
PROBE = "--probe" in sys.argv
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step6_probe")
OUT = (SCR if PROBE else HERE) / "step6_worklist.v1.json"
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
PROSE = ("boundary_rationale", "strongest_rejected_alternative", "device_notes")

rows = {r["decision_id"]: r for r in (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}
inv = json.loads((EZ / "ezek_device_inventory.v2.json").read_text(encoding="utf-8"))
e15 = json.loads((EZ / "ezek_controlling_agent_ruling_e15.v1.json").read_text(encoding="utf-8"))
e12 = json.loads((EZ / "ezek_controlling_agent_ruling_e12.v1.json").read_text(encoding="utf-8"))
q8 = e15["q8_transport_class"]


def skeleton(t):
    t = t.replace("\u05BE", " ")
    return "".join(ch for ch in unicodedata.normalize("NFD", t)
                   if not ("\u0591" <= ch <= "\u05C7" and ch not in "\u05D0\u05EA") or "\u05D0" <= ch <= "\u05EA")


verses = {}
for line in (EZ / "Ezek_oshb.txt").read_text(encoding="utf-8").splitlines():
    if "\t" in line:
        ref, text = line.split("\t", 1)
        verses[ref.strip()] = skeleton(text)
if len(verses) < 1200:
    raise SystemExit("REFUSED: the witness parsed to %d verses (E-36)" % len(verses))
ORDER = list(verses)

# ---- (D) transport, from the STATED predicate
F1 = re.compile(r"^(?:וי|ות|וה|ה)(?:ביא|בא|וציא|וצא|ולכ|עביר|עבר|שא|ניח|שב|סב|קח)ני$")
F2A, F2B = {"ויבא", "ותבא", "ותשא", "וישב"}, "ויביא"


def transport_hits(sk):
    toks = sk.split()
    hits = [t for t in toks if F1.match(t) or t == "נשאתני"]
    hits += ["%s %s" % (a, b) for a, b in zip(toks, toks[1:]) if (a in F2A and b == "אתי") or (a == F2B and b == "אותי")]
    return hits


D_transport = [v for v in ORDER if transport_hits(verses[v])]
A_transport = inv["vision_transport"]["verses_mt"]
transport_agree = set(D_transport) == set(A_transport)

# ---- (D) recognition
KI = "כי אני יהוה"


def fam(sk):
    return KI in sk and any("ידע" in t or re.match(r"^ו?[יתנא]?דע", t) for t in sk.split())


fams = inv["formulae"]
D_fam = [v for v in ORDER if fam(verses[v])]
D_2mp = [v for v in ORDER if "וידעתם " + KI in verses[v]]
D_2fp = [v for v in ORDER if "וידעתן " + KI in verses[v]]
recog = {"family_64": (fams["recognition_family_64"]["verses_mt"], D_fam),
         "2mp_21": (fams["recognition_formula_2mp"]["verses_mt"], D_2mp),
         "2fp_2": (fams["recognition_formula_2fp"]["verses_mt"], D_2fp)}
recog_agree = {k: set(a) == set(d) for k, (a, d) in recog.items()}


def vkey(ref):
    c, v = ref.split(".")[1:3]
    return int(c), int(v)


def in_span(rid, ref):
    s = rows[rid]["span"]
    m = re.match(r"(?:oshb|web)?:?Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)", s) or re.match(r"Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)", s)
    if not m:
        raise SystemExit("REFUSED: span form not understood on %s: %r" % (rid, s))
    a, b = (int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))
    return a <= vkey(ref) <= b, a


def row_of(ref):
    hit = [rid for rid in rows if in_span(rid, ref)[0]]
    if len(hit) != 1:
        raise SystemExit("REFUSED: %s falls in %d rows" % (ref, len(hit)))
    return hit[0]


items = []


def add(cls, row, data, order):
    refs = ["boundary_evidence_refs"] if cls in ("REL10", "A16", "ONSET5") else []
    items.append({"id": None, "class": cls, "row": row, "fields_hint": list(PROSE) + refs, "order": order, "data": data,
                  "status": "PENDING"})


# ---- REL10: peer_10's four transport rows, from its own words
p10 = json.loads((EZ / "reviews" / "peer_10.json").read_text(encoding="utf-8"))
u10 = next(u for u in p10["unresolved_uncertainty"] if "transport" in json.dumps(u, ensure_ascii=False))
pairs = re.findall(r"(P\d\d-\d\d\d) at (\d+):(\d+)", u10)
if len(pairs) != 4:
    raise SystemExit("REFUSED: peer_10's statement yields %d row/verse pairs, not four" % len(pairs))
for rid, c, v in pairs:
    ref = "Ezek.%s.%s" % (c, v)
    ok, _ = in_span(rid, ref)
    if not ok or ref not in A_transport or ref not in D_transport:
        raise SystemExit("REFUSED: released item %s %s fails a distinct check (span %s, inventory %s, scan %s)"
                         % (rid, ref, ok, ref in A_transport, ref in D_transport))
    add("REL10", rid, {"verse_mt": ref, "in_span": True, "in_inventory_33": True, "in_predicate_scan": True,
                       "tokens_found_by_scan": transport_hits(verses[ref]), "peer_10_said": u10},
        "RELEASED (Q8): score peer_10's held reading against the 33 - the verse IS a member, so a reading that depended "
        "on its being inside stands and one that depended on its being outside fails. The row may name it as a "
        "transport verse of the counted class (sweep: 33 verses / 46 occurrences); a '20' figure for the class is stale.")

# ---- REL03: peer_03's four findings, via the memberships it names
p03 = json.loads((EZ / "reviews" / "peer_03.json").read_text(encoding="utf-8"))
u03 = next(u for u in p03["unresolved_uncertainty"] if "64-verse" in json.dumps(u, ensure_ascii=False))
clause = re.search(r"memberships I rely on - (.*?) - follow", u03["what"])
if not clause:
    raise SystemExit("REFUSED: peer_03's membership clause not found in its own words")
mems = ["Ezek.%s.%s" % m for m in re.findall(r"(?:Ezek\.)?(\d{1,2})\.(\d{1,3})", clause.group(1))]
if len(mems) != 5:
    raise SystemExit("REFUSED: peer_03's clause names %d memberships, expected the five it lists: %r" % (len(mems), clause.group(1)))
by_row = {}
for ref in mems:
    by_row.setdefault(row_of(ref), []).append(ref)
if len(by_row) != 4:
    raise SystemExit("REFUSED: peer_03's memberships map to %d rows, not the four it names: %s" % (len(by_row), by_row))
for rid, refs in sorted(by_row.items()):
    checks = {ref: {k: {"inventory": ref in a, "scan": ref in d} for k, (a, d) in recog.items()} for ref in refs}
    for ref, ch in checks.items():
        if ch["family_64"]["inventory"] != ch["family_64"]["scan"] or not ch["family_64"]["inventory"]:
            raise SystemExit("REFUSED: %s fails the family distinct check: %s" % (ref, ch))
    peer_item = (p03.get("items") or {}).get(rid)
    add("REL03", rid, {"memberships": checks, "peer_03_said": u03, "peer_03_row_item": peer_item},
        "RELEASED (Q8): the memberships this finding rests on are now on pinned lists and pass both derivations. "
        "Score the finding against the row as it stands now: repair what still stands, NO_DEFECT with evidence what "
        "an earlier repair already cured.")

# ---- A16: interior members, from the ruling's own text
txt = q8["blast_radius_measured"]["interior_members_now_licensed_rivals_to_weigh_A16"]
entries = re.findall(r"(\d+:\d+)(?: and (\d+:\d+))? in (P\d\d-\d\d\d) \(([^;]*?(?:\([^)]*\)[^;]*?)*)\)?(?=;|$)", txt)
found = []
for m in re.finditer(r"(\d+:\d+)(?: and (\d+:\d+))? in (P\d\d-\d\d\d)", txt):
    for cv in filter(None, (m.group(1), m.group(2))):
        found.append((cv, m.group(3), txt[m.end():m.end() + 160]))
disclosure_only = [f for f in found if "DISCLOSURE-device" in f[2].split(";")[0]]
weighings = [f for f in found if f not in disclosure_only]
if len(found) != 8 or len(weighings) != 7:
    raise SystemExit("REFUSED: the ruling's interior list gives %d verses and %d weighings; Q8's sequence says seven" % (len(found), len(weighings)))
for cv, rid, tail in found:
    ref = "Ezek.%s.%s" % tuple(cv.split(":"))
    ok, _ = in_span(rid, ref)
    if not ok or ref not in A_transport or ref not in D_transport:
        raise SystemExit("REFUSED: A16 member %s %s fails a distinct check" % (rid, ref))
    if (cv, rid, tail) in disclosure_only:
        add("A16-DISCLOSE", rid, {"verse_mt": ref, "ruling_text_for_this_row": tail.split(";")[0]},
            "The ruling carries this member to a disclosure (a one-verse remainder): confirm the row discloses it as a "
            "device it does not rest on; weigh nothing here. INFERRED from the ruling's wording.")
    else:
        add("A16", rid, {"verse_mt": ref, "ruling_text_for_this_row": tail.split(";")[0],
                         "a16_substance": next(r["ruling"] for r in e12["rulings"] if r["class_id"].startswith("A16_"))},
            "WEIGH (A16): a transport verse inside the span is now a licensed rival. The strongest rival stays in the "
            "rejected-alternative field; any further live candidate is disclosed in one clause of device_notes as "
            "weighed and not taken, naming the device. Say what the guard or the stated ground is. No grade moves.")

# ---- ONSET5
txt5 = q8["blast_radius_measured"]["onset_members_already_at_a_row_onset"]
on5 = re.findall(r"(\d+):(\d+) \((P\d\d-\d\d\d)\)", txt5)
if len(on5) != 5:
    raise SystemExit("REFUSED: the ruling's onset list gives %d, not five" % len(on5))
for c, v, rid in on5:
    ref = "Ezek.%s.%s" % (c, v)
    ok, first = in_span(rid, ref)
    if first != (int(c), int(v)) or ref not in A_transport or ref not in D_transport:
        raise SystemExit("REFUSED: onset member %s %s is not the row's first verse or fails a distinct check" % (rid, ref))
    add("ONSET5", rid, {"verse_mt": ref, "tokens_found_by_scan": transport_hits(verses[ref])},
        "MAY (Q8): the onset verse is a transport verse of the counted class; the row may NAME that licensed driver. "
        "Optional: NO_DEFECT is a complete answer where the row already names it or naming adds nothing. No grade "
        "is raised; if you think the limb rises, say so as an observation for the confidence audit.")

# ---- STALE20: a '20' figure for the transport class anywhere in row prose
# a COUNT phrase (never a verse number such as 40:20 or a range such as 46.19-20), with a transport word within 300
# characters; a first probe keyed on any '20' near 'transport' returned 10 hits of which 8 were verse numbers
COUNT20 = re.compile(r"sweep:\s*20\b|(?<![\d:.\-])20[- ]verses?\b|closed 20\b|\btwenty verses\b", re.I)
TRANSPORT = re.compile(r"transport|guided[- ]motion|brought me|led me", re.I)
for rid, r in sorted(rows.items()):
    for f in PROSE:
        t = r.get(f) or ""
        for m in COUNT20.finditer(t):
            win = t[max(0, m.start() - 300):m.end() + 300]
            if TRANSPORT.search(win):
                add("STALE20", rid, {"field": f, "match": m.group(0), "window": win},
                    "The class is 33 verses / 46 occurrences; a '20' figure for it is a stale census claim. Correct "
                    "the figure or show the '20' is not a transport count.")
                break

# ---- ROUTED5: what the step-5 adjudications routed onward that is NOT a #e16 class question - claims measured false
# outside the prose pass and repairs that sit in refs entries the prose pass held read-only. Step 6 is the next author
# batch, so it carries them rather than letting them wait for the close. Each entry travels verbatim.
PID = re.compile(r"P\d\d-\d\d\d")
for h in (1, 2):
    adj = EZ / "author" / "repair2_step5" / ("h%d_adjudication" % h) / "adjudication.json"
    if not adj.is_file():
        if not PROBE:
            raise SystemExit("REFUSED: the step-5 half-%d adjudication has not landed; build with --probe only" % h)
        continue
    for e in json.loads(adj.read_text(encoding="utf-8")).get("routed") or []:
        to = str(e.get("to", "")) if isinstance(e, dict) else str(e)
        if re.match(r"\s*#e16\b", to) and "step 6" not in to.lower() and "next worklist" not in to.lower():
            continue
        text = json.dumps(e, ensure_ascii=False)
        # the adjudicators wrote no destination field; their own kind/class text says where an item belongs. A class
        # question for #e16, an open seam question, or a checker-arm question stays off the author worklist (the #e16
        # collector and the orchestrator's tool queue read it); every concrete repair comes here.
        kind = str(e.get("kind") or e.get("class") or "") if isinstance(e, dict) else ""
        if re.search(r"#e16|open seam question|member cannot see|pinned inputs disagree", kind):
            continue
        for rid in sorted(set(PID.findall(text))):
            if rid in rows:
                items.append({"id": None, "class": "ROUTED5", "row": rid, "fields_hint": list(PROSE) + ["boundary_evidence_refs"],
                              "order": ("ROUTED by the step-5 half-%d adjudication, verbatim below. Make the repair the evidence "
                                        "supports if it is a claim measured false or a refs entry defect on this row; NO_DEFECT "
                                        "with evidence if re-measurement does not reproduce it; STOP if it needs a ruling." % h),
                              "data": {"routed_entry": e, "source": str(adj.relative_to(EZ))}, "status": "PENDING"})

# ---- REG6: register flags on ANY row at build time. After step 5 the member was widened (the referents #e15 Q9(a)
# bars that its selftest had sanctioned), so the flags it newly finds are owed a prose repair in this batch.
sys.path.insert(0, str(EZ / "tools"))
import check_register as CR                                                    # noqa: E402
for rid, r in sorted(rows.items()):
    by_field = {}
    for f in CR.scan_row(r, "build"):
        by_field.setdefault(f["field"], []).append({k: f[k] for k in ("class", "match", "context")})
    for field, fl in sorted(by_field.items()):
        items.append({"id": None, "class": "REG6", "row": rid,
                      "fields_hint": list(PROSE) + (["boundary_evidence_refs"] if field.startswith("boundary_evidence_refs") else []),
                      "order": ("A register flag on %s: state the substance the flagged words point at, name the witness and its "
                                "layers instead of a record, file, list or label, and change no claim." % field),
                      "data": {"field": field, "register_flags": fl}, "status": "PENDING"})

for n, it in enumerate(items, 1):
    it["id"] = "S6-%03d" % n
by_class = {}
for it in items:
    by_class[it["class"]] = by_class.get(it["class"], 0) + 1
out = {"schema": "ezek_repair2_step6_worklist.v1", "probe": PROBE, "rows_sha256": sha(ROWS),
       "distinct_checks": {"transport_inventory_vs_scan_agree": transport_agree,
                           "transport_counts": {"inventory": len(A_transport), "scan": len(D_transport)},
                           "transport_disagreement": sorted(set(A_transport) ^ set(D_transport)),
                           "recognition_agree": recog_agree,
                           "recognition_counts": {k: {"inventory": len(a), "scan": len(d)} for k, (a, d) in recog.items()},
                           "recognition_disagreement": {k: sorted(set(a) ^ set(d)) for k, (a, d) in recog.items()}},
       "ruling_count_check": {"interior_verses_listed": len(found), "weighings": len(weighings),
                              "carried_to_disclosure": [f[:2] for f in disclosure_only],
                              "mapping_tier": "INFERRED from the ruling's wording ('one-verse remainder - DISCLOSURE-device, Q4')"},
       "items_by_class": by_class, "rows_owed": sorted({i["row"] for i in items}), "items": items}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({k: out[k] for k in ("probe", "rows_sha256", "distinct_checks", "ruling_count_check", "items_by_class", "rows_owed")},
                 ensure_ascii=False, indent=1))
print("worklist:", OUT, "sha256:", sha(OUT))
