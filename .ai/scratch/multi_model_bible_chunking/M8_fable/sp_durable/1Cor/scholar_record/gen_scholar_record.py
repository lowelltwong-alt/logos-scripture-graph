#!/usr/bin/env python3
"""GENERATOR for a book's scholar record (close-gate item 20, OW-17). Book-agnostic (TE-7).

Every book-specific name, path, digest, count and sentence lives in the parameter file; this script holds none.
A later book supplies a new parameter file and ports nothing. The document is a PURE FUNCTION of its inputs:

  * no clock, no randomness, sorted iteration;
  * every pinned input is opened by a named path under --book-root and its sha256 is checked against the
    parameter file; every landed output is opened by the path the pinned manifest of landed outputs gives, and
    its sha256 is checked against the digest that manifest holds. No directory is scanned and nothing is tested
    for existence: a missing or changed file is a hard stop;
  * every sentence about the text is a landed file's own string, passed through clean() (a mechanical
    substitution table the document prints in full); every other sentence is a template registered by T() and
    printed in the document's last section.

Usage:
  python -B gen_scholar_record.py [--params FILE] [--book-root DIR] [--out-root DIR] [--check]
    --params     parameter file; default: book_params.v1.json beside this script
    --book-root  inputs; default: the parent of this script's directory
    --out-root   outputs; default: the same as --book-root
    --check      write nothing; rebuild and compare with the document on disk (exit 1 on a difference)
"""
import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
KNOWN_KINDS = {"first_reading", "gate_review", "adjudication", "audit", "audit_supplement", "change_log",
               "revised_entries", "drafted_entries", "plan_candidate", "tool", "tool_report", "closing_message"}
QUOTED_KINDS = {"first_reading", "gate_review", "adjudication", "audit", "audit_supplement", "change_log"}
PARSED_JSONL_KINDS = {"drafted_entries"}


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


def load_params(path):
    return json.loads(Path(path).read_bytes().decode("utf-8"))


def jsonl(text):
    return [json.loads(l) for l in text.splitlines() if l.strip()]


class Inputs:
    """Everything read from disk, read once, digest-checked."""

    def __init__(self, P, book_root):
        self.P = P
        self.root = Path(book_root)
        self.raw = {}
        for rel in sorted(P["pinned"]):
            b = (self.root / rel).read_bytes()
            if sha(b) != P["pinned"][rel]:
                raise SystemExit("PINNED INPUT CHANGED: %s has sha256 %s, expected %s" % (rel, sha(b), P["pinned"][rel]))
            self.raw[rel] = b
        pa = P["paths"]
        self.rows = jsonl(self.text(pa["rows"]))
        self.rows_manifest = self.json(pa["rows_manifest"])
        self.manifest = self.json(pa["manifest"])
        self.routed = jsonl(self.text(pa["routed"]))
        self.marks = self.json(pa["marks"])
        self.inventory = self.json(pa["inventory"])
        self.rulings = [(rel, self.json(rel)) for rel in P["ruling_rels"]]
        self.outputs = []
        self.landed = {}
        self.drafts = []
        prefix = P["manifest_prefix"]
        for o in sorted(self.manifest["outputs"], key=lambda x: x["path"]):
            path = o["path"]
            if not path.startswith(prefix):
                raise SystemExit("manifest path outside the book: %s" % path)
            shown = path[len(prefix):]
            e = {"path": path, "shown": shown, "sha256": o["sha256"], "bytes": o.get("bytes"), "rel": None, "kind": None, "status": None}
            for pat, kind in P["not_opened_rules"]:
                if re.fullmatch(pat, shown):
                    e["kind"], e["status"] = kind, P["kind_note"][kind]
                    break
            if e["kind"] is None:
                b = (self.root / shown).read_bytes()
                if sha(b) != o["sha256"]:
                    raise SystemExit("LANDED OUTPUT CHANGED: %s has sha256 %s, manifest says %s" % (shown, sha(b), o["sha256"]))
                e["rel"] = shown
                e["kind"] = classify(P, shown)
                if e["kind"] in QUOTED_KINDS:
                    self.landed[shown] = json.loads(b.decode("utf-8"))
                    e["status"] = "opened, digest verified, quoted"
                else:
                    e["status"] = "opened, digest verified, not quoted (%s)" % P["kind_note"][e["kind"]]
                    if e["kind"] in PARSED_JSONL_KINDS:
                        self.drafts += jsonl(b.decode("utf-8"))
            self.outputs.append(e)

    def text(self, rel):
        return self.raw[rel].decode("utf-8")

    def json(self, rel):
        return json.loads(self.text(rel))

    def of_kind(self, kind):
        return [(e, self.landed[e["rel"]]) for e in self.outputs if e["kind"] == kind]


def classify(P, rel):
    for pat, kind in P["class_rules"]:
        if re.fullmatch(pat, rel):
            if kind not in KNOWN_KINDS:
                raise SystemExit("the parameter file names a kind this script cannot render: %s" % kind)
            return kind
    raise SystemExit("UNCLASSIFIED LANDED OUTPUT: %s (the generator must not omit it silently)" % rel)


# ---------------------------------------------------------------- references

def renumber(P, c, v):
    for z in P["numbering_zones"]:
        if c == z["chapter"] and z["from"] <= v <= z["to"]:
            return c + z["add_chapters"], v + z["add_verses"]
    return c, v


def parse_span(P, span):
    a = re.escape(P["book_abbrev"])
    m = re.fullmatch(r"%s\.(\d+)\.(\d+)-%s\.(\d+)\.(\d+)" % (a, a), span)
    if not m:
        raise SystemExit("unreadable span: %r" % span)
    return tuple(int(x) for x in m.groups())


def fmt_range(c1, v1, c2, v2):
    if (c1, v1) == (c2, v2):
        return "%d:%d" % (c1, v1)
    if c1 == c2:
        return "%d:%d–%d" % (c1, v1, v2)
    return "%d:%d–%d:%d" % (c1, v1, c2, v2)


