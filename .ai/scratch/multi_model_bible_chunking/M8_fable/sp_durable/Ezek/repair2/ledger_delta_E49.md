
## E-49 (2026-09-21) - AMENDS E-48: THE FIRST MEASURABLE CAUSE WAS ADOPTED WITHOUT TESTING IT

E-48 recorded that the two blind close-gate lanes failed on the account's five-hour usage window, measured at 95
percent with the weekly window at 13 percent, and concluded the gate "cannot be graded at all until the window
resets". The measurement was real. The conclusion was not tested. The window then reset - MEASURED at 6 percent used,
fresh for five hours - the brief pins were re-verified MATCH, and both lanes were relaunched. **Both failed again with
the identical HTTP 429.** A cause that holds at 95 percent and at 6 percent is not the window.

Rather than launch a fifth identical lane, the next dispatch was made as small as a dispatch can be: one line of
instruction, no brief, no file read, every tool forbidden, ordered to reply with the single word `OK`. It failed the
same way. That eliminates brief size, pinned-input cost, context and tool budget, and both usage windows. What remains
is the model: **`claude-fable-5-1` is not dispatchable on this account as configured**, which is also what the error
says in its own words - switch model, or add usage credits - with extra usage disabled at 0.00 of 65.00 USD.

**The lesson is not about a rate limit.** Five dispatches over two window states produced one diagnosis in about an
hour, and four of them were spent on a hypothesis that a single cheap probe would have refuted first. The habit to
break: *a measurement taken next to a failure is not a test of the failure's cause*. The five-hour window was at 95
percent, which was true, available and causally plausible - and being the first true thing found is not evidence.
**Cure: before retrying a failure whose cause is inferred, spend the smallest dispatch that would DISCRIMINATE between
the candidate causes, and prefer the probe that can falsify rather than the retry that can only confirm.** A probe
that costs one line is cheaper than any retry of the real work, and the cheapest probe is the one that removes every
variable except the one under test.

**The governance consequence stands and is now permanent rather than temporary.** OW-13 names Fable 5.1 for the
checking and adjudicating role; OW-19 forbids the orchestrator from grading its own work. Close-gate items 20-23 are
authored by the orchestrator and therefore have no admissible grader on this account today. An Opus lane is not a
substitute - same family and, for these items, the same author, which OW-19 counts as one voice. Ezekiel is therefore
**HELD at the close gate with every non-Fable item finished**, and the choice between enabling paid credits, naming a
different grader, or accepting a recorded grading gap is the owner's, not the orchestrator's. **E-48's design lesson
survives its own diagnosis being wrong: a governance floor that depends on a single named model can vanish for
reasons the campaign does not control, so the floor needs a declared fallback grader chosen in advance - by the
owner - rather than improvised at the gate by the agent the floor exists to check.**
