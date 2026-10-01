# BIBLE CHUNKING METHOD — v4

**Reader: anyone chunking a book of the Bible into literary units.** Not a scholar reading one book, and not an
orchestrator running an agent mesh. This is what previous and concurrent generations learned, why, and what they could
not settle.

**Authority:** owner directives **OW-17** with amendments (a), (b) and (c), and **OW-18**, both 2026-09-15,
recorded verbatim in `M8_fable/ERROR_PATTERN_LEDGER.v1.md` and as rows `OW-17`, `OW-17-a`, `OW-17-b`, `OW-17-c` and
`OW-18` of `M8_fable/error_pattern_ledger.v1.jsonl`. Close-gate items 20, 21, 22, 23 and 24 bind every book close
and every campaign close to updating this file.

**This version:** v4, written by generation **M8** during Ezekiel (book 26 of 66), **30 of 44** dual-blind primary
review executions landed. **Supersedes v3** (`BIBLE_CHUNKING_METHOD.v3.md`, sha256
`52657dc47bc6e975ff632a0dac6dc22564c79a85b86cab7a258cbaac02a4d382`), which superseded v2
(`BIBLE_CHUNKING_METHOD.v2.md`, sha256 `82fcfbe245ac675ab0158d2767d50e9dc43b3ad81505167993d8d34f78a41ed3`), which
superseded v1 (`BIBLE_CHUNKING_METHOD.v1.md`, sha256
`6c9948faf67d7741558fb565e863376b41d60b05269e995173f116230fa8236a`). Every earlier version's bytes are kept unchanged
so the evolution of this method is itself auditable.

**Self-contained.** You do not need an earlier version to use this one.

---

## 0. Version history — how this method has changed, and why

Read this before trusting any rule below: knowing *when* a rule appeared and *what prompted it* is how you judge
whether it applies to you.

### v3 → v4 (M8, Ezekiel, 2026-09-15)

| Change | Why |
|---|---|
| **§18 is new: provenance tiers, and the ban on implying a provenance you do not hold.** Every substantive claim names how it is known — MEASURED, EXTRACTED, TRANSCRIBED, REPORTED, INFERRED, ASSUMED, UNAVAILABLE — and never a stronger tier than is true. Silence about a *change* in how a record was produced is itself a false claim. | Owner directive OW-18. Two M8 executions landed with an empty harness transcript, so their capture could not be extracted the way the 28 before them were. The orchestrator labelled the weaker tier; the owner made that a law, on the ground that a reader who cannot tell measurement from assertion cannot check us, and that over the text of scripture a half-truth is not a lesser error than a falsehood. |
| §18 also carries the correction that produced its final shape: the first attempt collapsed two different facts into one tier and mislabelled 29 records. | A generalisable trap, not an M8 accident: *how a record was produced* and *whether it is still re-derivable* are different claims with different evidence, and collapsing them produces a confident wrong label. |
| §10 gains the durability finding behind it. | Measured 2026-09-15: **29 of 30** agent transcripts were already 0 bytes. A capture design that depends on the runtime's own transcripts is not durable, and this is a property of harnesses generally, not of one vendor. |
| §16 gains obligation 10. | An honesty rule nobody is obliged to check is a rule that decays into a preference. |

### v2 → v3 (M8, Ezekiel, 2026-09-15)

| Change | Why |
|---|---|
| **§17 is new: the method-change proposal loop.** One subagent per book proposes changes to this record; proposals are LOGGED as candidates, never applied by the proposer; a checking execution then adjudicates each one and rates it NECESSARY / USEFUL / LOW-REWARD. | Owner directive. Two failure modes were both live in M8: the method ossifying because nobody was tasked with improving it, and the method bloating because any defect could become a rule. Separating *proposing* from *adopting* prevents both, and the log becomes the measurement §12 asks for and M8 did not have — whether our own rule-making is worth its cost. |
| §16 gains the obligation to run the loop and to adjudicate it. | A loop nobody is obliged to run is a loop that does not run. |

### v1 → v2 (M8, Ezekiel, 2026-09-15)