def short_ref(P, span):
    return P["book_name"] + " " + fmt_range(*parse_span(P, span))


def full_ref(P, span):
    c1, v1, c2, v2 = parse_span(P, span)
    m1, m2 = renumber(P, c1, v1), renumber(P, c2, v2)
    out = P["book_name"] + " " + fmt_range(c1, v1, c2, v2)
    if m1 != (c1, v1) or m2 != (c2, v2):
        out += " (%s %s)" % (P["numbering_label"], fmt_range(m1[0], m1[1], m2[0], m2[1]))
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
FIELD_ABBREVIATIONS = [(r"sra|SRA", "the strongest alternative considered"), (r"ber", "the evidence list"),
                       (r"br|BR", "the stated reason for the boundary"), (r"oss", "the observed signals")]
TIER_WORDS = [("MEASURED", "counted"), ("EXTRACTED", "read from the source"), ("TRANSCRIBED", "copied"),
              ("REPORTED", "reported"), ("INFERRED", "interpretive"), ("ASSUMED", "assumed"),
              ("UNAVAILABLE", "unavailable"), ("NOT_TESTABLE", "not testable"), ("CONFIRM", "confirm"),
              ("RETURN", "return"), ("MET", "met"), ("GREEN", "passing"), ("RED", "failing")]
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
    (r"\bbook strategy\b", "reading plan"),
    (r"\bthe strategy\b", "the reading plan"),
    (r"\bcampaign\b", "project"),
    (r"\bmanifests?\b", "list"),
    (r"\bwaves?\b", "round"),
    (r"\breceipts?\b", "start record"),
    (r"\bworklist\b", "list of work"),
    (r"\bFable\b", "the final reviewer"),
    (r"\bclaude-opus-[\d-]+\b|\bOpus\b|\bClaude\b", "the model"),
    (r"\bgrader[_ ]fallback\b", "a substitute model"),
    (r"\bsha256\b", "digest"),
    (r"\bregex\b", "search pattern"),
    (r"\bngram7\b", "the repeated-phrase check"),
    (r"\bwriter(?:'s)?\b", "drafter"),
    (r"\bexecution e?(\d+)\b", r"pass \1"),
    (r"\bexecution\b", "pass"),
    (r"\battempts?\b", "pass"),
    (r"\bagent_id\b|\bagent ids?\b", "run identity"),
    (r"\bagents?\b", "reader"),
]


def _plural(word_s, word_p):
    def f(m):
        t = m.group(0)
        out = word_p if t.lower().endswith("s") else word_s
        return out.capitalize() if t[0].isupper() else out
    return f


