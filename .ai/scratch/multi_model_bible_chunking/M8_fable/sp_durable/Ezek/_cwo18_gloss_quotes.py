#!/usr/bin/env python3
"""CWO-EZ-18 (ezek_controlling_rulings_a1#e4), AMENDED by ezek_controlling_rulings_a1#e6 rulings CWO18-SCOPE-1, CWO18-NEARWEB-1 and
CWO18-SHORT-1, with its R1 clause read as ezek_controlling_rulings_a1#e7 ruling CWO18-R1-1 rules. It runs as its own
deterministic sweep after CWO-EZ-13: curly-double-quoted spans that are not WEB text. Both CWO-EZ-18 texts, and CWO18-R1-1's
decision and orders, are read from their rulings files and carried verbatim in the manifest.

PREDICATE (as WIDENED by #e6): every curly-double-quoted span in ANY string field of a row that check_web_quotes classes 'curly
quote with NO web: ref in its field'. That covers the prose fields, each boundary_evidence_refs entry as its own field, and
literature_type_guess. The class is located by replaying the tool's own filter path by path: no web: ref in the field, and the
span, stripped, has at least two words and no Hebrew majority. The replay must reproduce the installed tool's flags span by
span, or the run aborts. A class span in any other field kind is a problem, because no ruling covers it.

CLASSES, decided per span in this order. The WEB text is ezek_lib's verse map built from Ezek_web_clean.txt: 1,273 verses in
canonical order.
  - short_common_label (CWO18-SHORT-1): ezek_lib.web_quote_found finds the span in the WEB, it has three words or fewer
    (whitespace split after strip), and web_quote_found over each verse's own text holds in two or more verses. CONVERTED;
    listed to its part's FIXUP-1 author as an informational item.
  - verbatim_author (CWO-EZ-18 (ii)): found in the WEB and not a label. A FIXUP-1 author item; never edited.
  - near_web_author (CWO18-NEARWEB-1): not found by web_quote_found, but ' ' + fold(span) + ' ' is a substring of the folded
    text of all verses joined. fold = norm_english, lowercase, every non-alphanumeric to a space, whitespace collapsed. A
    FIXUP-1 author item with its folded verse keys; never edited.
  - gloss (CWO-EZ-18 (i)): found under neither matcher. CONVERTED.
A conversion replaces the U+201C/U+201D pair with ASCII single quotes, or U+2018/U+2019 when the span contains an ASCII
apostrophe.

PER-SPAN EQUALITY (CWO18-SCOPE-1 (2)). Before anything is written, every span's class must equal the class the three rulings
give it. The expected classes come from the analysis file and the first dry run, both at the digests #e6 ruled on:
  - prose spans: the first dry run's conversions are glosses unless the analysis lists them near-WEB. The analysis's routed
    (ii) items are labels when their own record has <= 3 words and >= 2 verses holding them verbatim (cross-checked against
    short_common_items), and verbatim authors otherwise;
  - outside-prose spans: the 30 spans #e6 enumerates by row, path and class. Each entry is checked present in the ruling's text
    and consistent with the analysis's matcher facts.
A span classed otherwise is listed and the run stops; it returns to the controlling lane.

Before any write, the exact output bytes are probed with the validator suite in a scratch directory. The run aborts unless:
  - each changed string differs from its input only at the replaced quote characters, and nothing but the strings holding a
    conversion changed;
  - every touched boundary_evidence_refs entry keeps its strict-R1-shape status (_cwo_coverage_ezek.CANON_REF): r1_after ==
    r1_before (#e7 CWO18-R1-1). The touched entries outside the shape are pinned to the one pre-existing entry, P08-013
    [105].boundary_evidence_refs[1], at its bytes (outside_r1_before == outside_r1_after == 1). That entry is reported by row,
    path, old and new bytes, and why. Any status change, any other outside entry or any other count aborts;
  - web_quotes: the class drops by exactly the conversions, quotes_checked by the same number, and every other flag is
    identical;
  - citation_sweep's problems and check_marks' flags are unchanged;
  - SUITE PARITY: every other check is identical, with accounted exceptions: check_universals, check_register, and
    check_refs_mirror only if it moves. Each also runs on the input and the output with every converted span's interior blanked
    (delimiters kept), and those runs must agree exactly. In the unblanked runs nothing is removed and every addition sits at a
    converted path, field or row. The triage count moves by exactly
    -(conversions) + (universals added) + (register added) + (refs_mirror added).
A real run requires --install-receipt, an input that is the output of the CWO-EZ-13 manifest, and #e7's gate
cwo18_real_run_may_proceed (#e7 CWO18-R1-1 makes its gate the CWO-EZ-18 gate). --dry-run evaluates everything, writes the full report to the scratch directory, and writes nothing
under SP.

Usage: _cwo18_gloss_quotes.py --in repair/rows_v3_cwo13.jsonl --out repair/rows_v3_cwo18.jsonl --expect-in <sha256>
       --scratch <session scratchpad> [--install-receipt <receipt>] [--dry-run]"""
import argparse
import copy
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
TOOLS, CAMPAIGN = EZ / "tools", EZ.parent / "campaign"
sys.path.insert(0, str(EZ))
sys.path.insert(0, str(TOOLS))
from _sweep_common import REPAIR, dump_rows, load_rows, sha, sha_bytes, summary, write_sweep  # noqa: E402
from ezek_lib import load_verse_maps, norm_english, web_quote_found  # noqa: E402

_spec = importlib.util.spec_from_file_location("cwo_coverage_ezek", EZ / "_cwo_coverage_ezek.py")
_cov = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cov)
CANON_REF = _cov.CANON_REF

RULINGS_E4 = EZ / "ezek_controlling_agent_rulings_e4.v1.json"
RULINGS_E6 = EZ / "ezek_controlling_agent_rulings_e6.v1.json"
RULINGS_E7 = EZ / "ezek_controlling_agent_rulings_e7.v1.json"
RULINGS_E7_SHA = "2f83b81c5dbaefd00c1489607114e0c766fe9b95c86dad23b3773ccc034c1e9c"
ANALYSIS = REPAIR / "cwo18_questions_analysis.v1.json"
FIRST_DRY = REPAIR / "cwo18_dry_run_over_cwo13.v1.json"
CHAIN_HEAD_RULED = "324d23589924e405c09c3aeaf178867449ba33fa949cefa63258ff3250288f27"
# #e7 CWO18-R1-1: the one touched refs entry outside the strict R1 shape, before and after, pinned at its bytes
R1_OUTSIDE_PINNED = {"row": "P08-013", "path": "[105].boundary_evidence_refs[1]",
                     "bytes": "oshb:Ezek.36.26 “a new heart” — contrasted, single-witness, with oshb:Ezek.11.19 “one heart” (same witness); both spliced verbatim"}