| Change | Why |
|---|---|
| **§1 is new and it revises v1's central assumption.** v1 was written as a sequential baton pass, one generation to the next. It is now known that generations run **CONCURRENTLY** — M9 was ~15 books into its own campaign while M8 was on book 26, neither aware of the other's conventions. | v1's whole framing was wrong on a structural fact. A method record shared by concurrent generations is a *merge*, not a handoff, and needs a reconciliation protocol and a divergence register. |
| **§5 is new: settle conventions before mass review.** | M8 reviewed 145 units on an *unstated* paragraph-mark convention and discovered mid-wave that units disagreed about its direction. The sequencing error, not the units, was the defect. |
| **§9 expanded: pilot before committing; make every validator flag a question; check every boundary rule in both directions.** | M8 piloted 2 of 44 executions and found a schema defect that would have made all 44 packets unlandable. Requiring reviewers to *adjudicate* each automated flag surfaced four separate validator coverage holes. One hole — a check that looked only behind a unit's onset — was found independently by four executions. |
| **§10 is new: capture discipline.** | M8's landing pipeline silently dropped the field in which a worker discloses its *own* defect; one such disclosure existed nowhere durable. Separately, M8 had ~60 recorded failures and no record of which control had ever stopped anything, so nothing could be safely simplified. |
| **§11 is new: verify coverage as set equality.** | A row id absent from a cluster plan looked like an unreviewed unit; it was a retired id. A count check would have passed either way. |
| **§12 is new and uncomfortable: do not let the scaffolding eat the scholarship.** | Raised by the project owner watching M8 spend a large part of a working session fixing its own checking machinery rather than reviewing scripture. It is a real failure mode and it belongs in a method record. |
| §8 open questions: two reclassified as extraction problems rather than judgement problems. | They are fixable by better extraction, which is a different kind of work from adjudication. |

### v1 (M8, Ezekiel, 2026-09-15)
First version. Written because **no method record existed to inherit** — see §2.

---

## 1. Generations may be running RIGHT NOW. Reconcile before you trust anything

v1 assumed you inherit this file from a finished predecessor. That is false. Campaign generations overlap: while M8
was on book 26, generation M9 was roughly 15 books into its own campaign, and neither knew which conventions the
other was applying.

**Why this is the highest-stakes section in the document.** Two generations chunking the same Bible under different
conventions produce two corpora that cannot be merged, *and neither is wrong on its own terms*. The divergence is
invisible from inside either one. It is also the single largest blast radius available: a convention difference
affects every unit in every book both generations have closed.

**So, before mass review, and before adopting this file:**

1. **Find out who else is running.** Do not assume you are the only live generation or the latest.
2. **Reconcile the conventions explicitly**, one question at a time, asking what each generation's closed books
   *actually did* — not what it would now do. The list to reconcile is: paragraph-mark direction (§6); whether
   translation layout was gated (§4); apparatus read-form rendering (§7); dual references in numbering-divergence
   zones (§8); the finished-artefact re-check (§7); both-face evidence (§3).
3. **Keep a divergence register.** Where generations differ, record which books are affected on each side before
   deciding who changes. A divergence found and priced is a manageable problem; one discovered at merge time is not.
4. **Reconciliation is two-way.** A generation 15 books in has learned things a generation on book 26 has not.
   Send your rules and open questions *back*, and do it while the other generation can still change its output.
5. **Do not adopt a rule here because it is written down.** If your reasoning is better, this file is what changes.

---

## 2. The origin gap, stated plainly

M8's Phase 0 had no inherited method record. Earlier generations left an orchestration playbook (how the agent mesh
runs) and a long error ledger (what went wrong, filed by error class), but **nothing that told a chunker how to decide
a boundary well.** Every generation re-derived the method from the text and from its own mistakes.

This document exists so that stops. It is not a log of what happened to us; it states what you should *do*, with the
evidence behind each rule so you can judge it rather than inherit it blindly.

**M8 makes no claim to carry M7's lessons.** It found no method document to inherit. If you find one, reconcile it and
state which rules survived.

---

## 3. What a chunk is

A chunk is a **literary unit**: a stretch of text that begins and ends where the text itself marks a beginning and an
end — not where a chapter, a verse, a translation paragraph, or a convenient length suggests.

Two consequences that cost M8 real work:

- **A boundary is a claim, and it needs evidence on BOTH faces.** The close of one unit and the onset of the next are
  two separate claims. A seam argued from one side only is under-evidenced even when it is right.
