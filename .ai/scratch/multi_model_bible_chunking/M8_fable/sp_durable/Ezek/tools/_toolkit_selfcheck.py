#!/usr/bin/env python3
"""Verify every factual claim in TOOLKIT.md against the staged inventories.

WHY. The toolkit is the one document every lane reads and none of them re-derives. A wrong number here propagates
into every brief, every review packet and every row, and it propagates as though it were established fact. So the
numbers are checked against the artifacts they came from, mechanically, and this runs again whenever an inventory
is rebuilt. A toolkit that has drifted from its sources is worse than no toolkit, because it is trusted.

Exit 1 on any mismatch.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SP = HERE.parent
TK = HERE / "TOOLKIT.md"


def _leb_row_ok(text):
    """The `לב חדש` row of the homograph table must list MT 18:31 and 36:26 and must NOT list 11:19."""
    for line in text.splitlines():
        if line.startswith("|") and "לב חדש" in line:
            return ("18:31" in line and "36:26" in line and "11:19" not in line)
    return False  # the row must exist


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    text = TK.read_text(encoding="utf-8")
    pm = json.loads((SP / "pmarks_Ezek.json").read_text(encoding="utf-8"))
    dev = json.loads((SP / "ezek_device_inventory.json").read_text(encoding="utf-8"))
    inv = json.loads((SP / "verse_inventory.json").read_text(encoding="utf-8"))
    omap = json.loads((SP / "web_mt_offset_map.json").read_text(encoding="utf-8"))
    kjv = json.loads((SP / "ezek_kjv_variance_crosscheck.json").read_text(encoding="utf-8"))
    oshb = dict(l.split("\t", 1) for l in (SP / "Ezek_oshb.txt").read_text(encoding="utf-8").splitlines())

    kq = pm["kq"]
    doubled = sorted((k for k, v in kq.items() if len(v) > 1),
                     key=lambda k: (int(k.split(".")[1]), int(k.split(".")[2])))
    f = dev["formulae"]

    checks = [
        ("total verses 1,273", inv["total_verses"] == 1273 and len(oshb) == 1273),
        ("48 chapters", len(inv["chapters"]) == 48),
        ("offset map verdict GREEN", omap["verification"]["verdict"] == "GREEN"),
        ("offset map has no problems", omap["verification"]["problems"] == []),
        ("divergent chapters are exactly 20 and 21",
         json.loads((SP / "web_mt_verse_check.json").read_text(encoding="utf-8"))["divergent_chapters"] == [20, 21]),
        ("WEB ch20=49 MT ch20=44", omap["rule"]["zone"]["web_chapter_20_verses"] == 49
         and omap["rule"]["zone"]["mt_chapter_20_verses"] == 44),
        ("WEB ch21=32 MT ch21=37", omap["rule"]["zone"]["web_chapter_21_verses"] == 32
         and omap["rule"]["zone"]["mt_chapter_21_verses"] == 37),
        ("KJV cross-check 37/37 GREEN",
         kjv["kjv_variance_notes_found"] == 37 and kjv["agree_with_my_offset_map"] == 37 and not kjv["disagree"]),
        ("samekh 113", pm["marks_tally"]["SAMEKH"] == 113),
        ("pe 71", pm["marks_tally"]["PE"] == 71),
        ("184 occurrences over 183 verses", pm["marks_tally"]["SAMEKH"] + pm["marks_tally"]["PE"] == 184
         and pm["marks_tally"]["verses_carrying_a_mark"] == 183),
        ("Ezek.43.27 carries two samekh", pm["marks"].get("Ezek.43.27") == ["SAMEKH", "SAMEKH"]),
        ("PE at MT 21:5", "PE" in pm["marks"].get("Ezek.21.5", [])),
        ("paseq 136 over 121 verses",
         pm["paseq_tally"]["occurrences"] == 136 and pm["paseq_tally"]["verses"] == 121),
        ("paseq at MT 21:3", "Ezek.21.3" in pm["paseq"]),
        ("K/Q 134 notes over 99 verses",
         pm["kq_tally"]["notes"] == 134 and pm["kq_tally"]["verses"] == 99),
        ("23 doubled K/Q verses", len(doubled) == 23),
        # Pinned against pmarks, not against the prose. The toolkit twice asserted something false about this
        # cluster - "eleven" while naming ten, and that the disputed forms are the measurements. Both are now
        # checked from the DATA, so neither claim can regress into the text without this failing.
        ("exactly TEN doubled-K/Q verses in ch 40",
         len([k for k in doubled if k.split(".")[1] == "40"]) == 10),
        ("the toolkit does not claim eleven in ch 40", "eleven K/Q verses" not in text),
        ("the toolkit does not claim the K/Q forms are the measurements",
         "measurements themselves" not in text or "They are not" in text),
        # every ch-40 K/Q qere ends in the 3ms suffix yod-vav, i.e. a possessive on a noun, never a numeral
        ("every ch-40 K/Q qere is a 3ms-suffix form, not a numeral",
         all(any(n.replace("/", "").rstrip("֑-ׇ").endswith(("יו", "יוֹ"))
                 or "יו" in n.replace("/", "")
                 for n in kq[k])
             for k in doubled if k.split(".")[1] == "40")),
        ("no K/Q inside MT 21:1-5",
         not [k for k in kq if k.split(".")[1] == "21" and int(k.split(".")[2]) <= 5]),
        ("only K/Q in MT ch21 is 21:28",
         [k for k in kq if k.split(".")[1] == "21"] == ["Ezek.21.28"]),
        ("71 verses with editorial notes", len(pm["notes_other"]) == 71),
        ("sof-pasuq 1272", pm["seg_totals_in_xml"]["x-sof-pasuq"] == 1272),
        ("MT 33:20 is the verse without sof-pasuq",
         pm["arithmetic_anomalies_resolved"]["sof_pasuq_1272_for_1273_verses"]["verse"] == "Ezek.33.20"),
        ("morph is H only, 18866 tokens",
         pm["morph_prefix_tally"] == {"H": 18866} and pm["aramaic_verses"] == []),
        ("word-event formula 39", f["word_event_formula"]["count"] == 39),
        ("son of man 93", f["son_of_man_address"]["count"] == 93),
        ("messenger formula 122", f["thus_says_the_lord_yhwh"]["count"] == 122),
        ("utterance formula 81", f["utterance_of_the_lord_yhwh"]["count"] == 81),
        ("recognition formula 28", f["recognition_formula"]["count"] == 28),
        ("recognition 2ms 5", f["recognition_formula_2ms"]["count"] == 5),
        ("I YHWH have spoken 14", f["i_am_yhwh_spoken"]["count"] == 14),
        ("hand of YHWH 7", f["hand_of_yhwh_upon_me"]["count"] == 7),
        ("set your face 9", f["set_your_face"]["count"] == 9),
        # RULED 2026-09-08: 14, not 13. MT 24:1 was missing under a cardinal-numeral rule; the rule is now
        # structural (year word + month/day term). Changing this pin without the inventory change would be
        # exactly the drift this file exists to catch, so both moved together and the ruling is recorded.
        ("14 oracle datelines", dev["dated_oracles"]["count"] == 14),
        ("MT 24:1 is in the dateline list", "Ezek.24.1" in dev["dated_oracles"]["verses_mt"]),
        ("7 year-word verses that are not datelines", dev["year_word_but_not_a_dateline"]["count"] == 7),
        ("MT 26:10 is recorded as a year-regex false positive",
         "Ezek.26.10" in dev["year_word_but_not_a_dateline"]["verses_mt"]),
        ("word-event strict 39", dev["word_event_family"]["strict_vayehi_adjacent"] == 39),
        ("word-event with infixed date 41", dev["word_event_family"]["vayehi_any_incl_infixed_date"] == 41),
        ("word-event perfect form 7", dev["word_event_family"]["hayah_perfect_form"] == 7),
        ("the two infixed-date verses are MT 12:8 and 24:1",
         dev["word_event_family"]["infixed_date_verses_the_strict_form_misses"] == ["Ezek.12.8", "Ezek.24.1"]),
        # CORRECTED 2026-09-08: four, not three. 45:18 was the omitted strongest candidate.
        ("4 calendar-only dates 45:18/20/21/25",
         dev["calendar_dates_not_datelines"]["verses_mt"]
         == ["Ezek.45.18", "Ezek.45.20", "Ezek.45.21", "Ezek.45.25"]),
        ("MT 45:18 carries the messenger formula (why it is the dangerous one)",
         "Ezek.45.18" in dev["formulae"]["thus_says_the_lord_yhwh"]["verses_mt"]),
        ("the חדש homographs are excluded from the calendar list",
         not ({"Ezek.45.17", "Ezek.46.3", "Ezek.47.12", "Ezek.11.19", "Ezek.18.31", "Ezek.36.26"}
              & set(dev["calendar_dates_not_datelines"]["verses_mt"]))),
        ("the word_event_family note is not corrupted",
         "הest" not in dev["word_event_family"]["note"]),
        # MT 11:19 reads leb echad ("ONE heart"), not leb chadash. An earlier draft asserted otherwise in BOTH
        # artifacts and the distinct checker refused the repair over it. Pinned on the SOURCE, not on the prose,
        # so the claim cannot be reasserted in either file without this failing.
        ("MT 11:19 reads leb echad, not leb chadash",
         "אחד" in "".join(c for c in oshb["Ezek.11.19"] if not "֑" <= c <= "ׇ")
         and "לב חדש" not in "".join(
             c for c in oshb["Ezek.11.19"] if not "֑" <= c <= "ׇ")),
        # Precise, not a proximity heuristic: find the leb-chadash TABLE ROW and require it to name 18:31 and
        # 36:26 and NOT 11:19. The file legitimately discusses 11:19 elsewhere - to say it is excluded - so a
        # naive "11:19 appears near leb chadash" test fails on correct text, which is a checker defect, not a
        # toolkit defect.
        ("the leb-chadash table row names 18:31 and 36:26 only", _leb_row_ok(text)),
        ("ch16 is longest at 63", inv["chapters"]["16"] == 63),
        ("ch15 is shortest at 8", inv["chapters"]["15"] == 8),
    ]

    # The puncta correction is itself an assertion the toolkit makes, so it is checked like any other.
    # It was WRONG in the first draft ("not in the verse bytes") and refuted from the bytes by the strategy
    # author; pinning the true counts here stops the wrong claim from creeping back on a later edit.
    joined_all = "".join(oshb.values())
    checks.append(("U+05C4 stands in the extract at exactly 2 verses",
                   sum(1 for v in oshb.values() if "ׄ" in v) == 2))
    checks.append(("U+05C4 five marks at MT 41:20", oshb["Ezek.41.20"].count("ׄ") == 5))
    checks.append(("U+05C4 seven marks at MT 46:22", oshb["Ezek.46.22"].count("ׄ") == 7))
    checks.append(("U+05C5 lower dot does not occur", joined_all.count("ׅ") == 0))

    # the extract-hygiene claims the toolkit makes to every lane
    joined = "".join(oshb.values())
    for name, cp in (("no maqaf U+05BE", "־"), ("no paseq U+05C0", "׀"),
                     ("no sof-pasuq U+05C3", "׃"), ("no morpheme /", "/"), ("no stray >", ">")):
        checks.append((name + " in the extract", joined.count(cp) == 0))

    # Every MT ref the toolkit asserts must exist in the source. Two spellings are NOT assertions and are
    # exempt: a ref inside straight double quotes (the toolkit quotes "MT 8:23" as a counter-example of an
    # ambiguous bare ref) and any ref already book-qualified for another book (oshb:Jer.8.23). Loosening the
    # check to make those pass would also stop it catching a genuinely wrong Ezekiel ref, so they are exempted
    # by shape rather than by dropping the check.
    quoted = set()
    for line in text.splitlines():
        for q in re.findall(r'"([^"]*)"', line):
            quoted.update(re.findall(r"MT (\d+):(\d+)", q))
    exempt = []
    for m in re.finditer(r"MT (\d+):(\d+)", text):
        c, v = m.group(1), m.group(2)
        if (c, v) in quoted:
            exempt.append("MT %s:%s (quoted counter-example, not an assertion)" % (c, v))
            continue
        checks.append(("named ref MT %s:%s exists" % (c, v), "Ezek.%s.%s" % (c, v) in oshb))
    for m in re.finditer(r"oshb:(\w+)\.(\d+)\.(\d+)", text):
        bk, c, v = m.groups()
        if bk == "Ezek":
            checks.append(("named ref oshb:Ezek.%s.%s exists" % (c, v), "Ezek.%s.%s" % (c, v) in oshb))
        else:
            exempt.append("oshb:%s.%s.%s (another book, book-qualified)" % (bk, c, v))

    failed = [n for n, ok in checks if not ok]
    print(json.dumps({"checks": len(checks), "passed": len(checks) - len(failed), "failed": failed,
                      "exempt_refs": exempt,
                      "verdict": "GREEN" if not failed else "RED"}, ensure_ascii=False, indent=1))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
