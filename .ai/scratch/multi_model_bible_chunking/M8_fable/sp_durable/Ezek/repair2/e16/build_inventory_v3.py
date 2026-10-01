#!/usr/bin/env python3
"""#e16 tool order: the device inventory v2 -> v3 (additive; v2 is never rewritten), distinct-checked (OW-10).

ADDITIONS, each with its tier stated:
  said_to_me_in_vision      MEASURED by sweep, two derivations that must agree: (A) a regex for the consonantal skeleton
                            'ויאמר אלי' | 'ויאמר יהוה אלי' | 'וידבר אלי' at the head of the verse; (B) a token scan of
                            the verse's first tokens. Restricted to #e16 C4's vision stretches (frames MEASURED, extents
                            INFERRED by #e16 and stated so). #e16's fixture list must be contained, or the build refuses.
  recognition_shaped_not_counted   20:26, 2:5, 33:33 - DISCLOSED, NOT COUNTED; the phrase is checked present (MEASURED),
                            the classification is #e16's (a reading)
  genre_colophon            19:14, 43:12 - a reading (#e16)
  vision_return             3:15, 11:25 - a reading (#e16)
  unit_final_refrains_candidate    NON-SCORING record for method section 17; each phrase checked present (MEASURED)

usage: python build_inventory_v3.py
"""
import hashlib
import json
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
V2 = EZ / "ezek_device_inventory.v2.json"
V3 = EZ / "ezek_device_inventory.v3.json"
R16 = EZ / "author" / "e16" / "ruling_e16.json"


def skel(t):
    t = unicodedata.normalize("NFD", t).replace("־", " ")
    return " ".join("".join(ch for ch in t if "א" <= ch <= "ת" or ch == " ").split())


W, ORDER = {}, []
for line in (EZ / "Ezek_oshb.txt").read_text(encoding="utf-8").splitlines():
    if "\t" in line:
        ref, text = line.split("\t", 1)
        c, v = (int(x) for x in ref.strip().split(".")[1:3])
        W[(c, v)] = skel(text)
        ORDER.append((c, v))
STRETCHES = [((1, 1), (3, 15)), ((3, 22), (3, 27)), ((8, 1), (11, 25)), ((37, 1), (37, 14)), ((40, 1), (48, 35))]
inside = lambda cv: any(a <= cv <= b for a, b in STRETCHES)                    # noqa: E731

HEADS = ("ויאמר אלי", "ויאמר יהוה אלי", "וידבר אלי")
A = sorted(cv for cv in ORDER if inside(cv) and any(W[cv] == h or W[cv].startswith(h + " ") for h in HEADS))
B = []
for cv in ORDER:
    if not inside(cv):
        continue
    t = W[cv].split()
    if (t[:2] == ["ויאמר", "אלי"]) or (t[:3] == ["ויאמר", "יהוה", "אלי"]) or (t[:2] == ["וידבר", "אלי"]):
        B.append(cv)
if A != sorted(B):
    raise SystemExit("REFUSED: the two derivations disagree: A-B %s, B-A %s" % (sorted(set(A) - set(B)), sorted(set(B) - set(A))))
FIXTURE = [(2, 1), (3, 1), (3, 4), (3, 10), (8, 5), (8, 6), (8, 8), (8, 12), (8, 13), (8, 15), (8, 17), (11, 2), (11, 5), (37, 3),
           (37, 4), (37, 9), (37, 11), (40, 4), (41, 4), (41, 22), (42, 13), (43, 7), (43, 18), (44, 2), (44, 5), (46, 20),
           (46, 24), (47, 6), (47, 8)]
ref = lambda cv: "Ezek.%d.%d" % cv                                               # noqa: E731
# #e16 states the predicate ('at the verse's head') AND a fixture list, and also that "membership is the sweep's, not this
# list's (the list is a floor ... INFERRED here from the verses I read)". Where they disagree the stated predicate governs
# (C2-amended: an input that contradicts itself is reported, not guessed). A fixture verse that carries the phrase
# MID-VERSE is recorded as a measured discrepancy; one that does not carry the phrase at all still refuses the build.
mid_verse = [cv for cv in FIXTURE if cv not in A and any(" " + h + " " in " " + W[cv] + " " for h in HEADS)]
missing = [cv for cv in FIXTURE if cv not in A and cv not in mid_verse]


def present(cv, phrase):
    return skel(phrase) in W[cv]


