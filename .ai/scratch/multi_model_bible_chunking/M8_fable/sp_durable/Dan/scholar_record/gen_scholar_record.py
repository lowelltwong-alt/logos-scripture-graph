#!/usr/bin/env python3
"""GENERATOR for the Daniel scholar record (close-gate item 20, OW-17).

Ported in FORM from the Ezekiel generator; every constant, count and sentence about the text is re-derived from
Daniel's own landed files. The document is a PURE FUNCTION of the pinned inputs:

  * no clock, no randomness, sorted iteration;
  * every pinned input is opened by a named path under --dan-root and its sha256 is checked against a constant
    held here; every landed output is opened by the path the pinned manifest of landed outputs gives, and its
    sha256 is checked against the digest that manifest holds. No directory is scanned and nothing is tested
    for existence: a missing or changed file is a hard stop.
  * every sentence about the text is a landed file's own string, passed through clean() (a mechanical
    substitution table that the document prints in full); every other sentence is a template string registered
    by T() and printed in the document's last section.

Usage:
  python -B gen_scholar_record.py [--dan-root DIR] [--out-root DIR] [--check]
    --dan-root  inputs; default: the parent of this script's directory
    --out-root  outputs; default: the same as --dan-root
    --check     write nothing; rebuild and compare with the document on disk (exit 1 on a difference)
"""
import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True

DOC_NAME = "DANIEL_SCHOLAR_RECORD.v1.md"
MANIFEST_REL = "close/dan_landed_outputs_manifest.v1.json"
MANIFEST_PREFIX = "sp_durable/Dan/"