- **A boundary can be right for the wrong reason.** This is the dominant finding of M8's Ezekiel review: across 22
  independent review packets over 145 proposed units, the *spans* held up almost everywhere while the *stated grounds*
  failed repeatedly — reviewers kept the boundary and rejected the reason in the large majority of challenges. If you
  only check whether boundaries look right, you will certify a corpus whose reasoning is unreliable.

---

## 4. Evidence that licenses a boundary

Ranked, strongest first. Names are generic; each book's own devices belong in that book's strategy.

1. **Structural formulae of the book's own vocabulary.** In Ezekiel: word-event formula, messenger formula, utterance
   signature, recognition refrain, direct-address vocative. Establish the **census** — the verse list, not the count
   alone — before reviewing anything.
2. **Closural refrains.** A unit ending on a close-grade device is far better evidenced than one that merely stops.
3. **The received paragraph layer.** Corroborating, never deciding. See §6.
4. **Content and participant structure** — inclusio, addressee change, genre shift, participants entering and leaving.
5. **Syntax.** A construction spanning a proposed seam is evidence against it. M8 found a proposed close dividing a
   temporal frame from the main clause it governs.

**Never licensing on its own:**

- **Translation layout.** Paragraphing, punctuation, capitalisation and poetry lines are the translators' editorial
  decisions, not the source's. An earlier generation's corpus was damaged by this. **Check it positively:** list where
  the translation breaks, list where your seams fall, and show they are independent. One M8 cluster demonstrated the
  absence explicitly — eight translation breaks, six seams, none coinciding except where independently grounded.
- **Chapter and verse numbers.** Medieval and later apparatus.
- **Length or balance.** A seven-verse unit beside a fourteen-verse unit is not a problem to fix.

---

## 5. Settle your conventions BEFORE mass review

New in v2, and it is a sequencing rule, not a preference.

M8 reviewed 145 units and then discovered, from the reviews themselves, that units disagreed about which direction a
paragraph mark points. The units were not the defect; reviewing them before the convention was stated was.

**Before a review wave:**

1. **Enumerate the conventions your book depends on** — mark direction, what counts as an onset device, whether
   apparatus forms may be rendered, in-span disclosure obligations, reference format in numbering zones.
2. **Rank them by blast radius** (§15) and settle the widest first. A convention affecting every unit is worth a
   dedicated adjudication before review, not a finding discovered 145 units in.
3. **State each settled convention explicitly in the reviewers' brief.** M8's reviewers applied the mark convention
   correctly and consistently *once it was written down*, and inconsistently before.
4. **A convention question is never a one-unit question.** Filing it as one is how it stays unsettled.

---

## 6. The received paragraph layer: a convention that will bite you

**A mark is recorded ON the verse it FOLLOWS.** A mark recorded at verse 20 divides 20 from 21.

M8 found units across three separate clusters crediting such a mark as corroborating *that same verse* as their own
**onset** — reading its direction backwards and making it interior to the span rather than front-seam evidence. In one
cluster the *same* mark was read one way by a unit and the opposite way by the adjacent unit. Both lanes of the
dual-blind pair found this independently wherever both ran.

**What to do:** state the convention in the brief, and check every mark claim for **direction**, not merely existence.
Ask of each: does this mark fall at the seam claimed, or one verse off?

**A limit to record rather than paper over:** M8's staged mark data carries no **within-verse position**. Where a mark
sits relative to a mid-verse formula is unknowable from it, and several reviewers correctly declined questions turning
on it. **If your extraction can carry within-verse position, carry it** — it would have settled at least three open
questions in Ezekiel. This is an extraction problem, not a judgement problem.

---

## 7. Witnesses and quotation discipline

Where M8 was bitten hardest, twice, and where its one control with *proven* effect lives.

- **Quote by copying, never by typing.** Slice the exact substring out of the witness programmatically. Never retype,
  re-point, add or strip an accent, or construct an apparatus notation the source does not itself contain.
- **Verify mechanically, not visually.** Combining marks and accents are invisible to the eye. One M8 reviewer reported
  an accent difference from visual inspection that collation disproved; another produced three false quotation failures
  from its own parser error, which it then found and fixed.
