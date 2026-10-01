#!/usr/bin/env python3
"""Route the M8 error-ledger delta E-68 into the DAD lesson intake.

Built by gen_dad_ingest_E68.py from dad_ingest_E66_E67.py: same logic, new records and identifiers.

Keyed to CONTENT, per E-51: every record names its source entry ids, the markdown ledger's sha256 pinned at WRITE
time, and a sha256 of each entry's own text. The JSONL ledger is dead at E-43 and is never read here.

Order of operations (each step refuses rather than proceeding on a doubt):
  1. locate every source entry by its exact heading - each must occur exactly once
  2. ONE scan of the live tree: every new slug and new id must be absent - and the next free C marker is taken
     from that same scan
  3. re-pin the ledger sha immediately before the first write - abort if it moved since step 1
  4. write through the DAD venv python (no cmd.exe shim - it would re-parse | and %) - after the FIRST write
     assert exactly one new file appeared in the scanned root - so a mis-resolved hub stops at one record
  5. read back every new file and compare lessons and evidence to what was sent - then re-scan
Text items must not contain , ; or newline because DAD's split_multi splits list items on them.
"""
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
MD = M8 / "ERROR_PATTERN_LEDGER.v1.md"
MD_REL = r".ai\scratch\multi_model_bible_chunking\M8_fable\ERROR_PATTERN_LEDGER.v1.md"
REPO = r"C:\wt\logos-t423-m8-fable"
SCAN = r"C:\Users\lowel\.dad\bin\dad_lessons_scan.py"
PY = r"C:\Users\lowel\OneDrive\Desktop\Git Projects\04_Digital_Assett_Directory\.venv\Scripts\python.exe"
OUT = Path(__file__).with_name("dad_ingest_E68.result.json")
SCAN_JSON = Path(__file__).with_name("dad_ingest_E68.scan.json")
TASK = ("Route M8_fable error-ledger delta E-68 from ERROR_PATTERN_LEDGER.v1.md into the "
        "DAD lesson graph keyed to content per E-51")
AGENT = "claude-code M8 orchestrator"
MODEL = "claude-opus-5-5"

# (entry id, exact heading prefix)
HEADINGS = {
    **{f"E-{n}": f"## E-{n} (" for n in range(68, 69)},
}

NA = "DOES NOT APPLY"
R = []  # records


def rec(kind, entries, tag, slug, tail, lessons, instance, tier, why):
    R.append(dict(kind=kind, entries=entries, tag=tag, slug=slug, tail=tail, lessons=lessons,
                  instance=instance, tier=tier, why=why))


rec("E", ["E-68"], "E-68", "a_validator_suite_fails_closed_and_a_toolkit_is_read_against_its_tools_code",
    "a validator suite could report GREEN with a HARD member dead and a toolkit stated its tools' contracts more "
    "strongly than their code",
    ["Each HARD member's predicate was written as that member's own failure status one member at a time so a member "
     "that crashed or printed no JSON object became ERROR and counted as nothing unless it was one of three named "
     "members. A crash in the member that refuses fabricated references could sit under a GREEN verdict",
     "The suite parsed the review normalizer's whole stdout as one object while the normalizer prints one JSON line per "
     "input file - so any review file made the member ERROR and the option was a false RED every time. No fixture ran "
     "the suite with more than one input",
     "The toolkit's tool table was written from docstrings and stated intent rather than read clause by clause against "
     "the code: it omitted three write sites and put a hard-errors heading over two FLAGS tools and said enforces where "
     "a selfcheck runs only a floor. Only the review lane that read the code could see it",
     "Rule: a suite fails closed. A member that produced no evidence is a HARD failure whatever its tier and is listed "
     "by name. A toolkit's account of a tool is read against the tool's code - write sites first - before it is pinned",
     "A toolkit that restates an owner directive quotes the owner's words and labels the orchestrator's reading of them "
     "as INFERRED",
     "This is E-64's and E-67's family: acting on an unread assumption about a tool",
     "APPLIES to any validator suite that aggregates member verdicts and to any toolkit or contract document that "
     "describes tools a lane will trust. DOES NOT APPLY to the suites of closed books which keep the old predicate and "
     "are not reopened for this",
     "DANGER IF STRIPPED: a crashed reference-refusal member under a GREEN verdict lets fabricated citations pass the "
     "HARD gate and a lane trusting an overstated contract under-checks exactly where the contract overstates"],
    ["of 115 suite reports under the campaign none reports GREEN while any member is ERROR - observed harm nil",
     "7 of the 8 suite files in the campaign lack a dead-member rule by a text search whose predicates were not read "
     "one by one - so the exposure is INFERRED to be campaign-wide",
     "the code-reading review lane found 13 defects and each was confirmed against the cited lines before any "
     "correction - the byte-reading lane found none",
     "the amended suite passed a 4-case regression run in a scratch copy with the other members stubbed: dead members "
     "turn RED and a two-file normalizer run turns GREEN",
     "the corrected toolkit passed its selfcheck in full and in artifacts-only scope and both zone fixture tests exit 0"],
    "MEASURED", "the ledger entry records the confirmed defects and the before and after regression runs and the "
    "selfcheck results - the campaign-wide exposure is labelled INFERRED in the entry")


SPLIT = re.compile(r"[,;\n]")


def fail(msg):
    raise SystemExit("REFUSED: " + msg)


