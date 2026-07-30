import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'book_chunks'/'Judg'/'chunks.jsonl'; rows=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
fix={
'M7_sol-Judg-004':'Preserve split Judg.2.1-3 / 2.4-5 as oracle versus response, but retain speech, weeping, place naming, and sacrifice as one oracle-response event; messenger/YHWH identity remains unresolved.',
'M7_sol-Judg-008':'Preserve splits Judg.3.12-18 / 3.19-26 / 3.27-30 as oppression/tribute, covert killing/escape, and muster/battle; the larger cycle retains causal setup, reversal, victory, and rest.',
'M7_sol-Judg-021':'Preserve split Judg.8.22-23 / 8.24-28 as rule offer/refusal versus gold-ephod-snare-rest; retain the larger aftermath because the request follows the rule exchange and reaches rest closure.',
'M7_sol-Judg-026':'Preserve split Judg.10.6-9 / 10.10-16 as apostasy/oppression versus cry, rebuttal, confession, removal, and grief; retain the complete accusation-response movement.',
'M7_sol-Judg-028':'Preserve Judg.11.12-13 / 11.14-27 / 11.28 as initial claim, full counterargument, and refusal; retain the entire messenger exchange so claim and answer remain together.',
'M7_sol-Judg-030':'Preserve split Judg.12.1-6 / 12.7 as Ephraim conflict/dialect test versus tenure-death-burial notice; retain verse 7 as Jephthah cycle closure.',
'M7_sol-Judg-034':'Preserve split Judg.15.9-17 / 15.18-20 as Judah handover/Lehi victory-poem versus thirst-prayer/water/judge notice; retain victory and narrated answer/closure together.',
'M7_sol-Judg-041':'Preserve split Judg.18.27-29 / 18.30-31 as Laish conquest/Dan naming versus image-priestly-line/Shiloh coda; retain founding and cult epilogue together while Moses/Manasseh pressure stays unresolved.',
'M7_sol-Judg-043':'Preserve split Judg.20.1-11 / 20.12-17 as assembly/testimony/decision versus Benjamin refusal and opposing musters; retain the conflict setup from summons response through battle readiness.',
'M7_sol-Judg-044':'Preserve Judg.20.18-23 / 20.24-25 / 20.26-28 as first inquiry-defeat, second defeat, and intensified third inquiry; retain their progressive repeated structure through the governing promise.',
'M7_sol-Judg-045':'Preserve split Judg.20.29-36 / 20.37-48 as ambush/reversal versus detailed collapse, remnant, and destruction; retain battle and immediate aftermath as one third-attempt resolution.',
'M7_sol-Judg-047':'Preserve split Judg.21.16-22 / 21.23-25 as Shiloh seizure plan versus execution, return, and final refrain; retain remedy and book-closing consequence together while oath/moral questions remain deferred.'}
seen=set()
for row in rows:
 if row['decision_id'] in fix:
  row['rejected_alternative']=fix[row['decision_id']]; row['red_team_questions'][1]='Does this explicit rejected alternative better preserve the local form: '+fix[row['decision_id']]; seen.add(row['decision_id'])
assert seen==set(fix)
p.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in rows),encoding='utf-8',newline='\n')
print(hashlib.sha256(p.read_bytes()).hexdigest())