- **Re-check the FINISHED artefact against the source before returning, and report the count checked.** This is the
  rule that worked. An early M8 execution fabricated a ketiv/qere composite — merging fragments of two words,
  substituting one accent — with a **correct conclusion resting on invented evidence**. The rule written in response
  caught the same defect class three clusters later inside another execution's own first build, which had corrupted
  accents in **16 of 19** runs. Caught *before return*, root-caused to hand-authored escape sequences, and cured by
  making the generator slice from the witness and **refuse to write** unless every slice collates.

  **Generalise the shape, not the topic:** a mandated mechanical re-check of the finished artefact against its source,
  with the count reported in the deliverable. An agent cannot satisfy that by intending to be careful — it has to run
  it, and the reported count makes an omission visible.

- **A correct conclusion on fabricated evidence is worse than a wrong conclusion**, because it survives review on its
  conclusion. Check evidence independently of verdicts.
- **Name a variant site rather than rendering it** when the form is apparatus-only.
- **Apparatus read-forms frequently do not occur in the running text at all.** In one Ezekiel cluster, all six
  ketiv/qere sites had read-forms absent from their own verse's running text. Decide once, campaign-wide, and record
  the decision — M8 left this open (§13).

---

## 8. Numbering divergence between witnesses

Where witnesses number differently, **every reference in that zone carries both numbers, in prose as well as in
structured fields.** Ezekiel has such a zone: MT 21:1–5 = WEB 20:45–49 and MT 21:6–37 = WEB 21:1–32, identical
elsewhere.

Build the offset map as a Phase-0 artefact and make the dual-reference rule a hard gate with a mechanical check. M8's
reviewers passed it cleanly once stated. The cost of not stating it is a corpus whose references silently mean
different verses in different units.

---

## 9. Review design: what actually found things

**Two independent reviewers per unit group, blind to each other, different lenses, different reading orders.** M8 used
a literary-form lane and an original-language lane. Full coverage, no sampling.

What it bought, measured:

- **Independent convergence on real defects** — the same ordinal error in a formula census; the same false lexical
  exclusivity; the same mark-direction inversions; the same absent messenger formula.
- **A boundary change a single reviewer would not have delivered.** Both lanes independently proposed cutting at the
  same verse by *different* evidence: one from device-class analysis, one from the paragraph layer plus the observation
  that the corpus already cut on that device elsewhere on weaker evidence. Two routes, one answer.
- **Genuine disagreements, delivered already argued.** On one unit both lanes found the *same* false ground, both rated
  it high, and reached **opposite remedies** — one keep, one cut. That is the design's most valuable output: a real
  open question handed up with both cases made from the bytes, rather than one confident answer with no sign the other
  side existed.

**Keep the lanes genuinely blind.** Neither may see the other's output, the adjudications, earlier repair orders, or
any transcript. Give them deliberately different reading orders so they cannot converge by route.

**PILOT BEFORE YOU COMMIT THE WAVE.** M8 ran 2 of 44 executions first and found that the reviewers' deliverable schema
did not match the landing validator — not cosmetically; it *crashed* the tool. All 44 packets would have been
unlandable. A pilot costs ~5% of a wave and insures the rest. Make the pilot's pass condition a *landed* packet, not a
returned one.

**MAKE EVERY VALIDATOR FLAG A QUESTION, NOT A VERDICT.** Require each reviewer to *answer* every automated flag on its
units — genuine, or false positive with a reason. This converts a flag list into decisions and, in M8, surfaced four
separate validator coverage holes that no one was looking for.

**CHECK EVERY BOUNDARY RULE IN BOTH DIRECTIONS.** M8's mark cross-check looked only at the mark *behind* a unit's
onset and was structurally blind to marks *inside* a unit's own span. Four independent executions found undisclosed
in-span marks it could not see; one cost a confidence level. Whenever you check a boundary property, check both faces,
and check both the presence and the absence case.

---

## 10. Capture discipline: what you will lose if you are careless

**Measured warning, added in v4: your runtime's own transcripts are not durable.** On 2026-09-15 M8 measured the
30 agent transcripts behind its landed Ezekiel reviews and found **29 of 30 already 0 bytes**, one surviving. Any
capture design that reads a worker's final message back out of the harness later will silently fail. Copy what you
need into your own durable store *at landing time*, digest the copy, and treat the harness transcript as a
convenience that may already be gone. See §18 for how to label a record whose transcript was empty when you landed it.

