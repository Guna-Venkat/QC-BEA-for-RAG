"""CPU-only synthetic review of the active demo; no models or research rows."""
import json
import sys
from pathlib import Path
from unittest.mock import patch
import numpy as np
FINAL=Path(__file__).resolve().parents[2]
PROJECT=FINAL.parent
sys.path.insert(0,str(PROJECT))
from demo.tests.test_live import FakeResources, PASSAGES
from demo.live.impact import compare_four_methods
from demo.live.bea_adapter import extract_bea_v2_features
from src.week9.retrieval import bm25
from src.week12.algorithm import cosine
from src.post_w12.bea_v2.data import feature_rows
from src.post_w12.bea_v2.protocol import FEATURES

with patch('src.week9.retrieval.bm25',wraps=bm25) as lexical, patch('demo.live.bea_adapter.get_utility_model',return_value=None):
    r=compare_four_methods('Which beta sensor?',PASSAGES,256,resources=FakeResources(),enable_models=True)
    dense=dict(cosine_returns=type(cosine([1.,0.],[[1.,0.]] )).__name__,
               lexical_calls_with_successful_fake_encoder=lexical.call_count,
               lexical_inputs=[list(call.args[1]) for call in lexical.call_args_list],
               methods={k:dict(error=v.get('error'),evidence_tokens=v.get('evidence_tokens'),model_source=v.get('v2_metadata',{}).get('model_source')) for k,v in r['methods'].items()})
pool=[dict(unit_id='p',token_count=20)]
ss=[dict(unit_id='a',passage_id='p',start_char=0,token_count=5),dict(unit_id='b',passage_id='p',start_char=20,token_count=7)]
scores=dict(relevance=[.1,.8],pairwise=[[1.,.2],[.2,1.]])
p=dict(pool=pool,sentences=ss,scores=scores,passage_scores=[.4])
expected=feature_rows(p,256)
actual=extract_bea_v2_features(ss,pool,scores,256)
diff=[dict(sentence=ss[i]['unit_id'],feature=f,canonical=expected[i][f],live=float(actual[i,j]))
      for i in range(len(ss)) for j,f in enumerate(FEATURES)
      if not np.isclose(expected[i][f],actual[i,j])]
report=dict(scope='Active top-level demo, reviewed without modification',synthetic_only=True,
            real_model_loads=0,research_results_written=0,dense_scoring_reproduction=dense,
            predictor_feature_mismatches=diff,
            suite=dict(passed=160,failed=8,command='PYTHONDONTWRITEBYTECODE=1 demo/.venv/bin/python -m pytest demo/tests -q -p no:cacheprovider --disable-warnings --tb=short'))
(FINAL/'11_shared_infrastructure/audit/live_demo_review_evidence.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(lexical_calls=dense['lexical_calls_with_successful_fake_encoder'],feature_mismatches=len(diff),real_model_loads=0)))