# pinned inputs, relative to --dan-root; each digest was read from the build's pinned-input list and is
# re-verified on every run
PINNED = {
    "rows_v1_final.jsonl": "783a0e9ac2c8fe4c942b3b8f7dd65efaefdb28f6fcb55fdde42b500a5c395e09",
    "rows_v1_final.manifest.json": "21568cd63a0dc34f1ae9e18bc590907c723eac89565132dcb5354c10c4cb9bdb",
    MANIFEST_REL: "316676f61170822036032027b1a635ff7a7ee1ad229318b56a7d267b3a1fe378",
    "book_strategy_Dan.md": "158e517af36db3411fe5cb8647fea20a50218b89bcf0338129d558d60b5a20da",
    "fable_end_review/routed_items.v1.jsonl": "42efe601b731e212ba60bc9b19fd9b3199d86e8d5a152bb7571f8e956376b0d6",
    "review/boss/dan_boss_audit.v1.json": "ea70f94e48aed5d24f0adb604c3215a8f6e95ccf940b59da89147de3636a13c3",
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
RULING_RELS = ["review/dan_controlling_agent_rulings_E%d.v1.json" % n for n in range(1, 13)]
NUMBERING_ANCHOR = "MT 3:31-33 = WEB 4:1-3"  # must stand in Daniel's own section-mark file, or the map below is unfounded
SEV_RANK = {"high": 3, "medium": 2, "low": 1, None: 0, "": 0}
SEV_NAME = {3: "high", 2: "medium", 1: "low", 0: "none recorded"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def leaves(v):
    """every non-empty string at any depth, in order"""
    if isinstance(v, str):
        if v.strip():
            yield v
    elif isinstance(v, dict):
        for k in v:
            yield from leaves(v[k])
    elif isinstance(v, list):
        for x in v:
            yield from leaves(x)


class Inputs:
    """Everything read from disk, read once, digest-checked."""

    def __init__(self, dan_root):
        self.root = Path(dan_root)
        self.raw = {}
        for rel in sorted(PINNED):
            b = (self.root / rel).read_bytes()
            if sha(b) != PINNED[rel]:
                raise SystemExit("PINNED INPUT CHANGED: %s has sha256 %s, expected %s" % (rel, sha(b), PINNED[rel]))
            self.raw[rel] = b
        self.rows = [json.loads(l) for l in self.text("rows_v1_final.jsonl").splitlines() if l.strip()]
        self.rows_manifest = self.json("rows_v1_final.manifest.json")
        self.manifest = self.json(MANIFEST_REL)
        self.routed = [json.loads(l) for l in self.text("fable_end_review/routed_items.v1.jsonl").splitlines() if l.strip()]
        self.pmarks = self.json("pmarks_Dan.json")
        self.inventory = self.json("dan_device_inventory.json")
        self.rulings = [(rel, self.json(rel)) for rel in RULING_RELS]
        if NUMBERING_ANCHOR not in str(self.pmarks.get("numbering", "")):
            raise SystemExit("the section-mark file no longer states the numbering zones this generator maps")
        self.outputs = []
        self.landed = {}
        for o in sorted(self.manifest["outputs"], key=lambda x: x["path"]):
            path = o["path"]
            name = path.replace("\\", "/").rsplit("/", 1)[-1]
            e = {"path": path, "name": name, "sha256": o["sha256"], "bytes": o.get("bytes"), "lane": o.get("lane"),
                 "rel": None, "kind": None, "status": None}
            if name.startswith("final_message"):
                e["kind"], e["status"] = "closing_message", "not opened: a closing message, outside this record's inputs"
            elif ":" in path:
                e["kind"], e["status"] = "outside_tree", "not opened: held outside the tree; named by its file name and listed digest only"
            else:
                if not path.startswith(MANIFEST_PREFIX):
                    raise SystemExit("manifest path outside the book: %s" % path)
                rel = path[len(MANIFEST_PREFIX):]
                b = (self.root / rel).read_bytes()
                if sha(b) != o["sha256"]:
                    raise SystemExit("LANDED OUTPUT CHANGED: %s has sha256 %s, manifest says %s" % (rel, sha(b), o["sha256"]))
                e["rel"] = rel
                e["kind"] = classify(rel)
                if e["kind"] in QUOTED_KINDS:
                    self.landed[rel] = json.loads(b.decode("utf-8"))
                    e["status"] = "opened, digest verified, quoted"
                else:
                    e["status"] = "opened, digest verified, not quoted (%s)" % KIND_NOTE[e["kind"]]
            self.outputs.append(e)

    def text(self, rel):
        return self.raw[rel].decode("utf-8")

    def json(self, rel):
        return json.loads(self.text(rel))

    def of_kind(self, kind):
        return [(e, self.landed[e["rel"]]) for e in self.outputs if e["kind"] == kind]


CLASS_RULES = [
    (r"primaries/rev_(LF|OL)_c\d+\.json", "first_reading"),
    (r"primaries/final_(LF|OL)_c\d+_e\d+\.json", "closing_statement"),
    (r"review/peer/peer_g\d+\.json", "reconciling"),
    (r"review/peer/final_peer_g\d+_e\d+\.json", "closing_statement"),
    (r"review/(p13|p13r7|rr8|rr9|rr10)/\1_(OS|TB)\.json", "rereading"),
    (r"review/(p13|p13r7|rr8|rr9|rr10)/\1_(OS|TB)_final_e\d+\.json", "closing_statement"),
    (r"review/boss/dan_boss_audit\.v1\.json", "audit"),
    (r"review/boss/dan_boss_audit_final_e\d+\.json", "closing_statement"),
    (r"review/boss/supp_e2/dan_boss_audit_b8_b14\.json", "audit_supplement"),
    (r"fixup/landed\d*/W\d+_e\d+/fixup\d+_W\d+_changes\.json", "change_log"),
    (r"fixup/landed\d*/W\d+_e\d+/fixup\d+_W\d+_rows\.jsonl", "revised_entries"),
]
QUOTED_KINDS = {"first_reading", "reconciling", "rereading", "audit", "audit_supplement", "change_log"}
KIND_NOTE = {"closing_statement": "a reader's closing statement; the report it closes is quoted instead",
             "revised_entries": "an intermediate revision of the entries; the final entries are a pinned input"}
KIND_LABEL = {"first_reading": "first reading", "reconciling": "reconciling reading", "rereading": "later paired re-reading",
              "audit": "audit", "audit_supplement": "supplementary audit", "change_log": "revision log",
              "closing_statement": "closing statement", "revised_entries": "intermediate entries",
              "closing_message": "closing message", "outside_tree": "revision log held outside the tree"}


def classify(rel):
    for pat, kind in CLASS_RULES:
        if re.fullmatch(pat, rel):
            return kind
    raise SystemExit("UNCLASSIFIED LANDED OUTPUT: %s (the generator must not omit it silently)" % rel)


# ---------------------------------------------------------------- references

def web_to_mt(c, v):
    if c == 4 and 1 <= v <= 3:
        return 3, 30 + v
    if c == 4 and v >= 4:
        return 4, v - 3
    if c == 5 and v == 31:
        return 6, 1
    if c == 6:
        return 6, v + 1
    return c, v


def parse_span(span):
    m = re.fullmatch(r"Dan\.(\d+)\.(\d+)-Dan\.(\d+)\.(\d+)", span)
    if not m:
        raise SystemExit("unreadable span: %r" % span)
    return tuple(int(x) for x in m.groups())


def fmt_range(c1, v1, c2, v2):
    if (c1, v1) == (c2, v2):
        return "%d:%d" % (c1, v1)
    if c1 == c2:
        return "%d:%d–%d" % (c1, v1, v2)
    return "%d:%d–%d:%d" % (c1, v1, c2, v2)


def short_ref(span):
    return "Daniel " + fmt_range(*parse_span(span))


def full_ref(span):
    c1, v1, c2, v2 = parse_span(span)
    m1, m2 = web_to_mt(c1, v1), web_to_mt(c2, v2)
    out = "Daniel " + fmt_range(c1, v1, c2, v2)
    if m1 != (c1, v1) or m2 != (c2, v2):
        out += " (Hebrew numbering %s)" % fmt_range(m1[0], m1[1], m2[0], m2[1])
    return out


# ---------------------------------------------------------------- the substitution table

FIELD_NAMES = [
    ("boundary_evidence_refs", "the evidence list"),
    ("boundary_rationale", "the stated reason for the boundary"),
    ("strongest_rejected_alternative", "the strongest alternative considered"),
    ("observed_substrate_signals", "the observed signals"),
    ("strong_or_hebrew_tags_used", "the lexical tags"),
    ("literature_type_guess", "the literary type"),
    ("device_notes", "the formula notes"),
    ("unit_type", "the unit type"),
    ("writer_decision_id", "the entry number"),
    ("decision_id", "the entry number"),
    ("medium_low", "medium-low"),
]
FILE_NAMES = [
    (r"pmarks_Dan\.json", "the section-mark layer"),
    (r"dan_device_inventory\.json", "the formula inventory"),
    (r"dan_language_zones\.json", "the language-zone layer"),
    (r"Dan_oshb\.txt", "the Hebrew-Aramaic text"),
    (r"Dan_web_clean\.txt", "the English text"),
    (r"book_strategy_Dan\.md", "the reading plan for the book"),
]
TIER_WORDS = [("MEASURED", "counted"), ("EXTRACTED", "read from the source"), ("TRANSCRIBED", "copied"),
              ("REPORTED", "reported"), ("INFERRED", "interpretive"), ("ASSUMED", "assumed"),
              ("UNAVAILABLE", "unavailable"), ("NOT_TESTABLE", "not testable"), ("CONFIRM", "confirm"),
              ("RETURN", "return")]
PROCESS_NOUNS = [
    (r"\bcontrolling[- ]agent(?:'s)?\b", "adjudicator"),
    (r"\bboss[- ]audit(?:or)?\b", "audit"),
    (r"\bboss\b", "audit"),
    (r"\bend[- ]review\b", "final review"),
    (r"\bfix-?ups?\b", "revision"),
    (r"\borchestrator(?:'s)?\b", "editor"),
    (r"\bsub-?agents?\b", "reader"),
    (r"\bthe brief(?:'s)?\b", "the instructions"),
    (r"\bbriefs?\b", "instructions"),
    (r"\bpackets?\b", "report"),
    (r"\bvalidator suite\b|\bsuite runner\b", "automated checks"),
    (r"\bvalidators?\b", "automated check"),
    (r"\bledger\b", "log"),
    (r"\breceipts?\b", "start record"),
    (r"\bworklist\b", "list of work"),
    (r"\bFable\b", "the final reviewer"),
    (r"\bclaude-opus-[\d-]+\b|\bOpus\b|\bClaude\b", "the model"),
    (r"\bgrader[_ ]fallback\b", "a substitute model"),
    (r"\bsha256\b", "digest"),
    (r"\bregex\b", "search pattern"),
    (r"(?<!king's )(?<!king’s )\bgates?\b", "checkpoint"),
    (r"\bwriter(?:'s)?\b", "drafter"),
    (r"\bexecution e?(\d+)\b", r"pass \1"),
    (r"\bexecution\b", "pass"),
    (r"\battempts?\b", "pass"),
    (r"\bagent_id\b|\bagent ids?\b", "run identity"),
    (r"\bagents?\b", "reader"),
]
LANE_NAMES = [("LF", "reading A"), ("OL", "reading B"), ("OS", "the scope reading"), ("TB", "the text reading")]
CODE_KEEP = {"WEB", "MT", "OSHB", "WLC", "PE", "SAMEKH", "LXX", "KJV", "BHS", "A", "H", "I", "II", "III"}
CODE_FAMILIES = [("CWO", "a standing order"), ("TRIAGE", "an early screening question"), ("FIXUP", "a revision round"),
                 ("OW", "an owner directive"), ("E", "a logged error")]


def _plural(word_s, word_p):
    def f(m):
        t = m.group(0)
        out = word_p if t.lower().endswith("s") else word_s
        return out.capitalize() if t[0].isupper() else out
    return f


class Cleaner:
    """clean() = scripture references for entry numbers, then the printed table of private terms."""

    def __init__(self, inp):
        self.by_id = {}
        for r in inp.rows:
            self.by_id[r["decision_id"]] = r
            self.by_id[r["writer_decision_id"]] = r
        self.unknown_ids = Counter()
        self.devices = []
        for k in sorted(inp.inventory.get("formulae", {}), key=lambda s: (-len(s), s)):
            g = inp.inventory["formulae"][k]
            gloss = g.get("gloss") if isinstance(g, dict) else None
            self.devices.append((k, "the formula “%s”" % " ".join(str(gloss).split()) if gloss else k.replace("_", " ")))
        self.table = self._build()

    def row_of(self, rid):
        return self.by_id.get(rid)

    def _rid(self, m):
        r = self.by_id.get(m.group(0))
        if r is None:
            self.unknown_ids[m.group(0)] += 1
            return "an entry outside the final set"
        return short_ref(r["span"])

    def _code(self, m):
        t = m.group(0)
        if re.fullmatch(r"W\d-\d{1,3}", t):
            return t
        parts = t.split("-")
        if all(p in CODE_KEEP or p.isdigit() for p in parts):
            return t
        ids = [x for x in re.findall(r"W\d-\d{3}", t) if x in self.by_id]
        if ids:
            return "the adjudication on " + short_ref(self.by_id[ids[0]]["span"])
        for fam, word in CODE_FAMILIES:
            if parts[0] == fam:
                return word
        return "a numbered adjudication item"

    def _build(self):
        t = []
        t.append((r"`", "", "(removed)"))
        t.append((r"\b[a-z0-9_]+_a\d+(?:#e\d+)?\b", "an earlier pass", "an earlier pass"))
        t.append((r"#e\d+\b", "", "(removed)"))
        t.append((r"\b[0-9a-f]{64}\b|\b[0-9a-f]{6,}\.\.\.[0-9a-f]{4,}\b", "(digest omitted)", "(digest omitted)"))
        t.append((r"(?:[A-Za-z]:)?(?:[\w.-]+[\\/])+(?=[\w.-]+\.(?:jsonl|json|py|md|txt)\b)", "", "(directory prefix removed)"))
        for pat, rep in FILE_NAMES:
            t.append((r"\b" + pat, rep, rep))
        t.append((r"\b[\w.-]+\.(?:jsonl|json|py|md|txt)\b", "a working file", "a working file"))
        t.append((r"(?<![\w.])\.(?:jsonl|json|py|md)\b", "file-suffix", "file-suffix"))
        t.append((r"\b(W\d-\d{3})\.(?=[a-z_]+)", r"\1 ", "(the joining dot removed)"))
        t.append((r"\bM8[_ ]fable\b", "the project", "the project"))
        for k, rep in self.devices:
            t.append((r"\b" + re.escape(k) + r"\b", rep, rep))
        for k, rep in FIELD_NAMES:
            t.append((r"\b" + re.escape(k) + r"\[(\d+)\]", rep + r", item \1 (counted from 0)", rep + ", item N (counted from 0)"))
            t.append((r"\b" + re.escape(k) + r"\b", rep, rep))
        for k, rep in TIER_WORDS:
            t.append((r"\b" + k + r"\b", rep, rep))
        t.append((r"\b[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+\b", lambda m: m.group(0).replace("_", " "),
                  "the same words with spaces for underscores"))
        t.append((r"\bweb:Dan\.(\d+)\.(\d+)", r"\1:\2 (English numbering)", "chapter:verse (English numbering)"))
        t.append((r"\boshb:Dan\.(\d+)\.(\d+)", r"\1:\2 (Hebrew numbering)", "chapter:verse (Hebrew numbering)"))
        t.append((r"\bDan\.(\d+)\.(\d+)", r"\1:\2", "chapter:verse"))
        t.append((r"\bW(\d{1,2})#(\d+)\b", r"revision note \1.\2", "revision note N.M"))
        t.append((r"(?<![\w-])(?:[A-Z][A-Z0-9]*-)+[A-Z0-9]+(?![\w])", self._code,
                  "the adjudication on <passage>, or a standing order, an early screening question, a revision round, "
                  "an owner directive, a logged error, or a numbered adjudication item"))
        t.append((r"\bW\d-\d{3}\b", self._rid, "the passage's scripture reference"))
        t.append((r"\bW\d-\d{1,2}\b", self._rid, "the passage's scripture reference"))
        t.append((r"\bW([1-6])\b", r"drafting part \1", "drafting part N"))
        t.append((r"\bW(\d{1,2})\b", r"revision set \1", "revision set N"))
        t.append((r"(?i)\bfix-?up[ -]?(\d+)\b", r"revision round \1", "revision round N"))
        t.append((r"(?i)\b(?:rr\d+|p13r7|p13)\b", "a later re-reading", "a later re-reading"))
        t.append((r"(?i)\btier(?:ed|ing)\b", "graded for evidence", "graded for evidence"))
        t.append((r"(?i)\btiers\b", "evidence grades", "evidence grades"))
        t.append((r"(?i)\btier\b", "evidence grade", "evidence grade"))
        t.append((r"(?i)\blaunch(?:es|ed)?\b", "start", "start"))
        t.append((r"(?i)\bsuite\b", "set of automated checks", "set of automated checks"))
        t.append((r"(?i)\bpeers\b", "reconciling readings", "reconciling readings"))
        t.append((r"(?i)\bpeer\b", "reconciling reading", "reconciling reading"))
        t.append((r"(?i)\bprimaries\b", "first readings", "first readings"))
        t.append((r"(?i)\bexecutions\b", "passes", "passes"))
        for pat, rep in PROCESS_NOUNS:
            t.append((r"(?i)" + pat, rep, rep.replace("\\1", "N")))
        t.append((r"(?i)\blanes\b", _plural("reading", "readings"), "readings"))
        t.append((r"(?i)\blane\b", _plural("reading", "readings"), "reading"))
        t.append((r"(?i)\brows\b", _plural("entry", "entries"), "entries"))
        t.append((r"(?i)\brow\b", _plural("entry", "entries"), "entry"))
        for k, rep in LANE_NAMES:
            t.append((r"\b" + k + r"\b", rep, rep))
        t.append((r"\bE(\d{1,2})\b", r"adjudication round \1", "adjudication round N"))
        t.append((r"\bB(\d{1,2})\b", r"audit condition \1", "audit condition N"))
        t.append((r"\bP(\d{1,2})\b", r"review condition \1", "review condition N"))
        t.append((r"\bF(\d{1,2})\b", r"finding \1", "finding N"))
        t.append((r"\b[cg](\d{2})\b", r"group \1", "group N"))
        t.append((r"\be(\d{1,2})\b", r"pass \1", "pass N"))
        t.append((r"\b[A-Z]\d{1,2}(?:-[a-z])?\b", "a numbered rule", "a numbered rule"))
        t.append((r"\b(?:the|a|an) (the|an?) ", r"\1 ", "(a doubled article left by a substitution reduced to the second)"))
        return [(re.compile(p), r, d, p) for p, r, d in t]

    def clean(self, s):
        s = " ".join(str(s).split())
        for rx, rep, _d, _p in self.table:
            s = rx.sub(rep, s)
        return " ".join(s.split())


# ---------------------------------------------------------------- the document

class Doc:
    def __init__(self):
        self.lines = []
        self.templates = []
        self.seen = set()

    def T(self, s):
        if s not in self.seen:
            self.seen.add(s)
            self.templates.append(s)
        return s

    def add(self, s=""):
        self.lines.append(s)


def row_ids_in(v, cl):
    out = []
    for x in re.findall(r"W\d-\d{1,3}", json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v):
        r = cl.row_of(x)
        if r is not None and r["decision_id"] not in out:
            out.append(r["decision_id"])
    return out


def collect(inp, cl):
    """All per-passage material, keyed by the entry's own number. Shared with the checker."""
    C = {"first": defaultdict(dict), "peer": {}, "audit": {}, "reread": defaultdict(list), "rulings": defaultdict(list),
         "class_rulings": [], "changes": Counter(), "pair_disagree": []}
    for e, d in inp.of_kind("first_reading"):
        lane = re.search(r"rev_(LF|OL)_", e["rel"]).group(1)
        for it in d.get("items", []):
            r = cl.row_of(it.get("row_id"))
            if r is None:
                raise SystemExit("first reading names an entry outside the final set: %r" % it.get("row_id"))
            C["first"][r["decision_id"]][lane] = it
    for e, d in inp.of_kind("reconciling"):
        for it in d.get("items", []):
            r = cl.row_of(it.get("row_id"))
            if r is None:
                raise SystemExit("reconciling reading names an entry outside the final set: %r" % it.get("row_id"))
            C["peer"][r["decision_id"]] = it
    for e, d in inp.of_kind("audit"):
        for it in d.get("rows", []):
            r = cl.row_of(it.get("row"))
            if r is None:
                raise SystemExit("audit names an entry outside the final set: %r" % it.get("row"))
            C["audit"][r["decision_id"]] = it
    stages = defaultdict(dict)
    for e, d in inp.of_kind("rereading"):
        m = re.fullmatch(r"review/(\w+)/\1_(OS|TB)\.json", e["rel"])
        stage, lane = m.group(1), m.group(2)
        stages[stage][lane] = d
        for it in d.get("items", []):
            if it.get("verdict") != "support":
                for rid in row_ids_in(it.get("row", ""), cl):
                    C["reread"][rid].append((stage, lane, "item", it))
        for it in d.get("extra_findings", []):
            for rid in row_ids_in(it.get("row", ""), cl):
                C["reread"][rid].append((stage, lane, "extra", it))
    for stage in sorted(stages):
        if set(stages[stage]) == {"OS", "TB"}:
            a = {it.get("record"): it for it in stages[stage]["OS"].get("items", [])}
            b = {it.get("record"): it for it in stages[stage]["TB"].get("items", [])}
            for rec in sorted(set(a) | set(b), key=lambda s: [int(x) for x in re.findall(r"\d+", str(s))]):
                va = a[rec].get("verdict") if rec in a else "no finding"
                vb = b[rec].get("verdict") if rec in b else "no finding"
                if va != vb:
                    C["pair_disagree"].append((stage, rec, (a.get(rec) or b.get(rec)), va, vb))
    for rel, d in inp.rulings:
        n = int(re.search(r"_E(\d+)\.", rel).group(1))
        for ru in d.get("rulings", []):
            ids = row_ids_in([ru.get("id", ""), [o.get("row") for o in ru.get("orders", []) if isinstance(o, dict)]], cl)
            if 1 <= len(ids) <= 3:
                for rid in ids:
                    C["rulings"][rid].append((n, ru))
            else:
                C["class_rulings"].append((n, ru, len(ids)))
    for e, d in inp.of_kind("change_log"):
        for ch in d.get("changes", []):
            for rid in row_ids_in(ch.get("row", ""), cl):
                C["changes"][rid] += 1
    return C


def severities_for(rid, C):
    out = []
    for lane in sorted(C["first"].get(rid, {})):
        out.append(C["first"][rid][lane].get("severity"))
    for pf in (C["peer"].get(rid) or {}).get("primary_findings", []) or []:
        out.append(pf.get("severity"))
    out.append((C["peer"].get(rid) or {}).get("proposal_severity"))
    for f in (C["audit"].get(rid) or {}).get("findings", []) or []:
        out.append(f.get("severity"))
    for _s, _l, _k, it in C["reread"].get(rid, []):
        out.append(it.get("severity"))
    return max([SEV_RANK.get(s, 0) for s in out] or [0])


def first_disagree(rid, C):
    f = C["first"].get(rid, {})
    kinds = []
    va, vb = (f.get("LF") or {}).get("verdict"), (f.get("OL") or {}).get("verdict")
    if va != vb:
        kinds.append("verdict")
    elif va == "challenge" and (f["LF"].get("decision") != f["OL"].get("decision")):
        kinds.append("remedy")
    if (C["peer"].get(rid) or {}).get("lanes_disagreed") is True:
        kinds.append("recorded")
    return kinds


def is_dispute(rid, C):
    f = C["first"].get(rid, {})
    if any((f.get(l) or {}).get("verdict") != "support" for l in ("LF", "OL")):
        return True
    if first_disagree(rid, C) or C["reread"].get(rid):
        return True
    return bool((C["audit"].get(rid) or {}).get("findings"))


def build(dan_root):
    inp = Inputs(dan_root)
    cl = Cleaner(inp)
    C = collect(inp, cl)
    D = Doc()
    T, A = D.T, D.add
    q = lambda s: A("> " + cl.clean(s))

    def quote_all(label, v):
        ls = [x for x in leaves(v)]
        if ls:
            A(label)
            A()
            for x in ls:
                q(x)
                A()

    rows = inp.rows
    order = {r["decision_id"]: i for i, r in enumerate(rows)}
    disputes = sorted([r for r in rows if is_dispute(r["decision_id"], C)],
                      key=lambda r: (-severities_for(r["decision_id"], C), order[r["decision_id"]]))
    quiet = [r for r in rows if not is_dispute(r["decision_id"], C)]
    kinds = Counter(e["kind"] for e in inp.outputs)

    A(T("# The division of Daniel into reading units: a record of what was disputed"))
    A()
    A(T("This record is generated mechanically from the reports of the readers who examined a proposed division of the book of Daniel into %d reading units. It is written for a reader of Daniel, not for a reader of the project that produced it: passages are named by chapter and verse, in the English numbering, with the Hebrew numbering added where the two differ.") % len(rows))
    A()
    A(T("Every quotation set off with a rule at the left is a reader's own sentence, altered only by the mechanical substitutions listed in full near the end. Every other sentence is the generator's own frame, and every such sentence is printed in the last section so that the frame can be inspected apart from the evidence."))
    A()
    A(T("This record makes no judgement of its own. It changes no unit, weighs no boundary and settles no dispute; it reports what the readers wrote. Its limits are stated in section 2 and are not small."))
    A()

    # ---- 1
    A(T("## 1. What made this book difficult"))
    A()
    lang = Counter(r.get("language") for r in rows)
    A(T("Daniel is written in two languages. Of the %d units, %d lie in Hebrew, %d in Aramaic and %d cross from one to the other (%s). The formula inventory counts %s verses in %s chapters.") % (
        len(rows), lang.get("H", 0), lang.get("A", 0), lang.get("mixed", 0),
        "; ".join(full_ref(r["span"]) for r in rows if r.get("language") == "mixed") or "none",
        inp.inventory.get("totals", {}).get("verses"), inp.inventory.get("totals", {}).get("chapters")))
    A()
    A(T("The Hebrew and English traditions number the verses differently in four stretches, so that a boundary stated in one numbering can be misread in the other. The section-mark layer states the difference in these words:"))
    A()
    q(inp.pmarks.get("numbering", ""))
    A()
    marks = Counter(m for k in sorted(inp.pmarks.get("marks", {})) for m in inp.pmarks["marks"][k])
    A(T("The Hebrew text carries paragraph marks, and the division had to decide how much weight each bears. The section-mark layer holds %d marked verses: %s.") % (
        len(inp.pmarks.get("marks", {})), ", ".join("%d %s" % (marks[k], k) for k in sorted(marks))))
    A()
    for key in ("marks_note",):
        if isinstance(inp.pmarks.get(key), str):
            q(inp.pmarks[key])
            A()
    A(T("The book marks time with date notices and recurring formulae, and several of the disputes below turn on whether a formula opens a unit or merely continues one. The formula inventory records %s date notices and the following formulae:") % inp.inventory.get("datelines", {}).get("count"))
    A()
    for k in sorted(inp.inventory.get("formulae", {})):
        g = inp.inventory["formulae"][k]
        if isinstance(g, dict):
            A(T("- “%s” (%s): %s occurrences") % (cl.clean(g.get("gloss")), cl.clean(g.get("language")), g.get("count")))
    A()
    conf = Counter(r.get("confidence") for r in rows)
    A(T("The division as it stands is not confident. Its own grades of confidence are: %s. Its unit types are: %s.") % (
        "; ".join("%s, %d" % (cl.clean(k), conf[k]) for k in sorted(conf)),
        "; ".join("%s, %d" % (cl.clean(k), n) for k, n in sorted(Counter(r.get("unit_type") for r in rows).items()))))
    A()

    # ---- 2
    A(T("## 2. How the division was examined, and what that does and does not establish"))
    A()
    A(T("The division was read in stages. Two first readings, here called reading A and reading B, each examined every unit without sight of the other (%d reports, %d findings). A reconciling reading then took both and said which stood (%d reports, %d findings). The entries were revised in rounds (%d revision logs opened here, with %d recorded changes), and the later revisions were re-read in pairs, one reading attending to scope and one to the text (%d reports). An audit followed (%d report and %d supplement). An adjudicator ruled between the stages (%d rounds, %d rulings).") % (
        kinds["first_reading"], sum(len(d.get("items", [])) for _e, d in inp.of_kind("first_reading")),
        kinds["reconciling"], sum(len(d.get("items", [])) for _e, d in inp.of_kind("reconciling")),
        kinds["change_log"], sum(len(d.get("changes", [])) for _e, d in inp.of_kind("change_log")),
        kinds["rereading"], kinds["audit"], kinds["audit_supplement"],
        len(inp.rulings), sum(len(d.get("rulings", [])) for _r, d in inp.rulings)))
    A()
    A(T("What this does not establish. Every reading at every stage was produced by one family of language model. Where two readings agree, that is one voice heard twice, not two independent witnesses, and agreement in this record must never be taken as confirmation. No human scholar has examined any unit. No reading consulted a version, a manuscript or a commentary beyond the two witnesses named in section 8. The readers said as much themselves; their own statements of limit are collected in section 6."))
    A()
    A(T("Of the %d files the project lists as landed, %d were opened and quoted, %d were opened and checked but not quoted, and %d were not opened (%d closing messages and %d revision logs held outside the tree). Section 7 lists every one.") % (
        len(inp.outputs), sum(1 for e in inp.outputs if e["kind"] in QUOTED_KINDS),
        kinds["closing_statement"] + kinds["revised_entries"], kinds["closing_message"] + kinds["outside_tree"],
        kinds["closing_message"], kinds["outside_tree"]))
    A()

    # ---- 3
    A(T("## 3. The disputes"))
    A()
    A(T("A passage appears here if either first reading challenged its entry, if the first readings differed, if a later re-reading challenged it or added a finding on it, or if the audit recorded a finding on it. %d of the %d units appear. They are ordered by the highest severity any reader assigned, then by their place in the book. Severity is the readers' own grade; most challenges concern how an entry words or supports its boundary, not where the boundary falls.") % (len(disputes), len(rows)))
    A()
    sevc = Counter(SEV_NAME[severities_for(r["decision_id"], C)] for r in disputes)
    A(T("By highest severity: %s.") % "; ".join("%s, %d" % (k, sevc[k]) for k in ("high", "medium", "low", "none recorded") if sevc[k]))
    A()
    for r in disputes:
        rid = r["decision_id"]
        A(T("### %s — highest severity: %s") % (full_ref(r["span"]), SEV_NAME[severities_for(rid, C)]))
        A()
        A(T("The unit as it stands: language %s; type %s; confidence %s.") % (
            {"A": "Aramaic", "H": "Hebrew"}.get(r.get("language"), r.get("language")), cl.clean(r.get("unit_type")), cl.clean(r.get("confidence"))))
        A()
        A(T("The stated reason for the boundary, as the entry now reads:"))
        A()
        quote_all(T("(the entry's own words)"), r.get("boundary_rationale"))
        quote_all(T("The strongest alternative the entry considered and declined:"), r.get("strongest_rejected_alternative"))
        A(T("**Evidence on each side.**"))
        A()
        f = C["first"].get(rid, {})
        for lane, name in (("LF", "Reading A"), ("OL", "Reading B")):
            it = f.get(lane)
            if it is None:
                A(T("%s left no finding on this passage.") % name)
                A()
                continue
            A(T("%s: verdict %s; severity %s; its proposed course:") % (name, it.get("verdict"), it.get("severity") or "none given"))
            A()
            q(it.get("decision", ""))
            A()
            quote_all(T("Its claim:"), it.get("claim"))
            quote_all(T("The two sides as it set them out:"), it.get("both_sides"))
            quote_all(T("The evidence it cited:"), it.get("evidence"))
            quote_all(T("The correction it suggested:"), it.get("suggested_fix"))
        dk = first_disagree(rid, C)
        if dk:
            A(T("**The first readings disagreed here** (%s).") % ", ".join(
                {"verdict": "their verdicts differ", "remedy": "both challenged but proposed different courses",
                 "recorded": "the reconciling reading recorded a disagreement"}[k] for k in dk))
        else:
            A(T("The first readings did not disagree here."))
        A()
        A(T("**Resolution.**"))
        A()
        p = C["peer"].get(rid)
        if p:
            quote_all(T("The reconciling reading said which reading stands:"), p.get("which_reading_stands"))
            quote_all(T("Its reason, from the text:"), p.get("why_from_the_bytes"))
            for pf in p.get("primary_findings", []) or []:
                A(T("It held the finding of %s (severity %s) to be %s, on this basis:") % (
                    cl.clean(pf.get("lane", "")), pf.get("severity"), pf.get("state")))
                A()
                for x in leaves(pf.get("basis")):
                    q(x)
                    A()
            if p.get("proposed_span_change") is not None:
                quote_all(T("It proposed a change to the extent of the unit:"), p.get("proposed_span_change"))
            if p.get("proposed_confidence_change") is not None:
                quote_all(T("It proposed a change of confidence:"), p.get("proposed_confidence_change"))
            if p.get("proposed_text_change"):
                quote_all(T("It proposed a change of wording (severity %s):") % (p.get("proposal_severity") or "none given"), p.get("proposed_text_change"))
        else:
            A(T("No reconciling finding exists for this passage."))
            A()
        for n, ru in C["rulings"].get(rid, []):
            A(T("The adjudicator, in round %d, ruled (%s):") % (n, cl.clean(ru.get("ruling", ""))))
            A()
            for x in leaves([ru.get("decision"), ru.get("reason")]):
                q(x)
                A()
        for stage, lane, kind, it in C["reread"].get(rid, []):
            A(T("A later re-reading (%s) %s (severity %s) on %s:") % (
                cl.clean(lane), {"item": "challenged a revision", "extra": "added a finding"}[kind],
                it.get("severity") or "none given", cl.clean(it.get("field", ""))))
            A()
            for x in leaves([it.get("claim"), it.get("decision")]):
                q(x)
                A()
        a = C["audit"].get(rid)
        if a:
            A(T("The audit's verdict on the entry: %s.") % cl.clean(a.get("verdict", "")))
            A()
            quote_all(T("Its reason:"), a.get("why"))
            for fd in a.get("findings", []) or []:
                A(T("The audit recorded a finding (severity %s) on %s:") % (fd.get("severity"), cl.clean(fd.get("field", ""))))
                A()
                for x in leaves([fd.get("claim"), fd.get("evidence")]):
                    q(x)
                    A()
        A(T("Recorded changes to this entry across all revision rounds: %d.") % C["changes"].get(rid, 0))
        A()
    A(T("### Passages on which no reader raised anything"))
    A()
    A(T("%d units were supported by both first readings and drew no later finding: %s.") % (
        len(quiet), "; ".join(full_ref(r["span"]) for r in quiet) or "none"))
    A()

    # ---- 4
    A(T("## 4. What changed"))
    A()
    A(T("No reconciling reading proposed moving a boundary or changing a grade of confidence: across the %d reconciling findings, %d proposed a change to a unit's extent, %d a change of confidence and %d a change of wording.") % (
        len(C["peer"]), sum(1 for p in C["peer"].values() if p.get("proposed_span_change") is not None),
        sum(1 for p in C["peer"].values() if p.get("proposed_confidence_change") is not None),
        sum(1 for p in C["peer"].values() if p.get("proposed_text_change"))))
    A()
    A(T("The revision logs record the following. Each line is one log; the counts are of its own change records, by the part of the entry changed."))
    A()
    for e, d in inp.of_kind("change_log"):
        ch = d.get("changes", [])
        byf = Counter(cl.clean(re.sub(r"\[\d+\]", "", str(c.get("field")))) for c in ch)
        m = re.search(r"fixup(\d+)_W(\d+)_changes", e["rel"])
        A(T("- Revision round %s, set %s: %d changes on %d passages (%s); %d ordered changes not made; %d claims found contradicted by the text.") % (
            m.group(1), m.group(2), len(ch), len({x for c in ch for x in row_ids_in(c.get("row", ""), cl)}),
            "; ".join("%s, %d" % (k, byf[k]) for k in sorted(byf)) or "none",
            len(d.get("blocked", []) or []) + len(d.get("not_applied", []) or []), len(d.get("contradicted", []) or [])))
        for b in (d.get("blocked", []) or []) + (d.get("not_applied", []) or []):
            if isinstance(b, dict):
                A()
                A(T("  Not made, on %s (%s), for this reason:") % (cl.clean(b.get("row", "")), cl.clean(b.get("field", ""))))
                A()
                for x in leaves(b.get("why")):
                    q(x)
        for b in d.get("contradicted", []) or []:
            if isinstance(b, dict):
                A()
                A(T("  Contradicted by the text, on %s (%s):") % (cl.clean(b.get("row", "")), cl.clean(b.get("field", ""))))
                A()
                for x in leaves([b.get("claim"), b.get("bytes")]):
                    q(x)
                    A()
    A()
    A(T("%d further revision logs are listed as landed but are held outside the tree and were not opened; what they changed is not reported here.") % kinds["outside_tree"])
    A()

    # ---- 5
    A(T("## 5. The later re-readings, the adjudication and the audit"))
    A()
    for e, d in inp.of_kind("rereading"):
        m = re.fullmatch(r"review/(\w+)/\1_(OS|TB)\.json", e["rel"])
        its = d.get("items", [])
        A(T("- Re-reading stage %s, %s: %d findings (%d support, %d challenge) and %d further findings.") % (
            m.group(1).replace("p13r7", "2").replace("p13", "1").replace("rr8", "3").replace("rr9", "4").replace("rr10", "5"),
            cl.clean(m.group(2)), len(its), sum(1 for i in its if i.get("verdict") == "support"),
            sum(1 for i in its if i.get("verdict") != "support"), len(d.get("extra_findings", []) or [])))
    A()
    A(T("Each stage was read twice, and the two readings did not always agree. They gave different verdicts on %d revisions:") % len(C["pair_disagree"]))
    A()
    for stage, rec, it, va, vb in C["pair_disagree"]:
        A(pair_line(cl, T, stage, rec, it, va, vb))
    A()
    A(T("The first readings were also each asked a small set of screening questions. Where a reading answered one for its part of the book, its answer was:"))
    A()
    for e, d in inp.of_kind("first_reading"):
        for ta in d.get("triage_answers", []) or []:
            if isinstance(ta, dict) and ta.get("in_my_cluster"):
                A(T("- %s, on %s:") % ({"LF": "Reading A", "OL": "Reading B"}[re.search(r"rev_(LF|OL)_", e["rel"]).group(1)],
                                       "; ".join(short_ref(cl.row_of(x)["span"]) for x in row_ids_in(ta.get("rows", ""), cl)) or "no named passage"))
                A()
                for x in leaves(ta.get("decision")):
                    q(x)
                    A()
    A(T("Adjudications that concern a class of entries or more than three passages, and so are not placed under a single passage in section 3 (%d):") % len(C["class_rulings"]))
    A()
    for n, ru, k in C["class_rulings"]:
        A(T("- Round %d, bearing on %d named passages (%s):") % (n, k, cl.clean(ru.get("ruling", ""))))
        A()
        for x in leaves(ru.get("decision")):
            q(x)
            A()
    for e, d in inp.of_kind("audit"):
        cv = Counter(c.get("verdict") for c in d.get("conditions", []))
        ov = d.get("overall", {})
        A(T("The audit tested %d conditions (%s) and gave a verdict on each of %d entries (%s). **Its overall verdict was: %s.** That verdict is reported here as it was given and is not softened: the audit did not pass the division outright.") % (
            len(d.get("conditions", [])), "; ".join("%s, %d" % (cl.clean(k), cv[k]) for k in sorted(cv)),
            len(d.get("rows", [])), "; ".join("%s, %d" % (cl.clean(k), n) for k, n in sorted(Counter(x.get("verdict") for x in d.get("rows", [])).items())),
            cl.clean(ov.get("verdict", ""))))
        A()
        for c in d.get("conditions", []):
            if c.get("verdict") != "MET":
                A(T("A condition the audit could not settle (%s):") % cl.clean(c.get("verdict", "")))
                A()
                for x in leaves([c.get("how"), c.get("evidence")]):
                    q(x)
                    A()
        quote_all(T("Matters the audit raised for decision:"), d.get("escalations"))
        quote_all(T("Places where the audit found something reported that should have been counted:"), d.get("reported_where_measured"))
    for e, d in inp.of_kind("audit_supplement"):
        A(T("A supplementary audit later took up the conditions the first could not settle. Its verdicts (%s) are its own and rest on the grounds it states:") % "; ".join(
            "%s, %s" % (cl.clean(c.get("verdict", "")), cl.clean(c.get("tier", ""))) for c in d.get("conditions", [])))
        A()
        for c in d.get("conditions", []):
            for x in leaves([c.get("condition_text"), c.get("how"), c.get("why_it_suffices")]):
                q(x)
                A()
    A(T("How the two audits were joined into the standing of the final entries is stated by the list that accompanies those entries, in these words:"))
    A()
    for k in ("basis", "holds", "boss_audit", "audit"):
        for x in leaves(inp.rows_manifest.get(k)):
            q(x)
            A()

    # ---- 6
    A(T("## 6. What remains open"))
    A()
    A(T("%d questions are carried open. None is settled by anything in this record. Each awaits a final review that has not yet taken place; until it does, each stands exactly as written here.") % len(inp.routed))
    A()
    for i, it in enumerate(inp.routed, 1):
        A(T("### Open question %d") % i)
        A()
        A(T("How it was left (%s):") % cl.clean(it.get("ruling", "")))
        A()
        for x in leaves(it.get("decision")):
            q(x)
            A()
        quote_all(T("What was asked of the final review:"), it.get("order"))
        A(T("Status: open."))
        A()
    A(T("### Limits the readers stated themselves"))
    A()
    A(T("Each reader was required to say what it could not establish. Those statements follow, grouped by stage, each with the reader's own account of why it matters. Repeated statements are printed once."))
    A()
    seen = set()
    groups = [(T("**First readings.**"), [d for _e, d in inp.of_kind("first_reading")]),
              (T("**Reconciling readings.**"), [d for _e, d in inp.of_kind("reconciling")]),
              (T("**Later re-readings.**"), [d for _e, d in inp.of_kind("rereading")]),
              (T("**The audit and its supplement.**"), [d for _e, d in inp.of_kind("audit")] + [d for _e, d in inp.of_kind("audit_supplement")]),
              (T("**The adjudicator.**"), [d for _r, d in inp.rulings])]
    for name, ds in groups:
        A(name)
        A()
        for d in ds:
            for u in d.get("unresolved_uncertainty", []) or []:
                parts = [x for x in leaves(u)]
                key = tuple(cl.clean(x) for x in parts)
                if not parts or key in seen:
                    continue
                seen.add(key)
                for x in parts:
                    q(x)
                A()

    # ---- 7
    A(T("## 7. Provenance"))
    A()
    A(T("Every file the project lists as landed for Daniel, with the digest that list gives for it. A file marked as opened had its digest recomputed and matched before any word of it was used."))
    A()
    A("| record | kind | sha256 | use |")
    A("|---|---|---|---|")
    for e in inp.outputs:
        A("| %s | %s | %s | %s |" % (e["rel"] or e["name"], KIND_LABEL[e["kind"]], e["sha256"], e["status"]))
    A()
    A(T("Pinned inputs that are not in that list, with the digest this generator holds and verifies for each:"))
    A()
    A("| record | sha256 |")
    A("|---|---|")
    for rel in sorted(PINNED):
        A("| %s | %s |" % (rel, PINNED[rel]))
    A()
    A(T("Key from the passages of section 3 to the entry numbers the reports use:"))
    A()
    A("| passage | entry numbers |")
    A("|---|---|")
    for r in rows:
        A("| %s | %s, %s |" % (full_ref(r["span"]), r["decision_id"], r["writer_decision_id"]))
    A()
    A(T("Key from the open questions of section 6 to the identifiers the project uses:"))
    A()
    A("| open question | identifier | raised at |")
    A("|---|---|---|")
    for i, it in enumerate(inp.routed, 1):
        A("| %d | %s | %s |" % (i, it.get("id"), " ".join(str(it.get("from")).split()).replace("|", "/")))
    A()

    # ---- 8
    A(T("## 8. Licence and attribution"))
    A()
    A(T("The Hebrew and Aramaic text is from the Open Scriptures Hebrew Bible, a transcription of the Westminster Leningrad Codex, released into the public domain by its transcribers; the morphological annotation is distributed under the Creative Commons Attribution 4.0 licence and is attributed to the Open Scriptures project. The English text is the World English Bible, which is in the public domain. Quotations of either witness above carry these terms with them. This record makes no claim on either text beyond quotation for the purpose of showing what was argued from it."))
    A()
    lic = re.compile(r"(?i)licen[cs]|public domain|creative commons|\bCC BY\b|copyright")
    hits = sum(len(lic.findall(inp.text(rel))) for rel in ("Dan_oshb.txt", "Dan_web_clean.txt", "pmarks_Dan.json", "dan_device_inventory.json", "rows_v1_final.manifest.json"))
    A(T("A limit on the paragraph above. Those terms are stated here as the project's record for Ezekiel states them for the same two witnesses. Daniel's own files do not state them: a search of the Hebrew-Aramaic text file, the English text file, the section-mark layer, the formula inventory and the list accompanying the final entries for the words licence, public domain, Creative Commons or copyright found %d occurrences. What Daniel's own files do say about their sources is quoted next. The licence terms should be confirmed against the witnesses' own distributions before this record is published.") % hits)
    A()
    for line in inp.text("book_strategy_Dan.md").splitlines():
        if "carry their attribution" in line:
            A("> " + " ".join(line.split()))
            A()
    for k in sorted(inp.pmarks):
        v = inp.pmarks[k]
        if isinstance(v, str) and re.search(r"(?i)oshb|wlc|openscriptures", v) and k != "numbering":
            A("> " + " ".join(v.split()))
            A()

    # ---- 9
    A(T("## 9. Private terms replaced"))
    A()
    A(T("The readers wrote for one another and used the project's private vocabulary. Before quotation, each of the following patterns was replaced as shown, in this order, and nothing else was altered. The patterns are printed as the generator holds them. %d entry numbers in the quoted sentences matched no entry in the final set and were rendered as “an entry outside the final set”.") % sum(cl.unknown_ids.values()))
    A()
    A("| pattern | replaced with |")
    A("|---|---|")
    for _rx, _rep, desc, pat in cl.table:
        A("| `%s` | %s |" % (pat.replace("|", "\\|"), desc.replace("|", "\\|")))
    A()

    # ---- 10
    A(T("## 10. The apparatus's own words"))
    A()
    A(T("Every sentence in this record that is not a quotation was assembled from one of the following strings. A mark such as %d or %s stands where a count or a value from the reports was inserted."))
    A()
    for s in D.templates:
        A("- " + s.replace("\n", " "))
    A()
    return ("\n".join(D.lines).rstrip("\n") + "\n").encode("utf-8"), {"inp": inp, "cl": cl, "C": C, "disputes": disputes, "quiet": quiet}


def pair_line(cl, T, stage, rec, it, va, vb):
    return T("- %s on %s (%s): the scope reading gave %s; the text reading gave %s.") % (
        cl.clean(str(rec)).capitalize(), cl.clean(str(it.get("row", ""))), cl.clean(str(it.get("field", ""))), va, vb)


def main():
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--dan-root", default=str(here.parent))
    ap.add_argument("--out-root", default=None)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    out_root = Path(a.out_root) if a.out_root else Path(a.dan_root)
    doc, _ctx = build(a.dan_root)
    target = out_root / "scholar_record" / DOC_NAME
    if a.check:
        ok = target.read_bytes() == doc
        print("%s sha256 %s bytes %d: %s" % (DOC_NAME, sha(doc), len(doc), "IDENTICAL" if ok else "DIFFERS"))
        return 0 if ok else 1
    target.write_bytes(doc)
    print("%s sha256 %s bytes %d lines %d" % (DOC_NAME, sha(doc), len(doc), doc.count(b"\n")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
