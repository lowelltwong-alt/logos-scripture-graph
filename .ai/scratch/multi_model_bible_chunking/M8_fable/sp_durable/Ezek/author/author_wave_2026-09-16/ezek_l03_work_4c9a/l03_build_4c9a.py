#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Builds the ezek_author_l03 deliverable.

Discipline enforced by construction:
  * expected_before is COPIED from the lane file's your_rows, never retyped.
  * every prose change is an exact-fragment substitution asserted to occur ONCE.
  * every WEB quotation and every Hebrew string is SPLICED from the staged verse
    maps by index (E-01 / strategy hygiene: never hand-typed).
  * '~' in an old fragment matches any apostrophe-like codepoint, so no edit can
    fail on a straight-vs-curly apostrophe.
  * every dual-written zone pair is VERIFIED against verse_map_web's own `mt`
    back-reference; no face is crossed by arithmetic.
"""
import json, re, sys, io, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = (r"C:\Users\lowel\AppData\Local\Temp\claude"
        r"\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
        r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad")
LANE = BASE + r"\ezek_aw\lanes\lane_03_worklist.json"
OUT = BASE + r"\ezek_l03_work_4c9a"
D = r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek"

lane = json.load(open(LANE, encoding='utf-8'))
ROWS = {r['decision_id']: r for r in lane['your_rows']}
ITEMS = lane['your_worklist_items']
WEB = json.load(open(D + r"\tools\verse_map_web.json", encoding='utf-8'))
OSHB = json.load(open(D + r"\tools\verse_map_oshb.json", encoding='utf-8'))

PROBLEMS = []
APOS = "['\u2018\u2019]"

# ---------------------------------------------------------------- item ids
def iid(n):
    it = ITEMS[n]
    disc = (it.get('citation') or it.get('run') or it.get('new_value')
            or it.get('action', '')[:40])
    return f"idx{n:02d}:{it['row_id']}:{it['cls']}:{disc}"

# ------------------------------------------------------- programmatic splice
def _strip(s, mode):
    lead = '\u201c\u2018"\u2014- '
    trail = ',.;:?!\u2019\u201d\'" \u2014-'
    if 'L' in mode:
        while s and s[0] in lead:
            s = s[1:]
    if 'T' in mode:
        while s and s[-1] in trail:
            s = s[:-1]
    return s

def splice(spec):
    """{{WEB:key:i:j|MODE}} or {{HEB:key:i:j}} -> exact spliced text."""
    body, _, mode = spec.partition('|')
    kind, key, i, j = body.split(':')[0], body.split(':')[1], int(body.split(':')[2]), int(body.split(':')[3])
    src = WEB if kind == 'WEB' else OSHB
    if key not in src:
        PROBLEMS.append(f"splice: {key} absent from the {kind} map")
        return '<<MISSING>>'
    txt = src[key]['text'] if kind == 'WEB' else src[key]['text']
    words = txt.split()
    if j > len(words):
        PROBLEMS.append(f"splice: {key} has {len(words)} words, asked for {j}")
        return '<<MISSING>>'
    out = _strip(' '.join(words[i:j]), mode)
    if '[fn]' in out:
        PROBLEMS.append(f"splice: {key}[{i}:{j}] carries a footnote marker: {out!r}")
    return out

def expand(text):
    return re.sub(r'\{\{([^}]+)\}\}', lambda m: splice(m.group(1)), text)

# --------------------------------------------------- zone dual verification
def verify_dual(entry):
    """every 'web:X = oshb:Y' pair in a string is checked against the map."""
    for w, o in re.findall(r'web:(Ezek\.\d+\.\d+)\s*=\s*oshb:(Ezek\.\d+\.\d+)', entry):
        got = WEB.get(w, {}).get('mt')
        if got != o:
            PROBLEMS.append(f"DUAL MISMATCH in {entry!r}: web:{w} maps to {got}, written as oshb:{o}")

# ------------------------------------------------------------- edit helpers
EDITS = []

def prose(row_id, field, pairs, items, sweep, why, tier):
    """pairs: list of (old_fragment_with_~, new_fragment_with_{{splices}})"""
    r = ROWS[row_id]
    cur = r[field]
    if not isinstance(cur, str):
        PROBLEMS.append(f"{row_id}.{field} is not a string")
        return
    new = cur
    for old, repl in pairs:
        pat = re.escape(old).replace(re.escape('~'), APOS)
        ms = list(re.finditer(pat, new))
        if len(ms) != 1:
            PROBLEMS.append(f"{row_id}.{field}: fragment matched {len(ms)}x (need 1): {old[:90]!r}")
            return
        new = new[:ms[0].start()] + expand(repl) + new[ms[0].end():]
    if new == cur:
        PROBLEMS.append(f"{row_id}.{field}: substitution produced no change")
        return
    verify_dual(new)
    EDITS.append({"row_id": row_id, "field": field, "op": "set",
                  "expected_before": cur, "value": new,
                  "worklist_item_ids": [iid(n) for n in items],
                  "sweep": sweep, "why": why, "tier": tier})

def listset(row_id, field, pairs, items, sweep, why, tier):
    """fragment substitution inside exactly one element of a list field."""
    r = ROWS[row_id]
    cur = r[field]
    new = list(cur)
    for old, repl in pairs:
        pat = re.escape(old).replace(re.escape('~'), APOS)
        hits = [k for k, e in enumerate(new) if re.search(pat, e)]
        if len(hits) != 1:
            PROBLEMS.append(f"{row_id}.{field}: fragment in {len(hits)} elements (need 1): {old[:80]!r}")
            return
        k = hits[0]
        new[k] = re.sub(pat, lambda m: expand(repl), new[k], count=1)
    if new == cur:
        PROBLEMS.append(f"{row_id}.{field}: list substitution produced no change")
        return
    for e in new:
        verify_dual(e)
    EDITS.append({"row_id": row_id, "field": field, "op": "set",
                  "expected_before": cur, "value": new,
                  "worklist_item_ids": [iid(n) for n in items],
                  "sweep": sweep, "why": why, "tier": tier})

def conf(row_id, value, items):
    r = ROWS[row_id]
    if value not in ('high', 'medium', 'medium_low', 'low'):
        PROBLEMS.append(f"{row_id}: confidence {value!r} is off the four-value scale")
        return
    if r['confidence'] == value:
        PROBLEMS.append(f"{row_id}: confidence already {value}")
        return
    EDITS.append({"row_id": row_id, "field": "confidence", "op": "set_confidence",
                  "expected_before": r['confidence'], "value": value,
                  "worklist_item_ids": [iid(n) for n in items], "sweep": "confidence",
                  "why": f"the ruling grades this row {value}; applied, not chosen.",
                  "tier": "EXTRACTED from the ruling as carried in the worklist"})

def ref(row_id, entry, token, items, why, tier="MEASURED"):
    r = ROWS[row_id]
    e = expand(entry)
    if f"[{token}]" not in e:
        PROBLEMS.append(f"{row_id}: entry is missing its role token: {e!r}")
    free = e.split(']', 1)[1].strip()
    if len(free.split()) > 6:
        PROBLEMS.append(f"{row_id}: free text is {len(free.split())} words (max 6): {free!r}")
    verify_dual(e)
    EDITS.append({"row_id": row_id, "field": "boundary_evidence_refs", "op": "append_ref",
                  "expected_before": r['boundary_evidence_refs'], "value": e,
                  "worklist_item_ids": [iid(n) for n in items], "sweep": "a4",
                  "role_token": token, "why": why, "tier": tier})

# =========================================================== THE EDITS =====
# ---- P03-004
prose("P03-004", "boundary_rationale",
      [("(~you took your sons and your daughters~)",
        "(the WEB has \u201c{{WEB:Ezek.16.20:1:9|T}}\u201d, web:Ezek.16.20)")],
      [0], "a6",
      "A run of five identical consecutive WEB words stood undelimited; it is not the fixed "
      "rendering of a counted device nor of a listed addressee title, so A6-b does not exempt it "
      "and the quotation convention is owed.",
      "MEASURED: the run and its WEB wording are spliced from the staged WEB verse map")
ref("P03-004", "web:Ezek.16.15-Ezek.16.19 [WARRANT-rival] backward merge weighed, not taken",
    "WARRANT-rival", [1],
    "The rejected alternative weighs folding this short row back into the preceding span; the "
    "range is one citation and takes one range entry.")
ref("P03-004", "web:Ezek.16.24-Ezek.16.34 [WARRANT-rival] forward merge weighed and declined",
    "WARRANT-rival", [2],
    "The same field weighs the forward merge; a dash-range is one citation, so one range entry.")

# ---- P03-005
ref("P03-005", "web:Ezek.16.26-Ezek.16.29 [ANCHOR] nations catalogue, not seam evidence",
    "ANCHOR", [3],
    "The rationale cites the four-nation catalogue as content inside the span; the boundary does "
    "not rest on it, so an ANCHOR token is the honest label.")

# ---- P03-007
conf("P03-007", "medium_low", [4])
prose("P03-007", "strongest_rejected_alternative",
      [("the samekh on 16:50 is a clean, mark-corroborated close borne out by the single-witness "
        "paragraph layer itself, and 16:51 opens a fresh comparative move (Samaria~s sins measured "
        "against Sodom~s) rather than continuing 16:44-50~s genealogical frame.",
        "a samekh follows MT 16:50, single witness, and the Sodom comparison\u2019s content is "
        "complete at that verse. The far face of the same seam carries no licensed text signal: "
        "MT 16:51 opens on the conjunction with Samaria, {{HEB:Ezek.16.51:0:2}} "
        "(oshb:Ezek.16.51), the sister already named at 16:46, and it carries no counted onset "
        "formula (sweep: 1 verse). That cross-seam continuity argues against the cut, so the merge "
        "through 16:58 is held as a live alternative on the mark and the content close rather than "
        "refused on the bytes.")],
      [8], "grounds",
      "The C4 order is discharged by disclosing what MT 16:51 actually carries: a waw-conjunctive "
      "continuation naming the sister of 16:46 and no counted onset formula, so the close seam's "
      "far face is empty and the merge stays licensed.",
      "MEASURED: mark direction from the pinned marks layer; MT 16:51's device membership measured "
      "against the pinned inventory, which lists it in none of its formula classes")
ref("P03-007", "web:Ezek.16.45-Ezek.16.46 [ANCHOR] sisters named, no boundary claim",
    "ANCHOR", [5],
    "The genealogical comparison is cited as content; the onset rests on 16:44, not on these two "
    "verses, so no WARRANT token is honest here.")
ref("P03-007", "web:Ezek.16.51 [WARRANT-rival] the held rival\u2019s far face",
    "WARRANT-rival", [6],
    "16:51 is the far face of this row's close seam and the verse at which the merge alternative "
    "is weighed.")
ref("P03-007", "oshb:Ezek.16.47 [DISCLOSURE-kq] one Ketiv/Qere note, single witness",
    "DISCLOSURE-kq", [7],
    "The device note asserts a K/Q at this verse; the marks layer carries exactly one K-Q pair "
    "string for it.",
    "MEASURED: the pinned marks layer holds one K-Q pair string in the LIST keyed to this verse")

# ---- P03-008
prose("P03-008", "boundary_rationale",
      [("(~you bear the penalty of your lewdness and your abominations, declares YHWH~)",
        "(the WEB reads \u201c{{WEB:Ezek.16.58:0:8|T}}\u201d, web:Ezek.16.58)")],
      [9], "a6",
      "The undelimited five-word run is not a counted-device rendering, so the convention is owed; "
      "the WEB's own wording replaces the paraphrase that carried the run.",
      "MEASURED: spliced from the staged WEB verse map")
prose("P03-008", "strongest_rejected_alternative",
      [("(~that you may bear your disgrace~)",
        "(\u201c{{WEB:Ezek.16.54:0:7|T}}\u201d, web:Ezek.16.54)")],
      [10], "a6",
      "The gloss shared five consecutive words with the WEB at this verse and then diverged; "
      "quoting the WEB exactly both delimits the run and removes the divergence.",
      "MEASURED: spliced from the staged WEB verse map")
ref("P03-008", "web:Ezek.16.59 [ANCHOR] covenant turn named, not argued",
    "ANCHOR", [11],
    "The rejected alternative mentions the covenant turn only as what the internal split was said "
    "to anticipate; the row's close does not rest on it.")
ref("P03-008", "oshb:Ezek.16.52 [DISCLOSURE-paseq] paseq, count-only, single witness",
    "DISCLOSURE-paseq", [12],
    "The device note asserts a paseq at this verse; the marks layer lists it once, and no "
    "intra-verse position is claimed.",
    "MEASURED: one occurrence of this key in the pinned paseq list, which is count-only")

# ---- P03-010
prose("P03-010", "boundary_rationale",
      [("(~son of man, propound a riddle and speak a parable to the house of Israel~)",
        "(rendered \u201c{{WEB:Ezek.17.2:0:15|LT}}\u201d, web:Ezek.17.2)")],
      [13], "a6",
      "An eleven-word run stood undelimited; the addressee title inside it does not exempt the "
      "whole run under A6-b, which exempts only a run that is nothing but a device or title "
      "rendering.",
      "MEASURED: spliced from the staged WEB verse map")
ref("P03-010", "web:Ezek.17.11 [WARRANT-close] far-face word-event completes this close",
    "WARRANT-close", [14],
    "The close rests on the strict word-event standing past the seam; this verse is in the "
    "39-verse strict word-event class.",
    "MEASURED: membership in the pinned inventory's strict word-event class of 39 verses")
ref("P03-010", "oshb:Ezek.17.9 [DISCLOSURE-paseq] one paseq occurrence, count-only",
    "DISCLOSURE-paseq", [15],
    "The device note names paseq inside the span at this verse; it is listed once and its position "
    "is not asserted.",
    "MEASURED: one occurrence of this key in the pinned count-only paseq list")

# ---- P03-011
prose("P03-011", "boundary_rationale",
      [("(~say now to the rebellious house~)",
        "(\u201c{{WEB:Ezek.17.12:0:6|LT}}\u201d, web:Ezek.17.12)")],
      [16], "a6",
      "A six-word WEB run stood undelimited and is not a counted-device rendering, so the "
      "convention is owed.",
      "MEASURED: spliced from the staged WEB verse map")
ref("P03-011", "oshb:Ezek.17.19 [WARRANT-close] fresh messenger formula past the seam",
    "WARRANT-close", [17],
    "The close rests on the far-face messenger formula introduced by 'therefore'; this verse is in "
    "the 122-verse long messenger class.",
    "MEASURED: membership in the pinned inventory's 122-verse long messenger class")
ref("P03-011", "web:Ezek.17.19-Ezek.17.21 [WARRANT-rival] forward merge weighed here",
    "WARRANT-rival", [18],
    "The rejected alternative weighs folding the sentence proper into this row; a dash-range is "
    "one citation and takes one range entry.")

# ---- P03-012
conf("P03-012", "medium", [19])
prose("P03-012", "strongest_rejected_alternative",
      [("the samekh on 17:21 corroborates keeping them apart.",
        "a samekh follows MT 17:21, single witness, corroborating the separation. The stronger "
        "alternative runs the other way: reading 17:11-21 as one interpretation-and-sentence unit, "
        "which would dissolve this row's onset seam. That seam is weighed on both faces. Its near "
        "face, 17:19, carries the long messenger formula with the as-I-live oath, one of the 122 "
        "verses carrying that formula; its far face, 17:18, ends on a content clause and not on a "
        "close-role formula, so the messenger formula is not licensed as a sub-onset there \u2014 the "
        "addressee does not change and the preceding verse does not end on an utterance or "
        "recognition signature, and a paragraph mark cannot stand in for that limb. The cut is held "
        "on the stated ground that 17:19 turns from narrated history to a first-person oath sentence "
        "and that the mark behind it corroborates the turn, so the merge remains licensed and held "
        "rather than refuted.")],
      [21], "grounds",
      "The A16 order is discharged by naming the 17:11-21 merge and weighing it on both faces, "
      "stating that the row's own onset formula is not licensed as a sub-onset and that the rival "
      "is therefore held, not defeated \u2014 which is what the ruled medium grade records.",
      "MEASURED: mark direction and the two verses' device membership from the pinned marks layer "
      "and inventory; the merge alternative itself is EXTRACTED from the order")
ref("P03-012", "web:Ezek.17.22-Ezek.17.24 [WARRANT-rival] rival close weighed at this range",
    "WARRANT-rival", [20],
    "The rejected alternative weighs merging with the restoration figure that follows; one range "
    "citation, one range entry.")

# ---- P03-013
prose("P03-013", "boundary_rationale",
      [("(~I YHWH have spoken, and I will do it~)",
        "(the WEB closes it \u201c{{WEB:Ezek.17.24:35:43|LT}}\u201d, web:Ezek.17.24)")],
      [22], "a6",
      "The gloss reproduced a five-word WEB run that the WEB carries at two far-side verses and "
      "NOT at this row's own verse; quoting this verse's own WEB wording removes the false "
      "implication and installs the convention.",
      "MEASURED: my own scan of the staged WEB map finds the run at exactly two verses, neither in "
      "this span; the replacement is spliced from this verse")
listset("P03-013", "boundary_evidence_refs",
        [("the verse-final ~I YHWH have spoken and I will do it~ close",
          "the verse-final emphatic I-YHWH-have-spoken close")],
        [23], "a6",
        "The same five-word run stood in a reference entry. The entry now names the counted close "
        "device instead of carrying an English run, so no quotation convention is owed inside the "
        "index.",
        "MEASURED: the run's WEB locations measured; the device name is the inventory's own class")

# ---- P03-014
prose("P03-014", "boundary_rationale",
      [("(~the fathers eat sour grapes, and the children~s teeth are set on edge~)",
        "(\u201c{{WEB:Ezek.18.2:15:29|LT}}\u201d, web:Ezek.18.2)")],
      [24], "a6",
      "An eight-word run stood undelimited inside a paraphrase that otherwise diverges from the "
      "WEB; the WEB's own proverb wording is quoted with the in-field reference.",
      "MEASURED: spliced from the staged WEB verse map")
ref("P03-014", "web:Ezek.18.5 [WARRANT-rival] extension rival weighed at this verse",
    "WARRANT-rival", [25],
    "The rejected alternative weighs extending the row through the righteous-man case, and 18:5 is "
    "where that extension is weighed.")

# ---- P03-015
ref("P03-015", "oshb:Ezek.18.4 [WARRANT-onset] onset rests on this far face",
    "WARRANT-onset", [27],
    "The onset is argued from the far side of the seam: a samekh follows MT 18:4 and the thesis "
    "closes there.",
    "MEASURED: the pinned marks layer records a samekh on this verse, which is the verse the mark "
    "follows")
ref("P03-015", "web:Ezek.18.10 [WARRANT-close] empty far face at the close",
    "WARRANT-close", [28],
    "The close is argued from what the far face lacks: 18:10 opens the next case with no formula "
    "of its own, and it is in none of the inventory's formula classes.",
    "MEASURED: measured against the pinned inventory, which lists this verse in no formula class")
ref("P03-015", "web:Ezek.18.10-Ezek.18.20 [WARRANT-rival] fusion rival weighed, span kept",
    "WARRANT-rival", [29],
    "The rejected alternative weighs fusing the two case-law blocks; one range citation, one range "
    "entry.")

# ---- P03-016
ref("P03-016", "web:Ezek.18.14 [WARRANT-rival] interior cut weighed, not adopted",
    "WARRANT-rival", [30],
    "The rationale weighs an interior cut at the righteous grandson's case and declines it; 18:14 "
    "is the near face of that rival.")
ref("P03-016", "web:Ezek.18.18 [ANCHOR] generational recall, content only",
    "ANCHOR", [31],
    "18:18 is cited for the content link that keeps the three cases together, not as a seam signal.")

# ---- P03-017
prose("P03-017", "boundary_rationale",
      [("(~but if the wicked turns~)",
        "(\u201c{{WEB:Ezek.18.21:0:13|LT}}\u201d, web:Ezek.18.21)"),
       ("with the rhetorical question~s own final clause, ~and not rather that he should turn from "
        "his way and live~, still to follow;",
        "with the verse\u2019s own final clause, \u201c{{WEB:Ezek.18.23:14:26|L}}\u201d "
        "(web:Ezek.18.23), still to follow;")],
      [32, 33, 34], "a6",
      "Three runs sat in one field. Two are WEB runs at this row's own verses and owed the "
      "convention; the third, 'turn from his way and live', was a mis-gloss that reproduced a "
      "far-side verse instead of 18:23, so quoting 18:23 exactly discharges both at once.",
      "MEASURED: my scan locates the far-side run at exactly two verses, neither in this span; "
      "both replacements are spliced from the staged WEB map")

# ---- P03-018
prose("P03-018", "boundary_rationale",
      [("(~but when a righteous person turns from his righteousness and does injustice~)",
        "(\u201c{{WEB:Ezek.18.24:0:12|LT}}\u201d, web:Ezek.18.24)")],
      [35], "a6",
      "The gloss reproduced a five-word run the WEB carries at two far-side verses but not at "
      "18:24, whose own wording has 'turns away from'; quoting this verse removes the collision and "
      "installs the convention.",
      "MEASURED: the run's two WEB locations measured by my own scan; the replacement is spliced "
      "from 18:24")

# ---- P03-019
prose("P03-019", "boundary_rationale",
      [("(~therefore I will judge you, each according to his ways, O house of Israel, declares the "
        "Lord YHWH~)",
        "(\u201c{{WEB:Ezek.18.30:0:13|LT}}\u201d, web:Ezek.18.30)")],
      [36], "a6",
      "A five-word WEB run stood undelimited; it is not a counted-device rendering, so the "
      "convention is owed and the WEB's own clause is quoted.",
      "MEASURED: spliced from the staged WEB verse map")

# ---- P03-020
prose("P03-020", "boundary_rationale",
      [("(~and you, take up a lamentation for the princes of Israel~)",
        "(\u201c{{WEB:Ezek.19.1:0:10|LT}}\u201d, web:Ezek.19.1)"),
       ("(~so that his voice should no more be heard on the mountains of Israel~)",
        "(\u201c{{WEB:Ezek.19.9:21:35|T}}\u201d, web:Ezek.19.9)"),
       ("(~your mother was like a vine in your vineyard, planted by the water~)",
        "(\u201c{{WEB:Ezek.19.10:0:13|LT}}\u201d, web:Ezek.19.10)"),
       ("(~this is a lamentation, and it is used as a lamentation~)",
        "(\u201c{{WEB:Ezek.19.14:27:37|T}}\u201d, web:Ezek.19.14)")],
      [37, 38, 39, 40], "a6",
      "Four WEB runs of five to fourteen words stood undelimited in one field; none is the fixed "
      "rendering of a counted device or a listed addressee title, so each owes the convention, and "
      "two of the four paraphrases also diverged from the WEB they reproduced.",
      "MEASURED: all four replacements spliced from the staged WEB verse map")
ref("P03-020", "oshb:Ezek.19.2 [ANCHOR] lion figure tag, not evidence",
    "ANCHOR", [41],
    "The Hebrew tag at 19:2 is cited for the lion figure's content; the row's seams do not rest on "
    "it.")

# ---- P04-001
ref("P04-001", "oshb:Ezek.20.9 [WARRANT-rival] refrain-split rival weighed here",
    "WARRANT-rival", [42],
    "The rationale weighs the for-my-name's-sake refrains as a rival split and declines them; "
    "20:9 is in none of the inventory's formula classes, which is the ground stated.",
    "MEASURED: measured against the pinned inventory, which lists this verse in no formula class")
ref("P04-001", "oshb:Ezek.20.3 [WARRANT-rival] alternate close weighed here",
    "WARRANT-rival", [43],
    "20:3 carries the messenger formula and a verse-final utterance signature and is weighed as a "
    "competing close; it is in both the 122-verse messenger class and the 81-verse utterance class.",
    "MEASURED: membership in the pinned inventory's 122-verse messenger and 81-verse utterance "
    "classes")
ref("P04-001", "oshb:Ezek.19.14 [DISCLOSURE-mark] pe follows, single witness",
    "DISCLOSURE-mark", [44],
    "The rationale cites the paragraph mark behind this row's onset; the marks layer records a pe "
    "on the verse it follows.",
    "MEASURED: the pinned marks layer records PE on this verse")
ref("P04-001", "oshb:Ezek.20.4 [WARRANT-rival] son-of-man address, no word-event",
    "WARRANT-rival", [45],
    "The rejected alternative weighs a cut before 20:4. The free text records what the verse "
    "carries rather than the field's claim that it carries no onset device: 20:4 is in the "
    "93-verse son-of-man class, which the inventory gives an onset role.",
    "MEASURED: membership in the pinned inventory's 93-verse son-of-man class")

# ---- P04-002
prose("P04-002", "boundary_rationale",
      [("(web:Ezek.20.29 renders it, ~What does the high place where you go mean?~ So its name is "
        "called Bamah to this day.)",
        "(web:Ezek.20.29 renders it \u201c{{WEB:Ezek.20.29:0:14}}\u201d and then names the high "
        "place Bamah to this day)")],
      [46, 48], "a6",
      "The eighteen-word WEB run was present with its reference but marked with single curly "
      "quotes, which this corpus reserves for glosses; double curly quotes are the WEB marker. The "
      "same install now carries the peer's five-word run 'Then I said to them', which the WEB has "
      "at this same in-span verse.",
      "MEASURED: spliced from the staged WEB verse map; the footnote marker is excluded by ending "
      "the splice before it")
ref("P04-002", "oshb:Ezek.20.26 [DISCLOSURE-mark] onset-seam samekh, single witness",
    "DISCLOSURE-mark", [47],
    "The onset is argued partly from the closed-section mark behind it; the marks layer records a "
    "samekh on the verse the mark follows.",
    "MEASURED: the pinned marks layer records SAMEKH on this verse")

# ---- P04-003
conf("P04-003", "medium_low", [49])

# ---- P04-005
prose("P04-005", "boundary_rationale",
      [("as ~Isn~t he a speaker of parables?~,",
        "as \u201c{{WEB:Ezek.20.49:10:16|LT}}\u201d,")],
      [50, 53], "a6",
      "The run was already referenced dual but delimited with single curly quotes; the WEB marker "
      "is double curly quotes. One install discharges both union members, which name the same run "
      "in two spellings.",
      "MEASURED: spliced from the staged WEB verse map")
ref("P04-005", "web:Ezek.20.44 = oshb:Ezek.20.44 [DISCLOSURE-mark] pe behind this onset, single witness",
    "DISCLOSURE-mark", [51],
    "The rationale cites the pe standing behind the onset. The pair is written on both faces "
    "although this verse is outside the renumbering shift, so no reader has to infer which face it "
    "is on.",
    "MEASURED: the pinned marks layer records PE on this verse; the face identity is stated by the "
    "crosswalk, not computed")
ref("P04-005", "web:Ezek.21.1 = oshb:Ezek.21.6 [WARRANT-close] second hard seam past the close",
    "WARRANT-close", [52],
    "The close rests on the fresh strict word-event standing past the seam; that verse is in the "
    "39-verse strict word-event class.",
    "MEASURED: membership in the pinned inventory's strict 39 class; the dual pair is verified "
    "against the crosswalk's own back-reference")

# ---- P04-006
prose("P04-006", "literature_type_guess",
      [("the sword drawn against the land of Israel, the mashal~s plain-sense twin",
        "the drawn sword \u201c{{WEB:Ezek.21.2:15:20|T}}\u201d (web:Ezek.21.2 = oshb:Ezek.21.7), "
        "the mashal\u2019s plain-sense twin")],
      [54], "a6",
      "A five-word WEB run sat undelimited in this field. 'The land of Israel' is not one of the "
      "listed addressee titles A6-b exempts, so the convention is owed, and inside this zone the "
      "in-field reference is written dual.",
      "MEASURED: spliced from the staged WEB verse map; the dual pair verified against the "
      "crosswalk")
prose("P04-006", "boundary_rationale",
      [("still a hard seam despite the repetition.",
        "still a hard seam despite the repetition. The paragraph layer corroborates it from the far "
        "side: a pe follows web:Ezek.20.49 = oshb:Ezek.21.5, single witness, so the mark falls "
        "between that verse and this onset rather than on the onset verse itself.")],
      [55], "grounds",
      "The MARKS-3D order is discharged on the onset direction: the marks layer records the pe on "
      "the verse it follows, which places it at this row's onset seam, and the reference is "
      "dual-written because it touches the renumbering zone.",
      "MEASURED: the pinned marks layer records PE on that verse; direction is the layer's own "
      "stated convention")
ref("P04-006", "web:Ezek.20.49 = oshb:Ezek.21.5 [DISCLOSURE-mark] closing pe at this onset seam",
    "DISCLOSURE-mark", [55],
    "The disclosure the order requires puts a verse citation at the onset seam, so the reference "
    "index carries it too rather than leaving a new unmirrored citation behind.",
    "MEASURED: the pinned marks layer records PE on that verse; the dual pair verified against the "
    "crosswalk")

# ---- P04-007
ref("P04-007", "web:Ezek.21.5 = oshb:Ezek.21.10 [DISCLOSURE-mark] samekh behind this onset",
    "DISCLOSURE-mark", [56],
    "The rationale cites the closed-section mark at the onset seam; the marks layer records a "
    "samekh on the verse it follows.",
    "MEASURED: the pinned marks layer records SAMEKH on that verse; the dual pair verified against "
    "the crosswalk")

# ---- P04-008
conf("P04-008", "medium_low", [57])
prose("P04-008", "strongest_rejected_alternative",
      [("Cutting a second time at web:Ezek.21.12 = oshb:Ezek.21.17 (cry and wail, son of man), "
        "which carries its own son-of-man emphasis and a WEB paragraph mark, was considered and "
        "rejected: no fresh word-event or messenger formula stands there, and translation "
        "paragraphing never drives a boundary on its own.",
        "Cutting a second time at web:Ezek.21.12 = oshb:Ezek.21.17, which the WEB renders "
        "\u201c{{WEB:Ezek.21.12:0:6|T}}\u201d, was considered and rejected. That verse carries the son-of-man address, one of the 93 verses in that "
        "class, and carries no word-event and no messenger formula; the WEB opens no paragraph at "
        "it, and translation lineation would not drive a boundary in any case."),
       ("The unit still runs past that seam on the byte evidence that the address at MT 21:19 "
        "brings no fresh word-event or messenger formula with it; it renews the same address "
        "already opened at web:Ezek.21.9 = oshb:Ezek.21.14 and repeated at web:Ezek.21.12 = "
        "oshb:Ezek.21.17, now a third time,",
        "That signature is verse-final, its verse being one of the 81 in the long utterance class, "
        "so the second limb of the sub-onset test is met on the bytes here and is not denied. What "
        "carries the unit past the seam is the shape of the renewal: a renewed prophesying command "
        "to the same addressee, standing after a verse-final utterance signature, is a paragraph "
        "and not an onset. That renewed address already stands "
        "at web:Ezek.21.9 = oshb:Ezek.21.14, which the messenger-variant census carries as a "
        "short-form occurrence \u2014 its fourth short-form verse and its third distinct shape \u2014 "
        "so that verse is not merely a repeated addressee title, and again at web:Ezek.21.12 = "
        "oshb:Ezek.21.17,")],
      [58, 62], "grounds",
      "The A9/A16 order is discharged three ways: the pe and the ve'attah are named on both faces "
      "with their measured class membership; the denial is corrected, because the preceding verse "
      "does end verse-final on the utterance signature and the true ground is the renewed-command "
      "clause, not the absence of a word-event; and the class blend is corrected, because the "
      "verse called a repeated address is carried by the messenger-variant census as a short form. "
      "The A6 run in the same field is delimited in the same edit.",
      "MEASURED: the utterance-class and son-of-man-class memberships, the mark, and the WEB's "
      "own paragraph state are measured from the pinned layers; the short-form shape figures are "
      "EXTRACTED from the pinned inventory's census block")
ref("P04-008", "web:Ezek.21.9 = oshb:Ezek.21.14 [DISCLOSURE-device] in-span messenger short form",
    "DISCLOSURE-device", [59],
    "The field now cites this verse for what the census records there; the boundary does not rest "
    "on it, so a disclosure token rather than a warrant token is honest.",
    "EXTRACTED from the pinned inventory's messenger-variant census; the dual pair verified against "
    "the crosswalk")
ref("P04-008", "web:Ezek.21.9-Ezek.21.11 = oshb:Ezek.21.14-Ezek.21.16 [ANCHOR] sword already sharpened, content only",
    "ANCHOR", [60],
    "The range is cited for the sword's prior sharpening, a content statement; one range citation, "
    "one range entry, written dual.",
    "MEASURED: both endpoints' dual pairs verified against the crosswalk's own back-references")
ref("P04-008", "web:Ezek.21.15 = oshb:Ezek.21.20 [DISCLOSURE-paseq] count-only paseq, single witness",
    "DISCLOSURE-paseq", [61],
    "The device note names paseq at this verse; it is listed once and no position is asserted.",
    "MEASURED: one occurrence of this key in the pinned count-only paseq list")

# ---- P04-009
ref("P04-009", "web:Ezek.21.17 = oshb:Ezek.21.22 [DISCLOSURE-mark] pe recorded here, single witness",
    "DISCLOSURE-mark", [63],
    "The rationale cites this mark as onset corroboration; the marks layer records a pe on the "
    "verse it follows.",
    "MEASURED: the pinned marks layer records PE on that verse; the dual pair verified against the "
    "crosswalk")
ref("P04-009", "web:Ezek.21.22 = oshb:Ezek.21.27 [DISCLOSURE-paseq] paseq present, position unsourceable",
    "DISCLOSURE-paseq", [64],
    "The device note names paseq at this verse; the layer is count-only, so the position is not "
    "claimed.",
    "MEASURED: one occurrence of this key in the pinned count-only paseq list")

# ---- P04-010
ref("P04-010", "web:Ezek.21.24 = oshb:Ezek.21.29 [DISCLOSURE-mark] mark behind this onset, single witness",
    "DISCLOSURE-mark", [65],
    "The rationale cites the pe standing behind this row's onset; the marks layer records it on the "
    "verse it follows.",
    "MEASURED: the pinned marks layer records PE on that verse; the dual pair verified against the "
    "crosswalk")

# ---- P04-011
prose("P04-011", "boundary_rationale",
      [("a foreign addressee, the children of Ammon and their reproach, an addressee-class shift",
        "a foreign addressee \u2014 the WEB reads it \u201c{{WEB:Ezek.21.28:12:21|T}}\u201d "
        "\u2014 an addressee-class shift")],
      [66], "a6",
      "A five-word WEB run stood undelimited; 'the children of Ammon' is not one of the listed "
      "addressee titles A6-b exempts, so the convention is owed and the reference is dual-written.",
      "MEASURED: spliced from the staged WEB verse map; the dual pair verified against the "
      "crosswalk")
prose("P04-011", "literature_type_guess",
      [("the sword unsheathed against the children of Ammon",
        "the sword unsheathed over Ammon\u2019s reproach")],
      [67], "a6",
      "This field reproduced a five-word WEB run that the WEB carries at one far-side verse and "
      "not at any verse in this span. Delimiting it would assert a quotation of a verse the row "
      "does not argue, so the label is reworded to the row's own words; the properly delimited "
      "quotation of this span's own wording is installed in the rationale.",
      "MEASURED: my scan finds the run at exactly one WEB verse, outside this span")

# ---- P05-001
ref("P05-001", "web:Ezek.22.17 [WARRANT-close] far-face word-event past the close",
    "WARRANT-close", [68],
    "The close is argued against the next onset; 22:17 is in the 39-verse strict word-event class.",
    "MEASURED: membership in the pinned inventory's strict 39 class")
ref("P05-001", "oshb:Ezek.22.12 [WARRANT-rival] alternate close weighed and declined",
    "WARRANT-rival", [69],
    "The rejected alternative weighs closing at 22:12; that verse is in the 81-verse utterance "
    "class, which is what makes the rival real.",
    "MEASURED: membership in the pinned inventory's 81-verse utterance class")
ref("P05-001", "oshb:Ezek.22.2 [DISCLOSURE-device] son-of-man address in span",
    "DISCLOSURE-device", [70],
    "The tag field cites this verse for the address it carries; the boundary does not rest on it.",
    "MEASURED: membership in the pinned inventory's 93-verse son-of-man class")
ref("P05-001", "oshb:Ezek.22.3 [DISCLOSURE-device] messenger formula inside the span",
    "DISCLOSURE-device", [71],
    "The tag field cites the messenger formula here; it is a sub-onset device the row's seams do "
    "not rest on.",
    "MEASURED: membership in the pinned inventory's 122-verse long messenger class")
ref("P05-001", "oshb:Ezek.22.14 [DISCLOSURE-device] emphatic spoken close in span",
    "DISCLOSURE-device", [72],
    "The tag field cites the emphatic spoken formula at 22:14; the row closes two verses later, so "
    "this is an in-span device, not a warrant.",
    "MEASURED: membership in the pinned inventory's 14-verse emphatic spoken class")
ref("P05-001", "oshb:Ezek.22.11 [DISCLOSURE-paseq] paseq recorded, no position claimed",
    "DISCLOSURE-paseq", [73],
    "The device note names paseq at this verse; the layer is count-only.",
    "MEASURED: one occurrence of this key in the pinned count-only paseq list")

# ---- P05-002
prose("P05-002", "strongest_rejected_alternative",
      [("Treating the samekh mark at 22:18 (one verse into the unit) as a competing internal seam "
        "\u2014 rejected: no formula device stands there, and a mark with no formula is disclosed and "
        "never cuts alone.",
        "An interior rival was weighed and not taken. The paragraph layer writes a samekh on MT "
        "22:18, the verse the mark follows, so the seam it corroborates falls between 22:18 and "
        "22:19 rather than on 22:18 itself. Both faces of that seam carry real evidence: the far "
        "face, 22:18, is a son-of-man address, one of the 93 verses in that class, and the near "
        "face, 22:19, opens on the long messenger formula, one of the 122 verses in that class. The "
        "seam is still not licensed as a sub-onset. The indicted party does not change across it, "
        "the house of Israel named at 22:18 being the same party gathered at 22:19, and 22:18 does "
        "not end on a close-role formula \u2014 its last clause is the silver-dross statement \u2014 "
        "so the second limb is unmet and a paragraph mark cannot stand in for it. The mark is "
        "therefore disclosed for the alternative it corroborates, and this unit is held whole on "
        "that stated ground.")],
      [76], "grounds",
      "The false ground was the denial that any formula device stands at the rival seam: the far "
      "face carries the son-of-man address and the near face the long messenger formula, both "
      "measured. The replacement states what is there, locates the mark on the verse it follows "
      "instead of on the seam, and holds the unit on the sub-onset test rather than on a denial.",
      "MEASURED: both class memberships from the pinned inventory, the mark from the pinned marks "
      "layer, and 22:18's closing clause from the staged MT verse map")
ref("P05-002", "oshb:Ezek.22.18 [WARRANT-rival] the rival seam\u2019s far face",
    "WARRANT-rival", [74],
    "The rewritten field weighs the interior rival at this verse and states the address it "
    "carries.",
    "MEASURED: membership in the pinned inventory's 93-verse son-of-man class; the mark is on this "
    "verse, which is the verse it follows")
ref("P05-002", "oshb:Ezek.22.19 [WARRANT-rival] unlicensed rival, near face weighed",
    "WARRANT-rival", [75],
    "22:19 is the rival seam's near face and carries the messenger formula the weighing turns on.",
    "MEASURED: membership in the pinned inventory's 122-verse long messenger class")

# ---- P05-003
ref("P05-003", "oshb:Ezek.22.28 [WARRANT-rival] quoted-speech onset weighed, refused",
    "WARRANT-rival", [77],
    "The rejected alternative weighs the embedded messenger clause at 22:28 as an internal onset; "
    "the verse is in the 122-verse messenger class, which is why the rival needs weighing.",
    "MEASURED: membership in the pinned inventory's 122-verse long messenger class")
ref("P05-003", "oshb:Ezek.22.24 [DISCLOSURE-device] addressee title inside the span",
    "DISCLOSURE-device", [78],
    "The tag field cites the son-of-man address at 22:24; the row's seams do not rest on it.",
    "MEASURED: membership in the pinned inventory's 93-verse son-of-man class")

# ======================================================= self-checks =======
def norm(s):
    s = s.lower()
    for a, b in (('\u2019', "'"), ('\u2018', "'"), ('\u201c', '"'), ('\u201d', '"')):
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9' ]+", ' ', s).replace("'", '')
    return re.sub(r'\s+', ' ', s).strip()

WEBWORDS = {k: norm(v['text']).split() for k, v in WEB.items() if k.startswith('Ezek.')}

def undelimited_runs(text):
    """report every >=5-word WEB run in `text` that is NOT inside curly double quotes."""
    masked = re.sub(r'\u201c[^\u201d]*\u201d', lambda m: ' ' * len(m.group(0)), text)
    w = norm(masked).split()
    hits = []
    for n in range(len(w), 4, -1):
        pass
    for i in range(len(w)):
        for j in range(i + 5, min(i + 22, len(w)) + 1):
            seg = w[i:j]
            for k, ww in WEBWORDS.items():
                L = len(seg)
                for p in range(0, max(0, len(ww) - L + 1)):
                    if ww[p:p + L] == seg:
                        hits.append((' '.join(seg), k))
                        break
                else:
                    continue
                break
    best = {}
    for seg, k in hits:
        best.setdefault(k, set()).add(seg)
    out = []
    for k, segs in best.items():
        longest = max(segs, key=lambda s: len(s.split()))
        if not any(longest != s and longest in s for s in segs):
            out.append((k, longest))
    return out

print("#" * 70)
print(f"EDITS BUILT: {len(EDITS)}")
one_per = {}
for e in EDITS:
    if e['op'] in ('set', 'set_confidence'):
        key = (e['row_id'], e['field'])
        one_per[key] = one_per.get(key, 0) + 1
for k, v in one_per.items():
    if v > 1:
        PROBLEMS.append(f"more than one non-append edit on {k}: {v}")

# append_ref edits on the same row must share one expected_before
from collections import defaultdict
byrow = defaultdict(list)
for e in EDITS:
    if e['op'] == 'append_ref':
        byrow[e['row_id']].append(e)
for rid, es in byrow.items():
    if any(e['expected_before'] != es[0]['expected_before'] for e in es):
        PROBLEMS.append(f"{rid}: append_ref edits disagree on expected_before")
    if any(e['field'] != 'boundary_evidence_refs' for e in es):
        PROBLEMS.append(f"{rid}: append_ref on a field other than boundary_evidence_refs")
    if rid in {e['row_id'] for e in EDITS if e['op'] == 'set' and e['field'] == 'boundary_evidence_refs'}:
        PROBLEMS.append(f"{rid}: both a set and appends on boundary_evidence_refs")

# expected_before must equal the live lane value, byte for byte
for e in EDITS:
    live = ROWS[e['row_id']][e['field']]
    if e['expected_before'] != live:
        PROBLEMS.append(f"{e['row_id']}.{e['field']}: expected_before is not the live value")

# no seam / identity field may be touched
BANNED = {'span', 'osis_start', 'osis_end', 'decision_id', 'writer_part',
          'writer_decision_id', 'writer_attempt_id', 'model_id', 'book',
          'chunk_index_in_book', 'parent_collection'}
for e in EDITS:
    if e['field'] in BANNED:
        PROBLEMS.append(f"{e['row_id']}: edit touches the banned field {e['field']}")

print("\n--- residual undelimited WEB runs in every new prose value ---")
for e in EDITS:
    if e['op'] != 'set':
        continue
    vals = e['value'] if isinstance(e['value'], list) else [e['value']]
    for v in vals:
        for k, seg in undelimited_runs(v):
            print(f"  {e['row_id']}.{e['field']}: {len(seg.split())}w run also at {k}: {seg!r}")

print("\n--- rotation: formulations per role token ---")
rot = defaultdict(set)
for e in EDITS:
    if e['op'] == 'append_ref':
        rot[e['role_token']].add(e['value'].split(']', 1)[1].strip())
for t, s in sorted(rot.items()):
    flag = '' if (len(s) >= 4 or sum(1 for e in EDITS if e.get('role_token') == t) < 4) else '  <-- TOO FEW'
    print(f"  {t}: {sum(1 for e in EDITS if e.get('role_token')==t)} uses, {len(s)} distinct{flag}")

print("\n--- PROBLEMS ---")
for p in PROBLEMS:
    print("  !!", p)
if not PROBLEMS:
    print("  none")

json.dump(EDITS, open(OUT + r"\_edits_stage.json", 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print(f"\nwrote {OUT}\\_edits_stage.json")