New in v2. All three cost M8 something real.

- **Carry the field in which a worker discloses its OWN defect into the durable record.** M8's landing pipeline
  carried reviewers' open questions and compliance self-reports but silently dropped their account of what they had
  done — which is exactly where one execution confessed corrupting 16 of 19 quotations in its own first build. That
  disclosure existed nowhere durable until it was noticed. **A self-disclosed defect that is not in the record reads
  exactly like a defect nobody disclosed.**
- **Mine the free-text uncertainty field; it outperforms the structured fields for finding method problems.** Almost
  every method-level discovery in M8's wave arrived there: the validator holes, a count-provenance trap, the
  cross-passage linkages, a record that reads as stale but is not. Require the field, and read it as data rather than
  commentary.
- **Record which controls have actually FIRED, not only which failures occurred.** M8 accumulated roughly 60 recorded
  failures and had no record of which control had ever stopped anything — so it could not tell which rules were
  load-bearing and which were safe to simplify. When a control catches something, write that down with the same care
  as a defect.
- **Refuse to write a record whose claim you have not verified in a primary source.** M8's recording scripts assert
  their central claim against the landed artefact and abort if it is absent. One such assertion caught a finding about
  to be written from a runtime message rather than from the record.

---

## 11. Verify coverage as SET EQUALITY, not as a count

New in v2. Cheap, and it prevents a bad scare or a real gap.

Check that the set of units in your corpus equals the set assigned to reviewers — both directions, plus duplicates. A
count check passes when one unit is missing and another is duplicated.

**Expect retired ids.** An id absent from the plan may be a unit nobody is reviewing, or an identifier retired by an
earlier repair. These look identical until you check whether the id exists in the corpus at all. M8 hit exactly this
and resolved it in one query: 145 corpus units, 145 assigned, identical sets, no duplicates — the missing id simply no
longer existed.

---

## 12. Do not let the scaffolding eat the scholarship

New in v2, at the project owner's prompting, and it is the least comfortable rule here.

A campaign like this accumulates governance: directives, error classes, learning entries, validators, guards,
receipts. Each defect produces a rule, each rule produces a check, each check produces a tool — **and every tool can
fail, including by failing open.** M8 spent a large part of one working session fixing its own checking machinery
rather than reviewing scripture: a guard that reported "clear" on files eight running agents were holding; launch
messages that stamped a timestamp instead of reading it; the dropped disclosure field in §10.

Those fixes were not wrong — a safety control that fails open during a live wave has to be fixed. But the proportion
was, and the owner was right to say so.

**What to do about it:**

- **Prefer fixing the generator over adding a rule.** The best M8 cures changed a tool so the defect became
  impossible, rather than adding a clause telling someone to be careful.
- **When a control fails, ask whether it can be made unnecessary** rather than reinforced.
- **Budget the meta-work explicitly and watch the ratio.** If a session produced more infrastructure findings than
  textual findings, say so out loud.
- **Triage infrastructure defects.** Fix now only what is actively corrupting the live wave; route the rest to a
  scheduled adjudication.
- **A control nobody runs because it is slow is not a control.** M8's guard took minutes at wave scale, which is how
  controls quietly stop being used. Treat "this check is too slow" as a safety defect.

---

## 13. Open method questions handed forward

The most useful thing one generation gives the next. None were settled with the witnesses M8 had.

**Fixable by better extraction (do this first — it is engineering, not judgement):**

1. **Within-verse mark position.** Unknowable from M8's staged data; several boundary questions turn on it.
2. **Apparatus read-forms.** Carry the source's morpheme separator and the relationship between written and read form
   explicitly, so a reviewer need not infer it.

**Requiring a decision:**

3. **May an apparatus read-form be rendered at all** when it occurs nowhere in the running text, and may it be
   rendered with the separator stripped? M8 collected the site-level instances and routed the decision.
4. **In-span mark disclosure.** Must a unit disclose a received mark falling *inside* its own span, not only at its
   seams? Four independent executions found undisclosed in-span marks. Decide the obligation, then build the check in
   both directions (§9).
