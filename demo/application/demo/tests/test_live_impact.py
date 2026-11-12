"""Scientific-contract regressions; no weights, downloads or experiment writes."""
import copy
import re
import threading
import numpy as np
import pytest
from src.week12.reader import prompt_ids, parse_label
from src.week12.protocol import digest
from src.week12.algorithm import serialize
from demo.live.impact import (score_answer, classify_loo_effect, compare_four_methods,
    analyze_evidence_impact, rescore_existing_impact, comparison_input_id)
from demo.live.inference import generate
from demo.live.bea_adapter import extract_bea_v2_features, get_utility_model, V1_PARAMETERS
from demo.tests.test_live import CharTokenizer

PASSAGES=['The fictional vessel Aurora17 was painted violet.',
          'Aurora17 was assembled at an invented northern station.']
QUERY='What color was the fictional vessel Aurora17?'

class Resources:
    def __init__(self):
        self.tok=CharTokenizer();self.lock=threading.RLock();self.device='cpu';self.calls=[];self.embeds=[]
        self.fail=False;self.answer_override=None;self.fail_embed=False
        self.cfg=dict(models=dict(Qwen=dict(id='TEST_READER',revision='r1'),SFR=dict(id='TEST_ENCODER',revision='r1')),
            labels=['SUPPORT','REFUTE','NOT_ENOUGH_INFO'],seed=42,generation=dict(max_new_tokens_qa=128,max_new_tokens_verification=16))
    def tokenizer(self):return self.tok
    def inference_identity(self):return dict(copy.deepcopy(self.cfg),device=self.device,template='test-template-v1')
    def embed(self,texts,role):
        self.embeds.append((texts,role))
        if self.fail_embed:raise RuntimeError('synthetic encoder failure')
        return np.asarray([[1.,float('painted' in t),float('station' in t)] for t in texts])
    def generate(self,q,sel,task_type='freeform_qa'):
        ids=prompt_ids(self.tok,q,task_type,sel['evidence_ids'],self.cfg['labels'])
        self.calls.append(dict(question=q,selection=copy.deepcopy(sel),task=task_type,ids=ids))
        if self.fail:raise RuntimeError('synthetic reader failure')
        answer=self.answer_override
        if answer is None:
            answer='violet' if 'painted violet' in sel['text'] else 'UNKNOWN'
        raw=answer
        if task_type=='verification':answer=parse_label(answer)
        return dict(prediction=answer,raw_prediction=raw,prompt_hash=digest(ids),prompt_tokens=len(ids),generated_tokens=3)

@pytest.fixture
def res():return Resources()

def compare(res,ref='violet',cache=None,task='qa',passages=None):
    return compare_four_methods(QUERY,passages or PASSAGES,256,task,ref,res,True,cache=cache)

def loo(c,res,ref='violet',n=1,cache=None):
    return analyze_evidence_impact(c,ref,n,res,True,cache)

def row(a):return a['impact_by_method']['FIXED_SENTENCE']['units_analyzed'][0]

def test_qa_and_strict_verification():
    assert score_answer('violet','violet')['score']==1
    assert score_answer('Based on evidence: SUPPORT','SUPPORT','verification')['score']==0
    assert score_answer('I do not SUPPORT this claim','SUPPORT','verification')['predicted_label']=='INVALID_OUTPUT'
    assert score_answer('garbled','NOT_ENOUGH_INFO','verification')['score']==0
    assert score_answer('NOT_ENOUGH_INFO','NOT_ENOUGH_INFO','verification')['score']==1
    assert score_answer(None,'violet')['score'] is None
    with pytest.raises(ValueError):score_answer('SUPPORT','wrong','verification')

@pytest.mark.parametrize('delta,effect',[(-.014,'HELPFUL'),(.014,'HARMFUL'),(-.01,'NO_MEASURABLE_CHANGE'),(.01,'NO_MEASURABLE_CHANGE'),(None,'UNAVAILABLE')])
def test_thresholds(delta,effect):assert classify_loo_effect(delta)[0]==effect

def test_canonical_methods_and_no_lexical_substitution(res,monkeypatch):
    import src.week9.retrieval
    monkeypatch.setattr(src.week9.retrieval,'bm25',lambda *a,**k:pytest.fail('BM25 substitution'))
    c=compare(res)
    for m in ['FIXED_SENTENCE','QBGF','BEA_V1']:
        assert c['methods'][m]['status']=='COMPLETE'
        assert c['methods'][m]['evidence_tokens']<=256
        assert c['methods'][m]['receipt']['prompt_ids']
    assert c['methods']['BEA_V1']['execution_metadata']['execution_contract']['parameters']==V1_PARAMETERS
    assert c['methods']['BEA_V2']['status']=='COMPLETE'
    assert c['methods']['BEA_V2']['execution_metadata']['threshold']==8e-5
    assert len(get_utility_model()['bundles'])==15


