# REPAIR-2 STEP 2 — GROUNDS. Author brief.

You are ONE OF TWO BLIND LANES. Another lane has this same brief and the same slices. You will not see its work
and it will not see yours; I reconcile. Do not look for it, and do not read any directory but your own and the
shared inputs named below. Where the two lanes agree I apply; where they differ I adjudicate or escalate. Your
independence is the whole value of your pass — a lane that guesses what the other will say is worth nothing.

## What this step is

Sixteen rows of a Hebrew-Bible chunking corpus carry a decision (a span and a confidence grade) whose GROUND is
missing, stale, or measurably false in the row's own prose. A controlling agent has ruled on each one. Your job
is to write the prose that states the ruled ground, so that — in the ruling's words — *"no row again carries a
grade its own text does not state."*

Nine of these rows had their grade moved mechanically a short while ago and their text has not caught up. That
is why this step exists and why it is urgent: right now those rows are internally inconsistent.

## Inputs (exact paths; read these and nothing else)

- SLICES: `step2_slices.v1.json` in the shared step-2 directory — per row: the live prose, the live evidence
  refs, the current grade, and **THE ORDERS THAT APPLY TO THAT ROW, verbatim** from the rulings and the audit at
  their digests.
- THE GATE: `check_candidate.py` in the same directory. See "The gate" below.

Do not open the corpus file, the rulings themselves, or any review directory. Everything you need is in the
slice.

## The one rule three earlier lanes did not have

**An order is authority for exactly what it names and nothing adjacent.** Three earlier reviewers were given
the before/after bytes but not the orders, and so judged authorised work as unauthorised — three reviewers,
three different thresholds. You have the orders. Use them as the authority for what the row must say.

**A false only-ground is a STOP, never a substitution.** If an order's ground is false on the evidence in your
slice, you do not quietly write a different true ground and call it a repair. You write the order's ground as
far as it is sound, and you report the falsity in `stops` (see the output format). Three rows in an earlier wave
replaced a false only-ground with a true one and reported a successful repair; that is the failure this rule
exists to prevent.

## What to write, and what NOT to write

For each row, propose replacement text for the prose fields that need it:
`boundary_rationale`, `strongest_rejected_alternative`, `device_notes`, `literature_type_guess`.

DO:
- State the ruled ground **in substance**, as a description of the text and its devices.
- Name the verses and the devices: which formula stands where, whether it is verse-final or mid-verse, what
  section mark (samekh / pe) stands on which verse, what the far face of a seam carries.
- Delete sentences the orders identify as false, and sentences that state a grade the row no longer carries.
- Keep the row's voice and length discipline. Match the surrounding prose; these are terse scholarly notes.
- Where you quote Hebrew, the quotation travels with its witness attribution (OSHB/WLC); where you quote the
  English version, likewise (WEB). Do not paste long runs — a few words is the convention here.

DO NOT:
- **Do not change any confidence grade.** They are already applied and are not yours to move. Write prose that
  is true of the grade the slice states.
- **Do not change any span, verse range, or identity field.**
- **Do not re-face or re-tokenise the evidence refs** (the `oshb:` / `web:` prefixes, the bracketed role tokens,
  the near/far/interior qualifiers). Several orders mention that work; it is a LATER step with its own
  vocabulary, and doing it here would collide. Prose only.
- **Do not narrate the repair.** No "this was corrected", "the earlier claim is withdrawn", "as ordered". The
  row states facts about the biblical text, not its own editorial history.
- **Do not name the machinery.** No rule identifiers, no ruling numbers, no file or tool names, no digests, no
  "the audit", no "the division plan", no reviewer or wave references. State the fact; the authority is recorded
  elsewhere. This is a hard rule and the gate enforces a floor under it.

## The gate — run it until it says ALL_CLEAN

Run, from the shared step-2 directory:

    python check_candidate.py <your-dir>/proposal.json

`proposal.json` maps a row id to the fields you are replacing, and nothing else. The tool builds your row in
memory (it never writes to the corpus) and reports every register class that fires with the matched substring,
plus the citation-mirroring verdict.

**Iterate until `ALL_CLEAN` is true.** A proposal with flags is not finished. If a flag looks wrong to you, say
so in `disagreements` and rephrase anyway — the gate is a floor, not a ceiling, and argued exceptions go to me.

This gate exists because a brief was once written from the orders and never checked against the gate: three
checks it called green went red, and one duty was not merely omitted but contradicted. Do not repeat that.

## Evidence tiers — say which you have

Every factual claim you write carries its true tier, and you record that in your output (not in the row prose):
MEASURED (you verified it in the slice's own bytes) > EXTRACTED (quoted from an order in the slice) > REPORTED
(an order asserts it and you did not verify) > INFERRED > ASSUMED > UNAVAILABLE.

UNAVAILABLE is a value you write, never a blank you leave. Corroboration never upgrades a tier. If an order
states a measurement you cannot check from the slice, your tier is REPORTED — say so; do not write MEASURED
because a ruling measured it.

## Output — write exactly these two files in YOUR OWN directory

1. `proposal.json` — the replacement text, gate-clean.
2. `discharge.json`, with this shape:

    {
      "lane": "<your lane letter>",
      "rows": {
        "P08-003": {
          "orders_discharged": [
            {"order": "<the clause you are discharging, quoted from the slice>",
             "the_sentence_that_discharges_it": "<quote from your own proposal>",
             "tier": "MEASURED|EXTRACTED|REPORTED|INFERRED|ASSUMED|UNAVAILABLE"}
          ],
          "sentences_deleted_and_why": [{"deleted": "...", "why": "..."}],
          "fields_left_alone": ["..."],
          "stops": [{"order": "...", "why_its_ground_is_false": "...", "what_i_wrote_instead": "..."}],
          "disagreements": [{"with": "the order|the gate", "what": "...", "my_reading": "..."}]
        }
      },
      "gate": {"ALL_CLEAN": true, "total_register_flags": 0},
      "what_i_could_not_verify": ["..."],
      "limit": "<one paragraph: what your pass covered, what it did not, and where a reader should not trust it>"
    }

Every order in every slice must appear either in `orders_discharged` or in `stops`. An order you silently drop
is the exact defect this step is cleaning up: four ordered items reached no row while every sweep reported full
parity, because the sweeps counted items and never read content.

## Hard stops

- Never modify any file outside your own directory. Not the corpus, not the slices, not the tools.
- Never run git. Never write a receipt. Never touch a registry or manifest.
- If an input is missing or a digest looks wrong, STOP and report it rather than working around it.
- If you find you have made a mistake mid-pass, say so in your output plainly and correct it; a disclosed
  mistake costs a paragraph, an undisclosed one costs the round.