R1_OUTSIDE_WHY = ("outside the strict R1 shape before this sweep and after it, its status unchanged: CWO-EZ-01 coverage v3 flags it "
                  "'outside the strict ruling-R1 shape (ref, optional dual, then a parenthesised disclosure)'; CWO-EZ-11 left it for "
                  "'words between refs in the head; a split would drop them'. This sweep touched it at two quote characters only "
                  "(#e7 CWO18-R1-1).")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
SUITE_TOOLS = ("run_validator_suite.py", "citation_sweep.py", "normalize_hebrew_in_json.py", "check_web_quotes.py",
               "check_refs_mirror.py", "check_marks.py", "check_universals.py", "check_language_zones.py", "ngram7.py",
               "cap_sweep.py", "check_register.py", "ezek_lib.py")
PROSE = ("boundary_rationale", "device_notes", "strongest_rejected_alternative")
CLASS = "curly quote with NO web: ref in its field"
QUOTE = re.compile(r"“([^”]+)”")
WREF = re.compile(r"web:(Ezek\.\d+\.\d+(?:-(?:Ezek\.)?\d+(?:\.\d+)?)?)")
HEBREW_CP = re.compile(r"[֐-׿]")
PATH = re.compile(r"^\[(\d+)\]\.([A-Za-z_]+)(?:\[(\d+)\])?$")
TOP = re.compile(r"^\[(\d+)\]\.([A-Za-z_]+)")
FLAT = re.compile(r"\[\d+\]\.[A-Za-z_]+")
GLOSS, LABEL, NEAR, VERB = "gloss", "short_common_label", "near_web_author", "verbatim_author"
CLASSES = (GLOSS, LABEL, NEAR, VERB)
CONVERT = (GLOSS, LABEL)
E6_RULINGS = ("CWO18-SCOPE-1", "CWO18-NEARWEB-1", "CWO18-SHORT-1")
# #e6 CWO18-SCOPE-1 (2): the hand counts are a cross-check only; the gate is the per-span equality
EXPECTED_COUNTS_E6 = {"prose": {GLOSS: 21, LABEL: 34, NEAR: 26, VERB: 37},
                      "outside_prose": {GLOSS: 4, LABEL: 11, NEAR: 4, VERB: 11}}
RULED_CITATION_PROBLEMS, RULED_MARK_FLAGS = 10, 78
R = "boundary_evidence_refs"
# #e6 CWO18-SCOPE-1's per-span enumeration of the 30 outside-prose spans: (row, field path in the row, span as the ruling
# writes it or None where the ruling names the path only, class). Each entry is checked present in the ruling's text.
OUTSIDE_RULED = (
    ("P02-020", R + "[8]", "Adaptations to a Qere which L and BHS, by their design, do not indicate", GLOSS),
    ("P02-020", R + "[9]", None, GLOSS),
    ("P08-002", R + "[3]", "We read punctuation in L differently from BHS", GLOSS),
    ("P08-010", R + "[0]", "and you, son of man", GLOSS),
    ("P02-006", R + "[1]", None, LABEL),
    ("P02-007", R + "[1]", None, LABEL),
    ("P02-007", R + "[2]", "river Chebar", LABEL),
    ("P08-002", R + "[1]", None, LABEL),
    ("P08-006", R + "[2]", None, LABEL),
    ("P08-007", R + "[5]", None, LABEL),
    ("P08-007", R + "[8]", "As I live", LABEL),
    ("P08-005", R + "[0]", None, LABEL),
    ("P08-012", R + "[1]", "son of man", LABEL),
    ("P08-015", R + "[0]", "my flock", LABEL),
    ("P08-013", R + "[1]", "a new heart", LABEL),
    ("P02-008", R + "[1]", "you have multiplied your slain", NEAR),
    ("P02-014", "literature_type_guess", "the days are prolonged, and every vision fails", NEAR),
    ("P08-007", R + "[9]", "they have been laid desolate", NEAR),
    ("P08-013", R + "[2]", "you will be my people", NEAR),
    ("P02-009", R + "[1]", None, VERB),
    ("P02-010", R + "[1]", None, VERB),
    ("P02-010", R + "[1]", None, VERB),
    ("P02-017", "literature_type_guess", "there is no peace", VERB),
    ("P02-018", R + "[4]", None, VERB),
    ("P08-001", R + "[1]", None, VERB),
    ("P08-015", R + "[3]", None, VERB),
    ("P08-007", R + "[2]", None, VERB),
    ("P08-007", R + "[6]", None, VERB),
    ("P08-013", R + "[1]", "one heart", VERB),
    ("P08-014", R + "[1]", None, VERB),
)
REMEDY = {
    ("prose", VERB): "add the inline web: ref with the span verbatim to the WEB bytes, or drop the curly form for single quotes",
    ("prose", NEAR): ("restore the WEB bytes verbatim (case and punctuation) inside the curly quotes and add the inline web: ref, "
                      "or rewrite it as a single-quoted gloss; never leave a WEB sentence with a changed first letter or a swapped "
                      "end mark inside curly quotes"),
    ("refs", VERB): ("add 'web:Ezek.C.V' inside the entry's own parenthetical with the span verbatim, or single-quote the span; "
                     "the landing suite's citation_sweep (HARD) decides whether that token is in shape - if it is not, "
                     "single-quote the span"),
    ("refs", NEAR): ("restore the WEB bytes verbatim (case and punctuation) and add 'web:Ezek.C.V' inside the entry's own "
                     "parenthetical, or single-quote the span; the landing suite's citation_sweep (HARD) decides whether that "
                     "token is in shape - if it is not, single-quote the span"),
    ("literature_type_guess", VERB): "use single quotes (a classification field carries no quotation)",
    ("literature_type_guess", NEAR): "use single quotes (a classification field carries no quotation)",
}
WQ_MAY_MOVE = ("quotes_checked", "flag_count", "flags", "status", "_exit")
UNIV_MAY_MOVE = ("claims_seen", "flag_count", "flags", "tier_vocabulary_dampened", "e16_exclusivity_undampened", "status", "_exit")
UNIV_COUNTS = ("claims_seen", "flag_count", "tier_vocabulary_dampened", "e16_exclusivity_undampened")
REG_MAY_MOVE = ("flag_count", "flags", "status", "_exit")
MIRROR_MAY_MOVE = ("flag_count", "flags", "orphan_ref_warn_rows", "orphan_ref_warn_count", "orphan_ref_warns", "status", "_exit")
MIRROR_COMPARED = ("flag_count", "flags", "orphan_ref_warn_rows", "orphan_ref_warn_count", "orphan_ref_warns")


