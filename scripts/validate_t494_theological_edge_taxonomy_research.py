#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parent.parent
CONTROL=ROOT/'.ai/control/t494_theological_edge_taxonomy_research.yaml'
ROADMAP=ROOT/'docs/roadmap/T494_THEOLOGICAL_EDGE_TAXONOMY_RESEARCH.md'
FAMILIES={'canonical_argument_grounding','christological_motif_correspondence','covenant_development_correspondence','pneumatological_motif_correspondence','ecclesial_and_sacramental_pressure','soteriological_argument_pressure','eschatological_and_apocalyptic_correspondence','lexical_phrase_context_correspondence'}
def fail(m): print(f'FAIL: {m}',file=sys.stderr); raise SystemExit(1)
def validate(d):
    if d.get('task_id')!='T494' or d.get('research_only') is not True or d.get('non_authorizing') is not True: fail('research-only contract required')
    a=d.get('authority',{})
    for k in ('expands_predicate_registry','creates_candidate_or_canonical_edges','creates_graph_retrieval_vector_or_index_truth','selects_doctrine_reading_tradition_or_canon'):
        if a.get(k) is not False: fail(f'authority.{k} must be false')
    c=d.get('research_record_contract',{})
    if c.get('explicitly_not_predicate_schema') is not True or len(c.get('required_fields',[]))<10: fail('research record contract incomplete')
    if {x.get('research_family_id') for x in d.get('research_families',[])}!=FAMILIES: fail('research families incomplete')
    if len(d.get('review_ladder',[]))!=5: fail('review ladder incomplete')
    for q in d.get('unresolved_questions',[]):
        if q.get('status')!='unresolved' or q.get('owner_needed') is not True: fail('questions must remain unresolved')
def main():
    d=yaml.safe_load(CONTROL.read_text(encoding='utf-8')); validate(d)
    t=ROADMAP.read_text(encoding='utf-8').lower()
    for p in ('research families, not predicates or graph edges','unresolved questions remain questions','no candidate rows'):
        if p not in t: fail(f'roadmap missing {p}')
    print('T494 theological edge taxonomy research OK'); return 0
if __name__=='__main__': raise SystemExit(main())
