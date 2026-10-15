#!/usr/bin/env python3
"""Adapt the Daniel toolkit members to 1 Corinthians, deterministically, and record how.

Lineage: Dan/tools/<name> -> 1Cor/tools/<name>, modelled on Dan/tools/_adapt_tools_dan.py (Ezek -> Dan). Two passes,
both exact:
  1. CODE TOKENS. Using Python's tokenizer, every NAME token, non-docstring string token and f-string segment has
     its book token swapped. A Python NAME cannot begin with a digit, so NAMES and STRINGS take different maps:
         NAME:   dan_lib -> cor_lib,  DAN -> COR,   Dan -> Cor
         STRING: dan_lib -> cor_lib,  DAN -> 1COR,  Dan -> 1Cor
     Each swap matches the book token only as a whole token (not inside a longer word: "Daniel" is never turned into
     "1Coriel"; it is left for the residual scan). Docstrings and comments are NOT swapped by this pass, because in
     them the book token usually sits inside a Daniel FACT ("WEB 4:1-3 = MT 3:31-33") that a token swap would turn
     into a false 1 Corinthians claim.
  2. PROSE, FIXTURES AND LOGIC. Per-tool exact-count substitutions (SUBS in _adapt_tools_1cor_spec.py). Each `old`
     must occur exactly the stated number of times in the output so far, or the run refuses.
Then a residual scan lists every line that still carries a Daniel or Ezekiel token, a Daniel-only fact pattern (357
verses, 12 chapters, the numbering-zone refs, OSHB, WLC, the MT face, Aramaic, Qere/Ketiv, the Hebrew paragraph and
paseq apparatus), any Hebrew character, and every 1Cor ref that names no verse on its face (a fixture carried from
Daniel). A line may remain only if it is listed in KEEP with its reason.

Modes:
  --stage DIR   write the adapted files to DIR (a scratch directory), compile them, print the residual report
  --install DIR copy staged files from DIR into 1Cor/tools (this file's own directory); refuses if a residual is
                unresolved, if a target exists and differs, or if the staged file no longer matches a fresh adaptation.
                Written as Daniel's is; it is the orchestrator's mode, never the porting lane's.
Option:
  --extra-spec PATH  adapt ONLY the tools named by that spec file's TOOLS, with its SUBS and KEEP, instead of the
                spec above. The file may also define RENAME {cor_name: dan_name}. A tool the base spec already adapts
                is refused.
Protected (never written by this script): cor_lib.py, TOOLKIT.md, _toolkit_selfcheck.py, _adapt_tools_1cor.py,
_adapt_tools_1cor_spec.py.
"""
from __future__ import annotations

import hashlib
import io
import json
import py_compile
import re
import sys
import tokenize
from pathlib import Path

COR_TOOLS = Path(__file__).resolve().parent
SP = COR_TOOLS.parent.parent
DAN_TOOLS = SP / "Dan" / "tools"
PROTECTED = {"cor_lib.py", "TOOLKIT.md", "_toolkit_selfcheck.py", "_adapt_tools_1cor.py", "_adapt_tools_1cor_spec.py"}
sys.path.insert(0, str(COR_TOOLS))
from _adapt_tools_1cor_spec import KEEP, SUBS, TOOLS  # noqa: E402  {tool: [(old, new, count)]}, {tool: [(substr, why)]}
from cor_lib import LAST_VERSE  # noqa: E402  identity numbering: one verse space serves web:, rp: and sbl:

