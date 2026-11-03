#!/usr/bin/env python3
"""Build a book's atlas candidate rows and the dimensions record the shared feed cannot hold.

CLOSE-GATE ITEM 22. Book-agnostic: every book-specific name, path, digest, count and word list lives in
book_params.v1.json; this script holds none. Two outputs, from pinned inputs only:

  <feed file>        one row per final row graded low or medium_low, in the 16 fields of the shared atlas feed,
                     nothing added. Merging is the owner's act; this tool never touches the shared feed and never
                     reads it (it is not a pinned input, so the 16 field names are a form constant in the parameters).
  <dimensions file>  four kinds of record, told apart by the field `record`:
                       header         the input digests and the measured counts
                       unit           one per final row (all of them), with MEASURED, DEPENDENCY and JUDGED kept in
                                      separate blocks
                       open_question  one per question carried open: routed end-review items, packet and ruling
                                      unresolved entries, packet escalations, inventory items for the end review,
                                      findings routed to the end review with no routed id, and strategy lines that
                                      send a question to the end review; each with a blast-radius class
                       linkage        one per pair of units a landed source names together, or that a reviewer ties
                                      together with a chapter:verse cross-reference, with the treatment of the two
                                      units compared and a statement on any difference

SELECTION IS MEASURED: a feed row exists exactly when the final row's recorded confidence is in the selected set.
STATE IS DERIVED PER ROW: candidate_hold_state and chunk_review_status mirror the row. review_packet_final_state is
derived per row from the row's review status, its hold and the verdict of the last audit that read it, never assumed.
PROSE IS TRANSCRIBED: why_low_confidence carries the row's own sentences, filtered so that no witness bytes, quoted
translation, internal code or process talk travels. possible_downstream_risk is COMPOSED from measured dependency facts.
LINKAGES ARE CO-MENTION ONLY: a linkage says that a named source names two units together, by unit id or by a
chapter:verse reference the reviewer wrote. It asserts no similarity. A reference to an adjacent unit is the seam under
review, not a cross-reference, and is not harvested.
NUMBERING: row spans are on the numbering face the inventory declares. Any zone in the parameters is converted with
that constant, checked against the inventory's own numbering sentence. An empty zone list means identity.

Usage: gen_atlas_rows.py [--params FILE] [--book-root DIR] [--out-root DIR] [--check]
       --params     default: book_params.v1.json beside this script
       --book-root  where inputs are read (default: the parent of this script's directory)
       --out-root   where outputs are written, under deliverables/ (default: the same as --book-root)
       --check      rebuilds and compares bytes only, writing nothing; prints DETERMINISTIC: MATCH
No clock, no randomness, no directory scan: every input is a named path or a path read from the manifest.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLASS_ORDER = ("one_unit", "several_units", "one_book", "campaign_wide")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def flat(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True)


def jl(b):
    return [json.loads(l) for l in b.decode("utf-8").splitlines() if l.strip()]


class Book:
    """The parameters with their patterns compiled. Holds no book-specific value of its own."""

    def __init__(self, P):
        self.P = P
        self.name = P["book"]
        self.select = set(P["select_confidence"])
        self.bad_bytes = re.compile(P["witness_bytes_regex"])
        self.quote = re.compile(P["quote_regex"])
        self.token = re.compile(P["internal_token_regex"], re.I)
        self.sent = re.compile(P["sentence_split_regex"])
        self.fragment = re.compile(P["sentence_fragment_regex"])
        self.chap = re.compile(P["chapter_ref_regex"], re.I)
        self.min_sentence = P["min_sentence"]
        self.rowref = re.compile(P["row_ref_regex"])
        self.rowrange = re.compile(P["row_range_regex"])
        self.rowfull = re.compile(P["row_id_full_regex"])
        self.verse = re.compile(r"^%s\.(\d+)\.(\d+)$" % re.escape(P["verse_prefix"]))
        self.cref = re.compile(P["crossref_regex"])
        self.other_book = re.compile(P["crossref_other_book_regex"])
        self.campaign = re.compile(P["campaign_regex"], re.I)
        self.convention = re.compile(P["convention_regex"], re.I)
        self.limit = re.compile(P["limit_regex"], re.I)
        self.flag = re.compile(P["divergence_regex"], re.I)
        self.pair_cap = P["pair_cap"]
        self.serious = set(P["severity_words_counting_for_judged"])
        self.judged_rule = (
            "low confidence 2, medium_low 1; any two blind lanes' verdicts differ 1; any finding of severity %s landed "
            "1; the onset seam does not carry evidence on both faces 1; named by a routed open question 1; span holds "
            "a verse whose chapter differs between the numberings, or the unit's language differs from a neighbour's "
            "or is mixed 1; high at %d, medium at %d"
            % ("/".join(P["severity_words_counting_for_judged"]), P["judged_high_at"], P["judged_medium_at"]))
        self.statement_rule = (
            "applies only where the two units differ in recorded confidence or unit_type. "
            "real_distinction/standing_after_controlling_ruling: a controlling ruling entry or routed item that "
            "names at most %d units names both, and the difference stands in the final rows. "
            "possible_inconsistency_unruled: no such entry, and a source that names both uses a word of divergence. "
            "real_distinction/different_recorded_kind: only unit_type differs. "
            "real_distinction/no_packet_alleges_inconsistency: grades differ, no source that names both uses a word "
            "of divergence, and the last audit confirmed each row." % self.pair_cap)

    def read_pinned(self, root, rel):
        b = (root / rel).read_bytes()
        if sha(b) != self.P["pins"][rel]:
            raise SystemExit("REFUSED: %s moved since it was pinned" % rel)
        return b

    def vref(self, s):
        m = self.verse.match(s or "")
        return (int(m.group(1)), int(m.group(2))) if m else None

    def ref(self, cv):
        return "%s.%d.%d" % (self.P["verse_prefix"], cv[0], cv[1])

    def fmt(self, a, b):
        return self.P["row_id_format"] % (a, int(b))

    def norm_id(self, s):
        m = self.rowfull.match(str(s or ""))
        return self.fmt(m.group(1), m.group(2)) if m else None

    def rows_named(self, text, known):
        out = {self.fmt(a, b) for a, b in self.rowref.findall(text)}
        for a, b, c, d in self.rowrange.findall(text):
            if a == c and int(b) <= int(d):
                out |= {self.fmt(a, i) for i in range(int(b), int(d) + 1)}
        return sorted(out & known)

    def to_primary(self, cv):
        """Numbering face to primary witness. Zones are {chapter, from_verse, to_verse, to_chapter, verse_offset}."""
        c, v = cv
        for z in self.P["numbering"]["zones"]:
            if c == z["chapter"] and z["from_verse"] <= v <= z["to_verse"]:
                return (z["to_chapter"], v + z["verse_offset"])
        return cv

    def verses_cited(self, text, valid):
        """Chapter:verse tokens that are verses of this book. A token preceded by another book's name is skipped."""
        out = []
        for m in self.cref.finditer(text or ""):
            if self.other_book.search(text[max(0, m.start() - 16):m.start()]):
                continue
            cv = (int(m.group(1)), int(m.group(2)))
            if cv in valid and cv not in out:
                out.append(cv)
        return out

    def chapters_cited(self, text, chapters):
        """Chapter numbers named as 'chapter N' that are chapters of this book, unless another book's name precedes."""
        out = set()
        for m in self.chap.finditer(text or ""):
            if not self.other_book.search(text[max(0, m.start() - 16):m.start()]) and int(m.group(1)) in chapters:
                out.add(int(m.group(1)))
        return out

    def clean_sentences(self, text, limit):
        """Sentences of the row's own prose that can travel. Returns (kept, filtered, capped, short).

        filtered: carried witness bytes, a quotation mark, an internal code or process talk. short: under the minimum
        length (a label, not a reason), or a lower-case piece left by a split at a semicolon, which cannot stand alone.
        capped: usable but past this field's limit. Sentences the row itself marks INFERRED are taken first, in their
        own order: that is where the row says its reading goes beyond the bytes."""
        usable, filtered, short = [], 0, 0
        for s in self.sent.split((text or "").replace("\n", " ")):
            s = s.strip()
            if not s:
                continue
            if self.bad_bytes.search(s) or self.quote.search(s) or self.token.search(s):
                filtered += 1
                continue
            if len(s) < self.min_sentence or self.fragment.match(s):
                short += 1
                continue
            s = s.rstrip(";").rstrip()
            usable.append(s if s[-1] == "." else s + ".")
        ordered = [s for s in usable if "INFERRED" in s] + [s for s in usable if "INFERRED" not in s]
        return ordered[:limit], filtered, max(0, len(ordered) - limit), short

    def blast(self, text, n_rows, qid):
        camp = sorted({m.group(0).lower() for m in self.campaign.finditer(text)})
        conv = sorted({m.group(0).lower() for m in self.convention.finditer(text + " " + qid)})
        if qid.startswith("routed:") and not self.rowref.search(qid):
            conv.append("routed id names no unit")
        if camp:
            cls = "campaign_wide"
        elif conv or n_rows == 0 or n_rows >= self.P["one_book_at_units"]:
            cls = "one_book"
        elif n_rows >= 2:
            cls = "several_units"
        else:
            cls = "one_unit"
        return cls, camp, conv


