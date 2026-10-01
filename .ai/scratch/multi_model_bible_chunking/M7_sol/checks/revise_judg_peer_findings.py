import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'book_chunks'/'Judg'/'chunks.jsonl'
rows=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
fix={
'M7_sol-Judg-002':'Rejected expansion to Judg.1.22-1.36: the Bethel spy-and-mercy scene closes with the spared man founding Luz at 1:26; 1:27 opens Manasseh and a repeated multi-tribe non-dispossession register.',
'M7_sol-Judg-003':'Rejected atomization at Judg.1.28/29, 1.30/31, 1.32/33, and 1.33/34: repeated did-not-drive-out clauses form one escalating register whose Dan/Amorite territorial notice closes at 1:36.',
'M7_sol-Judg-005':'Rejected expansion to Judg.2.1-2.10: Bochim speech, weeping, naming, and sacrifice close at 2:5; 2:6 resumes Joshua dismissal as a retrospective generational frame.',
'M7_sol-Judg-007':'Rejected split Judg.3.7-8 / 3.9-11: apostasy and oppression are the causal setup for cry, raised deliverer, victory, rest, and death in the compact Othniel cycle.',
'M7_sol-Judg-009':'Rejected expansion to Judg.3.31-4.3: the after-him Shamgar deliverance is a complete annal; 4:1 begins a new apostasy formula explicitly keyed to Ehud death.',
'M7_sol-Judg-014':'Rejected split Judg.6.25-26 / 6.27-32: the night command requires its execution, city accusation, Joash response, and Jerubbaal naming consequence.',
'M7_sol-Judg-016':'Rejected split Judg.7.1-3 / 7.4-8: the fear dismissal and water test are two stages of one announced force-reduction procedure, closed by dismissal and retention of three hundred.',
'M7_sol-Judg-025':'Rejected split Judg.10.1-2 / 10.3-5: after-him formulae, tenure, death, burial, and the compact transition to 10:6 make Tola and Jair a paired minor-judge annal register.',
'M7_sol-Judg-031':'Rejected separate chunks Judg.12.8-10 / 12.11-12 / 12.13-15: repeated after-him, tenure, death, and burial formulae form a compact three-judge annal register.',
'M7_sol-Judg-035':'Rejected expansion to Judg.15.9-16.3: the Lehi scene closes with prayer, water/place notice, and twenty-year judge formula at 15:20; 16:1 opens a fresh Gaza arrival and ambush vignette.',
'M7_sol-Judg-037':'Rejected split Judg.16.23-27 / 16.28-31: the Dagon feast and mockery set up Samson placement and final prayer; collapse, death comparison, burial, and judge notice complete the scene.',
'M7_sol-Judg-039':'Rejected split Judg.18.1-6 / 18.7-10: Dan inheritance/scout commission and Micah-priest oracle govern the same reconnaissance mission whose Laish report and go-up exhortation close at 18:10.'}
seen=set()
for row in rows:
 if row['decision_id'] in fix:
  row['rejected_alternative']=fix[row['decision_id']]
  row['red_team_questions'][1]='Does this explicit rejected alternative better preserve the local form: '+fix[row['decision_id']]
  seen.add(row['decision_id'])
assert seen==set(fix)
p.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in rows),encoding='utf-8',newline='\n')
print(hashlib.sha256(p.read_bytes()).hexdigest())
