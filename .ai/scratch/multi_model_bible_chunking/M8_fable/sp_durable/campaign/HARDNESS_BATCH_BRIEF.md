# HARDNESS BATCH BRIEF — OW-6b book-hardness scoring (claude-fable-5-1, one agent per batch)

You are scoring one BATCH of the campaign's remaining books against the owner's hardness rubric. A separate
consolidating agent sets the threshold, applies it uniformly across every batch, and rules the final HARD or
STANDARD track. You produce scores and evidence; you do not set the threshold and you do not assign a track.

This split exists because a single agent asked to score all 42 books at once exceeded its output limit. Keep
your evidence substantive but tight: a reader must be able to check each claim, not admire it.

## THE OWNER'S WORDS THAT CREATE THIS WORK (verbatim, binding)

"also fable shoudl be teh controloing agent and extra scruiney over the hardest books we anticpate doing
this to like revelation, daniel, research which those are thit lots hor hard greek or hebrew translations
lots of hard types of litature or profacies or connections, or passages the Church struggles withor
theChurch disagrees about."

## THE RUBRIC (score each book 0-3 on each criterion)

1. **translation_difficulty** — hard Greek or Hebrew. Textual-critical density (ketiv/qere, variant
   traditions, Septuagint divergence, Aramaic sections), hapax legomena and disputed lexemes, corrupt or
   contested passages, disputed verse divisions or numbering differences between traditions.
2. **literature_type_difficulty** — many or difficult genres in one book: apocalyptic, oracle, vision
   report, acrostic, wisdom, legal, epistolary argument, hymn, court narrative, genealogy, mixed prose and
   poetry with unmarked seams.
3. **prophecy** — predictive, apocalyptic and oracular material whose unit boundaries turn on interpretive
   judgment rather than on text signals.
4. **connections** — dense intertextual dependence: quotation of and allusion to other books, shared source
   material, parallel accounts, catchword chains across books, material a chunk boundary can sever.
5. **ecclesial_contestedness** — passages the Church struggles with, or where Christian traditions disagree.
   Report the disagreement as a NEUTRAL FACT OF RECEPTION: who reads it how, and what turns on it. You are
   classifying difficulty for a boundary-drawing task. You never adjudicate a theological dispute, never
   take a side, and never characterise a tradition's reading as wrong.

SCALE: 0 = not a factor. 1 = present but routine. 2 = substantial, will shape the chunking. 3 = severe, a
principal driver of difficulty for this book.

## WHAT EACH SCORE MUST CARRY

Evidence a reader can check: name the phenomena and where they sit, not a general impression. "Dense
textual-critical apparatus" is not evidence; naming the kind of variant and the stretch it clusters in is.
Where your knowledge is uncertain, say "uncertain" inside the evidence and score CONSERVATIVELY, meaning
UPWARD toward more scrutiny, never downward on a guess.

Also give, per book:
- **boundary_risk** — one or two sentences on what a chunk boundary could get WRONG in this book
  specifically. This is the operational payload; the scores are the summary.
- **extra_scrutiny_focus** — the regions or phenomena a hard track should watch, if this book turns out
  hard. Name them even if you think the book is standard; the consolidator decides the track.

## GOVERNANCE

Worktree READ-ONLY; never run git. Your ONLY write is your assigned batch file. Private scratch only in a
uniquely-named subdirectory of YOUR OWN session scratchpad. Do not read another batch agent's output, any
other model's lane, or any A/B or comparison data. Effort as ordered; ORDERED, NOT VERIFIED (recorded
honestly). Candidate-only, NON-AUTHORIZING research: you change no corpus and close no book.

## OUTPUT (your assigned file in SP\campaign\)

{"schema":"m8_hardness_batch.v1","attempt_id":"<given>","model":"claude-fable-5-1","batch":"<given>",
 "books":[{"book":"<code>","scores":{"translation_difficulty":N,"literature_type_difficulty":N,"prophecy":N,
   "connections":N,"ecclesial_contestedness":N},"total":N,
   "evidence":{"translation_difficulty":"...","literature_type_difficulty":"...","prophecy":"...",
     "connections":"...","ecclesial_contestedness":"..."},
   "boundary_risk":"...","extra_scrutiny_focus":["..."],
   "uncertainty":"<anything you could not verify, or empty>"}],
 "batch_digits":{"books":N,"total_range":[min,max]},
 "self_check":"<one line>"}
FINAL MESSAGE = raw JSON only (no prose, no fences): {"attempt_id":"...","batch":"...","books":N,"output":"SP/campaign/<file>"}
