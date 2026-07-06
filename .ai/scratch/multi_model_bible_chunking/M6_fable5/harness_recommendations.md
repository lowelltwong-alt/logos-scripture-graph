# M6_fable5 — Harness Recommendations for literary_marker_aware_v2

Non-authorizing feedback from a complete 66-book marathon. Companion machine-readable rows:
`grammar_literary_gap_register.jsonl`.

## Where the protocol was strong

1. **Sidecar triad with required_ids enforcement.** Keying low-confidence/frontier/atlas rows to
   `decision_id` and validating presence per book made escalation impossible to forget. Best
   single control in the harness.
2. **Frontier-book rule (Dan/Rev).** Simple, mechanical, effective; every apocalyptic chunk got
   deliberate frontier consideration.
3. **Book-strategy-before-chunks gate.** Forcing a written strategy (with the strong/evidence/
   strategy keyword check) genuinely improved boundary quality on mixed-genre books.
4. **Substrate-first design.** Anchoring starts to substrate versification eliminated the whole
   class of versification errors (Ps 119, Jonah 1:17/2:1, 3John 14 vv, Joel/Malachi chapter
   variance) without reading raw USFM.
5. **Chapter-fallback logging.** For genuine fallback (Proverbs sentence collections) the
   logged-medium_low path worked exactly as intended.

## Where it was vague, rigid, or inadequate

6. **Chapter-coincidence cap is the big rigidity (315 of 474 sidecar rows).** The validator
   treats any span equal to a chapter's full extent on a marker-rich/pilot book as fallback-like
   and demands medium_low. But psalm=chapter, Lamentations poem=chapter, and Job speech=chapter
   are *identities*, not laziness. Consequence: honest high-confidence units are mispriced, and
   sidecars are ~66% noise, burying the 17 real variant spans and 31 theology-pressure spans.
   **Fix:** add a `chapter_coincident_literary_identity: true` chunk field (or evidence tag)
   that, when justified in the book strategy, lets confidence stay high while still emitting an
   atlas row for audit. Distinguish "chapter-only because no finer signal was sought" from
   "unit happens to equal chapter".
7. **Confidence taxonomy conflates boundary-confidence with content-pressure.** Isa 52:13-53:12
   has near-certain boundaries but maximal theology pressure; Mark 16:9-20 has certain boundaries
   and maximal variant pressure. One `confidence` scalar cannot say both. **Fix:** sidecar/chunk
   fields `boundary_confidence` and `content_pressure` (enum), keeping `confidence` as the min
   for compatibility.
8. **No merge-direction signal.** The schema lets a model flag "this could split further" via
   sidecars but has no way to say "this chunk could merge with its neighbor" (Ps 9-10, Ps 42-43,
   Ezra 4 parenthesis). **Fix:** optional `merge_candidate_with: <decision_id>` sidecar field.
9. **Validator false-positive risk in `_is_chapter_rollup`.** Any span textually equal to the
   chapter feature span counts as rollup even when evidence refs show deliberate literary
   judgment. Suggest also requiring the absence of literary evidence tags before the cap bites.
10. **Isolation validator cannot distinguish pre-existing working-tree dirt from agent writes.**
    It failed this run on a one-line owner modification to `comparison/model_agreement_matrix.yaml`
    that predates the session. **Fix:** snapshot forbidden-path hashes at marathon start
    (`t423_pin_substrate.py` could also pin these) and fail only on *changes since pin*; or have
    the runner record a git stash-hash baseline.

## Literature types handled poorly by the current signal set

11. **Unmarked hymns/creeds in prose epistles** — Phil 2:6-11, Col 1:15-20, 1Tim 3:16 (partially
    q-marked), Titus 2:11-14/3:4-7, 1Pet 3:18-22. WEB prints most as prose; the substrate gives
    no poetry signal. Add a curated "candidate embedded hymn/creed" span list to the research
    baseline (evidence-only).
