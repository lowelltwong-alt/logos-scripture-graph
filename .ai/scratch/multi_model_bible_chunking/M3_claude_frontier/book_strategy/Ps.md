# Psalms — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Lyric **poetry** (`genre_psalms`): 150 discrete psalms across the Psalter's five books
(1–41, 42–72, 73–89, 90–106, 107–150), each closed by a doxology (41:13; 72:18–19; 89:52;
106:48; and Ps 150 as the whole-book doxology). Dense q1/q2 poetry, `d` superscriptions, `qs`
Selah, and `b` strophe breaks throughout.

## Local marker signals (Rust substrate)
- `d`=138 (superscriptions), `qs`=142 (Selah), q1=2504/q2=2970 (poetic lines), `b`=97
  (strophe/blank), `ms1` (book-division headings). `has_variant_reading` present. `has_footnote`
  textual notes — evidence only. `has_strong_h` — Strong's Hebrew **evidence only**.

## Boundary handling (independent rationale)
- **The psalm is the unit.** Each psalm is chunked whole (superscription + body), because a
  psalm is a self-contained poem delimited by its superscription/`d` marker and doxological or
  Selah structure. This is a literary-form judgment, not chapter fallback.
- **Ps 119 is the exception:** its 176 verses form a 22-letter **acrostic**, so it is split into
  its 22 eight-verse stanzas (aleph … taw), never one block — per the protocol's explicit rule.
- Literature-type guesses distinguish hymn, individual/communal lament, thanksgiving, royal,
  wisdom/torah, penitential, imprecatory, zion, enthronement, historical, songs of ascent
  (120–134), and hallel (113–118; 146–150) where the genre is well established. Genre is a
  guess/evidence label, not authority.

## Strong's / WJ handling
Strong's Hebrew = evidence only. Superscription author-labels (`d`) are editorial evidence,
not authorship or theology authority. `wj_or_red_letter` n/a (OT).

## Low-confidence & frontier escalation triggers
- **Every whole-psalm unit is flagged `medium_low`** and surfaced to all three sidecars: the
  whole-psalm boundary is confident, but per protocol the unit coincides with the chapter and
  its internal **stanza/strophe/Selah** structure is not sub-chunked — a genuine review point.
- Royal/messianic psalms (2; 45; 72; 110), penitential (51), and imprecatory psalms (e.g. 137)
  carry additional theological/ethical review load, surfaced (not encoded) in the sidecars.

## Why this is not silent chapter-only
The psalm-as-unit is the correct literary form (not a lazy chapter default); it is explicitly
flagged with per-psalm evidence, Ps 119 is stanza-split, and genre is classified per psalm.
