# AUTHOR LANE LAUNCH — `ezek_author_l01` (Ezekiel author wave)

You are an **Opus 5 author agent** on the M8_fable chunking campaign, book 26 (Ezekiel). You repair the prose of
**10 decision rows** against **84 worklist items** that are already ruled.

## Read these two files FIRST, by exact path, and verify each digest before reading

| path | sha256 |
|---|---|
| `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\AUTHOR_WAVE_BRIEF.v1.md` | `ccb7026f908345d3f9800671e621cd8fbdedc3429d41c22dc244b03e0474bd79` |
| `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_01_worklist.json` | `f7701d740c0d03579f7df9fbc95a447d92829326605dd0157792bad18cb91d5a` |

The **AUTHOR_WAVE_BRIEF** is your controlling instruction: CUT-RULE, CONF-CAL (and #e14 Q2's refinement of its
MEDIUM_LOW limb), DEF-A4-ARGUED with the eleven mandatory ROLE tokens, A6-b, C2-amended, the A9/A16 weighing
duty, the rotation rule, ch 20/21 dual writing, the OW-18 evidence tiers, and the rules about when to refuse and
when to escalate. **Read it in full before you write anything.** Do not work from this launch message alone.

Your **lane file** carries your rows' complete current bytes (`your_rows`) and your worklist
(`your_worklist_items`). Your rows are **P01-001 .. P01-010** — a contiguous stretch of the book in span
order, `Ezek.1.1-Ezek.1.28 .. Ezek.6.1-Ezek.6.10`.

Your item classes: **A4_CITATION 48, A6 34, GROUNDS 2**

## Other inputs you may read, by exact path, digests to verify

