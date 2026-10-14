"""Line-ending guard for recorded digests (E-73).

Git stores this tree's text files with LF (`* text=auto eol=lf`). A file written with CRLF keeps its CRLF bytes in
the working tree only until git next rewrites it (any ref switch); after that the bytes are LF and every sha256
recorded on the CRLF bytes stops matching. A clone never has the CRLF bytes at all. So a digest is only durable if
it was taken on LF bytes.

usage:
  _eol_digest_audit.py --selftest
  _eol_digest_audit.py --check PATH [PATH ...]   exit 1 if any PATH holds CRLF. Run BEFORE recording its digest.
  _eol_digest_audit.py --tree                    exit 1 if any text file in the campaign tree holds CRLF.
  _eol_digest_audit.py --recorded [--emit FILE]  classify every recorded (path, sha256) pair against current bytes;
                                                 --emit writes one correction row per CRLF_ONLY pair (never
                                                 overwrites FILE).
Classes: RAW recorded == bytes on disk. CRLF_ONLY recorded == CRLF form of the bytes on disk (the file was CRLF
when the digest was taken and is LF now; content is otherwise byte-identical, which the match proves).
LF_ONLY recorded == LF form and the disk is CRLF. NONE no form matches (a later amended file, or unknown).
This tool reads; only --emit writes, and only its own FILE.
"""
import datetime, hashlib, json, subprocess, sys, tempfile
from collections import Counter
from pathlib import Path

M8 = Path(__file__).resolve().parents[2] if Path(__file__).resolve().parent.name == "campaign" else None
SKIP = {"transcripts", "orchestrator_scratch", "shell_outputs", "__pycache__", "greek_substrate", ".git"}
SCHEMA = "m8_eol_digest_correction.v1"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def is_binary(b):
    return b"\0" in b[:8000]


def has_crlf(b):
    return (not is_binary(b)) and b"\r\n" in b


def forms(b):
    lf = b.replace(b"\r\n", b"\n")
    return sha(b), sha(lf), sha(lf.replace(b"\n", b"\r\n"))


def classify(recorded, b):
    raw, lf, crlf = forms(b)
    if recorded == raw:
        return "RAW"
    if recorded == crlf:
        return "CRLF_ONLY"
    if recorded == lf:
        return "LF_ONLY"
    return "NONE"


def pairs(o):
    if isinstance(o, dict):
        for pk in ("path", "installed_path", "file"):
            p = o.get(pk)
            if isinstance(p, str):
                for k, v in o.items():
                    if isinstance(v, str) and len(v) == 64 and "sha" in k.lower():
                        yield p, v, k
        for v in o.values():
            yield from pairs(v)
    elif isinstance(o, list):
        for v in o:
            yield from pairs(v)


def resolve(m8, p):
    sp = m8 / "sp_durable"
    q = p.replace("\\", "/")
    for marker, base in (("sp_durable/", sp), ("M8_fable/", m8)):
        if marker in q:
            return base / q.split(marker, 1)[1]
    if q.startswith("SP/"):
        return sp / q[3:]
    for base in (sp, m8):
        if "/" in q and (base / q).is_file():
            return base / q
    return None


def tree_files(m8):
    for f in sorted(m8.rglob("*")):
        if f.is_file() and not (SKIP & set(f.relative_to(m8).parts)):
            yield f


def cmd_check(paths):
    bad = [p for p in paths if has_crlf(Path(p).read_bytes())]
    print(json.dumps({"checked": len(paths), "crlf": bad, "verdict": "LF_CLEAN" if not bad else "CRLF_PRESENT"}))
    return 1 if bad else 0


def cmd_tree(m8):
    bad = [f.relative_to(m8).as_posix() for f in tree_files(m8) if has_crlf(f.read_bytes())]
    print(json.dumps({"crlf_files": len(bad), "first": bad[:15], "verdict": "LF_CLEAN" if not bad else "CRLF_PRESENT"}))
    return 1 if bad else 0