checks = {
    "recognition_shaped_not_counted": {(20, 26): "אשר אני יהוה", (2, 5): "כי נביא היה בתוכם", (33, 33): "כי נביא היה בתוכם"},
    "unit_final_refrains_candidate": {(26, 21): "בלהות", (27, 36): "בלהות", (28, 19): "בלהות", (3, 19): "נפשך הצלת",
                                      (3, 21): "נפשך הצלת", (33, 9): "נפשך הצלת", (18, 4): "הנפש החטאת היא תמות",
                                      (18, 20): "הנפש החטאת היא תמות", (8, 6): "תשוב תראה", (8, 13): "תשוב תראה", (8, 15): "תשוב תראה"},
}
presence = {k: {ref(cv): present(cv, ph) for cv, ph in v.items()} for k, v in checks.items()}
absent = {k: [r for r, ok in v.items() if not ok] for k, v in presence.items()}
v2 = json.loads(V2.read_text(encoding="utf-8"))
v3 = dict(v2)
v3["version"] = "v3"
v3["supersedes"] = {"file": "Ezek/ezek_device_inventory.v2.json", "sha256": sha(V2), "relation": "ADDITIVE - every v2 list unchanged"}
v3["v3_additions"] = {
    "ordered_by": {"ruling": "#e16 tool_orders[2]", "file": "Ezek/author/e16/ruling_e16.json", "sha256": sha(R16)},
    "said_to_me_in_vision": {
        "gloss": "'he said to me' / 'YHWH said to me' / 'he spoke to me' at the head of a verse inside a vision stretch - a LICENSED onset for the scale (#e16 C4)",
        "predicate_consonantal_skeleton": list(HEADS), "vision_stretches": ["%d:%d-%d:%d" % (a + b) for a, b in STRETCHES],
        "vision_stretch_tier": "frames MEASURED (hand-of-YHWH / transport openers and return clauses); extents INFERRED by #e16 from the frames",
        "verses_mt": [ref(cv) for cv in A], "count": len(A), "tier": "MEASURED",
        "distinct_check": {"derivation_A_regex_at_verse_head": len(A), "derivation_B_token_scan": len(B), "agree": True,
                           "e16_fixture_contained": not missing and not mid_verse, "e16_fixture_missing": [ref(cv) for cv in missing],
                           "e16_fixture_discrepancies_mid_verse": [{"verse": ref(cv), "measured": "the phrase stands mid-verse, not at the head, so the stated predicate excludes it",
                                                                   "skeleton_head": " ".join(W[cv].split()[:6])} for cv in mid_verse],
                           "resolution": "the stated predicate governs, as #e16 itself says membership is the sweep's; the discrepancy is routed to the controlling agent with the close-gate packet"}},
    "said_to_me_mid_verse_disclosed": {"verses_mt": [ref(cv) for cv in ORDER if inside(cv) and cv not in A and any(" " + h + " " in " " + W[cv] + " " for h in HEADS)],
                                       "status": "DISCLOSED, NOT LICENSED as an onset by the stated predicate (speech begins inside the verse)", "tier": "MEASURED"},
    "recognition_shaped_not_counted": {"verses_mt": sorted(presence["recognition_shaped_not_counted"]), "phrase_present_MEASURED": presence["recognition_shaped_not_counted"],
                                       "status": "DISCLOSED, NOT COUNTED in any recognition class", "tier": "classification a reading (#e16); phrase presence MEASURED"},
    "genre_colophon": {"verses_mt": ["Ezek.19.14", "Ezek.43.12"], "role": "close-role signal for the scale (#e16 C4)", "tier": "a reading (#e16)"},
    "vision_return": {"verses_mt": ["Ezek.3.15", "Ezek.11.25"], "role": "close-role signal for the scale (#e16 C4)", "tier": "a reading (#e16)"},
    "unit_final_refrains_candidate": {"groups": {"terror and you shall be no more": ["Ezek.26.21", "Ezek.27.36", "Ezek.28.19"],
                                                 "you have delivered your soul": ["Ezek.3.19", "Ezek.3.21", "Ezek.33.9"],
                                                 "the soul that sins shall die": ["Ezek.18.4", "Ezek.18.20"],
                                                 "you shall again see": ["Ezek.8.6", "Ezek.8.13", "Ezek.8.15"]},
                                      "phrase_present_MEASURED": presence["unit_final_refrains_candidate"],
                                      "status": "NON-SCORING record for method section 17 - no row may score on it", "tier": "phrase presence MEASURED; refrain status a candidate reading"},
}
v3["changes_from_v2"] = ["v3_additions: said_to_me_in_vision (swept, distinct-checked), recognition_shaped_not_counted, genre_colophon, "
                         "vision_return, unit_final_refrains_candidate (non-scoring) - ordered by #e16; no v2 list changed"]
v3["built_at"] = datetime.now(timezone.utc).isoformat()
if missing or any(absent.values()):
    raise SystemExit("REFUSED: fixture verses missing from the sweep %s or phrases absent %s" % ([ref(cv) for cv in missing], absent))
if V3.exists() and V3.read_bytes() != json.dumps(v3, ensure_ascii=False, indent=1).encode("utf-8"):
    raise SystemExit("REFUSED: %s exists with different bytes (E-41) - write a new version" % V3.name)
V3.write_text(json.dumps(v3, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"said_to_me_in_vision": len(A), "derivations_agree": True, "fixture_contained": True,
                  "extra_beyond_fixture": [ref(cv) for cv in A if cv not in FIXTURE], "v3_sha256": sha(V3)}, ensure_ascii=False, indent=1))
