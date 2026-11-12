"""Verify saved UI with optional model packages blocked; no downloads or inference."""
import importlib.abc,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
APPLICATION=ROOT/'demo/application'
sys.path.insert(0,str(APPLICATION))
OPTIONAL={'torch','transformers','sentence_transformers','accelerate','datasets','peft','huggingface_hub','tokenizers'}
class BlockOptional(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in OPTIONAL:raise ModuleNotFoundError('Saved-profile test intentionally excludes '+fullname)
sys.meta_path.insert(0,BlockOptional())
from streamlit.testing.v1 import AppTest
app=AppTest.from_file(str(APPLICATION/'demo/app.py'),default_timeout=45).run()
checked=[]
for workspace in ['Start Here','Compare Methods','How the Algorithms Work','Live Lab']:
 next(r for r in app.sidebar.radio if r.label=='Workspace Navigation').set_value(workspace).run()
 assert not app.exception,[x.message for x in app.exception]
 assert not any('Primary research artifact verification failed' in e.value for e in app.error)
 checked.append(workspace)
assert not (OPTIONAL & set(sys.modules))
print(json.dumps(dict(status='PASSED',workspaces=checked,optional_model_packages_loaded=False),indent=2))
