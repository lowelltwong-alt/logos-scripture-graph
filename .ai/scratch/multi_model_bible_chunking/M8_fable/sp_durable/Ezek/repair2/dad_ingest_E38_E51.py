#!/usr/bin/env python3
"""Route the M8 error-ledger delta E-38..E-51 + OW-21..OW-24 into the DAD lesson intake.

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
OUT = Path(__file__).with_name("dad_ingest_E38_E51.result.json")
SCAN_JSON = Path(__file__).with_name("dad_ingest_E38_E51.scan.json")
TASK = ("Route M8_fable error-ledger delta E-38..E-51 plus OW-21..OW-24 from ERROR_PATTERN_LEDGER.v1.md into the "
        "DAD lesson graph keyed to content per E-51")
AGENT = "claude-code M8 orchestrator"
MODEL = "claude-opus-5-5"

# (entry id, exact heading prefix)
HEADINGS = {
    "E-38": "## E-38 - ", "E-38-addendum": "## E-38 addendum", "OW-21": "## OW-21 - ", "E-39": "## E-39 - ",
    "E-34-addendum": "## E-34 addendum", "E-40": "## E-40 - ", "E-35-addendum": "## E-35 addendum",
    "OW-22": "## OW-22 - ", "E-41": "## E-41 - ", "OW-23": "## OWNER DIRECTIVE OW-23 ",
    "OW-24": "## OWNER DIRECTIVE OW-24 ",
    **{f"E-{n}": f"## E-{n} (" for n in range(42, 52)},
}

NA = "DOES NOT APPLY"
R = []  # records


def rec(kind, entries, tag, slug, tail, lessons, instance, tier, why):
    R.append(dict(kind=kind, entries=entries, tag=tag, slug=slug, tail=tail, lessons=lessons,
                  instance=instance, tier=tier, why=why))


rec("E", ["E-38", "E-38-addendum"], "E-38", "a_census_over_records_cannot_see_work_that_produced_no_record",
    "a spend census summed receipt rows and so could not see attempts that produced no receipt",
    ["A census built by summing records is true only of the records that exist. Ten attempts landed with no receipt "
     "and four receipts declared unavailable a figure the runtime had reported - so about 5.4M tokens were invisible "
     "or unknown and the understated total hid a projected ceiling crossing",
     "Reconcile the record census against the runtime's own event log before any budget statement: the log is the "
     "denominator and the records are the record. A landing is not complete until its receipt exists. A no-blanks "
     "claim names its denominator",
     "Addendum folded in: an audit derived from a census reports an absence as a question with its basis and never "
     "as a finding - a census cannot see the classes it does not count",
     "APPLIES to any budget or completeness figure computed by summing per-attempt records where an attempt can end "
     "without writing one. DOES NOT APPLY where the record is written atomically by the mechanism that performs the "
     "attempt",
     "DANGER IF STRIPPED: a zero-undeclared-blanks report reads as complete coverage when it covers only the rows "
     "that exist"],
    ["census moved from 39.43M to 45.48M once the runtime notifications were reconciled"],
    "MEASURED", "recovered from runtime completion notifications in the session transcript")

rec("E", ["E-34-addendum"], "E-34 addendum", "a_gate_that_runs_a_subset_of_the_suite",
    "an adjudicator iterated a candidate to clean against a gate built from part of the suite and the full suite "
    "then failed it",
    ["Extends the E-34 record ingested 2026-09-16 (an instruction never checked against its gate) one level down: an "
     "agent faithful to its gate still fails the suite when the gate is a subset of the suite",
     "Hand every author or adjudicator gate the WHOLE pinned suite run on the candidate rows as well as the per-row "
     "checks",
     "APPLIES to iterative author or adjudicator loops that converge against a gate before a final suite run. "
     "DOES NOT APPLY where the gate and the final acceptance run are the same executable",
     "DANGER IF STRIPPED: an all-clean gate result is read as suite acceptance"],
    ["the full suite found a citation-sweep disclosure duty the subset gate could not see"],
    "MEASURED", "the full suite run on the adjudicated rows")

rec("E", ["E-35-addendum"], "E-35 addendum", "a_count_carried_as_the_identity_of_a_set",
    "a set referred to only by its size was carried through four documents and no record listed its members",
    ["Extends the E-35 record ingested 2026-09-16 (an inherited count base used as an operand): the eight held items "
     "were carried by count through four documents and no record listed the eight by id",
     "A hold or release or routing names its members by id at the moment it is written. A later builder that must "
     "reconstruct such a set refuses unless independent reconstructions agree",
     "APPLIES to hold lists and exception sets and deferred-item groups handed between steps or sessions. DOES NOT "
     "APPLY to counts that are only reported and never used to select members",
     "DANGER IF STRIPPED: a matching count is taken as proof that the right members were carried"],
    ["the step-6 builder reconstructed the set from two peers' own words and refused unless both counts came to four"],
    "TRANSCRIBED", "from the ledger entry and the builder's refusal rule")

rec("E", ["E-39"], "E-39", "a_failed_execution_with_no_receipt_makes_the_inflight_guard_refuse_forever",
    "an in-flight guard keyed on a missing receipt refused forever after an execution died without one and was "
    "then skipped",
    ["A guard that treats any execution without a receipt as in flight refuses forever once an execution dies "
     "without one. Four executions failed on a runtime watchdog and one never got a receipt - so every later "
     "mutation skipped the guard rather than read its refusal",
     "Write a receipt for every execution the moment it ends - watchdog failures included - and have a relaunch "
     "record the prior execution's outcome in the same step",
     "Read a guard's refusal before anything else. A refusal that names a dead execution is a capture defect to fix "
     "and never a reason to skip the guard. A control that can only refuse is a control that gets skipped",
     "APPLIES to in-flight or lock guards keyed on the absence of a completion record. DOES NOT APPLY to guards with "
     "a lease or timeout that expires by design",
     "DANGER IF STRIPPED: skipping a stuck guard becomes habit and the next refusal that names a live execution is "
     "skipped too"],
    ["no harm came because the executions were dead but three mutation batches ran without the guard"],
    "MEASURED", "transcript map against the receipts file")

rec("E", ["E-40"], "E-40", "a_ruling_that_bars_what_an_earlier_brief_sanctions_leaves_the_brief_pinned_and_contrary",
    "a later ruling barred phrases an earlier brief prescribed while the brief stayed a pinned input",
    ["A ruling barred referents that an earlier brief told authors to use. The brief was never re-versioned and stayed "
     "a pinned input - so a lane reading both found two instructions and the older one was the more specific",
     "A ruling's landing lists every pinned brief whose instruction it contradicts by section. A later brief that "
     "pins the older one states the supersession verbatim. The brief-versus-suite check gains a superseded-phrase arm",
     "APPLIES to layered instruction sets where rulings amend briefs that remain pinned inputs. DOES NOT APPLY when "
     "the amended brief is re-versioned and the old version unpinned",
     "DANGER IF STRIPPED: the more specific older instruction wins in the agent's reading and the ruling is silently "
     "undone"],
    ["found by the orchestrator while building the next brief and before any launch"],
    "MEASURED", "the two pinned documents compared section by section")

rec("E", ["E-41"], "E-41", "a_generator_rerun_rewrote_in_place_a_file_a_running_agent_had_pinned",
    "a widened generator was re-run and overwrote an output that a running agent had pinned by digest",
    ["While an agent ran with a file pinned by digest the orchestrator widened and re-ran the generator that makes "
     "it - and the re-run overwrote the pinned bytes. Seen within minutes and the pinned bytes reproduced exactly",
     "Root cause: the in-flight guard covered record writes but a generator's output was not treated as one and the "
     "generator overwrote its versioned output unconditionally",
     "Generators refuse to overwrite an existing output with different bytes. A changed extraction writes a new "
     "version. Run the in-flight guard on every output path before re-running a generator whose outputs a launch "
     "pinned",
     "APPLIES to any generator whose output is a pinned input of concurrent work. DOES NOT APPLY to scratch outputs "
     "that no launch has pinned",
     "DANGER IF STRIPPED: a digest pin detects the change only if the agent hashes inside the window - otherwise it "
     "works from different bytes than its brief names"],
    ["the pinned bytes were regenerated with a legacy flag and digest-verified and the widened result written as v2"],
    "MEASURED", "digest comparison of the pinned file before and after")

rec("E", ["E-42"], "E-42", "an_extract_that_fell_back_to_the_other_numbering",
    "a lookup fell back to a second numbering scheme's key and cross-mapped annotations where the schemes diverge",
    ["A per-slice extract looked a verse up by its primary key and fell back to a second numbering's key when the "
     "first held nothing. Where the numberings agree the bug is invisible - where they diverge it attached one "
     "verse's annotation to a different verse",
     "Layered review caught it: an adjudicator re-measured the claim against the pinned source and refused to carry "
     "it - two blind lanes had both repeated the wrong annotation",
     "One key only with the reason written at the line. An extract that derives a second numbering carries the "
     "derivation and never a fallback. A verifier re-measures every claim on a divergence-zone row before a merge",
     "APPLIES to lookups across two identifier schemes that coincide on most keys (versification or renumbered ids). "
     "DOES NOT APPLY where the schemes never coincide so a fallback would fail loudly",
     "DANGER IF STRIPPED: a fallback that fires only in the divergence zone passes every test drawn from the agreeing "
     "zone"],
    ["Ezekiel chapters 20-21 where the MT and WEB verse numbering differ"],
    "MEASURED", "adjudicator re-measurement against the pinned marks file")

rec("E", ["E-43"], "E-43", "a_prose_rule_applied_to_a_structured_field",
    "a check written for prose was run on a field of schema tokens and flagged rows with nothing wrong",
    ["A check written to catch schema words used as words in prose was applied to a field whose elements are schema "
     "tokens by construction - and flagged rows that had nothing wrong with them",
     "Scope each check arm to the field class it was written for: exclude it on that field only with a selftest "
     "vector proving the exclusion while every other arm still applies there",
     "APPLIES to lint or register checks run across heterogeneous fields (prose and structured tokens). DOES NOT "
     "APPLY to checks written for and applied to a single field class",
     "DANGER IF STRIPPED: disabling the arm outright instead of scoping it removes the prose protection too"],
    ["the last three register flags in the book were this false positive"],
    "MEASURED", "the flagged rows re-read against the field definition")

rec("E", ["E-44"], "E-44", "a_generator_extended_in_place_destroyed_the_position_it_had_produced",
    "a generator edited from v1 to v2 left its v1 output on disk and no longer reproducible",
    ["A generator was extended from v1 to v2 behaviour by editing the same file. The v2 output passes - the v1 "
     "output on disk is no longer reproducible from anything. A passing check on the new version says nothing about "
     "the old one",
     "An unversioned file name emitting a versioned artifact cannot record which position it holds",
     "Copy a shipped generator aside before extending it and re-issue it as vN+1. Name a generator for the version "
     "it produces. A missing generator is a FAILED check and never a SKIP",
     "APPLIES to generators of retained or cited artifacts whose earlier versions must stay reproducible. DOES NOT "
     "APPLY to throwaway scripts whose outputs are not retained",
     "DANGER IF STRIPPED: the artifact survives but its provenance does not - it can no longer be regenerated or "
     "audited"],
    ["the rule was then applied to itself: the census reader was branched to v3 with v2 bytes and output retained"],
    "MEASURED", "attempted regeneration of the v1 output")

rec("E", ["E-45"], "E-45", "a_check_that_was_run_and_not_retained_is_a_check_that_was_not_run",
    "a correct verification done by hand in chat left nothing to re-run at the next version",
    ["A change table was verified correct by hand in chat. At the next version there was nothing to re-run and no way "
     "to show it had ever been checked - the evidence had the durability of chat",
     "A check whose result is not on disk is a claim and not a check. Retain the checker - bidirectional where the "
     "relation is two-way - with a selftest that proves it catches tampering. A gate never shown failing is not "
     "evidence",
     "APPLIES to verification of any artifact that will be re-versioned or audited. DOES NOT APPLY to exploratory "
     "checks whose result nothing relies on",
     "DANGER IF STRIPPED: a correct but unretained verification is later indistinguishable from one never done"],
    ["the retained checker's selftest catches six tamperings"],
    "MEASURED", "selftest run of the retained checker")

rec("E", ["E-46"], "E-46", "proposer_author_and_orchestrator_collapsed_into_one_voice",
    "under a budget ceiling the orchestrator authored proposals about deliverables it had also written",
    ["Under a budget ceiling the orchestrator wrote the method-change proposals about deliverables it had also "
     "authored - proposer and author and orchestrator in one voice where the rule requires independent adjudication",
     "Disclosure in the file's own bytes and a strongest-reason-to-reject on each proposal kept it from being silent "
     "- but self-disclosed non-independence is still non-independence. Two of the orchestrator's own evidence claims "
     "were false and were caught only by re-measurement",
     "Adjudicate proposals in a SEPARATE execution even when budget is tight. When that cannot happen the close says "
     "the item is owed and not met",
     "APPLIES to any process whose rule requires the adjudicator to be independent of the proposer or author. DOES "
     "NOT APPLY to drafts that nothing adopts without separate review",
     "DANGER IF STRIPPED: budget pressure normalises self-review and disclosure is accepted in place of independence"],
    ["the proposals were not appended to the campaign log - that stays the owner's act after independent review"],
    "MEASURED", "the proposal file's recorded authorship and the re-measured claims")

rec("E", ["E-47"], "E-47", "a_reader_decided_what_a_row_was_by_string_matching_its_schema_name",
    "a census classified rows by a schema-name suffix and invented eighteen attempts from a new correct row type",
    ["A census decided whether a row was an attempt by testing the suffix of its schema name. A new and correct row "
     "type - a note ABOUT an attempt - was read as eighteen fresh attempts with null ids",
     "Key a predicate to the field that carries the meaning (a row carrying amends_execution_id is never itself an "
     "attempt). A predicate keyed to a naming convention fails the moment a new name is correct",
     "Branch the reader to a new version rather than editing it and keep the old reader and its output so the earlier "
     "position stays reproducible",
     "APPLIES to readers that classify heterogeneous rows appended by several writers. DOES NOT APPLY where one "
     "writer owns the schema and a closed enum field names the type",
     "DANGER IF STRIPPED: the data is right and the reader invents defects that are then chased in the data"],
    ["detected and cured within the hour as census v3"],
    "MEASURED", "census v2 against v3 on the same rows")

rec("E", ["E-48"], "E-48", "a_governance_floor_that_depends_on_one_named_model_can_vanish",
    "a two-lane review floor naming one model had no admissible grader once that model could not be dispatched",
    ["The two blind lanes required to grade close-gate items both failed at launch because the one model the "
     "governance names for grading could not be dispatched. The book could not close and orchestration cannot "
     "substitute - a same-family lane grading same-author work counts as one voice",
     "E-48's first diagnosis (a short usage window) was wrong and is superseded by E-49 - the design lesson survives: "
     "a floor that depends on a single named model needs a fallback grader declared IN ADVANCE by the owner rather "
     "than improvised at the gate by the agent the floor exists to check",
     "Receipt a launch-time failure as an attempt rather than retrying it into invisibility - these failures carried "
     "no usage block and zero-byte outputs so their spend is unrecoverable and not zero. Never report a floor as met "
     "by a lane that did not run",
     "APPLIES to review or approval floors that name one specific model or provider or person. DOES NOT APPLY where "
     "the floor names a capability class with more than one admissible provider already declared",
     "DANGER IF STRIPPED: the gap is filled under pressure by whichever reviewer is reachable - usually the author's "
     "own family"],
    ["the close tool asserts the grading model by name so the dependency is compiled into the pipeline"],
    "MEASURED", "five refused dispatches with receipts and the close tool's own assertions")

rec("E", ["E-49"], "E-49", "the_first_measurable_cause_was_adopted_without_testing_it",
    "a usage window measured beside a failure was adopted as its cause and one cheap probe would have refuted it",
    ["A usage window measured at 95 percent beside a failure was adopted as its cause. After the window reset to 6 "
     "percent the identical failure recurred - a cause that holds in both states is not the cause",
     "A one-line dispatch with no brief and no tools failed identically - removing brief size and context and tool "
     "budget and both usage windows in one probe. Four of five dispatches had gone on a hypothesis that one cheap "
     "probe would have refuted first",
     "A measurement taken next to a failure is not a test of its cause. Before retrying a failure whose cause is "
     "inferred spend the smallest dispatch that DISCRIMINATES between the candidate causes - prefer a probe that can "
     "falsify over a retry that can only confirm",
     "APPLIES to diagnosing any failure where a plausible correlated measurement is at hand. DOES NOT APPLY when the "
     "error text names a verified cause and the fix is cheap and reversible",
     "DANGER IF STRIPPED: the first true and available fact is taken as evidence and retries of the real work burn "
     "budget confirming nothing"],
    ["amends E-48 whose design lesson stands"],
    "MEASURED", "two window states and a no-tool probe")

rec("E", ["E-50"], "E-50", "completeness_measured_over_the_task_list_not_over_the_gate",
    "an owner packet said every non-blocked close item was finished and the close tool showed four passes still owed",
    ["An owner decision packet stated that every close item not needing the blocked model was finished. Each item "
     "named was true and verified - the set was invented from the items in hand. Reading the close tool showed four "
     "more passes and an unassembled corpus outstanding",
     "Distinct from E-49: that adopts the first plausible CAUSE and this infers the SCOPE of completion from the "
     "artifacts one is holding. A genuine well-evidenced blocker lends unearned credibility to the claim about "
     "everything else",
     "Measure completeness against the mechanism that enforces it and never against the task list: read the gate or "
     "tool or checklist that decides done and enumerate its requirements from its bytes. An owner-facing "
     "near-completion claim cites where its definition of complete came from",
     "Correct by superseding version: the wrong packet was retained and the new one states what it supersedes and why",
     "APPLIES to any claim that a unit is finished or nearly finished where an enforcing gate or tool exists. DOES NOT "
     "APPLY where no enforcing mechanism exists - then name the definition used and its source",
     "DANGER IF STRIPPED: a false premise enters a decision the owner then makes on it"],
    ["the close tool's assertions and required directories were read after the packet and contradicted it"],
    "MEASURED", "the close tool's assertions read from its bytes")

rec("E", ["E-51"], "E-51", "the_routing_cursor_was_keyed_to_a_ledger_surface_that_had_stopped_being_written",
    "a lesson-routing cursor tracked a row number into a ledger copy that no tool still wrote",
    ["A campaign kept its error ledger in two surfaces and the lesson-routing convention tracked a row number into the "
     "one that had stopped being written - no tool read or wrote it. Routing from the next row would have reported "
     "success and dropped the seven newest lessons",
     "A cursor that advances correctly over the wrong surface reports success while losing the payload",
     "Key an intake cursor to CONTENT - the entry id plus the source sha at write time - and treat a row number as a "
     "convenience only. Name ONE surface authoritative: a second surface no tool writes is a decoy. A stored "
     "position asserts at read time that its file is still the one being written (compare mtime and last id)",
     "APPLIES to any incremental ingest or sync that stores a position into a source. DOES NOT APPLY to full "
     "re-ingests that dedupe by content",
     "DANGER IF STRIPPED: the intake looks healthy on every run while the payload silently stops arriving",
     "This record and its batch were ingested under the corrected rule - by entry id and the markdown sha pinned at "
     "write time"],
    ["JSONL row 85 was E-37 - exactly where the previous ingest stopped - which confirmed the cursor's surface"],
    "MEASURED", "row counts and last ids and writer search of both surfaces")

rec("C", ["OW-21", "OW-22"], "OW-21 OW-22", "a_repeatedly_raised_budget_ceiling_becomes_a_hard_line",
    "after two owner-approved raises the ceiling was declared a hard line with scope cuts in place of raises",
    ["A ceiling raise is the owner's decision at a pre-crossing check-in and is recorded in the ceiling carrier "
     "through a guarded patch - scripts read the carrier and never hardcode the value",
     "After repeated misses name their causes before asking again - here an undercounted census base and each step "
     "surfacing new owed work and review lanes multiplied before re-projecting",
     "Declare the ceiling a hard line: re-forecast from measured per-step actuals at set points with a growth "
     "allowance and bring any forecast above the line as a named scope cut and never as another raise",
     "APPLIES to budgeted multi-step agent work under an owner-set ceiling. DOES NOT APPLY to open-ended exploration "
     "with no ceiling",
     "DANGER IF STRIPPED: each raise is reasonable on its own and the forecast method that keeps missing is never "
     "fixed"],
    ["paraphrased with no verbatim chat and no budget figures per the 2026-09-11 and 2026-09-14 precedent"],
    "TRANSCRIBED", "owner directives OW-21 and OW-22 of 2026-09-16")

rec("C", ["OW-23"], "OW-23", "hardest_first_ordering_rests_on_measurement_and_surfaces_its_input_decisions",
    "an ordering directive was paired with a measured difficulty ranking and the input decision it depends on",
    ["A sequencing directive such as hardest units first rests on a MEASURED difficulty ranking and not on "
     "impression",
     "When the ordering runs into an unmade input decision - here which source text under which licence for a whole "
     "language family - surface that decision as owed with its options and licences before the dependent unit's first "
     "phase. Here it gated most of the remaining units",
     "Units the decision does not gate proceed meanwhile and the decision stays the owner's",
     "APPLIES to campaigns whose order the owner sets and whose units share inputs not yet chosen. DOES NOT APPLY "
     "where every input is already staged",
     "DANGER IF STRIPPED: the named first unit starts and stalls at its first phase on an input nobody was asked to "
     "choose"],
    ["paraphrased with no verbatim chat"],
    "TRANSCRIBED", "owner directive OW-23 of 2026-09-21")

rec("C", ["OW-24"], "OW-24", "cache_reads_are_the_bill_optimise_the_resident_context",
    "in long agent sessions the cost is re-reading resident context and not any single call",
    ["Measured on one orchestrating session: 5566 requests and 2.61 billion cache-read tokens with no single costly "
     "call. Every payload placed in context is re-read by every later request so large writes and tool results carry "
     "the cost",
     "Compact at phase boundaries and past about 120K resident tokens. Read ranges and not whole files. Keep command "
     "output small by construction. Prefer a parameterised generator over re-sent text. Batch independent calls. Give "
     "subagents scoped extracts and a bounded number of tool calls",
     "Enforce it with settings and hooks and a weekly deterministic watchdog that spends no model tokens and "
     "escalates only on issues - not with memory",
     "APPLIES to long agentic sessions with prompt caching. DOES NOT APPLY to short single-shot requests with small "
     "resident context",
     "DANGER IF STRIPPED: per-call tokens are optimised while resident context grows - every call looks cheap and the "
     "bill rises"],
    ["weighted carrying cost led by write payloads then bash results then bash commands then agent prompts"],
    "MEASURED", "one session transcript measured 2026-09-21")

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

    new_ids = [f"E-{n}" for n in range(38, 52)] + ["OW-21", "OW-22", "OW-23", "OW-24"]
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
    result = dict(date="2026-09-22", ledger=str(MD), ledger_sha256_pinned=sha, ledger_sha256_after=sha_after,
                  lessons_root=str(root), files_before=files_before, files_after=post["files_scanned"],
                  next_marker_after=post["next_marker"], markers=markers, problems=problems,
                  records=[{k: w[k] for k in ("tag", "slug", "marker", "lesson_id", "file")} for w in written])
    OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"written {len(written)} | files {files_before} -> {post['files_scanned']} | markers {markers} | "
          f"next free {post['next_marker']} | ledger pinned {sha[:16]} after {sha_after[:16]} | "
          f"problems {problems or 'none'}")


if __name__ == "__main__":
    main()
