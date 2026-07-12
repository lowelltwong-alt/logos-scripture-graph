import importlib.util
from pathlib import Path
import pytest,yaml
ROOT=Path(__file__).resolve().parent.parent; SCRIPT=ROOT/'scripts/validate_t494_theological_edge_taxonomy_research.py'; CONTROL=ROOT/'.ai/control/t494_theological_edge_taxonomy_research.yaml'
def mod():
 s=importlib.util.spec_from_file_location('v',SCRIPT);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def data(): return yaml.safe_load(CONTROL.read_text(encoding='utf-8'))
def test_current(): assert mod().main()==0
def test_no_edges():
 d=data();d['authority']['creates_candidate_or_canonical_edges']=True
 with pytest.raises(SystemExit):mod().validate(d)
def test_not_predicates():
 d=data();d['research_record_contract']['explicitly_not_predicate_schema']=False
 with pytest.raises(SystemExit):mod().validate(d)
def test_questions_unresolved():
 d=data();d['unresolved_questions'][0]['status']='selected'
 with pytest.raises(SystemExit):mod().validate(d)