def locate(lines):
    out = {}
    for key, prefix in HEADINGS.items():
        hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
        if len(hits) != 1:
            fail(f"heading {prefix!r} matched {len(hits)} times")
        a = hits[0]
        b = next((j for j in range(a + 1, len(lines)) if lines[j].startswith("## ")), len(lines))
        while b > a + 1 and not lines[b - 1].strip():
            b -= 1
        text = "\n".join(lines[a:b])
        out[key] = (a + 1, b, hashlib.sha256(text.encode("utf-8")).hexdigest()[:16])
    return out


def scan(terms, next_marker=True):
    args = [sys.executable, SCAN]
    for t in terms:
        args += ["--grep", t]
    if next_marker:
        args += ["--next-marker", "C"]
    args += ["--json", str(SCAN_JSON)]
    subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return json.loads(SCAN_JSON.read_text(encoding="utf-8"))


def main():
    for r in R:
        for item in [r["tail"], r["slug"], *r["lessons"], *r["instance"], r["why"]]:
            if SPLIT.search(item):
                fail(f"{r['tag']}: text contains , ; or newline -> {item[:70]!r}")
        if not any(NA in x for x in r["lessons"]):
            fail(f"{r['tag']}: no DOES NOT APPLY line")
    b0 = MD.read_bytes()
    sha0 = hashlib.sha256(b0).hexdigest()
    loc = locate(b0.decode("utf-8").split("\n"))

    new_ids = [f"E-{n}" for n in range(68, 69)]
    s = scan([r["slug"] for r in R] + new_ids)
    taken = {t: v for t, v in s["hits"].items() if v}
    if taken:
        fail(f"already in the live tree: {sorted(taken)}")
    root = Path(s["lessons_root"])
    base = int(s["next_marker"].split("-")[1])
    markers = {}
    for r in R:
        if r["kind"] == "C":
            markers[r["slug"]] = f"C-{base:02d}"
            base += 1
    files_before = s["files_scanned"]

    b1 = MD.read_bytes()
    sha = hashlib.sha256(b1).hexdigest()
    if sha != sha0:
        fail("the ledger changed between locate and write - re-run")
    before = set(glob.glob(str(root / "*" / "*.json")))
    written = []
    for n, r in enumerate(R):
        if r["kind"] == "E":
            summary = f"M8_fable error pattern {r['slug']} [{r['tag']}]: {r['tail']}"
        else:
            summary = f"M8_fable campaign control {markers[r['slug']]} {r['slug']} [{r['tag']}]: {r['tail']}"
        spans = " and ".join(f"{loc[e][0]}-{loc[e][1]}" for e in r["entries"])
        evidence = [f"source repo logos-t423-m8-fable | file {MD_REL} | ledger sha256 {sha[:16]} pinned at write "
                    f"time | lines {spans}"]
        evidence += [f"content key {e} entry sha256 {loc[e][2]}" for e in r["entries"]]
        evidence += [f"confidence basis OW-18 evidence tier {r['tier']} - {r['why']}"] + r["instance"]
        args = [PY, "-m", "digital_asset_directory.cli", "lesson", "add", "--repo", REPO, "--summary", summary,
                "--task", TASK, "--agent", AGENT, "--model", MODEL, "--file", MD_REL, "--confidence", "high"]
        for x in r["lessons"]:
            args += ["--lesson", x]
        for x in evidence:
            args += ["--evidence", x]
        p = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if p.returncode != 0:
            fail(f"lesson add exit {p.returncode} on {r['tag']} after {len(written)} writes: {p.stderr[-300:]}")
        now = set(glob.glob(str(root / "*" / "*.json")))
        fresh = sorted(now - before - {w["file"] for w in written})
        if len(fresh) != 1:
            fail(f"{r['tag']}: expected 1 new file in {root}, saw {len(fresh)} after {len(written)} writes")
        written.append(dict(tag=r["tag"], slug=r["slug"], marker=markers.get(r["slug"]), file=fresh[0],
                            summary=summary, lessons=r["lessons"], evidence=evidence))

    problems = []
    for w in written:
        d = json.loads(Path(w["file"]).read_text(encoding="utf-8"))
        w["lesson_id"] = d.get("lesson_id")
        if d.get("summary") != w["summary"]:
            problems.append(f"{w['tag']} summary")
        if d.get("lessons") != w["lessons"]:
            problems.append(f"{w['tag']} lessons {len(d.get('lessons') or [])}/{len(w['lessons'])}")
        if d.get("evidence") != w["evidence"]:
            problems.append(f"{w['tag']} evidence {len(d.get('evidence') or [])}/{len(w['evidence'])}")
        if d.get("review_status") != "candidate":
            problems.append(f"{w['tag']} review_status {d.get('review_status')}")
    post = scan([r["slug"] for r in R] + list(markers.values()), next_marker=True)
    for t, v in post["hits"].items():
        if len(v) != 1:
            problems.append(f"post-scan {t}: {len(v)} hits")
    sha_after = hashlib.sha256(MD.read_bytes()).hexdigest()
    result = dict(date="2026-09-29", ledger=str(MD), ledger_sha256_pinned=sha, ledger_sha256_after=sha_after,
                  lessons_root=str(root), files_before=files_before, files_after=post["files_scanned"],
                  next_marker_after=post["next_marker"], markers=markers, problems=problems,
                  records=[{k: w[k] for k in ("tag", "slug", "marker", "lesson_id", "file")} for w in written])
    OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"written {len(written)} | files {files_before} -> {post['files_scanned']} | markers {markers} | "
          f"next free {post['next_marker']} | ledger pinned {sha[:16]} after {sha_after[:16]} | "
          f"problems {problems or 'none'}")


if __name__ == "__main__":
    main()
