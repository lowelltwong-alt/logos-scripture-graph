rec("E", ["E-52"], "E-52", "a_pointer_to_future_state_written_into_the_store_that_defines_it_is_a_write_to_it",
    "a postflight that named the next free marker number for the next writer took that number itself",
    ["A record written to help the next writer changed the state the next writer reads: the DAD scanner allocates the "
     "next control marker from every bare marker mention in any non-index record - so a postflight that named the next "
     "free number as a pointer burned it",
     "Never write a forward marker number into any record. Say the next free marker per the scanner and let the next "
     "writer read it in the same scan that clears its dedupe",
     "Enforce it in a tool and not in memory: a pre-send lint uses the scanner's own bare-mention pattern and refuses "
     "any marker at or beyond next-free that the write is not allocating. The burned number stays burned because the "
     "series is append-only and a skipped number costs nothing",
     "APPLIES to any store whose next identifier is derived from the mentions already in it. DOES NOT APPLY where "
     "identifiers are issued by a counter that record text cannot move",
     "DANGER IF STRIPPED: a helpful forward pointer reads as harmless prose while it silently advances or collides the "
     "series"],
    ["the scanner reported the next free marker one past the last allocation once the postflight was written"],
    "MEASURED", "a re-scan of the live lesson tree in the same session")

rec("C", ["OW-25"], "OW-25", "a_declared_same_weights_fallback_grader_is_recorded_as_a_downgrade",
    "a checking role assigned to one model family ran on the authoring model when the assigned model was unavailable",
    ["When the model assigned to checking and adjudicating roles is unavailable the owner may declare in advance one "
     "fallback model for every role. The fallback is recorded as a downgrade on every completion receipt and never as "
     "the original assignment",
     "Author and grader then share one set of weights. A blind lane of the same model is a genuine second context but a "
     "weaker second mind because correlated habits are what a same-weights reviewer is least able to see",
     "Decorrelate the two-lane floor by the means that remain: blind briefs that differ in method and read order and no "
     "shared intermediate files and deterministic gates wherever a check can be computed and evidence that cites source "
     "bytes rather than another lane's prose",
     "A code gate keeps naming its model: it reads the declared fallback from a carrier and asserts the downgrade "
     "statement rather than being loosened to accept any model. A closed unit's tool is its record and is not edited",
     "APPLIES to multi-lane review where one model family was assigned the checking roles. DOES NOT APPLY where "
     "reviewers of different families remain available",
     "DANGER IF STRIPPED: a same-weights grade is read as an independent grade and the floor looks met while its "
     "decorrelation is gone"],
    ["paraphrased with no verbatim chat and no account or budget details"],
    "TRANSCRIBED", "owner directive OW-25 of 2026-09-22")

rec("C", ["OW-26"], "OW-26", "a_merged_verdict_scope_cut_states_that_its_passes_share_one_reader",
    "separately scoped review passes were merged into one blind lane pair returning every verdict to stay under a "
    "budget line",
    ["When a budget line forces a scope cut the cut is named and chosen by the owner in place of a raise. Here several "
     "separately scoped passes became one pair of blind lanes that each return every verdict in one pass",
     "State the weakness with the choice: the verdicts share one reader per lane so a checker that misses something "
     "misses it in all of them. The two-lane floor is still met but the passes are no longer separate lenses and the "
     "completion receipt says so",
     "A pass that is cut is recorded as OWED NOT MET - it is not run and not claimed",
     "APPLIES to review plans cut to fit a budget or a deadline. DOES NOT APPLY where every pass runs as scoped",
     "DANGER IF STRIPPED: merged verdicts are read as independent passes and the owed pass is forgotten"],
    ["paraphrased with no verbatim chat and no budget figures"],
    "TRANSCRIBED", "owner directive OW-26 of 2026-09-22")

