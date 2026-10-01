import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'book_chunks'/'Ruth'/'chunks.jsonl'; rows=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
h={
'M7_sol-Ruth-001':'Ruth.1.1-5 migration, personal/place-name forms, marriage-duration wording, and repeated bereavement terms are evidence only; they decide no chronology, ethnicity, providence, or theology.',
'M7_sol-Ruth-002':'Ruth.1.8 hesed/kindness language and Ruth.1.20-21 Naomi/Mara, pleasant/bitter, Shaddai, and affliction wordplay support cohesion only; they decide no conversion, ethnicity, providence, or theology.',
'M7_sol-Ruth-003':'Ruth.2.12 refuge-under-wings idiom and Ruth.2.20 hesed referent plus goel/near-redeemer vocabulary support the encounter/report relation only; they decide no legal system, ethnicity, providence, or theology.',
'M7_sol-Ruth-004':'Ruth.3.3-14 threshing-floor, uncover/feet, lying, secrecy, Ruth.3.9 wing/skirt petition, and Ruth.3.12-13 goel language are unresolved translation/social-legal pressures; they decide no sexual, legal, or theological reading.',
'M7_sol-Ruth-005':'Ruth.4.5 acquisition wording and witness pressure, Ruth.4.3-10 goel/redemption/inheritance and sandal custom, and Ruth.4.11-17 blessing, birth, naming, and son-to-Naomi language are evidence only; no property, marriage, ethnic, providential, or theological ruling.',
'M7_sol-Ruth-006':'Ruth.4.18 generations-of-Perez formula, repeated fathering clauses, and personal-name forms support a genealogy register only; they decide no completeness, chronology, authorship, harmonization, messianic, or genealogical theology claim.'}
for row in rows: row['original_language_translation_holds']=[h[row['decision_id']]]
p.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in rows),encoding='utf-8',newline='\n')
print(hashlib.sha256(p.read_bytes()).hexdigest())