# every 1Cor ref left in an adapted file must exist (a fixture carried from Daniel may not)
CORREF = re.compile(r"(?<![\w.])(?:(web|rp|sbl|oshb):)?1Cor\.(\d+)\.(\d+)")
HEBREW = re.compile("[֐-׿יִ-ﭏ]")
FACT = re.compile(
    r"(?:(?<![A-Za-z])|(?<=\\b))(?:Daniel|DANIEL|[Dd]an(?![a-z])|DAN(?![A-Z]))"          # Daniel tokens (also after a regex \b)
    r"|[Ee]zek|EZEK"                                                        # the Ezekiel predecessor
    r"|\b357\b|\b12 chapters|\b4:1-3[37]?\b|\b5:31\b|\b6:1-2[89]\b|\b3:3[1-3]\b|\b4:34\b|\b66 verses"
    r"|\b2:4[ab]?\b|\b7:28\b|\b2:4b?-7:28"                                  # Daniel zones and the Aramaic island
    r"|[Aa]ramaic|ARAMAIC|[Oo][Ss][Hh][Bb]|\bWLC\b|\bMT\b"                  # the Hebrew witness and its face
    r"|[Qq]ere\b|[Kk]etiv|\bK/Q\b|[Pp]aseq|[Pp]arashah|[Ss]amekh|[Mm]aqaf|[Cc]onsonant")
_NAME_MAP = [(re.compile(r"dan_lib"), "cor_lib"), (re.compile(r"(?:(?<![A-Za-z])|(?<=\\b))DAN(?![A-Z])"), "COR"),
             (re.compile(r"(?:(?<![A-Za-z])|(?<=\\b))Dan(?![a-z])"), "Cor")]
_STR_MAP = [(re.compile(r"dan_lib"), "cor_lib"), (re.compile(r"(?:(?<![A-Za-z])|(?<=\\b))DAN(?![A-Z])"), "1COR"),
            (re.compile(r"(?:(?<![A-Za-z])|(?<=\\b))Dan(?![a-z])"), "1Cor")]
TOKEN_MAP = {"name": [(p.pattern, n) for p, n in _NAME_MAP], "string": [(p.pattern, n) for p, n in _STR_MAP]}


def swap(s: str, table) -> str:
    for pat, new in table:
        s = pat.sub(new, s)
    return s


def pass1(src: str) -> str:
    lines = src.splitlines(keepends=True)
    edits = []
    prev = None
    fmid = getattr(tokenize, "FSTRING_MIDDLE", -1)
    for t in tokenize.generate_tokens(io.StringIO(src).readline):
        if t.type in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT):
            if t.type == tokenize.NEWLINE:
                prev = t
            continue
        table = None
        if t.type == tokenize.NAME:
            table = _NAME_MAP
        elif t.type == fmid:
            table = _STR_MAP
        elif t.type == tokenize.STRING:
            triple = t.string.lstrip("rbuRBUfF").startswith(('"""', "'''"))
            is_doc = triple and (prev is None or prev.type == tokenize.NEWLINE or prev.string == ":")
            table = None if is_doc else _STR_MAP
        if table is not None:
            (sr, sc), (er, ec) = t.start, t.end
            # the SOURCE slice, not t.string: an f-string middle reports '{{' as '{' in t.string
            if sr == er:
                text = lines[sr - 1][sc:ec]
            else:
                text = lines[sr - 1][sc:] + "".join(lines[sr:er - 1]) + lines[er - 1][:ec]
            new = swap(text, table)
            if new != text:
                edits.append((t.start, t.end, new))
        prev = t
    for (sr, sc), (er, ec), new in reversed(edits):
        if sr != er:
            head, tail = lines[sr - 1][:sc], lines[er - 1][ec:]
            lines[sr - 1:er] = [head + new + tail]
        else:
            lines[sr - 1] = lines[sr - 1][:sc] + new + lines[sr - 1][ec:]
    return "".join(lines)


RENAME: dict[str, str] = {}   # {cor_name: dan_name}; set only by --extra-spec