rec("E", ["E-53"], "E-53", "a_blind_guard_that_answers_clear_is_worse_than_no_guard",
    "a pin guard read the orchestrator's own launch rows as landings and answered clear while two lanes ran",
    ["Two faults in one lane pair. Close briefs told lanes to run record-writing checkers in place - checkers that "
     "regenerate the records the same briefs pin - though those briefs were never dispatched. And the in-flight pin "
     "guard treated every receipt row carrying an execution id as a landing including launch rows - so two lanes were "
     "counted as landed at launch",
     "A blind guard that answers CLEAR licenses the write it exists to stop. Observed impact was nil because no write "
     "made while the guard was blind touched a pinned path - that was luck and not control",
     "Route every record-writing checker a lane runs through a mirror that copies it into the lane's own scratch. A "
     "launch row is never a landing: a lane's completion row amends its launch row and a resumed execution gets no row "
     "until it lands. Never trust a guard CLEAR unless its in-flight list names what is known to be running",
     "APPLIES to any guard that infers in-flight state from records written by the process it guards. DOES NOT APPLY "
     "where in-flight state comes from the runtime itself",
     "DANGER IF STRIPPED: a regeneration during a blind review changes the bytes both verdicts are bound to"],
    ["all 100 lane pins measured intact afterwards",
     "guard selftest of 22 vectors green with the pre-fix guard red on 3 of them"],
    "MEASURED", "a digest re-check of every lane pin and the guard's selftest")

rec("E", ["E-54"], "E-54", "a_completion_notification_token_figure_is_the_last_requests_context_not_spend",
    "per-lane token figures taken from the completion notification were recorded as spend",
    ["The token figure in a subagent completion notification is the last request's total context size and not "
     "cumulative spend. Spend is input plus cache creation plus output per unique message id and is measured from "
     "usage fields at landing",
     "A census that sums notification figures is a lower bound in a weaker sense than stated and a budget line read "
     "against it can be crossed while it reads as held",
     "Sibling: a failed or interrupted execution is measured from its output directory and usage fields and never from "
     "its last message - one reported as having done essentially no work had written 82 files",
     "This record's inference that compaction caused the undercount was superseded by the E-55 re-measure",
     "APPLIES to any budget or effort figure taken from an agent runtime's completion summary. DOES NOT APPLY where the "
     "runtime reports cumulative usage explicitly",
     "DANGER IF STRIPPED: the reported figure looks exact and is off by a multiple"],
    ["two merged lanes measured at several times their notification figures and amended before any decision used them"],
    "MEASURED", "each lane's own usage fields deduplicated by message id with content not read")

rec("E", ["E-55"], "E-55", "a_diagnosis_drawn_from_two_cases_is_tested_across_the_census_before_adoption",
    "the undercount blamed on compaction sits mostly in never-compacted runs as repeated cache writes and output",
    ["Amends the E-54 record: across 226 re-measured attempts the notification figure matched the last request's "
     "context in 152 of 185 groups which confirms the unit finding. But the gap sits mostly in groups that never "
     "compacted - cache writes summed well past the executions' maximum contexts and output added the rest",
     "A diagnosis drawn from two cases is tested across the whole census before it is adopted. Why the caches were "
     "rewritten is recorded UNKNOWN and not guessed",
     "When two units disagree the unit a ceiling is denominated in is the owner's to rule. The orchestrator does not "
     "reinterpret it and neither unit is claimed to be how the owner's plan meters usage",
     "APPLIES to cost or effort audits that reconcile per-execution figures against a measured total. DOES NOT APPLY "
     "where the only figure available is the runtime's own cumulative count",
     "DANGER IF STRIPPED: the cure targets compaction while the real cost driver keeps running"],
    ["spend-unit lower bound about 1.66 times the notification-unit sum over the same attempts",
     "siblings: 7 launch rows put the lane id in the parent field and 2 lanes were missing from the transcript map"],
    "MEASURED", "226 attempts re-measured from their own transcripts' usage fields")

