# BIBLE CHUNKING METHOD — v1

**Reader: the next chunker.** Not a scholar reading one book, and not an orchestrator running an agent mesh. If you
are about to chunk a book of the Bible into literary units, this is what the previous generation learned, why, and
what it could not settle.

**Authority:** owner directive OW-17 amendment (a), 2026-09-15, recorded verbatim in
`M8_fable/ERROR_PATTERN_LEDGER.v1.md` and as row `OW-17-a` of `M8_fable/error_pattern_ledger.v1.jsonl`. Close-gate
item 21 binds every book close and every campaign close to updating this file.

**This version was written by:** generation **M8**, during Ezekiel (book 26 of 66), with 22 of 44 dual-blind primary
review executions landed. It is v1 because *no such document existed to inherit* — see §1.

---

## 1. The origin gap, stated plainly

M8's Phase 0 had no inherited method record. Earlier generations left an orchestration playbook (how the agent mesh
runs) and a long error ledger (what went wrong and in which class), but **nothing that told a chunker how to decide a
boundary well.** Every generation re-derived the method from the text and from its own mistakes.

This document exists so that stops. It is not a log of what happened to us; it states what you should *do*, with the
evidence behind each rule so you can judge it rather than inherit it blindly.

**M8 makes no claim to carry M7's lessons.** This generation did not read M7's method, because there was none to read.
If you find one, reconcile it with this and say which rules survived.

---

## 2. What a chunk is

A chunk is a **literary unit**: a stretch of text that begins and ends where the text itself marks a beginning and an
end, not where a chapter, a verse, a translation paragraph, or a convenient length suggests.

Two consequences that cost M8 real work to learn:

- **A chunk boundary is a claim about the text, and it needs evidence on BOTH faces.** The close of one unit and the
  onset of the next are two separate claims. A seam argued from one side only is under-evidenced even when it is right.
- **A boundary can be right for the wrong reason.** This is the dominant finding of M8's Ezekiel review: across 22
  independent review packets covering 145 proposed units, the *spans* held up almost everywhere, while the *stated
  grounds* failed repeatedly. Reviewers kept the boundary and rejected the reason in the large majority of challenges.
  If you only check whether boundaries look right, you will certify a corpus whose reasoning is unreliable.

---

## 3. Evidence that licenses a boundary

Ranked, strongest first. The names are generic on purpose; each book's own devices go in that book's strategy.

1. **Structural formulae of the book's own vocabulary.** In Ezekiel: the word-event formula, the messenger formula,
   the utterance signature, the recognition refrain, the direct-address vocative. Establish the *census* of every such
   formula before reviewing anything — the verse list, not the count alone.
2. **Closural refrains.** A unit that ends on the book's close-grade device is far better evidenced than one that
   merely stops.
3. **The received paragraph layer** (in the Hebrew: *petuchah* / *setumah*). Corroborating, not deciding. See §4.
4. **Content and participant structure** — inclusio, addressee change, genre shift, named participants entering and
   leaving.
5. **Syntax.** A construction that spans a proposed seam is evidence against it. M8 found a proposed close that divided
   a temporal frame from the main clause it governs.

**Never licensing on its own:**

- **Translation layout.** Paragraphing, punctuation, capitalisation and poetry line breaks in a translation are the
  translators' editorial decisions, not the source's. M8 carries this as its own error class because an earlier
  generation's corpus was damaged by it. Check it positively: list where the translation breaks, list where your seams
  fall, and show they are independent.
- **Chapter and verse numbers.** Medieval and later apparatus.
- **Length or balance.** A seven-verse unit beside a fourteen-verse unit is not a problem to fix.

---

## 4. The received paragraph layer: a convention that will bite you

**A mark is recorded ON the verse it FOLLOWS.** A *setumah* recorded at verse 20 marks the division *after* verse 20 —
between 20 and 21.

M8 found rows across three separate clusters that credited such a mark as corroborating *that same verse* as their own
**onset**. That reads the mark's direction backwards and makes it interior to the span rather than front-seam evidence.
In one cluster the *same* mark was read one way by a row and the opposite way by the adjacent row. Both lanes of the
dual-blind pair found this independently wherever both ran.

**What to do:** state the convention explicitly in your brief, and check every mark-based claim for direction, not just
for existence. Ask of each: does this mark fall at the seam the row claims, or one verse off?

**A limit to record, not to paper over:** M8's staged mark data carries no *within-verse* position. Where a mark sits
relative to a mid-verse formula is therefore unknowable from the staged files, and several reviewers correctly declined
to decide questions that turned on it. If your extraction can carry within-verse position, carry it — it would have
settled at least three open questions in Ezekiel.

---

## 5. Witnesses and quotation discipline

This is where M8 was bitten hardest, twice, and where its one control with *proven* effect lives.

- **Quote by copying, never by typing.** Slice the exact substring out of the witness file programmatically. Do not
  retype, re-point, add or strip an accent, or construct an apparatus notation the file does not itself contain.