def cmd_recorded(m8, emit):
    found = []
    unparsed = 0
    for f in tree_files(m8):
        if f.suffix not in (".json", ".jsonl") or ".pre_" in f.name or f.stat().st_size > 6_000_000:
            continue
        try:
            text = f.read_text(encoding="utf-8")
            docs = [json.loads(x) for x in text.splitlines() if x.strip()] if f.suffix == ".jsonl" else [json.loads(text)]
        except Exception:  # noqa: BLE001
            unparsed += 1
            continue
        for i, d in enumerate(docs, 1):
            for p, dig, key in pairs(d):
                t = resolve(m8, p)
                if t is not None:
                    found.append((t, key, dig, f, i))
    cache, cls, out = {}, Counter(), []
    for t, key, dig, src, row in found:
        if not t.is_file():
            cls["ABSENT"] += 1
            continue
        b = cache.setdefault(t, t.read_bytes())
        c = classify(dig, b)
        cls[c] += 1
        if c == "CRLF_ONLY":
            out.append({"schema": SCHEMA, "path": t.resolve().relative_to(m8).as_posix(), "digest_key": key,
                        "recorded_sha256": dig, "canonical_lf_sha256": sha(b),
                        "proof": "sha256 of the CRLF form of the current LF bytes equals recorded_sha256 (MEASURED)",
                        "recorded_in": src.relative_to(m8).as_posix(), "recorded_in_row": row})
    summary = {"record_files_unparsed": unparsed, "pairs": len(found), "classes": dict(cls),
               "crlf_only_files": len({r["path"] for r in out})}
    if emit:
        e = Path(emit)
        if e.exists():
            print(json.dumps({"verdict": "REFUSED", "why": "emit file exists; never overwrite"}))
            return 2
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with open(e, "w", encoding="utf-8", newline="\n") as fh:
            for r in out:
                r["measured_at"] = now
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        summary["emitted"] = len(out)
        summary["emit_sha256"] = sha(e.read_bytes())
    print(json.dumps(summary))
    return 0


def selftest():
    fails = []
    lf_b, crlf_b = b"a\nb\n", b"a\r\nb\r\n"
    for rec, b, want in ((sha(lf_b), lf_b, "RAW"), (sha(crlf_b), lf_b, "CRLF_ONLY"), (sha(lf_b), crlf_b, "LF_ONLY"),
                         (sha(b"x"), lf_b, "NONE"), (sha(crlf_b), crlf_b, "RAW")):
        got = classify(rec, b)
        if got != want:
            fails.append(f"classify want {want} got {got}")
    if has_crlf(lf_b) or not has_crlf(crlf_b) or has_crlf(b"\0\r\n"):
        fails.append("has_crlf")
    # The real failure, reproduced: a ref switch rewrites a committed CRLF file as LF and leaves an LF file alone.
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        r = Path(td)

        def git(*a):
            return subprocess.run(["git", "-C", str(r), *a], capture_output=True, text=True)

        if git("init", "-q").returncode != 0:
            fails.append("git init failed: the round-trip test did not run")
        else:
            for k, v in (("user.name", "t"), ("user.email", "t@example.invalid"), ("core.autocrlf", "true"),
                         ("commit.gpgsign", "false")):
                git("config", k, v)
            (r / ".gitattributes").write_bytes(b"* text=auto eol=lf\n")
            git("add", ".gitattributes")
            git("commit", "-q", "-m", "base")
            git("branch", "base")
            (r / "lf.txt").write_bytes(lf_b)
            (r / "crlf.txt").write_bytes(crlf_b)
            before = {n: sha((r / n).read_bytes()) for n in ("lf.txt", "crlf.txt")}
            if cmd_check_quiet([r / "lf.txt"]) or not cmd_check_quiet([r / "crlf.txt"]):
                fails.append("--check did not separate the LF file from the CRLF file")
            git("add", "lf.txt", "crlf.txt")
            git("commit", "-q", "-m", "evidence")
            head = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
            git("checkout", "-q", "base")
            git("checkout", "-q", head)
            if not (r / "lf.txt").is_file() or not (r / "crlf.txt").is_file():
                fails.append("round trip did not restore the files")
            else:
                after = {n: (r / n).read_bytes() for n in ("lf.txt", "crlf.txt")}
                if sha(after["lf.txt"]) != before["lf.txt"]:
                    fails.append("an LF file changed across the ref switch")
                if sha(after["crlf.txt"]) == before["crlf.txt"]:
                    fails.append("the CRLF file survived the ref switch: the hazard is not reproduced here")
                if classify(before["crlf.txt"], after["crlf.txt"]) != "CRLF_ONLY":
                    fails.append("the rewritten CRLF file is not classed CRLF_ONLY against its recorded digest")
    print(json.dumps({"selftest": "PASS" if not fails else "FAIL", "failures": fails}))
    return 1 if fails else 0


def cmd_check_quiet(paths):
    return [p for p in paths if has_crlf(Path(p).read_bytes())]


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--check" in argv:
        return cmd_check(argv[argv.index("--check") + 1:])
    if M8 is None or not (M8 / "sp_durable").is_dir():
        print(json.dumps({"verdict": "REFUSED", "why": "run the installed copy in sp_durable/campaign"}))
        return 2
    if "--tree" in argv:
        return cmd_tree(M8)
    if "--recorded" in argv:
        return cmd_recorded(M8, argv[argv.index("--emit") + 1] if "--emit" in argv else None)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
