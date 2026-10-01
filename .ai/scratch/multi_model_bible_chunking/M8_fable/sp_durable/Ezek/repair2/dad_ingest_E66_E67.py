#!/usr/bin/env python3
"""Route the M8 error-ledger delta E-66..E-67 into the DAD lesson intake.

Built by gen_dad_ingest_E66_E67.py from dad_ingest_E59_E65.py: same logic, new records and identifiers.

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
OUT = Path(__file__).with_name("dad_ingest_E66_E67.result.json")
SCAN_JSON = Path(__file__).with_name("dad_ingest_E66_E67.scan.json")
TASK = ("Route M8_fable error-ledger delta E-66..E-67 from ERROR_PATTERN_LEDGER.v1.md into the "
        "DAD lesson graph keyed to content per E-51")
AGENT = "claude-code M8 orchestrator"
MODEL = "claude-opus-5-5"

# (entry id, exact heading prefix)
HEADINGS = {
    **{f"E-{n}": f"## E-{n} (" for n in range(66, 68)},
}

NA = "DOES NOT APPLY"
R = []  # records


def rec(kind, entries, tag, slug, tail, lessons, instance, tier, why):
    R.append(dict(kind=kind, entries=entries, tag=tag, slug=slug, tail=tail, lessons=lessons,
                  instance=instance, tier=tier, why=why))


rec("E", ["E-66"], "E-66", "an_audit_that_derives_its_input_set_by_pairing_must_list_every_file_it_did_not_pair",
    "a token-transform audit paired ported files by same name so it skipped a renamed port in silence and audited "
    "an authored file as a port",
    ["The audit's input set was implicit: the Daniel files that have a same-name source. The rename map lived only in "
     "a lane's scratch. The silent skip merged two states - a file that is not a port and a port under a new name - so "
     "a clean result meant only nothing in the set it looked at. This is E-65's shape again",
     "State an audit's input set explicitly: pair by name and failing that by the adapter's filename token transform "
     "and report each row's source and pairing basis. Declare every authored file with its reason and never align it. "
     "List every remaining unpaired file so an absence is visible and not silent",
     "A clean report over an incomplete set is a half-truth (OW-18) and a renamed port is where a transform rewrites "
     "the most",
     "A guard for a class of leaked predecessor figures states its blind spots: a whole-token search for integers of "
     "100 or more cannot see a smaller figure or a figure true for both books or a non-integer - so the review-lane "
     "control stands beside it unchanged",
     "A review script that reads Hebrew imports the book library's skeleton function and never hand-rolls a strip: "
     "putting a space in place of each mark split every word into letters",
     "APPLIES to any audit or census whose input set is derived by pairing or matching files rather than enumerated. "
     "DOES NOT APPLY where the input set is an explicit enumerated list that is itself checked for completeness",
     "DANGER IF STRIPPED: a renamed port escapes the only control for history rewritten by the book-token transform "
     "and the audit still reports clean"],
    ["the renamed port _test_zone_tools_dan.py went unaudited: 148 source-token lines and 16 lines pairing a Daniel "
     "token with a lineage word",
     "at the fix all 16 unread lines were read and each is true lineage - observed impact nil",
     "after the cure the audit covers 20 files with 416 source-token lines (414 changed and 2 kept verbatim) and 23 "
     "Daniel lines naming the source book and 31 lineage-signature lines",
     "a compaction summary had framed a later-created data file as an omission of an earlier entry and a fresh read "
     "of the file times corrected it before anything was written - E-59's rule working",
     "the Hebrew misread was seen in output and corrected before any record used it and the corrected strip equals "
     "the library skeleton on all 357 verses with 0 differences"],
    "MEASURED", "the ledger entry records a before and after run of the audit with a row diff and a measured equality "
    "of the corrected strip against the library skeleton")

rec("E", ["E-67"], "E-67", "a_gate_is_not_a_pure_reader_read_its_write_sites_and_rerun_it_after_placing_a_file",
    "a smoke run on another book's brief wrote a Daniel-named report into durable state and a recorded GREEN went "
    "stale when a file was placed into the directory the gate scans",
    ["Both slips treated a gate as a pure reader of its own inputs. The brief check wrote its report to a fixed path "
     "beside itself whatever brief it was given. A gate that scans a directory gives a verdict about that directory's "
     "state when it runs - placing a file changes the state and the verdict expires",
     "Before smoke-running a tool in durable state read its write sites. Run tools on foreign inputs only from scratch "
     "copies. Re-run every gate that scans a directory after placing a file into it",
     "Tie a tool's durable write target to its input: write the durable report only for an input inside the tool's "
     "own book and for any other input print the verdict and write nothing. A selftest proves that a foreign passing "
     "input and a foreign failing input and a missing input each leave the report byte-for-byte unchanged",
     "When a recorded pass expires correct the carrier by amendment: a stale GREEN is a half-truth (OW-18) that a "
     "resume could launch review lanes against",
     "This is E-64's family: acting on an unread assumption about a tool",
     "APPLIES to any smoke run or gate run in a durable directory and to any recorded verdict of a gate that scans a "
     "directory. DOES NOT APPLY to a run whose write sites were read in the same session on scratch copies of its "
     "inputs",
     "DANGER IF STRIPPED: once a real brief exists the same smoke run overwrites the book's own PASS or FAIL record "
     "with another book's verdict under the book's own filename"],
    ["the stray report was moved to scratch evidence under a pinned digest before anything used it and no Daniel "
     "authoring brief existed so no real report was overwritten",
     "the selfcheck pre-image executed against the current tree gave 155/157 RED on two checks while the carrier "
     "still claimed GREEN",
     "after the cure and after the toolkit file was placed every gate that scans the tree was re-run: selfcheck "
     "232/232 full scope and 157/157 artifacts-only GREEN",
     "a write-site audit of every Daniel tool found 10 files that write and no other tool writes a fixed durable "
     "path from a foreign input"],
    "MEASURED", "the ledger entry records the pre-image run against the current tree and the post-cure runs and a "
    "write-site audit of every Daniel tool")


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

    new_ids = [f"E-{n}" for n in range(66, 68)]
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
    result = dict(date="2026-09-28", ledger=str(MD), ledger_sha256_pinned=sha, ledger_sha256_after=sha_after,
                  lessons_root=str(root), files_before=files_before, files_after=post["files_scanned"],
                  next_marker_after=post["next_marker"], markers=markers, problems=problems,
                  records=[{k: w[k] for k in ("tag", "slug", "marker", "lesson_id", "file")} for w in written])
    OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"written {len(written)} | files {files_before} -> {post['files_scanned']} | markers {markers} | "
          f"next free {post['next_marker']} | ledger pinned {sha[:16]} after {sha_after[:16]} | "
          f"problems {problems or 'none'}")


if __name__ == "__main__":
    main()