- **Verify before writing, mechanically.** Combining marks and accents are invisible to the eye. One M8 reviewer
  reported an accent difference from visual inspection that programmatic collation disproved; another produced three
  false quotation failures from a parser error it then found and fixed.
- **Re-check the FINISHED artefact against the source before returning, and report the count checked.** This is the
  rule that worked. An early M8 execution fabricated a ketiv/qere composite — merging fragments of two words and
  substituting one accent — with a *correct* conclusion resting on invented evidence. The rule written in response
  caught the same defect class three clusters later, inside another execution's own first build, which had corrupted
  accents in **16 of 19** runs. It was caught *before return*, root-caused to hand-authored escape sequences, and cured
  by making the generator slice from the witness and refuse to write unless every slice collates.

  **Generalise the shape, not the topic:** a mandated mechanical re-check of the finished artefact against its source,
  with the count reported in the deliverable. An agent cannot satisfy that by intending to be careful; it has to run it,
  and the reported count makes an omission visible.

- **A correct conclusion on fabricated evidence is worse than a wrong conclusion**, because it survives review on its
  conclusion. Check evidence independently of verdicts.
- **Name a variant site rather than rendering it** when the form is apparatus-only. "The unpointed written form at X" is
  precise and safe.
- **Apparatus read-forms frequently do not occur in the running text at all.** In one Ezekiel cluster, all six
  ketiv/qere sites had read-forms absent from their own verse's running text. Decide once, campaign-wide, whether
  rendering them is sanctioned, and record the decision — M8 left this open (§8).

---

## 6. Numbering divergence between witnesses

Where two witnesses number differently, **every reference in that zone must carry both numbers, in prose as well as in
structured fields.** Ezekiel has such a zone: MT 21:1–5 = WEB 20:45–49 and MT 21:6–37 = WEB 21:1–32, with the two
systems identical in every other chapter.

Build the offset map as a Phase-0 artefact and make the dual-reference rule a hard gate with a mechanical check. M8's
reviewers passed this cleanly once it was stated; the cost of *not* stating it is a corpus whose references silently
mean different verses in different rows.

---

## 7. Review design: what actually found things

**Two independent reviewers per unit group, blind to each other, with different lenses and different reading orders.**
M8 used a literary-form lane and an original-language lane. Full coverage, no sampling.

What this bought, measured:

- **Independent convergence on real defects.** Both lanes separately found the same ordinal error in a formula census;
  the same false lexical-exclusivity claim; the same mark-direction inversions; the same absent messenger formula.
- **One boundary change that a single reviewer would not have delivered.** Both lanes independently proposed cutting at
  the same verse, and reached it by *different* evidence — one from device-class analysis, one from the paragraph layer
  plus the observation that the corpus already cut on that same device elsewhere on weaker evidence. Two routes, one
  answer.
- **Genuine disagreements, delivered already argued.** On one unit both lanes found the *same* false ground, both rated
  it high, and reached **opposite remedies** — one keep, one cut. That is the most valuable output of the design: a real
  open question handed up with both cases made from the bytes, instead of one confident answer with no sign the other
  side existed.

**Keep the lanes genuinely blind.** Neither reviewer may see the other's output, the adjudications, the earlier repair
orders, or any transcript. The pair is worth nothing if either sees the other. M8 also gave the lanes deliberately
different reading orders so they would not converge by route.

**Make a validator's flag a question, not a verdict.** M8 required each reviewer to *answer* every automated flag on its
rows — genuine, or false positive with a reason — which converted a flag list into decisions and surfaced several
validator defects.

---

## 8. Open method questions handed forward

The most useful thing M8 can give you. None of these were settled with the witnesses M8 had.

1. **Apparatus read-forms.** Is rendering a ketiv/qere read-form a sanctioned corpus class when the form occurs nowhere
   in the running text? And is rendering it with the source's morpheme separator stripped acceptable? M8 collected the
   site-level instances and routed the decision; it did not decide it.
2. **Within-verse mark position.** Unknowable from M8's staged extraction. Several boundary questions turn on it. Fix
   this in extraction if you can.
3. **In-span mark disclosure.** Must a unit disclose a received paragraph mark that falls *inside* its own span, not only
   at its seams? M8's automated check only ever looked behind a unit's onset, and four independent executions found
   undisclosed in-span marks it could not see — one of which cost a confidence level. Decide the obligation, then build
   the check in both directions.
4. **Single-witness editorial notes.** Must a unit disclose that layer? Across Ezekiel, 27 of 37 spans carrying it
   mentioned it and 10 did not, and two structurally identical units split on it.
5. **Device-class labels that are not morphological claims.** A category labelled by its masculine form containing
   feminine members invites a later pass to "correct" a correct row. Either label by class or record the exception.
6. **Counts that differ between two authoritative-looking sources.** A close-family count of 21 in one artefact and 5 in
   another, both correct for their own definition, will be re-derived by a later lane and reopened. Where two artefacts
   carry different figures for a similar-sounding class, say in both which definition each uses.