class Cleaner:
    """clean() = scripture references for entry numbers, then the printed table of private terms."""

    def __init__(self, P, inp):
        self.P = P
        self.rid_rx = P["row_id_regex"]
        self.by_id = {}
        for r in inp.rows:
            self.by_id[self.canon(r["decision_id"])] = r
            self.by_id[self.canon(r["writer_decision_id"])] = r
        self.unknown_ids = Counter()
        self.devices = []
        for k in sorted(inp.inventory.get("formulae", {}), key=lambda s: (-len(s), s)):
            g = inp.inventory["formulae"][k]
            gloss = g.get("gloss") if isinstance(g, dict) else None
            if "_" in k:
                self.devices.append((k, "the formula “%s”" % " ".join(str(gloss).split()) if gloss else k.replace("_", " ")))
        self.keep_rx = [re.compile(x) for x in P["code_keep_regexes"]]
        self.table = self._build()

    @staticmethod
    def canon(x):
        head, tail = x.rsplit("-", 1)
        return "%s-%d" % (head, int(tail))

    def row_of(self, rid):
        return self.by_id.get(self.canon(str(rid)))

    def _rid(self, m):
        r = self.row_of(m.group(0))
        if r is None:
            self.unknown_ids[m.group(0)] += 1
            return "an entry outside the final set"
        return short_ref(self.P, r["span"])

    def _code(self, m):
        t = m.group(0)
        if re.fullmatch(self.rid_rx, t) or any(k.fullmatch(t) for k in self.keep_rx):
            return t
        parts = t.split("-")
        if all(p in self.P["code_keep"] or p.isdigit() for p in parts):
            return t
        ids = [x for x in re.findall(self.rid_rx, t) if self.row_of(x) is not None]
        if ids:
            return "the adjudication on " + short_ref(self.P, self.row_of(ids[0])["span"])
        for fam, word in self.P["code_families"]:
            if re.fullmatch(fam, parts[0]):
                return word
        return "a numbered adjudication item"

    def _build(self):
        P = self.P
        a = re.escape(P["book_abbrev"])
        t = []
        t.append((r"[\x00-\x08\x0b-\x1f\x7f]", "", "(a stray control character removed)"))
        t.append((r"`", "", "(removed)"))
        t.append((r"\b[a-z0-9_]+_a\d+(?:#e\d+)?\b", "an earlier pass", "an earlier pass"))
        t.append((r"#e\d+\b", "", "(removed)"))
        t.append((r"\b[0-9a-f]{64}\b|\b[0-9a-f]{6,}\.\.\.[0-9a-f]{4,}\b", "(digest omitted)", "(digest omitted)"))
        t.append((r"(?:[A-Za-z]:)?(?:[\w.-]+[\\/])+(?=[\w.-]+\.(?:jsonl|json|py|md|txt)\b)", "", "(directory prefix removed)"))
        for pat, rep in P["file_names"]:
            t.append((r"\b" + pat, rep, rep))
        t.append((r"\b[\w.-]+\.(?:jsonl|json|py|md|txt)(?:\.pre_[0-9a-f]+)?\b", "a working file", "a working file"))
        t.append((r"(?<![\w.])\.(?:jsonl|json|py|md)\b", "file-suffix", "file-suffix"))
        t.append((r"(?:[A-Za-z]:)?\\?(?:[\w.<>-]+\\)+[\w.<>-]*", "a working path", "a working path"))
        t.append((r"\b(?:SP|OUT)[\\/]", "", "(removed)"))
        t.append((r"(?:\s*(?<![\w-])--[a-z][\w-]*(?:[ =](?:\d+|[A-Z]?\d|<\w+>|[\w.]+\d))?)+", " (with its settings)", "(with its settings)"))
        t.append((r"\b(?=[0-9a-f]*\d)(?=[0-9a-f]*[a-f])[0-9a-f]{7,63}\b", "(digest omitted)", "(digest omitted)"))
        t.append((r"(" + P["row_id_regex"] + r")\.(?=[a-z_]+)", r"\1 ", "(the joining dot removed)"))
        t.append((r"\bM8[_ ]fable\b", "the project", "the project"))
        for k, rep in self.devices:
            t.append((r"\b" + re.escape(k) + r"\b", rep, rep))
        for k, rep in FIELD_NAMES:
            t.append((r"\b" + re.escape(k) + r"\[(\d+)\]", rep + r", item \1 (counted from 0)", rep + ", item N (counted from 0)"))
            t.append((r"\b" + re.escape(k) + r"\b", rep, rep))
        for k, rep in FIELD_ABBREVIATIONS:
            t.append((r"\b(?:" + k + r")\[(\d+)\]", rep + r", item \1 (counted from 0)", rep + ", item N (counted from 0)"))
            t.append((r"\b(?:" + k + r")\b", rep, rep))
        for k, rep in TIER_WORDS:
            t.append((r"\b" + k + r"\b", rep, rep))
        t.append((r"\b[A-Za-z0-9]+(?:_[A-Za-z0-9]+)+\b", lambda m: m.group(0).replace("_", " "),
                  "the same words with spaces for underscores"))
        for tag, label in P["witness_tags"]:
            t.append((r"\b" + tag + ":" + a + r"\.(\d+)\.(\d+)", r"\1:\2 (" + label + ")", "chapter:verse (%s)" % label))
        t.append((r"\b" + a + r"\.(\d+)\.(\d+)", r"\1:\2", "chapter:verse"))
        for pat, rep in P["word_subs_before_codes"]:
            t.append((pat, rep, rep.replace("\\1", "N").replace("\\2", "M")))
        t.append((r"\b" + P["part_regex"] + r"#(\d+)\b", r"revision note \1.\2", "revision note N.M"))
        t.append((r"\bS\d{1,2}-\d+[a-z]\b", "a numbered review finding", "a numbered review finding"))
        t.append((r"(?<![\w-])[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+(?![\w])", self._code,
                  "the adjudication on <passage>, or a standing order, an early screening question, a numbered review "
                  "finding, an owner directive, a logged error, or a numbered adjudication item"))
        t.append((r"\b" + P["row_id_regex"] + r"\b", self._rid, "the passage's scripture reference"))
        t.append((r"\b" + P["part_regex"] + r"\b", r"drafting part \1", "drafting part N"))
        for pat, rep in P["book_word_subs"]:
            t.append((pat, rep, rep))
        t.append((r"\bCWO-?\d*\b", "a standing order", "a standing order"))
        t.append((r"§+\s*\d+[\w.]*", "a section of the reading plan", "a section of the reading plan"))
        t.append((r"(?i)\bfix-?up[ -]?(\d+)\b", r"revision round \1", "revision round N"))
        t.append((r"(?i)\btier(?:ed|ing)\b", "graded for evidence", "graded for evidence"))
        t.append((r"(?i)\btiers\b", "evidence grades", "evidence grades"))
        t.append((r"(?i)\btier\b", "evidence grade", "evidence grade"))
        t.append((r"(?i)\blaunch(?:es|ed)?\b", "start", "start"))
        t.append((r"(?i)\bsuite\b", "set of automated checks", "set of automated checks"))
        t.append((r"(?i)\bpeers\b", "reconciling readings", "reconciling readings"))
        t.append((r"(?i)\bpeer\b", "reconciling reading", "reconciling reading"))
        t.append((r"(?i)\bprimaries\b", "first readings", "first readings"))
        t.append((r"(?i)\bexecutions\b", "passes", "passes"))
        gate = "".join("(?<!%s )" % re.escape(x) for x in P["gate_word_exempt_prefixes"])
        t.append((r"(?i)" + gate + r"\bgates?\b", "checkpoint", "checkpoint"))
        for pat, rep in PROCESS_NOUNS:
            t.append((r"(?i)" + pat, rep, rep.replace("\\1", "N")))
        t.append((r"(?i)\blanes\b", _plural("reading", "readings"), "readings"))
        t.append((r"(?i)\blane\b", _plural("reading", "readings"), "reading"))
        t.append((r"(?i)\brows\b", _plural("entry", "entries"), "entries"))
        t.append((r"(?i)\brow\b", _plural("entry", "entries"), "entry"))
        for k, rep in P["lane_names"]:
            t.append((r"\b" + k + r"\b", rep, rep))
        for letter, rep in P["letter_codes"]:
            t.append((r"\b" + letter + r"(\d{1,2})\b", rep + r" \1", rep + " N"))
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

    def plain(self, v):
        """a landed value of any shape as one cleaned phrase"""
        if v is None or isinstance(v, (bool, int, float)):
            return str(v)
        return self.clean(" ".join(leaves(v)))


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
    for x in re.findall(cl.rid_rx, json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v):
        r = cl.row_of(x)
        if r is not None and r["decision_id"] not in out:
            out.append(r["decision_id"])
    return out


def ruling_ids(ru, cl):
    return row_ids_in([ru.get("id", ""), ru.get("orders", [])], cl)


def lane_of(P, rel):
    return re.search(P["first_reading_lane_regex"], rel).group(1)


def verdict_of(it):
    return str((it or {}).get("verdict") or "").lower() or None


def order_value(it):
    """a routed item's order, decoded when the file holds it as a JSON string"""
    v = it.get("order")
    if isinstance(v, str) and v.lstrip().startswith("{"):
        return json.loads(v)
    return v


