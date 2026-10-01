#!/usr/bin/env python3
"""Record P6 as landed, and ROUTE the three findings that are not mine to settle."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
NOW = datetime.now(timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()          # noqa: E731
E = []


def add(**kw):
    E.append(dict(kw, opened_at=NOW, raised_by="orchestrator (claude-opus-5), from the P6 subagent's "
                                               "measurement"))


add(id="E13-66",
    severity="MEDIUM",
    headline="P6 IS DONE: the device inventory's next version landed with EXACT digest parity, and every v1 "
             "figure it re-derived reproduced VERSE FOR VERSE rather than merely in count",
    status="DONE", blocks_author_wave=False, tier="MEASURED",
    what_landed={"inventory": "Ezek/ezek_device_inventory.v2.json",
                 "inventory_sha256": sha(EZ / "ezek_device_inventory.v2.json"),
                 "derivation_record": "Ezek/p6_derivation_record.v1.json",
                 "derivation_record_sha256": sha(EZ / "p6_derivation_record.v1.json"),
                 "v1_untouched_sha256": sha(EZ / "ezek_device_inventory.json"),
                 "tokens_reported": 245535},
    deliverables_measured={
        "D1": "five figures, not three: strict 39, vayehi-any 41, hayah-perfect 7, family 48, any-form 49. MT "
              "1:3 is in NONE of the three lists, which is why 49 = 48 + 1",
        "D2": "the messenger chain MT 36:2-36:7 is SIX and cannot be seven (six verses, one occurrence each; "
              "MT 36:1 and 36:8 empty). MT 21:14 is the fourth short-form VERSE but the THIRD distinct SHAPE - "
              "only three shapes exist and they account for all 126 occurrences",
        "D3": "five adonai-form recognition verses (MT 13:9, 23:49, 24:24, 28:24, 29:16), reproduced verse for "
              "verse INDEPENDENTLY of peer_03; agreement does not upgrade the tier",
        "D4": "recognition_formula_2ms relabelled recognition_formula_2s - the form is 2-SINGULAR and "
              "gender-UNRESOLVED; pointing MEASURED as feminine at MT 16:62 and 22:16, masculine at MT 25:7, "
              "35:4, 35:12. Old key kept as an alias",
        "D5": "year-word non-datelines 7 -> 11, MT 39:9 present",
        "the_64": "64, decomposing disjointly as 28 + 8 + 21 + 5 + 2; six verses carry the formula with NO "
                  "knowing verb and are what the predicate excludes",
        "the_21": "21, identical to strategy section 2a verse for verse",
        "transport_A12b": "33 verses / 46 occurrences from a stated predicate",
    },
    the_agents_most_valuable_self_disclosure=(
        "its first hand-of-YHWH predicate returned 5 by matching bare yod-daleth and dropping the vav-prefixed "
        "form, and BOTH OF ITS DERIVATIONS AGREED AT THE WRONG ANSWER. Two derivations by one agent are not two "
        "lenses (OW-19) - they share the agent's misreading of the predicate. What caught it was comparing "
        "every class against the v1 list verse for verse: an EXTERNAL reference, not a second internal pass. "
        "This is the sharpest illustration this campaign has of why OW-19 counts decorrelation and not "
        "repetition."),
    an_error_in_my_own_brief=("my P6 brief glossed '49/41/48' as the three word-event sub-labels. That does NOT "
                              "reproduce - strict is 39 and hayah-perfect is 7. I took #e12's label string and "
                              "read it as a mapping it never claimed. The agent re-derived from the bytes "
                              "instead of fitting its measurement to my gloss, which is what the brief asked "
                              "for and the opposite of what a compliant agent would have done."))

add(id="E13-67",
    severity="HIGH",
    headline="FOR THE CONTROLLING AGENT: R11's third premise is FALSE against the pinned bytes - pmarks NAMES "
             "MT 33:20, with a finding and a status",
    status="OPEN - needs the controlling agent", blocks_author_wave=False, tier="MEASURED",
    what_r11_said=("#e13 R11 routed the MT 33:20 sof-pasuq discrepancy as an input discrepancy: 'strategy "
                   "asserts none; the extract carries none anywhere; pmarks implies one verse lacks it and "
                   "NAMES NONE'. Routed to the inventory's next version as UNAVAILABLE at verse granularity; "
                   "no row scored on it."),
    what_is_true=("premises one and two reproduce exactly - the strategy names the verse twice (sections 2f and "
                  "7), and U+05C3 occurs ZERO times across all 1273 extract verses, so the extract can neither "
                  "confirm nor deny. Premise THREE does not: pmarks names it explicitly at "
                  "arithmetic_anomalies_resolved.sof_pasuq_1272_for_1273_verses.verse = 'Ezek.33.20', with a "
                  "finding and a status field. The ruling recorded that premise as REPORTED by peer_08 and it "
                  "was never checked against the file."),
    what_is_actually_unavailable=("INDEPENDENT VERIFICATION, not the name. The only pinned witness carries no "
                                  "sof-pasuq anywhere, and the OSHB XML is not a path pinned to any agent under "
                                  "E-19. So the value is UNAVAILABLE for verification while the NAME is "
                                  "MEASURED - a distinction the ruling's wording collapses."),
    consequence="no row is scored on it either way, so nothing in the corpus turns on this. What turns on it is "
                "whether a ruling's premise stands, which is the controlling agent's to correct.",
    the_general_lesson=("a premise recorded as REPORTED inside a ruling is still an unverified claim. This one "
                        "survived a ruling because its tier was honest and nobody opened the file it described "
                        "- which is UNAVAILABLE-where-MEASURABLE wearing a correct tier label."))

add(id="E13-68",
    severity="HIGH",
    headline="FOR THE CONTROLLING AGENT: the transport class is 33 verses once its predicate is STATED, and the "
             "strategy's closed 20 is a strict SUBSET - membership changes on 13 verses",
    status="OPEN - needs the controlling agent; 8 held items depend on it",
    blocks_author_wave=False, tier="MEASURED",
    measured=("33 verses / 46 occurrences satisfy the stated guided-motion predicate. The strategy's closed list "
              "of 20 is not the output of ANY stated predicate - it is 20 of the 33 that satisfy one. The 13 "
              "beyond it: MT 3:12, 3:14, 37:2, 40:2, 40:3, 40:24, 40:48, 42:15, 43:1, 44:1, 46:21, 47:3, 47:4."),
    why_it_explains_earlier_findings=("MT 40:24 carries the very verb the closed list accepts at 47:6, and MT "
                                      "46:21 is the plene spelling of a form the list accepts three times - "
                                      "which is why lanes reading the bytes kept finding them and being marked "
                                      "wrong. MT 40:3 is dropped by any sweep keyed on the short object form "
                                      "alone."),
    the_question=("A12-b's hold was 'until those lists land'. The lists have landed, so the hold's literal "
                  "condition is met - but the transport list landed with a DIFFERENT membership from the "
                  "strategy's closed 20. C2-amended says the INVENTORY governs list membership and the STRATEGY "
                  "governs named held questions, which points at the inventory; the P6 agent explicitly "
                  "declined to rule it and so do I."),
    what_i_did_instead=("the 8 held items (peer_03's four sweep findings, peer_10's four transport rows) remain "
                        "HELD and are NOT in the worklist. The author brief forbids writing a transport-class "
                        "membership claim for any of the 13 verses and tells authors to escalate instead. The "
                        "other 20 are unchanged and authors may rely on them. So the wave proceeds without "
                        "pre-empting the ruling."),
    also_measured_beyond_the_order=("four year-residue verses are genuine members that no ruling ordered: MT "
                                    "4:5, 22:4, 38:8, 38:17. MT 26:10 is excluded as the substring artefact the "
                                    "v1 itself named, retained as a named exclusion."))

with Q.open("a", encoding="utf-8", newline="\n") as fh:
    for e in E:
        fh.write(json.dumps(e, ensure_ascii=False) + "\n")
rows = [json.loads(l) for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()]
print(json.dumps({"appended": [e["id"] for e in E], "queue_rows": len(rows),
                  "open_for_the_controlling_agent": [r["id"] for r in rows
                                                     if "needs the controlling agent" in str(r.get("status"))]},
                 indent=1))
