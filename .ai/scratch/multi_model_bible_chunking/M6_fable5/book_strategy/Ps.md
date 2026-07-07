# Ps — M6_fable5 book strategy (literary_marker_aware_v2)

- **Selected strategy:** one chunk per psalm. The individual psalm is the canonical
  liturgical/literary unit; subdividing ordinary psalms into stanzas would fragment liturgical
  integrity, and merging psalms would cross superscription boundaries. The single exception is
  **Ps 119**, chunked as 22 acrostic stanzas of 8 verses (aleph-taw), per protocol and per the
  acrostic evidence itself.
- **Literature type / mixed genre:** psalm poetry throughout (q1/q2 on nearly every verse):
  laments, hymns, thanksgivings, royal psalms (2; 45; 72; 110), wisdom/torah psalms (1; 19B; 37;
  119), historical recitals (78; 105; 106; 136), acrostics (9-10; 25; 34; 37; 111; 112; 119; 145),
  songs of ascents (120-134), and the five-book doxology frame (41:13; 72:18-20; 89:52; 106:48;
  146-150 as closing hallel).
- **Substrate markers considered:** `q1/q2` poetry density; `d` superscriptions; `qs` Selah
  markers; `b` stanza breaks. **Substrate quirk found:** `d` markers are attributed to the last
  verse of the *preceding* psalm (e.g., Ps 3's title registers at Ps 2's final verse; Ps 10, which
  has no Hebrew title, shows d@18 = Ps 11's title). Logged for the grammar/literary gap register;
  superscription evidence used at chapter level only.
- **Strong's/Hebrew metadata:** evidence-only; Selah and musical terms are performance evidence,
  not boundary authority; `strong_or_hebrew_tags_used: false`.
- **Expected low-confidence regions:** every whole-psalm chunk coincides with a chapter and is
  marker-rich, so the protocol caps all ~149 of them at medium_low even though psalm-as-unit
  confidence is genuinely high — this rigidity is the single largest sidecar driver in this
  marathon and is reported in harness_recommendations.md. Genuinely uncertain seams: Ps 9-10
  (single acrostic split across two chapters), Ps 42-43 (one lament with shared refrain), and the
  Ps 14/53 doublet (parallel-text pressure).
- **Chapter-only fallback:** not applicable — psalm units are chosen on literary grounds, not as
  fallback; the chapter coincidence is an artifact of psalm=chapter identity.
- **Frontier/atlas expectations:** rows for every capped psalm (automated), with the 9-10 and
  42-43 join questions and the 14/53 doublet as the real review targets; Ps 119 stanzas carry
  high confidence on acrostic evidence.
- **Independent boundary rationale:** psalm boundaries follow the canonical psalter division and
  superscription frames; Ps 119 stanza starts every 8 verses (1,9,17,...,169) follow the acrostic;
  no template span or other model folder used.
