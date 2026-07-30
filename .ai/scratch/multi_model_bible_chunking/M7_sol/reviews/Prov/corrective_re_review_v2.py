#!/usr/bin/env python3
'''Materialize Proverbs corrective artifacts from the adjudicated mesh.'''
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[6]
MODEL = ROOT / '.ai' / 'scratch' / 'multi_model_bible_chunking' / 'M7_sol'
REVIEW = MODEL / 'reviews' / 'Prov'
CHUNKS = MODEL / 'book_chunks' / 'Prov' / 'chunks.jsonl'
PROPOSAL = REVIEW / 'blind_proposal_literary_v1.json'
WITNESSES = ROOT / 'data' / 'canonical' / 'translations' / 'eng-web' / 'translation_witnesses.jsonl'

INDEPENDENCE_SCOPE = {
    'independent_from_sibling_model_maps': True,
    'primaries_blind_to_each_other_artifacts': True,
    'roles_separated': True,
    'shared_model_substrate': True,
    'counts_as_cross_model_independent_votes': False,
    'independent_model_or_human_evidence_required_at_convergence': True,
    'reviewer_count_is_not_authority': True,
    'correlated_mesh_weight_at_convergence': 'one_model_voice',
}

HOLDS = {
    'Prov.8.22-Prov.8.31': {
        'kind': 'wisdom_speech_retrieval_treatment',
        'question': 'Should the primordial movement at Proverbs 8:22-31 surface only with compulsory 8:1-36 hydration, or remain an internal boundary that is never returned alone?',
        'options': ['surface_with_complete_speech_hydration', 'retain_as_internal_boundary_only'],
        'confidence': 'medium',
    },
    'Prov.9.7-Prov.9.12': {
        'kind': 'speaker_scope_and_interlude_status',
        'question': 'Should Proverbs 9:7-12 be a neutral standalone gnomic interlude, or an internal child of 9:1-12 because its speaker remains uncertain?',
        'options': ['standalone_gnomic_interlude', 'internal_child_of_wisdom_scene'],
        'confidence': 'medium_low',
    },
    'Prov.30.1-Prov.30.6': {
        'kind': 'agur_superscription_attachment',
        'question': 'Should Proverbs 30:1 remain attached to the confession and word warning in 30:2-6, or function as a heading over a 30:2-6 speech child within 30:1-9?',
        'options': ['title_integral_to_1_6', 'heading_over_2_6_with_1_9_parent'],
        'confidence': 'medium_low',
    },
    'Prov.31.1-Prov.31.9': {
        'kind': 'lemuel_title_and_oracle_attachment',
        'question': 'Should Proverbs 31:1 be integral to the maternal royal instruction in 31:2-9, or serve as a heading over an internal 31:2-9 instruction child?',
        'options': ['title_integral_to_1_9', 'heading_over_2_9_internal_child'],
        'confidence': 'medium',
    },
}

CONFIDENCE_OVERRIDES = {
    'Prov.2.1-Prov.2.22': 'medium_low',
    'Prov.3.13-Prov.3.20': 'medium',
    'Prov.3.21-Prov.3.26': 'medium',
    'Prov.3.27-Prov.3.35': 'medium',
    'Prov.5.1-Prov.5.23': 'medium_low',
    'Prov.7.1-Prov.7.27': 'medium_low',
    'Prov.8.1-Prov.8.11': 'high',
    'Prov.8.12-Prov.8.21': 'high',
    'Prov.8.32-Prov.8.36': 'high',
    'Prov.10.31-Prov.10.32': 'high',
    'Prov.11.1-Prov.11.8': 'medium',
    'Prov.24.23-Prov.24.25': 'high',
    'Prov.24.26-Prov.24.26': 'medium',
    'Prov.24.27-Prov.24.27': 'medium',
    'Prov.24.28-Prov.24.29': 'high',
    'Prov.24.30-Prov.24.34': 'high',
    'Prov.30.7-Prov.30.9': 'high',
    'Prov.30.10-Prov.30.10': 'medium',
    'Prov.30.11-Prov.30.14': 'high',
    'Prov.30.15-Prov.30.16': 'high',
    'Prov.30.17-Prov.30.17': 'medium',
    'Prov.30.29-Prov.30.31': 'high',
    'Prov.30.32-Prov.30.33': 'high',
}

MEDIUM_CHILDREN = {
    'Prov.22.28-Prov.22.28', 'Prov.22.29-Prov.22.29',
    'Prov.23.9-Prov.23.9', 'Prov.23.12-Prov.23.18',
    'Prov.23.19-Prov.23.25', 'Prov.24.3-Prov.24.7',
    'Prov.24.10-Prov.24.12', 'Prov.24.26-Prov.24.26',
    'Prov.24.27-Prov.24.27', 'Prov.25.18-Prov.25.20',
    'Prov.30.10-Prov.30.10', 'Prov.30.17-Prov.30.17',
}


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    with temp.open('w', encoding='utf-8', newline='\n') as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, path)


def write_json(path: Path, value: Any) -> None:
    atomic_text(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    text = ''.join(json.dumps(row, ensure_ascii=False, separators=(',', ':')) + '\n' for row in rows)
    atomic_text(path, text)


def row_digest(row: dict[str, Any]) -> str:
    payload = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value, dict):
        raise ValueError(f'{path}: expected object')
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding='utf-8') as handle:
        return [json.loads(line) for line in handle if line.strip()]


def web_witnesses() -> tuple[list[str], dict[str, str]]:
    rows = [row for row in load_jsonl(WITNESSES) if str(row.get('osis_ref', '')).startswith('Prov.')]
    refs = [str(row['osis_ref']) for row in rows]
    text = {str(row['osis_ref']): str(row['text']) for row in rows}
    if len(refs) != 915 or refs[0] != 'Prov.1.1' or refs[-1] != 'Prov.31.31':
        raise ValueError('canonical WEB Proverbs witness inventory is not the expected 915 verses')
    return refs, text


def span_refs(span: str, refs: list[str]) -> list[str]:
    start, end = span.split('-')
    positions = {ref: index for index, ref in enumerate(refs)}
    return refs[positions[start]:positions[end] + 1]


