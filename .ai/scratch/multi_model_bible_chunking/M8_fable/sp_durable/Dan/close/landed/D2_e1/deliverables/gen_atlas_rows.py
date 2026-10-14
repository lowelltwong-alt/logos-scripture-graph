#!/usr/bin/env python3
"""Build Daniel's atlas candidate rows and the dimensions record the shared feed cannot hold.

CLOSE-GATE ITEM 22. Two outputs, from pinned inputs only (every input digest is a constant verified here):

  atlas_candidate_feed_rows.jsonl   one row per final row graded low or medium_low, in the 16 fields of the shared
                                    atlas feed, nothing added. Merging is the owner's act; this tool never touches
                                    the shared feed and never reads it (it is not a pinned input of this build, so
                                    the 16 field names are held here as a constant).
  Dan_atlas_dimensions.v1.jsonl     four kinds of record, told apart by the field `record`:
                                      header         the input digests and the measured counts
                                      unit           one per final row (all of them, not only the feed rows), with
                                                     MEASURED, DEPENDENCY and JUDGED kept in separate blocks
                                      open_question  one per question carried open (the routed end-review items) or
                                                     raised as unresolved in a landed packet or ruling, each with a
                                                     blast-radius class
                                      linkage        one per pair of units that a landed packet, ruling or routed
                                                     item names together, with the treatment of the two units
                                                     compared and a statement on any difference

SELECTION IS MEASURED: a feed row exists exactly when the final row's recorded confidence is low or medium_low.
No Daniel row is held, so every feed row mirrors its corpus row: candidate_hold_state null, the row's own
review_status, and review_packet_final_state accepted_candidate.

PROSE IS TRANSCRIBED: why_low_confidence carries the row's own sentences, filtered so that no witness bytes (no
Hebrew-block codepoint, no quoted translation), no internal code and no process talk travels.
possible_downstream_risk is COMPOSED from measured dependency facts and is labelled as composed.

LINKAGES ARE CO-MENTION ONLY: a linkage says that a named packet names two units together. It asserts no
similarity. Harvest is by unit id; a cross-reference written only as chapter:verse is not harvested (a limit).

NUMBERING: row spans are on the WEB face; the device inventory and the mark layer are on the MT face. The four
zones are converted with a constant that is checked against the inventory's own numbering sentence.

Usage: gen_atlas_rows.py [--dan-root DIR] [--out-root DIR] [--check]
       --dan-root  where inputs are read (default: the parent of this script's directory)
       --out-root  where outputs are written, under deliverables/ (default: the same as --dan-root)
       --check     rebuilds and compares bytes only, writing nothing; prints DETERMINISTIC: MATCH
No clock, no randomness, no directory scan: every input is a named path or a path read from the manifest.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOOK = "Dan"
PINS = {
    "rows_v1_final.jsonl": "783a0e9ac2c8fe4c942b3b8f7dd65efaefdb28f6fcb55fdde42b500a5c395e09",
    "close/dan_landed_outputs_manifest.v1.json": "316676f61170822036032027b1a635ff7a7ee1ad229318b56a7d267b3a1fe378",
    "fable_end_review/routed_items.v1.jsonl": "42efe601b731e212ba60bc9b19fd9b3199d86e8d5a152bb7571f8e956376b0d6",
    "Dan_oshb.txt": "8424e3630879c53a44530dee0b87e6c1a64f020619a3c3c0ac758a387a33b3a0",
    "Dan_web_clean.txt": "532fc0e391ac63777e1f57303213b3aaef4ce32071bede797a488bfcee5b6cfa",
    "pmarks_Dan.json": "7df2d3054a57ade7b3441883f5601a03e0baeea4ae22c076ed446f268bad7c9b",
    "dan_device_inventory.json": "466d7e6e91a6af396fe9d5e38e1e54fc10272be79229d398283af92168552964",
    "review/dan_controlling_agent_rulings_E1.v1.json": "541e3c1958d0bbf723d1537a0a00f62e16f207bf54d12ec11ae86f7d4bd9da30",
    "review/dan_controlling_agent_rulings_E2.v1.json": "43ae72e748fe1e55be3103e826194672a3b317300ff413d690682697b121f940",
    "review/dan_controlling_agent_rulings_E3.v1.json": "680b621d178e1f1c173204d504131c7c80f0de6a78bfe93dd52a10a060c318c0",
    "review/dan_controlling_agent_rulings_E4.v1.json": "ff21977a7c635f5104c810053f773a5f7c74a03a548bdd39f16d1f04f7adc6e1",
    "review/dan_controlling_agent_rulings_E5.v1.json": "a447f1412ca0e56d7ab55b31ed5c1edd3ce34898b4904a462d5b9b03e702f97d",
    "review/dan_controlling_agent_rulings_E6.v1.json": "d1626dea516a88039fbc6124934994f973b99c7d1e615b4ce435e31feb646759",
    "review/dan_controlling_agent_rulings_E7.v1.json": "0648ec2988fac5d25cb48026bf0ff4268674910c2c62dd684435b2bf8fbca9ef",
    "review/dan_controlling_agent_rulings_E8.v1.json": "2e1877aa81f32b6e35d0154b5e196cc33393fe24c18a0c850cb38570b851f42c",
    "review/dan_controlling_agent_rulings_E9.v1.json": "73a482ab17232319f3c4384cd57d56f5207423953538f1b56db12947605f7e13",
    "review/dan_controlling_agent_rulings_E10.v1.json": "ef7a3e0028eca463fbe011e5c166b6ea38d825ded7abd12fc1a832413db9b85d",
    "review/dan_controlling_agent_rulings_E11.v1.json": "54c547cdec3fe96e2a3ba000326c801e87dcd0c306bf21d3bd5cc6e141c71fc8",
    "review/dan_controlling_agent_rulings_E12.v1.json": "8bc16d34306a990deeb39637e6314b5465da6865dbd647fb4b456a905a2285e1",
}
RULING_NUMBERS = tuple(range(1, 13))
# The review packets, chosen from the manifest of landed outputs by file name. Final messages are never opened.
PACKET_NAME = re.compile(r"^(?:rev_(?:LF|OL)_c\d\d|peer_g\d\d|p13_(?:OS|TB)|p13r7_(?:OS|TB)|rr(?:8|9|10)_(?:OS|TB)"
                         r"|dan_boss_audit\.v1|dan_boss_audit_b8_b14)\.json$")
FEED_KEYS = ["model_id", "book", "span", "chunk_decision_id", "confidence", "observed_substrate_signals",
             "review_packet_final_state", "chunk_review_status", "candidate_hold_state", "non_authorizing",
             "concern_type", "why_low_confidence", "possible_downstream_risk", "suggested_reviewer",
             "proposed_atlas_action", "atlas_promotion_authority"]
SELECT = {"low", "medium_low"}
HEB = re.compile("[֐-׿יִ-ﭏ]")
QUOTE = re.compile("[\"“”]")
TOKEN = re.compile(r"\bW\d+-\d+\b|\bW\d+#\d+|\bE\d{1,2}\b|\bS\d-\d+|\bCWO\b|FIXUP|\bP13\b|\bOW-\d+|\.jsonl?\b|\bTRIAGE\b"
                   r"|end review|device item|fix-up|fix round", re.I)
SENT = re.compile(r"(?<=[.;])\s+")
MIN_SENTENCE = 40
ROWREF = re.compile(r"\bW([1-9])-(\d{1,3})\b")
NUMBERING_HEAD = ("MT != WEB in four zones: MT 3:31-33 = WEB 4:1-3; MT 4:1-34 = WEB 4:4-37; MT 6:1 = WEB 5:31; "
                  "MT 6:2-29 = WEB 6:1-28; identity elsewhere")
CAMPAIGN = re.compile(r"\bcampaign\b|method record|other books?\b|every book|cross-book|later books?\b|next book"
                      r"|next generation|validator|toolkit|\bsuite\b|\bschema\b|shared feed|\bEzekiel\b|all books", re.I)
CONVENTION = re.compile(r"\bconvention|\bclass\b|\brules?\b|\bpolicy\b|\bstrategy\b|tier word|tier grammar"
                        r"|vocabulary|every row|all rows|each row|\bcorpus\b|book-wide|whole book|\binventory\b"
                        r"|unit_type|numbering|\bregister\b", re.I)
LIMIT = re.compile(r"single[- ]witness|no lemma|no morphology|NOT_TESTABLE|not testable"
                   r"|cannot be (?:settled|answered|decided|tested|verified|measured)"
                   r"|not (?:in|among) the pinned|outside the pinned|no second witness"
                   r"|witness(?:es)? (?:do|does) not|carries no (?:lemma|morphology|mark)", re.I)
FLAG = re.compile(r"inconsisten|differently|asymmetr|\bunlike\b|not the same|\buneven|\bwhereas\b", re.I)
PAIR_CAP = 6
CLASS_ORDER = ("one_unit", "several_units", "one_book", "campaign_wide")
JUDGED_RULE = ("low confidence 2, medium_low 1; the two blind lanes' verdicts differ 1; any finding of severity medium "
               "or high landed 1; the onset seam does not carry evidence on both faces 1; named by a routed open "
               "question 1; span holds a verse whose chapter differs between the two numberings, or the unit's "
               "language differs from a neighbour's or is mixed 1; high at 4, medium at 2")
STATEMENT_RULE = ("applies only where the two units differ in recorded confidence or unit_type. "
                  "real_distinction/standing_after_controlling_ruling: a controlling ruling entry or routed item that "
                  "names at most %d units names both, and the difference stands in the final rows. "
                  "possible_inconsistency_unruled: no such entry, and a source that names both uses a word of "
                  "divergence. real_distinction/different_recorded_kind: only unit_type differs. "
                  "real_distinction/no_packet_alleges_inconsistency: grades differ, no source that names both uses a "
                  "word of divergence, and the final audit confirmed each row." % PAIR_CAP)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read_pinned(root, rel):
    b = (root / rel).read_bytes()
    if sha(b) != PINS[rel]:
        raise SystemExit("REFUSED: %s moved since it was pinned" % rel)
    return b


def jl(b):
    return [json.loads(l) for l in b.decode("utf-8").splitlines() if l.strip()]


def norm_id(s):
    m = re.match(r"^W(\d+)-(\d{1,3})$", str(s or ""))
    return "W%s-%03d" % (m.group(1), int(m.group(2))) if m else None


def rows_named(text, known):
    return sorted({"W%s-%03d" % (a, int(b)) for a, b in ROWREF.findall(text)} & known)


def flat(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True)


def vref(s):
    m = re.match(r"Dan\.(\d+)\.(\d+)$", s or "")
    return (int(m.group(1)), int(m.group(2))) if m else None


def web_to_mt(cv):
    c, v = cv
    if c == 4:
        return (3, 30 + v) if v <= 3 else (4, v - 3)
    if (c, v) == (5, 31):
        return (6, 1)
    if c == 6:
        return (6, v + 1)
    return (c, v)


def ref(cv):
    return "Dan.%d.%d" % cv


def clean_sentences(text, limit):
    """Sentences of the row's own prose that can travel. Returns (kept, filtered, capped, short).

    filtered: carried witness bytes, a quotation mark, an internal code or process talk. short: under MIN_SENTENCE
    characters (a label, not a reason). capped: usable but past this field's limit. Sentences the row itself marks
    INFERRED are taken first, in their own order: that is where the row says its reading goes beyond the bytes."""
    usable, filtered, short = [], 0, 0
    for s in SENT.split((text or "").replace("\n", " ")):
        s = s.strip()
        if not s:
            continue
        if HEB.search(s) or QUOTE.search(s) or TOKEN.search(s):
            filtered += 1
            continue
        if len(s) < MIN_SENTENCE:
            short += 1
            continue
        usable.append(s if s[-1] in ".;" else s + ".")
    ordered = [s for s in usable if "INFERRED" in s] + [s for s in usable if "INFERRED" not in s]
    return ordered[:limit], filtered, max(0, len(ordered) - limit), short


def blast(text, n_rows, qid):
    camp = sorted({m.group(0).lower() for m in CAMPAIGN.finditer(text)})
    conv = sorted({m.group(0).lower() for m in CONVENTION.finditer(text + " " + qid)})
    if qid.startswith("routed:") and not ROWREF.search(qid):
        conv.append("routed id names no unit")
    if camp:
        cls = "campaign_wide"
    elif conv or n_rows == 0 or n_rows >= 8:
        cls = "one_book"
    elif n_rows >= 2:
        cls = "several_units"
    else:
        cls = "one_unit"
    return cls, camp, conv


def build(dan_root):
    m8 = dan_root.parent.parent
    rows = jl(read_pinned(dan_root, "rows_v1_final.jsonl"))
    order = sorted(rows, key=lambda r: r["chunk_index_in_book"])
    known = {r["decision_id"] for r in rows}
    by_id = {r["decision_id"]: r for r in rows}
    cid = {r["decision_id"]: "M8-%s-%03d" % (BOOK, r["chunk_index_in_book"]) for r in rows}
    inv = json.loads(read_pinned(dan_root, "dan_device_inventory.json").decode("utf-8"))
    if not str(inv.get("numbering", "")).startswith(NUMBERING_HEAD) or inv.get("numbering_face") != "MT":
        raise SystemExit("REFUSED: the device inventory's numbering sentence is not the one this tool converts by")
    pm = json.loads(read_pinned(dan_root, "pmarks_Dan.json").decode("utf-8"))
    marks = pm["marks"]

    # the two witnesses: verse sets and sizes
    mt_words = {}
    for line in read_pinned(dan_root, "Dan_oshb.txt").decode("utf-8").splitlines():
        k, _, t = line.partition("\t")
        if vref(k):
            mt_words[vref(k)] = len(t.split())
    web_verses, ch = [], None
    for line in read_pinned(dan_root, "Dan_web_clean.txt").decode("utf-8").splitlines():
        m = re.match(r"===== DAN (\d+) =====", line)
        if m:
            ch = int(m.group(1))
            continue
        m = re.match(r"\[v\] (\d+)\b", line)
        if m and ch:
            web_verses.append((ch, int(m.group(1))))
    web_pos = {cv: i for i, cv in enumerate(web_verses)}

    # device map on the MT face: every inventory list that names a verse as carrying a counted device
    dev = {}

    def add(v, key):
        if vref(v):
            dev.setdefault(vref(v), set()).add(key)
    for v in inv["datelines"]["verses_mt"]:
        add(v, "dateline")
    for v in inv["calendar_dates_not_datelines"]["verses_mt"]:
        add(v, "calendar_date")
    for key in sorted(inv["formulae"]):
        for v in inv["formulae"][key].get("verses_mt") or []:
            add(v, key)
    for s in inv["language_switches"]:
        add(s["mt"], "language_switch")

    # the packets, by manifest
    man = json.loads(read_pinned(dan_root, "close/dan_landed_outputs_manifest.v1.json").decode("utf-8"))
    packets = []
    for o in sorted(man["outputs"], key=lambda o: o["path"]):
        name = o["path"].split("/")[-1]
        if name.startswith("final_message") or not PACKET_NAME.match(name):
            continue
        b = (m8 / o["path"]).read_bytes()
        if sha(b) != o["sha256"]:
            raise SystemExit("REFUSED: %s does not match the manifest of landed outputs" % o["path"])
        packets.append((name, o["path"], o["sha256"], json.loads(b.decode("utf-8"))))
    rulings = []
    for n in RULING_NUMBERS:
        rel = "review/dan_controlling_agent_rulings_E%d.v1.json" % n
        rulings.append(("E%d" % n, "sp_durable/Dan/" + rel, PINS[rel], json.loads(read_pinned(dan_root, rel).decode("utf-8"))))
    routed = jl(read_pinned(dan_root, "fable_end_review/routed_items.v1.jsonl"))

    # per-unit packet measurements
    prim = {r: {} for r in known}
    peer = {}
    rounds = {r: {"supports": 0, "challenges": 0, "extra_findings": 0} for r in known}
    audit = {}
    sev = {r: {"high": 0, "medium": 0, "low": 0} for r in known}
    item_links = []  # (row, other, packet path, locator, flagged)

    def land(r, s):
        if s in ("high", "medium", "low"):
            sev[r][s] += 1

    def harvest(r, obj, path, loc):
        t = flat(obj)
        for x in rows_named(t, known):
            if x != r:
                item_links.append((r, x, path, loc, bool(FLAG.search(t))))
    for name, path, _digest, d in packets:
        if name.startswith("rev_"):
            lane = name[4:6]
            for i, it in enumerate(d.get("items") or []):
                r = norm_id(it.get("row_id"))
                if r not in known:
                    continue
                prim[r].setdefault(lane, []).append({"cluster": d.get("cluster"), "verdict": it.get("verdict"),
                                                     "severity": it.get("severity")})
                if it.get("verdict") == "challenge":
                    land(r, it.get("severity"))
                harvest(r, it, path, "items[%d]" % i)
        elif name.startswith("peer_"):
            for i, it in enumerate(d.get("items") or []):
                r = norm_id(it.get("row_id"))
                if r not in known:
                    continue
                states = {}
                for f in it.get("primary_findings") or []:
                    k = "%s:%s" % (f.get("severity"), f.get("state"))
                    states[k] = states.get(k, 0) + 1
                peer[r] = {"group": d.get("peer_group"), "lanes_disagreed": it.get("lanes_disagreed"),
                           "primary_findings_by_severity_and_state": dict(sorted(states.items())),
                           "proposes_span_change": it.get("proposed_span_change") is not None,
                           "proposes_confidence_change": it.get("proposed_confidence_change") is not None,
                           "proposes_text_change": it.get("proposed_text_change") is not None,
                           "proposal_severity": it.get("proposal_severity")}
                harvest(r, it, path, "items[%d]" % i)
        elif name.startswith("dan_boss_audit.v1"):
            for i, it in enumerate(d.get("rows") or []):
                r = norm_id(it.get("row"))
                if r not in known:
                    continue
                audit[r] = {"verdict": it.get("verdict"), "findings": len(it.get("findings") or [])}
                for f in it.get("findings") or []:
                    land(r, f.get("severity"))
                harvest(r, it, path, "rows[%d]" % i)
        else:
            for key in ("items", "extra_findings"):
                for i, it in enumerate(d.get(key) or []):
                    r = norm_id(it.get("row"))
                    if r not in known:
                        continue
                    if key == "extra_findings":
                        rounds[r]["extra_findings"] += 1
                        land(r, it.get("severity"))
                    elif it.get("verdict") == "challenge":
                        rounds[r]["challenges"] += 1
                        land(r, it.get("severity"))
                    else:
                        rounds[r]["supports"] += 1
                    harvest(r, it, path, "%s[%d]" % (key, i))

    # open questions
    questions = []

    def question(qid, kind, path, locator, text, state):
        named = rows_named(text, known)
        cls, camp, conv = blast(text, len(named), qid)
        first, _f, _c, _s = clean_sentences(text, 1)
        questions.append({
            "schema": "dan_atlas_dimensions.v1", "record": "open_question", "question_id": qid, "kind": kind,
            "source": {"path": path, "locator": locator, "tier": "EXTRACTED"},
            "state": state, "text_sha256": sha(text.encode("utf-8")),
            "first_sentence_that_can_travel": first[0] if first else None,
            "measured": {"units_named": named, "units_named_count": len(named),
                         "parents_named": sorted({by_id[r]["parent_collection"].split(" ")[0] for r in named}),
                         "convention_words": conv, "campaign_words": camp,
                         "states_a_witness_limit": bool(LIMIT.search(text))},
            "blast_radius": {"class": cls, "tier": "JUDGED_BY_RULE",
                             "rule": "campaign_wide if a campaign word occurs; else one_book if a convention word "
                                     "occurs (a routed item whose id names no unit counts as one), or no unit is "
                                     "named, or eight or more are; else several_units if two "
                                     "or more units are named; else one_unit. A question with a convention word is "
                                     "never one_unit.",
                             "not_a_measurement": "The class is assigned by the stated rule over the measured "
                                                  "fields above. No one re-read the question to produce it."}})
        return named, text
    q_named = {}
    for it in routed:
        text = " ".join(str(it.get(k) or "") for k in ("order", "decision"))
        q_named["routed:" + it["id"]] = question(
            "routed:" + it["id"], "routed_end_review_item", "sp_durable/Dan/fable_end_review/routed_items.v1.jsonl",
            "id=" + it["id"], text, "carried open to the end review (ruling word on record: %s)" % it.get("ruling"))
    for name, path, _digest, d in packets + rulings:
        for i, u in enumerate(d.get("unresolved_uncertainty") or []):
            text = " ".join(str(u.get(k) or "") for k in ("what", "why_it_matters")) if isinstance(u, dict) else str(u)
            qid = "%s#unresolved[%d]" % (name[:-5] if name.endswith(".json") else name, i)
            q_named[qid] = question(qid, "unresolved_in_ruling" if name.startswith("E") and name[1:].isdigit()
                                    else "unresolved_in_packet", path, "unresolved_uncertainty[%d]" % i, text,
                                    "raised as unresolved by its author; its later disposition is not derived here")
    questions.sort(key=lambda q: q["question_id"])
    q_by_row = {r: [] for r in known}
    for q in questions:
        for r in q["measured"]["units_named"]:
            q_by_row[r].append(q)

    # ruling entries (for the statement rule and for linkage)
    ruled_sets = []  # (label, units named, path)
    for name, path, _digest, d in rulings:
        for e in d.get("rulings") or []:
            ruled_sets.append(("%s:%s" % (name, e.get("id")), rows_named(flat(e), known), path, flat(e)))
    for it in routed:
        ruled_sets.append(("routed:" + it["id"], q_named["routed:" + it["id"]][0],
                           "sp_durable/Dan/fable_end_review/routed_items.v1.jsonl", q_named["routed:" + it["id"]][1]))

    # linkages: co-mention only
    links = {}

    def link(a, b, kind, path, loc, flagged):
        if a == b:
            return
        k = tuple(sorted((a, b)))
        links.setdefault(k, {})[(kind, path, loc)] = flagged or links.get(k, {}).get((kind, path, loc), False)
    for r, x, path, loc, flagged in item_links:
        link(r, x, "named_inside_a_review_item_on_the_other_unit", path, loc, flagged)
    for q in questions:
        named = q["measured"]["units_named"]
        if 2 <= len(named) <= PAIR_CAP:
            fl = bool(FLAG.search(q_named[q["question_id"]][1]))
            for i, a in enumerate(named):
                for b in named[i + 1:]:
                    link(a, b, "named_together_in_an_open_question", q["source"]["path"], q["question_id"], fl)
    for label, named, path, text in ruled_sets:
        if label.startswith("routed:"):
            continue
        if 2 <= len(named) <= PAIR_CAP:
            for i, a in enumerate(named):
                for b in named[i + 1:]:
                    link(a, b, "named_together_in_a_controlling_ruling", path, label, bool(FLAG.search(text)))
    link_recs, partners = [], {r: set() for r in known}
    for (a, b) in sorted(links):
        ra, rb = by_id[a], by_id[b]
        srcs = [{"kind": k, "path": p, "locator": loc, "uses_a_word_of_divergence": fl, "tier": "EXTRACTED"}
                for (k, p, loc), fl in sorted(links[(a, b)].items())]
        differs = [f for f in ("confidence", "unit_type") if ra[f] != rb[f]]
        ruled_by = sorted(label for label, named, _p, _t in ruled_sets
                          if a in named and b in named and len(named) <= PAIR_CAP)
        flagged = any(s["uses_a_word_of_divergence"] for s in srcs)
        if not differs:
            st = {"verdict": "same_treatment", "basis": "recorded confidence and unit_type are equal"}
        elif ruled_by:
            st = {"verdict": "real_distinction", "basis": "standing_after_controlling_ruling",
                  "ruling_entries_naming_both": ruled_by,
                  "carried_to_end_review_under": [x for x in ruled_by if x.startswith("routed:")]}
        elif flagged:
            st = {"verdict": "possible_inconsistency_unruled",
                  "basis": "a source that names both units uses a word of divergence, and no controlling ruling "
                           "entry of %d units or fewer names both" % PAIR_CAP}
        elif differs == ["unit_type"]:
            st = {"verdict": "real_distinction", "basis": "different_recorded_kind"}
        else:
            st = {"verdict": "real_distinction", "basis": "no_packet_alleges_inconsistency",
                  "final_audit_verdicts": [audit.get(a, {}).get("verdict"), audit.get(b, {}).get("verdict")]}
        st.update({"tier": "JUDGED_BY_RULE", "rule": STATEMENT_RULE,
                   "not_a_measurement": "Assigned by the stated rule. No one re-read the two passages to produce it."})
        partners[a].add(b)
        partners[b].add(a)
        link_recs.append({
            "schema": "dan_atlas_dimensions.v1", "record": "linkage", "pair": [a, b],
            "chunk_decision_ids": [cid[a], cid[b]], "spans": [ra["span"], rb["span"]],
            "asserts": "co-mention only: the sources below name both units; no similarity is asserted here",
            "sources": srcs,
            "treatment": {"confidence": [ra["confidence"], rb["confidence"]],
                          "unit_type": [ra["unit_type"], rb["unit_type"]],
                          "parent_collection": [ra["parent_collection"], rb["parent_collection"]],
                          "in_feed": [ra["confidence"] in SELECT, rb["confidence"] in SELECT], "tier": "MEASURED"},
            "treated_differently": bool(differs), "differs_in": differs, "statement": st})

    # units
    parent_n = {}
    for r in rows:
        parent_n[r["parent_collection"]] = parent_n.get(r["parent_collection"], 0) + 1
    ends = {}
    for r in order:
        a, _, b = r["span"].partition("-")
        ends[r["decision_id"]] = (vref(a), vref(b))

    def seam(left_row, right_row):
        if left_row is None or right_row is None:
            return {"book_edge": True, "left_face": None, "right_face": None, "evidence_on_both_faces": None}
        lv, rv = web_to_mt(ends[left_row["decision_id"]][1]), web_to_mt(ends[right_row["decision_id"]][0])
        left = {"verse_mt": ref(lv), "section_mark_after": list(marks.get(ref(lv)) or []),
                "devices_at_verse": sorted(dev.get(lv, ()))}
        right = {"verse_mt": ref(rv), "devices_at_verse": sorted(dev.get(rv, ()))}
        lo, ro = bool(left["section_mark_after"] or left["devices_at_verse"]), bool(right["devices_at_verse"])
        return {"book_edge": False, "left_face": left, "right_face": right, "evidence_on_left_face": lo,
                "evidence_on_right_face": ro, "evidence_on_both_faces": lo and ro}
    feed, units = [], []
    stats = {"sentences_kept": 0, "filtered": 0, "capped": 0, "short": 0, "fallback": 0}
    for i, r in enumerate(order):
        rid, span = r["decision_id"], r["span"]
        prev_r, next_r = (order[i - 1] if i else None), (order[i + 1] if i + 1 < len(order) else None)
        (w1, w2) = ends[rid]
        span_web = web_verses[web_pos[w1]:web_pos[w2] + 1]
        span_mt = [web_to_mt(cv) for cv in span_web]
        chapter_divergent = any(m[0] != w[0] for m, w in zip(span_mt, span_web))
        offset_zone = any(m != w for m, w in zip(span_mt, span_web))
        lang_seam = r["language"] == "mixed" or any(n is not None and n["language"] != r["language"]
                                                    for n in (prev_r, next_r))
        onset, close = seam(prev_r, r), seam(r, next_r)
        lanes = {k: v for k, v in sorted(prim[rid].items())}
        lf = sorted({x["verdict"] for x in lanes.get("LF", [])})
        ol = sorted({x["verdict"] for x in lanes.get("OL", [])})
        verdicts_differ = bool(lf and ol and lf != ol)
        qs = q_by_row[rid]
        routed_ids = [q["question_id"] for q in qs if q["kind"] == "routed_end_review_item"]
        limit_ids = [q["question_id"] for q in qs if q["measured"]["states_a_witness_limit"]]
        widest = max([CLASS_ORDER.index(q["blast_radius"]["class"]) for q in qs], default=None)
        if limit_ids:
            ans = "a_witness_limit_is_stated"
        elif onset["evidence_on_both_faces"] or (onset["book_edge"] and dev.get(span_mt[0])):
            ans = "seam_evidence_present_in_the_witness_layers"
        else:
            ans = "left_out"
        feat = {"zone": chapter_divergent, "lang": lang_seam, "contested": verdicts_differ,
                "one_face": onset["evidence_on_both_faces"] is False, "routed": bool(routed_ids)}
        concern = ("numbering_zone_seam" if feat["zone"] else "language_seam" if feat["lang"] else
                   "contested_between_lanes" if feat["contested"] else
                   "seam_evidence_on_one_face_or_none" if feat["one_face"] else
                   "open_question_carried" if feat["routed"] else "reading_rests_on_prose")
        classes = []
        if chapter_divergent:
            classes.append("numbering_chapter_divergence")
        elif offset_zone:
            classes.append("numbering_offset_zone")
        if lang_seam:
            classes.append("language_seam")
        if parent_n[r["parent_collection"]] > 1:
            classes.append("shared_frame")
        nb = [n["span"] for n in (prev_r, next_r) if n is not None]
        if nb:
            classes.append("shared_seam")
        if widest is not None and widest >= 2:
            classes.append("convention_reach")
        if partners[rid]:
            classes.append("linked_units")
        risk = []
        if chapter_divergent:
            risk.append("This unit holds a verse whose chapter differs between the two numberings, so every "
                        "reference into it must carry both witnesses' numbers.")
        elif offset_zone:
            risk.append("This unit lies where the two numberings differ by a verse offset, so every reference into "
                        "it must carry both witnesses' numbers.")
        if lang_seam:
            risk.append("It stands at a change of language, or holds one.")
        if len(nb) == 1:
            risk.append("It shares a seam with the adjacent unit at %s, so moving that boundary moves two units." % nb[0])
        elif nb:
            risk.append("It shares seams with the adjacent units at %s, so moving either boundary moves two units."
                        % " and ".join(nb))
        n_sib = parent_n[r["parent_collection"]] - 1
        if n_sib:
            risk.append("It sits inside a frame shared with %d other unit%s of this book."
                        % (n_sib, "" if n_sib == 1 else "s"))
        if qs:
            risk.append("%d open question%s on record name%s it, the widest of them classed %s."
                        % (len(qs), "" if len(qs) == 1 else "s", "s" if len(qs) == 1 else "",
                           CLASS_ORDER[widest].replace("_", " ")))
        if partners[rid]:
            risk.append("The review record names it together with %d other unit%s."
                        % (len(partners[rid]), "" if len(partners[rid]) == 1 else "s"))
        sev_any_mh = bool(sev[rid]["high"] or sev[rid]["medium"])
        score = ({"low": 2, "medium_low": 1}.get(r["confidence"], 0) + (1 if verdicts_differ else 0)
                 + (1 if sev_any_mh else 0) + (1 if onset["evidence_on_both_faces"] is False else 0)
                 + (1 if routed_ids else 0) + (1 if (chapter_divergent or lang_seam) else 0))
        in_feed = r["confidence"] in SELECT
        derivation = None
        if in_feed:
            parts, filt_n, cap_n, short_n = clean_sentences(r.get("device_notes"), 2)
            n_notes = len(parts)
            alt, filt_a, cap_a, short_a = clean_sentences(r.get("strongest_rejected_alternative"), 1)
            if alt and alt[0] not in parts:
                parts.append("Recorded alternative: " + alt[0])
            why = " ".join(parts).strip()
            fallback = not why
            if fallback:
                why = ("Recorded at %s confidence for %s; every sentence of the row's own reason carries witness "
                       "bytes, a quotation or an internal code, which this deliverable does not transcribe."
                       % (r["confidence"], span))
            stats["sentences_kept"] += 0 if fallback else len(parts)
            stats["filtered"] += filt_n + filt_a
            stats["capped"] += cap_n + cap_a
            stats["short"] += short_n + short_a
            stats["fallback"] += fallback
            derivation = {
                "why_low_confidence_source_fields": [f for f, n in (("device_notes", n_notes),
                                                                    ("strongest_rejected_alternative",
                                                                     len(parts) - n_notes)) if n],
                "sentences_kept": 0 if fallback else len(parts),
                "sentences_filtered": filt_n + filt_a, "sentences_too_short_to_be_a_reason": short_n + short_a,
                "sentences_usable_but_over_cap": cap_n + cap_a, "composed_not_derived": fallback,
                "filter": "filtered means the sentence carries a Hebrew-block codepoint, a double quotation mark, an "
                          "internal code or process talk; too short means under %d characters; over cap means usable "
                          "but past the limit of 2 sentences from device_notes and 1 from "
                          "strongest_rejected_alternative; sentences the row marks INFERRED are taken first"
                          % MIN_SENTENCE}
            feed.append({
                "model_id": "M8_fable", "book": BOOK, "span": span, "chunk_decision_id": cid[rid],
                "confidence": r["confidence"],
                "observed_substrate_signals": list(r.get("observed_substrate_signals") or []),
                "review_packet_final_state": "accepted_candidate",
                "chunk_review_status": r["review_status"],
                "candidate_hold_state": r["candidate_hold_state"],
                "non_authorizing": True, "concern_type": concern, "why_low_confidence": why,
                "possible_downstream_risk": " ".join(risk) or None,
                "suggested_reviewer": ("human_owner" if feat["zone"] else
                                       "convergence" if (feat["contested"] or feat["routed"]) else
                                       "literary_form_reviewer"),
                "proposed_atlas_action": "consider_only", "atlas_promotion_authority": "none"})
        units.append({
            "schema": "dan_atlas_dimensions.v1", "record": "unit", "chunk_decision_id": cid[rid],
            "internal_decision_id": rid, "writer_decision_id": r["writer_decision_id"], "span": span,
            "in_feed": in_feed,
            "measured": {
                "tier": "MEASURED by this tool over the pinned records, except where a field says REPORTED",
                "confidence_recorded": r["confidence"], "review_status_recorded": r["review_status"],
                "candidate_hold_state_recorded": r["candidate_hold_state"], "unit_type": r["unit_type"],
                "parent_collection": r["parent_collection"], "language": r["language"],
                "signals": list(r.get("observed_substrate_signals") or []),
                "span_mt": "%s-%s" % (ref(span_mt[0]), ref(span_mt[-1])),
                "verses": len(span_web), "words_mt": sum(mt_words[m] for m in span_mt),
                "holds_a_verse_whose_chapter_differs_between_numberings": chapter_divergent,
                "in_numbering_offset_zone": offset_zone, "at_or_holding_a_language_change": lang_seam,
                "contested_between_blind_lanes": {
                    "verdicts_differ": verdicts_differ, "lanes": lanes,
                    "peer_reports_lanes_disagreed": (peer.get(rid) or {}).get("lanes_disagreed"),
                    "peer_tier": "REPORTED (the reconciling reader's own flag)"},
                "severities_landed": dict(sev[rid]),
                "severities_landed_counts": "challenges by either blind lane, challenges and extra findings of the "
                                            "later review rounds, and findings of the final audit; the reconciling "
                                            "reader restates the blind lanes' findings and is not counted twice",
                "peer_reconciliation": peer.get(rid), "later_review_rounds": rounds[rid],
                "final_audit": dict(audit.get(rid) or {}, tier="REPORTED"),
                "seam_evidence": {"onset": onset, "close": close,
                                  "note": "presence of a section mark or of a device the inventory counts at the "
                                          "verse; presence is not strength, and several counted devices are weak "
                                          "connectives"},
                "answerable_from_the_witnesses": {
                    "value": ans, "open_questions_stating_a_witness_limit": limit_ids,
                    "left_out_means": "no packet states a witness limit for this unit and its onset seam does not "
                                      "carry evidence on both faces, so nothing here derives an answer; the rating "
                                      "is left out rather than guessed"},
            },
            "derivation": derivation,
            "dependency": {"classes": classes, "neighbour_spans": nb,
                           "units_sharing_this_frame": parent_n[r["parent_collection"]],
                           "open_questions_naming_this_unit": [q["question_id"] for q in qs],
                           "routed_open_questions_naming_this_unit": routed_ids,
                           "widest_blast_radius_class": CLASS_ORDER[widest] if widest is not None else None,
                           "linked_units": sorted(partners[rid]),
                           "composed_sentence_in_feed": (" ".join(risk) or None) if in_feed else None},
            "judged": {"tier": "JUDGED_BY_RULE", "atlas_hardness": "high" if score >= 4 else
                       "medium" if score >= 2 else "low", "score": score, "rule": JUDGED_RULE,
                       "risk_rating": None,
                       "risk_rating_left_out": "no packet rates risk for a unit, so no risk rating is derived here",
                       "not_a_measurement": "This rating is assigned by the stated rule over measured inputs. No "
                                            "one re-read the passage to produce it."}})
    diff = [l for l in link_recs if l["treated_differently"]]
    header = {
        "schema": "dan_atlas_dimensions.v1", "record": "header", "book": BOOK,
        "inputs_sha256": dict(sorted(PINS.items())),
        "packets_read": [{"path": p, "sha256": d} for _n, p, d, _j in packets],
        "counts": {
            "final_rows": len(rows), "feed_rows": len(feed),
            "feed_rows_by_confidence": {c: sum(1 for f in feed if f["confidence"] == c) for c in ("low", "medium_low")},
            "units_contested_between_blind_lanes": sum(1 for u in units if u["measured"]["contested_between_blind_lanes"]["verdicts_differ"]),
            "open_questions": len(questions),
            "open_questions_by_kind": {k: sum(1 for q in questions if q["kind"] == k)
                                       for k in ("routed_end_review_item", "unresolved_in_packet", "unresolved_in_ruling")},
            "open_questions_by_blast_radius": {c: sum(1 for q in questions if q["blast_radius"]["class"] == c) for c in CLASS_ORDER},
            "linkages": len(link_recs), "linkages_treated_differently": len(diff),
            "statements": {k: sum(1 for l in link_recs if l["statement"]["verdict"] + "/" + l["statement"].get("basis", "")[:40] == k)
                           for k in sorted({l["statement"]["verdict"] + "/" + l["statement"].get("basis", "")[:40] for l in link_recs})},
            "hardness": {h: sum(1 for u in units if u["judged"]["atlas_hardness"] == h) for h in ("high", "medium", "low")},
            "why_low_confidence": stats},
        "tier": "MEASURED: every count is produced by this tool"}
    return feed, [header] + units + questions + link_recs, rows


def dump(objs):
    return "".join(json.dumps(o, ensure_ascii=False) + "\n" for o in objs).encode("utf-8")


def roots(argv):
    dan_root = HERE.parent
    out_root = None
    for flag in ("--dan-root", "--out-root"):
        if flag in argv:
            v = Path(argv[argv.index(flag) + 1])
            if flag == "--dan-root":
                dan_root = v
            else:
                out_root = v
    return dan_root, (out_root or dan_root)


def main():
    dan_root, out_root = roots(sys.argv)
    feed, dims, rows = build(dan_root)
    out_rows = out_root / "deliverables" / "atlas_candidate_feed_rows.jsonl"
    out_dim = out_root / "deliverables" / "Dan_atlas_dimensions.v1.jsonl"
    a, b = dump(feed), dump(dims)
    if "--check" in sys.argv:
        ok = True
        for p, data in ((out_rows, a), (out_dim, b)):
            on = sha(p.read_bytes()) if p.is_file() else "ABSENT"
            ok = ok and on == sha(data)
            print("%-34s on_disk %s  rebuilt %s" % (p.name, on[:12], sha(data)[:12]))
        print("DETERMINISTIC: MATCH" if ok else "DIFFERS")
        sys.exit(0 if ok else 1)
    out_rows.write_bytes(a)
    out_dim.write_bytes(b)
    print(json.dumps(dims[0]["counts"], indent=1))
    print("concern types        %s" % json.dumps({c: sum(1 for f in feed if f["concern_type"] == c)
                                                  for c in sorted({f["concern_type"] for f in feed})}))
    print("%-34s %d bytes  sha256 %s" % (out_rows.name, len(a), sha(a)))
    print("%-34s %d bytes  sha256 %s" % (out_dim.name, len(b), sha(b)))


if __name__ == "__main__":
    main()