def collect(P, inp, cl):
    """All per-passage material, keyed by the entry's own number. Shared with the checker."""
    C = {"first": defaultdict(dict), "audit": defaultdict(list), "gate": defaultdict(list), "seam": defaultdict(list),
         "gate_wide": [], "seam_wide": [], "rulings": defaultdict(list), "class_rulings": [], "changes": Counter()}
    for e, d in inp.of_kind("first_reading"):
        lane = lane_of(P, e["rel"])
        for it in d.get("items", []):
            r = cl.row_of(it.get("row_id"))
            if r is None:
                raise SystemExit("first reading names an entry outside the final set: %r" % it.get("row_id"))
            C["first"][r["decision_id"]][lane] = it
    for g in P["gate_reviews"]:
        rel, d = g["rel"], inp.landed[g["rel"]]
        for f in d.get("new_findings", []):
            ids = row_ids_in(f.get("row_or_artifact", ""), cl)
            if 1 <= len(ids) <= P["max_rows_under_a_passage"]:
                for rid in ids:
                    C["gate"][rid].append((g["label"], f))
            else:
                C["gate_wide"].append((g["label"], f))
        for s in d.get("seams", []):
            if s.get("verdict") == "accept" and not s.get("findings"):
                continue
            ids = row_ids_in(s.get("rows", []), cl)
            if 1 <= len(ids) <= P["max_rows_under_a_passage"]:
                for rid in ids:
                    C["seam"][rid].append((g["label"], s))
            else:
                C["seam_wide"].append((g["label"], s))
    for n, kind in enumerate(("audit", "audit_supplement"), 1):
        for e, d in inp.of_kind(kind):
            for it in d.get("rows", []):
                r = cl.row_of(it.get("row"))
                if r is None:
                    raise SystemExit("audit names an entry outside the final set: %r" % it.get("row"))
                C["audit"][r["decision_id"]].append((n, it))
    for rel, d in inp.rulings:
        n = int(re.search(r"_E(\d+)\.", rel).group(1))
        for ru in d.get("rulings", []):
            ids = ruling_ids(ru, cl)
            if 1 <= len(ids) <= P["max_rows_under_a_passage"]:
                for rid in ids:
                    C["rulings"][rid].append((n, ru))
            else:
                C["class_rulings"].append((n, ru, len(ids)))
    for e, d in inp.of_kind("change_log"):
        for ch in d.get("changes", []):
            for rid in row_ids_in(ch.get("row", ""), cl):
                C["changes"][rid] += 1
    return C


def sev_rank(P, s):
    return P["severity_rank"].get(str(s).lower(), 0) if s else 0


def severities_for(P, rid, C):
    out = [C["first"][rid][l].get("severity") for l in sorted(C["first"].get(rid, {}))]
    out += [f.get("severity") for _l, f in C["gate"].get(rid, [])]
    for _n, a in C["audit"].get(rid, []):
        out += [f.get("severity") for f in a.get("findings", []) or []]
    return max([sev_rank(P, s) for s in out] or [0])


def first_disagree(rid, C):
    f = C["first"].get(rid, {})
    kinds = []
    vs = {verdict_of(f[l]) for l in f}
    if len(vs) > 1:
        kinds.append("verdict")
    else:
        ch = [json.dumps(f[l].get("decision"), ensure_ascii=False, sort_keys=True) for l in sorted(f) if verdict_of(f[l]) == "challenge"]
        if len(ch) >= 2 and len(set(ch)) > 1:
            kinds.append("remedy")
    return kinds


def is_dispute(rid, C):
    f = C["first"].get(rid, {})
    if any(verdict_of(f[l]) != "support" for l in f) or first_disagree(rid, C):
        return True
    if C["gate"].get(rid) or C["seam"].get(rid) or C["rulings"].get(rid):
        return True
    return any(a.get("findings") or a.get("verdict") != "CONFIRM" for _n, a in C["audit"].get(rid, []))


def book_slots(P, inp, cl, C, rows, disputes):
    kinds = Counter(e["kind"] for e in inp.outputs)
    by_id = {r["decision_id"]: r for r in rows}
    final = {}
    for r in rows:
        final[cl.canon(r["decision_id"])] = r
    span_diff = conf_diff = 0
    for x in inp.drafts:
        r = final[cl.canon(x["decision_id"])]
        span_diff += int(x["span"] != r["span"])
        conf_diff += int(x["confidence"] != r["confidence"])
    S = {"units": len(rows), "drafted": len(inp.drafts), "span_changes_from_draft": span_diff, "confidence_changes_from_draft": conf_diff,
         "first_reports": kinds["first_reading"], "first_findings": sum(len(d.get("items", [])) for _e, d in inp.of_kind("first_reading")),
         "gate_reports": kinds["gate_review"], "gate_findings": sum(len(d.get("new_findings", [])) for _e, d in inp.of_kind("gate_review")),
         "change_logs": kinds["change_log"], "changes": sum(len(d.get("changes", [])) for _e, d in inp.of_kind("change_log")),
         "audits": kinds["audit"] + kinds["audit_supplement"], "rulings_rounds": len(inp.rulings),
         "rulings": sum(len(d.get("rulings", [])) for _r, d in inp.rulings),
         "listed": len(inp.outputs), "quoted_files": sum(1 for e in inp.outputs if e["kind"] in QUOTED_KINDS),
         "not_opened": sum(1 for e in inp.outputs if e["rel"] is None),
         "not_matching": len(inp.manifest.get("not_matching", [])),
         "no_digest": inp.manifest.get("completion_rows_listing_no_digest"),
         "open_questions": len(inp.routed)}
    S["checked_not_quoted"] = S["listed"] - S["quoted_files"] - S["not_opened"]
    groups = {}
    for e, _d in inp.of_kind("first_reading"):
        groups.setdefault(lane_of(P, e["rel"]), set()).add(re.search(P["first_reading_group_regex"], e["rel"]).group(1))
    S["groups_all"] = len(set().union(*groups.values()))
    for lane, g in groups.items():
        S["groups_" + lane] = len(g)
    S["ruling_kinds"] = "; ".join("%s, %d" % (cl.clean(k), n) for k, n in sorted(Counter(ru.get("ruling") for _r, d in inp.rulings for ru in d.get("rulings", [])).items()))
    lic = re.compile(P["licence_search_regex"])
    S["licence_hits_witness_files"] = sum(len(lic.findall(inp.text(rel))) for rel in P["witness_files"])
    return S