7. **Conjectural emendations in glosses.** One Ezekiel row glossed a byte-exact splice with a conjectural reading
   rather than what the witness says. Decide whether a gloss may carry a conjecture beside a quotation, and if so how it
   must be marked.

---

## 9. Anti-patterns, stated for a chunker rather than as error classes

- **A figure read is not a figure measured.** Never copy a count from prose into a brief, a row or a report. Read it
  from the artefact at build time. M8 shipped a reviewer brief printing two device counts that its own pinned inventory
  contradicted; a reviewer caught it and reported it rather than acting on it.
- **A denial hidden behind a comma.** "No formula opens here, and the mark is single-witness" reads as one claim and is
  two. M8 found several such denials where the clause after the comma was false. Make each denial its own sentence.
- **An exclusivity claim without a digit.** "The only verse that…" needs the sweep and the count, or it will be false
  somewhere.
- **A closed list that is not closed.** M8 found an enumeration of a collection's hard seams that omitted four members.
- **Historical bindings at the obvious key.** If a record keeps accepted-at-review digests at the top level and current
  ones in an additive list, a careful reader will read the top level and conclude the artefact is stale. Put a pointer
  at the historical key. Two M8 reviewers spent effort on this; one was left uncertain and one resolved it correctly.

---

## 10. Your obligations to the generation after you

1. **Read this file in your Phase 0.** It is a required input, not background.
2. **If you contradict a rule here, do it deliberately and say so**, with the evidence that changed it.
3. **Update it at every BOOK close, not only at campaign close** — so book *n+1* of your own campaign inherits book
   *n*'s lesson. A close whose method record is unchanged must state in one line why the book taught nothing. "Nothing
   new" is a real answer; an unexamined one is not.
4. **Every rule you add names the generation and book that produced it, and the evidence behind it.**
5. **Carry §8 forward**: answer what you can, and hand on what you cannot, stated precisely enough to be worked on.
6. **Publish the next version at your campaign close and name it as the required Phase-0 input for whoever follows.**

---

## Provenance and limits of this version

- Written during M8 / Ezekiel with 22 of 44 dual-blind primary executions landed. Every measured claim above traces to a
  landed review packet under `M8_fable/sp_durable/Ezek/reviews/` or to a finding under
  `M8_fable/sp_durable/campaign/`.
- **Not verified:** M7's method (none was found to inherit). Conclusions from the remaining 22 Ezekiel executions, and
  from Daniel, are not yet in this file.
- The per-book scholar-facing record required by OW-17 is a *different* document with a different reader, generated from
  the landed packets.
- Witness licensing travels with any published quotation: the Hebrew witness (OSHB) and the translation (WEB) carry
  their own attribution terms, which a published record must state.
- **Canonical home:** this file sits under `M8_fable/` because that is where this generation's write authority reaches
  (OW-11). Its proper home is above any single generation's directory; placing it there is the owner's act.


---

## 11. The atlas: difficulty, risk and blast radius (OW-17 amendment (b))

Added to this method record by owner directive on 2026-09-15. It is the axis that makes everything above compound.

**Record three different things about a passage and never merge them:**

- **MEASURED** — did the two blind lanes disagree about it; what severities landed on it; does its seam carry device
  evidence on both faces, one, or neither; is the deciding question answerable from the witnesses at all.
- **DEPENDENCY** — what else rests on it. Classes seen in Ezekiel: a shared frame governing every sub-unit inside it; a
  census or count claim many units rest on; a convention with book-wide or campaign-wide reach; membership of a
  numbering-divergence zone; a seam shared between adjacent units where each is the other's far face.
- **JUDGED** — any hardness or risk rating you assign. Keep it visibly separate. A judgement presented as a measurement
  is the defect this whole method is built to avoid.

**Blast radius is not difficulty, and it is the more useful number.** A conjectural gloss in one unit has radius one. A
convention — mark direction, apparatus read-form rendering, in-span mark disclosure — has radius measured in books.
M8 allocated its review effort by instinct; ranking by blast radius would have told it to settle the mark-direction
convention *before* reviewing 145 units that each depend on it. **Decide the widest-radius questions first, and spend
your second opinions there.**

**Harvest the linkages your reviewers already give you.** M8's reviewers spontaneously recognised structural
recurrence — one, while deciding a seam, recorded that another cluster's disputed seam was the same configuration and
said so for whoever held it. Those cross-references arrive free in the uncertainty fields. Pull them out and make them
first class; do not rediscover them a book later.

**Then compare the solutions, not just the problems.** When two passages are linked as related shapes:

- treated the **same** → that is precedent, and the next passage of that shape should cite it;
- treated **differently** → either a real distinction worth stating, or an inconsistency worth fixing. Surface it
  either way.

Across 66 books this is the difference between a corpus that is locally defensible and one that is internally
consistent. It is also the mechanism by which the twenty-seventh book is genuinely easier than the twenty-sixth.
