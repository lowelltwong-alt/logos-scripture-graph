#!/usr/bin/env python3
from pathlib import Path
import sys,yaml
ROOT=Path(__file__).resolve().parent.parent; CONTROL=ROOT/'.ai/control/t495_doctrine_genealogy_governance_handoff.yaml'; ROADMAP=ROOT/'docs/roadmap/T495_DOCTRINE_GENEALOGY_GOVERNANCE_HANDOFF.md'
CLASSES={'person_influenced_person','work_cites_or_responds_to_work','doctrine_development_event','denominational_adoption_or_rejection','reception_of_scripture_passage'}
def fail(m): print(f'FAIL: {m}',file=sys.stderr);raise SystemExit(1)
def validate(d):
 if d.get('task_id')!='T495' or d.get('planning_only') is not True or d.get('non_authorizing') is not True:fail('planning-only required')
 a=d.get('authority',{})
 if a.get('repository_creation_authorized') is not False or a.get('records_edges_indexes_or_runtime_authorized') is not False:fail('implementation authority forbidden')
 if len(d.get('registration_prerequisites',[]))<9:fail('registration prerequisites incomplete')
 if {x.get('claim_class') for x in d.get('future_claim_classes',[])}!=CLASSES:fail('claim classes incomplete')
 if d.get('cross_repo_flows',{}).get('genealogy_to_scripture_graph')!='no_write_or_promotion_path':fail('Scripture write path forbidden')
 for q in d.get('unresolved_questions',[]):
  if q.get('status')!='unresolved' or q.get('owner_needed') is not True:fail('questions unresolved')
def main():
 d=yaml.safe_load(CONTROL.read_text(encoding='utf-8'));validate(d);t=ROADMAP.read_text(encoding='utf-8').lower()
 for p in ('does not create the repository','chronology or similarity alone can never prove influence','unresolved questions remain questions'):
  if p not in t:fail(f'missing {p}')
 print('T495 doctrine genealogy governance handoff OK');return 0
if __name__=='__main__':raise SystemExit(main())