def lookup(inp, slots, spec):
    if isinstance(spec, str):
        return slots[spec]
    src, path = spec[0], list(spec[1:])
    if src == "landed":
        v = inp.landed[path.pop(0)]
    else:
        v = {"marks": inp.marks, "inventory": inp.inventory, "rows_manifest": inp.rows_manifest, "manifest": inp.manifest}[src]
    for k in path:
        v = v[k]
    return v


def build(params_path, book_root):
    P = load_params(params_path)
    inp = Inputs(P, book_root)
    cl = Cleaner(P, inp)
    C = collect(P, inp, cl)
    D = Doc()
    T, A = D.T, D.add

    def q(s):
        c = cl.clean(s)
        if c:
            A("> " + c)

    def quote_all(label, v):
        ls = [x for x in leaves(v)]
        if ls:
            A(label)
            A()
            for x in ls:
                q(x)
                A()

    def quote_bare(v):
        for x in leaves(v):
            q(x)
            A()

    rows = inp.rows
    order = {r["decision_id"]: i for i, r in enumerate(rows)}
    sev = lambda r: severities_for(P, r["decision_id"], C)
    disputes = sorted([r for r in rows if is_dispute(r["decision_id"], C)], key=lambda r: (-sev(r), order[r["decision_id"]]))
    quiet = [r for r in rows if not is_dispute(r["decision_id"], C)]
    slots = book_slots(P, inp, cl, C, rows, disputes)
    strategy = inp.text(P["paths"]["strategy"]).splitlines()
    lane_names = {k: v for k, v in P["first_reading_lanes"]}
    sev_name = {int(k): v for k, v in P["severity_names"].items()}

    def blocks(bs):
        for b in bs:
            if "text" in b:
                vals = tuple(lookup(inp, slots, s) for s in b.get("values", []))
                A(T(b["text"]) % vals if vals else T(b["text"]))
                A()
            elif "quote" in b:
                quote_bare(lookup(inp, slots, b["quote"]))
            elif "strategy_between" in b:
                x, y = b["strategy_between"]
                for l in strategy[strategy.index(x) + 1:strategy.index(y)]:
                    if l.strip():
                        q(l)
                        A()
            elif "strategy_matching" in b:
                for l in strategy:
                    if re.search(b["strategy_matching"], l):
                        q(l)
                        A()
            elif "formulae" in b:
                for k in sorted(inp.inventory.get("formulae", {})):
                    g = inp.inventory["formulae"][k]
                    A(T(b["formulae"]) % (cl.clean(g.get("gloss")), cl.clean(g.get("family")), g.get("count_rp"), g.get("count_sbl")))
                A()
            else:
                raise SystemExit("unknown block in the parameter file: %r" % sorted(b))

    A(T("# The division of %s into reading units: a record of what was disputed") % P["book_name"])
    A()
    A(T("This record is generated mechanically from the reports of the readers who examined a proposed division of %s into %d reading units. It is written for a reader of the book, not for a reader of the project that produced it: passages are named by chapter and verse.") % (P["book_name"], len(rows)))
    A()
    A(T("Every quotation set off with a rule at the left is a reader's own sentence, altered only by the mechanical substitutions listed in full near the end. Every other sentence is the generator's own frame, and every such sentence is printed in the last section so that the frame can be inspected apart from the evidence."))
    A()
    A(T("This record makes no judgement of its own. It changes no unit, weighs no boundary and settles no dispute; it reports what the readers wrote. Its limits are stated in section 2 and are not small."))
    A()

    # ---- 1
    A(T("## 1. What made this book difficult"))
    A()
    blocks(P["section1"])
    conf = Counter(r.get("confidence") for r in rows)
    A(T("The division as it stands records its own grades of confidence: %s. Its unit types are: %s.") % (
        "; ".join("%s, %d" % (cl.clean(k), conf[k]) for k in sorted(conf)),
        "; ".join("%s, %d" % (cl.clean(k), n) for k, n in sorted(Counter(r.get("unit_type") for r in rows).items()))))
    A()

    # ---- 2
    A(T("## 2. How the division was examined, and what that does and does not establish"))
    A()
    A(T("The examination left these reports: %d first-reading reports with %d findings; %d reviews between revision rounds with %d new findings; %d revision logs with %d recorded changes; %d audits; and %d adjudication rounds with %d rulings (%s).") % (
        slots["first_reports"], slots["first_findings"], slots["gate_reports"], slots["gate_findings"], slots["change_logs"], slots["changes"],
        slots["audits"], slots["rulings_rounds"], slots["rulings"], slots["ruling_kinds"]))
    A()
    A(T("Each first reading stated its own role. The distinct statements are:"))
    A()
    roles = []
    for _e, d in inp.of_kind("first_reading"):
        if d.get("role") not in roles:
            roles.append(d.get("role"))
    quote_bare(roles)
    blocks(P["section2_limits"])
    A(T("Of the %d files the project lists as landed, %d were opened and quoted, %d were opened and checked but not quoted, and %d were not opened (closing messages, named by the listed digest only). Section 7 lists every one. The project's records also name %d further outputs that have no durable file at any named place, and %d completion records that list no digest; those outputs could not be read by anyone and are not represented here beyond the list in section 7.") % (
        slots["listed"], slots["quoted_files"], slots["checked_not_quoted"], slots["not_opened"], slots["not_matching"], slots["no_digest"]))
    A()

    # ---- 3
    A(T("## 3. The disputes"))
    A()
    A(T("A passage appears here if any first reading challenged its entry, if the first readings differed, if a review recorded a finding or left a seam unaccepted on it, if an adjudication named it, or if an audit recorded a finding on it or did not confirm it. %d of the %d units appear. They are ordered by the highest severity any reader assigned, then by their place in the book. Severity is the readers' own grade.") % (len(disputes), len(rows)))
    A()
    A(T("The readers used different words for severity. For ordering only, this record ranks them as follows: %s. The reader's own word is printed with each finding.") % P["severity_mapping_text"])
    A()
    sevc = Counter(sev_name[sev(r)] for r in disputes)
    A(T("By highest severity: %s.") % "; ".join("%s, %d" % (sev_name[k], sevc[sev_name[k]]) for k in sorted(sev_name, reverse=True) if sevc[sev_name[k]]))
    A()
    for r in disputes:
        rid = r["decision_id"]
        A(T("### %s — highest severity: %s") % (full_ref(P, r["span"]), sev_name[sev(r)]))
        A()
        A(T("The unit as it stands: language %s; type %s; confidence %s.") % (
            P["language_names"].get(r.get("language"), r.get("language")), cl.clean(r.get("unit_type")), cl.clean(r.get("confidence"))))
        A()
        A(T("The stated reason for the boundary, as the entry now reads:"))
        A()
        quote_bare(r.get("boundary_rationale"))
        quote_all(T("The strongest alternative the entry considered and declined:"), r.get("strongest_rejected_alternative"))
        A(T("**Evidence on each side.**"))
        A()
        f = C["first"].get(rid, {})
        for lane, name in P["first_reading_lanes"]:
            it = f.get(lane)
            if it is None:
                A(T("%s did not read this passage.") % name)
                A()
                continue
            A(T("%s: verdict %s; severity %s; graded by the reader as %s; its proposed course:") % (
                name, verdict_of(it), it.get("severity") or "none given", cl.plain(it.get("tier")) if it.get("tier") else "none given"))
            A()
            quote_bare(it.get("decision", ""))
            quote_all(T("Its claim:"), it.get("claim"))
            quote_all(T("The two sides as it set them out:"), it.get("both_sides"))
            quote_all(T("The evidence it cited:"), it.get("evidence"))
            quote_all(T("The correction it suggested:"), it.get("suggested_fix"))
        dk = first_disagree(rid, C)
        if dk:
            A(T("**The first readings disagreed here** (%s).") % ", ".join(
                {"verdict": "their verdicts differ", "remedy": "both or all challenged but proposed different courses"}[k] for k in dk))
        else:
            A(T("The first readings did not disagree here."))
        A()
        A(T("**Resolution.**"))
        A()
        for label, g in C["gate"].get(rid, []):
            A(T("%s recorded a finding (severity %s) on %s:") % (label, g.get("severity") or "none given", cl.plain(g.get("row_or_artifact"))))
            A()
            quote_bare([g.get("claim"), g.get("evidence"), g.get("suggested_fix")])
        for label, s in C["seam"].get(rid, []):
            A(T("%s examined the seam at %s (%s) and left it as: %s.") % (label, cl.plain(s.get("seam")), cl.plain(s.get("kind")), cl.plain(s.get("verdict"))))
            A()
            quote_bare(s.get("findings"))
        for n, ru in C["rulings"].get(rid, []):
            A(T("The adjudicator, in round %d, ruled (%s):") % (n, cl.clean(ru.get("ruling", ""))))
            A()
            quote_bare([ru.get("decision"), ru.get("reason")])
        for n, a in C["audit"].get(rid, []):
            A(T("The verdict of audit %d on the entry: %s.") % (n, cl.clean(a.get("verdict", ""))))
            A()
            quote_all(T("Its reason:"), a.get("why"))
            for fd in a.get("findings", []) or []:
                A(T("Audit %d recorded a finding (severity %s; graded by the auditor as %s) on %s:") % (n, fd.get("severity"), cl.plain(fd.get("tier")), cl.plain(fd.get("field", ""))))
                A()
                quote_bare([fd.get("claim"), fd.get("evidence")])
            quote_all(T("The work it ordered:"), a.get("work_order"))
        A(T("Recorded changes to this entry in the revision logs: %d.") % C["changes"].get(rid, 0))
        A()
    A(T("### Passages on which no reader raised anything"))
    A()
    A(T("%d units drew no challenge from any first reading and no later finding: %s.") % (len(quiet), "; ".join(full_ref(P, r["span"]) for r in quiet) or "none"))
    A()

    # ---- 4
    A(T("## 4. What changed"))
    A()
    A(T("Compared with the first draft, as a count over the two sets of entries: of %d drafted units, %d changed in extent and %d changed in grade of confidence. No boundary count here says the boundary is right; it says only whether it moved.") % (
        slots["drafted"], slots["span_changes_from_draft"], slots["confidence_changes_from_draft"]))
    A()
    A(T("The revision logs record the following. Each log gives its counts, then the words of each change as the log holds them."))
    A()
    for e, d in inp.of_kind("change_log"):
        ch = d.get("changes", [])
        byf = Counter(cl.clean(re.sub(r"\[\d+\]", "", str(c.get("field")))) for c in ch)
        m = re.search(P["change_log_regex"], e["rel"])
        A(T("- Revision round %s, drafting part %s: %d changes on %d passages (%s); %d ordered changes not made.") % (
            m.group(1), m.group(2), len(ch), len({x for c in ch for x in row_ids_in(c.get("row", ""), cl)}),
            "; ".join("%s, %d" % (k, byf[k]) for k in sorted(byf)) or "none", len(d.get("blocked", []) or [])))
        A()
        for c in ch:
            A(T("  On %s (%s), graded by the reviser as %s, the words before:") % (cl.plain(c.get("row", "")), cl.plain(c.get("field", "")), cl.plain(c.get("tier"))))
            A()
            quote_bare(c.get("before"))
            A(T("  and after:"))
            A()
            quote_bare(c.get("after"))
        for b in d.get("blocked", []) or []:
            A(T("  Not made, on %s (%s), for this reason:") % (cl.plain(b.get("row", "no named passage")), cl.plain(b.get("field", "no named field"))))
            A()
            quote_bare([b.get("why"), b.get("evidence")])
        for k in P["change_log_note_keys"]:
            quote_all(T("  The log's own note on what it left alone:"), d.get(k))
    blocks(P["section4_limits"])

    # ---- 5
    A(T("## 5. The reviews, the adjudication and the audit"))
    A()
    A(T("Each review between revision rounds was one reader's report. Each is summarised below, with its findings that bear on many passages or on the apparatus rather than on one passage. Its findings on one to %d passages stand under those passages in section 3.") % P["max_rows_under_a_passage"])
    A()
    for g in P["gate_reviews"]:
        d = inp.landed[g["rel"]]
        nf = d.get("new_findings", [])
        A(T("### %s") % g["label"])
        A()
        A(T("Its verdict on readiness: %s. New findings: %d (%s). Earlier findings it re-examined: %d (%s). Conditions: %d (%s).") % (
            cl.plain(d.get("readiness") or d.get("verdict")), len(nf),
            "; ".join("%s, %d" % (k, n) for k, n in sorted(Counter(str(f.get("severity")) for f in nf).items())) or "none",
            len(d.get("ruled_findings", [])), "; ".join("%s, %d" % (cl.clean(k), n) for k, n in sorted(Counter(x.get("status") for x in d.get("ruled_findings", [])).items())) or "none",
            len(d.get("conditions", [])), "; ".join("%s, %d" % (cl.clean(k), n) for k, n in sorted(Counter(x.get("status") for x in d.get("conditions", [])).items())) or "none"))
        A()
        for label, f in C["gate_wide"]:
            if label == g["label"]:
                A(T("A finding (severity %s) on %s:") % (f.get("severity") or "none given", cl.plain(f.get("row_or_artifact"))))
                A()
                quote_bare([f.get("claim"), f.get("evidence"), f.get("suggested_fix")])
        for label, s in C["seam_wide"]:
            if label == g["label"]:
                A(T("A seam or target examined (%s), left as %s: %s.") % (cl.plain(s.get("kind")), cl.plain(s.get("verdict")), cl.plain(s.get("seam"))))
                A()
                quote_bare(s.get("findings"))
        for x in d.get("ruled_findings", []):
            if x.get("status") == "not_cured":
                A(T("An earlier finding it held not cured:"))
                A()
                quote_bare(x.get("evidence"))
        for x in d.get("conditions", []):
            if x.get("status") != "met":
                A(T("A condition it held not met:"))
                A()
                quote_bare([x.get("text"), x.get("evidence")])
        quote_all(T("What it said must change:"), [x.get("what") for x in d.get("changes_required", [])])
        quote_all(T("What the text showed on items carried forward:"), [x.get("bytes_show") for x in d.get("carried_items", [])])
        quote_all(T("Its test of a stated reason for not using a drafter:"), d.get("deviation_test"))
    A(T("### Screening questions"))
    A()
    A(T("The first readings were also each asked a small set of screening questions. Where a reading answered one for its part of the book, its answer was:"))
    A()
    for e, d in inp.of_kind("first_reading"):
        for ta in d.get("triage_answers", []) or []:
            if isinstance(ta, dict) and ta.get("in_my_cluster"):
                A(T("- %s, on %s:") % (lane_names[lane_of(P, e["rel"])], "; ".join(short_ref(P, cl.row_of(x)["span"]) for x in row_ids_in(ta.get("rows", ""), cl)) or "no named passage"))
                A()
                quote_bare(ta.get("decision") or ta.get("answer"))
    A(T("### Adjudications"))
    A()
    A(T("Adjudications that concern a class of entries or more than %d passages, and so are not placed under a single passage in section 3 (%d):") % (P["max_rows_under_a_passage"], len(C["class_rulings"])))
    A()
    for n, ru, k in C["class_rulings"]:
        A(T("- Round %d, bearing on %d named passages (%s):") % (n, k, cl.clean(ru.get("ruling", ""))))
        A()
        quote_bare([ru.get("decision"), ru.get("reason")])
    for rel, d in inp.rulings:
        n = int(re.search(r"_E(\d+)\.", rel).group(1))
        for o in d.get("corpus_wide_orders", []) or []:
            A(T("A standing order issued in round %d for the whole book:") % n)
            A()
            quote_bare(o)
    A(T("### The audits"))
    A()
    for e, d in inp.of_kind("audit"):
        cv = Counter(c.get("verdict") for c in d.get("conditions", []))
        A(T("The first audit tested %d conditions (%s) and gave a verdict on each of %d entries (%s). **Its overall verdict was: %s.** That verdict is reported here as it was given.") % (
            len(d.get("conditions", [])), "; ".join("%s, %d" % (cl.clean(k), cv[k]) for k in sorted(cv)),
            len(d.get("rows", [])), "; ".join("%s, %d" % (cl.clean(k), n) for k, n in sorted(Counter(x.get("verdict") for x in d.get("rows", [])).items())),
            cl.clean(d.get("overall", {}).get("verdict", ""))))
        A()
        if d.get("overall", {}).get("verdict") != "CONFIRM":
            A(T("The first audit did not pass the division as it then stood: it returned %d entries for further work.") % sum(1 for x in d.get("rows", []) if x.get("verdict") != "CONFIRM"))
            A()
        for c in d.get("conditions", []):
            if c.get("verdict") != "MET":
                A(T("A condition the first audit could not settle (%s):") % cl.clean(c.get("verdict", "")))
                A()
                quote_bare([c.get("how"), c.get("evidence")])
        quote_all(T("Matters the first audit raised for decision:"), d.get("escalations"))
        quote_all(T("Places where the first audit found something reported that should have been counted:"), d.get("reported_where_measured"))
    for e, d in inp.of_kind("audit_supplement"):
        ov = d.get("overall", {})
        A(T("A second audit read the revision that followed. **Its overall verdict was: %s.** It tested %d conditions (%s), re-examined %d carried conditions, and gave a verdict on %d entries; %d entries were carried by byte equality and were not re-read by it.") % (
            cl.clean(ov.get("verdict", d.get("verdict", ""))), len(d.get("conditions", [])),
            "; ".join("%s, %s" % (cl.clean(c.get("verdict", "")), cl.clean(c.get("tier", ""))) for c in d.get("conditions", [])),
            len(d.get("carried_conditions", [])), len(d.get("rows", [])), ov.get("rows_carried_by_byte_equality", 0)))
        A()
        for c in d.get("conditions", []):
            quote_bare([c.get("how"), c.get("evidence")])
        quote_all(T("Conditions it carried, and on what ground:"), [[c.get("why"), c.get("result")] for c in d.get("carried_conditions", [])])
        quote_all(T("What it found of the entries the first audit returned:"), [[c.get("e1_findings"), c.get("state")] for c in d.get("return_cleared", [])])
        quote_all(T("Places where the second audit tested what had been reported:"), d.get("reported_where_measured"))
    A(T("How the audits were joined into the standing of the final entries is stated by the list that accompanies those entries, in these words:"))
    A()
    quote_bare([inp.rows_manifest.get(k) for k in P["rows_manifest_standing_keys"]])

    # ---- 6
    A(T("## 6. What remains open"))
    A()
    A(T("%d questions are carried open. None is settled by anything in this record. Each awaits a final review that has not yet taken place; until it does, each stands exactly as written here.") % len(inp.routed))
    A()
    A(T("The file that carries them gives their status in these words:"))
    A()
    quote_bare(sorted({it.get("status") for it in inp.routed}))
    for i, it in enumerate(inp.routed, 1):
        A(T("### Open question %d") % i)
        A()
        A(T("How it was left (%s):") % cl.clean(it.get("ruling", "")))
        A()
        quote_bare(it.get("decision"))
        quote_all(T("What was asked of the final review:"), order_value(it))
        A(T("Status: open."))
        A()
    blocks(P["section6_extra"])
    A(T("### Limits the readers stated themselves"))
    A()
    A(T("Each reader was required to say what it could not establish. Those statements follow, grouped by stage, each with the reader's own account of why it matters. Repeated statements are printed once."))
    A()
    seen = set()
    groups = [(T("**First readings.**"), [d.get("unresolved_uncertainty") for _e, d in inp.of_kind("first_reading")]),
              (T("**Reviews.**"), [[d.get("unresolved_uncertainty"), [x.get("note") for x in d.get("unresolved_uncertainty_bearing", [])]] for _e, d in inp.of_kind("gate_review")]),
              (T("**The audits.**"), [d.get("unresolved_uncertainty") for _e, d in inp.of_kind("audit") + inp.of_kind("audit_supplement")]),
              (T("**The adjudicator.**"), [d.get("unresolved_uncertainty") for _r, d in inp.rulings])]
    for name, ds in groups:
        A(name)
        A()
        for u in ds:
            for x in leaves(u):
                key = cl.clean(x)
                if key and key not in seen:
                    seen.add(key)
                    q(x)
                    A()

    # ---- 7
    A(T("## 7. Provenance"))
    A()
    A(T("Every file the project lists as landed, with the digest that list gives for it. A file marked as opened had its digest recomputed and matched before any word of it was used."))
    A()
    A("| record | kind | sha256 | use |")
    A("|---|---|---|---|")
    for e in inp.outputs:
        A("| %s | %s | %s | %s |" % (e["shown"], P["kind_label"][e["kind"]], e["sha256"], e["status"]))
    A()
    A(T("Outputs the project's records name that have no durable file at any named place, with the digest those records give. These were not read:"))
    A()
    A("| execution | listed path | sha256 | reason |")
    A("|---|---|---|---|")
    for x in sorted(inp.manifest.get("not_matching", []), key=lambda n: (str(n.get("execution_id")), str(n.get("listed_path")))):
        A("| %s | %s | %s | %s |" % (x.get("execution_id"), x.get("listed_path"), x.get("sha256"), x.get("reason")))
    A()
    A(T("Pinned inputs, with the digest the parameter file holds and this generator verifies for each:"))
    A()
    A("| record | sha256 |")
    A("|---|---|")
    for rel in sorted(P["pinned"]):
        A("| %s | %s |" % (rel, P["pinned"][rel]))
    A()
    A(T("Key from the passages of section 3 to the entry numbers the reports use:"))
    A()
    A("| passage | entry numbers |")
    A("|---|---|")
    for r in rows:
        A("| %s | %s, %s |" % (full_ref(P, r["span"]), r["decision_id"], r["writer_decision_id"]))
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
    blocks(P["section8"])

    # ---- 9
    A(T("## 9. Private terms replaced"))
    A()
    A(T("The readers wrote for one another and used the project's private vocabulary. Before quotation, each of the following patterns was replaced as shown, in this order, and nothing else was altered. Each reader's verdict word is also printed in lower case. The patterns are printed as the generator holds them. %d entry numbers in the quoted sentences matched no entry in the final set and were rendered as “an entry outside the final set”.") % sum(cl.unknown_ids.values()))
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
    return ("\n".join(D.lines).rstrip("\n") + "\n").encode("utf-8"), {"P": P, "inp": inp, "cl": cl, "C": C, "disputes": disputes, "quiet": quiet}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", default=str(HERE / "book_params.v1.json"))
    ap.add_argument("--book-root", default=str(HERE.parent))
    ap.add_argument("--out-root", default=None)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    out_root = Path(a.out_root) if a.out_root else Path(a.book_root)
    doc, ctx = build(a.params, a.book_root)
    name = ctx["P"]["doc_name"]
    target = out_root / "scholar_record" / name
    if a.check:
        ok = target.read_bytes() == doc
        print("%s sha256 %s bytes %d: %s" % (name, sha(doc), len(doc), "IDENTICAL" if ok else "DIFFERS"))
        return 0 if ok else 1
    target.write_bytes(doc)
    print("%s sha256 %s bytes %d lines %d" % (name, sha(doc), len(doc), doc.count(b"\n")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