def load_web_verses(B, root):
    w = B.P["witnesses"]["web"]
    head, vers = re.compile(w["chapter_header_regex"]), re.compile(w["verse_regex"])
    out, ch = [], None
    for line in B.read_pinned(root, w["file"]).decode("utf-8").splitlines():
        m = head.match(line)
        if m:
            ch = int(m.group(1))
            continue
        m = vers.match(line)
        if m and ch:
            out.append((ch, int(m.group(1))))
    return out


def load_device_map(B, inv, which):
    key = B.P["device_verse_keys"][which]
    excl = re.compile(B.P["device_family_excluded_regex"])
    dev = {}
    for name in sorted(inv["formulae"]):
        f = inv["formulae"][name]
        if excl.search(str(f.get("family"))):
            continue
        for v in f.get(key) or []:
            if B.vref(v):
                dev.setdefault(B.vref(v), set()).add(name)
    return dev


def load_packets(B, m8, man):
    """Packets by manifest, by name. A file the never-open pattern matches is skipped before it can be opened."""
    never = re.compile(B.P["never_open_name_regex"])
    kinds = [(k["kind"], re.compile(k["name_regex"]), k["expected"]) for k in B.P["packet_kinds"]]
    got = {k[0]: [] for k in kinds}
    for o in sorted(man["outputs"], key=lambda o: o["path"]):
        name = o["path"].split("/")[-1]
        if never.search(name):
            continue
        for kind, rx, _e in kinds:
            m = rx.match(name)
            if m:
                b = (m8 / o["path"]).read_bytes()
                if sha(b) != o["sha256"]:
                    raise SystemExit("REFUSED: %s does not match the manifest of landed outputs" % o["path"])
                got[kind].append({"name": name, "path": o["path"], "sha256": o["sha256"], "kind": kind,
                                  "lane": m.groupdict().get("lane"), "doc": json.loads(b.decode("utf-8"))})
    for kind, _rx, expected in kinds:
        if len(got[kind]) != expected:
            raise SystemExit("REFUSED: %d %s packets in the manifest, parameters expect %d" % (len(got[kind]), kind, expected))
    return [p for k in kinds for p in got[k[0]]]


