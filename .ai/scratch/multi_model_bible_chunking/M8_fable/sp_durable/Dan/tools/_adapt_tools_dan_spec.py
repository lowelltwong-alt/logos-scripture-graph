"""Substitution spec for _adapt_tools_dan.py. Every entry is (old, new, exact_count) against the pass-1 output.
KEEP lists residual lines that stay on purpose, each with its reason. Facts written here are Daniel facts asserted by
dan_lib._selftest (zones, verse counts) or read from the Phase 0 artifacts; none is typed from recall."""

TOOLS = ["run_validator_suite.py", "cap_sweep.py", "ngram7.py", "normalize_hebrew_in_json.py", "check_universals.py",
         "check_register.py", "check_role_tokens.py", "check_tiling.py", "collate.py", "sweep.py",
         "check_atomic_isolation.py", "check_brief_vs_suite.py"]

LINEAGE = "lineage: an Ezekiel ruling, record or convention cited by its Ezekiel id; the arm it installed is inherited"

SUBS = {
    "run_validator_suite.py": [
        ("(m8-mesh-r3), Ezek. Orchestrator-run", "(m8-mesh-r3), Dan. Orchestrator-run", 1),
        ("JER SUITE UPGRADES, inherited by Ezek (per", "JER SUITE UPGRADES, inherited by Ezek and then Dan (per", 1),
    ],
    "cap_sweep.py": [
        ("confidence-cap sweep, Ezek - Tier-0", "confidence-cap sweep, Dan - Tier-0", 1),
        ("assert len(LAST_VERSE) == 48 and sum(LAST_VERSE.values()) == 1273, \\",
         "assert len(LAST_VERSE) == 12 and sum(LAST_VERSE.values()) == 357, \\", 1),
    ],
    "ngram7.py": [
        ("(Hebrew-quotation-aware), Ezek.", "(Hebrew-quotation-aware), Dan.", 1),
        ("bare Ezek.C.V tokens", "bare Dan.C.V tokens", 2),
        ('"C2 Ezek.10.1-..."', '"C2 Dan.1.1-..."', 1),
        ('(the Jer run; Ezek rows carry "Ezek" and are excluded the same way)',
         '(the Jer run; Dan rows carry "Dan" and are excluded the same way)', 1),
    ],
    "normalize_hebrew_in_json.py": [
        ("for any Ezek campaign JSON", "for any Dan campaign JSON", 1),
        ("Ezek_oshb.txt standing on word boundaries", "Dan_oshb.txt standing on word boundaries", 1),
        ("QERE TIER (Ezek):", "QERE TIER (Dan):", 1),
        ("split per note by ezek_lib.kq_split", "split per note by dan_lib.kq_split", 1),
        ('counted under "qere", mirroring SP/Ezek/_validate_writer_part.py. An NFD-only',
         'counted under "qere", mirroring the Ezek writer-part validator (lineage). An NFD-only', 1),
        ("_test_zone_tools_ezek.py proves that arm refuses a Qere cited at the wrong verse\n(T1 review, 2026-09-10).",
         "_test_zone_tools_dan.py proves that arm refuses a Qere cited at the wrong verse\n"
         "(ported from the Ezek T1-review test, 2026-09-10).", 1),
    ],
    "check_universals.py": [
        ("(Ezek; lexicon WIDENED", "(Dan; lexicon WIDENED", 1),
        ("citation periods (Ezek.C.V,", "citation periods (Dan.C.V,", 1),
        ("(NEW for Jer and inherited by Ezek, per", "(NEW for Jer and inherited by Ezek and Dan, per", 1),
        ("citation/abbreviation dot (Ezek.3.1,", "citation/abbreviation dot (Dan.3.1,", 1),
        ('"oshb:Dan.47.5 [WARRANT-rival:far] 47.4/47.5 one-faced only"',
         '"oshb:Dan.9.5 [WARRANT-rival:far] 9.4/9.5 one-faced only"', 1),
        ("(sweep: 5 verses) at 13:9", "(sweep: 5 verses) at 9:13", 1),
    ],
    "check_register.py": [
        ("Register sweep, Ezek - FLAGS", "Register sweep, Dan - FLAGS", 1),
        ('"oshb:Dan.24.24 [DISCLOSURE-device]', '"oshb:Dan.9.24 [DISCLOSURE-device]', 1),
    ],
    "check_role_tokens.py": [
        ("The ch 20/21 zone is never computed: an entry touching it is verified on its web: face only when it\n"
         "is written dual, and its MT face is not re-derived by arithmetic.",
         "The numbering zone is never computed: an entry whose ref (or range end) lies in the zone ON ITS OWN FACE\n"
         "is counted, not derived, and its other face is not re-derived by arithmetic. The zone is read from dan_lib's\n"
         "crosswalk (WEB 4:1-37, 5:31, 6:1-28 = MT 3:31-4:34, 6:1-29; 66 verses on each face), never typed.", 1),
        ('EZ = Path(r"C:\\wt\\logos-t423-m8-fable\\.ai\\scratch\\multi_model_bible_chunking\\M8_fable\\sp_durable\\Dan")\n'
         'sys.path.insert(0, str(EZ / "tools"))',
         'BK = Path(__file__).resolve().parent.parent\n'
         'sys.path.insert(0, str(BK / "tools"))\n'
         'from dan_lib import LAST_VERSE, MT_LAST_VERSE, mt_to_web, web_to_mt  # noqa: E402', 1),
        ('(EZ / "verse_inventory.json")', '(BK / "verse_inventory.json")', 1),
        ("ZONE_WEB = {(20, v) for v in range(45, 50)} | {(21, v) for v in range(1, 33)}",
         "ZONE_WEB = {(c, v) for c, n in LAST_VERSE.items() for v in range(1, n + 1) if web_to_mt(c, v) != (c, v)}\n"
         "ZONE_MT = {(c, v) for c, n in MT_LAST_VERSE.items() for v in range(1, n + 1) if mt_to_web(c, v) != (c, v)}", 1),
        ('            if face == "oshb" or cv in ZONE_WEB or (cv[0] in (20, 21) and g[5] is None and cv[0] == 21):\n'
         '                if cv in ZONE_WEB or cv[0] == 21:\n'
         '                    counts["zone_entries_not_derived"] += 1\n'
         '                    continue\n',
         '            zone = ZONE_MT if face == "oshb" else ZONE_WEB\n'
         '            if cv in zone or (g[3] and (int(g[3]), int(g[4])) in zone):\n'
         '                counts["zone_entries_not_derived"] += 1\n'
         '                continue\n', 1),
        ("no formula inside 33:13", "fixture: an absence inside the span", 1),
        ("Dan.33.", "Dan.9.", 18),
        ("33.11/33.12", "9.11/9.12", 4),
        ("the ve'attah re-address opens", "fixture: the onset seam verse", 1),
        ("samekh behind the onset", "fixture: the verse behind the onset", 1),
        ("verdict clause closes", "fixture: the close seam verse", 1),
        ("dateline opens the next", "fixture: the verse after the close", 1),
        ("ve'attah same audience", "fixture: a candidate onset inside the span", 1),
        ("pe behind the rival", "fixture: the verse behind the rival", 1),
        ("ve'attah without a seam pair", "fixture: a rival with no seam pair", 1),
        ('"Dan.18.1-Dan.18.4"', '"Dan.9.1-Dan.9.4"', 1),
        ('"oshb:Dan.17.24 [WARRANT-onset:far] refrain behind the chapter"',
         "\"oshb:Dan.8.27 [WARRANT-onset:far] fixture: the previous chapter's last verse\"", 1),
        ("# #e16 tool-order fixtures for the :merge arm (rows shaped as P03-011, P01-006, P03-012)",
         "# #e16 tool-order fixtures for the :merge arm (shaped as Ezek rows P03-011, P01-006, P03-012; Daniel refs)", 1),
        ("Dan.17.11-Dan.17.18", "Dan.11.11-Dan.11.18", 2),
        ("Dan.17.19-Dan.17.21", "Dan.11.19-Dan.11.21", 3),
        ("17.18/17.19", "11.18/11.19", 2),
        ("17.10/17.11", "11.10/11.11", 1),
        ('    merge_on_close = dict(row, boundary_evidence_refs=["oshb:Dan.9.20 [WARRANT-close:merge] not a rival"])\n',
         '    merge_on_close = dict(row, boundary_evidence_refs=["oshb:Dan.9.20 [WARRANT-close:merge] not a rival"])\n'
         '    # Dan: the numbering zone on its own face is counted, never derived (MT 3:31 is the MT face of WEB 4:1)\n'
         '    zone_row = {"decision_id": "Z", "span": "Dan.4.1-Dan.4.3",\n'
         '                "boundary_evidence_refs": ["oshb:Dan.3.31 [WARRANT-onset:near] fixture: MT face of WEB 4:1",\n'
         '                                           "web:Dan.4.37 [WARRANT-close:far] fixture: WEB-zone verse"]}\n'
         '    z_flags, z_counts = check_rows([zone_row], "post")\n'
         '    zone_cases = [("a ref inside the numbering zone on its own face is counted, not derived",\n'
         '                   not z_flags and z_counts["zone_entries_not_derived"] == 2),\n'
         '                  ("the zone derives 66 verses on each face", len(ZONE_WEB) == 66 == len(ZONE_MT))]\n', 1),
        ('("the denominator is nonzero", g_counts["entries_read"] == 9)] + merge_cases',
         '("the denominator is nonzero", g_counts["entries_read"] == 9)] + merge_cases + zone_cases', 1),
    ],
    "check_tiling.py": [
        ("--range Ezek.1.1-Ezek.2.20", "--range Dan.1.1-Dan.2.49", 1),
        ('("Ezek.C.V-Ezek.C.V" or single verse;', '("Dan.C.V-Dan.C.V" or single verse;', 1),
    ],
    "collate.py": [
        ("skeleton tiers), Ezek.", "skeleton tiers), Dan.", 1),
        ("--ref oshb:Ezek.3.7 --quote", "--ref oshb:Dan.3.31 --quote", 1),
        ("--ref Ezek.4.1 --quote", "--ref Dan.4.1 --quote", 1),
        ("--ref Ezek.1.5-Ezek.1.11 --quote", "--ref Dan.1.5-Dan.1.11 --quote", 1),
        ("the oshb: prefix. Ezek is NOT an identity book (byte-proven;\n"
         "web_mt_offset_map.json): EXACTLY ONE offset zone, pure renumbering, NO\n"
         "split - MT 21:1-5 = WEB 20:45-49 / MT 21:6-37 = WEB 21:1-32 \u2014 bare/web: refs pass\n"
         "through web_to_mt() internally, so a WEB ch-9 ref collates against the\n"
         "CORRECT shifted MT verse; every WEB verse has exactly one WLC counterpart\n"
         "(injective crosswalk).",
         "the oshb: prefix. Dan is NOT an identity book (byte-proven;\n"
         "web_mt_offset_map.json): TWO offset zones, pure renumbering, NO split -\n"
         "MT 3:31-33 = WEB 4:1-3 / MT 4:1-34 = WEB 4:4-37 and MT 6:1 = WEB 5:31 /\n"
         "MT 6:2-29 = WEB 6:1-28 \u2014 bare/web: refs pass through web_to_mt() internally,\n"
         "so a WEB ch-4 ref collates against the CORRECT shifted MT verse; every WEB\n"
         "verse has exactly one WLC counterpart (injective crosswalk).", 1),
        ("# dedupe guard (inert in Ezek:", "# dedupe guard (inert in Dan:", 1),
    ],
    "sweep.py": [
        ("universal/exclusivity claim), Ezek.", "universal/exclusivity claim), Dan.", 1),
        ("(Ezek toolkit convention)", "(Ezek toolkit convention, inherited by dan_lib)", 1),
    ],
    "check_atomic_isolation.py": [
        ("scoped-mesh cluster builder (Ezek,", "scoped-mesh cluster builder (Dan,", 1),
        ("via the ezek_lib crosswalk (the MT\ntext of WEB 20:45 is MT 21:1's). Ezek has NO split verse",
         "via the dan_lib crosswalk (the MT\ntext of WEB 4:1 is MT 3:31's). Dan has NO split verse", 1),
        ("SP/Ezek/review_scope.json", "SP/Dan/review_scope.json", 1),
    ],
    "check_brief_vs_suite.py": [
        ('"""Does the author brief carry a duty for every check the validator suite will measure it by?\n',
         '"""Does the author brief carry a duty for every check the validator suite will measure it by?\n\n'
         "Daniel port of the Ezek control (Dan/tools/_adapt_tools_dan.py). The history below is EZEKIEL's, kept as\n"
         "lineage; the Daniel changes are the language_zones duties (three all_of groups), a refusal in place of the\n"
         "silent last-report fallback, and a path read from this file's location.\n", 1),
        ('EZ = Path(r"C:\\wt\\logos-t423-m8-fable\\.ai\\scratch\\multi_model_bible_chunking\\M8_fable\\sp_durable\\Dan")',
         "EZ = Path(__file__).resolve().parent.parent", 1),
        ('    "language_zones": {"phrases": ["MT 21:1-5 = WEB 20:45-49", "BOTH faces"],\n'
         '                       "duty": "dual writing inside the renumbering zone"},',
         '    "language_zones": {"all_of": [["Aramaic island"], ["2:4a", "2:4b"], ["BOTH faces"]],\n'
         '                       "duty": ("disclose the Aramaic island (2:4b-7:28), state the 2:4a/2:4b half at a "\n'
         '                                "mid-verse boundary or quotation, and write both faces inside the numbering "\n'
         '                                "zones")},', 1),
        ("if not members:\n"
         "    # fall back to the names the suite actually emitted in the last report\n"
         '    rep = json.loads((EZ / "repair" / "rows_v7_cwo24.jsonl.validator_report.json")\n'
         '                     .read_text(encoding="utf-8"))\n'
         '    members = sorted(k for k in rep if k not in ("rows_file", "summary"))\n',
         "if not members:\n"
         "    # Dan: no fallback. A report on disk cannot know a member added since it was written (the failure the\n"
         "    # comment above records), so an empty discovery is a refusal, never a silent substitute.\n"
         '    raise SystemExit("REFUSED: no suite members discovered in %s" % SUITE)\n', 1),
        ('    hits = [p for p in spec["phrases"] if p in brief]\n'
         "    ok = bool(hits)\n"
         '    rows.append({"check": m, "status": "DUTY PRESENT" if ok else "DUTY MISSING",\n'
         '                 "duty": spec["duty"], "matched_phrases": hits,\n'
         '                 "searched_for": spec["phrases"]})\n',
         '    # Dan: a member may carry several duties; every "all_of" group must be spoken to (any phrase of the group)\n'
         '    groups = spec.get("all_of", [spec.get("phrases", [])])\n'
         "    hits = [p for g in groups for p in g if p in brief]\n"
         "    ok = all(any(p in brief for p in g) for g in groups)\n"
         '    rows.append({"check": m, "status": "DUTY PRESENT" if ok else "DUTY MISSING",\n'
         '                 "duty": spec["duty"], "matched_phrases": hits,\n'
         '                 "searched_for": groups})\n', 1),
        ('"schema": "ezek_brief_vs_suite.v1",', '"schema": "dan_brief_vs_suite.v1",', 1),
        ('"why": ("the Daniel author brief was written from the rulings and not checked against the suite; three "\n'
         '            "checks that were GREEN went red because the brief never named their duty"),',
         '"why": ("lineage (Ezek): the Ezekiel author brief was written from the rulings and not checked against "\n'
         '            "the suite; three checks that were GREEN went red because the brief never named their duty"),', 1),
        ("It would have caught all three of this book's regressions, ",
         "It would have caught all three of Ezekiel's regressions, ", 1),
    ],
}

KEEP = {
    "run_validator_suite.py": [("inherited by Ezek and then Dan", LINEAGE)],
    "normalize_hebrew_in_json.py": [("ported from the Ezek T1-review test", LINEAGE),
                                    ("mirroring the Ezek writer-part validator (lineage)", LINEAGE)],
    "check_universals.py": [("inherited by Ezek and Dan", LINEAGE)],
    "check_register.py": [("ezek_controlling_rulings_a1", LINEAGE)],
    "check_role_tokens.py": [("shaped as Ezek rows", LINEAGE)],
    "sweep.py": [("Ezek toolkit convention, inherited by dan_lib", LINEAGE)],
    "check_brief_vs_suite.py": [("I wrote the Ezekiel author brief from the RULINGS", LINEAGE),
                                ("Daniel port of the Ezek control", LINEAGE),
                                ("lineage (Ezek): the Ezekiel author brief", LINEAGE),
                                ("all three of Ezekiel's regressions", LINEAGE)],
}
