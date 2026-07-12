import importlib.util
from pathlib import Path
import pytest,yaml
ROOT=Path(__file__).resolve().parent.parent;SCRIPT=ROOT/'scripts/validate_t495_doctrine_genealogy_governance_handoff.py';CONTROL=ROOT/'.ai/control/t495_doctrine_genealogy_governance_handoff.yaml'
def mod():s=importlib.util.spec_from_file_location('v',SCRIPT);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def data():return yaml.safe_load(CONTROL.read_text(encoding='utf-8'))
def test_current():assert mod().main()==0
def test_no_repo_creation():
 d=data();d['authority']['repository_creation_authorized']=True
 with pytest.raises(SystemExit):mod().validate(d)
def test_no_scripture_write():
 d=data();d['cross_repo_flows']['genealogy_to_scripture_graph']='write'
 with pytest.raises(SystemExit):mod().validate(d)
def test_questions_unresolved():
 d=data();d['unresolved_questions'][0]['status']='selected'
 with pytest.raises(SystemExit):mod().validate(d)