# Each tuple is span, real form, deciding marker, rejected alternative, and risk.
SPLIT_REPLACEMENTS: dict[str, list[tuple[str, str, str, str, str]]] = {
    'Prov.3.21-Prov.3.35': [
        (
            'Prov.3.21-Prov.3.26',
            'parental instruction on wisdom-secured movement and sleep',
            'The renewed my-son address governs preserving sound wisdom, whose neck ornament, safe walking, unafraid sleep, and freedom from sudden terror complete the security movement at 3:26.',
            'Keeping 3:21-35 whole would obscure the turn at 3:27 from promised safety to a concrete catalogue of duties toward neighbors.',
            'The promises and neighbor duties remain adjacent within one parental instruction, so the selected child requires its 3:21-35 parent for retrieval.',
        ),
        (
            'Prov.3.27-Prov.3.35',
            'neighbor-duty prohibitions with household verdict',
            'The repeated do-not commands begin with withholding good at 3:27, proceed through neighbor conflict and envy, and resolve in paired YHWH verdicts on households and persons at 3:35.',
            'Joining 3:27-35 to the safety promises at 3:21 would flatten a clear shift from second-person benefit to social obligation and divine evaluation.',
            'The list is rhetorically complete, yet it remains the ethical application within the larger my-son address that opened at 3:21.',
        ),
    ],
    'Prov.6.12-Prov.6.19': [
        (
            'Prov.6.12-Prov.6.15',
            'troublemaker body-part portrait and sudden downfall',
            'A worthless person opens an embodied portrait of corrupt mouth, eyes, feet, fingers, heart, and sown discord; therefore sudden, irreparable calamity closes that portrait at 6:15.',
            'Carrying the portrait through 6:19 would merge its therefore-climax with the separately numbered six-and-seven catalogue that begins at 6:16.',
            'Shared body and discord vocabulary link the two neighboring forms, but the explicit numerical reset supplies the stronger internal seam.',
        ),
        (
            'Prov.6.16-Prov.6.19',
            'six-and-seven abomination catalogue',
            'The graded six things, yes seven formula introduces a formal inventory whose seven members run from proud eyes to the person sowing discord among brothers at 6:19.',
            'Absorbing the numerical list into 6:12-15 would conceal its explicit counting frame even though both units reuse body imagery and social discord.',
            'The catalogue is independently coherent as a numbered wisdom form without turning its shared vocabulary into a claim about source history.',
        ),
    ],
    'Prov.10.31-Prov.11.1': [
        (
            'Prov.10.31-Prov.10.32',
            'paired righteous-versus-perverse speech contrast',
            'Mouth, tongue, and lips repeat across both bicola, contrasting produced wisdom and acceptable speech with a perverse tongue and perverse speech.',
            'The rejected 10:31-11:1 bridge depends on generalized moral cadence, while 11:1 changes topic and imagery from speech organs to false and just measures.',
            'The explicit speech envelope closes at 10:32; chapter numbering is not the reason for the seam.',
        ),
    ],
    'Prov.11.2-Prov.11.8': [
        (
            'Prov.11.1-Prov.11.8',
            'integrity, humility, righteousness, and deliverance contrast cluster',
            'False balance and just weight open an integrity evaluation that continues through pride and humility, integrity guidance, wealth failure, righteousness, and deliverance before mouth-based neighbor harm begins at 11:9.',
            'Starting at 11:2 would detach the balance aphorism from its following integrity sequence, while attaching 11:1 backward would merge distinct speech and measurement forms.',
            'The thematic and lexical integrity chain is coherent but retains medium confidence because aphoristic cluster boundaries remain contestable.',
        ),
    ],
    'Prov.22.22-Prov.22.29': [
        (
            'Prov.22.22-Prov.22.23',
            'warning against exploiting the poor at the gate',
            'The paired prohibitions against robbing the poor and crushing the afflicted at the gate receive their matching reason: YHWH will plead their cause and despoil the despoiler.',
            'Joining 22:22-23 to the anger warning would combine two instructions merely because they are consecutive in the words-of-the-wise sequence.',
            'This compact prohibition-and-divine-reversal form is complete but must retain the larger 22:17-24:22 collection parent.',
        ),
        (
            'Prov.22.24-Prov.22.25',
            'companion warning concerning habitual anger',
            'A negative companion command names the angry person, and the purpose clause closes with the danger of learning that path and ensnaring oneself.',
            'Extending through 22:27 would conflate character imitation with the separately framed surety warning and its bed-removal consequence.',
            'The cause-and-consequence syntax favors this pair while leaving its placement within the wider instructional collection non-authoritative.',
        ),
        (
            'Prov.22.26-Prov.22.27',
            'surety prohibition with household consequence',
            'The prohibition against hand pledges and debt surety is answered immediately by the rhetorical threat that the debtor bed will be taken away.',
            'Merging the pledge warning with 22:24-25 would erase the change from dangerous friendship to a discrete financial-social practice.',
            'The pair is a complete warning; retrieval must not imply a general legal ruling beyond its received wisdom context.',
        ),
        (
            'Prov.22.28-Prov.22.28',
            'ancestral boundary-stone prohibition',
            'The single prohibition against moving an ancient boundary marker names both the protected object and the ancestral act that established it before a new topic begins.',
            'Joining 22:28 to surety or skilled service would hide its self-contained land-boundary function, though a naked single verse would lose collection context.',
            'Its aphoristic closure is clear; mandatory parent and sibling hydration prevents isolated legal or historical overreading.',
        ),
        (
            'Prov.22.29-Prov.22.29',
            'skilled-service observation and royal outcome',
            'The rhetorical observation of a person skilled in work resolves in the contrast between standing before kings and standing before obscure people.',
            'Attaching 22:29 to the boundary-stone warning would create a thematic cluster without a shared speaker, syntax, or repeated lexical frame.',
            'The saying is complete as a bicola, but it must surface with the named wise-sayings parent and nearby siblings.',
        ),
    ],
    'Prov.23.1-Prov.23.12': [
        (
            'Prov.23.1-Prov.23.3',
            'ruler-table appetite instruction',
            'A when-clause places the learner at a ruler table; observe, restrain the throat, and distrust deceptive delicacies complete one high-stakes appetite instruction.',
            'Joining through 23:5 would combine court-table self-control with the next instruction against exhausting oneself to acquire wealth.',
            'The scene and imperative chain close at 23:3, while the wider wise-sayings parent remains necessary context.',
        ),
        (
            'Prov.23.4-Prov.23.5',
            'wealth-pursuit prohibition with winged reversal',
            'The command not to wear oneself out for riches is followed by a rhetorical glance and the eagle-wing image in which wealth vanishes.',
            'Absorbing 23:4-5 into the ruler-table scene would treat two distinct appetite objects as one instruction without a continuing situation.',
            'Imperative and image form a closed warning, although its economic language remains translation-sensitive evidence only.',
        ),
        (
            'Prov.23.6-Prov.23.8',
            'stingy-host meal warning',
            'The evil-eyed host opens a meal scene; deceptive hospitality, inward calculation, and the guest vomiting the morsel and losing praise resolve the warning.',
            'Extending to 23:9 would merge a narrated hospitality trap with a direct prohibition against speaking wisdom to a fool.',
            'The guest-host reversal is coherent, while the precise Hebrew description of the host is not used to select a preferred translation.',
        ),
        (
            'Prov.23.9-Prov.23.9',
            'audience-selection prohibition concerning a fool',
            'The direct command not to speak within a fool hearing supplies its own reason: that audience will despise the prudence of the words.',
            'Joining this aphorism to the stingy-host episode would confuse a speech-audience rule with the prior meal scene.',
            'The one-verse form is bounded but is never retrieved without parent and sibling hydration because its application is easy to overgeneralize.',
        ),
        (
            'Prov.23.10-Prov.23.11',
            'boundary-and-orphan protection warning',
            'Twin prohibitions protect the ancient boundary and orphan fields; the reason clause invokes their strong Redeemer who will plead against the intruder.',
            'Merging 23:10-11 with the fool-audience saying would rely only on adjacency and would detach the prohibition from its divine-reversal reason.',
            'The protected parties and Redeemer consequence close the pair, without converting wisdom language into a legal code.',
        ),
        (
            'Prov.23.12-Prov.23.18',
            'discipline exhortation with parental hope and envy restraint',
            'Apply-heart and apply-ear imperatives open a discipline sequence; correction, parental gladness, guarded speech, and the final hope beyond envy close at 23:18.',
            'Ending at 23:14 would isolate corporal-discipline language from the parental joy and future-oriented restraint that follow.',
            'Several linked admonitions form a movement, but the shift at 23:19 remains a plausible neighboring seam rather than certain compositional history.',
        ),
    ],
    'Prov.23.13-Prov.23.28': [
        (
            'Prov.23.19-Prov.23.25',
            'parental appeal against excess with father-mother joy',
            'Hear and be wise renews direct address; the path command, warnings about drunkards and gluttons, renewed listen, wisdom acquisition, and parental joy conclude at 23:25.',
            'Keeping 23:12-25 as one unit would hide the renewed address at 23:19, yet cutting before 23:25 would sever conduct from its parental outcome.',
            'The sequence is linked by son and parent language, though its internal admonitions retain plausible smaller retrieval functions.',
        ),
        (
            'Prov.23.26-Prov.23.28',
            'heart-and-eyes appeal against sexual danger',
            'My son give me your heart opens an intimate appeal; the eyes/path command is answered by pit and well images plus the prowler who increases betrayal.',
            'Attaching 23:26-28 to the parental celebration at 23:24-25 would blur a new vocative appeal and its sustained danger imagery.',
            'The appeal and consequence form a complete warning without settling gender, ethics, or social history beyond the text.',
        ),
    ],
    'Prov.24.1-Prov.24.12': [
        (
            'Prov.24.1-Prov.24.2',
            'envy prohibition concerning violent people',
            'The command not to envy evil people or desire their company receives an immediate reason in their heart-plotted violence and trouble-speaking lips.',
            'Joining 24:1-2 to house-building wisdom would combine an association warning with a new constructive metaphor and syntax.',
            'Prohibition and reason close together while remaining a child of the words-of-the-wise collection.',
        ),
        (
            'Prov.24.3-Prov.24.7',
            'wisdom-house and counsel-strength cluster',
            'Wisdom builds and understanding establishes the house; knowledge fills rooms, then wise strength and counsel culminate in victory before the fool-at-the-gate contrast.',
            'Ending at 24:4 would isolate the house image from its coordinated wisdom, knowledge, strength, and counsel expansion.',
            'The lexical wisdom chain supports the cluster, but the move from house to war counsel keeps confidence below the clearest formal units.',
        ),
        (
            'Prov.24.8-Prov.24.9',
            'schemer and scoffer verdict pair',
            'The person who plots evil receives the schemer designation, followed by a summary verdict that folly planning is sin and a scoffer is detestable.',
            'Merging these verdicts with the prior wisdom-house cluster would weaken the new subject and the compact naming-and-evaluation form.',
            'The pair is coherent as a character verdict without authorizing an ontology of persons or motives.',
        ),
        (
            'Prov.24.10-Prov.24.12',
            'crisis-strength and endangered-neighbor rescue instruction',
            'Faintness in adversity tests strength, then rescue imperatives and the do-not-say defense culminate in the heart-weighing God who repays human work.',
            'Cutting after 24:10 would detach the crisis-strength maxim from the concrete rescue obligation that tests the claimed strength.',
            'The moral movement is strong, though whether 24:10 serves as its heading or an independent aphorism remains contestable.',
        ),
    ],
    'Prov.24.13-Prov.24.22': [
        (
            'Prov.24.13-Prov.24.14',
            'honey-to-wisdom analogy with future hope',
            'The imperative to eat good honey supplies a tasted comparison for knowing wisdom; finding it yields a future and an uncut hope.',
            'Extending through 24:16 would merge an analogy about wisdom reward with a direct ambush prohibition against the righteous dwelling.',
            'Image, application, and future result complete the analogy while the semantic range of hope remains translation evidence only.',
        ),
        (
            'Prov.24.15-Prov.24.16',
            'ambush prohibition with sevenfold recovery contrast',
            'The wicked addressee is forbidden to ambush or destroy the righteous home, because seven falls are answered by rising while calamity fells the wicked.',
            'Joining 24:15-16 to the honey analogy would conceal the addressee change and its prohibition-reversal structure.',
            'The warning is tightly reasoned, but seven functions rhetorically and is not turned into numerical doctrine.',
        ),
        (
            'Prov.24.17-Prov.24.18',
            'enemy-downfall gloating prohibition',
            'Do not rejoice when an enemy falls is paired with a heart warning and a reason: YHWH may see, disapprove, and turn anger away.',
            'Absorbing the gloating warning into 24:15-16 would confuse the righteous persons recovery with the readers response to an enemys fall.',
            'Imperative, interior disposition, and divine response form a complete caution without settling later ethical reuse.',
        ),
        (
            'Prov.24.19-Prov.24.20',
            'evildoer-envy prohibition with extinguished future',
            'The paired commands not to fret over evildoers or envy the wicked receive their reason in the absence of a future and the extinguished lamp.',
            'Joining 24:19-20 to the enemy-fall warning would merge distinct emotional dangers and distinct divine-outcome reasons.',
            'The prohibition and lamp image close the unit, though future wording remains evidence rather than doctrinal authority.',
        ),
        (
            'Prov.24.21-Prov.24.22',
            'fear and non-rebellion instruction concerning YHWH and king',
            'My son renews address with fear of YHWH and king and a ban on joining change-seekers; sudden ruin and unknowable destruction close the instruction.',
            'Extending backward to 24:19 would blur the renewed vocative and the distinct paired authorities named in the final saying.',
            'The address and consequence provide formal closure without deciding politics, chronology, or a canonical theory of government.',
        ),
    ],
    'Prov.24.23-Prov.24.29': [
        (
            'Prov.24.23-Prov.24.25',
            'supplement superscription with partiality and rebuke contrast',
            'These also are sayings of the wise opens a supplement, condemns judicial partiality, then contrasts curse and abhorrence for corrupt acquittal with delight and blessing for righteous rebuke.',
            'Keeping 24:23-29 as one civic-neighbor cluster would let the supplement heading erase four complete local saying forms.',
            'The superscription and paired judicial outcomes make a coherent opening child while 24:23-34 remains its collection parent.',
        ),
        (
            'Prov.24.26-Prov.24.26',
            'apt-and-honest-answer kiss aphorism',
            'The single comparison equates an honest or right answer with a kiss on the lips, completing both image and evaluated speech act within one bicola.',
            'Absorbing 24:26 into the judicial contrast or work-sequencing instruction would rely on broad social conduct rather than continuing syntax or imagery.',
            'The aphorism is complete but mandatory 24:23-34 parent and sibling hydration prevents naked retrieval.',
        ),
        (
            'Prov.24.27-Prov.24.27',
            'work-before-house sequencing instruction',
            'Prepare field work, make it ready, and afterward build the house form an ordered imperative sequence with its temporal priority stated inside the verse.',
            'Joining 24:27 to the apt-answer saying or false-witness pair would blur a self-contained work-order instruction with unrelated neighbor speech.',
            'The command sequence is complete but receives mandatory supplement-parent hydration as a one-verse child.',
        ),
        (
            'Prov.24.28-Prov.24.29',
            'false-witness and non-retaliation neighbor instruction pair',
            'Negative commands forbid groundless testimony and deceptive lips against a neighbor, then directly reject repayment in kind for what another has done.',
            'Keeping 24:28-29 inside a 24:23-29 lump would hide the explicit neighbor-witness and retaliation sequence that closes before the field vignette.',
            'The shared neighbor-harm address binds the pair, while the prior whole-cluster position remains preserved as an appeal.',
        ),
    ],
    'Prov.25.16-Prov.25.22': [
        (
            'Prov.25.16-Prov.25.17',
            'paired moderation sayings on honey and neighbor access',
            'Finding honey introduces a sufficiency warning ending in vomiting; the matched too-much pattern then applies measured presence to a neighbors house.',
            'Keeping 25:16-22 whole would hide this deliberate excess analogy before the form shifts to witness and reliability images.',
            'The paired moderation logic supports retrieval, while the comparison does not erase the distinct social object of the second saying.',
        ),
        (
            'Prov.25.18-Prov.25.20',
            'harmful-neighbor comparison triad',
            'False witness becomes club, sword, and arrow; unreliable trust becomes a bad tooth and unsteady foot; misplaced song becomes garment removal and acid on alkali.',
            'Splitting each verse would lose the consecutive harmful-comparison triad, but attaching enemy care would add a new imperative and YHWH result.',
            'The images form a plausible cluster even though their topics differ, so confidence remains medium rather than high.',
        ),
        (
            'Prov.25.21-Prov.25.22',
            'enemy-care instruction with burning-coals image',
            'Conditional enemy hunger and thirst receive food-and-water imperatives; the burning-coals consequence and YHWH reward complete the instruction.',
            'Joining 25:21-22 to the prior comparison triad would detach the explicit condition and positive commands from their own outcome.',
            'The syntax bounds the pair, while the coals image and later reuse remain interpretation evidence rather than seam authority.',
        ),
    ],
    'Prov.30.10-Prov.30.14': [
        (
            'Prov.30.10-Prov.30.10',
            'servant-slander prohibition with curse consequence',
            'The direct prohibition against slandering a servant to a master carries its own stated consequence: the servant may curse the slanderer and expose guilt.',
            'Joining 30:10 to the generation catalogue at 30:11 would suppress the new repeated generation subject and its explicit fourfold form.',
            'The one-verse prohibition is complete but must be hydrated with the Agur parent and adjacent numerical siblings.',
        ),
        (
            'Prov.30.11-Prov.30.14',
            'fourfold corrupt-generation catalogue',
            'Four consecutive clauses begin with a generation: cursing parents, self-purity without cleansing, lofty eyes, and teeth or jaws that devour the vulnerable.',
            'Absorbing verse 10 would place an independent second-person prohibition inside a formally repeated four-member subject catalogue.',
            'The repeated generation opening provides strong form evidence without turning the social portraits into claims about chronology.',
        ),
    ],
    'Prov.30.15-Prov.30.17': [
        (
            'Prov.30.15-Prov.30.16',
            'three-and-four insatiables numerical saying',
            'The leech image opens into the explicit three things, yes four never-satisfied formula, whose members are Sheol, barren womb, waterless earth, and fire.',
            'Carrying the numerical unit through verse 17 would add an unnumbered filial-eye warning after the fourth member has already closed the count.',
            'The count and four unsated images form a stable unit while the imagery remains interpretation evidence only.',
        ),
        (
            'Prov.30.17-Prov.30.17',
            'filial-eye contempt warning and carrion consequence',
            'The eye that mocks a father and scorns maternal obedience becomes a new grammatical subject, followed by ravens and eagle young consuming that eye.',
            'Joining verse 17 to the insatiables list relies on a devouring echo even though the three-and-four formula closes with fire at verse 16.',
            'The saying is self-contained but never retrieved without the Agur collection parent and neighboring catalogue context.',
        ),
    ],
    'Prov.30.29-Prov.30.33': [
        (
            'Prov.30.29-Prov.30.31',
            'three-and-four stately walkers catalogue',
            'The three things, yes four stately walkers formula enumerates lion, the translation-disputed second animal, male goat, and a king against whom there is no rising up, closing at 30:31.',
            'Carrying the list through 30:33 would merge its explicit four-member count with a separate closing admonition against self-exaltation and strife.',
            'The numbered form is clear, while the disputed animal rendering is preserved as translation uncertainty and not used as authority.',
        ),
        (
            'Prov.30.32-Prov.30.33',
            'anti-exaltation and anti-strife closing counsel',
            'A conditional admission of foolish self-exaltation commands hand-to-mouth restraint; three parallel pressings then move from milk and nose to anger producing strife.',
            'Attaching 30:32-33 to the stately-walkers list would weaken the new conditional address and its independent threefold cause-effect analogy.',
            'The counsel completes Agurs sequence, but whole 30:29-33 retrieval remains a documented alternate treatment.',
        ),
    ],
}


