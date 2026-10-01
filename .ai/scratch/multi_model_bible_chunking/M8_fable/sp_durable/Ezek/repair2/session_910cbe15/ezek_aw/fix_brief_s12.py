#!/usr/bin/env python3
"""Correct the author brief's MT 33:20 sentence, which forbade an assertion the evidence supports.

I wrote, in section 12: "MT 33:20's sof pasuq is UNAVAILABLE at verse granularity and no row is scored on it.
Do not resolve it, do not assert it either way, and do not treat the strategy's mention as a measurement."

Minutes earlier I had recorded, in queue E13-67, that pmarks NAMES MT 33:20 explicitly with a finding and a
status, that what is UNAVAILABLE is INDEPENDENT VERIFICATION rather than the name, and - in my own words - that
"#e13's wording collapses that distinction". Then I collapsed it. An UNAVAILABLE that is really an UNVERIFIED
forbids exactly the assertion the evidence supports, which is a half-truth in the strongest sense OW-18 means.

Lane 05 was handed a ruled item ordering the opposite of my brief. It carried the RULED ORDER, cited the pmarks
key, and told me to fix this before another author agent read it. That is the correct precedence and the correct
escalation, and it is the reason this edit exists.
"""
import hashlib
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
TARGETS = [EZ / "AUTHOR_WAVE_BRIEF.v1.md",
           Path(__file__).resolve().parent / "AUTHOR_WAVE_BRIEF.v1.md"]

OLD = ("**MT 33:20's sof pasuq is UNAVAILABLE at verse granularity** and no row is scored on it. Do not "
       "resolve it, do\nnot assert it either way, and do not treat the strategy's mention as a measurement.")

NEW = """**MT 33:20's sof pasuq — read this carefully, because my first version of this paragraph was wrong.**

What is MEASURED: `pmarks_Ezek.json` NAMES the verse, at
`arithmetic_anomalies_resolved.sof_pasuq_1272_for_1273_verses.verse = "Ezek.33.20"`, with a finding and a status
beside it. What is UNAVAILABLE is **independent verification** — the pinned witness carries no sof pasuq
anywhere, at any verse, so it can neither confirm nor deny the anomaly. Those are different things, and an
earlier version of this paragraph said the FACT was unavailable and forbade asserting it. That forbade exactly
the assertion the evidence supports.

So: **no row is scored on it**; where an order requires the fact, cite the pmarks key and label it EXTRACTED
from pmarks with verification UNAVAILABLE; never present the strategy's mention as a measurement; and do not
attempt to resolve the anomaly itself.

If a work order and this brief ever disagree, **the ruled order wins** and you say so in your escalations — one
lane has already had to do exactly that here, and it was right."""

for p in TARGETS:
    t = p.read_text(encoding="utf-8")
    if "my first version of this paragraph was wrong" in t:
        print("already corrected:", p.name)
        continue
    n = t.count(OLD)
    assert n == 1, "expected 1 occurrence in %s, found %d" % (p, n)
    t = t.replace(OLD, NEW, 1)
    p.write_text(t, encoding="utf-8", newline="\n")
    print("corrected %s -> sha256 %s (%d lines)"
          % (p.name, hashlib.sha256(p.read_bytes()).hexdigest(), len(t.splitlines())))

# the lane launch template pins the brief's digest; it must follow
brief_sha = hashlib.sha256((EZ / "AUTHOR_WAVE_BRIEF.v1.md").read_bytes()).hexdigest()
tpl = Path(__file__).resolve().parent / "LANE_LAUNCH_TEMPLATE.md"
tt = tpl.read_text(encoding="utf-8")
import re
old_pin = re.search(r"`([0-9a-f]{64})` \|\n\| `\{LANE_FILE\}`", tt)
if old_pin and old_pin.group(1) != brief_sha:
    tt = tt.replace(old_pin.group(1), brief_sha)
    tpl.write_text(tt, encoding="utf-8", newline="\n")
    print("launch template's brief digest updated to %s" % brief_sha)
else:
    print("launch template already pins %s" % brief_sha)