12. **Hidden acrostics** — Nah 1:2-8 has no q markers; Ps 9-10/25/34/37/111/112/145 acrostics are
    invisible (only Ps 119 is culturally famous enough to be protocol-named). Add an acrostic
    inventory sidecar to the baseline.
13. **Refrain-bounded units** — Isa 9:8-10:4 ("his hand is stretched out still"), Amos 4
    ("yet you did not return"), Eccl refrains, Song adjurations. Refrain recurrence is a
    first-class discourse boundary no marker exposes. A Rust refrain-repetition detector
    (n-gram recurrence at verse granularity) would be a high-value substrate addition.
14. **Language shifts** — Ezra 4:8/6:18/7:12-26 and Dan 2:4b-7:28 Aramaic panels are hard
    discourse boundaries absent from the substrate. Strong's H-prefix vs Aramaic lemma ranges
    could be surfaced as a `language_shift` risk flag.
15. **Sentence-proverb collections** — the protocol handles them only via fallback+cap; a
    dedicated `no_internal_boundary_literature` category would name the reality instead of
    treating it as a deficiency.

## Grammar/discourse features missed

16. **Speech-introduction formulae** (wayyomer/"Then X answered"/peri de/"when Jesus finished")
    are my main seam evidence but exist nowhere in the substrate. A formula-detection pass
    (even keyword-level on WEB text) would let validators *check* claimed speech boundaries.
17. **`d` superscription attribution bug/quirk:** superscription markers attach to the *previous*
    psalm's last verse in verse_observations.jsonl (Ps 3's title registers at Ps 2:12; Ps 10,
    which has no title, shows d@18 = Ps 11's). Any future tool using d-position for boundaries
    will be systematically off by one psalm. Verify scanner inter-verse attribution.
18. **WJ runs cross pericope seams** silently (Matt 23-25 continuous). WJ evidence needs
    run-start/run-end exposure, not per-verse counts, to be useful for discourse edges.
19. **Quotation-block edges** (Heb 8:8-12 Jer 31; catenae) — `x` crossrefs mark presence, not
    extent. Quotation-span extents would serve intertext review directly.

## Suggested sidecar fields (beyond #7, #8)

- `versification_sensitivity: [english_hebrew_offset|lxx_order|verse_absent_in_critical_text]`
- `parallel_text_refs` (Kings/Chronicles/Isaiah 36-39, synoptics, Ps 14/53, 2Pet 2/Jude)
- `speaker_attribution_status: none_asserted|marked_editorial|owner_review_pending` (John 3, Song, Rev 22)
- `hymn_or_creed_candidate: true`

## Suggested frontier escalation triggers

- any chunk whose span contains a dossier-listed variant ref (auto-match against the
  textual-variant dossier queue)
- any chunk quoting or quoted-by another canonical book (parallel/quotation pressure)
- speaker-undecided spans in WJ books
- English/Hebrew or MT/LXX versification divergence inside the span

## Suggested atlas feed improvements

- Split feed by concern class (variant / theology / structure / list) so the 315 structural
  cap rows do not bury 17 variant rows.
- Add `expected_cross_model_disagreement: low|medium|high` — my chapter-coincident rows predict
  *agreement*, while proverb-cluster rows predict arbitrary disagreement; the compare harness
  should weight these differently when computing revert signals.

## Prompt/template improvements

- State explicitly in the marathon prompt that psalm/poem/speech units equal to chapters are
  *not* chapter fallback (models may otherwise over-fragment psalms to dodge the cap).
- Provide the digest tooling pattern (per-chapter marker digest) in the template; deriving it
  per-model wastes effort and invites substrate misreads.
- Template `model_manifest.yaml` should include the `research_baseline_manifest_sha256` field
  name (the baseline requires it, the template omits it).
- Branch-per-slot isolation (`scratch/t423-M6-*`) conflicts with running in the owner's live
  checkout when required toolchain hardening is uncommitted; the playbook should say which wins
  (this run: stayed on the owner's branch, writes confined to the model folder, logged here).