def test_failed_sfr_disables_methods(res):
    res.fail_embed=True;c=compare(res)
    assert all(x['status']=='UNAVAILABLE' for x in c['methods'].values())
    assert not res.calls


def test_models_off_never_fakes_algorithms(res):
    c=compare_four_methods(QUERY,PASSAGES,256,resources=res,enable_models=False)
    assert all(x['status']=='UNAVAILABLE' for x in c['methods'].values()) and not res.embeds


def test_exact_canonical_features():
    from src.post_w12.bea_v2.data import feature_rows
    from src.post_w12.bea_v2.protocol import FEATURES
    pool=[dict(unit_id='P',token_count=30)]
    ss=[dict(unit_id='A',passage_id='P',start_char=0,token_count=10),dict(unit_id='B',passage_id='P',start_char=20,token_count=10)]
    scores=dict(relevance=[.1,.9],pairwise=[[1.,.2],[.2,1.]])
    expected=feature_rows(dict(pool=pool,sentences=ss,scores=scores,passage_scores=[.4]),256)
    actual=extract_bea_v2_features(ss,pool,scores,256,[.4])
    np.testing.assert_array_equal(actual,[[r[f] for f in FEATURES] for r in expected])


def test_deletion_is_exact_source_order_no_refill(res,monkeypatch):
    c=compare(res);original=copy.deepcopy(c);units=c['methods']['FIXED_SENTENCE']['units']
    import src.week12.algorithm
    monkeypatch.setattr(src.week12.algorithm,'choose',lambda *a,**k:pytest.fail('allocation during LOO'))
    a=loo(c,res,n=2)
    assert c==original
    for u in a['impact_by_method']['FIXED_SENTENCE']['units_analyzed']:
        assert [x['unit_id'] for x in u['remaining_units']]==[x['unit_id'] for x in units if x['unit_id']!=u['unit_id']]
        assert len(u['remaining_units'])==len(units)-1
        assert u['receipt']['evidence_tokens']==u['remaining_tokens']
        assert u['original_receipt']['request_id']!=u['receipt']['request_id']
        assert 'violet' not in res.tok.decode(u['receipt']['prompt_ids']) if 'violet' in u['text'] else True


def test_reference_only_does_not_change_prompt_or_selection(res):
    a=compare(res,'violet');b=compare(res,'REFERENCE_SENTINEL')
    for m in ['FIXED_SENTENCE','QBGF','BEA_V1']:
        assert a['methods'][m]['receipt']['request_id']==b['methods'][m]['receipt']['request_id']
        assert 'REFERENCE_SENTINEL' not in res.tok.decode(b['methods'][m]['receipt']['prompt_ids'])
    assert a['methods']['FIXED_SENTENCE']['evaluation']['score']!=b['methods']['FIXED_SENTENCE']['evaluation']['score']
    impact=loo(a,res);before=len(res.calls)
    changed=rescore_existing_impact(impact,'UNKNOWN')
    assert len(res.calls)==before and changed is not impact
    assert row(changed)['ablated_answer']==row(impact)['ablated_answer']


def test_cache_is_request_bound_and_reference_independent(res):
    cache={};c=compare(res);a=loo(c,res,cache=cache);before=len(res.calls)
    b=loo(c,res,'wrong',cache=cache)
    assert len(res.calls)==before and row(b)['receipt']['cache_hit']
    assert row(a)['original_score']!=row(b)['original_score']
    for change in ['revision','device','seed','generation','template']:
        other=Resources()
        if change=='revision':other.cfg['models']['Qwen']['revision']='r2'
        elif change=='device':other.device='cuda'
        elif change=='seed':other.cfg['seed']=9
        elif change=='generation':other.cfg['generation']['max_new_tokens_qa']=16
        else:other.inference_identity=lambda:dict(other.cfg,device='cpu',template='changed-template')
        own=compare(other);n=len(other.calls);new=loo(own,other,cache=cache)
        assert len(other.calls)>n and not row(new)['receipt']['cache_hit']


def test_old_or_tampered_cache_is_not_eligible(res):
    c=compare(res);cache={};a=loo(c,res,cache=cache);key=next(iter(cache));cache[key]='legacy answer'
    n=len(res.calls);b=loo(c,res,cache=cache);assert len(res.calls)>n
    cache[key]['response']['prediction']='tampered';n=len(res.calls)
    loo(c,res,cache=cache);assert len(res.calls)>n


def test_failed_generation_and_missing_baseline_no_effect(res):
    c=compare(res);res.fail=True;a=loo(c,res)
    assert row(a)['status']=='FAILED' and row(a)['loo_delta'] is None and row(a)['effect']=='UNAVAILABLE'
    res.fail=False;c['methods']['FIXED_SENTENCE']['answer']=None
    a=loo(c,res);assert not a['impact_by_method']['FIXED_SENTENCE']['units_analyzed']


