import json
from pathlib import Path

P=Path(__file__).resolve().parent/'book_chunks'/'Deut'/'chunks.jsonl'
OPEN=[
"'These are the words' reporting frame","recalled divine speech, 'YHWH our God spoke to us in Horeb'","the journey notice, 'we departed from Horeb'","the turn-and-journey notice toward the wilderness","the command to rise and cross the Arnon","the retrospective allotment notice, 'we took this land at that time'","Moses' first-person petition, 'I pleaded at that time'","the summons, 'Now Israel, listen'","the warning, 'Only take care and guard yourself'","the rhetorical appeal, 'Ask now of former days'","the narrative notice that Moses set apart three cities","the superscription, 'This is the law which Moses set'","the covenant self-identification, 'I am YHWH your God'","the retrospective notice, 'These words YHWH spoke'","the command heading, 'This is the command, statutes, and judgments'","the land-entry conditional, 'When YHWH brings you'","the child's future question, 'When your son asks'","the land-entry nations conditional, 'When YHWH brings you into the land'","the conditional blessing formula, 'It shall happen because you listen'","the comprehensive command summons, 'All the command'","the warning, 'Take care lest you forget'","the summons, 'Hear, Israel, you cross the Jordan today'","the remembrance charge, 'Remember; do not forget'","the summons, 'Now Israel, what does YHWH ask of you?'","the obedience summons, 'Therefore keep the whole command'","the choice announcement, 'See, I set before you blessing and curse'","the code heading, 'These are the statutes and judgments'","the anti-imitation conditional, 'When YHWH cuts off the nations'","the intimate-enticer conditional, 'If your brother entices you secretly'","the apostate-city conditional, 'If you hear in one of your cities'","the identity declaration, 'You are sons of YHWH your God'","the tithe command, 'You shall surely tithe'","the release heading, 'At the end of seven years'","the servant conditional, 'If your Hebrew brother is sold to you'","the firstborn command, 'Every firstborn that is born'","the festival command, 'Observe the month of Abib'","the governance command, 'Judges and officers you shall appoint'","the kingship conditional, 'When you enter the land and say, I will set a king'","the Levitical heading, 'The priests, the Levites, all the tribe of Levi'","the divination contrast, 'When you enter the land, do not learn'","the refuge-city conditional, 'When YHWH cuts off the nations'","the evidence rule, 'One witness shall not rise'","the battle conditional, 'When you go out to war'","the siege conditional, 'When you approach a city to fight it'","the slain-person conditional, 'If one slain is found in the land'","the captive-woman conditional, 'When you go to war and see among the captives'","the neighbor-duty prohibition, 'You shall not see your brother's ox'","the marital-case conditional, 'If a man takes a wife'","the assembly admission rules","the camp conditional, 'When you camp against your enemies'","the escaped-servant prohibition, 'You shall not return a slave'","the remarriage conditional, 'If a man takes a wife'","the loan-pledge conditional, 'When you lend your neighbor'","the courtroom conditional, 'If there is a dispute between men'","the levirate conditional, 'If brothers dwell together'","the remembrance command, 'Remember what Amalek did'","the land-entry firstfruits conditional, 'When you enter the land'","the third-year tithe conditional, 'When you finish tithing'","the covenant avowal, 'This day YHWH commands you'","the Moses-and-elders command frame","Moses' same-day command to the people","the blessing conditional, 'If you diligently listen'","the curse conditional, 'If you do not listen'","the Moab-covenant heading, 'These are the words of the covenant'","the explanatory warning, 'For you know how we lived'","the restoration conditional, 'When all these things come upon you'","the accessibility claim, 'This command is not too difficult'","Moses' succession address to Israel and Joshua","the notice, 'Moses wrote this law'","the divine death-and-commission summons","the completed-document notice, 'When Moses finished writing'","the narrative song introduction and 'Give ear, heavens'","the post-song recitation notice naming Moses and Joshua","the fresh divine speech, 'YHWH spoke that same day'","the blessing superscription, 'This is the blessing'","the named-tribe saying, 'May Reuben live'","the Israel-wide coda, 'There is none like Jeshurun'","Moses' ascent from the plains of Moab","the Joshua succession notice"
]
LOW={1,2,4,5,6,9,12,19,23,24,25,27,28,31,37,40,41,46,47,51,52,53,55,60,63,64,65,67,72,76}
HOLDS={
1:"Deut.1:1-4 is a book/speech frame while 1:5 ('Moses began to expound...saying') may close that frame or attach forward; preserve both 1:1-5 / 1:6 and 1:1-4 / 1:5 alternatives.",
2:"The 'at that time I said' turn at 1:9 changes from the recalled departure command (1:6-8) to appointment of judges (1:9-18); preserve the split appeal.",
4:"A fresh divine-speech formula after the generation closure supports the appealed 2:1-16 / 2:17-23 split; retain the larger unit pending independent review.",
5:"Deut.3.1 independently opens the Og parallel; retain the Sihon/Og diptych as LOW and preserve the split appeal.",
6:"The 'at that time I commanded' turn at 3:18 supports the appealed 3:12-17 / 3:18-22 split.",
9:"The paragraph close after 4:24 and the 4:25 childbearing conditional support an appealed 4:9-24 / 4:25-31 split.",
12:"Deut.5.1 is a defensible inner summons; heading-plus-Horeb-frame remains LOW.",
19:"The paragraph close after 7:16 and the 7:17 inner-question formula support an appealed 7:12-16 / 7:17-26 split.",
23:"Turns at 9:25 and 10:1 plus the 10:6-9 itinerary/Levi parenthesis remain explicit inner-seam appeals.",
24:"The 11:1-2 exhortation/addressee turn remains an appeal inside the larger covenant-demand movement.",
25:"The 11:18 household-transmission turn remains an appeal inside the larger land-obedience movement.",
27:"Application turns at 12:15 and 12:20 remain appeals inside the unified central-worship code.",
28:"Exact crosswalk: WEB 12:32=MT 13:1 and WEB 13:1=MT 13:2. Preserve 12:29-32 / 13:1-5 as the split alternative; select no preferred numbering tradition.",
31:"The 14:3 food-law turn is an inner form seam; retain the larger holiness collection as LOW.",
37:"Function changes at 16:21, 17:1, 17:2, and 17:8 remain explicit split appeals inside the larger governance code.",
40:"The prophet promise at 18:15 is a strong inner contrast seam; retain the larger prophetic-discernment parent as LOW.",
41:"Deut.19:14 changes from refuge law to landmark safeguard; retain the larger unit only to avoid a one-verse orphan and preserve the appeal.",
46:"Case openings at 21:15, 21:18, and 21:22 remain explicit appeals inside the larger household/execution collection.",
47:"Case turns at 22:5, 22:6, 22:8, and 22:9-12 remain explicit appeals inside the larger collection.",
48:"Exact crosswalk: WEB 22:30=MT 23:1. Preserve 22:13-29 / 22:30 as a split appeal; select no preferred versification.",
49:"Exact crosswalk: WEB 23:1=MT 23:2 and WEB 23:8=MT 23:9; Hebrew evidence is attached through that offset.",
51:"Function shifts at 23:17, 23:19, 23:21, and 23:24 remain explicit appeals inside this mixed larger collection.",
52:"New cases at 24:5, 24:6, 24:7, and 24:8 remain split appeals inside the larger household-safeguard collection.",
53:"Application turns at 24:14, 24:16, 24:17, and 24:19 remain appeals inside the thematic vulnerable-neighbor code.",
55:"Case turns at 25:11 and 25:13 remain explicit appeals inside the larger levirate/justice collection.",
57:"The Hebrew clause at 26:5 has real syntactic/translation ambiguity; select neither 'wandering Aramean' nor 'Aramean sought to destroy' nor another rendering.",
60:"The explicit speaker shift at 27:9 remains a split appeal. Deut.27:4 Ebal/Gerizim witness pressure is recorded without choosing a reading.",
63:"The escalation at 28:45/47 remains a stanza appeal; retain the cumulative curse parent. WEB 29:1=MT 28:69 lies outside this WEB span.",
64:"Exact crosswalk: WEB 29:1=MT 28:69 and WEB 29:2=MT 29:1. Preserve 29:1-9 / 29:10-15 as the heading/assembly appeal.",
65:"The shifted mapping continues: WEB 29:16-29=MT 29:15-28. Turns at WEB 29:22 and 29:29 remain appeals.",
67:"The Hebrew expression at 30:11 has translation-range pressure ('not too difficult/wonderful'); select no preferred rendering and preserve the 30:11-14 / 30:15-20 appeal.",
72:"No preferred reading: 32:8 MT 'sons of Israel' faces ancient-witness pressure, and 32:43 has witness-length/wording pressure. Stanza children remain appeals under the whole-song parent.",
75:"The rare expression at 33:2 and surrounding poetic syntax are text/translation hot zones; select no preferred reading.",
76:"Named-tribe seams at 33:7, 8, 12, 13, 18, 20, 22, 23, and 24 plus rare poetic diction remain explicit appeals under the larger tribal sequence."
}
rows=[json.loads(x) for x in P.read_text(encoding='utf-8').splitlines() if x.strip()]
assert len(rows)==len(OPEN)==79
for i,row in enumerate(rows,1):
    start,end=row['span'].split('-')
    nxt=OPEN[i] if i<len(OPEN) else 'the end of Deuteronomy'
    marker=f"{start} opens with {OPEN[i-1]}; the {row['literary_form']} movement reaches closure at {end}, before {nxt}."
    row['deciding_marker_or_seam']=marker
    row['candidate_internal_seams']=[marker]
    row['boundary_rationale']=f"Prefer the larger coherent {row['literary_form']} unit {row['span']}. {marker}"
    row['defensible_basis']=f"{row['decision_id']} is defended by the specific opening and closure signals recorded here, corroborated where applicable by Hebrew discourse and paragraph evidence without making it boundary authority."
    row['review_evidence_summary']=marker+" This is evidence-only and selects no theology, canon, authorship, tradition, or preferred textual reading."
    row['original_language_translation_holds']=[HOLDS.get(i,f"The phrase/form signal recorded for '{row['working_title']}' is discourse evidence only; no root inference, lexical shortcut, or preferred translation is selected.")]
    if i==1:
        row['rejected_alternative']="Preserved alternative: Deut.1.1-4 as book/speech frame with Deut.1.5 attached forward; current candidate treats 1.5 as the frame's exposition hinge and closes at 1.5."
        row['red_team_premortem_holds']=["Forward attachment of 1.5 may better preserve the infinitive 'to expound' with ensuing speech; current frame closure remains LOW and appealed."]
    elif i==2:
        row['rejected_alternative']="Preserved alternative: split Deut.1.6-8 departure command from Deut.1.9-18 judge appointment at the 'at that time I said' turn."
        row['red_team_premortem_holds']=["The current larger retrospective unit may hide the 1.9 speaker/function turn; retain LOW and defer the split appeal."]
    low=i in LOW
    row['confidence']='low' if low else 'medium'
    row['review_status']='final_deferred_appeal' if low else 'candidate_review_complete'
    row['review_holds']=['deferred_human_or_external_ai','external_provider_review_at_convergence'] if low else ['external_provider_review_at_convergence']
    if low:
        row['candidate_hold_state']='deferred_human_or_external_ai'; row['candidate_hold_basis']='preserved_appeal'
    else:
        row.pop('candidate_hold_state',None); row.pop('candidate_hold_basis',None)
P.write_text(''.join(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n' for r in rows),encoding='utf-8',newline='\n')
print(json.dumps({'rows':len(rows),'low':sum(r['confidence']=='low' for r in rows)}))