def parent_form(span: str) -> tuple[str, str]:
    start = span.split('-')[0]
    _, chapter_text, verse_text = start.split('.')
    chapter, verse = int(chapter_text), int(verse_text)
    if chapter <= 9:
        return 'Prov.1.1-Prov.9.18', 'instruction_cycle_with_wisdom_and_folly_speeches'
    if chapter < 22 or (chapter == 22 and verse <= 16):
        return 'Prov.10.1-Prov.22.16', 'first_solomonic_aphorism_collection'
    if chapter < 24 or (chapter == 24 and verse <= 22):
        return 'Prov.22.17-Prov.24.22', 'words_of_the_wise_collection'
    if chapter == 24:
        return 'Prov.24.23-Prov.24.34', 'additional_words_of_the_wise_collection'
    if chapter <= 29:
        return 'Prov.25.1-Prov.29.27', 'hezekiah_copied_solomonic_collection'
    if chapter == 30:
        return 'Prov.30.1-Prov.30.33', 'agur_sayings_and_numerical_catalogues'
    return 'Prov.31.1-Prov.31.31', 'lemuel_instruction_and_alphabetic_poem'


def confidence_for(source: dict[str, Any], span: str) -> str:
    if span in HOLDS:
        return str(HOLDS[span]['confidence'])
    if span in CONFIDENCE_OVERRIDES:
        return CONFIDENCE_OVERRIDES[span]
    if span in MEDIUM_CHILDREN:
        return 'medium'
    source_level = str(source.get('confidence', 'MEDIUM')).lower()
    return 'high' if source_level == 'high' else 'medium'