def build(book_root, P, params_sha):
    B = Book(P)
    m8 = book_root.parent.parent
    rows = jl(B.read_pinned(book_root, P["rows_file"]))
    order = sorted(rows, key=lambda r: r["chunk_index_in_book"])
    known = {r["decision_id"] for r in rows}
    by_id = {r["decision_id"]: r for r in rows}
    idx = {r["decision_id"]: i for i, r in enumerate(order)}
    cid = {r["decision_id"]: P["cid_format"] % r["chunk_index_in_book"] for r in rows}
    rows_man = json.loads(B.read_pinned(book_root, P["rows_manifest_file"]).decode("utf-8"))
    grader = json.loads(B.read_pinned(book_root, P["grader_file"]).decode("utf-8"))
    inv = json.loads(B.read_pinned(book_root, P["inventory_file"]).decode("utf-8"))
    nb_cfg = P["numbering"]
    if not str(inv.get("numbering", "")).startswith(nb_cfg["inventory_numbering_head"]) \
            or inv.get("numbering_face") != nb_cfg["inventory_numbering_face"]:
        raise SystemExit("REFUSED: the device inventory's numbering sentence is not the one this tool converts by")
    pm = json.loads(B.read_pinned(book_root, P["marks"]["file"]).decode("utf-8"))
    marks = set(pm[P["marks"]["counted_key"]])
    recorded_marks = set(pm[P["marks"]["recorded_not_evidence_key"]])
    diffs = set(pm[P["marks"]["difference_key"]])
    variants = set(pm[P["marks"]["variant_sites_key"]])
    mark_face = P["marks"]["counted_face"]

    # the witnesses: verse sets and sizes
    words = {}
    for line in B.read_pinned(book_root, P["witnesses"]["primary"]["file"]).decode("utf-8").splitlines():
        k, _, t = line.partition("\t")
        if B.vref(k):
            words[B.vref(k)] = len(t.split())
    sec = {B.vref(l.partition("\t")[0]) for l in B.read_pinned(book_root, P["witnesses"]["secondary"]["file"]).decode("utf-8").splitlines()}
    sec.discard(None)
    if sec != set(words):
        raise SystemExit("REFUSED: the primary and secondary witnesses differ in their verse sets")
    web_verses = load_web_verses(B, book_root)
    web_pos = {cv: i for i, cv in enumerate(web_verses)}
    valid = set(web_verses)

    dev = {w: load_device_map(B, inv, w) for w in ("primary", "secondary")}
    man = json.loads(B.read_pinned(book_root, P["landed_manifest_file"]).decode("utf-8"))
    packets = load_packets(B, m8, man)
    rulings = []
    for n in P["ruling_numbers"]:
        rel = P["ruling_path_format"] % n
        rulings.append({"name": "E%d" % n, "path": P["book_path_in_m8"] + rel, "sha256": P["pins"][rel],
                        "kind": "ruling", "doc": json.loads(B.read_pinned(book_root, rel).decode("utf-8"))})
    routed = jl(B.read_pinned(book_root, P["routed_file"]))
    routed_ids = sorted(it["id"] for it in routed)

    # spans: which unit holds each verse
    ends, unit_of = {}, {}
    for r in order:
        a, _, b = r["span"].partition("-")
        ends[r["decision_id"]] = (B.vref(a), B.vref(b))
        for cv in web_verses[web_pos[B.vref(a)]:web_pos[B.vref(b)] + 1]:
            unit_of[cv] = r["decision_id"]

    # per-unit packet measurements
    prim = {r: {} for r in known}
    spot = {r: {} for r in known}
    audits = {r: [] for r in known}
    restated = {r: 0 for r in known}
    sev = {r: {w: 0 for w in P["severity_words"]} for r in known}
    item_links = []  # (a, b, kind, packet path, locator, flagged)
    harvest_stats = {"items_over_pair_cap_skipped": 0, "crossrefs_to_adjacent_unit_skipped": 0,
                     "crossrefs_harvested": 0}

    def land(r, s):
        if s in sev[r]:
            sev[r][s] += 1

    def pairs(named, kind, path, loc, text):
        if len(named) > B.pair_cap:
            harvest_stats["items_over_pair_cap_skipped"] += 1
            return
        fl = bool(B.flag.search(text))
        for i, a in enumerate(named):
            for b in named[i + 1:]:
                item_links.append((a, b, kind, path, loc, fl))

    def crossrefs(r, text, whole, path, loc):
        for cv in B.verses_cited(text, valid):
            x = unit_of[cv]
            if x == r:
                continue
            if abs(idx[x] - idx[r]) == 1:
                harvest_stats["crossrefs_to_adjacent_unit_skipped"] += 1
                continue
            harvest_stats["crossrefs_harvested"] += 1
            item_links.append((r, x, "cross_reference_written_in_a_review_item", path, loc, bool(B.flag.search(whole))))

    fields = P["crossref_fields"]
    for p in packets:
        path, d = p["path"], p["doc"]
        if p["kind"] == "primary":
            lane = p["lane"]
            for i, it in enumerate(d.get("items") or []):
                r = B.norm_id(it.get("row_id"))
                if r not in known:
                    continue
                verdict = str(it.get("verdict")).lower()
                prim[r].setdefault(lane, []).append({"cluster": d.get("cluster"), "verdict": verdict,
                                                     "severity": it.get("severity")})
                if verdict == "challenge":
                    land(r, it.get("severity"))
                t = flat(it)
                named = B.rows_named(t, known)
                if len(named) > B.pair_cap:
                    harvest_stats["items_over_pair_cap_skipped"] += 1
                else:
                    for x in named:
                        if x != r:
                            item_links.append((r, x, "named_inside_a_review_item_on_the_other_unit", path,
                                               "items[%d]" % i, bool(B.flag.search(t))))
                crossrefs(r, " ".join(str(it.get(k) or "") for k in fields["primary"]), t, path, "items[%d]" % i)
        elif p["kind"] == "final_audit":
            for i, it in enumerate(d.get("rows") or []):
                r = B.norm_id(it.get("row"))
                if r not in known:
                    continue
                n_routed = 0
                for f in it.get("findings") or []:
                    if f.get("already_routed"):
                        n_routed += 1
                    else:
                        land(r, f.get("severity"))
                restated[r] += n_routed
                audits[r].append({"audit": p["name"], "verdict": it.get("verdict"),
                                  "findings": len(it.get("findings") or []), "findings_already_routed": n_routed})
                t = flat(it)
                named = B.rows_named(t, known)
                if len(named) > B.pair_cap:
                    harvest_stats["items_over_pair_cap_skipped"] += 1
                else:
                    for x in named:
                        if x != r:
                            item_links.append((r, x, "named_inside_a_review_item_on_the_other_unit", path,
                                               "rows[%d]" % i, bool(B.flag.search(t))))
                text = " ".join(str(it.get(k) or "") for k in fields["final_audit_row"])
                for f in it.get("findings") or []:
                    text += " " + " ".join(str(f.get(k) or "") for k in fields["final_audit_finding"])
                crossrefs(r, text, t, path, "rows[%d]" % i)
        else:
            for i, it in enumerate(d.get("new_findings") or []):
                named = B.rows_named(str(it.get("row_or_artifact") or ""), known)
                for r in named:
                    spot[r][p["name"]] = spot[r].get(p["name"], 0) + 1
                    land(r, it.get("severity"))
                t = flat(it)
                pairs(B.rows_named(t, known), "named_together_in_a_review_finding", path, "new_findings[%d]" % i, t)
                if len(named) == 1:
                    crossrefs(named[0], " ".join(str(it.get(k) or "") for k in fields["spot_review"]), t, path,
                              "new_findings[%d]" % i)
            for key in ("carried_items", "seams", "changed_rows"):
                for i, it in enumerate(d.get(key) or []):
                    t = flat(it)
                    pairs(B.rows_named(t, known), "named_together_in_a_review_finding", path, "%s[%d]" % (key, i), t)

    # open questions
    questions, q_text = [], {}

    def question(qid, kind, path, locator, text, state):
        ids = B.rows_named(text + " " + qid, known)
        by_verse = sorted({unit_of[cv] for cv in B.verses_cited(text, valid)} - set(ids))
        cited_ch = B.chapters_cited(text, {cv[0] for cv in valid})
        by_chapter = sorted({unit_of[cv] for cv in valid if cv[0] in cited_ch} - set(ids) - set(by_verse))
        named = sorted(set(ids) | set(by_verse) | set(by_chapter))
        cls, camp, conv = B.blast(text, len(named), qid)
        first, _f, _c, _s = B.clean_sentences(text, 1)
        q_text[qid] = text
        questions.append({
            "schema": P["schemas"]["dimensions"], "record": "open_question", "question_id": qid, "kind": kind,
            "source": {"path": path, "locator": locator, "tier": "EXTRACTED"},
            "state": state, "text_sha256": sha(text.encode("utf-8")),
            "first_sentence_that_can_travel": first[0] if first else None,
            "measured": {"units_named": named, "units_named_by_id": ids, "units_reached_by_verse_reference": by_verse,
                         "units_reached_by_chapter_reference": by_chapter, "units_named_count": len(named),
                         "parents_named": sorted({by_id[r]["parent_collection"].split(" ")[0] for r in named}),
                         "convention_words": conv, "campaign_words": camp,
                         "states_a_witness_limit": bool(B.limit.search(text))},
            "blast_radius": {"class": cls, "tier": "JUDGED_BY_RULE",
                             "rule": "campaign_wide if a campaign word occurs; else one_book if a convention word "
                                     "occurs (a routed item whose id names no unit counts as one), or no unit is "
                                     "named, or %d or more are; else several_units if two or more units are named "
                                     "by id or reached by a verse or chapter reference; else one_unit. A question with a "
                                     "convention word is never one_unit." % P["one_book_at_units"],
                             "not_a_measurement": "The class is assigned by the stated rule over the measured "
                                                  "fields above. No one re-read the question to produce it."}})

    for it in routed:
        try:
            order_text = json.loads(it.get("order") or "{}").get("order") or ""
        except (TypeError, ValueError):
            order_text = str(it.get("order") or "")
        question("routed:" + it["id"], "routed_end_review_item", P["routed_path_in_m8"], "id=" + it["id"],
                 " ".join((str(order_text), str(it.get("decision") or ""))),
                 "carried open to the end review (ruling word on record: %s)" % it.get("ruling"))
    for p in packets + rulings:
        stem = p["name"][:-5] if p["name"].endswith(".json") else p["name"]
        for i, u in enumerate(p["doc"].get("unresolved_uncertainty") or []):
            text = str(u)
            if isinstance(u, dict):
                text = " ".join(str(u.get(k) or "") for k in ("what", "why_it_matters")).strip() or flat(u)
            question("%s#unresolved[%d]" % (stem, i), "unresolved_in_ruling" if p["kind"] == "ruling"
                     else "unresolved_in_packet", p["path"], "unresolved_uncertainty[%d]" % i, text,
                     "raised as unresolved by its author; its later disposition is not derived here")
        for i, e in enumerate(p["doc"].get("escalations") or []):
            text = " ".join(str(e.get(k) or "") for k in ("row", "topic", "issue")).strip() if isinstance(e, dict) else str(e)
            question("%s#escalations[%d]" % (stem, i), "escalation_in_packet", p["path"], "escalations[%d]" % i, text,
                     "escalated by its author; its later disposition is not derived here")
        if p["kind"] == "spot_review":
            for i, f in enumerate(p["doc"].get("new_findings") or []):
                fid = str(f.get("id"))
                if str(f.get("route")) == P["end_review_route"] \
                        and not any(x == fid or x.endswith("-" + fid) for x in routed_ids):
                    question("%s#new_findings[%d]" % (stem, i), "finding_routed_to_end_review", p["path"],
                             "new_findings[%d]" % i, " ".join(str(f.get(k) or "") for k in ("claim", "suggested_fix")),
                             "routed to the end review by its finding; it has no entry in the routed items")
    inv_path = P["book_path_in_m8"] + P["inventory_file"]
    for i, e in enumerate(inv.get(P["inventory_open_key"]) or []):
        question("device_inventory#%s[%d]" % (P["inventory_open_key"], i), "device_inventory_end_review_item", inv_path,
                 "%s[%d]" % (P["inventory_open_key"], i),
                 " ".join(str(e.get(k) or "") for k in ("item", "question", "measurement")),
                 "listed by the device inventory for the end review")
    strategy = B.read_pinned(book_root, P["strategy_file"]).decode("utf-8").splitlines()
    strat_rx = re.compile(P["strategy_open_regex"])
    for i, line in enumerate(strategy):
        if strat_rx.search(line):
            question("strategy#line[%d]" % (i + 1), "strategy_line_for_end_review", P["book_path_in_m8"] + P["strategy_file"],
                     "line %d" % (i + 1), line, "sent to the end review by the book strategy")
    questions.sort(key=lambda q: q["question_id"])
    q_by_row = {r: [] for r in known}
    for q in questions:
        for r in q["measured"]["units_named"]:
            q_by_row[r].append(q)

    # ruling entries (for the statement rule and for linkage)
    ruled_sets = []  # (label, units named, path, text)
    for p in rulings:
        for e in p["doc"].get("rulings") or []:
            ruled_sets.append(("%s:%s" % (p["name"], e.get("id")), B.rows_named(flat(e), known), p["path"], flat(e)))
    for it in routed:
        q = "routed:" + it["id"]
        ruled_sets.append((q, [x for y in questions if y["question_id"] == q for x in y["measured"]["units_named"]],
                           P["routed_path_in_m8"], q_text[q]))

    # linkages: co-mention only
    links = {}

    def link(a, b, kind, path, loc, flagged):
        if a == b:
            return
        k = tuple(sorted((a, b)))
        links.setdefault(k, {})[(kind, path, loc)] = flagged or links.get(k, {}).get((kind, path, loc), False)
    for a, b, kind, path, loc, flagged in item_links:
        link(a, b, kind, path, loc, flagged)
    for q in questions:
        named = q["measured"]["units_named"]
        if 2 <= len(named) <= B.pair_cap:
            fl = bool(B.flag.search(q_text[q["question_id"]]))
            for i, a in enumerate(named):
                for b in named[i + 1:]:
                    link(a, b, "named_together_in_an_open_question", q["source"]["path"], q["question_id"], fl)
    for label, named, path, text in ruled_sets:
        if label.startswith("routed:"):
            continue
        if 2 <= len(named) <= B.pair_cap:
            for i, a in enumerate(named):
                for b in named[i + 1:]:
                    link(a, b, "named_together_in_a_controlling_ruling", path, label, bool(B.flag.search(text)))

    def last_audit(rid):
        names = P["audit_order"]
        have = sorted(audits[rid], key=lambda a: names.index(a["audit"]))
        return have[-1] if have else None

    link_recs, partners = [], {r: set() for r in known}
    for (a, b) in sorted(links):
        ra, rb = by_id[a], by_id[b]
        srcs = [{"kind": k, "path": p, "locator": loc, "uses_a_word_of_divergence": fl, "tier": "EXTRACTED"}
                for (k, p, loc), fl in sorted(links[(a, b)].items())]
        differs = [f for f in ("confidence", "unit_type") if ra[f] != rb[f]]
        ruled_by = sorted(label for label, named, _p, _t in ruled_sets
                          if a in named and b in named and len(named) <= B.pair_cap)
        flagged = any(s["uses_a_word_of_divergence"] for s in srcs)
        if not differs:
            st = {"verdict": "same_treatment", "basis": "equal_confidence_and_unit_type"}
        elif ruled_by:
            st = {"verdict": "real_distinction", "basis": "standing_after_controlling_ruling",
                  "ruling_entries_naming_both": ruled_by,
                  "carried_to_end_review_under": [x for x in ruled_by if x.startswith("routed:")]}
        elif flagged:
            st = {"verdict": "possible_inconsistency_unruled", "basis": "word_of_divergence_and_no_controlling_ruling"}
        elif differs == ["unit_type"]:
            st = {"verdict": "real_distinction", "basis": "different_recorded_kind"}
        else:
            st = {"verdict": "real_distinction", "basis": "no_packet_alleges_inconsistency",
                  "final_audit_verdicts": [(last_audit(a) or {}).get("verdict"), (last_audit(b) or {}).get("verdict")]}
        st.update({"tier": "JUDGED_BY_RULE", "rule": B.statement_rule,
                   "not_a_measurement": "Assigned by the stated rule. No one re-read the two passages to produce it."})
        partners[a].add(b)
        partners[b].add(a)
        link_recs.append({
            "schema": P["schemas"]["dimensions"], "record": "linkage", "pair": [a, b],
            "chunk_decision_ids": [cid[a], cid[b]], "spans": [ra["span"], rb["span"]],
            "asserts": "co-mention only: the sources below name both units; no similarity is asserted here",
            "sources": srcs,
            "treatment": {"confidence": [ra["confidence"], rb["confidence"]],
                          "unit_type": [ra["unit_type"], rb["unit_type"]],
                          "parent_collection": [ra["parent_collection"], rb["parent_collection"]],
                          "in_feed": [ra["confidence"] in B.select, rb["confidence"] in B.select], "tier": "MEASURED"},
            "treated_differently": bool(differs), "differs_in": differs, "statement": st})

    # units
    parent_n = {}
    for r in rows:
        parent_n[r["parent_collection"]] = parent_n.get(r["parent_collection"], 0) + 1

    def face(web_cv, side):
        cv = B.to_primary(web_cv)
        rf = B.ref(cv)
        return {"verse_primary": rf, "counted_mark_at_verse": rf in marks and side == mark_face,
                "devices_primary": sorted(dev["primary"].get(cv, ())),
                "devices_secondary": sorted(dev["secondary"].get(cv, ())),
                "recorded_mark_not_evidence": B.ref(web_cv) in recorded_marks and side == mark_face,
                "witnesses_differ_at_verse": rf in diffs, "secondary_variant_site_at_verse": rf in variants}

    def has_evidence(f):
        return bool(f["counted_mark_at_verse"] or f["devices_primary"] or f["devices_secondary"])

    def seam(left_row, right_row):
        if left_row is None or right_row is None:
            return {"book_edge": True, "left_face": None, "right_face": None, "evidence_on_both_faces": None}
        left = face(ends[left_row["decision_id"]][1], "left")
        right = face(ends[right_row["decision_id"]][0], "right")
        lo, ro = has_evidence(left), has_evidence(right)
        return {"book_edge": False, "left_face": left, "right_face": right, "evidence_on_left_face": lo,
                "evidence_on_right_face": ro, "evidence_on_both_faces": lo and ro}

    fs = P["final_state"]
    feed, units = [], []
    stats = {"sentences_kept": 0, "filtered": 0, "capped": 0, "short": 0, "fallback": 0}
    primary_label = P["witnesses"]["primary"]["label"]
    for i, r in enumerate(order):
        rid, span = r["decision_id"], r["span"]
        prev_r, next_r = (order[i - 1] if i else None), (order[i + 1] if i + 1 < len(order) else None)
        (w1, w2) = ends[rid]
        span_web = web_verses[web_pos[w1]:web_pos[w2] + 1]
        span_pri = [B.to_primary(cv) for cv in span_web]
        chapter_divergent = any(m[0] != w[0] for m, w in zip(span_pri, span_web))
        offset_zone = any(m != w for m, w in zip(span_pri, span_web))
        lang_seam = r["language"] == "mixed" or any(n is not None and n["language"] != r["language"]
                                                    for n in (prev_r, next_r))
        onset, close = seam(prev_r, r), seam(r, next_r)
        lanes = {k: v for k, v in sorted(prim[rid].items())}
        lane_sets = {k: sorted({x["verdict"] for x in v}) for k, v in lanes.items()}
        verdicts_differ = len({tuple(v) for v in lane_sets.values()}) > 1
        qs = q_by_row[rid]
        routed_q = [q["question_id"] for q in qs if q["kind"] == "routed_end_review_item"]
        limit_ids = [q["question_id"] for q in qs if q["measured"]["states_a_witness_limit"]]
        widest = max([CLASS_ORDER.index(q["blast_radius"]["class"]) for q in qs], default=None)
        edge_dev = bool(dev["primary"].get(span_pri[0]) or dev["secondary"].get(span_pri[0]))
        if limit_ids:
            ans = "a_witness_limit_is_stated"
        elif onset["evidence_on_both_faces"] or (onset["book_edge"] and edge_dev):
            ans = "seam_evidence_present_in_the_witness_layers"
        else:
            ans = "left_out"
        feat = {"zone": chapter_divergent, "lang": lang_seam, "contested": verdicts_differ,
                "one_face": onset["evidence_on_both_faces"] is False, "routed": bool(routed_q)}
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
            risk.append("This unit holds a verse whose chapter differs between the numberings, so every reference "
                        "into it must carry both witnesses' numbers.")
        elif offset_zone:
            risk.append("This unit lies where the numberings differ by a verse offset, so every reference into it "
                        "must carry both witnesses' numbers.")
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
        sev_serious = any(sev[rid][w] for w in B.serious)
        score = ({"low": 2, "medium_low": 1}.get(r["confidence"], 0) + (1 if verdicts_differ else 0)
                 + (1 if sev_serious else 0) + (1 if onset["evidence_on_both_faces"] is False else 0)
                 + (1 if routed_q else 0) + (1 if (chapter_divergent or lang_seam) else 0))
        la = last_audit(rid)
        accepted = (r["review_status"] == fs["requires_review_status"] and r["candidate_hold_state"] is None
                    and la is not None and la["verdict"] == fs["confirm_word"])
        final_state = {"value": fs["accepted_value"] if accepted else fs["other_value"],
                       "tier": "DERIVED per row",
                       "rule": "%s only when review_status is %s, the hold is null and the verdict of the last audit "
                               "that read the row is %s" % (fs["accepted_value"], fs["requires_review_status"],
                                                            fs["confirm_word"]),
                       "last_audit": (la or {}).get("audit"), "last_audit_verdict": (la or {}).get("verdict"),
                       "last_audit_is_the_first_audit_carried_by_byte_equality":
                           bool(la and la["audit"] == P["audit_order"][0]),
                       "carried_by_byte_equality_tier": "REPORTED (the later audit's own statement; not re-measured here)"}
        in_feed = r["confidence"] in B.select
        derivation = None
        if in_feed:
            parts, filt_n, cap_n, short_n = B.clean_sentences(r.get("device_notes"), 2)
            first_field = "device_notes"
            if not parts:
                first_field = "boundary_rationale"
                parts, f2, c2, s2 = B.clean_sentences(r.get("boundary_rationale"), 2)
                filt_n, cap_n, short_n = filt_n + f2, cap_n + c2, short_n + s2
            # A controlling ruling may name the row's own sentence of doubt to lead the reason (1Cor R8-FEED-011).
            lead = (P.get("why_lead_sentence") or {}).get(cid[rid])
            lead_field = None
            if lead:
                where = [k for k in ("device_notes", "boundary_rationale", "strongest_rejected_alternative")
                         if lead in (r.get(k) or "").replace("\n", " ")]
                kept, f_l, _, s_l = B.clean_sentences(lead, 1)
                if not where or kept != [lead] or f_l or s_l:
                    raise SystemExit("REFUSED: why_lead_sentence for %s is not one travelling sentence of the row's "
                                     "own prose" % cid[rid])
                lead_field = where[0]
                parts = [lead] + [p for p in parts if p != lead]
            n_notes = len(parts)
            alt, filt_a, cap_a, short_a = B.clean_sentences(r.get("strongest_rejected_alternative"), 1)
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
                "why_low_confidence_source_fields": [f for f, n in ((first_field, n_notes),
                                                                    ("strongest_rejected_alternative",
                                                                     len(parts) - n_notes)) if n],
                "sentences_kept": 0 if fallback else len(parts),
                "sentences_filtered": filt_n + filt_a, "sentences_too_short_to_be_a_reason": short_n + short_a,
                "sentences_usable_but_over_cap": cap_n + cap_a, "composed_not_derived": fallback,
                "filter": "filtered means the sentence carries a witness-script codepoint, a double quotation mark, an "
                          "internal code or process talk; too short means under %d characters or a lower-case piece "
                          "left by a split at a semicolon; over cap means usable but past the limit of 2 sentences "
                          "from device_notes (from boundary_rationale when device_notes gives none) and 1 from "
                          "strongest_rejected_alternative; sentences the row marks INFERRED are taken first"
                          % B.min_sentence}
            if lead_field:
                derivation["why_low_confidence_lead"] = {"field": lead_field, "set_by": "book_params.why_lead_sentence"}
                if lead_field not in derivation["why_low_confidence_source_fields"]:
                    derivation["why_low_confidence_source_fields"].insert(0, lead_field)
            feed.append({
                "model_id": P["model_id"], "book": B.name, "span": span, "chunk_decision_id": cid[rid],
                "confidence": r["confidence"],
                "observed_substrate_signals": list(r.get("observed_substrate_signals") or []),
                "review_packet_final_state": final_state["value"],
                "chunk_review_status": r["review_status"],
                "candidate_hold_state": r["candidate_hold_state"],
                "non_authorizing": True, "concern_type": concern, "why_low_confidence": why,
                "possible_downstream_risk": " ".join(risk) or None,
                "suggested_reviewer": ("human_owner" if feat["zone"] else
                                       "convergence" if (feat["contested"] or feat["routed"]) else
                                       "literary_form_reviewer"),
                "proposed_atlas_action": "consider_only", "atlas_promotion_authority": "none"})
        units.append({
            "schema": P["schemas"]["dimensions"], "record": "unit", "chunk_decision_id": cid[rid],
            "internal_decision_id": rid, "writer_decision_id": r["writer_decision_id"], "span": span,
            "in_feed": in_feed,
            "measured": {
                "tier": "MEASURED by this tool over the pinned records, except where a field says REPORTED",
                "confidence_recorded": r["confidence"], "review_status_recorded": r["review_status"],
                "candidate_hold_state_recorded": r["candidate_hold_state"],
                "review_packet_final_state": final_state, "unit_type": r["unit_type"],
                "parent_collection": r["parent_collection"], "language": r["language"],
                "signals": list(r.get("observed_substrate_signals") or []),
                "primary_witness": primary_label,
                "span_primary": "%s-%s" % (B.ref(span_pri[0]), B.ref(span_pri[-1])),
                "verses": len(span_web), "words_primary": sum(words[m] for m in span_pri),
                "verses_where_the_witnesses_differ": sum(1 for m in span_pri if B.ref(m) in diffs),
                "holds_a_verse_whose_chapter_differs_between_numberings": chapter_divergent,
                "in_numbering_offset_zone": offset_zone, "at_or_holding_a_language_change": lang_seam,
                "contested_between_blind_lanes": {
                    "verdicts_differ": verdicts_differ, "lane_verdicts": lane_sets, "lanes": lanes,
                    "limit": "the blind lanes read an earlier state of the rows than the final rows, and every lane "
                             "ran on one model family, so a split is a split inside one voice"},
                "severities_landed": dict(sev[rid]),
                "severities_landed_counts": "challenges by a blind lane, new findings of the spot reviews on the rows "
                                            "they name, and audit findings not marked already routed; a finding that "
                                            "was fixed later still counts as landed; the scales are kept as written "
                                            "and not converted into one another",
                "audit_findings_restating_a_routed_item": restated[rid],
                "spot_review_findings": dict(sorted(spot[rid].items())),
                "audits": [dict(a, tier="REPORTED") for a in audits[rid]],
                "seam_evidence": {"onset": onset, "close": close,
                                  "note": "presence of a counted mark or of a device the inventory counts at the "
                                          "verse; presence is not strength, and several counted devices are weak; "
                                          "a recorded mark is shown and never counted"},
                "answerable_from_the_witnesses": {
                    "value": ans, "witnesses": [P["witnesses"][w]["label"] for w in ("primary", "secondary", "web")],
                    "open_questions_stating_a_witness_limit": limit_ids,
                    "left_out_means": "no open question states a witness limit for this unit and its onset seam does "
                                      "not carry evidence on both faces, so nothing here derives an answer; the "
                                      "rating is left out rather than guessed"},
            },
            "derivation": derivation,
            "dependency": {"classes": classes, "neighbour_spans": nb,
                           "units_sharing_this_frame": parent_n[r["parent_collection"]],
                           "open_questions_naming_this_unit": [q["question_id"] for q in qs],
                           "routed_open_questions_naming_this_unit": routed_q,
                           "widest_blast_radius_class": CLASS_ORDER[widest] if widest is not None else None,
                           "linked_units": sorted(partners[rid]),
                           "composed_sentence_in_feed": (" ".join(risk) or None) if in_feed else None},
            "judged": {"tier": "JUDGED_BY_RULE", "atlas_hardness": "high" if score >= P["judged_high_at"] else
                       "medium" if score >= P["judged_medium_at"] else "low", "score": score, "rule": B.judged_rule,
                       "risk_rating": None,
                       "risk_rating_left_out": "no packet rates risk for a unit, so no risk rating is derived here",
                       "not_a_measurement": "This rating is assigned by the stated rule over measured inputs. No "
                                            "one re-read the passage to produce it."}})
    diff = [l for l in link_recs if l["treated_differently"]]
    kinds = sorted({q["kind"] for q in questions})
    st_keys = sorted({l["statement"]["verdict"] + "/" + l["statement"]["basis"] for l in link_recs})
    src_kinds = sorted({s["kind"] for l in link_recs for s in l["sources"]})
    header = {
        "schema": P["schemas"]["dimensions"], "record": "header", "book": B.name,
        "params_sha256": params_sha,
        "inputs_sha256": dict(sorted(P["pins"].items())),
        "packets_read": [{"path": p["path"], "sha256": p["sha256"], "kind": p["kind"]} for p in packets],
        "rows_manifest_holds": {"text": rows_man.get("holds"), "tier": "EXTRACTED"},
        "seam_evidence_rule": {"counted": P["marks"]["counted_label"] + " on the " + P["marks"]["counted_face"]
                               + " face, and any device the inventory counts at the verse",
                               "recorded_not_counted": P["marks"]["recorded_not_evidence_label"],
                               "device_families_excluded": P["device_family_excluded_regex"],
                               "why_excluded": P["device_family_excluded_why"]},
        "grader": {"fallback_in_force": grader.get("fallback_in_force"), "model": grader.get("declared_fallback_model"),
                   "tier": "EXTRACTED", "limit": "every lane of this book ran on one model family (OW-19)"},
        "counts": {
            "final_rows": len(rows), "feed_rows": len(feed),
            "feed_rows_by_confidence": {c: sum(1 for f in feed if f["confidence"] == c) for c in P["select_confidence"]},
            "feed_rows_by_final_state": {v: sum(1 for f in feed if f["review_packet_final_state"] == v)
                                         for v in sorted({f["review_packet_final_state"] for f in feed})},
            "units_contested_between_blind_lanes": sum(1 for u in units if u["measured"]["contested_between_blind_lanes"]["verdicts_differ"]),
            "feed_units_contested_between_blind_lanes": sum(1 for u in units if u["in_feed"] and u["measured"]["contested_between_blind_lanes"]["verdicts_differ"]),
            "open_questions": len(questions),
            "open_questions_by_kind": {k: sum(1 for q in questions if q["kind"] == k) for k in kinds},
            "open_questions_by_blast_radius": {c: sum(1 for q in questions if q["blast_radius"]["class"] == c) for c in CLASS_ORDER},
            "linkages": len(link_recs), "linkages_treated_differently": len(diff),
            "linkage_source_kinds": {k: sum(1 for l in link_recs for s in l["sources"] if s["kind"] == k) for k in src_kinds},
            "harvest": harvest_stats,
            "statements": {k: sum(1 for l in link_recs if l["statement"]["verdict"] + "/" + l["statement"]["basis"] == k)
                           for k in st_keys},
            "hardness": {h: sum(1 for u in units if u["judged"]["atlas_hardness"] == h) for h in ("high", "medium", "low")},
            "answerable": {v: sum(1 for u in units if u["measured"]["answerable_from_the_witnesses"]["value"] == v)
                           for v in sorted({u["measured"]["answerable_from_the_witnesses"]["value"] for u in units})},
            "why_low_confidence": stats},
        "tier": "MEASURED: every count is produced by this tool"}
    return feed, [header] + units + questions + link_recs, rows


def dump(objs):
    return "".join(json.dumps(o, ensure_ascii=False) + "\n" for o in objs).encode("utf-8")


def on_disk_sha(p):
    try:
        return sha(p.read_bytes())
    except FileNotFoundError:
        return "ABSENT"


def arg(argv, flag):
    return argv[argv.index(flag) + 1] if flag in argv else None


def roots(argv):
    params = Path(arg(argv, "--params") or HERE / "book_params.v1.json")
    book_root = Path(arg(argv, "--book-root") or HERE.parent)
    out_root = Path(arg(argv, "--out-root") or book_root)
    return params, book_root, out_root


def main():
    params, book_root, out_root = roots(sys.argv)
    raw = params.read_bytes()
    P = json.loads(raw.decode("utf-8"))
    feed, dims, rows = build(book_root, P, sha(raw))
    out_rows = out_root / "deliverables" / P["outputs"]["feed"]
    out_dim = out_root / "deliverables" / P["outputs"]["dimensions"]
    a, b = dump(feed), dump(dims)
    if "--check" in sys.argv:
        ok = True
        for p, data in ((out_rows, a), (out_dim, b)):
            on = on_disk_sha(p)
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
