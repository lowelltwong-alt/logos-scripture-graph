import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'book_chunks'/'1Sam'/'chunks.jsonl'; rows=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
H=[
'1Sam.1.11 vow/no-razor wording and 1:20 Samuel/asked wordplay support petition-fulfillment cohesion only; roots decide neither name meaning nor vow theology.',
'1Sam.2.1-10 archaic poetry, horn, Sheol, reversal, king and anointed language support a complete song only; no date, authorship, royal, messianic, or theological ruling.',
'1Sam.2.12-26 sons-of-Eli conduct, 2:22 women-at-entrance clause, 2:25 divine-agency wording, robe and growth refrains are textual/discourse evidence only.',
'1Sam.2.27-36 priestly-house ancestry, sign, faithful-priest promise, and oracle formulae remain unresolved historical/identity pressures and do not select a priestly theory.',
'1Sam.3.13 wording about the sons curse/blasphemy and Eli not restraining them is textually difficult; it supports keeping call, oracle, disclosure, and response together without culpability ruling.',
'1Sam.4 ark/glory language, Hebrews/Israel labels, battlefield totals, Ichabod naming and glory-departed wording support capture-to-household consequence only; no presence theology.',
'1Sam.5 Dagon anatomy, plural-god speech, divine-hand formulae, and tumor terminology are translation/witness pressures; city escalation is literary evidence only.',
'1Sam.6 mice/tumor/guilt-offering vocabulary, causation test, and especially 6:19 action and fifty-thousand-seventy casualty witnesses remain unresolved; no preferred number or reading.',
'1Sam.7.2 twenty-year notice, mourning/longing wording, Ebenezer naming, restoration scope and judgeship formulae are chronology/translation evidence only.',
'1Sam.8 king, judge, mishpat as way/custom/right, listen/reject language and divine concession support the demand-warning exchange only; no political or kingship theology.',
'1Sam.9.9 seer/prophet retrospective, 9:16 and 10:1 prince/anoint terms, short-MT/expansion pressure at 10:1, and sign wording remain unresolved; no textual or chronology choice.',
'1Sam.10 tribal lot/selection, hidden-among-baggage wording, kingdom regulation document, loyal band and contempt labels are procedure evidence only.',
'1Sam.11 Nahash demand, Spirit/muster formulae, troop totals, rescue timing, reprisal refusal and Gilgal renewal vocabulary remain textual/social pressures only.',
'1Sam.12 Bedan/person-name witness pressure, covenant-lawsuit rhetoric, thunder/wheat-harvest sign and fear/serve language support the assembly form only.',
'1Sam.13.1 defective Hebrew regnal age/length versus supplied English numbers and 13:14 according-to-his-heart language remain unresolved; no reconstruction, chronology, or character theology.',
'1Sam.13.15-14.23 force totals, smith/weapons register, Geba/Gibeah, 14:18 ark/ephod witness pressure, Jonathan sign and panic agency remain unresolved.',
'1Sam.14.24-46 oath/curse, honey, blood, inquiry silence, 14:41 lot-prayer plus/minus, and popular ransom/rescue wording remain legal/textual evidence only.',
'1Sam.14.47-52 reign/war formulae, enemy names, royal kinship, Abner relation, and recruitment wording support a functional register, not chronology or royal evaluation.',
'1Sam.15 herem/devoted-destruction vocabulary, totalizing action, confession, torn robe, Agag death, and nḥm grief/repent/relent wording at 15:11,29,35 remain morally/theologically unresolved.',
'1Sam.16.1-13 see/choose/anoint and heart/appearance wording, son order and Spirit-rush formula support selection form only; no character or divine-choice theology.',
'1Sam.16.14-23 Spirit departure and evil-spirit-from-YHWH/God wording, musician remedy and relief language support court transition only; no ontology, causation, or diagnosis.',
'1Sam.17.1-18.5 major MT/LXX plus-minus, Goliath height, David age/family/arrival, Saul acquaintance, lineage inquiry and Jonathan aftermath remain unresolved; no harmonized sequence.',
'1Sam.18.6-16 women antiphonal thousands/ten-thousands, jealousy/eye wording, evil-spirit and spear episodes, success/fear language are embedded plot evidence, not numeric history or diagnosis.',
'1Sam.18.17-30 Merab/Michal sequence, bride-price and body-language, love/fear terms and campaign totals require textual/social review; no marriage or moral ruling.',
'1Sam.19.1-7 kill-command, Jonathan advocacy, oath and restoration vocabulary support a completed intercession scene; covenant/political implications remain evidence only.',
'1Sam.19.8-17 spear wording, escape timing, Michal deception, teraphim/image, goats-hair pillow and illness report remain translation/social pressures only.',
'1Sam.19.18-24 prophetic behavior, repeated messenger waves, Spirit language, stripping/lying and naked wording remain untranslated interpretive pressure; no psychological or cultic diagnosis.',
'1Sam.20 covenant and hesed language, family sacrifice, new-moon purity, insult terms, arrow sign and farewell oath support plan-test-fulfillment cohesion only.',
'1Sam.21 holy bread, sexual-purity language, Ahimelech/Ahijah/Abiathar name relations, Doeg title and Goliath sword wording require legal/textual review; WEB/MT numbering differs.',
'1Sam.21.10-15 Achish identity/title, recognition-song quotation, fear, changed-behavior and madness language remain narrative evidence only; no diagnosis or harmonization.',
'1Sam.22.1-5 cave/place names, distressed/debtor/bitter-soul labels, family movement, stronghold wording and Gad direction are social/geographic evidence only.',
'1Sam.22.6-23 Doeg office/title, Ahimelech defense, priest casualty count, Nob destruction and Abiathar name relations remain witness/agency pressures; no oracle harmonization.',
'1Sam.23.1-13 ephod/divine inquiry and counterfactual answers, Keilah deliverance/hand-over terms and force totals support inquiry-action cohesion only; no providence system.',
'1Sam.23.14-18 strengthen-his-hand-in-God, covenant, succession speech and Saul knowledge wording remain social/political/theological evidence only.',
'1Sam.23.19-29 WEB/MT numbering displacement around 23:29/24:1, Ziph/Maon geography, encirclement and messenger interruption require mapped textual review.',
'1Sam.24 WEB/MT verse displacement, cave euphemism cover-feet, robe-skirt cutting, anointed language, confession and oath remain evidence only; no kingship or source theory.',
'1Sam.25.1 Samuel death/burial placement, Nabal name wordplay, one-who-urinates-against-wall euphemism, hospitality/protection economics, bloodguilt, Abigail status, and marriage wording remain unresolved.',
'1Sam.26 spear/jar proof, deep-sleep agency, anointed language, David-Saul dialogue and relation to chapter 24 are literary evidence only; no doublet collapse or chronology.',
'1Sam.27.1-28.2 Philistine-service duration, raid locations/victims, David reports, Achish trust, ambiguous campaign/bodyguard dialogue and chronology remain unharmonized.',
'1Sam.28 medium/necromancer terminology, elohim at 28:13, perceived apparition identity, narrator naming, Saul inference, reported speech, consultation claims and tomorrow-with-me remain unresolved.',
'1Sam.29 Philistine ranks/units, commanders titles, recognition-song reuse, Achish innocence language, David protest and ambiguous loyalty speech remain narrative evidence only.',
'1Sam.30.1-20 spoil/captive terminology, grief/threat, ephod inquiry, Egyptian servant status, place names, combat duration and total-recovery claims require textual/social review.',
'1Sam.30.21-31 spoil division, wicked/worthless labels, equal-share statute/custom wording and gift destination register remain functional evidence only; no legal-history ruling.',
'1Sam.31 death wording, armor-bearer action, body stripping/display, burning/burial and fasting terms plus later 2Sam/Chronicles reports remain unresolved; no preferred account or harmonization.'
]
assert len(H)==44
for row,hold in zip(rows,H):
 row['original_language_translation_holds']=[hold+' Evidence only; no preferred reading, chronology, moral, political, occult, or theological conclusion.']
 row['hard_passage_forecast']=[hold]
p.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in rows),encoding='utf-8',newline='\n')
print(hashlib.sha256(p.read_bytes()).hexdigest())
