#!/usr/bin/env python3
"""Mechanical check of BIBLE_CHUNKING_METHOD.vN.md, with a negative control (v6 obligation 12).

WHY THIS EXISTS. v5's change table claims "a mechanical check now verifies every section this table names". Measured
2026-09-21: no such check existed anywhere under this generation's tree - its bytes were not retained. A check whose
bytes are gone is indistinguishable from a check that never ran, so the claim was unfalsifiable. This tool is kept
beside the document it checks, and it is BIDIRECTIONAL: every section the newest change table's Change column names
must carry a version marker for this version, AND every section carrying such a marker must be named in that table.
One direction alone still passes a table row pointing at a section nobody touched.

The version marker is 'new in vN' (any case) or '(vN,' / '(vN)'. The front matter, the version-history section and the
provenance tail are excluded from the marker side, because they talk ABOUT the version by definition.

Usage: check_method_record.py [<doc.md>]        checks the document, writes method_record_check.vN.json beside it
       check_method_record.py --selftest        tampers with a copy six ways and requires the right check to fail
Exit 0 PASS, 1 FAIL, 2 input error. Read-only apart from its own check record."""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

M8 = Path(__file__).resolve().parent
DEFAULT_DOC = M8 / "BIBLE_CHUNKING_METHOD.v6.md"
SEC_RE = re.compile(r"(?m)^## (\d+)\. ")
MARKER_RE = re.compile(r"(?i)new in v(\d+)\b|\(v(\d+)[,)]")
ITEM_RE = re.compile(r"(?m)^(\d+)\. \*\*")
BAN = "review by a single lens is prohibited"
PLACEHOLDERS = ("TODO", "TBD", "FIXME", "XXX", "<fill", "LOREM")


def sections(text):
    """number -> body, where body runs to the next '## N.' heading or the provenance tail."""
    marks = [(int(m.group(1)), m.start()) for m in SEC_RE.finditer(text)]
    tail = text.find("## Provenance and limits of this version")
    out = {}
    for i, (num, pos) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else (tail if tail > pos else len(text))
        out[num] = text[pos:end]
    return out


def newest_change_table(text, ver):
    """The rows of the '### v(ver-1) -> v(ver)' subsection's table."""
    head = re.search(r"(?m)^### v%d → v%d\b.*$" % (ver - 1, ver), text)
    if not head:
        return None
    rest = text[head.end():]
    nxt = re.search(r"(?m)^#{2,3} ", rest)
    block = rest[:nxt.start()] if nxt else rest
    rows = [ln for ln in block.splitlines() if ln.startswith("| ") and not ln.startswith("|---")]
    return [ln for ln in rows if not re.match(r"\|\s*Change\s*\|", ln)]


