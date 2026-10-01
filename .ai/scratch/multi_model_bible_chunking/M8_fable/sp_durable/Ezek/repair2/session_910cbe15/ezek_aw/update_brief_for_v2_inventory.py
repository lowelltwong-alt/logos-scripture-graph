#!/usr/bin/env python3
"""Point the author wave at the v2 inventory, and tell authors exactly what changed in it.

WHY THIS EDIT IS THE REASON THE WAVE WAITED. C2-amended makes the INVENTORY govern counts and list membership.
The v1 inventory's messenger census is 7 where the measured figure is 6; it carries no transport class at all
where the measured class is 33 verses; its recognition-2ms label names a gender the pointing does not resolve;
and it lacks the 64-verse, 21-verse and adonai-recognition lists entirely. An author writing a census figure
from v1 would write a superseded number into a row, and the spot wave would then be checking prose against the
wrong list.
"""
import hashlib
import json
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
BRIEF = EZ / "AUTHOR_WAVE_BRIEF.v1.md"
LOCAL = HERE / "AUTHOR_WAVE_BRIEF.v1.md"
TPL = HERE / "LANE_LAUNCH_TEMPLATE.md"
V2SHA = "356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f"
V1SHA = "0112add3b18927e9d23f09ecb850e3aa1ef9b1220c073063d49a377cf8929142"

ADD = """
---

## 12. THE DEVICE INVENTORY YOU READ IS **v2** — and here is what changed

`ezek_device_inventory.v2.json`, sha256 `%s`, landed as precondition P6. **Read v2, not v1.**
`ezek_device_inventory.json` (v1, sha256 `%s`) is kept on disk and is NOT deleted, but it is
SUPERSEDED for counts and list membership. Under C2-amended the inventory governs those, so a census figure
taken from v1 is a superseded number written into a row.

**What v2 corrects or adds, all MEASURED over the pinned witness:**

| item | v1 | v2 |
|---|---|---|
| messenger chain MT 36:2-36:7 | 7 | **6** — six verses, one occurrence each; MT 36:1 and 36:8 are empty |
| messenger formula shapes | — | **3 distinct shapes** account for all 126 occurrences. MT 21:14 (= web:Ezek.21.9, `כה אמר אדני` + imperative `אמר`) is the **fourth short-form VERSE but the THIRD distinct SHAPE** |
| word-event family labels | "49/41/48" | **five figures**: strict 39, vayehi-any 41, hayah-perfect 7, family total 48, any-form 49. MT 1:3 is in **none** of the three lists, which is why 49 = 48 + 1 |
| adonai-form recognition (D3) | absent | **5 verses**: MT 13:9, 23:49, 24:24, 28:24, 29:16 — all verse-final, three `וידעתם` and two `וידעו` |
| `recognition_formula_2ms` (D4) | 2ms | relabelled **`recognition_formula_2s`**: `וידעת` is 2-SINGULAR and gender-UNRESOLVED. Pointing MEASURED: MT 16:62 and 22:16 feminine; MT 25:7, 35:4, 35:12 masculine. The old key is kept as an alias |
| year-word non-datelines (D5) | 7 | **11**, including MT 39:9 (`שבע שנים`, a plural duration with no month or day term) |
| the 64-verse recognition family | absent | **64**, decomposing disjointly as 28 + 8 + 21 + 5 + 2. Six verses carry `כי אני יהוה` with **no knowing verb** and are what the predicate excludes |
| the 21-verse 2mp set | absent | **21** (`וידעתם כי אני יהוה`), identical to strategy §2a verse for verse |
| transport class (A12-b) | **no class at all** | **33 verses / 46 occurrences** from a stated predicate |

**THE TRANSPORT CLASS NEEDS YOUR CARE, and it is the one item here that is NOT settled.** The strategy's closed
list of 20 is a **strict subset** of the measured 33; membership differs on 13 verses (MT 3:12, 3:14, 37:2, 40:2,
40:3, 40:24, 40:48, 42:15, 43:1, 44:1, 46:21, 47:3, 47:4). Whether the v2 class supersedes the strategy's closed
20 **for rows** is the controlling agent's call and has been routed to it. Until it rules:

- **Do NOT write a transport-class membership claim for any of those 13 verses.** If a row of yours needs one,
  put it in `items_NOT_discharged` with the reason, or `escalations`.
- The other 20 are unchanged and you may rely on them.
- peer_03's four sweep-based findings and peer_10's four transport rows remain **HELD and unscored**; they are
  not in your worklist and you must not invent items for them.

**MT 33:20's sof pasuq is UNAVAILABLE at verse granularity** and no row is scored on it. Do not resolve it, do
not assert it either way, and do not treat the strategy's mention as a measurement.

**One correction to how I briefed P6, recorded because it bears on how much weight to give my figure glosses.**
My P6 brief glossed "the 49/41/48 figures" as the three word-event sub-labels. That mapping does **not**
reproduce — strict is 39 and hayah-perfect is 7. The agent re-derived from the bytes instead of fitting its
measurement to my gloss, which is what the brief asked for and what you should do too. **If a figure I hand you
disagrees with the pinned input, the input wins and you say so.**
""" % (V2SHA, V1SHA)

