#!/usr/bin/env python3
"""Refine Isaiah 1–12 and Jeremiah 26–33 prophetic seam metadata."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks"


def classify(book: str, ch: int):
    if book == "Isa":
        table = {
            1: ("judgment_lawsuit_oracle", "Zion lawsuit and accusation oracle", ["superscription", "lawsuit_opening", "judgment_to_hope"]),
            2: ("vision_and_judgment_oracle", "Zion vision, instruction, and pride judgment", ["vision_heading", "instruction_poem", "judgment_turn"]),
            3: ("social_judgment_oracle", "Leadership/social judgment and daughter-Zion lament", ["woe_formula", "social_catalogue", "lament_turn"]),
            4: ("restoration_oracle", "Branch/restoration and purified Zion vision", ["restoration_heading", "purification", "presence_closure"]),
            5: ("vineyard_song_and_woes", "Vineyard song followed by woe series", ["song_onset", "song_to_woe", "refrain"]),
            6: ("call_vision", "Throne vision, commission, and hardening response", ["vision_frame", "commission", "response_closure"]),
            7: ("sign_act_oracle", "Syro-Ephraim crisis narrative and sign oracle", ["narrative_frame", "sign_request", "oracle_response"]),
            8: ("sign_name_and_refuge_oracle", "Sign-name, witness instruction, and darkness/refuge oracle", ["sign_name", "witness_frame", "oracle_turn"]),
            9: ("light_and_judgment_oracle", "Light/child oracle and repeated judgment refrain", ["hope_oracle", "refrain", "judgment_cycle"]),
            10: ("woe_and_remnant_oracle", "Legal woe, Assyrian instrument, and remnant return", ["woe_formula", "boast_speech", "remnant_song"]),
            11: ("branch_and_earthwide_reign_oracle", "Branch, spirit, transformed creation, and return", ["branch_oracle", "creation_image", "return_song"]),
            12: ("salvation_song", "Paired thanksgiving/salvation song closure", ["song_onset", "refrain", "collection_closure"]),
        }
        return table[ch] + (["Hebrew wordplay, oracle headings, and addressee shifts require review"], ["Test poetry/song versus oracle transitions without using later fulfillment as boundary authority"])
    if book == "Jer":
        table = {
            26: ("temple_sermon_trial", "Temple sermon, prophetic warning, and trial narrative", ["sermon_frame", "crowd_response", "trial_closure"]),
            27: ("yoke_sign_act_oracle", "Yoke sign-act and submission oracle", ["sign_act", "prophetic_address", "oracle_closure"]),
            28: ("prophet_conflict_sign_act", "Jeremiah/Hananiah conflict and broken-yoke sign", ["speaker_conflict", "sign_act", "death_oracle"]),
            29: ("exilic_letter_and_counter_oracle", "Exilic letter, response, and counter-oracle", ["letter_frame", "letter_body", "counter_oracle"]),
            30: ("restoration_oracle", "Restoration oracle with wound/healing and return turns", ["oracle_heading", "lament_to_restoration", "closure"]),
            31: ("consolation_poetry_and_covenant_oracle", "Consolation poems, return images, and covenant discourse", ["refrain", "poetic_insert", "covenant_turn", "closure"]),
            32: ("sign_act_purchase_and_prayer", "Field purchase sign-act, prayer, and restoration oracle", ["narrative_frame", "purchase_sign", "prayer", "oracle_response"]),
            33: ("restoration_and_dynastic_oracle", "Restoration, city, and covenant/dynastic oracle closure", ["oracle_heading", "city_restoration", "covenant_formula", "closure"]),
        }
        return table[ch] + (["Hebrew prose/poetry shifts, document formulae, and textual-order variants require review"], ["Test chronology and parallel Kings material as context only, never as seam authority"])
    raise ValueError(book)


def main() -> int:
    changed = 0
    for book, lo, hi in (("Isa", 1, 12), ("Jer", 26, 33)):
        path = BASE / book / "chunks.jsonl"
        rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
        for row in rows:
            ch = int(row["span"].split(".", 2)[1].split("-", 1)[0])
            if not lo <= ch <= hi:
                continue
            form, title, seams, lang, red = classify(book, ch)
            row["literature_type_guess"] = form
            row["working_title"] = title
            row["working_title_origin"] = "isa_jer_prophetic_wave_v1"
            row["working_title_is_boundary_authority"] = False
            row["boundary_rationale"] = "Chapter-sized outer candidate retained provisionally; local oracle, song, sign-act, prose, and poetic transitions require independent review."
            row["candidate_internal_seams"] = seams
            row["original_language_translation_holds"] = lang
            row["red_team_premortem_holds"] = red
            row["review_revision"] = int(row.get("review_revision", 0)) + 1
            row["candidate_only"] = True
            row["non_authorizing"] = True
            refs = list(row.get("boundary_evidence_refs") or [])
            if "isa_jer_prophetic_wave.v1" not in refs:
                refs.append("isa_jer_prophetic_wave.v1")
            row["boundary_evidence_refs"] = refs
            changed += 1
        path.write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows), encoding="utf-8", newline="\n")
    print(json.dumps({"books": ["Isa", "Jer"], "rows_changed": changed, "spans_unchanged": True, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