def evaluate(doc):
    text = doc.read_text(encoding="utf-8")
    res, failed = {}, []

    def check(name, ok, detail):
        res[name] = {"ok": bool(ok), "detail": detail}
        if not ok:
            failed.append(name)

    m_file = re.search(r"\.v(\d+)\.md$", doc.name)
    m_title = re.match(r"# BIBLE CHUNKING METHOD — v(\d+)\n", text)
    m_this = re.search(r"\*\*This version:\*\* v(\d+),", text)
    ver = int(m_file.group(1)) if m_file else (int(m_title.group(1)) if m_title else 0)
    if not ver:
        print("FAIL: cannot determine the version from the filename or the title line")
        sys.exit(2)
    check("header_version_matches_filename",
          m_title and m_this and int(m_title.group(1)) == ver and int(m_this.group(1)) == ver,
          "filename v%d, title %s, this-version %s" % (ver, m_title and m_title.group(1), m_this and m_this.group(1)))

    m_sup = re.search(r"\*\*Supersedes v(\d+)\*\* \(`(BIBLE_CHUNKING_METHOD\.v\d+\.md)`, sha256\s*\n?`([0-9a-f]{64})`",
                      text)
    if not m_sup:
        check("superseded_digest_true", False, "no parseable 'Supersedes vM (file, sha256 hex)' statement")
    else:
        prior = M8 / m_sup.group(2)
        real = hashlib.sha256(prior.read_bytes()).hexdigest() if prior.exists() else "ABSENT"
        check("superseded_digest_true", real == m_sup.group(3),
              "%s cited %s, measured %s" % (m_sup.group(2), m_sup.group(3)[:12], real[:12]))

    secs = sections(text)
    rows = newest_change_table(text, ver)
    if rows is None:
        check("change_table_present", False, "no '### v%d → v%d' change table" % (ver - 1, ver))
        named = set()
    else:
        check("change_table_present", len(rows) > 0, "%d rows" % len(rows))
        named = set()
        for ln in rows:
            cells = ln.split("|")
            named |= {int(n) for n in re.findall(r"§(\d+)", cells[1] if len(cells) > 1 else "")}
        check("change_table_names_real_sections", named and named <= set(secs),
              "table names %s, missing %s" % (sorted(named), sorted(named - set(secs))))

    marked = set()
    for num, body in secs.items():
        if num == 0:
            continue
        if any(int(a or b) == ver for a, b in MARKER_RE.findall(body)):
            marked.add(num)
    check("marker_table_bidirectional", marked == named,
          "marked %s, named %s, marked-not-named %s, named-not-marked %s"
          % (sorted(marked), sorted(named), sorted(marked - named), sorted(named - marked)))

    want_ob = max([int(n) for ln in (rows or []) for n in
                   re.findall(r"obligations? (\d+)(?: and (\d+))?", ln) for n in n if n] or [0])
    ob = [int(m.group(1)) for m in ITEM_RE.finditer(secs.get(16, ""))]
    check("obligations_contiguous_and_complete",
          ob == list(range(1, len(ob) + 1)) and len(ob) >= max(want_ob, 11),
          "%d obligations, contiguous %s, table asks for at least %d" % (len(ob), ob == list(range(1, len(ob) + 1)),
                                                                        max(want_ob, 11)))

    q = [int(m.group(1)) for m in ITEM_RE.finditer(secs.get(13, ""))]
    check("open_questions_contiguous_and_carried", q == list(range(1, len(q) + 1)) and len(q) >= 8,
          "%d questions handed forward, contiguous %s" % (len(q), q == list(range(1, len(q) + 1))))

    hist = [k for k in range(1, ver) if re.search(r"(?m)^### v%d → v%d\b" % (k, k + 1), text)]
    check("version_history_complete", len(hist) == ver - 1 and "### v1 (" in text,
          "transitions present %s of %d, origin entry %s" % (hist, ver - 1, "### v1 (" in text))

    earlier = {k: (M8 / ("BIBLE_CHUNKING_METHOD.v%d.md" % k)) for k in range(1, ver)}
    check("earlier_versions_on_disk", all(p.exists() and p.stat().st_size > 0 for p in earlier.values()),
          "; ".join("v%d %s" % (k, p.stat().st_size if p.exists() else "ABSENT") for k, p in earlier.items()))

    check("lens_floor_intact", BAN in text and 19 in secs and "### The ban" in secs.get(19, ""),
          "ban sentence %s, §19 %s" % (BAN in text, 19 in secs))

    hits = [p for p in PLACEHOLDERS if p in text]
    check("no_placeholders", not hits, "found %s" % hits)

    prov = text[text.find("## Provenance and limits of this version"):] if "## Provenance and limits" in text else ""
    check("provenance_tail_complete",
          bool(prov) and "**Not verified:**" in prov and "Checked mechanically" in prov and "generated" in prov,
          "%d bytes" % len(prov))

    gen = M8 / ("gen_method_v%d.py" % ver)
    if doc.resolve() == (M8 / ("BIBLE_CHUNKING_METHOD.v%d.md" % ver)).resolve() and gen.exists():
        p = subprocess.run([sys.executable, str(gen), "--check"], capture_output=True, text=True, cwd=str(M8))
        check("generated_deterministically", p.returncode == 0 and "MATCH" in p.stdout,
              (p.stdout.strip().splitlines() or ["no output"])[-1])
    else:
        res["generated_deterministically"] = {"ok": None, "detail": "SKIP: not the canonical file, or no generator"}

    return ver, text, res, failed