rec("C", ["OW-27"], "OW-27", "re_measure_by_script_before_spending_apparent_headroom",
    "the owner raised a per-book ceiling and ordered a script-only re-measure before any lane spent the room it "
    "appeared to leave",
    ["When headroom is an upper bound over a total that may already be past the line the first act is a re-measure by "
     "script with no model lanes. Only if it confirms room does the next lane run and then under a hard per-lane cap "
     "forecast from measured actuals with a growth allowance",
     "A ceiling raise is recorded in the ceiling carrier through a guarded patch",
     "When the owner's words leave a ruling's scope open the orchestrator's reading is recorded as INFERRED beside the "
     "owner's words and never merged into them",
     "APPLIES to budgeted agent work where the spend total is uncertain. DOES NOT APPLY where spend is metered exactly "
     "at every step",
     "DANGER IF STRIPPED: a lane is dispatched on room that was never there"],
    ["paraphrased with no verbatim chat and no budget figures"],
    "TRANSCRIBED", "owner directive OW-27 of 2026-09-23")

rec("C", ["OW-28"], "OW-28", "budgets_tracked_not_gating_and_a_deferred_gate_is_never_met",
    "the owner made budgets tracked rather than gating and deferred the strongest model's review to the campaign's end",
    ["The owner may change a budget from a gate to a tracked figure. Token efficiency stays a goal: lean lanes and "
     "delta re-checks and spend measured at every landing with both units named",
     "When a review by an unavailable model is deferred to the end of a campaign each unit's close carries a packet for "
     "it: every row graded low or medium_low with its sidecar and register entry and the orchestrator's notes on lane "
     "splits and reservations and residuals",
     "A close gate that requires the deferred model is recorded DEFERRED and never MET",
     "APPLIES to long campaigns whose strongest reviewer is scarce or costly. DOES NOT APPLY where every gate's reviewer "
     "is available at each close",
     "DANGER IF STRIPPED: a deferred gate is read as passed and the end review has nothing to review"],
    ["paraphrased with no verbatim chat and no budget figures"],
    "TRANSCRIBED", "owner directive OW-28 of 2026-09-23")

rec("E", ["E-56"], "E-56", "an_owner_question_premise_carries_the_evidence_duty_of_a_finding",
    "an owner choice was framed from a tool's docstring and two of its premises measured false",
    ["The facts in a question put to the owner were drawn from an earlier description in a tool's docstring and not "
     "from a measurement made for the question. Measured afterwards the shared feed already mixed the two shapes and "
     "neither option had been checked against the validator rule that would refuse one of them",
     "Implication is assertion: a premise in an owner question is sourced from a measurement made for it with its "
     "evidence tier named",
     "Sibling: an expected-before check in an amend script was a no-op on its run and was disclosed with the exact "
     "before-bytes kept",
     "APPLIES to any decision packet whose options are described with facts about current state. DOES NOT APPLY to "
     "questions of pure preference with no factual premise",
     "DANGER IF STRIPPED: the owner chooses on false premises and the choice binds a shared registry"],
    ["the owner asked for pros and cons before choosing and the answer given then was measured"],
    "MEASURED", "the shared feed's row shapes counted by book")

rec("E", ["E-57"], "E-57", "a_gate_named_for_a_rule_is_re_read_field_by_field_against_the_rule",
    "a coverage gate named for a validator rule checked four of its five fields and its cure bound wrong",
    ["A gate named for a validator's rule did not check one of the rule's fields so its name overclaimed. The rule had "
     "been transcribed from memory of the validator and not re-read field by field against its code",
     "Its cure appended a precedence-sensitive boolean without parentheses and no unit case exercised a row outside the "
     "target set. Both faults were caught by the first dry run before any close",
     "Running the full validator exposed a campaign-level gap older than the unit: the closed books from one point in "
     "the campaign on lack a review-packet file that no later close tool writes. It is routed to the owner as a "
     "decision and not fixed inside one unit's close",
     "APPLIES to any gate or check that claims to implement another tool's rule. DOES NOT APPLY where the gate calls "
     "the rule's own code",
     "DANGER IF STRIPPED: a gate passes a feed the validator refuses and a crash hides a gate's verdict"],
    ["unit cases lifted from the close tool by AST: the fixed copy passes all five and each earlier copy fails the "
     "case written for it"],
    "MEASURED", "the full validator run and the close tool's unit cases")

