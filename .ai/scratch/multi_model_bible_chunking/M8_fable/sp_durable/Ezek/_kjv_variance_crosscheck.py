"""Independent cross-check of the Ezekiel offset map against the OSHB's OWN KJV-variance note layer.

The map in web_mt_offset_map.json was derived from per-chapter verse counts and confirmed from verse CONTENT.
The OSHB separately carries `KJV:Ezek.C.V` notes, an entirely different layer of the same source that states the
English-tradition reference for each MT verse. If the two agree on every verse the map is corroborated by
evidence that was not used to build it. If they disagree anywhere, the map is wrong and nothing may be built on it.
"""
import json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
pm = json.load(open(SP / "pmarks_Ezek.json", encoding="utf-8"))


def mt_to_web(c, v):
    if c == 21 and v <= 5:
        return (20, v + 44)
    if c == 21:
        return (21, v - 5)
    return (c, v)


claims, agree, disagree = 0, 0, []
for ref, notes in pm["notes_other"].items():
    for n in notes:
        m = re.match(r"KJV:Ezek\.(\d+)\.(\d+)$", n["text"].strip())
        if not m:
            continue
        claims += 1
        _, c, v = ref.split(".")
        want = (int(m.group(1)), int(m.group(2)))
        got = mt_to_web(int(c), int(v))
        if got == want:
            agree += 1
        else:
            disagree.append({"mt": ref, "oshb_says_kjv": "%d.%d" % want, "my_map_says_web": "%d.%d" % got})

print(json.dumps({
    "kjv_variance_notes_found": claims,
    "agree_with_my_offset_map": agree,
    "disagree": disagree,
    "verdict": "GREEN - corroborated by an independent source layer" if claims and not disagree else
               ("RED - the map contradicts the source's own variance layer" if disagree else
                "NO EVIDENCE - no KJV notes found"),
    "why_this_matters": ("the map was built from verse COUNTS and confirmed from verse CONTENT. This layer was "
                         "not used in either step, so agreement is genuine corroboration rather than a "
                         "restatement of the same evidence."),
    "scope_note": ("the OSHB annotates only the verses where the traditions diverge, so the absence of notes "
                   "outside ch 21 is itself consistent with identity numbering elsewhere"),
}, ensure_ascii=False, indent=1))
sys.exit(1 if disagree else 0)