for p in (BRIEF, LOCAL):
    t = p.read_text(encoding="utf-8")
    if "THE DEVICE INVENTORY YOU READ IS **v2**" in t:
        print("already carries the v2 section:", p.name)
        continue
    # the C2-amended paragraph must point at v2
    old = ("**A12-b** — a class with no verse list in the inventory is not an A12 sweep class. The inventory's "
           "next version\n(P6) gains lists for the 64-verse recognition family, the 21-verse 2mp set, and the "
           "transport class, from stated\npredicates, distinct-checked. **Until those lists land, peer_03's four "
           "sweep-based findings and peer_10's four\ntransport rows are HELD, not scored.** Your worklist will "
           "tell you if a held item has been released.")
    new = ("**A12-b** — a class with no verse list in the inventory is not an A12 sweep class. **P6 HAS LANDED** "
           "as\n`ezek_device_inventory.v2.json`, which gains the 64-verse recognition family, the 21-verse 2mp "
           "set and the\ntransport class from stated predicates, distinct-checked — see section 12 for what "
           "changed and for the one\nunsettled part. **peer_03's four sweep-based findings and peer_10's four "
           "transport rows remain HELD and\nunscored**, because the transport membership question they turn on "
           "is routed to the controlling agent.")
    if old in t:
        t = t.replace(old, new, 1)
    else:
        print("NOTE: the A12-b paragraph did not match exactly in %s; the v2 section below governs" % p.name)
    t = t.rstrip("\n") + "\n" + ADD
    p.write_text(t, encoding="utf-8", newline="\n")
    print("updated %s -> sha256 %s (%d lines)"
          % (p.name, hashlib.sha256(p.read_bytes()).hexdigest(), len(t.splitlines())))

# the lane launch template's input table must name v2 with its digest
t = TPL.read_text(encoding="utf-8")
old_row = ("| `ezek_device_inventory.json` | `0112add3b18927e9d23f09ecb850e3aa1ef9b1220c073063d49a377cf8929142` "
           "| counts and list membership (C2-amended: the inventory governs these) |")
new_row = ("| `ezek_device_inventory.v2.json` | `%s` | **counts and list membership — READ v2** (C2-amended: "
           "the inventory governs these). See brief section 12 |\n"
           "| `ezek_device_inventory.json` | `%s` | v1, SUPERSEDED for counts; kept on disk, cite only to show "
           "what changed |" % (V2SHA, V1SHA))
assert t.count(old_row) == 1, "the template's inventory row did not match exactly"
t = t.replace(old_row, new_row, 1)
brief_sha = hashlib.sha256(BRIEF.read_bytes()).hexdigest()
t = t.replace("`2a30eb07698b5a80fc6a30621f91ef2694b379115a939dffafa34ba07b73426e`", "`%s`" % brief_sha)
TPL.write_text(t, encoding="utf-8", newline="\n")
print("template updated; brief digest in the template is now %s" % brief_sha)