def load_extra(path: Path) -> None:
    """Replace TOOLS/SUBS/KEEP with an extra spec file's own (see --extra-spec)."""
    global TOOLS, SUBS, KEEP, RENAME
    import importlib.util
    spec = importlib.util.spec_from_file_location("_extra_spec", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    clash = sorted(set(mod.TOOLS) & set(TOOLS))
    if clash:
        raise SystemExit("REFUSED: the base spec already adapts %s" % clash)
    TOOLS, SUBS, KEEP = list(mod.TOOLS), dict(mod.SUBS), dict(getattr(mod, "KEEP", {}))
    RENAME = dict(getattr(mod, "RENAME", {}))


def adapt(name: str) -> tuple[str, list[str]]:
    out = pass1((DAN_TOOLS / RENAME.get(name, name)).read_text(encoding="utf-8"))
    for old, new, count in SUBS.get(name, []):
        n = out.count(old)
        if n != count:
            raise SystemExit("REFUSED %s: %r occurs %d times, spec says %d" % (name, old[:60], n, count))
        out = out.replace(old, new)
    keeps = KEEP.get(name, [])
    residual = []
    for i, line in enumerate(out.splitlines(), 1):
        kept = any(k in line for k, _why in keeps)
        if (FACT.search(line) or HEBREW.search(line)) and not kept:
            residual.append("%s:%d: %s" % (name, i, line.strip()[:150]))
        for m in CORREF.finditer(line):
            c, v = int(m.group(2)), int(m.group(3))
            if v < 1 or v > LAST_VERSE.get(c, 0):
                residual.append("%s:%d: NO SUCH VERSE %s" % (name, i, m.group(0)))
    return out, residual


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 3:
        raise SystemExit("usage: _adapt_tools_1cor.py --stage|--install DIR [--extra-spec PATH]")
    mode, target = sys.argv[1], Path(sys.argv[2])
    if mode not in ("--stage", "--install"):
        raise SystemExit("REFUSED: unknown mode %s" % mode)
    report = {"mode": mode, "token_map": TOKEN_MAP, "tools": {}, "residual": []}
    if len(sys.argv) == 5 and sys.argv[3] == "--extra-spec":
        load_extra(Path(sys.argv[4]))
        report["extra_spec"] = {"path": sys.argv[4],
                                "sha256": hashlib.sha256(Path(sys.argv[4]).read_bytes()).hexdigest()[:16]}
    elif len(sys.argv) != 3:
        raise SystemExit("usage: _adapt_tools_1cor.py --stage|--install DIR [--extra-spec PATH]")
    if mode == "--stage" and target.resolve() in (COR_TOOLS, DAN_TOOLS):
        raise SystemExit("REFUSED: --stage writes to a scratch directory, never a toolkit directory")
    for name in TOOLS:
        if name in PROTECTED:
            raise SystemExit("REFUSED: %s is protected" % name)
        out, residual = adapt(name)
        report["residual"].extend(residual)
        sha = hashlib.sha256(out.encode("utf-8")).hexdigest()
        src = DAN_TOOLS / RENAME.get(name, name)
        report["tools"][name] = {"sha256": sha[:16], "source": src.name,
                                 "source_sha256": hashlib.sha256(src.read_bytes()).hexdigest()[:16]}
        if mode == "--stage":
            target.mkdir(parents=True, exist_ok=True)
            (target / name).write_text(out, encoding="utf-8", newline="\n")
            py_compile.compile(str(target / name), doraise=True)
    if mode == "--install":
        if report["residual"]:
            raise SystemExit("REFUSED: %d unresolved residual lines" % len(report["residual"]))
        for name in TOOLS:
            staged = (target / name).read_text(encoding="utf-8")
            fresh, _ = adapt(name)
            if staged != fresh:
                raise SystemExit("REFUSED: staged %s no longer matches a fresh adaptation" % name)
            dst = COR_TOOLS / name
            if dst.exists() and dst.read_text(encoding="utf-8") != fresh:
                raise SystemExit("REFUSED: %s exists and differs" % dst)
            dst.write_text(fresh, encoding="utf-8", newline="\n")
    report["residual_count"] = len(report["residual"])
    print(json.dumps(report, ensure_ascii=False, indent=0))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
