#!/usr/bin/env python3
"""Route the M8 error-ledger delta E-59..E-65 into the DAD lesson intake.

Built by gen_dad_ingest_E59_E65.py from dad_ingest_E52_E58.py: same logic, new records and identifiers.

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
OUT = Path(__file__).with_name("dad_ingest_E59_E65.result.json")
SCAN_JSON = Path(__file__).with_name("dad_ingest_E59_E65.scan.json")
TASK = ("Route M8_fable error-ledger delta E-59..E-65 from ERROR_PATTERN_LEDGER.v1.md into the "
        "DAD lesson graph keyed to content per E-51")
AGENT = "claude-code M8 orchestrator"
MODEL = "claude-opus-5-5"

# (entry id, exact heading prefix)
HEADINGS = {
    **{f"E-{n}": f"## E-{n} (" for n in range(59, 66)},
}

NA = "DOES NOT APPLY"
R = []  # records


def rec(kind, entries, tag, slug, tail, lessons, instance, tier, why):
    R.append(dict(kind=kind, entries=entries, tag=tag, slug=slug, tail=tail, lessons=lessons,
                  instance=instance, tier=tier, why=why))


rec("E", ["E-59"], "E-59", "durable_records_are_drafted_from_a_fresh_source_read_never_from_a_compaction_summary",
    "records drafted from a compaction summary carried three clauses the source ledger does not say",
    ["A compaction summary is a lossy carrier: drafting durable records from it lets plausible generalisations that "
     "sound like the source stand in for the source. Three drafted clauses were unsupported - a rule the source never "
     "states - an owner request for token efficiency restated as a specific procedure the owner never gave - and a "
     "record that left out a fact and overstated a claim about what was written",
     "Draft every record bound for a durable store from a fresh read of its source range or check it clause by clause "
     "against one before the write. Check every figure by extraction",
     "No tool can check that a paraphrase is supported so this control is procedural: it is recorded so that the "
     "next ingest harness brief carries it",
     "APPLIES to any record written after a context compaction or handoff to a shared store that later sessions read "
     "as evidence. DOES NOT APPLY to transient working notes that no one reads as evidence",
     "DANGER IF STRIPPED: the writer's paraphrase enters the store labelled as transcribed or measured content - the "
     "half-truth that later sessions then cite as evidence"],
    ["all three clauses were cut or corrected before the write and every figure in the drafts held against the "
     "ledger text", "the control that caught it was a deliberate re-read and not a gate"],
    "TRANSCRIBED", "the ledger entry records a clause-by-clause re-read of the drafts against their source range")

rec("E", ["E-60"], "E-60", "uniqueness_is_proved_in_the_store_being_written_and_a_red_postvalidation_restores_the_preimage",
    "an amendment addressed receipts by a unique execution id but keyed pointer-map entries on an attempt id that "
    "retries share so two edit pairs collided and the shared patch tool left its red write on disk",
    ["Two stores carried two identities. The address check proved uniqueness in the store with the unique key and "
     "assumed it in the other. Both checks in each colliding pair passed because both were written against the same "
     "absent value - so the second edit silently overwrote the first",
     "A shared patch tool refuses before any write a plan that addresses one key more than once. When its own "
     "postvalidation goes red it restores the exact preimage only if the file is still exactly what it wrote and "
     "otherwise skips the rollback and says so",
     "Key execution n above one as the attempt id plus an execution suffix and have the amendment itself refuse "
     "duplicate keys. Prove the tool fix with a regression test that passes on the fixed tool and fails on the "
     "preimage copy",
     "A map that keeps prior executions in a nested list needs its readers taught to join through that list: a census "
     "that joins only the top-level entry cannot reach those executions through the map",
     "APPLIES to any plan that addresses records in more than one store or through a key that retries or re-runs can "
     "share. DOES NOT APPLY where every store is keyed by the same unique identity",
     "DANGER IF STRIPPED: a colliding plan applied directly leaves the pointer index silently short with only a red "
     "receipt and the audit that reads the index misses the lost executions"],
    ["the calling wrapper's own postvalidation restored all three files in the same run with digests measured equal "
     "to the preimages", "the regression test passes 4 of 4 on the fixed tool and fails 4 of 4 on the preimage copy",
     "map coverage over 231 attempts: 11 are reachable only through the nested prior-execution list"],
    "MEASURED", "the rollback digests and the regression test and the map coverage recorded in the ledger entry")

rec("E", ["E-61"], "E-61", "forward_application_starts_from_the_predecessor_final_artifacts_not_its_stage_script",
    "a stage script copied from the predecessor book lost that book's later amendment and the ported consumer refused",
    ["A unit's setup contract is its staging script plus every amendment applied after it. The amendments live in "
     "repair directories and not in the script - so a copy of the script inherits none of them and nothing compared "
     "the new unit's artifacts with the predecessor's final ones",
     "Forward application starts from the predecessor's final artifacts and not only its stage script. The check is a "
     "two-way top-level key-parity audit of every setup artifact against its predecessor counterpart with each "
     "difference declared",
     "Measure before declaring: the numbering-face declaration is written only after every per-chapter count equals "
     "that face's side of the verse check and the total matches. Its obligation text is copied from the predecessor "
     "at run time and never retyped",
     "A declared exception must also account for readers that are not tools: the first statement that only the "
     "builder touched a field overlooked an author lane that had read it as evidence - so the next unit's authoring "
     "brief must name the replacement evidence",
     "Guard first and then write: two new files were written before the in-flight pin guard ran on them. The guard "
     "returned clear afterwards and the control is the order",
     "APPLIES to any per-unit pipeline where each unit is prepared by porting the previous unit's tools and "
     "artifacts. DOES NOT APPLY to a unit staged by a tool that has already absorbed every amendment",
     "DANGER IF STRIPPED: the new unit silently runs on the predecessor's pre-amendment contract and only a consumer "
     "that happens to assert the amended field will notice"],
    ["the ported consumer refused on its first run before any row of the new book existed",
     "a consumer that assumed a face could have mis-keyed references in offset zones totalling 66 verses on each "
     "face (inferred)"],
    "MEASURED", "the face check and the key-parity audit recorded in the ledger entry")

rec("E", ["E-62"], "E-62", "a_launch_checklist_in_prose_is_not_a_gate_so_a_tool_refuses_a_message_that_lacks_it",
    "an audit of 207 agent launches found 42 carrying none of the required strings because the launch checklist "
    "lived only in prose",
    ["A rule that every launch message carry fixed strings was stated in prose and nothing refused a launch that "
     "lacked it. After compactions messages were composed from a brief-centric shape and the checklist items fell "
     "out (inferred)",
     "Gate the message itself: write it to a file - run a checker that requires every string verbatim plus a brief "
     "line whose file is at its stated digest and a unit inside the owner's exception - launch only on a match with "
     "the file's exact text - and record the message digest in the launch receipt",
     "A fail-closed pre-launch tool that no gate calls is not obeyed: a brief pin check found no table in a "
     "four-column brief and those lanes launched anyway. The launch gate now runs the brief pin check and records any "
     "verdict other than a match as a gap",
     "The gate carries an expiry: once the last unit in the owner's exception completes it refuses every launch until "
     "a new grant is recorded",
     "Check for exact strings and name the limit: a launch that paraphrased the required content lacks the strings "
     "by measurement and lacks the content only by inference",
     "What kept the outcome small was a control: subagents write only outside the worktree and the orchestrator lands "
     "their work - so no subagent wrote state under an exception it could not see",
     "APPLIES to any content that every agent launch must carry. DOES NOT APPLY to content already enforced by a tool "
     "that refuses the launch",
     "DANGER IF STRIPPED: after the next compaction the checklist falls out again and lanes run without the owner's "
     "exception or the research preamble - exposed to stopping and to the content filter"],
    ["161 launches carried all five audited strings inline and 4 in their message file while 42 carried none",
     "the real failing message is refused with 9 gaps and a message naming the four-column brief is refused with the "
     "single gap brief pin check NO_TABLE"],
    "MEASURED", "an exact-string audit of every launch in the orchestrator's own session transcript")

rec("E", ["E-63"], "E-63", "a_new_row_kind_or_field_in_an_append_only_store_is_taught_to_every_reader_through_one_fold",
    "receipts gained amending rows and unit token fields that no reader knew so wrong figures reached the owner and "
    "the pin guard would have landed a running execution on an amendment",
    ["The row vocabulary grew in the writer and nowhere else. Each reader kept a private unstated idea of which rows "
     "and fields exist and nothing refused a row it did not understand. Before adding a field or a row kind find "
     "every reader",
     "Put the reading in one shared fold with a selftest and a parity check against the reader it replaces and make every "
     "reader use it. A reader takes a row's own execution id where the row names one and never derives it from row "
     "order",
     "A release rule names exactly the rows that release: an execution lands only on a row that is not a launch "
     "record and carries an outcome that is non-empty and not running. The older rule that any non-launch row is a "
     "landing became false when amending rows appeared",
     "Scripts that repeat a shared rule import it rather than restate it",
     "Still owed: no reader refuses an unknown token field so a new unit field could still be written that the fold "
     "ignores",
     "APPLIES to any append-only record store read by several independent tools. DOES NOT APPLY to a store whose only "
     "reader changes together with its writer",
     "DANGER IF STRIPPED: status figures count amendments as runs and mix token units - and one routine amendment of "
     "a running lane releases every pin it holds so a file can be regenerated under an agent that is reading it with "
     "nothing to show it happened"],
    ["a status figure of 278 executions folds to 231 once 47 amending rows stop counting as executions",
     "the capture index had indexed four landed runs as first runs because each failed first run's row was "
     "back-filled after its landing row and the run number came from row order",
     "the guard selftest passes 24 of 24 including an outcome-less and a running-outcome amendment that both go red "
     "under the old rule"],
    "TRANSCRIBED", "the ledger transcribes the reader figures from the cycle state where they were measured at the cure")

rec("E", ["E-64"], "E-64", "read_what_a_tool_does_before_acting_on_an_assumption_about_it",
    "three slips acted on an unread assumption about a tool: a check after a failed write - a stop reason typed by a "
    "template - and a bytecode file written into durable state",
    ["In each slip a tool's behaviour was assumed and not read: a lane assumed a parse failure might have written "
     "something - a launch builder assumed every stop was a watchdog stall - and the orchestrator assumed the "
     "no-bytecode flag governs py_compile which writes its output regardless",
     "A relaunch brief reads the prior stop from the prior execution's landing row and refuses when that row is "
     "unlanded or names no known stop class - never a typed default",
     "Syntax checks in durable directories use a parser that writes nothing and never a compiler that writes "
     "bytecode. Scripts that import shared code set the no-bytecode switch before the import",
     "Blind briefs state explicitly that a check after a failed write is still an existence check and that a shell "
     "wildcard is a glob even inside the lane's own output",
     "Template text that is true only for the first run is the same class as a typed stop reason: make every "
     "templated statement true for every run it is built for",
     "APPLIES to any action whose safety depends on a tool's side effects or on a fact about the previous run. DOES "
     "NOT APPLY where that behaviour was read or measured in the same session",
     "DANGER IF STRIPPED: a false stop reason in a relaunch brief is a false durable statement that also "
     "misclassifies the failure in any stop-class census - and an unreceipted file in durable state is swept into "
     "the next digest census or commit"],
    ["both the launched relaunch brief and the set-aside build contain 0 occurrences of watchdog",
     "the builder refuses a relaunch while the prior execution is in flight and refuses one whose prior execution "
     "completed",
     "older bytecode directories in durable state predate the session and are left alone because removing them is a "
     "cleanup act that needs the owner's authority"],
    "MEASURED", "the brief contents and the builder refusals - the two lane slips are reported by the lanes themselves")

rec("E", ["E-65"], "E-65", "residual_zero_means_no_listed_fact_survived_not_that_no_predecessor_fact_survived",
    "a ported tool staged at residual zero would have told every report of the new book to compare its counts with "
    "the predecessor book's shipped figures",
    ["A residual scanner built on a fixed list of known predecessor facts proves only that no listed fact survived. "
     "A bare predecessor figure with no book token passes both it and a token-transform audit - and the behaviour "
     "selftests did not read the text of the emitted note",
     "Emitting a predecessor's true figures as the comparison baseline for another unit is a half-truth: the figures "
     "are true but the text implies they are the right baseline",
     "At landing read the strings the ported tool emits. Any number in an emitted string or note that is not a fact "
     "of the new unit is a review item for the blind toolkit review lanes",
     "Amend at landing without touching the lane's own spec: an orchestrator copy appends exact-once substitutions "
     "whose old strings are read from the staged file and it refuses unless each occurs exactly once",
     "Adding the figures to the fixed list was considered and rejected: it repeats the fixed-list weakness and changes "
     "a tool that another lane reads and runs",
     "APPLIES to any tool ported between units by token substitution and a residual scan. DOES NOT APPLY to a tool "
     "written fresh against the new unit's own data",
     "DANGER IF STRIPPED: every report of the new book steers a reviewer to judge its coverage against another book's "
     "corpus"],
    ["the predecessor's figures appeared in a legacy comment and in the note the tool emits in every report",
     "after the amendment the restage is residual 0 with only that tool differing in 2 hunks and its selftest passes "
     "32 of 32 in place",
     "the remaining predecessor mentions in the installed tools were each read as lineage in a docstring or a ruling "
     "comment and none is emitted"],
    "MEASURED", "the staged file read at landing and the restage and in-place selftest")


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

    new_ids = [f"E-{n}" for n in range(59, 66)]
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