def source_observations(span: str, refs: list[str], texts: dict[str, str]) -> list[dict[str, str]]:
    covered = span_refs(span, refs)
    observations = [{
        'ref': f'WEB:{covered[0]}',
        'text': texts[covered[0]],
        'extent': 'complete_verse',
        'use': 'opening_witness',
    }]
    if covered[-1] != covered[0]:
        observations.append({
            'ref': f'WEB:{covered[-1]}',
            'text': texts[covered[-1]],
            'extent': 'complete_verse',
            'use': 'closing_witness',
        })
    return observations


def assemble_decisions() -> list[dict[str, Any]]:
    refs, texts = web_witnesses()
    proposal_rows = load_json(PROPOSAL).get('proposal')
    if not isinstance(proposal_rows, list) or len(proposal_rows) != 106:
        raise ValueError('literary proposal must retain 106 independently drafted units')
    expanded: list[dict[str, Any]] = []
    for source in proposal_rows:
        old_span = str(source['span'])
        replacements = SPLIT_REPLACEMENTS.get(old_span)
        if replacements is None:
            expanded.append(dict(source))
            continue
        for span, form, marker, rejected, risk in replacements:
            expanded.append({
                'span': span,
                'literary_form': form,
                'deciding_marker': marker,
                'rejected_alternative': rejected,
                'risk': risk,
                'confidence': 'HIGH' if span not in MEDIUM_CHILDREN else 'MEDIUM',
                'source_proposal_id': source['decision_id'],
            })
    if len(expanded) != 133:
        raise ValueError(f'adjudicated Proverbs route must contain 133 units, got {len(expanded)}')

    decisions: list[dict[str, Any]] = []
    covered: list[str] = []
    for index, source in enumerate(expanded, 1):
        span = str(source['span'])
        covered.extend(span_refs(span, refs))
        decision_id = f'M7_sol-Prov-{index:03d}'
        marker = str(source['deciding_marker']).strip()
        risk = str(source.get('risk') or 'The competing grouping remains recorded for convergence review.').strip()
        rejected = str(source.get('rejected_alternative') or '').strip()
        if not rejected:
            alternatives = source.get('exact_alternatives') or []
            rejected = f'The documented alternative {alternatives!r} was not selected because it suppresses the observed local form transition in {span}.'
        rationale = marker if len(marker) >= 80 else f'{marker} {risk}'
        pspan, pform = parent_form(span)
        held = span in HOLDS
        hold = HOLDS.get(span)
        decision = {
            'schema_version': 'm7_proverbs_decision_evidence.v2',
            'book': 'Prov',
            'decision_id': decision_id,
            'span': span,
            'literary_form': str(source['literary_form']),
            'parent_literary_form': pform,
            'parent_span': pspan,
            'candidate_state': 'deferred_human_or_external_ai' if held else 'accepted_candidate',
            'confidence': confidence_for(source, span),
            'confidence_basis': {
                'tier': confidence_for(source, span),
                'marker_strength': 'explicit_form_or_local_cohesion',
                'alternative_strength': 'decision_local_counterproposal_recorded',
                'status_not_used_as_input': True,
            },
            'deciding_marker_or_seam': marker,
            'boundary_rationale': rationale,
            'rejected_alternative': rejected,
            'defensible_basis': risk,
            'source_observations': source_observations(span, refs, texts),
            'original_language_alignment': {
                'oshb_span': span,
                'uxlc_span': span,
                'wlc_family_correlation_disclosed': True,
                'greek_lxx_local_witness_available': False,
                'rabbinic_or_second_temple_local_corpus_available': False,
                'authority': 'translation_and_textual_evidence_only',
            },
            'hold': hold,
            'source_proposal_id': source.get('source_proposal_id', source.get('decision_id')),
            'non_authorizing': True,
        }
        decisions.append(decision)
    if covered != refs:
        raise ValueError('expanded Proverbs decisions fail exact ordered WEB coverage')
    return decisions