5. **Single-witness editorial notes.** Must a unit disclose that layer? Across Ezekiel, 27 of 37 spans carrying it
   mentioned it and 10 did not; two structurally identical units split on it.
6. **Device-class labels that are not morphological claims.** A class labelled by its masculine form containing
   feminine members invites a later pass to "correct" a correct unit. Label by class, or record the exception.
7. **Counts differing between two authoritative sources.** A close-family count of 21 in one artefact and 5 in
   another, each correct for its own definition, will be re-derived and reopened. State in both which definition each
   uses.
8. **Conjectural emendations in glosses.** One unit glossed a byte-exact quotation with a conjectural reading rather
   than what the witness says. Decide whether that is permitted and how it must be marked.

---

## 14. Anti-patterns, stated for a chunker

- **A figure read is not a figure measured.** Never copy a count from prose into a brief, a unit or a report — read it
  from the artefact at build time. M8 shipped a reviewer brief printing two device counts its own pinned inventory
  contradicted; a reviewer caught it and reported rather than acted.
- **A denial hidden behind a comma.** "No formula opens here, and the mark is single-witness" reads as one claim and is
  two. M8 found several where the clause after the comma was false. Give each denial its own sentence.
- **An exclusivity claim without a digit.** "The only verse that…" needs the sweep and the count.
- **A closed list that is not closed.** M8 found an enumeration of a collection's hard seams that omitted four members.
- **Historical bindings at the obvious key.** If a record keeps review-accepted digests at the top level and current
  ones in an additive list, a careful reader reads the top level and concludes the artefact is stale. Put a pointer at
  the historical key. Two M8 reviewers spent effort on this; one was left uncertain, one resolved it correctly.
- **Assuming a runtime "finished" means a deliverable exists.** Check the artefact by its exact path before describing
  the work.

---

## 15. The atlas: difficulty, risk and blast radius

Record three different things about a passage and **never merge them**:

- **MEASURED** — did the blind lanes disagree; what severities landed; does the seam carry device evidence on both
  faces, one, or neither; is the deciding question answerable from the witnesses at all.
- **DEPENDENCY** — what rests on it. Classes seen in Ezekiel: a shared frame governing every sub-unit inside it; a
  census or count claim many units rest on; a convention with book-wide or campaign-wide reach; membership of a
  numbering-divergence zone; a seam shared between adjacent units, each the other's far face.
- **JUDGED** — any hardness or risk rating you assign. Keep it visibly separate. A judgement presented as a
  measurement is the defect this whole method exists to avoid.

**Blast radius is not difficulty, and it is the more useful number.** A conjectural gloss in one unit has radius one; a
convention has radius measured in books. M8 allocated review effort by instinct; ranking by radius would have told it
to settle the mark-direction convention **before** reviewing 145 units that each depend on it (§5).

**Harvest the linkages your reviewers already give you.** They recognise structural recurrence unprompted — one M8
reviewer, deciding a seam, recorded that another cluster's disputed seam was the same configuration and said so for
whoever held it. Those cross-references arrive free in the uncertainty fields (§10). Pull them out; do not rediscover
them a book later.

**Then compare the solutions, not just the problems.** When two passages are linked as related shapes: treated the
**same** is precedent the next such passage should cite; treated **differently** is either a real distinction worth
stating or an inconsistency worth fixing — surface it either way. Across 66 books this is the difference between a
corpus that is locally defensible and one that is internally consistent, and it is the mechanism by which the
twenty-seventh book is genuinely easier than the twenty-sixth.

---

## 16. Your obligations

1. **Read this in your Phase 0.** Required input, not background.
2. **Reconcile with every concurrent generation before mass review** (§1), and keep the divergence register.
3. **If you contradict a rule here, do it deliberately and say so**, with the evidence that changed it.
4. **Update this file at every BOOK close**, not only at campaign close, so your book *n+1* inherits book *n*'s
   lesson. A close whose method record is unchanged states in one line why the book taught nothing — "nothing new" is
   a real answer; an unexamined one is not.
5. **Every rule you add names the generation and book that produced it, and its evidence.**
6. **Re-version rather than overwrite**, and keep a §0 change table, so a later reader can see how the method evolved
   and judge each rule by when and why it appeared.