def test_stale_reader_baseline_rejected(res):
    c=compare(res);res.cfg['models']['Qwen']['revision']='new'
    a=loo(c,res)
    assert not a['impact_by_method']['FIXED_SENTENCE']['units_analyzed']
    assert 'configuration changed' in a['impact_by_method']['FIXED_SENTENCE']['error']


def test_claim_task_reaches_original_and_ablated_prompt(res):
    res.answer_override='SUPPORT';c=compare(res,'SUPPORT',task='verification');a=loo(c,res,'SUPPORT')
    assert res.calls and all(x['task']=='verification' for x in res.calls)
    assert all('allowed label' in res.tok.decode(x['ids']) for x in res.calls)
    assert row(a)['original_score']==1 and a['epsilon']==0
    with pytest.raises(ValueError):rescore_existing_impact(a,'violet','qa')


def test_changed_inputs_have_different_run_ids(res):
    a=comparison_input_id(QUERY,PASSAGES,256,'qa',res)
    assert all(a!=comparison_input_id(q,p,b,t,res) for q,p,b,t in [
        (QUERY+' Why?',PASSAGES,256,'qa'),(QUERY,[PASSAGES[0]+' Added.',PASSAGES[1]],256,'qa'),
        (QUERY,PASSAGES,1024,'qa'),(QUERY,PASSAGES,256,'verification')])


def test_last_unit_empty_context_and_duplicate_fact(res):
    one=compare(res,passages=PASSAGES[:1]);a=loo(one,res)
    assert row(a)['remaining_tokens']==0 and not row(a)['remaining_units']
    duplicate=compare(res,passages=[PASSAGES[0],PASSAGES[0]]);a=loo(duplicate,res)
    assert row(a)['remaining_units'] and row(a)['ablated_answer']=='violet'


def test_duplicate_ids_and_prompt_mismatch_fail(res):
    c=compare(res);bad=copy.deepcopy(c)
    bad['methods']['FIXED_SENTENCE']['selection']['units']*=2
    with pytest.raises(ValueError,match='Duplicate'):loo(bad,res)
    c['methods']['FIXED_SENTENCE']['receipt']['request_id']='wrong'
    assert not loo(c,res)['impact_by_method']['FIXED_SENTENCE']['units_analyzed']


def test_reader_prompt_mismatch_and_empty_output_are_failed(res):
    c=compare(res);sel=c['methods']['FIXED_SENTENCE']['selection']
    original=res.generate
    def wrong(*a,**kw):return dict(original(*a,**kw),prompt_hash='wrong')
    res.generate=wrong
    assert generate(res,QUERY,sel)['status']=='FAILED'
    def empty(*a,**kw):return dict(original(*a,**kw),prediction='INVALID_OUTPUT',raw_prediction='')
    res.generate=empty
    assert generate(res,QUERY,sel)['status']=='FAILED'


def test_receipt_snapshots_shared_configuration(res):
    from demo.live.inference import request
    c=compare(res);sel=c['methods']['FIXED_SENTENCE']['selection']
    res.inference_identity=lambda:dict(model=res.cfg['models']['Qwen'],labels=res.cfg['labels'],generation=res.cfg['generation'])
    prepared=request(res,QUERY,sel)
    res.cfg['models']['Qwen']['revision']='changed'
    assert prepared['contract']['reader']['model']['revision']=='r1'
    before=c['run_id'];res.cfg['models']['SFR']['revision']='changed-encoder'
    assert comparison_input_id(QUERY,PASSAGES,256,'qa',res)!=before


def test_bea_v2_ensemble_matches_saved_model_probabilities():
    from demo.live.bea_adapter import compute_phelp_probabilities
    from src.post_w12.bea_v2.protocol import FEATURES
    pool=[dict(unit_id='P',token_count=30)]
    sentences=[dict(unit_id='A',passage_id='P',start_char=0,token_count=10)]
    scores=dict(relevance=[.7],pairwise=[[1.]])
    ph,pm,meta=compute_phelp_probabilities(sentences,pool,scores,256,[.5])
    x=extract_bea_v2_features(sentences,pool,scores,256,[.5])
    bundles=get_utility_model()['bundles']
    np.testing.assert_allclose(ph,np.mean([b['models']['HELPFUL'].predict_proba(x)[:,1] for b in bundles],axis=0))
    np.testing.assert_allclose(pm,np.mean([b['models']['HARMFUL'].predict_proba(x)[:,1] for b in bundles],axis=0))
    assert meta['models']==15 and meta['threshold']==8e-5
    assert 'diagnostic only' in meta['harm_role']


def test_bea_v2_real_allocator_and_loo_execute(res):
    c=compare(res)
    method=c['methods']['BEA_V2']
    assert method['status']=='COMPLETE' and method['units']
    a=loo(c,res)
    rows=a['impact_by_method']['BEA_V2']['units_analyzed']
    assert rows and all(r['status']=='COMPLETE' for r in rows)
    assert all(len(r['remaining_units'])==len(r['original_units'])-1 for r in rows)