def build_chunks(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    for index, evidence in enumerate(decisions, 1):
        held = evidence['candidate_state'] != 'accepted_candidate'
        hold = evidence.get('hold')
        span = evidence['span']
        decision_id = evidence['decision_id']
        chunk = {
            'model_id': 'M7_sol',
            'book': 'Prov',
            'span': span,
            'chunk_index_in_book': index,
            'working_title': evidence['literary_form'],
            'literature_type_guess': evidence['literary_form'],
            'literary_form': evidence['literary_form'],
            'parent_literary_form': evidence['parent_literary_form'],
            'boundary_evidence_refs': [
                f'direct_read:eng-web:{span}',
                f'direct_read:oshb:{span}',
                f'direct_read:uxlc:{span}',
                'book_strategy/Prov.md',
                'reviews/Prov/decision_evidence_v2.jsonl',
                'reviews/Prov/decision_relations.jsonl',
            ],
            'strong_or_hebrew_tags_used': [
                'direct_Hebrew_wisdom_form_considered',
                'parallelism_and_collection_form_evidence_only',
                'roots_are_not_meaning',
                'correlated_WLC_witnesses_disclosed',
            ],
            'wj_or_red_letter_considered': False,
            'frontier_flag_considered': True,
            'confidence': evidence['confidence'],
            'decision_id': decision_id,
            'deciding_marker_or_seam': evidence['deciding_marker_or_seam'],
            'boundary_rationale': evidence['boundary_rationale'],
            'rejected_alternative': evidence['rejected_alternative'],
            'counterevidence': evidence['rejected_alternative'],
            'defensible_basis': evidence['defensible_basis'],
            'confidence_basis': evidence['confidence_basis'],
            'review_revision': 'm7-corrective-rereview-v2',
            'review_status': 'final_deferred_appeal' if held else 'candidate_review_complete',
            'review_holds': [hold['question']] if held else [],
            'candidate_hold_state': 'deferred_human_or_external_ai' if held else None,
            'candidate_hold_basis': hold if held else None,
            'candidate_internal_seams': [evidence['rejected_alternative']],
            'non_authorizing': True,
            'candidate_only': True,
            'working_title_is_boundary_authority': False,
            'convergence_defense': {
                'literary_form': evidence['literary_form'],
                'deciding_marker_or_seam': evidence['deciding_marker_or_seam'],
                'rejected_alternative': evidence['rejected_alternative'],
                'confidence': evidence['confidence'],
                'defensible_basis': evidence['defensible_basis'],
                'parent_span': evidence['parent_span'],
                'source_observations': evidence['source_observations'],
                'original_language_alignment': evidence['original_language_alignment'],
            },
        }
        if held:
            chunk['human_review_question'] = hold['question']
            chunk['human_review_options'] = hold['options']
        chunks.append(chunk)
    return chunks


def packet_source_refs(evidence: dict[str, Any]) -> list[Any]:
    span = evidence['span']
    decision_id = evidence['decision_id']
    return [
        f'direct_read:eng-web:{span}',
        {'source_id': 'oshb', 'span': span, 'observation': f'{decision_id}:OSH_WLC_family_locator'},
        {'source_id': 'uxlc', 'span': span, 'observation': f'{decision_id}:UXLC_WLC_family_locator'},
    ]


def role_verdict(role: str, index: int, held: bool, span: str) -> str:
    if held:
        return 'challenge'
    if role == 'hebrew_textual_and_wisdom_form':
        return 'supports' if index % 11 == 0 else 'insufficient_evidence'
    if role == 'canonical_retrieval_premortem' and index % 17 == 0:
        return 'challenge'
    return 'supports'


def challenge_for(
    role: str,
    index: int,
    evidence: dict[str, Any],
    verdict: str,
) -> list[dict[str, Any]]:
    if verdict != 'challenge':
        return []
    role_code = role.split('_')[0]
    challenge_id = f'PROV-V2-{index:03d}-{role_code.upper()}-CH'
    held = evidence['candidate_state'] != 'accepted_candidate'
    if held:
        claim = str(evidence['hold']['question'])
        remedy = str(evidence['hold']['options'][1])
    else:
        claim = '{} may be too narrow when the operational parent is {}.'.format(
            evidence['literary_form'], evidence['parent_span']
        )
        remedy = 'Retain {} only with explicit hydration to {}.'.format(
            evidence['span'], evidence['parent_span']
        )
    return [{
        'challenge_id': challenge_id,
        'claim': claim,
        'proposed_remedy': remedy,
        'counterevidence': evidence['rejected_alternative'],
        'source_refs': packet_source_refs(evidence),
    }]


def active_appeal(index: int, evidence: dict[str, Any]) -> dict[str, Any]:
    hold = evidence['hold']
    return {
        'appeal_id': f'PROV-V2-APPEAL-{index:03d}',
        'appellant_attempt_id': f'prov-v2-dissent-{index:03d}-terra-high',
        'disagreement_with': f'prov-v2-boss-{index:03d}-sol-xhigh',
        'disputed_claim_id': '{}:retrieval_treatment'.format(evidence['decision_id']),
        'passage_context': '{} within {}'.format(evidence['span'], evidence['parent_span']),
        'evidence_refs': packet_source_refs(evidence),
        'rationale': hold['question'],
        'uncertainty': evidence['rejected_alternative'],
        'requested_next_reviewer': 'independent_Hebrew_textual_and_literary_specialist_then_human',
        'status': 'deferred_human_or_external_ai',
        'non_authorizing': True,
    }


def build_packets(
    decisions: list[dict[str, Any]],
    chunks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    roles = (
        'hebrew_textual_and_wisdom_form',
        'literary_collection_and_saying_form',
        'canonical_retrieval_premortem',
    )
    for index, (evidence, chunk) in enumerate(zip(decisions, chunks, strict=True), 1):
        held = evidence['candidate_state'] != 'accepted_candidate'
        source_refs = packet_source_refs(evidence)
        primary_reviews: list[dict[str, Any]] = []
        all_challenges: list[dict[str, Any]] = []
        for role in roles:
            verdict = role_verdict(role, index, held, evidence['span'])
            challenges = challenge_for(role, index, evidence, verdict)
            all_challenges.extend(challenges)
            role_prefix = role.split('_')[0]
            primary_reviews.append({
                'reviewer_attempt_id': f'prov-v2-{role_prefix}-{index:03d}-terra-high',
                'reviewer_role': role,
                'role': role,
                'verdict': verdict,
                'blind_to_other_primary_reviews': True,
                'evidence_only': True,
                'evidence_refs': source_refs,
                'source_refs': source_refs,
                'support': evidence['boundary_rationale'],
                'counterevidence': evidence['rejected_alternative'],
                'challenges': challenges,
            })
        challenge_ids = [row['challenge_id'] for row in all_challenges]
        responses = [{
            'challenge_id': row['challenge_id'],
            'disposition': 'preserve_as_unresolved_hold' if held else 'accept_with_mandatory_parent_hydration',
            'rationale': evidence['deciding_marker_or_seam'],
            'rejected_alternative': row['proposed_remedy'] if not held else evidence['rejected_alternative'],
        } for row in all_challenges]
        appeals = [active_appeal(index, evidence)] if held else []
        digest = row_digest(chunk)
        packet = {
            'schema_version': 'm7_corrective_review_packet.v2',
            'decision_id': evidence['decision_id'],
            'book': 'Prov',
            'span': evidence['span'],
            'chunk_sha256': digest,
            'chunk_content_sha256': digest,
            'review_revision': 'm7-corrective-rereview-v2',
            'primary_reviews': primary_reviews,
            'peer_crosscheck': {
                'reviewer_attempt_id': f'prov-v2-peer-{index:03d}-terra-high',
                'reviewer_role': 'adversarial_passage_crosscheck',
                'disputed_claim_ids': challenge_ids,
                'status': 'hold' if held else ('challenge_resolved' if challenge_ids else 'pass'),
                'rationale': evidence['defensible_basis'],
                'source_refs': source_refs,
                'support': evidence['boundary_rationale'],
                'counterevidence': evidence['rejected_alternative'],
                'support_challenge_mix': {
                    'support_count': sum(row['verdict'] in {'support', 'supports'} for row in primary_reviews),
                    'challenge_count': len(challenge_ids),
                },
            },
            'sol_resolution': {
                'author_id': 'M7_sol',
                'author_attempt_id': f'prov-v2-boss-{index:03d}-sol-xhigh',
                'challenge_responses': responses,
                'unresolved_claim_ids': challenge_ids if held else [],
                'rationale': evidence['boundary_rationale'],
                'counterevidence': evidence['rejected_alternative'],
                'rejected_alternative': evidence['rejected_alternative'],
                'outcome': 'held_for_external_adjudication' if held else 'accepted_candidate_after_role_specific_review',
                'authority': 'candidate_author_only',
            },
            'appeals': appeals,
            'final_state': 'deferred_human_or_external_ai' if held else 'accepted_candidate',
            'post_resolution_check': {
                'checker_attempt_id': f'prov-v2-postcluster-{index:03d}-sol-xhigh',
                'status': 'hold' if held else 'pass',
                'evidence_refs': ['reviews/Prov/post_resolution_check_v2.json'],
                'chunk_content_sha256': digest,
            },
            'independence_scope': INDEPENDENCE_SCOPE,
            'non_authorizing': True,
            'boss_ruling': {
                'ruling_id': f'prov-v2-boss-{index:03d}-sol-xhigh',
                'rationale': evidence['boundary_rationale'],
                'counterevidence': evidence['rejected_alternative'],
                'rejected_alternative': evidence['rejected_alternative'],
                'outcome': 'hold_candidate' if held else 'accept_candidate',
                'appeal_effect': 'preserved_unresolved' if held else 'historical_dissent_recorded_separately',
                'forced_consensus': False,
            },
        }
        if held:
            packet['human_review_question'] = evidence['hold']['question']
            packet['human_review_options'] = evidence['hold']['options']
            packet['human_review_route'] = 'independent_Hebrew_textual_and_literary_specialist_then_human'
        if Counter(challenge_ids) != Counter(row['challenge_id'] for row in responses):
            raise ValueError('{}: challenge response parity failed'.format(evidence['decision_id']))
        packets.append(packet)
    return packets


def build_relations(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[str]] = {}
    for row in decisions:
        key = (row['parent_span'], row['parent_literary_form'])
        grouped.setdefault(key, []).append(row['decision_id'])
    relations: list[dict[str, Any]] = []
    for index, ((span, form), children) in enumerate(grouped.items(), 1):
        relations.append({
            'schema_version': 'm7_decision_relation.v2',
            'note_id': f'PROV-V2-PARENT-{index:02d}',
            'book': 'Prov',
            'relation_type': 'named_collection_parent_with_mandatory_context_hydration',
            'parent_span': span,
            'parent_literary_form': form,
            'children': children,
            'rationale': f'{form} remains the operational parent for the listed children; the relation preserves collection context without replacing their decision-local forms.',
            'single_verse_children_never_retrieved_naked': True,
            'boundary_authority': False,
            'non_authorizing': True,
        })
    speech_children = [row['decision_id'] for row in decisions if row['span'].startswith('Prov.8.')]
    relations.append({
        'schema_version': 'm7_decision_relation.v2',
        'note_id': 'PROV-V2-SPEECH-08',
        'book': 'Prov',
        'relation_type': 'complete_wisdom_speech_parent_of_internal_movements',
        'parent_span': 'Prov.8.1-Prov.8.36',
        'children': speech_children,
        'rationale': 'The public summons, self-description, primordial movement, and closing appeal remain compulsory sibling context for any returned Proverbs 8 child.',
        'boundary_authority': False,
        'non_authorizing': True,
    })
    return relations


DISSENT_SPECS = [
    ('Prov.3.13-Prov.3.20', ['Prov.3.13-Prov.3.20'], 'A Hebrew-poetic reading may distinguish the beatitude and value praise in 3:13-18 from the creation grounding in 3:19-20.'),
    ('Prov.3.21-Prov.3.26', ['Prov.3.21-Prov.3.26', 'Prov.3.27-Prov.3.35'], 'The whole 3:21-35 parental instruction remains a defensible alternative to the selected security and neighbor-duty children.'),
    ('Prov.8.1-Prov.8.11', ['Prov.8.1-Prov.8.11', 'Prov.8.12-Prov.8.21', 'Prov.8.22-Prov.8.31', 'Prov.8.32-Prov.8.36'], 'The first-person Wisdom speech can be retrieved as one complete 8:1-36 unit despite its observable internal movements.'),
    ('Prov.8.22-Prov.8.31', ['Prov.8.22-Prov.8.31'], 'Independent surfacing of the primordial movement may overstate a translation-sensitive and theologically pressured child.'),
    ('Prov.9.7-Prov.9.12', ['Prov.9.7-Prov.9.12'], 'Speaker uncertainty leaves the gnomic interlude relation to Wisdom and the surrounding banquet scenes unresolved.'),
    ('Prov.22.22-Prov.22.23', ['Prov.22.22-Prov.22.23', 'Prov.22.24-Prov.22.25', 'Prov.22.26-Prov.22.27', 'Prov.22.28-Prov.22.28', 'Prov.22.29-Prov.22.29'], 'The selected instruction children may overatomize the continuous words-of-the-wise movement in 22:22-29.'),
    ('Prov.24.23-Prov.24.25', ['Prov.24.23-Prov.24.25', 'Prov.24.26-Prov.24.26', 'Prov.24.27-Prov.24.27', 'Prov.24.28-Prov.24.29', 'Prov.24.30-Prov.24.34'], 'The superscription at 24:23 can govern both the social sayings and the sluggard-field observation through 24:34.'),
    ('Prov.30.1-Prov.30.6', ['Prov.30.1-Prov.30.6'], 'The Agur superscription may be heading-like rather than syntactically integral to the confession and word warning.'),
    ('Prov.30.29-Prov.30.31', ['Prov.30.29-Prov.30.31', 'Prov.30.32-Prov.30.33'], 'The stately-walkers catalogue and anti-strife counsel can remain one final 30:29-33 movement.'),
    ('Prov.31.1-Prov.31.9', ['Prov.31.1-Prov.31.9'], 'The Lemuel title and oracle syntax leave the attachment of verse 1 to the maternal instruction genuinely contested.'),
    ('Prov.24.23-Prov.24.25', ['Prov.24.23-Prov.24.25', 'Prov.24.26-Prov.24.26', 'Prov.24.27-Prov.24.27', 'Prov.24.28-Prov.24.29'], 'The named supplement and broad civic-neighbor conduct could justify 24:23-29 as one retrieval cluster, although the boss now treats that case as a parent relation rather than one active child.'),
    ('Prov.30.17-Prov.30.17', ['Prov.30.15-Prov.30.16', 'Prov.30.17-Prov.30.17'], 'Devouring and unsated imagery can support attaching the filial-eye warning to 30:15-16, although the closed numerical formula and new eye subject favor separation.'),
]


def append_dissent_ledger(decisions: list[dict[str, Any]]) -> None:
    path = REVIEW / 'appeal_ledger.jsonl'
    prior = path.read_text(encoding='utf-8') if path.is_file() else ''
    prior_ids = {
        str(row.get('appeal_id'))
        for row in load_jsonl(path)
    } if path.is_file() else set()
    by_span = {row['span']: row for row in decisions}
    additions: list[dict[str, Any]] = []
    for ordinal, (anchor, affected, rationale) in enumerate(DISSENT_SPECS, 1):
        evidence = by_span[anchor]
        index = int(evidence['decision_id'].rsplit('-', 1)[1])
        active = anchor in HOLDS
        appeal_id = f'PROV-V2-APPEAL-{index:03d}' if active else f'PROV-V2-HISTORICAL-DISSENT-{ordinal:02d}'
        if appeal_id in prior_ids:
            continue
        additions.append({
            'schema_version': 'm7_append_only_appeal.v2',
            'appeal_id': appeal_id,
            'book': 'Prov',
            'decision_id': evidence['decision_id'],
            'affected_spans': affected,
            'passage_context': '{} within {}'.format(anchor, evidence['parent_span']),
            'rationale': rationale,
            'disagreement_with': f'prov-v2-boss-{index:03d}-sol-xhigh',
            'requested_next_reviewer': 'independent_original_language_and_literary_specialist_then_human',
            'status': 'deferred_human_or_external_ai' if active else 'preserved_historical_dissent_nonblocking',
            'active_packet_appeal': active,
            'forced_consensus': False,
            'non_authorizing': True,
        })
    suffix = ''.join(json.dumps(row, ensure_ascii=False, separators=(',', ':')) + '\n' for row in additions)
    if additions:
        atomic_text(path, prior + suffix)


def sidecar_replacement(decisions: list[dict[str, Any]], packets: list[dict[str, Any]]) -> dict[str, Any]:
    packet_by_id = {row['decision_id']: row for row in packets}
    rows = {name: [] for name in ('low_confidence_register.jsonl', 'frontier_escalation_queue.jsonl', 'atlas_candidate_feed.jsonl')}
    for evidence in decisions:
        if evidence['confidence'] not in {'low', 'medium_low'}:
            continue
        packet = packet_by_id[evidence['decision_id']]
        hold = evidence['hold']
        accepted = packet['final_state'] == 'accepted_candidate'
        if hold:
            question = hold['question']
            concern_type = hold['kind']
            reviewer = 'independent_Hebrew_textual_and_literary_specialist'
        else:
            question = '{} This complete instruction coincides with a chapter and therefore receives the protocol-required confidence reduction without changing its accepted disposition.'.format(evidence['defensible_basis'])
            concern_type = 'chapter_coincident_complete_instruction_protocol_check'
            reviewer = 'wisdom_literary_form_specialist'
        base = {
            'model_id': 'M7_sol',
            'book': 'Prov',
            'span': evidence['span'],
            'chunk_decision_id': evidence['decision_id'],
            'confidence': evidence['confidence'],
            'observed_substrate_signals': [evidence['deciding_marker_or_seam'], evidence['rejected_alternative'], question],
            'review_packet_final_state': packet['final_state'],
            'chunk_review_status': 'candidate_review_complete' if accepted else 'final_deferred_appeal',
            'candidate_hold_state': None if accepted else 'deferred_human_or_external_ai',
            'non_authorizing': True,
        }
        appeal_ids = [row['appeal_id'] for row in packet['appeals']]
        rows['low_confidence_register.jsonl'].append({
            **base,
            'why_low_confidence': question,
            'possible_downstream_risk': evidence['defensible_basis'],
            'competing_boundary_risk': evidence['rejected_alternative'],
            'appeal_status': 'candidate_review_complete_specialist_followup_optional' if accepted else 'deferred_human_or_external_ai',
            'appeal_ids': appeal_ids,
        })
        rows['frontier_escalation_queue.jsonl'].append({
            **base,
            'concern_type': concern_type,
            'why_frontier_review_needed': question,
            'suggested_reviewer': reviewer,
            'promotion_authority': 'none',
        })
        rows['atlas_candidate_feed.jsonl'].append({
            **base,
            'concern_type': concern_type,
            'why_low_confidence': question,
            'possible_downstream_risk': evidence['defensible_basis'],
            'suggested_reviewer': reviewer,
            'proposed_atlas_action': 'consider_only',
            'atlas_promotion_authority': 'none',
        })
    return {
        'schema_version': 'm7_proverbs_sidecar_replacement.v2',
        'book': 'Prov',
        'replace_all_existing_prov_rows': True,
        'rows': rows,
        'non_authorizing': True,
    }


def role_artifact(role: str, packets: list[dict[str, Any]]) -> dict[str, Any]:
    if role == 'peer':
        reviews = [row['peer_crosscheck'] for row in packets]
    elif role == 'boss':
        reviews = [row['boss_ruling'] for row in packets]
    else:
        reviews = [
            next(review for review in row['primary_reviews'] if review['reviewer_role'] == role)
            for row in packets
        ]
    return {
        'schema_version': 'm7_proverbs_role_artifact.v2',
        'book': 'Prov',
        'role': role,
        'decision_local_review_count': len(reviews),
        'reviews': reviews,
        'independence_scope': INDEPENDENCE_SCOPE,
        'non_authorizing': True,
    }


def materialize() -> None:
    decisions = assemble_decisions()
    chunks = build_chunks(decisions)
    packets = build_packets(decisions, chunks)
    relations = build_relations(decisions)
    write_jsonl(REVIEW / 'decision_evidence_v2.jsonl', decisions)
    write_jsonl(CHUNKS, chunks)
    write_jsonl(REVIEW / 'review_packets.jsonl', packets)
    write_jsonl(REVIEW / 'decision_relations.jsonl', relations)
    write_json(REVIEW / 'primary_hebrew_v2.json', role_artifact('hebrew_textual_and_wisdom_form', packets))
    write_json(REVIEW / 'primary_literary_v2.json', role_artifact('literary_collection_and_saying_form', packets))
    write_json(REVIEW / 'canonical_premortem_v2.json', role_artifact('canonical_retrieval_premortem', packets))
    write_json(REVIEW / 'peer_crosscheck_v2.json', role_artifact('peer', packets))
    write_json(REVIEW / 'boss_ruling_v2.json', role_artifact('boss', packets))
    write_json(REVIEW / 'sidecar_rows_v2.json', sidecar_replacement(decisions, packets))
    append_dissent_ledger(decisions)
    write_json(REVIEW / 'post_resolution_check_v2.json', {
        'schema_version': 'm7_post_resolution_check.v2',
        'book': 'Prov',
        'overall_status': 'pending_role_separated_hash_bound_checker',
        'checked_chunks_sha256': hashlib.sha256(CHUNKS.read_bytes()).hexdigest(),
        'checked_review_packets_sha256': hashlib.sha256((REVIEW / 'review_packets.jsonl').read_bytes()).hexdigest(),
        'checked_decision_relations_sha256': hashlib.sha256((REVIEW / 'decision_relations.jsonl').read_bytes()).hexdigest(),
        'failures': ['global_sidecars_not_installed_and_final_checker_not_received'],
        'independence_scope': INDEPENDENCE_SCOPE,
        'non_authorizing': True,
    })
    write_json(MODEL / 'receipts' / 'Prov_completion_v2.json', {
        'schema_version': 'm7_book_completion_receipt.v2',
        'book': 'Prov',
        'completion_state': 'invalidated_pending_corrective_rereview_closure',
        'non_authorizing': True,
    })
    counts = Counter(row['confidence'] for row in chunks)
    print(json.dumps({
        'book': 'Prov',
        'chunks': len(chunks),
        'accepted': sum(row['final_state'] == 'accepted_candidate' for row in packets),
        'held': sum(row['final_state'] != 'accepted_candidate' for row in packets),
        'confidence': dict(sorted(counts.items())),
        'sidecar_rows': len(sidecar_replacement(decisions, packets)['rows']['low_confidence_register.jsonl']),
        'global_sidecars_modified': False,
    }, indent=2))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def book_rows_digest(path: Path) -> str:
    rows = [row for row in load_jsonl(path) if row.get('book') == 'Prov']
    payload = b''.join(
        (json.dumps(row, sort_keys=True, separators=(',', ':'), ensure_ascii=False) + '\n').encode('utf-8')
        for row in rows
    )
    return hashlib.sha256(payload).hexdigest()


def postcheck_commands() -> list[tuple[str, list[str]]]:
    checks = MODEL / 'checks'
    return [
        ('exact_ordered_coverage', [sys.executable, str(checks / 'validate_exact_book_coverage.py'), '--book', 'Prov']),
        ('official_chunk_map', [sys.executable, str(ROOT / 'scripts' / 'validate_whole_bible_chunk_map.py'), str(CHUNKS), '--model-id', 'M7_sol', '--book', 'Prov', '--python-only']),
        ('review_status_sidecar_independence_parity', [sys.executable, str(checks / 'validate_book_review_coverage.py'), '--book', 'Prov']),
        ('literary_quality_protocol', [sys.executable, str(ROOT / 'scripts' / 'validate_t423_literary_quality_protocol.py'), '--model-folder', str(MODEL), '--book', 'Prov', '--require-artifacts']),
        ('corrective_review_depth', [sys.executable, str(ROOT / 'scripts' / 'validate_m7_corrective_review_depth.py'), '--model-root', str(MODEL), '--book', 'Prov', '--json']),
    ]


def finalize(checker_verdict_file: str) -> None:
    verdict_path = Path(checker_verdict_file)
    if not verdict_path.is_absolute():
        verdict_path = ROOT / verdict_path
    verdict_path = verdict_path.resolve()
    if verdict_path.parent != REVIEW.resolve():
        raise ValueError('checker verdict must be stored in the Proverbs review directory')
    verdict = load_json(verdict_path)
    packets_path = REVIEW / 'review_packets.jsonl'
    relations_path = REVIEW / 'decision_relations.jsonl'
    sidecars = {
        name: book_rows_digest(MODEL / name)
        for name in ('low_confidence_register.jsonl', 'frontier_escalation_queue.jsonl', 'atlas_candidate_feed.jsonl')
    }
    required = {
        'schema_version': 'm7_role_separated_checker_verdict.v1',
        'book': 'Prov',
        'checked_chunks_sha256': digest(CHUNKS),
        'checked_review_packets_sha256': digest(packets_path),
        'checked_decision_relations_sha256': digest(relations_path),
        'checked_uncertainty_sidecar_sha256': sidecars,
        'verdict': 'pass_with_holds',
        'role_separated_from_author': True,
        'shared_model_substrate': True,
        'counts_as_cross_model_independent_vote': False,
        'non_authorizing': True,
    }
    for field, expected in required.items():
        if verdict.get(field) != expected:
            raise ValueError(f'checker verdict field {field} does not match frozen Proverbs artifacts')
    checker_attempt_id = verdict.get('checker_attempt_id')
    if not isinstance(checker_attempt_id, str) or not checker_attempt_id or checker_attempt_id == 'M7_sol':
        raise ValueError('checker verdict requires a distinct checker attempt identity')
    if verdict.get('findings') not in ([], None):
        raise ValueError('checker verdict retains unresolved findings')

    results: list[dict[str, Any]] = []
    for gate_id, command in postcheck_commands():
        result = subprocess.run(command, cwd=ROOT, shell=False, check=False, capture_output=True, text=True)
        output = (result.stdout or result.stderr).strip()
        results.append({
            'gate_id': gate_id,
            'command': ' '.join(command),
            'exit_code': result.returncode,
            'status': 'pass' if result.returncode == 0 else 'fail',
            'output': output,
        })
        if result.returncode:
            raise RuntimeError(f'{gate_id} failed during final hash-bound postcheck: {output}')

    packets = load_jsonl(packets_path)
    accepted = sorted(row['decision_id'] for row in packets if row.get('final_state') == 'accepted_candidate')
    held = sorted(row['decision_id'] for row in packets if row.get('final_state') != 'accepted_candidate')
    appeals = sorted(
        appeal['appeal_id']
        for row in packets
        for appeal in row.get('appeals', [])
        if isinstance(appeal, dict) and isinstance(appeal.get('appeal_id'), str)
    )
    cluster_ids = sorted({row['post_resolution_check']['checker_attempt_id'] for row in packets})
    postcheck = {
        'schema_version': 'm7_post_resolution_check.v2',
        'checker_attempt_id': checker_attempt_id,
        'checker_attempt_ids': cluster_ids,
        'role': 'fresh_read_only_post_resolution_checker',
        'book': 'Prov',
        'checked_chunks_sha256': digest(CHUNKS),
        'checked_review_packets_sha256': digest(packets_path),
        'checked_decision_relations_sha256': digest(relations_path),
        'checked_uncertainty_sidecar_sha256': sidecars,
        'checked_decision_ids': sorted(row['decision_id'] for row in packets),
        'checker_verdict_path': verdict_path.relative_to(ROOT).as_posix(),
        'checker_verdict_sha256': digest(verdict_path),
        'validation_results': results,
        'chunk_count': len(packets),
        'review_packet_count': len(packets),
        'accepted_decision_count': len(accepted),
        'accepted_decision_ids': accepted,
        'held_decision_count': len(held),
        'held_decision_ids': held,
        'appeal_count': len(appeals),
        'appeal_ids': appeals,
        'independence_scope': INDEPENDENCE_SCOPE,
        'independence_limit': 'Role-separated checks share one model substrate and count as one correlated model voice.',
        'role_separated_checker_verdict_received': True,
        'independent_model_verdict_received': False,
        'failures': [],
        'overall_status': 'pass_with_holds',
        'forced_consensus': False,
        'non_authorizing': True,
    }
    write_json(REVIEW / 'post_resolution_check_v2.json', postcheck)
    command = [sys.executable, str(MODEL / 'checks' / 'write_completion_receipt_v2.py'), '--book', 'Prov']
    result = subprocess.run(command, cwd=ROOT, shell=False, check=False)
    if result.returncode:
        raise RuntimeError('completion receipt writer refused the finalized Proverbs artifacts')
    print(f'finalized Proverbs with {len(accepted)} accepted, {len(held)} held, and {len(appeals)} active appeals')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--finalize', action='store_true')
    parser.add_argument('--checker-verdict-file')
    args = parser.parse_args()
    if args.finalize:
        if not args.checker_verdict_file:
            parser.error('--finalize requires --checker-verdict-file')
        finalize(args.checker_verdict_file)
    else:
        materialize()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