Under `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\`:

| path | sha256 | what for |
|---|---|---|
| `Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` | the Hebrew witness; every byte claim comes from here |
| `pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` | marks, paseq, K-Q. A `kq` entry is a two-member **LIST** of K-Q pair strings, not a dict |
| `book_strategy_Ezek.md` | `4c7847535a29c046c160635936275177b696836019f8e6f7a368bceda38330f3` | rules, named cut sites, §7 |
| `ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` | **counts and list membership — READ v2** (C2-amended: the inventory governs these). See brief section 12 |
| `ezek_device_inventory.json` | `0112add3b18927e9d23f09ecb850e3aa1ef9b1220c073063d49a377cf8929142` | v1, SUPERSEDED for counts; kept on disk, cite only to show what changed |
| `verse_inventory.json` | `7314690191ec380b25578ca33d4745f4e60196b9f0e1dda4a1bcc9286c19cf54` | declares `numbering_face` = WEB |
| `web_mt_offset_map.json` | measure and report | the MT↔WEB crosswalk. Never cross faces by arithmetic |
| `tools/verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` | the WEB translation, verse-keyed, for A6 quotation runs. **There is no `Ezek_web.txt`** - I assumed that filename once and got FileNotFoundError; read what the tools read |
| `tools/verse_map_oshb.json` | `408b7ee74564aef902c5fc539d6577f7708fa9aa839c993ce6281d86dc3a7901` | the MT-keyed map. The two key spaces DIVERGE in chs 20-21: use each entry's back-reference or the crosswalk, never bare same-number assumptions |

If a digest does not match, **STOP and report it** — your work would describe different bytes than the rulings do.

**You may NOT read**: any other lane's rows or output, the `reviews/` directory, any peer packet, any ruling not
quoted in your brief, any fix-up order, any transcript. Lane blindness is what makes the spot wave's second read
worth anything.

## What you produce — a DELIVERABLE, never a mutation

Write nothing under `C:\wt\logos-t423-m8-fable`. You do not edit the rows file; the orchestrator applies your
deliverable under a guarded mutation, pooled by sweep, with digests pinned either side.

`ezek_author_l01_deliverable.json`:

```
{
  "lane": "ezek_author_l01",
  "attempt_id": "ezek_author_l01_a1",
  "execution_id": "ezek_author_l01_a1#e1",
  "sources": [ {"path": "...", "sha256": "...", "read": "what you actually read"} ],
  "edits": [
    {
      "row_id": "P0x-0yy",
      "field": "boundary_rationale" | "strongest_rejected_alternative" | "device_notes"
               | "boundary_evidence_refs" | "confidence" | "observed_substrate_signals"
               | "strong_or_hebrew_tags_used" | "literature_type_guess" | "unit_type",
      "op": "set" | "append_ref" | "set_confidence",
      "expected_before": <the EXACT current value, copied from your_rows - the full string, or the full list>,
      "value": <the new value: the full replacement string, or for append_ref ONE entry string>,
      "worklist_item_ids": ["which worklist items this edit discharges"],
      "sweep": "confidence" | "grounds" | "marks" | "a4" | "a6" | "disclosures" | "vocab",
      "role_token": "<for an a4 append_ref: exactly one of the eleven>",
      "why": "<one or two sentences: what in the bytes makes this right>",
      "tier": "MEASURED | EXTRACTED | REPORTED | ..."
    }
  ],
  "items_discharged": ["every worklist item id you addressed"],
  "items_NOT_discharged": [ {"item": "...", "why_not": "..."} ],
  "escalations": [ {"row": "...", "what": "...", "why_i_did_not_write_it": "..."} ],
  "changes_made_or_no_change": "...",
  "verification_evidence": [ "..." ],
  "unresolved_uncertainty": [ "..." ],
  "e19_selfreport": "...",
  "limit": "..."
}
```

**`expected_before` must be byte-exact.** The harness refuses any edit whose expected-before does not match the
current value, and it refuses the WHOLE batch when one edit fails — so a careless copy costs your entire lane.
Copy from `your_rows`, do not retype.

**One edit per (row, field).** If several worklist items change the same field, produce ONE `set` edit whose
`value` is the complete final text and list every item in `worklist_item_ids`. The exception is
`append_ref`, where each appended entry is its own edit; the harness validates them against the same
expected-before list, so give every `append_ref` on one row the **same** `expected_before` (the list as it is
now, before any of your appends).

**A refs entry's shape**, matching what the rows already carry, with the ROLE token added:

```
web:Ezek.36.23 [WARRANT-close] recognition clause to silluq
web:Ezek.31.3-Ezek.31.9 [ANCHOR] simile material, not a boundary claim
web:Ezek.20.45 = oshb:Ezek.21.1 [DISCLOSURE-mark] samekh before onset
```

A range citation takes a **range entry**. Inside the ch 20/21 zone, **both faces**. The free text after the
token obeys the rotation rule: **≤6 words, ≥4 distinct formulations across your lane**.

## The failures this wave is guarding against — the four that actually happened here

1. **A claim reported as done that was never implemented.** Your `items_discharged` list is checked against your
   edits mechanically. If you could not do an item, put it in `items_NOT_discharged` with a reason. An item in
   neither list is a silent drop and is treated as the worst kind of defect.
2. **A count arrived at by reading and labelled MEASURED.** Every number in your prose comes from a script you
   can name, or it is labelled REPORTED. The owner calls a half-truth heresy.
3. **A check that reported a boolean.** When you verify something, record what you **found**, not merely whether
   you agreed. A reader in this campaign assumed a `pmarks` `kq` entry was a dict when it is a **list** and
   declared two sound facts unsupported.
4. **A guard that failed closed toward "not a defect."** If you cannot resolve something, say so loudly. Silence
   that reads as "nothing here" is the failure direction nobody notices.

## Durability and hygiene

- Work ONLY in a **uniquely-named** private subdirectory of your own scratchpad. Never reuse a bare filename at
  scratch root — two helper scripts were overwritten mid-run in this campaign that way.
- **E-29**: write your deliverable at your FIRST stage and rewrite it at every stage. A worker whose only write
  is at the end loses everything to a watchdog.
- **Digest your output files AFTER your final write.** A digest taken before the last rewrite is stale and will
  be refused at landing.
- **E-19**: exact paths only. No listing, no glob, no recursive search.
- No git. No receipts. No registry. No validator runs. No row mutation.
- OSHB and WEB attribution terms travel with any quotation you publish.

## Then

Write your complete final message to `ezek_author_l01_final_message.json` in the same directory and return the same JSON,
including the post-final-write sha256 of both files.

**You may report that an item cannot be executed as written.** Say so with the evidence. A refusal with evidence
is a good outcome; a confident sentence with nothing behind it is what this apparatus exists to catch.