def report(doc):
    ver, text, res, failed = evaluate(doc)
    run = sum(1 for v in res.values() if v["ok"] is not None)
    out = {"schema": "method_record_check.v1", "doc": doc.name,
           "doc_sha256": hashlib.sha256(doc.read_bytes()).hexdigest(), "version": ver,
           "bytes": len(doc.read_bytes()), "checks_passed": run - len(failed), "checks_run": run,
           "FAILED": failed, "checks": res, "VERDICT": "PASS" if not failed else "FAIL"}
    return out, failed


TAMPERS = [
    ("marker_table_bidirectional",
     lambda t: t.replace("(§12, new in v6)", "(§12)").replace("(§10, new in v6)", "(§10)")),
    ("superseded_digest_true",
     lambda t: re.sub(r"(sha256\s*\n?`)([0-9a-f])", lambda m: m.group(1) + ("b" if m.group(2) == "a" else "a"), t,
                      count=1)),
    ("obligations_contiguous_and_complete",
     lambda t: re.sub(r"(?m)^13\. \*\*Keep the generator.*?(?=\n\n)", "", t, count=1, flags=re.S)),
    ("lens_floor_intact", lambda t: t.replace(BAN, "review is a matter of taste")),
    ("change_table_names_real_sections",
     lambda t: t.replace("**§16 gains obligations 12 and 13.**", "**§27 gains obligations 12 and 13.**")),
    ("no_placeholders", lambda t: t.replace("## 14. Anti-patterns", "TODO: finish this\n\n## 14. Anti-patterns")),
]


def selftest(doc):
    clean, failed = report(doc)
    ok = not failed
    print("clean document: %s (%d/%d)%s" % (clean["VERDICT"], clean["checks_passed"], clean["checks_run"],
                                            "" if ok else "  FAILED=%s" % failed))
    text = doc.read_text(encoding="utf-8")
    tmp = Path(tempfile.mkdtemp(prefix="methodcheck_"))
    for want, fn in TAMPERS:
        t = fn(text)
        if t == text:
            print("  %-40s TAMPER DID NOT APPLY" % want)
            ok = False
            continue
        p = tmp / "tamper.md"
        p.write_text(t, encoding="utf-8")
        _, got = report(p)
        hit = want in got
        ok = ok and hit
        print("  %-40s %s  (failed: %s)" % (want, "CAUGHT" if hit else "MISSED", ",".join(got) or "none"))
        p.unlink()
    tmp.rmdir()
    print("SELFTEST: %s" % ("PASS - the clean document passes and every tampering is caught" if ok else "FAIL"))
    return ok


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    doc = Path(args[0]) if args else DEFAULT_DOC
    if not doc.exists():
        sys.exit("FAIL: %s does not exist" % doc)
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest(doc) else 1)
    out, failed = report(doc)
    m = re.search(r"\.v(\d+)\.md$", doc.name)
    rec = doc.parent / ("method_record_check.v%s.json" % (m.group(1) if m else "adhoc"))
    rec.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("doc", "doc_sha256", "bytes", "checks_passed", "checks_run", "FAILED",
                                          "VERDICT")}, indent=1))
    for k, v in out["checks"].items():
        print("  %-42s %s  %s" % (k, {True: "PASS", False: "FAIL", None: "SKIP"}[v["ok"]], v["detail"][:110]))
    print("record: %s" % rec.name)
    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