def iter_strings(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from iter_strings(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from iter_strings(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o


def class_matches(s):
    if WREF.search(s):
        return []
    out = []
    for qm in QUOTE.finditer(s):
        span = qm.group(1).strip()
        if len(span.split()) < 2 or len(HEBREW_CP.findall(span)) > len(re.findall(r"[A-Za-z]", span)):
            continue
        out.append(qm)
    return out


def field_kind(path):
    m = PATH.fullmatch(path)
    if not m:
        return None
    if m.group(3) is not None:
        return "refs" if m.group(2) == R else None
    return "prose" if m.group(2) in PROSE else ("literature_type_guess" if m.group(2) == "literature_type_guess" else None)


def get_at(rows, path):
    m = PATH.fullmatch(path)
    v = rows[int(m.group(1))][m.group(2)]
    return v[int(m.group(3))] if m.group(3) is not None else v


def set_at(rows, path, s):
    m = PATH.fullmatch(path)
    if m.group(3) is not None:
        rows[int(m.group(1))][m.group(2)][int(m.group(3))] = s
    else:
        rows[int(m.group(1))][m.group(2)] = s


def canon(xs):
    return sorted(json.dumps(x, sort_keys=True, ensure_ascii=False) for x in xs)


def claims(u):
    return Counter((f["path"], f["claim"]) for f in u.get("flags", []))


def reg_keys(r):
    return Counter((f.get("decision_id"), f.get("field"), f.get("class"), f.get("match")) for f in r.get("flags", []))


def mirror_keys(r):
    return Counter(json.dumps(x, sort_keys=True, ensure_ascii=False) for x in r.get("flags", []) + r.get("orphan_ref_warns", []))


def fold(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]", " ", norm_english(s).lower())).strip()


def receipt_gate(path):
    p = Path(path)
    rec = json.loads(p.read_text(encoding="utf-8"))
    if rec.get("schema") != "m8_tool_install_receipt.v1" or rec.get("book") != "Ezek":
        raise SystemExit("ABORT: %s is not an Ezek tool install receipt" % p.name)
    bound = {}
    for name, f in rec["files"].items():
        if f.get("state") != "installed":
            continue
        loc = (EZ.parent / name) if name.startswith("campaign/") else next((d / name for d in (TOOLS, EZ, CAMPAIGN) if (d / name).exists()), None)
        if loc is None or sha(loc) != f["after"]:
            raise SystemExit("ABORT: %s does not carry the digest %s... that receipt %s installed" % (name, f["after"][:16], rec.get("batch")))
        bound[name] = f["after"]
    return {"batch": rec.get("batch"), "receipt": p.name, "receipt_sha256": sha(p), "ordered_by": rec.get("ordered_by"), "files_bound": bound}


def probe(rows, td):
    body = dump_rows(rows)
    p = Path(td) / "rows.jsonl"
    rep_p = Path(str(p) + ".validator_report.json")
    p.write_bytes(body)
    if rep_p.exists():
        rep_p.unlink()
    r = subprocess.run([sys.executable, str(TOOLS / "run_validator_suite.py"), str(p)], capture_output=True, text=True,
                       encoding="utf-8", env=ENV, cwd=str(TOOLS))
    if not rep_p.exists():
        raise SystemExit("ABORT: the suite wrote no report (exit %s): %s" % (r.returncode, r.stderr[-600:]))
    rep = json.loads(rep_p.read_text(encoding="utf-8"))
    rep.pop("rows_file", None)
    return sha_bytes(body), rep


def tool_json(tool, rows, td):
    p = Path(td) / "rows.jsonl"
    p.write_bytes(dump_rows(rows))
    r = subprocess.run([sys.executable, str(TOOLS / tool), str(p)], capture_output=True, text=True, encoding="utf-8", env=ENV, cwd=str(TOOLS))
    return json.loads(r.stdout)


def blank(rows, converted):
    rr = copy.deepcopy(rows)
    for path, spans in converted.items():
        s = get_at(rr, path)
        for a, b in spans:
            s = s[:a + 1] + " " * (b - a - 2) + s[b - 1:]
        set_at(rr, path, s)
    return rr


def differing(rep_in, rep_out, skip=()):
    out = {}
    for k in sorted(set(rep_in) | set(rep_out)):
        a, b = rep_in.get(k), rep_out.get(k)
        if k in skip or a == b:
            continue
        out[k] = sorted(kk for kk in set(a) | set(b) if a.get(kk) != b.get(kk)) if isinstance(a, dict) and isinstance(b, dict) else "value"
    return out


def ruled_digest(e6, name):
    hits = [x.get("sha256") for x in e6.get("inputs_ruled_on", []) if str(x.get("path", "")).replace("\\", "/").endswith("/" + name)]
    return hits[0] if len(hits) == 1 else None


def expected_prose(analysis, first):
    """{(row, field, offset): class} for every prose class span, from the pinned first dry run and analysis file."""
    exp, problems = {}, []
    near = {(x["row"], x["field"], x["offset"]) for x in analysis["near_web_glosses"]["items"]}
    for c in first["changes"]:
        k = (c["row"], c["field"], c["offset"])
        exp[k] = NEAR if k in near else GLOSS
    if not near <= set(exp):
        problems.append("analysis near-WEB items that are not first-dry-run conversions: %s" % sorted(near - set(exp))[:5])
    labels = Counter()
    for x in analysis["routed_ii"]["items"]:
        k = (x["row"], x["field"], x["offset"])
        if k in exp:
            problems.append("prose span %s is both converted and routed in the pinned sources" % (k,))
        is_label = x["words"] <= 3 and x["verses_holding_it_verbatim"] >= 2
        exp[k] = LABEL if is_label else VERB
        if is_label:
            labels[(x["row"], x["field"], x["span"])] += 1
    short = Counter((x["row"], x["field"], x["span"]) for x in analysis["routed_ii"]["short_common_items"])
    if labels != short:
        problems.append("the analysis's routed items read as labels differ from its short_common_items: %s / %s"
                        % (list((labels - short).items())[:3], list((short - labels).items())[:3]))
    first_routed = Counter((x["row"], x["field"], x["offset"]) for x in first["routed_to_author_wave_cwo18"])
    if first_routed != Counter((x["row"], x["field"], x["offset"]) for x in analysis["routed_ii"]["items"]):
        problems.append("the analysis's routed items are not the first dry run's routed items")
    return exp, problems


def pick(entries, span):
    """The ruled class of one outside-prose span among the ruled entries at its row and path."""
    if not entries:
        return None
    classes = {c for _, c in entries}
    if len(classes) == 1:
        return next(iter(classes))
    s = span.strip()
    named = [c for sp, c in entries if sp is not None and sp in (s, s.rstrip(",.;:"))]
    return named[0] if len(named) == 1 else None


def expected_outside(analysis, scope_text):
    """{(row, path in row): [(span or None, class)]} from #e6's enumeration, checked against its text and the analysis facts."""
    problems, by_key = [], {}
    for row, suffix, span, cls in OUTSIDE_RULED:
        idx = re.search(r"\[(\d+)\]$", suffix)
        where = "refs[%s]" % idx.group(1) if idx else suffix
        if row not in scope_text or where not in scope_text or (span is not None and span not in scope_text):
            problems.append("ruled outside-prose entry %s %s %r is not in CWO18-SCOPE-1's text" % (row, suffix, span))
        by_key.setdefault((row, suffix), []).append((span, cls))
    facts = {}
    for it in analysis["outside_prose_fields"]["items"]:
        facts.setdefault((it["row"], it["path"].split("].", 1)[1]), []).append(it)
    if {k: len(v) for k, v in by_key.items()} != {k: len(v) for k, v in facts.items()}:
        problems.append("the ruled outside-prose paths are not the analysis's outside-prose paths")
    for k, items in facts.items():
        for it in items:
            cls = pick(by_key.get(k, []), it["span"])
            want = {GLOSS: (False, False), NEAR: (False, True)}.get(cls)
            if cls is None or (want and (it["web_verbatim"], it["web_folded"]) != want) or (cls in (LABEL, VERB) and not it["web_verbatim"]):
                problems.append("ruled class %s at %s %r disagrees with the analysis facts (web_verbatim %s, web_folded %s)"
                                % (cls, k, it["span"], it["web_verbatim"], it["web_folded"]))
    return by_key, problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--expect-in", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--install-receipt")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    in_path, out_path, scratch = EZ / a.inp, EZ / a.out, Path(a.scratch)
    if not scratch.is_dir():
        raise SystemExit("ABORT: --scratch %s is not a directory" % scratch)
    if not a.dry_run and not a.install_receipt:
        raise SystemExit("ABORT: a real run requires --install-receipt (#e6 CWO18-SCOPE-1 (3))")
    tools_bound = receipt_gate(a.install_receipt) if a.install_receipt else None
    if sha(in_path) != a.expect_in:
        raise SystemExit("ABORT: %s is %s, not the expected input %s" % (a.inp, sha(in_path)[:16], a.expect_in[:16]))
    if a.expect_in != CHAIN_HEAD_RULED:
        raise SystemExit("ABORT: #e6 ruled this sweep over %s...; the pinned per-span sources index those bytes" % CHAIN_HEAD_RULED[:16])
    cwo13_mf = REPAIR / (in_path.stem + ".manifest.json")
    mf13 = json.loads(cwo13_mf.read_text(encoding="utf-8")) if cwo13_mf.exists() else {}
    after_cwo13 = mf13.get("cwo") == "CWO-EZ-13" and mf13.get("output", {}).get("sha256") == a.expect_in
    if not a.dry_run and not after_cwo13:
        raise SystemExit("ABORT: the input is not the output of a CWO-EZ-13 manifest; CWO-EZ-18 runs after CWO-EZ-13")

    e4 = json.loads(RULINGS_E4.read_text(encoding="utf-8"))
    ruled4 = next(c for c in e4["corpus_wide_orders"] if c["id"] == "CWO-EZ-18")
    for phrase in ("web_quote_found", "ASCII single quotes", "U+2018/U+2019", "1,273 verses", CLASS, "prose field"):
        if phrase not in ruled4["order"] + ruled4["predicate"]:
            raise SystemExit("ABORT: %r is not in the CWO-EZ-18 that #e4 carries" % phrase)
    e6 = json.loads(RULINGS_E6.read_text(encoding="utf-8"))
    if e6.get("execution_id") != "ezek_controlling_rulings_a1#e6":
        raise SystemExit("ABORT: %s is not execution #e6" % RULINGS_E6.name)
    ruled6 = next((c for c in e6.get("corpus_wide_orders", []) if c.get("id") == "CWO-EZ-18"), None)
    if not ruled6 or "ezek_controlling_rulings_a1#e4" not in ruled6.get("amends", ""):
        raise SystemExit("ABORT: #e6 carries no CWO-EZ-18 amending #e4's")
    for phrase in ("web_quote_found", "ASCII single quotes", "U+2018/U+2019", "1,273 verses", "short common label",
                   "folded matcher", "strict R1 shape", "every string field check_web_quotes reads", CLASS):
        if phrase not in ruled6["order"] + ruled6["predicate"]:
            raise SystemExit("ABORT: %r is not in the CWO-EZ-18 that #e6 carries" % phrase)
    r6 = {r.get("id"): r for r in e6.get("rulings", [])}
    if any(i not in r6 for i in E6_RULINGS):
        raise SystemExit("ABORT: #e6 lacks one of %s" % (E6_RULINGS,))
    gate = e6.get("gate", {})
    if sha(RULINGS_E7) != RULINGS_E7_SHA:
        raise SystemExit("ABORT: %s is not at the digest #e7 wrote (%s...)" % (RULINGS_E7.name, RULINGS_E7_SHA[:16]))
    e7 = json.loads(RULINGS_E7.read_text(encoding="utf-8"))
    r7 = next((r for r in e7.get("rulings", []) if r.get("id") == "CWO18-R1-1"), None)
    if e7.get("execution_id") != "ezek_controlling_rulings_a1#e7" or r7 is None:
        raise SystemExit("ABORT: #e7 carries no CWO18-R1-1")
    r7_text = r7["decision"] + "\n" + "\n".join(o.get("order", "") for o in r7.get("orders", []))
    for phrase in ("r1_after == r1_before", "outside_r1_before == outside_r1_after == 1", R1_OUTSIDE_PINNED["bytes"], "'not touched'"):
        if phrase not in r7_text:
            raise SystemExit("ABORT: %r is not in the CWO18-R1-1 that #e7 carries" % phrase)
    gate7 = e7.get("gate", {})   # #e7 CWO18-R1-1: this execution's gate is the CWO-EZ-18 gate
    if not a.dry_run and gate7.get("cwo18_real_run_may_proceed") is not True:
        raise SystemExit("ABORT: #e7's gate does not let the CWO-EZ-18 real run proceed")
    scope_text = r6["CWO18-SCOPE-1"]["decision"]
    pins = {}
    for p in (ANALYSIS, FIRST_DRY):
        want = ruled_digest(e6, p.name)
        if want is None or sha(p) != want:
            raise SystemExit("ABORT: %s is not at the digest #e6 ruled on" % p.name)
        pins["Ezek/repair/" + p.name] = want
    analysis = json.loads(ANALYSIS.read_text(encoding="utf-8"))
    first = json.loads(FIRST_DRY.read_text(encoding="utf-8"))
    if analysis["input"]["sha256"] != sha(FIRST_DRY) or first["probe"]["input_bytes_reproduced"] is not True:
        raise SystemExit("ABORT: the analysis file does not index the first dry run, or that run did not reproduce its input")
    exp_prose, p_prose = expected_prose(analysis, first)
    exp_out, p_out = expected_outside(analysis, scope_text)

    web, _ = load_verse_maps()
    keys = list(web)
    order = [tuple(int(x) for x in k.split(".")[1:]) for k in keys]
    if len(keys) != 1273 or order != sorted(order):
        raise SystemExit("ABORT: the WEB verse map is not 1,273 verses in canonical order")
    all_web = [web[k]["text"] for k in keys]
    web_folded = " %s " % fold(" ".join(all_web))
    verse_folded = [" %s " % fold(t) for t in all_web]

    def classify(span):
        s = span.strip()
        if web_quote_found(s, all_web):
            vk = [k for k, t in zip(keys, all_web) if web_quote_found(s, [t])]
            return (LABEL if len(s.split()) <= 3 and len(vk) >= 2 else VERB), {"verse_keys": vk, "verses_holding_it_verbatim": len(vk)}
        fs = fold(s)
        if fs and " %s " % fs in web_folded:
            fk = [k for k, t in zip(keys, verse_folded) if " %s " % fs in t]
            return NEAR, {"folded_verse_keys": fk, "folded_verses": len(fk)}
        return GLOSS, {}

    rows_in = load_rows(in_path)
    rows_out = copy.deepcopy(rows_in)
    problems = p_prose + p_out
    spans, by_path, converted, changes, mismatches, r1, r1_outside = [], {}, {}, [], [], [], []
    with tempfile.TemporaryDirectory(dir=scratch, prefix="cwo18_probe_") as td:
        in_probe_sha, rep_in = probe(rows_in, td)
        wq_in = rep_in["web_quotes"]
        tool = Counter((f["path"], f["quote"]) for f in wq_in["flags"] if f.get("issue") == CLASS)
        replay, sites = Counter(), []
        for path, s in iter_strings(rows_in):
            for qm in class_matches(s):
                replay[(path, qm.group(1).strip()[:90])] += 1
                sites.append((path, qm))
        if replay != tool:
            raise SystemExit("ABORT: the replayed class differs from the installed tool's flags: tool-only %s; replay-only %s"
                             % (list((tool - replay).items())[:5], list((replay - tool).items())[:5]))
        by_field_name = Counter((TOP.match(p).group(2) if TOP.match(p) else p) + ("" if FLAT.fullmatch(p) else " (nested)") for p, _ in sites)
        for path, qm in sites:
            kind = field_kind(path)
            if kind is None:
                problems.append("a class span sits at %s, a field kind no ruling covers" % path)
                continue
            m = PATH.fullmatch(path)
            row = rows_in[int(m.group(1))]
            cls, facts = classify(qm.group(1))
            rec = {"row": row.get("decision_id"), "writer_decision_id": row.get("writer_decision_id"), "writer_part": row.get("writer_part"),
                   "path": path, "field": m.group(2), "field_kind": kind, "offset": qm.start(), "span": qm.group(1), "class": cls} | facts
            if kind == "prose":
                ruled = exp_prose.get((rec["row"], rec["field"], rec["offset"]))
            else:
                ruled = pick(exp_out.get((rec["row"], path.split("].", 1)[1]), []), qm.group(1))
            if ruled != cls:
                mismatches.append(rec | {"class_ruled": ruled})
            spans.append(rec)
            by_path.setdefault(path, []).append((qm, rec))
        seen_prose = {(r["row"], r["field"], r["offset"]) for r in spans if r["field_kind"] == "prose"}
        if seen_prose != set(exp_prose):
            problems.append("prose class spans differ from the pinned sources: unseen %s; unexpected %s"
                            % (sorted(set(exp_prose) - seen_prose)[:5], sorted(seen_prose - set(exp_prose))[:5]))
        seen_out = Counter((r["row"], r["path"].split("].", 1)[1]) for r in spans if r["field_kind"] != "prose")
        if seen_out != Counter({k: len(v) for k, v in exp_out.items()}):
            problems.append("outside-prose class spans differ from #e6's enumeration")
        if mismatches:
            problems.append("%d spans are classed otherwise than #e6 rules them; they return to the controlling lane" % len(mismatches))

        for path, items in sorted(by_path.items()):
            s = get_at(rows_in, path)
            new, replaced = s, []
            for qm, rec in sorted(items, key=lambda x: x[0].start(), reverse=True):
                if rec["class"] not in CONVERT:
                    continue
                span = qm.group(1)
                op, cl = ("‘", "’") if "'" in span else ("'", "'")
                new = new[:qm.start()] + op + span + cl + new[qm.end():]
                replaced.append(qm)
                converted.setdefault(path, []).append((qm.start(), qm.end()))
                rec["old"], rec["new"] = qm.group(0), op + span + cl
                changes.append({k: rec[k] for k in ("row", "writer_decision_id", "writer_part", "path", "field", "offset", "class", "old", "new")})
            if not replaced:
                continue
            diff_pos = [k for k, (x, y) in enumerate(zip(s, new)) if x != y]
            want_pos = sorted(p for q in replaced for p in (q.start(), q.end() - 1))
            if len(new) != len(s) or diff_pos != want_pos:
                problems.append("%s differs from its input beyond the replaced quote characters" % path)
            set_at(rows_out, path, new)
            if field_kind(path) == "refs":
                r1.append({"row": rows_in[int(PATH.fullmatch(path).group(1))]["decision_id"], "path": path,
                           "r1_before": bool(CANON_REF.match(s)), "r1_after": bool(CANON_REF.match(new))})
                if not (r1[-1]["r1_before"] and r1[-1]["r1_after"]):
                    r1_outside.append(dict(r1[-1], old=s, new=new, why=R1_OUTSIDE_WHY))
        changes.sort(key=lambda c: (c["row"], c["path"], c["offset"]))
        restore = copy.deepcopy(rows_out)
        for path in converted:
            set_at(restore, path, get_at(rows_in, path))
        only_converted = restore == rows_in
        if not only_converted:
            problems.append("something other than the strings holding a conversion changed")
        not_r1 = [x for x in r1 if not x["r1_after"]]
        out_before = [x for x in r1 if not x["r1_before"]]
        status_changed = [x for x in r1 if x["r1_after"] != x["r1_before"]]
        if status_changed:
            problems.append("touched refs entries whose strict-R1-shape status changed: %s" % status_changed[:8])
        pinned_ok = (len(out_before) == len(not_r1) == 1
                     and [(x["row"], x["path"]) for x in out_before] == [(R1_OUTSIDE_PINNED["row"], R1_OUTSIDE_PINNED["path"])]
                     and [(x["row"], x["path"]) for x in not_r1] == [(R1_OUTSIDE_PINNED["row"], R1_OUTSIDE_PINNED["path"])]
                     and get_at(rows_in, R1_OUTSIDE_PINNED["path"]) == R1_OUTSIDE_PINNED["bytes"])
        if not pinned_ok:
            problems.append("the touched refs entries outside the strict R1 shape are not exactly the one entry #e7 CWO18-R1-1 pins "
                            "(%s %s at its bytes): before %s; after %s" % (R1_OUTSIDE_PINNED["row"], R1_OUTSIDE_PINNED["path"],
                                                                         [(x["row"], x["path"]) for x in out_before],
                                                                         [(x["row"], x["path"]) for x in not_r1]))
        out_sha, rep_out = probe(rows_out, td)
        b_in, b_out = blank(rows_in, converted), blank(rows_out, converted)
        ub_in, ub_out = tool_json("check_universals.py", b_in, td), tool_json("check_universals.py", b_out, td)
        rb_in, rb_out = tool_json("check_register.py", b_in, td), tool_json("check_register.py", b_out, td)
        mirror_moved = rep_in.get("refs_mirror") != rep_out.get("refs_mirror")
        mb_in, mb_out = ((tool_json("check_refs_mirror.py", b_in, td), tool_json("check_refs_mirror.py", b_out, td))
                         if mirror_moved else (None, None))

    n_conv = len(changes)
    wq_out = rep_out["web_quotes"]
    cls_in = sum(tool.values())
    cls_out = sum(1 for f in wq_out["flags"] if f.get("issue") == CLASS)
    if cls_out != cls_in - n_conv:
        problems.append("the class went %d -> %d, not down by the %d conversions" % (cls_in, cls_out, n_conv))
    if canon(f for f in wq_in["flags"] if f.get("issue") != CLASS) != canon(f for f in wq_out["flags"] if f.get("issue") != CLASS):
        problems.append("web_quotes flags outside the class changed")
    wq_moved = sorted(k for k in set(wq_in) | set(wq_out) if k not in WQ_MAY_MOVE and wq_in.get(k) != wq_out.get(k))
    if wq_moved:
        problems.append("web_quotes keys outside the class changed: %s" % wq_moved)
    if wq_in.get("quotes_checked", 0) - wq_out.get("quotes_checked", 0) != n_conv:
        problems.append("quotes_checked did not drop by the conversions")
    cs_n = len(rep_in["citation_sweep"].get("problems", []))
    mk_n = len(rep_in["mark_symmetry"].get("flags", []))
    if canon(rep_in["citation_sweep"].get("problems", [])) != canon(rep_out["citation_sweep"].get("problems", [])):
        problems.append("citation_sweep problems changed")
    if canon(rep_in["mark_symmetry"].get("flags", [])) != canon(rep_out["mark_symmetry"].get("flags", [])):
        problems.append("check_marks flags changed")
    if (cs_n, mk_n) != (RULED_CITATION_PROBLEMS, RULED_MARK_FLAGS):
        problems.append("citation_sweep problems %d and check_marks flags %d on the input are not the %d and %d #e6 ruled on"
                        % (cs_n, mk_n, RULED_CITATION_PROBLEMS, RULED_MARK_FLAGS))
    conv_paths = set(converted) | {p.rsplit("[", 1)[0] for p in converted if field_kind(p) == "refs"}
    conv_fields, conv_ids = set(), set()
    for p in converted:
        m = PATH.fullmatch(p)
        row = rows_in[int(m.group(1))]
        names = {m.group(2)} | ({"%s[%s]" % (m.group(2), m.group(3))} if m.group(3) is not None else set())
        conv_ids.add(row.get("decision_id"))
        for idk in ("decision_id", "writer_decision_id"):
            conv_fields |= {(row.get(idk), n) for n in names}

    ui, uo = rep_in["universals"], rep_out["universals"]
    u_removed, u_added = claims(ui) - claims(uo), claims(uo) - claims(ui)
    u_blank_same = claims(ub_in) == claims(ub_out) and all(ub_in.get(k) == ub_out.get(k) for k in UNIV_COUNTS)
    u_added_off = [[p, c, n] for (p, c), n in u_added.items() if p not in conv_paths]
    u_other = sorted(k for k in set(ui) | set(uo) if k not in UNIV_MAY_MOVE and ui.get(k) != uo.get(k))
    flags_added = uo.get("flag_count", 0) - ui.get("flag_count", 0)
    if not u_blank_same:
        problems.append("check_universals differs between the blanked input and output: the change reaches beyond the converted spans")
    if u_removed or u_added_off or u_other or flags_added != sum(u_added.values()):
        problems.append("check_universals moved beyond the converted spans: removed %s; added off converted paths %s; other keys %s; "
                        "flag_count +%d against %d added" % (list(u_removed.items())[:5], u_added_off[:5], u_other, flags_added, sum(u_added.values())))

    gi, go = rep_in["register"], rep_out["register"]
    g_removed, g_added = reg_keys(gi) - reg_keys(go), reg_keys(go) - reg_keys(gi)
    g_blank_same = reg_keys(rb_in) == reg_keys(rb_out) and rb_in.get("flag_count") == rb_out.get("flag_count")
    g_added_off = [list(k) + [n] for k, n in g_added.items() if (k[0], k[1]) not in conv_fields]
    g_other = sorted(k for k in set(gi) | set(go) if k not in REG_MAY_MOVE and gi.get(k) != go.get(k))
    reg_added = go.get("flag_count", 0) - gi.get("flag_count", 0)
    g_context_only = sum((Counter(canon(gi.get("flags", []))) - Counter(canon(go.get("flags", [])))).values()) - sum(g_removed.values())
    if not g_blank_same:
        problems.append("check_register differs between the blanked input and output: the change reaches beyond the converted spans")
    if g_removed or g_added_off or g_other or reg_added != sum(g_added.values()):
        problems.append("check_register moved beyond the converted spans: removed %s; added off converted fields %s; other keys %s; "
                        "flag_count +%d against %d added" % (list(g_removed.items())[:5], g_added_off[:5], g_other, reg_added, sum(g_added.values())))

    mirror = {"moved": mirror_moved}
    mirror_added = 0
    if mirror_moved:
        mi, mo = rep_in["refs_mirror"], rep_out["refs_mirror"]
        m_blank_same = all(mb_in.get(k) == mb_out.get(k) for k in MIRROR_COMPARED)
        m_removed, m_added = mirror_keys(mi) - mirror_keys(mo), mirror_keys(mo) - mirror_keys(mi)
        m_added_off = [k for k in m_added if json.loads(k).get("decision_id") not in conv_ids]
        m_other = sorted(k for k in set(mi) | set(mo) if k not in MIRROR_MAY_MOVE and mi.get(k) != mo.get(k))
        mirror_added = mo.get("flag_count", 0) - mi.get("flag_count", 0)
        if not m_blank_same:
            problems.append("check_refs_mirror differs between the blanked input and output: the change reaches beyond the converted spans")
        if m_removed or m_added_off or m_other:
            problems.append("check_refs_mirror moved beyond the converted rows: removed %d; added off converted rows %d; other keys %s"
                            % (sum(m_removed.values()), len(m_added_off), m_other))
        mirror |= {"blanked_runs_identical": m_blank_same, "flag_count": [mi.get("flag_count"), mo.get("flag_count")],
                   "orphan_ref_warn_count": [mi.get("orphan_ref_warn_count"), mo.get("orphan_ref_warn_count")],
                   "added": [json.loads(k) for k in sorted(m_added)], "removed": [json.loads(k) for k in sorted(m_removed)]}

    skip = ("web_quotes", "universals", "register", "summary") + (("refs_mirror",) if mirror_moved else ())
    parity = differing(rep_in, rep_out, skip=skip)
    if parity:
        problems.append("suite parity broken outside the accounted checks: %s" % parity)
    si, so = rep_in.get("summary", {}), rep_out.get("summary", {})
    if si.get("hard_status") != so.get("hard_status") or si.get("nfd_hard_e01") != so.get("nfd_hard_e01") or \
            si.get("triage_flags", 0) - so.get("triage_flags", 0) != n_conv - flags_added - reg_added - mirror_added:
        problems.append("the suite summary moved other than by -(conversions) + (universals, register and refs_mirror added): %s -> %s" % (si, so))

    order_key = lambda r: (r["row"], r["path"], r["offset"])  # noqa: E731
    counts = {"prose": Counter(), "outside_prose": Counter()}
    for r in spans:
        counts["prose" if r["field_kind"] == "prose" else "outside_prose"][r["class"]] += 1
    counts = {k: {c: v.get(c, 0) for c in CLASSES} for k, v in counts.items()}
    class_lists = {c: sorted((r for r in spans if r["class"] == c), key=order_key) for c in CLASSES}
    author_items, label_items = [], []
    for r in sorted(spans, key=order_key):
        base = {k: r[k] for k in ("row", "writer_decision_id", "writer_part", "path", "field", "field_kind", "offset", "span", "class")}
        if r["class"] == VERB:
            keys_ = ", ".join(r["verse_keys"]) or "no single verse (the span crosses a verse boundary)"
            text = ("CWO-EZ-18 (ii) verbatim_author (ezek_controlling_rulings_a1#e6 CWO18-SCOPE-1): a WEB-verbatim quotation without its "
                    "inline web: ref - %s; verses holding it verbatim: %s. Spans unchanged." % (REMEDY[(r["field_kind"], VERB)], keys_))
            author_items.append(base | {"verse_keys": r["verse_keys"], "item": text})
        elif r["class"] == NEAR:
            keys_ = ", ".join(r["folded_verse_keys"]) or "no single verse (the folded span crosses a verse boundary)"
            text = ("CWO-EZ-18 (ii) near_web_author (ezek_controlling_rulings_a1#e6 CWO18-NEARWEB-1): a WEB quotation carried inexactly - "
                    "%s; verses holding it once case and punctuation are folded: %s%s. Spans unchanged."
                    % (REMEDY[(r["field_kind"], NEAR)], keys_, "; name the verse the row means" if r["folded_verses"] > 1 else ""))
            author_items.append(base | {"folded_verse_keys": r["folded_verse_keys"], "item": text})
        elif r["class"] == LABEL:
            text = ("CWO-EZ-18 short_common_label (ezek_controlling_rulings_a1#e6 CWO18-SHORT-1), INFORMATIONAL - no action required: "
                    "converted to a single-quoted label (verbatim in %d WEB verses); if a quotation of one verse was meant, restore the "
                    "curly form with the inline web: ref. Spans unchanged." % r["verses_holding_it_verbatim"])
            label_items.append(base | {"old": r["old"], "new": r["new"], "verse_keys": r["verse_keys"], "item": text})
    extra = {
        "predicate_label": "CWO-EZ-18 predicate as WIDENED by ezek_controlling_rulings_a1#e6 CWO18-SCOPE-1: every string field check_web_quotes reads",
        "ruled_order_e4": ruled4["order"], "ruled_predicate_e4": ruled4["predicate"],
        "ruled_order_e6": ruled6["order"], "ruled_predicate_e6": ruled6["predicate"], "ruled_amends_e6": ruled6["amends"],
        "ruled_why_e6": ruled6.get("why"),
        "originally_ordered_by": {"execution": "ezek_controlling_rulings_a1#e4", "rulings_file": "Ezek/" + RULINGS_E4.name,
                                  "rulings_sha256": sha(RULINGS_E4)},
        "rulings_applied_e6": {"execution": "ezek_controlling_rulings_a1#e6", "rulings_file": "Ezek/" + RULINGS_E6.name,
                               "rulings_sha256": sha(RULINGS_E6), "rulings": list(E6_RULINGS),
                               "gate_cwo18_real_run_may_proceed": gate.get("cwo18_real_run_may_proceed"),
                               "author_orders_verbatim": {i: [o["order"] for o in r6[i].get("orders", []) if o.get("to") == "author_fixup"]
                                                          for i in E6_RULINGS}},
        "input_is_cwo13_output": after_cwo13,
        "web_text": {"source": "tools/verse_map_web.json (built from Ezek_web_clean.txt by build_verse_maps.py)", "verses": len(keys),
                     "verse_map_sha256": sha(TOOLS / "verse_map_web.json"), "web_clean_sha256": sha(EZ / "Ezek_web_clean.txt"),
                     "exact_matcher": "ezek_lib.web_quote_found over all verses joined in canonical order; per verse for the label count",
                     "folded_matcher": "' ' + fold(span) + ' ' in ' ' + fold(all verses joined) + ' '; fold = norm_english, lowercase, "
                                       "non-alphanumerics to space, whitespace collapsed"},
        "class_in": {"spans": cls_in, "rows": len({p.split("]")[0] for p, _ in tool}), "by_field": dict(sorted(by_field_name.items()))},
        "class_out": cls_out, "conversions": n_conv, "rows_with_conversions": len({c["row"] for c in changes}),
        "class_counts": counts,
        "class_counts_cross_check_e6": {"expected": EXPECTED_COUNTS_E6, "equal": counts == EXPECTED_COUNTS_E6,
                                        "note": "a cross-check only; the gate is the per-span equality (#e6 CWO18-SCOPE-1 (2))"},
        "class_lists": class_lists,
        "routed_to_author_wave_cwo18": author_items,
        "routed_to_author_wave_cwo18_informational_labels": label_items,
        "assert_replay_reproduces_tool_class": True,
        "assert_per_span_class_equality": {"spans": len(spans), "mismatches": mismatches, "pinned_sources": pins,
                                           "outside_prose_entries_ruled": len(OUTSIDE_RULED),
                                           "source_problems": p_prose + p_out},
        "assert_changed_only_at_quote_characters": not any("beyond the replaced" in p for p in problems),
        "assert_only_converted_strings_changed": only_converted,
        "assert_r1_shape_after": {"reads_as": ("ezek_controlling_rulings_a1#e7 CWO18-R1-1: shape-status preservation per touched "
                                               "entry (r1_after == r1_before); outside_r1_after == outside_r1_before == 1, the one "
                                               "entry reported"),
                                  "touched_entries": len(r1), "outside_r1_after": len(not_r1), "outside_r1_before": len(out_before),
                                  "status_unchanged_every_entry": not status_changed,
                                  "outside_pinned_to_the_one_entry_e7_rules": pinned_ok,
                                  "outside_entries_reported": r1_outside, "entries": r1},
        "assert_class_drops_by_conversions": cls_out == cls_in - n_conv,
        "assert_other_web_quotes_flags_unchanged": "web_quotes flags outside the class changed" not in problems,
        "assert_citation_sweep_problems_unchanged": {"problems": cs_n},
        "assert_check_marks_flags_unchanged": {"flags": mk_n},
        "assert_suite_parity": {
            "checks_compared": sorted(rep_in),
            "differences_outside_accounted_checks": parity,
            "universals_accounted": {
                "rule": ("check_universals ignores curly-double-quoted text, so a converted span's interior becomes visible to it; the "
                         "blanked input and output runs agree exactly; nothing is removed; every addition sits at a converted path"),
                "blanked_runs_identical": u_blank_same,
                "claims_seen": [ui.get("claims_seen"), uo.get("claims_seen")], "flag_count": [ui.get("flag_count"), uo.get("flag_count")],
                "flags_added": [{"path": p, "claim": c, "n": n} for (p, c), n in sorted(u_added.items())],
                "flags_removed": [{"path": p, "claim": c, "n": n} for (p, c), n in sorted(u_removed.items())]},
            "register_accounted": {
                "rule": ("check_register masks curly-double-quoted text too; flags compared by (row, field, class, match): the blanked "
                         "input and output runs agree exactly, nothing is removed, every addition sits at a converted field, and a context "
                         "snippet that changed only because a quote character inside it changed is not a difference"),
                "blanked_runs_identical": g_blank_same, "flag_count": [gi.get("flag_count"), go.get("flag_count")],
                "flags_added": [list(k) + [n] for k, n in sorted(g_added.items(), key=str)],
                "flags_removed": [list(k) + [n] for k, n in sorted(g_removed.items(), key=str)],
                "context_only_changes": g_context_only},
            "refs_mirror_accounted": mirror,
            "summary_in": si, "summary_out": so},
        "probe": {"output_sha256": out_sha, "input_bytes_reproduced": in_probe_sha == a.expect_in,
                  "tools_sha256": {n: sha(TOOLS / n) for n in SUITE_TOOLS}},
        "tools_bound_to_install_receipt": tools_bound,
        "old_and_new_bytes_per_change": True,
        "rulings_applied_e7": {"execution": "ezek_controlling_rulings_a1#e7", "rulings_file": "Ezek/" + RULINGS_E7.name,
                               "rulings_sha256": sha(RULINGS_E7), "ruling": "CWO18-R1-1", "decision_verbatim": r7["decision"],
                               "orders_verbatim": r7.get("orders", []),
                               "gate_cwo18_real_run_may_proceed": gate7.get("cwo18_real_run_may_proceed"),
                               "gate_note_verbatim": gate7.get("cwo18_real_run_note")},
        "script": {"path": "Ezek/_cwo18_gloss_quotes.py", "sha256": sha(Path(__file__))},
    }
    if "not touched" in json.dumps({k: v for k, v in extra.items() if k != "rulings_applied_e7"}, ensure_ascii=False):
        problems.append("the manifest uses the words 'not touched'; #e7 CWO18-R1-1 forbids them for the entry this sweep touches")
    if a.dry_run or problems:
        report = {"verdict": ("DRY RUN - nothing written under SP" if not problems else "ABORT - nothing written"), "problems": problems,
                  "changes": changes} | extra
        rp = scratch / "cwo18_dry_run_amended.json"
        rp.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        print(json.dumps({"verdict": report["verdict"], "problems": problems, "class_in": extra["class_in"], "class_out": cls_out,
                          "class_counts": counts, "counts_equal_e6_cross_check": counts == EXPECTED_COUNTS_E6,
                          "conversions": n_conv, "author_items": len(author_items), "label_items": len(label_items),
                          "per_span_mismatches": len(mismatches), "r1": extra["assert_r1_shape_after"] | {"entries": len(r1)},
                          "parity_differences": parity, "refs_mirror": {k: v for k, v in mirror.items() if k in ("moved", "blanked_runs_identical", "flag_count")},
                          "universals": {"blanked_runs_identical": u_blank_same, "added": sum(u_added.values()), "removed": sum(u_removed.values())},
                          "register": {"blanked_runs_identical": g_blank_same, "added": sum(g_added.values()), "removed": sum(g_removed.values()),
                                       "context_only_changes": g_context_only},
                          "citation_problems": cs_n, "mark_flags": mk_n, "summary_in": si, "summary_out": so,
                          "input_is_cwo13_output": after_cwo13, "input_bytes_reproduced": extra["probe"]["input_bytes_reproduced"],
                          "would_write_sha256": out_sha, "tools_bound": bool(tools_bound), "report": str(rp)}, ensure_ascii=False, indent=1))
        raise SystemExit(1 if problems else 0)
    mf = write_sweep("CWO-EZ-18 (as amended by ezek_controlling_rulings_a1#e6; R1 clause as read by ezek_controlling_rulings_a1#e7)", in_path, out_path, rows_in, rows_out, changes, extra,
                     ordered_by=("ezek_controlling_rulings_a1#e6", RULINGS_E6))
    if mf["output"]["sha256"] != out_sha:
        raise SystemExit("ABORT: the written bytes differ from the probed bytes")
    print(json.dumps(summary(mf), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