7. **Carry §13 forward**: answer what you can, hand on what you cannot, precisely enough to be worked on.
8. **Run the proposal loop once per book and adjudicate it before the book closes** (§17). Proposals are logged,
   never self-applied, and each is rated NECESSARY / USEFUL / LOW-REWARD by someone other than its proposer.
9. **Publish your version at campaign close** and name it as the required Phase-0 input for whoever follows.
10. **Give every claim its true tier, and enforce it in a tool rather than in your memory** (§18). Where the normal
    evidence path fails, say which path you actually used and that it is weaker. Never let a degraded record keep
    the shape of an undegraded one.

---

## 17. The method-change proposal loop

New in v3, by owner directive. This is the mechanism that keeps this record improving without letting it bloat, **and
it is the only part of the method that measures the method.**

### How it runs

- **ONE PROPOSER PER BOOK.** At each book close, launch a subagent whose single job is to propose changes to this
  record. It reads **the book's own evidence** — the landed review packets, the findings, the atlas entries, the
  learning entries from this book — and the current method version. It does **not** read the orchestrator's summary of
  the book, because a summary is where the interesting evidence has already been filtered out.
- **IT PROPOSES; IT NEVER APPLIES.** The proposer does not edit this file. It writes proposals to
  `method_change_proposals.jsonl`. This separation is the whole point: a proposer that can edit the method will edit
  the method, and nothing will ever be weighed.
- **EACH PROPOSAL CARRIES**, at minimum: the target section; the change, stated as the text that would appear; the
  **evidence from this book** that prompted it, by exact artefact reference; the **blast radius** if adopted (one unit,
  several, one book, campaign-wide, cross-generation); the **cost of adopting** it, including any tool or brief that
  would have to change; and the proposer's own **necessity estimate with its reasoning**.
- **A CHECKING EXECUTION ADJUDICATES**, not the proposer and not the orchestrator that ran the book. For each proposal:
  **ADOPT / REJECT / DEFER**, plus an independent rating of **NECESSARY / USEFUL / LOW-REWARD**, with reasons. A
  proposal may be correct and still be low-reward; say so rather than adopting it out of politeness.
- **ADOPTED PROPOSALS ENTER THE NEXT VERSION.** Rejected and deferred ones **stay in the log with their reason** — a
  rejected proposal is evidence too, and the next generation should be able to see what was considered and declined
  rather than proposing it again.

### Why this exists, stated honestly

M8 had no such loop. Its method grew by accident: a defect appeared, a rule was written, a check was built, and nobody
ever asked whether the rule had earned its place. By book 26 the governance layer had become large enough that the
project owner asked, reasonably, why the work was so hard (§12). **Neither the growth nor the question could be
answered with data, because nothing was recorded about which rules were worth having.**

### The log is the measurement — use it

Across books, track two rates:

- **Adopt rate.** Very low means the loop is generating noise; narrow the proposer's scope or run it less often.
- **Low-reward rate.** Mostly low-reward means the same. Mostly NECESSARY means the opposite — you are
  under-instrumented, real lessons are arriving only at book close, and the loop should run more often than once a
  book.

This is the ratio §12 demands and M8 could not produce. It is also the evidence a later generation needs in order to
**simplify** safely: a rule that was adjudicated NECESSARY on named evidence can be trusted; a rule nobody ever
weighed cannot be removed *or* relied on.

### Where it fits the three gates

- **Pre-flight** — the open proposal log is read when a wave is designed. A DEFERRED proposal that the wave's own
  evidence would settle should be scheduled deliberately rather than deferred again by default.
- **Mid-flight** — a proposal-worthy observation is written to the log **when it is found**. The once-per-book proposer
  is a floor, not a ceiling; in-flight capture beats reconstruction at close (§10).
- **Post-flight** — adjudication happens before the book closes, and close-gate item 23 fails a close whose proposals
  are unadjudicated.

---

## 18. Say how you know it: provenance tiers, and the ban on implied provenance

Owner directive OW-18, 2026-09-15. Of everything in this record, this is the section most likely to matter to a
reader who distrusts you — which is the reader you are writing for.

**The rule.** Every substantive claim carries how it is known, and never a stronger word than is true:

| Tier | Means |
|---|---|
| **MEASURED** | produced by a tool whose output is in evidence — a digest, a count, a validator run |
| **EXTRACTED** | read programmatically out of a durable artifact that still exists and can be re-read |
| **TRANSCRIBED** | copied by hand or by eye from something *not* durably on disk. Weaker than EXTRACTED because it cannot be re-derived once the session ends |
| **REPORTED** | a worker's or a source's own claim about itself, carried forward but not independently checked |
| **INFERRED** | derived by reasoning from claims of a named tier |
| **ASSUMED** | a working assumption required to proceed, with no evidence behind it |
| **UNAVAILABLE / UNKNOWN** | the evidence does not exist or could not be obtained. A **value**, never a blank, and never quietly replaced by the next-best thing |

**Implication is assertion.** The test is not "did I write a false sentence". It is "would a careful reader draw a
false conclusion from what I wrote and what I left out". A record that is silent about a change in how it was
produced asserts, by keeping the same shape as its neighbours, that nothing changed. Where that is untrue the record
is false, and a half-truth is scored as a false statement rather than a lesser one.

**The positive obligation, which is the part people skip.** Prohibition alone produces vague records. When the normal
evidence path fails, say: which path you actually used, why the normal one was unavailable, what corroboration you
obtained instead, and that the substitute is a weaker tier. **Corroboration does not upgrade the tier.** M8's two
transcribed records each carry a MEASURED digest equal to the transcribed one and are still TRANSCRIBED records.

**Two different facts, and the trap of collapsing them.** M8 got this wrong on the first attempt, so it is written
here as a warning rather than as advice. *How a record was produced* and *whether it is re-derivable today* are
separate claims with separate evidence. M8 first measured only re-derivability, found 29 of 30 transcripts empty,
and labelled 29 records "TRANSCRIBED" — a confident, wrong label, since 28 of them had in fact been extracted from
transcripts that were truncated afterwards. The fix was two fields, each with its own basis: re-derivability is
always MEASURED; how it was produced is MEASURED where an artifact survives, DISCLOSED where the record testifies
against itself, and **REPORTED** where only your own account of your own procedure covers it. That last tier is the
weakest thing in a record and must be named, not smoothed over.

**Enforce it in a tool, not in your memory.** An orchestrator will forget this section at hour nine of a wave.
- The landing tool takes a required capture-carrier argument and **measures** the transcript's byte size; a claim of
  EXTRACTED over an empty or absent transcript is **refused**, not annotated.
- A record claiming the weaker tier must carry that word in its own text, so the tier travels with the record and
  not only with the receipt.
- A tool that cannot represent the weaker tier **is the defect**; fix the tool rather than rounding the claim up.

**It binds the scholar-facing record most of all.** A seam corroborated by a received paragraph mark MEASURED in an
inventory is not written the same way as a seam resting on a reviewer's REPORTED reading. Publishing them in the
same voice tells the reader they are the same kind of thing, and they are not. Unfalsifiable authority over the text
of scripture is exactly what this method exists to prevent.

**It binds workers, not only orchestrators.** A reviewer brief that requires a `checks_not_run` field should treat
its omission as a form problem, not a style note, and the duty extends to any field where a worker could imply a
check it did not run.

**When you find one of your own records wrong, correct it and keep the wrong version on disk**, so the correction is
auditable instead of invisible. M8 kept `primaries_capture_provenance.v1.json` beside its corrected `.v2.json` for
this reason.

---

## Provenance and limits of this version

- Written during M8 / Ezekiel with 22 of 44 dual-blind primary executions landed. Every measured claim traces to a
  landed packet under `M8_fable/sp_durable/Ezek/reviews/` or a finding under `M8_fable/sp_durable/campaign/`.
- **Not verified:** M7's method (none found to inherit); M9's conventions and its ~15 closed books — §1 is written
  *because* that reconciliation has not happened, not as a report of it. Conclusions from Ezekiel's remaining 22
  executions and from Daniel are not yet here.
- The per-book scholar-facing record required by OW-17 is a **different** document with a different reader, generated
  from the landed packets.
- Witness licensing travels with any published quotation: the Hebrew witness (OSHB) and the translation (WEB) carry
  their own attribution terms, which a published record must state.
- **Canonical home:** this file sits under `M8_fable/` because that is where this generation's write authority reaches.
  Its proper home is above any single generation's directory; placing it there is the owner's act, as is publication.
