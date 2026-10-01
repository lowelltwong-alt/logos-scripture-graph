from __future__ import annotations
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'book_chunks'/'1Sam'/'chunks.jsonl'
# start,end,title,form,local opening/closure evidence
ROWS=[
('1.1','1.28','Hannah household petition birth and presentation','vow_fulfillment_narrative','Elkanah household and Shiloh worship open Hannah distress; petition, vow, Eli exchange, birth/name, weaning, presentation, and worship close at 1:28'),
('2.1','2.10','Hannah prayer song','framed_poetic_prayer','Hannah prayed and said explicitly opens sustained reversal poetry; adversary/judge/king-anointed conclusion closes at 2:10'),
('2.11','2.26','Samuel and Eli sons contrast panel','contrastive_sanctuary_narrative','Samuel serving before Eli opens an alternating panel; sons sacrilege and rebuke contrast with robe, blessing, Hannah children, and Samuel growth at 2:26'),
('2.27','2.36','Oracle against Eli house','prophetic_oracle','A man of God came to Eli opens retrospective accusation, reversal, sign, and faithful-priest promise through 2:36'),
('3.1','3.21','Samuel call disclosure and establishment','prophetic_call_narrative','Rare-word setting opens repeated call and recognition; oracle, compelled disclosure, Eli response, Samuel establishment, and renewed revelation close at 3:21'),
('4.1','4.22','Ark battle capture and Eli house deaths','battle_report_and_messenger_death_narrative','National battle begins from Samuel word; defeat, ark deployment/capture, messenger report, Eli death, childbirth death, and Ichabod interpretation close at 4:22'),
('5.1','5.12','Ark among Dagon and Philistine cities','traveling_ark_judgment_narrative','Ark relocation to Ashdod opens Dagon humiliation; Ashdod-Gath-Ekron transfer and affliction escalation close with death panic at 5:12'),
('6.1','7.2','Ark return Beth Shemesh and Kiriath Jearim settlement','ark_return_and_settlement_cycle','Seven-month reset opens return counsel, offering and cart test; journey, Beth Shemesh reception/crisis, requested transfer, Kiriath settlement, and twenty-year notice close at 7:2'),
('7.3','7.17','Mizpah return battle Ebenezer and judgeship','assembly_battle_and_judgeship_summary','Samuel summons all Israel to return; confession, intercession, Philistine defeat, Ebenezer, restoration, and judgeship circuit close at 7:17'),
('8.1','8.22','King demand warning and authorization','public_assembly_and_warning','Samuel old and sons appointed opens elders king demand; divine response, king custom warning, refusal, authorization, and dismissal close at 8:22'),
('9.1','10.16','Saul quest private anointing and signs fulfilled','quest_anointing_and_sign_cycle','Kish and Saul introduction opens donkey quest; seer meeting, meal, private anointing, announced signs, fulfillment, proverb, and uncle concealment close at 10:16'),
('10.17','10.27','Public selection and mixed reception','public_selection_procedure','Samuel calls the people to Mizpah; indictment, tribal selection, hidden Saul, acclamation, regulations, dispersal, loyalty, and contempt close at 10:27'),
('11.1','11.15','Jabesh rescue and kingdom renewal','battle_rescue_and_public_confirmation','Nahash siege opens Jabesh crisis; messengers, Spirit-enabled muster, victory, mercy, Gilgal renewal, sacrifice, and rejoicing close at 11:15'),
('12.1','12.25','Samuel farewell covenant assembly','public_covenant_speech_and_sign','Samuel addresses all Israel with integrity witness; historical recital, king conditions, thunder sign, confession, reassurance, and final warning close at 12:25'),
('13.1','13.14','Philistine crisis Gilgal offering and rejection oracle','battle_crisis_and_oracle','Problematic regnal formula opens Philistine crisis; distress, seven-day wait, offering, confrontation, and dynastic rejection oracle close at 13:14'),
('13.15','14.23','Military disadvantage Jonathan attack and deliverance','battle_phase','Samuel departs and forces are counted; raiders/weapons disadvantage leads into Jonathan sign/attack, panic, rally, and deliverance summary at 14:23'),
('14.24','14.46','Saul oath honey inquiry and Jonathan rescue','oath_and_battle_aftermath','Israel distress and Saul oath open honey breach; exhaustion/blood, altar, failed inquiry, lot, death sentence, popular rescue, and pursuit cessation close at 14:46'),
('14.47','14.52','Saul reign wars household and army register','royal_summary_register','Formulaic taking-of-kingship opens wars and victories; family, commander, continuing-war, and recruitment register close at 14:52'),
('15.1','15.35','Amalek command campaign rejection and rupture','command_battle_oracle_and_rupture','Samuel delivers a new commission; campaign/sparing, divine word, confrontation, torn robe, worship, Agag death, separation, mourning, and grief close at 15:35'),
('16.1','16.13','David selected and anointed','selection_and_anointing_narrative','New command after mourning sends Samuel to Bethlehem; sons pass, David is called/anointed, Spirit comes, and Samuel departs at 16:13'),
('16.14','16.23','Spirit transition and David court entry','court_entry_scene','Spirit departure from Saul opens court remedy search; David is recommended, summoned, favored, installed, and repeatedly relieves Saul through 16:23'),
('17.1','18.5','Goliath battle and immediate court aftermath','battle_cycle_and_covenant_aftermath','Philistine and Israelite armies assemble; challenge, David arrival/case, duel, victory/pursuit, lineage inquiry, Jonathan covenant, retention, and appointment close at 18:5'),
('18.6','18.16','Victory song jealousy attack and advancement','court_conflict_scene','Victory procession and women antiphon open Saul jealousy; spear attack, removal/promotion, success, fear, and public love close at 18:16'),
('18.17','18.30','Merab Michal marriage traps','court_scheme_and_marriage_narrative','Saul offers Merab as a trap; failed first offer motivates Michal scheme, bride-price, marriage, intensified fear/enmity, and success summary at 18:30'),
('19.1','19.7','Jonathan intercession and temporary restoration','intercession_scene','Saul orders David killed; Jonathan warns, advocates, secures Saul oath, and restores David to court at 19:7'),
('19.8','19.17','Renewed spear attack and Michal escape','attack_and_escape_scene','Renewed war and success trigger another spear attack; Michal enables house escape/deception and answers Saul through 19:17'),
('19.18','19.24','Naioth pursuit and prophetic reversal','pursuit_and_prophetic_reversal','David flees to Samuel at Ramah; three messenger waves and Saul are overtaken by prophetic behavior, closing with the repeated proverb at 19:24'),
('20.1','20.42','David Jonathan covenant test and farewell','covenant_test_and_farewell','David flees Naioth and challenges Jonathan; renewed covenant, new-moon/arrow test, Saul table confrontation, sign, private farewell, and oath close at 20:42'),
('21.1','21.9','Nob bread Doeg and Goliath sword','fugitive_priest_dialogue','David comes to Nob and Ahimelech; cover story, holy bread, Doeg notice, and Goliath sword close before flight to Gath at 21:10'),
('21.10','21.15','Gath recognition and feigned madness','fugitive_escape_scene','David flees to Achish; recognition song creates fear, feigned madness, and Achish dismissal close at 21:15'),
('22.1','22.5','Adullam band family relocation and Gad direction','fugitive_band_formation','David escapes to Adullam; family and distressed band gather, parents move to Moab, and Gad directs return to Judah at 22:5'),
('22.6','22.23','Saul hearing Doeg massacre and Abiathar escape','court_hearing_massacre_and_survivor_report','Saul hears David is discovered and accuses servants; Doeg report, priest defense, massacre, Abiathar escape, and David protection response close at 22:23'),
('23.1','23.13','Keilah rescue inquiries and escape','oracle_battle_and_escape','Keilah raid report opens repeated divine inquiry; rescue, Saul threat, counterfactual inquiry, warned departure, and abandoned siege close at 23:13'),
('23.14','23.18','Jonathan strengthens David and renews covenant','covenant_scene','David remains in wilderness strongholds; Jonathan comes to strengthen him, speaks succession terms, and renews covenant before departure at 23:18'),
('23.19','23.29','Ziph disclosure Maon pursuit and interruption','pursuit_and_messenger_escape','Ziphites approach Saul; pursuit and near encirclement culminate in Philistine messenger interruption, withdrawal, named place, and En Gedi movement at 23:29'),
('24.1','24.22','En Gedi cave Saul spared and oath','spared_saul_pursuit_and_covenant','Saul returns to pursue at En Gedi; cave opportunity, robe proof, David speech, Saul confession/recognition, offspring oath, and separation close at 24:22'),
('25.1','25.44','Samuel death and Abigail intervention cycle','death_transition_and_intervention_narrative','Samuel death/mourning/burial and David movement open transition; Nabal refusal, David oath, Abigail intervention, reversal, Nabal death, marriage, and wives notice close at 25:44'),
('26.1','26.25','Hachilah camp Saul spared and separation','spared_saul_pursuit','Ziphite disclosure opens camp infiltration; spear/jar proof, Abner rebuke, David-Saul exchange, confession/blessing, and separation close at 26:25'),
('27.1','28.2','Philistine refuge raids and campaign summons','relocation_raid_register_and_campaign_hinge','David decides on Philistine refuge; Ziklag tenure, raids/deception, Achish trust, campaign summons, and bodyguard commitment close at 28:2'),
('28.3','28.25','Saul failed inquiry medium consultation and departure','consultation_oracle_and_response','Samuel-death/ban and camp reset open failed authorized inquiry; disguised medium encounter, reported apparition/speech, collapse, meal, and night departure close at 28:25'),
('29.1','29.11','Philistine commanders reject David','military_assembly_and_dismissal','Philistine muster resumes David campaign thread; commanders object, Achish defends, dismissal is argued and ordered, and David returns at 29:11'),
('30.1','30.20','Ziklag loss inquiry pursuit and recovery','oracle_pursuit_and_battle_recovery','David reaches burned Ziklag; grief/threat, inquiry, pursuit, Egyptian guide, battle, total recovery, and plunder close at 30:20'),
('30.21','30.31','Equal share ruling and gift register','legal_procedure_and_distribution_register','Return to the two hundred opens spoil dispute; equal-share ruling, enduring statute, gifts, and destination list close at 30:31'),
('31.1','31.13','Gilboa deaths dishonor recovery and burial','battle_death_and_burial_closure','Philistine battle opens Israel flight; sons/Saul/armor-bearer deaths, territorial collapse, body treatment, Jabesh retrieval, burning/burial, and fast close at 31:13')]
LOW={1,3,5,6,8,9,11,13,15,16,17,19,21,22,25,26,27,28,31,33,34,35,37,39,40,42,43,44}
ALT={
1:'Preserve 1:1-8 / 1:9-20 / 1:21-28 children; the larger unit keeps petition/vow with birth, presentation, and fulfillment',
3:'Preserve 2:11-21 / 2:22-26; the larger contrast panel keeps Samuel growth brackets around sons conduct and Eli rebuke',
5:'Preserve 3:1-18 / 3:19-21; the larger call narrative keeps oracle disclosure with narrator establishment and renewed revelation',
6:'Preserve 4:1-11 / 4:12-18 / 4:19-22; the larger battle unit keeps capture with messenger-announced deaths and Ichabod consequence',
8:'Preserve 6:1-12 / 6:13-18 / 6:19-7:2 and Hebrew alternative ending at 7:1; larger LOW keeps return instructions, fulfillment, crisis, transfer, and settlement while 6:19 remains textual pressure',
9:'Preserve 7:3-14 / 7:15-17 and Hebrew alternative beginning at 7:2; larger unit keeps Mizpah return/battle with restoration and judgeship summary',
11:'Preserve 9:1-14 / 9:15-10:8 / 10:9-16; larger unit keeps private selection, announced signs, fulfillment, and concealment together',
13:'Preserve 11:1-13 / 11:14-15; larger unit keeps Jabesh victory with the public renewal it directly motivates',
15:'Preserve 13:1-7 / 13:8-14 or isolate 13:1; larger LOW keeps crisis and Gilgal confrontation while regnal numbers remain unresolved',
16:'Preserve 13:15-23 / 14:1-23 and Hebrew 13:23-14:23; larger unit retains military disadvantage as setup for Jonathan target, attack, and deliverance',
17:'Preserve oath, blood, inquiry, and lot subscenes at 14:30, 14:31, and 14:38; larger unit keeps oath through Jonathan rescue and pursuit cessation',
19:'Preserve 15:1-9 / 15:10-31 / 15:32-35; larger unit keeps command, breach, oracle, robe sign, Agag, rupture, mourning, and grief',
21:'Preserve separation at 16:13/14 and do not merge court entry with Goliath; interpretation of Spirit language remains LOW though scene seam is strong',
22:'Preserve 17:1-58 / 18:1-5 or finer battle children; cross-chapter unit retains grammatically immediate inquiry, Jonathan covenant, retention, and appointment amid MT/LXX pressure',
25:'Hebrew primary preferred all 19:1-24; preserve that parent while retaining Jonathan intercession as a completed temporary-restoration child',
26:'Hebrew primary preferred all 19:1-24; preserve that parent while the renewed war/spear and Michal house escape form a distinct causal scene',
27:'Hebrew primary preferred all 19:1-24; preserve that parent while Naioth has a new helper/location and proverb closure',
28:'Preserve 20:1-23 / 20:24-34 / 20:35-42; larger unit keeps covenant plan, test, arrow signal, farewell, and oath',
31:'Hebrew primary preferred 21:1-22:5; retain Adullam movement child but record continuity from Nob/Gath through band formation',
33:'Hebrew primary preferred 23:1-29; retain Keilah inquiry/action child while recording the sustained fugitive parent',
34:'Hebrew primary preferred 23:1-29; retain Jonathan covenant child but record it inside the sustained fugitive parent',
35:'Hebrew primary preferred 23:1-29; retain Ziph/Maon pursuit child with messenger interruption and En Gedi movement',
37:'Preserve 25:1 singleton, attachment backward to 24, or 25:1-44; larger forward unit avoids singleton but may obscure Samuel death closure',
39:'Preserve 27:1-27:12 / 28:1-2 or attach 28:1-2 to Endor war frame; larger Achish continuity is retained without chronology ruling',
40:'Preserve possible war-frame split before consultation; keep failed inquiry, medium encounter, reported oracle, collapse, meal, and departure whole without apparition ruling',
42:'Hebrew primary preferred 30:1-31; retain recovery child while recording its direct relation to spoil settlement',
43:'Hebrew primary preferred 30:1-31; retain legal distribution child because arrival at left-behind men changes function',
44:'Preserve 31:1-7 / 31:8-13; larger unit keeps deaths with territorial consequence, body recovery, burial, and fast without harmonizing later reports'}
out=[]
for i,(a,b,title,form,marker) in enumerate(ROWS,1):
 span=f'1Sam.{a}-1Sam.{b}'; did=f'M7_sol-1Sam-{i:03d}'; low=i in LOW
 if low: rejected=f'Preserved competing boundary/evidence alternative for {span}: {ALT[i]}.'
 else:
  nxt=ROWS[i] if i<len(ROWS) else None
  rejected=(f'Rejected expansion beyond 1Sam.{b} into 1Sam.{nxt[0]}-{nxt[1]} ({nxt[2]}): {marker} completes before the next unit opens with {nxt[4]}.' if nxt else f'Rejected narrower detachment before 1Sam.{b}: death, recovery, burial, and fast form the canonical book closure.')
 hold=ALT.get(i,f'Hebrew wording and source metadata for {span} corroborate the stated local form only; no root, textual, chronological, moral, political, occult, or theological ruling.')
 row={'model_id':'M7_sol','book':'1Sam','span':span,'chunk_index_in_book':i,'working_title':title,'literature_type_guess':form,'boundary_evidence_refs':[f'direct_read:eng-web:{span}',f'direct_read:oshb:1Sam.xml#{span}',f'direct_read:uxlc:1Sam.xml#{span}','book_strategy/1Sam.md','reviews/1Sam/primary_hebrew_v1.json','reviews/1Sam/primary_literary_v1.json','reviews/1Sam/canonical_premortem_v1.json','reviews/1Sam/peer_crosscheck_v1.json','reviews/1Sam/boss_ruling_v1.json','reviews/1Sam/decision_relations.jsonl'],'strong_or_hebrew_tags_used':['direct_hebrew_wording_considered','source_metadata_corrob_only','roots_are_not_meaning','original_language_is_not_boundary_authority'],'wj_or_red_letter_considered':False,'frontier_flag_considered':True,'confidence':'low' if low else 'medium','decision_id':did,'literary_form':form,'deciding_marker_or_seam':marker+'.','boundary_rationale':f'Prefer the complete {form} unit {span}. {marker}.','rejected_alternative':rejected,'defensible_basis':f'{did}: {marker}. This exact scene/speech/form/register signal—not chapter numbering, roots, chronology, or canonical parallels—supports the candidate boundary.','review_revision':1,'review_status':'final_deferred_appeal' if low else 'candidate_review_complete','review_holds':['deferred_human_or_external_ai','external_provider_review_at_convergence'] if low else ['external_provider_review_at_convergence'],'non_authorizing':True,'candidate_internal_seams':[marker+'.'],'original_language_translation_holds':[hold+'. Evidence only; no preferred reading or theological conclusion.'],'cross_reference_holds':['Internal and cross-book relations are recorded separately and cannot harmonize accounts or authorize this seam.'],'red_team_premortem_holds':[hold+'.'],'working_title_is_boundary_authority':False,'working_title_origin':'independent_1samuel_mesh_reconciliation_v1','candidate_only':True,'review_evidence_summary':marker+'. Candidate-only; no textual, chronology, kingship, moral, occult, or theology ruling.','red_team_questions':[f'Does the seam after 1Sam.{b} survive removal of headings and chapters?',f'Does this exact alternative better preserve the local scene: {rejected}'],'hard_passage_forecast':[hold+'.']}
 if low: row.update(candidate_hold_state='deferred_human_or_external_ai',candidate_hold_basis='preserved_appeal')
 out.append(row)
assert len(out)==44
OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in out),encoding='utf-8',newline='\n')
print(hashlib.sha256(OUT.read_bytes()).hexdigest(),len(out),sum(x['confidence']=='low' for x in out))