rec("C", ["OW-29"], "OW-29", "the_close_act_runs_only_after_a_same_arguments_dry_run_shows_zero_unmet",
    "the owner released a unit's close act to the orchestrator on a dry-run precondition and replaced the routine "
    "boundary stop with compaction",
    ["The orchestrator may run the close only after a dry run with the same arguments shows zero unmet gates. A refusal "
     "is a stop to report and never a retry around a gate",
     "The routine stop at a unit boundary becomes compact then continue. Stop only for decisions that are the owner's",
     "A decision the owner routes to a scarce model is given to it as a self-contained brief kept lean in both input "
     "and output as the owner asked",
     "APPLIES to campaigns with a deterministic close gate that has a dry mode. DOES NOT APPLY where the close has no "
     "dry mode or its gates are not deterministic",
     "DANGER IF STRIPPED: a close runs without a clean preview or the campaign stops at every boundary for no "
     "decision"],
    ["paraphrased with no verbatim chat"],
    "TRANSCRIBED", "owner directive OW-29 of 2026-09-23")

rec("C", ["OW-30"], "OW-30", "a_scarce_model_ruling_is_bought_once_and_recorded_as_standing_precedent",
    "one call to a scarce model was authorized for one ruling and its rule sentences were recorded to apply without "
    "asking again",
    ["When the owner authorizes a single call to a scarce or costly model the call is scoped to one decision and every "
     "other role stays on the declared model. Any further call needs a new authorization",
     "Ask the ruling model for its rule sentences as well as its rulings and record them where later units read them - "
     "so the same ruling is not bought twice",
     "For each later case measure its ground on the current corpus and apply the matching rule and record the rule and "
     "the measurement. A case that fits no rule or fits one only by judgment rather than measurement goes to the owner",
     "The precedent here: a hold whose row defect measures absent is released. A class question is not a row defect "
     "and releases the hold or drops a row graded above the low bands from the feed. A defect still present keeps the "
     "hold and re-versions the corpus for two blind lanes",
     "APPLIES to recurring hold or release decisions across the units of a campaign. DOES NOT APPLY to a case whose "
     "ground the precedent's rules do not name",
     "DANGER IF STRIPPED: the scarce model is asked the same question at every unit or its precedent is stretched by "
     "judgment to cases it never ruled"],
    ["one call with zero tool uses measured from its usage fields"],
    "TRANSCRIBED", "owner directive OW-30 of 2026-09-23 and the ruling file it produced")

rec("E", ["E-58"], "E-58", "a_subagent_cost_estimate_starts_from_the_measured_floor_of_its_agent_type",
    "a cost estimate for one ruling call was sized from the brief and missed by the agent's fixed context",
    ["An estimate put to the owner counted the brief and the reply but not the fixed system prompt and tool definitions "
     "the agent type carries - which were most of the measured cost",
     "Estimate a subagent call as the measured floor for that agent type plus the brief plus about twice the reply for "
     "reasoning",
     "A leaner agent definition with no tools lowers the floor. It is proposed to the owner and not created",
     "APPLIES to cost estimates for single subagent calls with small briefs. DOES NOT APPLY to long multi-call lanes "
     "where the floor is a small share",
     "DANGER IF STRIPPED: every estimate for a small call misses by the same floor on credits the owner pays for"],
    ["measured about 2.6 times the top of the stated estimate with the fixed floor near 90 percent of the total"],
    "MEASURED", "the call's own usage fields")
