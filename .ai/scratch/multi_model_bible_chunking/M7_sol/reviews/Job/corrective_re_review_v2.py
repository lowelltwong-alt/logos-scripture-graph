#!/usr/bin/env python3
"""Deterministic candidate-only T562 Job corrective rereview materializer."""
from __future__ import annotations
import argparse,hashlib,json,re
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[6]
MODEL=ROOT/'.ai'/'scratch'/'multi_model_bible_chunking'/'M7_sol';REV=MODEL/'reviews'/'Job';CHUNKS=MODEL/'book_chunks'/'Job'/'chunks.jsonl'
STRATEGY=MODEL/'book_strategy'/'Job.md';CONTRACT=MODEL/'review_contract.yaml';WEB=ROOT/'data'/'canonical'/'translations'/'eng-web'/'translation_witnesses.jsonl'
USFM=ROOT/'data'/'processed'/'bible'/'eng-web'/'usfm'/'extracted'/'19-JOBeng-web.usfm';OSHB=ROOT/'data'/'candidate'/'original_language_evidence'/'canonical_source_views'/'openscriptures_oshb'/'files'/'Job.xml';UXLC=ROOT/'data'/'candidate'/'original_language_evidence'/'canonical_source_views'/'tanach_us_uxlc'/'files'/'Job.xml'
BOSS=REV/'fresh_boss_adjudication_v1.json';POST=REV/'post_appeal_boss_ruling_v1.json'
PREFIX_BYTES=69218;PREFIX_SHA='e06842c3aa239a87cc162e9b8c6a5916719b4f97efc194cb01dfb71f4cf0a62f'
APPEAL_IDS={'T562-JOB-HEBREW-APPEAL-001','T562-JOB-LIT-APPEAL-001','T562-JOB-CANONICAL-APPEAL-001'}
HELD_IDS={'M7_sol-Job-055','M7_sol-Job-061','M7_sol-Job-062','M7_sol-Job-082','M7_sol-Job-083','M7_sol-Job-091'}
FROZEN={'strategy':'5a00446e91b6314c6e1bfbaa15c67497b6d1e5e87457a4dc399600def165c3b5','contract':'a32f4fa9d83039b97d96fa9ffc2c795f60272e6424a3ae053bd8cfe5a70011e0','fresh_boss_adjudication_v1.json':'60015dfb8c0468fe27a4b3832671bb1e5ec8d987e1c14c33ff67f042036216a7','post_appeal_boss_ruling_v1.json':'1e1933f79697e003ff69c85a297b31d39a10a6c5ead37820967a93e59534855d','blind_primary_hebrew_poetics_v1.json':'55b922a794e4c466c997df2d8bc49feacfd30a49d2d4eed6264c2ab97e1c59cf','blind_primary_wisdom_literary_v1.json':'cf62ca04fa38d297baae03197a432e36c8f81bd23f0822aebf92057c3599bd75','blind_primary_canonical_retrieval_v1.json':'70b438523348eb9cc40babbcb78a5fc33df8a2f15e5424dca9566a06f0a3e64f','post_ruling_response_hebrew_v1.json':'3ff9edd45a8131685cb3c1953ad6160779c3c9784d6b745d190ca0005cf91d06','post_ruling_response_literary_v1.json':'19f574e2d8deda75f21663eafe63df34b4cdb1e2b3d8c3e1e93f5ae06fb5a973','post_ruling_response_canonical_v1.json':'9056df6e2dbc21ecfa162ca32cb8b5786cf2cf5ebbaf42daa722efb84e05920e','blind_primary_job41_crosswalk_correction_overlay_v1.json':'e48bf5b8a79deddeee8d5214a4f152f446a451e9575c7ea39a6f37e613d22ba5','blind_primary_integrity_recheck_v1.json':'6e0ef842f96b24be6a4e7049e96dc918e3c1b3b952d6bad1e7fb1df37b430d14','usfm':'0a26a0f438b5a1e4ed2e6e5f5dcbb9ac26da135d1f477789fff41852dab0841a','oshb':'7db3311184122f37a8fd52f3c7c0c4a6d2da7b77ee82f4fdb26bcba9171d297f','uxlc':'4236b06f89b4d1dffd4ae7e462802e2b9b75e55fa6d1756b4e4ca29ed1126935'}
SOURCE_FAIL='independent_frozen_route_source_redteam_v1.json';SOURCE_FAIL_SHA='45c9ff93c2894f8738c8f387c705603f8196b869ea0959077e363927cf6804c3'
QUOTE_OVERLAY='frozen_boss_quote_fidelity_correction_overlay_v1.json';QUOTE_OVERLAY_SHA='d08b4d02fd093c28473fbb98ac9e8457dde69ffd02cce22c71ee94b634974596'
SOURCE_RECHECK='independent_frozen_route_source_redteam_recheck_v1.json';SOURCE_RECHECK_SHA='ba0814fad08fc641570c976db76877a12c0403d0170842c3c9657a439b9b9dff'
SOURCE_BACKUP_FAIL='independent_frozen_route_source_redteam_backup_v1.json';SOURCE_BACKUP_FAIL_SHA='7cd2b5c405364627a736275108093ee20bc701de056cb396483b98333c09b621'
SOURCE_BOSS='source_fidelity_boss_ruling_v1.json';SOURCE_BOSS_SHA='5981e6b4588e4e34b6d5c9c51957b3e7a8751313209b1d9140cf3b5547798835'
HEBREW_OVERLAY='frozen_boss_hebrew_anchor_union_correction_overlay_v1.json';HEBREW_OVERLAY_SHA='0333c60a734b2476a71e47a601d0b86d9a026fb9c47fbed2a7211aa3c59ae75a'
SOURCE_FINAL='independent_frozen_route_source_redteam_final_v1.json';SOURCE_FINAL_SHA='3b291321735457d2a9817fe40d5090a98263244124144e0aff443f8b17aa8b2f'
SOURCE_BACKUP_FINAL='independent_frozen_route_source_redteam_backup_final_v1.json';SOURCE_BACKUP_FINAL_SHA='0cd9063fae8e4dd419fc08700b4a00716012eb4193ce28370b5ed72d31050182'
LITERARY='independent_frozen_route_literary_redteam_v1.json';LITERARY_SHA='3b1460aaf76f86dcc61340dfe2da14c1f83c93ae0181f3ac8628296a69e43a3f'
PROSE_LITERARY='materialized_prose_repair_literary_proposal_v1.json';PROSE_LITERARY_SHA='2bc5618c070784ead29d9a4cee50b994eb8a3f5af27c2f77fde90489402f8533'
PROSE_SOURCE='materialized_prose_repair_source_constraints_v1.json';PROSE_SOURCE_SHA='aef1ed686d8789baa07910c54a1a8ef0dcb6f78e88224ecd938f4ffdedbfcdd7'
PROSE_BOSS='materialized_prose_repair_boss_adjudication_v1.json';PROSE_BOSS_SHA='ccdf1dc1001c82cf975b0af33af1e90c7e102dd10cfc059a1d88fbeb9bc20fea'
PRIMARY_PROSE_LITERARY='materialized_primary_prose_repair_literary_proposal_v1.json';PRIMARY_PROSE_LITERARY_SHA='a61334776734bc8c430cbbe8f15763c80a5abf0880c6fc666bb9446bf5697ca3'
PRIMARY_PROSE_SOURCE='materialized_primary_prose_repair_source_constraints_v1.json';PRIMARY_PROSE_SOURCE_SHA='5544fa020f75ef5ac576c236493ac01f64bce147fe2593cc12a3f533d83904b7'
PRIMARY_PROSE_BOSS='materialized_primary_prose_repair_boss_adjudication_v1.json';PRIMARY_PROSE_BOSS_SHA='023250fc9ac8e6fb12c0faf5482ef65c37efa960e694318c09b226b196d690e1'
ROLES=(('hebrew','hebrew_poetics','original_language_translation_specialist','blind_primary_hebrew_poetics_v1.json'),('literary','wisdom_literary','wisdom_dialogue_literary_form_specialist','blind_primary_wisdom_literary_v1.json'),('canonical','canonical_retrieval','canonical_relations_retrieval_premortem_primary','blind_primary_canonical_retrieval_v1.json'))
INDEP={'independent_from_sibling_model_maps':True,'primaries_blind_to_each_other_artifacts':True,'roles_separated':True,'shared_model_substrate':True,'counts_as_cross_model_independent_votes':False,'independent_model_or_human_evidence_required_at_convergence':True,'reviewer_count_is_not_authority':True,'correlated_mesh_weight_at_convergence':'one_model_voice'}
def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def shab(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def rj(p:Path)->dict[str,Any]:
 x=json.loads(p.read_text(encoding='utf-8'))
 if not isinstance(x,dict):raise ValueError(f'{p}: expected object')
 return x
def rjl(p:Path)->list[dict[str,Any]]:
 if not p.exists():return []
 out=[]
 for n,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
  if line.strip():
   x=json.loads(line)
   if not isinstance(x,dict):raise ValueError(f'{p}:{n}: expected object')
   out.append(x)
 return out
def jb(x:Any,pretty:bool=False)->bytes:return (json.dumps(x,ensure_ascii=False,indent=2) if pretty else json.dumps(x,ensure_ascii=False,separators=(',',':'))).encode('utf-8')+b'\n'
def jlb(xs:list[dict[str,Any]])->bytes:return b''.join(jb(x) for x in xs)
def wj(p:Path,x:Any)->None:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(jb(x,True))
def wjl(p:Path,x:list[dict[str,Any]])->None:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(jlb(x))
def rowsha(x:dict[str,Any])->str:return shab(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'))
def iter_strings(x:Any):
 if isinstance(x,str):yield x
 elif isinstance(x,dict):
  for v in x.values():yield from iter_strings(v)
 elif isinstance(x,list):
  for v in x:yield from iter_strings(v)
def effective_strings(x:Any,rules:list[dict[str,Any]])->Any:
 if isinstance(x,str):
  for r in rules:x=x.replace(r['actual_token'],r['effective_token'])
  return x
 if isinstance(x,list):return [effective_strings(v,rules) for v in x]
 if isinstance(x,dict):return {k:effective_strings(v,rules) for k,v in x.items()}
 return x
def token_count(x:Any,token:str)->int:return sum(v.count(token) for v in iter_strings(x))
def assert_no_bad_tokens(x:Any,rules:list[dict[str,Any]],label:str)->None:
 leaks={r['actual_token']:token_count(x,r['actual_token']) for r in rules if token_count(x,r['actual_token'])}
 if leaks:raise ValueError(f'{label}: superseded quote token leakage {leaks}')
def hebrew_count(x:Any)->int:return sum(1 for s in iter_strings(x) for c in s if '\u0590'<=c<='\u05ff')
def assert_no_hebrew_targets(x:Any,rules:list[dict[str,Any]],label:str)->None:
 by={r['decision_id']:r['actual_disputed_hebrew_target'] for r in rules};leaks:Counter[str]=Counter()
 def walk(v:Any,scope:str|None=None)->None:
  if isinstance(v,dict):
   own=str(v.get('decision_id') or '');scope=own if own in by else scope
   for child in v.values():walk(child,scope)
  elif isinstance(v,list):
   for child in v:walk(child,scope)
  elif isinstance(v,str) and scope in by and by[scope] in v:leaks[scope]+=v.count(by[scope])
 walk(x)
 if leaks:raise ValueError(f'{label}: scoped superseded Hebrew target leakage {dict(leaks)}')
def apply_hebrew_rules(route:list[dict[str,Any]],rules:list[dict[str,Any]])->list[dict[str,Any]]:
 by={r['decision_id']:r for r in rules}
 if len(by)!=14 or len(by)!=len(rules):raise ValueError('Hebrew overlay decision rules are not exactly 14 unique rows')
 out=[]
 for raw in route:
  did=raw['decision_id'];r=by.get(did)
  if r is None:out.append(raw);continue
  target=r['actual_disputed_hebrew_target'];replacement=r['source_neutral_effective_replacement'];expected=r['exact_base_occurrences_within_decision']
  if expected!=3 or token_count(raw,target)!=expected:raise ValueError(f'{did}: Hebrew target base occurrence count changed')
  if re.search(r'[\u0590-\u05ff]',replacement):raise ValueError(f'{did}: source-neutral replacement introduces Hebrew quotation')
  before=hebrew_count(raw);effective=effective_strings(raw,[{'actual_token':target,'effective_token':replacement}])
  if token_count(effective,target)!=0:raise ValueError(f'{did}: scoped Hebrew target replacement incomplete')
  if hebrew_count(effective)!=before-(expected*hebrew_count(target)):raise ValueError(f'{did}: Hebrew overlay introduced or removed unscoped Hebrew text')
  out.append(effective)
 if set(by)!={x['decision_id'] for x in out if x['decision_id'] in by}:raise ValueError('Hebrew overlay route decision coverage changed')
 assert_no_hebrew_targets(out,rules,'effective frozen boss route')
 return out
def apply_prose_rules(route:list[dict[str,Any]],rules:list[dict[str,Any]])->list[dict[str,Any]]:
 by={r['decision_id']:r for r in rules}
 if len(by)!=14 or len(by)!=len(rules):raise ValueError('prose repair decisions are not exactly 14 unique rows')
 out=[]
 for raw in route:
  u=dict(raw);r=by.get(u['decision_id'])
  if r is not None:
   if u['span']!=r['span'] or u['literary_form']!=r['preserved_literary_form'] or u['confidence']!=r['preserved_confidence'] or u['disposition']!=r['preserved_candidate_state']:raise ValueError(f"{u['decision_id']}: prose repair changes a frozen literary or state field")
   marker=r['final_deciding_marker_or_seam'];rat=r['final_boundary_rationale']
   if re.search(r'[\u0590-\u05ff]',marker+rat):raise ValueError(f"{u['decision_id']}: prose repair reintroduces Hebrew script")
   for target in r['forbidden_disputed_tokens']:
    if target in marker or target in rat:raise ValueError(f"{u['decision_id']}: prose repair reintroduces a forbidden source target")
   u['deciding_marker_or_seam']=marker;u['_effective_boundary_rationale']=rat
  out.append(u)
 if set(by)!={x['decision_id'] for x in out if x['decision_id'] in by}:raise ValueError('prose repair route decision coverage changed')
 return out
def mt_ref(r:str)->str:
 b,c0,v0=r.split('.');c,v=int(c0),int(v0)
 if b!='Job':raise ValueError(r)
 if c==41 and v<=8:return f'Job.40.{v+24}'
 if c==41:return f'Job.41.{v-8}'
 return r
def mt_span(s:str)->str:
 a,b=s.split('-');return f'{mt_ref(a)}-{mt_ref(b)}'
def srefs(span:str,did:str)->list[Any]:
 mapped=mt_span(span);status='validated_job_web_41_to_mt_40_25_through_41_26_crosswalk' if mapped!=span else 'validated_job_web_mt_same_coordinates';out:[Any]=[f'direct_read:eng-web:{span}']
 for sid in ('oshb','uxlc'):out.append({'source_id':sid,'span':span,'web_span':span,'source_span':mapped,'coordinate_system':'MT_WLC','crosswalk_status':status,'source_metadata_boundary_authority':False,'versification_crosswalk_is_evidence_only':True,'wlc_family_correlation_disclosed':True,'oshb_uxlc_are_independent_witnesses':False,'observation':f'{did}:{sid.upper()} correlated WLC-family locator {mapped}'})
 return out
def _verify_pre_hebrew_gate()->tuple[dict[str,str],list[dict[str,Any]]]:
 paths={'strategy':STRATEGY,'contract':CONTRACT,'fresh_boss_adjudication_v1.json':BOSS,'post_appeal_boss_ruling_v1.json':POST,'usfm':USFM,'oshb':OSHB,'uxlc':UXLC}
 for _c,_l,_r,n in ROLES:paths[n]=REV/n
 for n in ('post_ruling_response_hebrew_v1.json','post_ruling_response_literary_v1.json','post_ruling_response_canonical_v1.json','blind_primary_job41_crosswalk_correction_overlay_v1.json','blind_primary_integrity_recheck_v1.json'):paths[n]=REV/n
 for n,p in paths.items():
  got=sha(p)
  if got!=FROZEN[n]:raise ValueError(f'frozen Job input changed: {n} {got} != {FROZEN[n]}')
 crosswalk=rj(REV/'blind_primary_job41_crosswalk_correction_overlay_v1.json');primary_recheck=rj(REV/'blind_primary_integrity_recheck_v1.json')
 if crosswalk.get('defect_instance_count')!=11 or primary_recheck.get('verdict')!='pass_effective_view_safe_for_boss_use' or primary_recheck.get('remaining_effective_defect_count')!=0:raise ValueError('Job primary effective-view repair/recheck is not green')
 fail_path=REV/SOURCE_FAIL;overlay_path=REV/QUOTE_OVERLAY;lit_path=REV/LITERARY;source_recheck_path=REV/SOURCE_RECHECK
 if sha(fail_path)!=SOURCE_FAIL_SHA or sha(overlay_path)!=QUOTE_OVERLAY_SHA or sha(lit_path)!=LITERARY_SHA:raise ValueError('quote-fidelity evidence chain hash changed')
 lit=rj(lit_path)
 if lit.get('verdict')!='pass' or lit.get('blocking_defect_count')!=0 or lit.get('blocking_defects') not in ([],None):raise ValueError('literary frozen-route gate is not exact clean PASS')
 fail=rj(fail_path);fsummary=fail.get('defect_summary') or {};fquote=(fail.get('checks') or {}).get('curly_quoted_web_phrase_fidelity') or {}
 expected_decisions={'M7_sol-Job-033','M7_sol-Job-048','M7_sol-Job-049','M7_sol-Job-050','M7_sol-Job-051','M7_sol-Job-054','M7_sol-Job-059','M7_sol-Job-060','M7_sol-Job-070','M7_sol-Job-075','M7_sol-Job-076','M7_sol-Job-078','M7_sol-Job-080','M7_sol-Job-088'};defects=fquote.get('blocking_defects') or []
 if fail.get('overall_verdict')!='fail_blocking_source_quote_fidelity' or fsummary.get('blocking_defect_count')!=15 or fsummary.get('blocking_root_cause_count')!=1 or set(fsummary.get('blocking_decisions') or [])!=expected_decisions:raise ValueError('preserved source FAIL identity/counts changed')
 if fquote.get('verdict')!='fail' or fquote.get('failed_instances')!=15 or fquote.get('distinct_failed_phrases')!=11 or len(defects)!=15 or {x.get('defect_id') for x in defects}!={f'T562-JOB-SOURCE-QUOTE-{n:03d}' for n in range(1,16)}:raise ValueError('preserved source FAIL defects changed')
 overlay=rj(overlay_path);rules=overlay.get('replacement_rules') or []
 if overlay.get('audited_failed_claim_instances')!=15 or overlay.get('audited_distinct_failed_phrases')!=11 or overlay.get('affected_decision_count')!=14 or overlay.get('effective_boss_string_occurrence_count')!=29 or len(rules)!=11:raise ValueError('quote overlay counts changed')
 if overlay.get('base_inputs')!={'fresh_boss_sha256':FROZEN['fresh_boss_adjudication_v1.json'],'post_appeal_boss_ruling_sha256':FROZEN['post_appeal_boss_ruling_v1.json'],'source_redteam_fail_sha256':SOURCE_FAIL_SHA,'literary_redteam_pass_sha256':LITERARY_SHA}:raise ValueError('quote overlay base bindings changed')
 if len({r.get('rule_id') for r in rules})!=11 or len({r.get('actual_token') for r in rules})!=11 or len({r.get('effective_token') for r in rules})!=11 or sum(r.get('boss_occurrences',0) for r in rules)!=29:raise ValueError('quote overlay rules are not unique/exact')
 if any(any(q in str(r.get('effective_token','')) for q in ('"','“','”')) for r in rules):raise ValueError('effective quote replacement still claims quotation')
 if {str(r.get('actual_token','')).strip('“”') for r in rules}!={str(x.get('quoted_phrase','')) for x in defects}:raise ValueError('overlay phrases do not exactly cover preserved source defects')
 raw_boss=rj(BOSS)
 for r in rules:
  if token_count(raw_boss.get('final_candidate_route'),r['actual_token'])!=r['boss_occurrences']:raise ValueError(f"quote overlay boss count changed: {r['rule_id']}")
 if not source_recheck_path.is_file():raise ValueError(f'mandatory fresh source recheck absent: {source_recheck_path}')
 recheck_sha=sha(source_recheck_path);recheck=rj(source_recheck_path)
 if sha(source_recheck_path)!=recheck_sha:raise ValueError('source recheck changed while read')
 verdict=str(recheck.get('overall_verdict') or recheck.get('verdict') or '').lower();gate=str(recheck.get('materialization_gate') or '').lower();summary=recheck.get('defect_summary') or {};checks=recheck.get('checks') or {}
 quote=checks.get('quote_repair_overlay') or checks.get('curly_quoted_web_phrase_fidelity') or checks.get('effective_quote_fidelity') or checks.get('quote_fidelity') or {};hebrew=checks.get('hebrew_deciding_anchor_token_collation') or checks.get('hebrew_phrase_token_fidelity') or checks.get('hebrew_script_phrase_token_collation') or checks.get('hebrew_phrase_collation') or {}
 if not verdict.startswith('pass') or 'block' in gate:raise ValueError('fresh source recheck is not PASS/materialization-safe')
 if summary.get('blocking_defect_count',summary.get('remaining_blocking_defect_count',recheck.get('blocking_defect_count'))) != 0:raise ValueError('fresh source recheck retains blocking defects')
 if str(quote.get('verdict','')).lower()!='pass' or quote.get('failed_instances',quote.get('remaining_defect_count',0))!=0:raise ValueError('fresh source recheck quote fidelity is not zero-defect PASS')
 if str(hebrew.get('verdict','')).lower()!='pass' or 'coverage_unavailable' in json.dumps(hebrew).lower() or hebrew.get('completed') is False or hebrew.get('claims_checked')!=107 or hebrew.get('failed_claims',hebrew.get('remaining_defect_count',0))!=0:raise ValueError('fresh source recheck lacks completed zero-defect Hebrew phrase collation PASS')
 bound=set(iter_strings(recheck));required={FROZEN['fresh_boss_adjudication_v1.json'],FROZEN['post_appeal_boss_ruling_v1.json'],SOURCE_FAIL_SHA,QUOTE_OVERLAY_SHA,LITERARY_SHA}
 if not required.issubset(bound):raise ValueError('fresh source recheck is not hash-bound to the full correction chain')
 return {SOURCE_FAIL:SOURCE_FAIL_SHA,QUOTE_OVERLAY:QUOTE_OVERLAY_SHA,SOURCE_RECHECK:recheck_sha,LITERARY:LITERARY_SHA},rules
def _named_dicts(x:Any,needles:tuple[str,...],path:str='')->list[tuple[str,dict[str,Any]]]:
 out=[]
 if isinstance(x,dict):
  for k,v in x.items():
   child=f'{path}.{k}' if path else str(k)
   if isinstance(v,dict) and any(n in str(k).lower() for n in needles):out.append((child,v))
   out.extend(_named_dicts(v,needles,child))
 elif isinstance(x,list):
  for i,v in enumerate(x):out.extend(_named_dicts(v,needles,f'{path}[{i}]'))
 return out
def _zeroish(x:Any)->bool:
 if x in (0,None,False):return True
 if isinstance(x,(list,dict)):return len(x)==0 or (isinstance(x,dict) and all(_zeroish(v) for v in x.values()))
 return False
def _zero_current_defects(x:Any,label:str)->None:
 zero_keys={'blocking_defect_count','remaining_blocking_defect_count','remaining_nonblocking_defect_count','remaining_defect_count','failed_instances','failed_claims','failure_count','failures','mismatches','leaks','target_leakage_count','new_hebrew_quote_count','coverage_unavailable_checks','blocking_defects','blocking_classes','pin_errors'}
 if isinstance(x,dict):
  for k,v in x.items():
   failure_suffix=any(k.lower().endswith(s) for s in ('_failure_count','_failures','_error_count','_leak_count','_mismatch_count','_out_of_bounds_count'))
   if (k in zero_keys or failure_suffix) and not _zeroish(v):raise ValueError(f'{label}: nonzero {k}={v!r}')
   _zero_current_defects(v,label)
 elif isinstance(x,list):
  for v in x:_zero_current_defects(v,label)
def _verify_final_source_report(path:Path)->str:
 if not path.is_file():raise ValueError(f'mandatory final source report absent: {path}')
 report=rj(path);verdict=str(report.get('overall_verdict') or report.get('verdict') or '').lower();gate=str(report.get('materialization_gate') or report.get('source_gate') or '').lower()
 if not verdict.startswith('pass') or 'block' in gate:raise ValueError(f'{path.name}: final source verdict/gate is not PASS')
 _zero_current_defects(report,path.name);summary=report.get('defect_summary') or {};_zero_current_defects(summary,f'{path.name}:defect_summary')
 if report.get('blocking_defects') not in (None,[]):raise ValueError(f'{path.name}: blocking defects remain')
 checks=report.get('checks') or report.get('deterministic_source_checks') or {k:v for k,v in report.items() if isinstance(v,dict) and ('check' in k.lower() or k in ('ketiv_qere_apparatus_nonselection','coverage_and_invariance'))}
 if not isinstance(checks,dict) or not checks:raise ValueError(f'{path.name}: final source checks absent')
 for name,check in checks.items():
  if not isinstance(check,dict):continue
  cv=str(check.get('verdict') or check.get('status') or '').lower()
  if cv and not cv.startswith('pass'):raise ValueError(f'{path.name}:{name}: check not PASS')
  _zero_current_defects(check,f'{path.name}:{name}')
 hebrew=_named_dicts(report,('hebrew',))
 if not hebrew:raise ValueError(f'{path.name}: Hebrew final collation absent')
 hebrew_status=[str(x.get('verdict') or x.get('status') or '').lower() for _n,x in hebrew if x.get('verdict') or x.get('status')]
 if any(v.startswith('fail') for v in hebrew_status) or (hebrew_status and not any(v.startswith('pass') for v in hebrew_status)):raise ValueError(f'{path.name}: Hebrew final check failed')
 completion=[]
 for name,x in hebrew:
  _zero_current_defects(x,f'{path.name}:{name}')
  for k,v in x.items():
   if isinstance(v,int) and not isinstance(v,bool) and any(t in k.lower() for t in ('checked','collated','validated','claim','target','rule','row')):completion.append(v)
 if not completion or max(completion)<14:raise ValueError(f'{path.name}: remaining-Hebrew collation is not complete for all 14 union repairs')
 quote=_named_dicts(report,('english','quote'))
 quote_status=[str(x.get('verdict') or x.get('status') or '').lower() for _n,x in quote if x.get('verdict') or x.get('status')]
 if not quote or any(v.startswith('fail') for v in quote_status) or (quote_status and not any(v.startswith('pass') for v in quote_status)):raise ValueError(f'{path.name}: English quote-fidelity check failed or absent')
 for name,x in quote:_zero_current_defects(x,f'{path.name}:{name}')
 bound=set(iter_strings(report));required={FROZEN['fresh_boss_adjudication_v1.json'],FROZEN['post_appeal_boss_ruling_v1.json'],SOURCE_BOSS_SHA,QUOTE_OVERLAY_SHA,HEBREW_OVERLAY_SHA}
 if not required.issubset(bound):raise ValueError(f'{path.name}: final report is not hash-bound to all frozen route, fail, ruling, and overlay evidence')
 return sha(path)
def verify()->tuple[dict[str,str],list[dict[str,Any]],list[dict[str,Any]],list[dict[str,Any]],list[dict[str,Any]]]:
 paths={'strategy':STRATEGY,'contract':CONTRACT,'fresh_boss_adjudication_v1.json':BOSS,'post_appeal_boss_ruling_v1.json':POST,'usfm':USFM,'oshb':OSHB,'uxlc':UXLC}
 for _c,_l,_r,n in ROLES:paths[n]=REV/n
 for n in ('post_ruling_response_hebrew_v1.json','post_ruling_response_literary_v1.json','post_ruling_response_canonical_v1.json','blind_primary_job41_crosswalk_correction_overlay_v1.json','blind_primary_integrity_recheck_v1.json'):paths[n]=REV/n
 for n,p in paths.items():
  got=sha(p)
  if got!=FROZEN[n]:raise ValueError(f'frozen Job input changed: {n} {got} != {FROZEN[n]}')
 crosswalk=rj(REV/'blind_primary_job41_crosswalk_correction_overlay_v1.json');primary_recheck=rj(REV/'blind_primary_integrity_recheck_v1.json')
 if crosswalk.get('defect_instance_count')!=11 or primary_recheck.get('verdict')!='pass_effective_view_safe_for_boss_use' or primary_recheck.get('remaining_effective_defect_count')!=0:raise ValueError('Job primary effective-view repair/recheck is not green')
 evidence_hashes={SOURCE_FAIL:SOURCE_FAIL_SHA,SOURCE_RECHECK:SOURCE_RECHECK_SHA,SOURCE_BACKUP_FAIL:SOURCE_BACKUP_FAIL_SHA,SOURCE_BOSS:SOURCE_BOSS_SHA,QUOTE_OVERLAY:QUOTE_OVERLAY_SHA,HEBREW_OVERLAY:HEBREW_OVERLAY_SHA,LITERARY:LITERARY_SHA}
 for n,expected in evidence_hashes.items():
  got=sha(REV/n)
  if got!=expected:raise ValueError(f'Job source/literary evidence changed: {n} {got} != {expected}')
 lit=rj(REV/LITERARY)
 if lit.get('verdict')!='pass' or lit.get('blocking_defect_count')!=0 or lit.get('blocking_defects') not in ([],None):raise ValueError('literary frozen-route gate is not exact clean PASS')
 fail=rj(REV/SOURCE_FAIL);fsummary=fail.get('defect_summary') or {};fquote=(fail.get('checks') or {}).get('curly_quoted_web_phrase_fidelity') or {};defects=fquote.get('blocking_defects') or []
 expected_quote_decisions={'M7_sol-Job-033','M7_sol-Job-048','M7_sol-Job-049','M7_sol-Job-050','M7_sol-Job-051','M7_sol-Job-054','M7_sol-Job-059','M7_sol-Job-060','M7_sol-Job-070','M7_sol-Job-075','M7_sol-Job-076','M7_sol-Job-078','M7_sol-Job-080','M7_sol-Job-088'}
 if fail.get('overall_verdict')!='fail_blocking_source_quote_fidelity' or fsummary.get('blocking_defect_count')!=15 or fsummary.get('blocking_root_cause_count')!=1 or set(fsummary.get('blocking_decisions') or [])!=expected_quote_decisions:raise ValueError('preserved English source FAIL identity/counts changed')
 if fquote.get('verdict')!='fail' or fquote.get('failed_instances')!=15 or fquote.get('distinct_failed_phrases')!=11 or len(defects)!=15:raise ValueError('preserved English source FAIL defects changed')
 quote_overlay=rj(REV/QUOTE_OVERLAY);quote_rules=quote_overlay.get('replacement_rules') or []
 if quote_overlay.get('audited_failed_claim_instances')!=15 or quote_overlay.get('audited_distinct_failed_phrases')!=11 or quote_overlay.get('affected_decision_count')!=14 or quote_overlay.get('effective_boss_string_occurrence_count')!=29 or len(quote_rules)!=11:raise ValueError('English quote overlay counts changed')
 if quote_overlay.get('base_inputs')!={'fresh_boss_sha256':FROZEN['fresh_boss_adjudication_v1.json'],'post_appeal_boss_ruling_sha256':FROZEN['post_appeal_boss_ruling_v1.json'],'source_redteam_fail_sha256':SOURCE_FAIL_SHA,'literary_redteam_pass_sha256':LITERARY_SHA}:raise ValueError('English quote overlay base bindings changed')
 if len({r.get('rule_id') for r in quote_rules})!=11 or len({r.get('actual_token') for r in quote_rules})!=11 or len({r.get('effective_token') for r in quote_rules})!=11 or sum(r.get('boss_occurrences',0) for r in quote_rules)!=29:raise ValueError('English quote overlay rules are not unique/exact')
 if any(re.search(r'["\u201c\u201d]',str(r.get('effective_token',''))) for r in quote_rules):raise ValueError('effective English replacement still claims quotation')
 if {str(r.get('actual_token','')).strip('\u201c\u201d') for r in quote_rules}!={str(x.get('quoted_phrase','')) for x in defects}:raise ValueError('English overlay phrases do not exactly cover preserved source defects')
 raw_boss=rj(BOSS)
 for r in quote_rules:
  if token_count(raw_boss.get('final_candidate_route'),r['actual_token'])!=r['boss_occurrences']:raise ValueError(f"English quote overlay boss count changed: {r['rule_id']}")
 source_boss=rj(REV/SOURCE_BOSS);expected_union={'M7_sol-Job-003','M7_sol-Job-008','M7_sol-Job-017','M7_sol-Job-022','M7_sol-Job-026','M7_sol-Job-044','M7_sol-Job-048','M7_sol-Job-053','M7_sol-Job-062','M7_sol-Job-070','M7_sol-Job-072','M7_sol-Job-077','M7_sol-Job-090','M7_sol-Job-093'};expected_intersection={'M7_sol-Job-017','M7_sol-Job-022','M7_sol-Job-048','M7_sol-Job-062','M7_sol-Job-077','M7_sol-Job-090','M7_sol-Job-093'};expected_strict={'M7_sol-Job-003','M7_sol-Job-026','M7_sol-Job-044','M7_sol-Job-053','M7_sol-Job-072'};expected_backup={'M7_sol-Job-008','M7_sol-Job-070'}
 expected_boss_inputs={'fresh_boss_adjudication':FROZEN['fresh_boss_adjudication_v1.json'],'primary_strict_pointed_recheck':SOURCE_RECHECK_SHA,'backup_consonantal_report':SOURCE_BACKUP_FAIL_SHA,'english_quote_correction_overlay':QUOTE_OVERLAY_SHA,'review_contract':FROZEN['contract'],'oshb_job_xml':FROZEN['oshb'],'uxlc_job_xml':FROZEN['uxlc'],'web_usfm_member':FROZEN['usfm'],'job41_crosswalk_overlay':FROZEN['blind_primary_job41_crosswalk_correction_overlay_v1.json']}
 if source_boss.get('input_hashes')!=expected_boss_inputs:raise ValueError('source-fidelity boss input bindings changed')
 ar=source_boss.get('set_arithmetic') or {}
 if (ar.get('primary_strict_failure_count'),ar.get('backup_consonantal_failure_count'),ar.get('union_count'),ar.get('intersection_count'),ar.get('strict_only_count'),ar.get('backup_only_count'))!=(12,9,14,7,5,2):raise ValueError('source-fidelity boss set arithmetic changed')
 if set(ar.get('union') or [])!=expected_union or set(ar.get('intersection') or [])!=expected_intersection or set(ar.get('strict_only') or [])!=expected_strict or set(ar.get('backup_only') or [])!=expected_backup:raise ValueError('source-fidelity boss decision sets changed')
 preservation=source_boss.get('preservation_and_non_authority') or {}
 if preservation.get('preserve_fail_reports_append_only') is not True or any(preservation.get(k) is not False for k in ('selects_ketiv_or_qere','selects_pointing','selects_reading','selects_witness','changes_boundary','changes_state','changes_appeal','changes_theology_or_canon')):raise ValueError('source-fidelity boss preservation/non-selection ruling changed')
 hebrew_overlay=rj(REV/HEBREW_OVERLAY);hebrew_rules=hebrew_overlay.get('repair_rules') or []
 expected_overlay_inputs={'fresh_boss_sha256':FROZEN['fresh_boss_adjudication_v1.json'],'post_appeal_boss_ruling_sha256':FROZEN['post_appeal_boss_ruling_v1.json'],'strict_source_recheck_fail_sha256':SOURCE_RECHECK_SHA,'backup_source_fail_sha256':SOURCE_BACKUP_FAIL_SHA,'source_fidelity_boss_ruling_sha256':SOURCE_BOSS_SHA,'english_quote_overlay_sha256':QUOTE_OVERLAY_SHA}
 if hebrew_overlay.get('base_inputs')!=expected_overlay_inputs:raise ValueError('Hebrew union overlay base bindings changed')
 if (hebrew_overlay.get('union_decision_count'),hebrew_overlay.get('intersection_decision_count'),hebrew_overlay.get('strict_only_count'),hebrew_overlay.get('backup_only_count'),hebrew_overlay.get('exact_effective_boss_occurrence_count'),len(hebrew_rules))!=(14,7,5,2,42,14):raise ValueError('Hebrew union overlay counts changed')
 if hebrew_overlay.get('application_order')!=['fresh boss','post-appeal disposition override','Job 41 crosswalk overlay','English quote-fidelity overlay','this Hebrew-anchor union overlay']:raise ValueError('Hebrew union overlay application order changed')
 if {r.get('decision_id') for r in hebrew_rules}!=expected_union or len({r.get('actual_disputed_hebrew_target') for r in hebrew_rules})!=14 or sum(r.get('exact_base_occurrences_within_decision',0) for r in hebrew_rules)!=42:raise ValueError('Hebrew union overlay rules are not unique/exact')
 boss_rules={r['decision_id']:r for r in source_boss.get('per_decision_repair_rules') or []}
 if set(boss_rules)!=expected_union:raise ValueError('source-fidelity boss per-decision rule set changed')
 raw_route={x['decision_id']:x for x in raw_boss['final_candidate_route']}
 for r in hebrew_rules:
  did=r['decision_id'];br=boss_rules[did];target=r['actual_disputed_hebrew_target'];replacement=r['source_neutral_effective_replacement']
  if r.get('exact_base_occurrences_within_decision')!=3 or token_count(raw_route[did],target)!=3:raise ValueError(f'{did}: Hebrew overlay base occurrence binding changed')
  if br.get('disputed_targets')!=[target] or br.get('safe_source_neutral_replacement')!=replacement or br.get('membership')!=r.get('membership'):raise ValueError(f'{did}: Hebrew overlay diverges from boss ruling')
  if re.search(r'[\u0590-\u05ff]',replacement):raise ValueError(f'{did}: Hebrew overlay replacement is not source-neutral')
  if did in {'M7_sol-Job-090','M7_sol-Job-093'} and r.get('ketiv_qere_or_apparatus_guard')!='Preserve serialized alternatives; select no ketiv, qere, pointing, witness, or reading.':raise ValueError(f'{did}: apparatus non-selection guard changed')
 final_sha=_verify_final_source_report(REV/SOURCE_FINAL);backup_final_sha=_verify_final_source_report(REV/SOURCE_BACKUP_FINAL)
 if final_sha!=SOURCE_FINAL_SHA or backup_final_sha!=SOURCE_BACKUP_FINAL_SHA:raise ValueError('final source report hash changed')
 prose_paths={PROSE_LITERARY:PROSE_LITERARY_SHA,PROSE_SOURCE:PROSE_SOURCE_SHA,PROSE_BOSS:PROSE_BOSS_SHA}
 for n,expected in prose_paths.items():
  got=sha(REV/n)
  if got!=expected:raise ValueError(f'Job prose-repair mesh evidence changed: {n} {got} != {expected}')
 prose_lit=rj(REV/PROSE_LITERARY);prose_source=rj(REV/PROSE_SOURCE);prose_boss=rj(REV/PROSE_BOSS)
 final_judgment=prose_boss.get('final_judgment') or {};comparison=prose_boss.get('comparison_result') or {};contract=prose_boss.get('application_contract') or {}
 expected_prose_inputs={PROSE_LITERARY:PROSE_LITERARY_SHA,PROSE_SOURCE:PROSE_SOURCE_SHA,'book_chunks/Job/chunks.jsonl':'038f5da03133d94e2aa007777c0bb2fedf6073ccddb5190b2d5e998d675d9d07','review_packets.jsonl':'ea04b2cc9ecce98f3692909d38ef1ec59ff85a4e5c8248e5db87c1075d1ee44a','decision_evidence_v2.jsonl':'70ce935d29e814ccb0449c37115f6cf8346829049d8b5153124ba9c765ae2355',SOURCE_BOSS:SOURCE_BOSS_SHA,HEBREW_OVERLAY:HEBREW_OVERLAY_SHA}
 if prose_boss.get('input_hashes')!=expected_prose_inputs:raise ValueError('prose boss input bindings changed')
 if final_judgment.get('status')!='pass_no_holds' or final_judgment.get('held_decision_ids')!=[] or final_judgment.get('overturned_boundary_or_state_ruling_count')!=0:raise ValueError('prose boss did not return exact no-hold pass')
 if comparison.get('decision_count')!=14 or comparison.get('accepted_repair_count')!=14 or comparison.get('held_repair_count')!=0 or any(comparison.get(k)!=0 for k in ('old_text_binding_error_count','state_invariant_error_count','forbidden_token_error_count','hebrew_reconstruction_error_count','proposal_scope_difference_count')) or comparison.get('verdict')!='pass_no_holds':raise ValueError('prose boss comparison is not zero-defect')
 if contract.get('authorized_future_change')!='prose_only_exactly_as_adjudicated' or contract.get('active_artifacts_modified_by_this_adjudication') is not False:raise ValueError('prose boss application contract changed')
 proposals={x['decision_id']:x for x in prose_lit.get('proposals') or []};constraints={x['decision_id']:x for x in prose_source.get('decisions') or []};prose_rules=prose_boss.get('adjudications') or [];adjudicated={x['decision_id']:x for x in prose_rules}
 if set(proposals)!=expected_union or set(constraints)!=expected_union or set(adjudicated)!=expected_union or any(len(x)!=14 for x in (proposals,constraints,adjudicated)):raise ValueError('prose mesh decision sets changed')
 pre_route=apply_hebrew_rules(effective_strings(raw_boss['final_candidate_route'],quote_rules),hebrew_rules);pre_by={x['decision_id']:x for x in pre_route}
 for did in sorted(expected_union):
  p=proposals[did];s=constraints[did];a=adjudicated[did];u=pre_by[did]
  if p['exact_old_deciding_marker_or_seam']!=u['deciding_marker_or_seam'] or p['exact_old_boundary_rationale']!=rationale(u):raise ValueError(f'{did}: prose proposal old-text binding changed')
  if a.get('adjudication')!='accept_literary_proposal_under_source_constraints' or a.get('hold') is not None or a.get('boundary_or_state_change') is not False:raise ValueError(f'{did}: prose boss disposition changed')
  if a.get('span')!=u['span'] or a.get('preserved_literary_form')!=u['literary_form'] or a.get('preserved_confidence')!=u['confidence'] or a.get('preserved_candidate_state')!=u['disposition']:raise ValueError(f'{did}: prose boss changes frozen fields')
  if a.get('final_deciding_marker_or_seam')!=p['proposed_deciding_marker_or_seam'] or a.get('final_boundary_rationale')!=p['proposed_boundary_rationale']:raise ValueError(f'{did}: prose boss no longer adopts the literary proposal exactly')
  if a.get('forbidden_disputed_tokens')!=s.get('forbidden_disputed_tokens') or any(t in a['final_deciding_marker_or_seam']+a['final_boundary_rationale'] for t in a['forbidden_disputed_tokens']):raise ValueError(f'{did}: prose source constraints changed or leaked')
  if re.search(r'[\u0590-\u05ff]',a['final_deciding_marker_or_seam']+a['final_boundary_rationale']):raise ValueError(f'{did}: prose boss reintroduces Hebrew')
 primary_paths={PRIMARY_PROSE_LITERARY:PRIMARY_PROSE_LITERARY_SHA,PRIMARY_PROSE_SOURCE:PRIMARY_PROSE_SOURCE_SHA,PRIMARY_PROSE_BOSS:PRIMARY_PROSE_BOSS_SHA}
 for n,expected in primary_paths.items():
  got=sha(REV/n)
  if got!=expected:raise ValueError(f'Job primary-prose repair mesh evidence changed: {n} {got} != {expected}')
 primary_lit=rj(REV/PRIMARY_PROSE_LITERARY);primary_source=rj(REV/PRIMARY_PROSE_SOURCE);primary_boss=rj(REV/PRIMARY_PROSE_BOSS)
 primary_final=primary_boss.get('final_judgment') or {};primary_compare=primary_boss.get('comparison_result') or {};primary_contract=primary_boss.get('application_contract') or {}
 expected_primary_inputs={PRIMARY_PROSE_LITERARY:PRIMARY_PROSE_LITERARY_SHA,PRIMARY_PROSE_SOURCE:PRIMARY_PROSE_SOURCE_SHA,'blind_primary_hebrew_poetics_v1.json':FROZEN['blind_primary_hebrew_poetics_v1.json'],'decision_evidence_v2.jsonl':'cd78d829925a581a679cb8321160b3212cd02a40cd815e52598e76cf46b83197','review_packets.jsonl':'d8b83924874db3aa7ed0eab8ef0633d6edac61b5413c359aa2c42599344a770b','primary_hebrew_v2.json':'9bcb266569b2a779b274de51674f11eb167adac99c79917cf1911890cd92b745','corrective_specialist_hebrew_textual_v2.json':'9bcb266569b2a779b274de51674f11eb167adac99c79917cf1911890cd92b745'}
 if primary_boss.get('input_hashes')!=expected_primary_inputs:raise ValueError('primary-prose boss input bindings changed')
 if primary_final.get('status')!='pass_no_holds' or primary_final.get('held_decision_ids')!=[] or primary_final.get('overturned_boundary_or_review_ruling_count')!=0:raise ValueError('primary-prose boss did not return exact no-hold pass')
 if primary_compare.get('decision_count')!=14 or primary_compare.get('accepted_repair_count')!=14 or primary_compare.get('held_repair_count')!=0 or primary_compare.get('planned_total_fields')!=120 or primary_compare.get('verdict')!='pass_no_holds' or any(primary_compare.get(k)!=0 for k in ('active_old_core_field_mismatch_count','job062_active_old_derived_field_mismatch_count','forbidden_target_survivor_count','boss_prose_contamination_count')):raise ValueError('primary-prose boss comparison is not zero-defect')
 if primary_contract.get('active_artifacts_modified_by_this_adjudication') is not False or primary_contract.get('frozen_blind_primary_artifact_modified') is not False:raise ValueError('primary-prose application contract changed')
 if (primary_lit.get('validation') or {}).get('pass') is not True or (primary_source.get('preflight') or {}).get('pass') is not True:raise ValueError('primary-prose literary/source docket is not green')
 primary_proposals={x['decision_id']:x for x in primary_lit.get('proposals') or []};primary_constraints={x['decision_id']:x for x in primary_source.get('decisions') or []};raw_primary_rules=primary_boss.get('adjudications') or [];primary_adjudicated={x['decision_id']:x for x in raw_primary_rules}
 if set(primary_proposals)!=expected_union or set(primary_constraints)!=expected_union or set(primary_adjudicated)!=expected_union or any(len(x)!=14 for x in (primary_proposals,primary_constraints,primary_adjudicated)):raise ValueError('primary-prose mesh decision sets changed')
 primary_rules=[]
 for did in sorted(expected_union):
  p=primary_proposals[did];s=primary_constraints[did];a=primary_adjudicated[did];word=a.get('final_effective_primary_deciding_evidence_and_support','')
  if a.get('adjudication')!='accept_source_safe_frozen_blind_primary_restatement' or a.get('hold') is not None or a.get('boundary_or_review_state_change') is not False:raise ValueError(f'{did}: primary-prose boss disposition changed')
  if word!=p.get('proposed_deciding_evidence_and_support') or word!=s.get('safe_source_neutral_effective_primary_wording') or a.get('final_wording_sha256')!=s.get('safe_wording_sha256'):raise ValueError(f'{did}: primary-prose wording diverges across mesh')
  if a.get('boss_prose_used_as_primary_support') is not False or re.search(r'[\u0590-\u05ff]',word) or any(t in word for t in s.get('forbidden_targets') or []):raise ValueError(f'{did}: primary-prose source/provenance guard failed')
  effective=dict(a);effective['_exact_old_deciding_evidence_and_support']=p['exact_old_deciding_evidence_and_support'];primary_rules.append(effective)
 redhash={**evidence_hashes,SOURCE_FINAL:final_sha,SOURCE_BACKUP_FINAL:backup_final_sha,**prose_paths,**primary_paths}
 return redhash,quote_rules,hebrew_rules,prose_rules,primary_rules
def inventory()->tuple[list[str],dict[str,str]]:
 rows=[x for x in rjl(WEB) if str(x.get('osis_ref','')).startswith('Job.')];refs=[x['osis_ref'] for x in rows];texts={x['osis_ref']:x['text'] for x in rows}
 if len(refs)!=1070 or len(set(refs))!=1070 or refs[0]!='Job.1.1' or refs[-1]!='Job.42.17':raise ValueError('bad Job WEB inventory')
 return refs,texts
def units(boss:dict[str,Any],post:dict[str,Any])->list[dict[str,Any]]:
 out=[dict(x) for x in boss['final_candidate_route']];over={x['decision_id']:x for x in post['effective_decision_overrides']}
 for u in out:
  if u['decision_id'] in over:
   x=over[u['decision_id']];u['disposition']=x['effective_disposition'];u['confidence']=x['effective_confidence'];u['hold_question']=x['hold_question']
 if [x['decision_index'] for x in out]!=list(range(1,94)):raise ValueError('Job indices changed')
 if {x['decision_id'] for x in out if x['disposition']=='held_lower_confidence'}!=HELD_IDS:raise ValueError('Job held set changed')
 if Counter(x['confidence'] for x in out)!=Counter({'high':41,'medium':42,'medium_low':10}):raise ValueError('Job confidence changed')
 if Counter(x['disposition'] for x in out)!=Counter({'accepted_candidate':87,'held_lower_confidence':6}):raise ValueError('Job disposition changed')
 return out
def rejected(u:dict[str,Any])->str:
 xs=[]
 for x in u.get('rejected_alternatives_from_all_lanes',[]):
  if str(x.get('alternative','')).strip():xs.append(f"{str(x.get('lane','specialist')).replace('_',' ')} {x.get('proposal_span','alternative')}: {x['alternative']}")
 if not xs:raise ValueError(f"{u['decision_id']}: no rejected alternative")
 return '; '.join(xs[:3])
def rationale(u:dict[str,Any])->str:return str(u.get('_effective_boundary_rationale') or f"{u['deciding_marker_or_seam']} {u['counterevidence']} Alternative: {rejected(u)}")
def lane_position(u:dict[str,Any],lane:str)->dict[str,Any]:
 xs=[x for x in u['lane_evidence_considered'] if x['lane']==lane]
 if not xs:raise ValueError(f"{u['decision_id']}: missing {lane}")
 xs.sort(key=lambda x:(bool(x.get('exact_span_match')),x.get('proposed_disposition')=='accept',x.get('proposal_span')==u['span']),reverse=True);return xs[0]
def hold_parts(u:dict[str,Any],appeals:list[dict[str,Any]])->tuple[str,list[str],str]:
 q=str(u.get('hold_question') or '').strip()
 if '?' not in q or len(q)<30:raise ValueError(f"{u['decision_id']}: bad hold question")
 parent='; '.join(u.get('mandatory_parent_hydration') or [u['span']]);opts=[f"Surface {u['span']} only as the present larger coherent unit, with {parent} retained as context.",f"Permit the disputed child treatment described in the question only after independent review, with mandatory hydration from {parent}."]
 rs=sorted({str(x.get('requested_next_reviewer','')).strip() for x in appeals if x.get('requested_next_reviewer')});return q,opts,';'.join(rs) if rs else 'human_or_external_ai_job_wisdom_poetry_translation_and_retrieval_specialist'
def ledger_plan(packets:list[dict[str,Any]])->tuple[bytes,list[dict[str,Any]]]:
 p=REV/'appeal_ledger.jsonl';before=p.read_bytes()
 if len(before)<PREFIX_BYTES or shab(before[:PREFIX_BYTES])!=PREFIX_SHA or not before[:PREFIX_BYTES].endswith(b'\n') or not before.endswith(b'\n'):raise ValueError('Job ledger prefix/newline invariant failed')
 pairs=[(p0,a) for p0 in packets for a in p0.get('appeals',[])];ids={a['appeal_id'] for _p,a in pairs}
 if ids!=APPEAL_IDS or len(pairs)!=3:raise ValueError(f'Job packet appeals changed: {ids}')
 present={str(x.get('appeal_id','')) for x in rjl(p)}&APPEAL_IDS
 if len(present) not in (0,3):raise ValueError('partial T562 appeal append')
 adds=[] if present else [{**a,'schema_version':'m7_job_boundary_appeal.v2','task_id':'T562','book':'Job','decision_id':p0['decision_id'],'span':p0['span'],'append_only':True,'candidate_only':True,'non_authorizing':True,'forced_consensus':False} for p0,a in pairs]
 return before,adds
def validate_memory(chunks:list[dict[str,Any]],packets:list[dict[str,Any]],refs:list[str],covered:list[str])->dict[str,Any]:
 errors=[]
 if covered!=refs:errors.append('exact ordered coverage')
 if [x['chunk_index_in_book'] for x in chunks]!=list(range(1,94)):errors.append('indices')
 if len({x['decision_id'] for x in chunks})!=93 or {x['decision_id'] for x in chunks}!={x['decision_id'] for x in packets}:errors.append('decision parity')
 attempts=set();challenges=responses=0;rats=set()
 for ch,p in zip(chunks,packets,strict=True):
  if p['chunk_content_sha256']!=rowsha(ch):errors.append(f"{ch['decision_id']} hash")
  if len(p['primary_reviews'])!=3:errors.append(f"{ch['decision_id']} lanes")
  local=[x['reviewer_attempt_id'] for x in p['primary_reviews']]+[p['peer_crosscheck']['reviewer_attempt_id'],p['post_resolution_check']['checker_attempt_id'],p['sol_resolution']['author_attempt_id']]
  if len(local)!=len(set(local)) or attempts&set(local):errors.append(f"{ch['decision_id']} attempt collision")
  attempts.update(local);cs=[c for r0 in p['primary_reviews'] for c in r0['challenges']];rs=p['sol_resolution']['challenge_responses'];challenges+=len(cs);responses+=len(rs)
  if Counter(x['challenge_id'] for x in cs)!=Counter(x['challenge_id'] for x in rs):errors.append(f"{ch['decision_id']} response parity")
  if ch['boundary_rationale'] in rats or len(ch['boundary_rationale'])<80:errors.append(f"{ch['decision_id']} rationale")
  rats.add(ch['boundary_rationale'])
 blob=json.dumps({'chunks':chunks,'packets':packets},ensure_ascii=False)
 if any(x in blob for x in ('\ufffd','\u00c3','\u00e2\u20ac','\u00f0\u0178','??')) or re.search(r'[A-Za-z]\?[A-Za-z]',blob):errors.append('encoding loss')
 if errors:raise ValueError('Job in-memory validation failed: '+' | '.join(errors[:12]))
 verdicts=Counter(r0['verdict'] for p in packets for r0 in p['primary_reviews'])
 if not verdicts['supports'] or not verdicts['challenge']:raise ValueError(f'not genuine verdict mix: {verdicts}')
 return {'coverage_exact_ordered':True,'indices_positive_contiguous':True,'decision_count':93,'primary_review_count':279,'challenge_count':challenges,'response_count':responses,'distinct_workflow_attempt_ids':len(attempts),'verdicts':dict(verdicts),'encoding_loss_patterns':0,'unique_rationales':len(rats)}
def build()->tuple[dict[Path,tuple[str,Any]],dict[str,Any],bytes,list[dict[str,Any]]]:
 redhash,quote_rules,hebrew_rules,prose_rules,primary_rules=verify();boss=effective_strings(rj(BOSS),quote_rules);post=effective_strings(rj(POST),quote_rules);boss['final_candidate_route']=apply_prose_rules(apply_hebrew_rules(boss['final_candidate_route'],hebrew_rules),prose_rules);route=units(boss,post);active={x['appeal_id']:x for x in post['active_appeal_registry']}
 if set(active)!=APPEAL_IDS:raise ValueError('active appeal registry changed')
 bydecision:dict[str,list[dict[str,Any]]]=defaultdict(list)
 for a in active.values():bydecision[str(a['affected_decision_id'])].append(a)
 allrefs,texts=inventory();pos={r:i for i,r in enumerate(allrefs)};coverage=[];chunks=[];stage=[]
 for u in route:
  span=u['span'];a,b=span.split('-');cov=allrefs[pos[a]:pos[b]+1]
  if len(cov)!=u['span_verse_count']:raise ValueError(f"{u['decision_id']}: verse count")
  coverage+=cov;did=u['decision_id'];held=u['disposition']=='held_lower_confidence';apps=bydecision.get(did,[]);q=opts=reviewer=None
  if held:q,opts,reviewer=hold_parts(u,apps)
  parent='; '.join(u.get('mandatory_parent_hydration') or [span]);obs=[{'ref':f'WEB:{cov[0]}','text':texts[cov[0]],'extent':'complete_verse','use':'opening_witness'}]
  if cov[-1]!=cov[0]:obs.append({'ref':f'WEB:{cov[-1]}','text':texts[cov[-1]],'extent':'complete_verse','use':'closing_witness'})
  mapped=mt_span(span);align={'web_span':span,'oshb_span':mapped,'uxlc_span':mapped,'coordinate_system':'MT_WLC','crosswalk_status':'validated_job_web_41_to_mt_40_25_through_41_26_crosswalk' if mapped!=span else 'validated_job_web_mt_same_coordinates','crosswalk_rules':{'WEB_Job.41.1-Job.41.8':'MT_Job.40.25-MT_Job.40.32','WEB_Job.41.9-Job.41.34':'MT_Job.41.1-MT_Job.41.26','other_WEB_coordinates':'same_as_MT'},'source_metadata_boundary_authority':False,'versification_crosswalk_is_evidence_only':True,'wlc_family_correlation_disclosed':True,'oshb_uxlc_are_independent_witnesses':False,'roots_or_etymology_are_not_meaning':True,'variants_select_preferred_reading':False,'speaker_assignment_selected':False,'authority':'translation_textual_order_poetic_and_dialogue_evidence_only'}
  rat=rationale(u);chunk={'model_id':'M7_sol','book':'Job','span':span,'chunk_index_in_book':u['decision_index'],'working_title':u['literary_form'].replace('_',' '),'literature_type_guess':u['literary_form'],'literary_form':u['literary_form'],'parent_literary_form':f"context_hydrated_{u['literary_form']}_parent",'parent_span':parent,'boundary_evidence_refs':[f'direct_read:eng-web:{span}',f'direct_read:oshb:{span}',f'direct_read:uxlc:{span}','book_strategy/Job.md','reviews/Job/decision_evidence_v2.jsonl','reviews/Job/decision_relations.jsonl'],'strong_or_hebrew_tags_used':['direct_Biblical_Hebrew_poetic_dialogue_form_considered','Job_WEB_41_to_MT_40_25_through_41_26_crosswalk_evidence_only','roots_are_not_meaning','OSHB_and_UXLC_are_correlated_WLC_family_views','speaker_and_later_canonical_reuse_are_not_boundary_authority'],'wj_or_red_letter_considered':False,'frontier_flag_considered':True,'confidence':u['confidence'],'decision_id':did,'deciding_marker_or_seam':u['deciding_marker_or_seam'],'boundary_rationale':rat,'rejected_alternative':rejected(u),'counterevidence':u['counterevidence'],'defensible_basis':u['deciding_marker_or_seam']+' '+u['counterevidence'],'confidence_basis':{'tier':u['confidence'],'rationale':u['deciding_marker_or_seam'],'alternative_strength':u['counterevidence'],'status_not_used_as_input':True},'review_revision':'m7-corrective-rereview-v2','review_status':'final_deferred_appeal' if held and apps else 'final_deferred_review' if held else 'candidate_review_complete','review_holds':[q] if held else [],'candidate_hold_state':'deferred_human_or_external_ai' if held else None,'candidate_hold_basis':{'kind':'speaker_form_or_retrieval_boundary_dispute','question':q.split('?',1)[0].strip()+'?','options':opts,'mandatory_parent':parent} if held else None,'human_review_question':q if held else None,'human_review_route':reviewer if held else None,'candidate_internal_seams':[x['proposal_span'] for x in u.get('rejected_alternatives_from_all_lanes',[]) if x.get('proposal_span')!=span],'non_authorizing':True,'candidate_only':True,'working_title_is_boundary_authority':False,'original_language_translation_holds':['Hebrew syntax, poetic parallelism, section markers, text-critical or translation ambiguity, Job 41 versification, and speaker uncertainty remain evidence-only; no root, lemma, rendering, preferred reading, or speaker assignment decides the boundary.'],'cross_reference_holds':[u.get('canonical_internal_relation_evidence',{}).get('guard','Canonical reuse is evidence only and creates no authority.')],'red_team_premortem_holds':[u['counterevidence']],'convergence_defense':{'literary_form':u['literary_form'],'deciding_marker_or_seam':u['deciding_marker_or_seam'],'rejected_alternative':rejected(u),'confidence':u['confidence'],'defensible_basis':u['deciding_marker_or_seam']+' '+u['counterevidence'],'parent_span':parent,'source_observations':obs,'original_language_alignment':align}}
  if did in {'M7_sol-Job-090','M7_sol-Job-093'}:chunk['apparatus_nonselection_guard']='Preserve serialized alternatives; select no ketiv, qere, pointing, witness, or reading.'
  chunks.append(chunk);stage.append((u,chunk,srefs(span,did)))
 if coverage!=allrefs:raise ValueError('Job exact coverage failed')
 primary_by={x['decision_id']:x for x in primary_rules}
 roles={c:[] for c,*_ in ROLES};packets=[];evidence=[];peers=[];authors=[];bossrows=[]
 for u,ch,refs in stage:
  did=ch['decision_id'];n=ch['chunk_index_in_book'];held=ch['candidate_hold_state'] is not None;reviews=[];cids=[]
  for code,lane,role,fname in ROLES:
   x=lane_position(u,lane)
   if code=='hebrew' and did in primary_by:
    pr=primary_by[did];preserved=pr['preserved_primary_identity_and_substance'];old=x['deciding_evidence']
    if old!=pr['_exact_old_deciding_evidence_and_support'] or x.get('proposal_span')!=preserved['proposal_span'] or x.get('proposed_literary_form')!=preserved['literary_form'] or x.get('proposed_disposition')!=preserved['proposed_disposition'] or x.get('proposed_confidence')!=preserved['proposed_confidence'] or x.get('counterevidence')!=preserved['counterevidence']:raise ValueError(f'{did}: frozen Hebrew primary identity or substance changed before repair')
    x=dict(x);x['deciding_evidence']=pr['final_effective_primary_deciding_evidence_and_support'];x['effective_prose_correction_overlay']={'base_frozen_primary_artifact':preserved['frozen_blind_proposal'],'base_frozen_primary_sha256':preserved['frozen_blind_proposal_sha256'],'frozen_blind_primary_decision_id':pr['frozen_blind_primary_decision_id'],'frozen_blind_primary_reviewer_attempt_id':pr['frozen_blind_primary_reviewer_attempt_id'],'primary_source_constraints_sha256':PRIMARY_PROSE_SOURCE_SHA,'effective_wording_is_original_blind_wording':False,'boss_prose_used_as_primary_support':False,'frozen_blind_primary_artifact_modified':False,'candidate_only':True,'non_authorizing':True}
   challenge=not(x.get('exact_span_match') is True and x.get('proposed_disposition')=='accept');supports=not challenge or (did=='M7_sol-Job-030' and code=='hebrew' and str(x.get('proposal_span','')).endswith('Job.13.19'));chs=[]
   if challenge:
    cid=f'{did}-{code.upper()}-CHALLENGE-01';cids.append(cid);ps=x['proposal_span'];chs=[{'challenge_id':cid,'claim':f"{lane.replace('_',' ')} proposed {ps} against the effective {u['span']}: {x['deciding_evidence']}",'proposed_remedy':f"{x['deciding_evidence']} {x['counterevidence']} ({ps})",'counterevidence':u['counterevidence'],'source_refs':refs}]
   rr={'reviewer_attempt_id':f'job-v2-{code}-{n:03d}-blind-specialist-high','reviewer_role':role,'role':role,'verdict':'supports' if supports else 'challenge','blind_to_other_primary_reviews':True,'evidence_only':True,'primary_evidence_provenance':'frozen_blind_lane_position_only','frozen_blind_proposal':f'reviews/Job/{fname}','frozen_blind_proposal_sha256':FROZEN[fname],'recorded_position':x,'evidence_refs':refs,'source_refs':refs,'support':x['deciding_evidence'],'support_scope':'closing_boundary_at_Job.13.19_with_start_boundary_dissent_preserved' if did=='M7_sol-Job-030' and code=='hebrew' else 'full_effective_span' if not challenge else 'lane_evidence_only','counterevidence':x['counterevidence'],'challenges':chs};reviews.append(rr);roles[code].append(rr)
  apps=sorted(bydecision.get(did,[]),key=lambda x:x['appeal_id']);q=opts=reviewer=None
  if held:q,opts,reviewer=hold_parts(u,apps)
  responses=[{'challenge_id':cid,'disposition':'held_for_human_or_external_ai_resolution' if held else 'boss_retains_candidate_with_dissent_preserved','rationale':ch['boundary_rationale'],'rejected_alternative':ch['rejected_alternative']} for cid in cids]
  peer={'reviewer_attempt_id':f'job-v2-peer-{n:03d}-crosscheck-high','reviewer_role':'adversarial_job_dialogue_and_retrieval_crosscheck','status':'pass_with_hold' if held else 'pass','disputed_claim_ids':cids,'rationale':ch['deciding_marker_or_seam'],'counterevidence':ch['counterevidence'],'source_refs':refs,'support_challenge_mix':{'support_count':sum(x['verdict']=='supports' for x in reviews),'challenge_count':sum(x['verdict']=='challenge' for x in reviews)}}
  resolution={'author_id':'M7_sol','author_attempt_id':f'job-v2-boss-{n:03d}-sol-high','challenge_responses':responses,'unresolved_claim_ids':[f'{did}-EFFECTIVE-HOLD-01'] if held else [],'rationale':ch['boundary_rationale'],'counterevidence':ch['counterevidence'],'rejected_alternative':ch['rejected_alternative'],'outcome':'held_lower_confidence_for_independent_review' if held else 'accepted_candidate_after_role_specific_review','authority':'candidate_author_only'}
  cr=[{'challenge_id':x['challenge_id'],'ruling':x['disposition'],'rationale':x['rationale'],'rejected_alternative':x['rejected_alternative'],'forced_consensus':False} for x in responses];br={'ruling_id':resolution['author_attempt_id'],'frozen_boss_attempt_id':u['boss_attempt_id'],'rationale':ch['boundary_rationale'],'counterevidence':ch['counterevidence'],'rejected_alternative':ch['rejected_alternative'],'outcome':'hold_candidate' if held else 'accept_candidate','challenge_rulings':cr,'appeal_effect':f'{len(apps)} open append-only appeal(s)' if apps else 'specific hold without specialist appeal' if held else 'dissent preserved without active appeal','forced_consensus':False};h=rowsha(ch)
  packet={'schema_version':'m7_corrective_review_packet.v2','decision_id':did,'book':'Job','span':ch['span'],'chunk_sha256':h,'chunk_content_sha256':h,'review_revision':'m7-corrective-rereview-v2','primary_reviews':reviews,'peer_crosscheck':peer,'sol_resolution':resolution,'appeals':apps,'final_state':'held_lower_confidence' if held else 'accepted_candidate','human_review_question':q if held else None,'human_review_route':reviewer if held else None,'post_resolution_check':{'checker_attempt_id':f'job-v2-post-{n:03d}-role-separated-checker','status':'hold' if held else 'pass','evidence_refs':['reviews/Job/post_resolution_check_v2.json'],'chunk_content_sha256':h},'independence_scope':INDEP,'non_authorizing':True,'boss_ruling':br}
  packets.append(packet);peers.append({'decision_id':did,**peer});bossrows.append({'decision_id':did,**br});authors.append({'decision_id':did,'author_attempt_id':resolution['author_attempt_id'],'challenge_responses':responses,'all_challenges_answered_exactly_once':True,'candidate_only':True,'non_authorizing':True});evidence.append({'schema_version':'m7_job_decision_evidence.v2','book':'Job','decision_id':did,'span':ch['span'],'literary_form':ch['literary_form'],'parent_literary_form':ch['parent_literary_form'],'parent_span':ch['parent_span'],'candidate_state':packet['final_state'],'confidence':ch['confidence'],'confidence_basis':ch['confidence_basis'],'deciding_marker_or_seam':ch['deciding_marker_or_seam'],'boundary_rationale':ch['boundary_rationale'],'rejected_alternative':ch['rejected_alternative'],'defensible_basis':ch['defensible_basis'],'source_observations':ch['convergence_defense']['source_observations'],'original_language_alignment':ch['convergence_defense']['original_language_alignment'],'hold_question':q if held else None,'appeals':apps,'primary_reviews':reviews,'non_authorizing':True})
 relations=[]
 for u in route:
  parents=u.get('mandatory_parent_hydration') or []
  if parents:relations.append({'schema_version':'m7_decision_relation.v2','note_id':f"T562-JOB-PARENT-{u['decision_index']:03d}",'book':'Job','relation_type':'mandatory_dialogue_cycle_or_speech_parent_hydration','children':[u['decision_id']],'parent_surfaces':parents,'rationale':u['counterevidence'],'mandatory_hydration':True,'boundary_authority':False,'non_authorizing':True})
 for x in boss['preserved_material_losing_routes']:relations.append({'schema_version':'m7_decision_relation.v2','note_id':x['dissent_id'],'book':'Job','relation_type':x['relation_type'],'children':x['affected_final_decision_ids'],'losing_span':x['losing_span'],'literary_form':x['literary_form'],'rationale':x['deciding_evidence'],'counterevidence':x['counterevidence'],'appellant_role':x['lane'],'appellant_attempt_id':x['reviewer_attempt_id'],'status':x['status'],'forced_consensus':False,'boundary_authority':False,'non_authorizing':True})
 for x in active.values():relations.append({'schema_version':'m7_decision_relation.v2','note_id':x['appeal_id'],'book':'Job','relation_type':'active_post_ruling_appeal_against_boss_treatment','children':[x['affected_decision_id']],'question':next(u['hold_question'] for u in route if u['decision_id']==x['affected_decision_id']),'rationale':x['rationale'],'counterevidence':x['uncertainty'],'requested_treatment':x['requested_treatment'],'status':x['status'],'forced_consensus':False,'boundary_authority':False,'non_authorizing':True})
 for u in route:
  if u['decision_id'] in HELD_IDS:relations.append({'schema_version':'m7_decision_relation.v2','note_id':f"T562-JOB-EFFECTIVE-HOLD-{u['decision_index']:03d}",'book':'Job','relation_type':'effective_human_or_external_ai_hold','children':[u['decision_id']],'question':u['hold_question'],'rationale':u['counterevidence'],'status':'deferred_human_or_external_ai','forced_consensus':False,'boundary_authority':False,'non_authorizing':True})
 checks=validate_memory(chunks,packets,allrefs,coverage);mix={c:dict(Counter(x['verdict'] for x in roles[c])) for c,*_ in ROLES};rolearts={}
 lane_for={'hebrew':'hebrew_poetics','literary':'wisdom_literary','canonical':'canonical_retrieval'}
 for code,_lane,role,fname in ROLES:
  aids=sorted(x['appeal_id'] for x in active.values() if x['specialist_lane']==lane_for[code]);rolearts[code]={'schema_version':'m7_job_role_artifact.v2','book':'Job','role':role,'decision_local_review_count':93,'reviews':roles[code],'blind_primary_artifact':f'reviews/Job/{fname}','blind_primary_artifact_sha256':FROZEN[fname],'blind_primary_artifacts_remain_frozen':True,'post_ruling_active_appeals':len(aids),'active_appeal_ids':aids,'candidate_only':True,'non_authorizing':True}
 artifacts={CHUNKS:('jsonl',chunks),REV/'review_packets.jsonl':('jsonl',packets),REV/'decision_evidence_v2.jsonl':('jsonl',evidence),REV/'decision_relations.jsonl':('jsonl',relations),REV/'primary_hebrew_v2.json':('json',rolearts['hebrew']),REV/'corrective_specialist_hebrew_textual_v2.json':('json',rolearts['hebrew']),REV/'primary_literary_v2.json':('json',rolearts['literary']),REV/'corrective_specialist_literary_v2.json':('json',rolearts['literary']),REV/'canonical_premortem_v2.json':('json',rolearts['canonical']),REV/'corrective_specialist_canonical_premortem_v2.json':('json',rolearts['canonical']),REV/'peer_crosscheck_v2.json':('json',{'schema_version':'m7_job_peer_crosscheck.v2','book':'Job','reviews':peers,'candidate_only':True,'non_authorizing':True}),REV/'author_responses_v2.json':('json',{'schema_version':'m7_job_author_responses.v2','book':'Job','responses':authors,'challenge_count':checks['challenge_count'],'all_challenges_answered_exactly_once':True,'candidate_only':True,'non_authorizing':True}),REV/'boss_ruling_v2.json':('json',{'schema_version':'m7_job_boss_ruling.v2','task_id':'T562','book':'Job','route_count':93,'accepted':87,'held':6,'confidence':{'high':41,'medium':42,'medium_low':10},'boss_attempt_id':boss['artifact_id'],'frozen_boss_adjudication_sha256':FROZEN['fresh_boss_adjudication_v1.json'],'post_appeal_overlay_sha256':FROZEN['post_appeal_boss_ruling_v1.json'],'rulings':bossrows,'challenge_ruling_count':checks['challenge_count'],'specialist_post_ruling_active_appeals':3,'forced_consensus':False,'candidate_only':True,'non_authorizing':True}),REV/'mesh_instruction_and_dissent_v2.json':('json',{'schema_version':'m7_job_mesh_instruction_record.v2','task_id':'T562','roles':[x[2] for x in ROLES]+['boss_adjudicator','role_separated_post_resolution_checker'],'instructions':['blind read-only primaries','original-language and canonical relations are evidence only','retain the larger coherent unit under tied evidence','boss answers every challenge without forcing consensus','every specialist receives a post-ruling appeal opportunity','specific unresolved seams route to human or external AI'],'pre_materialization_redteam_bindings':redhash,'active_appeal_ids':sorted(APPEAL_IDS),'candidate_only':True,'non_authorizing':True})}
 def data(p:Path)->bytes:
  kind,x=artifacts[p];return jlb(x) if kind=='jsonl' else jb(x,True)
 for target,(kind,value) in artifacts.items():assert_no_bad_tokens(value,quote_rules,str(target));assert_no_hebrew_targets(value,hebrew_rules,str(target))
 postcheck={'schema_version':'m7_post_resolution_check.v2','checker_attempt_id':'T562-Job-role-separated-materialized-binding-check-v2','role':'fresh_role_separated_post_resolution_binding_checker','book':'Job','status':'pass_with_holds','checked_decision_ids':[x['decision_id'] for x in chunks],'checker_attempt_ids':[f'job-v2-post-{n:03d}-role-separated-checker' for n in range(1,94)],'checked_review_packets_sha256':shab(data(REV/'review_packets.jsonl')),'checked_chunks_sha256':shab(data(CHUNKS)),'checked_decision_relations_sha256':shab(data(REV/'decision_relations.jsonl')),'role_separated_checker_verdict_received':True,'independent_model_verdict_received':False,'coverage':{'expected':1070,'observed':len(coverage),'exact_ordered':coverage==allrefs},'accepted':87,'held':6,'pre_materialization_redteam_bindings':redhash,'in_memory_checks':checks,'candidate_only':True,'non_authorizing':True};artifacts[REV/'post_resolution_check_v2.json']=('json',postcheck)
 assert_no_bad_tokens(postcheck,quote_rules,'post_resolution_check_v2.json');assert_no_hebrew_targets(postcheck,hebrew_rules,'post_resolution_check_v2.json')
 before,adds=ledger_plan(packets)
 assert_no_bad_tokens(adds,quote_rules,'appeal_ledger_additions');assert_no_hebrew_targets(adds,hebrew_rules,'appeal_ledger_additions')
 summary={'book':'Job','chunks':93,'coverage':1070,'accepted':87,'held':6,'confidence':{'high':41,'medium':42,'medium_low':10},'primary_reviews':279,'role_verdict_mix':mix,'challenge_count':checks['challenge_count'],'author_response_count':checks['response_count'],'active_appeals':3,'relations':len(relations),'appeal_ledger_bytes_before':len(before),'appeal_ledger_rows_planned':len(adds),'in_memory_validation':'pass','in_memory_checks':checks,'redteam_hashes':redhash,'planned_hashes':{'chunks':shab(data(CHUNKS)),'packets':shab(data(REV/'review_packets.jsonl')),'evidence':shab(data(REV/'decision_evidence_v2.jsonl')),'relations':shab(data(REV/'decision_relations.jsonl')),'boss':shab(data(REV/'boss_ruling_v2.json')),'post_resolution':shab(jb(postcheck,True))}}
 return artifacts,summary,before,adds
def materialize(dry:bool)->dict[str,Any]:
 arts,summary,before,adds=build()
 if dry:return {'dry_run':True,'writes':0,**summary}
 for p,(kind,x) in arts.items():wjl(p,x) if kind=='jsonl' else wj(p,x)
 if adds:
  with (REV/'appeal_ledger.jsonl').open('ab') as h:h.write(jlb(adds))
 after=(REV/'appeal_ledger.jsonl').read_bytes()
 if not after.startswith(before) or shab(after[:PREFIX_BYTES])!=PREFIX_SHA:raise ValueError('Job ledger append invariant failed')
 return {'dry_run':False,'writes':len(arts)+(1 if adds else 0),**summary,'appeal_ledger_rows_appended':len(adds),'hashes':{'chunks':sha(CHUNKS),'packets':sha(REV/'review_packets.jsonl'),'evidence':sha(REV/'decision_evidence_v2.jsonl'),'relations':sha(REV/'decision_relations.jsonl'),'boss':sha(REV/'boss_ruling_v2.json'),'post_resolution':sha(REV/'post_resolution_check_v2.json'),'appeal_ledger':sha(REV/'appeal_ledger.jsonl')}}
def main()->int:
 ap=argparse.ArgumentParser();ap.add_argument('--dry-run',action='store_true');a=ap.parse_args();print(json.dumps(materialize(a.dry_run),ensure_ascii=False,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())