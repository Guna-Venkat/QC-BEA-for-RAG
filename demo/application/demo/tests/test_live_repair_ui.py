"""Current two-action UI: valid receipts, failed interventions and stale state."""
from pathlib import Path
from streamlit.testing.v1 import AppTest


def host(tmp_path):
    script=tmp_path/'corrected_live_host.py'
    script.write_text('''import streamlit as st
from demo.live import ui
from demo.tests.test_live_impact import Resources,PASSAGES,QUERY
if '_test_resources' not in st.session_state:
 st.session_state['_test_resources']=Resources()
ui.resources=lambda:st.session_state['_test_resources']
ui.available=lambda:dict(sfr_local=True,qwen_local=True,gpu_free_mib=None)
if 'live_passages_data' not in st.session_state:
 st.session_state['live_passages_data']=[dict(id=i,title=str(i),text=p) for i,p in enumerate(PASSAGES)]
 st.session_state['live_query']=QUERY
 st.session_state['live_models_enabled']=True
 st.session_state['live_user_ref_text']='violet'
ui.render()
''')
    at=AppTest.from_file(str(script),default_timeout=30).run()
    assert not at.exception,[x.message for x in at.exception]
    return at

def click(at,text):
    next(b for b in at.button if text in b.label).click().run()
    assert not at.exception,[x.message for x in at.exception]
    return at

def texts(at):return ' '.join(x.value for group in [at.markdown,at.caption,at.warning,at.error,at.info] for x in group)


def test_current_comparison_loo_receipts_and_reference_rescore(tmp_path):
    at=host(tmp_path);click(at,'Compare Four Methods');click(at,'Analyze Evidence Impact')
    text=texts(at)
    assert 'Before / After Answer Comparison' in text and 'Live LOO threshold: 0.01' in text
    assert 'Threshold: |Δ| > 0.05' not in text
    assert 'BEA-v2 · τ' not in text
    assert any(e.label=='Advanced details · BEA-V2 execution' for e in at.expander)
    assert at.session_state['live_four_results']['methods']['BEA_V2']['status']=='COMPLETE'
    a=at.session_state['live_impact_results'];r=a['impact_by_method']['FIXED_SENTENCE']['units_analyzed'][0]
    assert r['status']=='COMPLETE' and r['original_receipt'] and r['receipt']
    before=len(at.session_state['_test_resources'].calls)
    next(x for x in at.text_area if 'Reference Answer' in x.label).set_value('UNKNOWN').run()
    click(at,'Rescore Answers')
    assert len(at.session_state['_test_resources'].calls)==before


def test_changed_input_blocks_analysis(tmp_path):
    at=host(tmp_path);click(at,'Compare Four Methods')
    next(x for x in at.text_area if x.label=='Your query').set_value('A changed question?').run()
    click(at,'Analyze Evidence Impact')
    assert 'Analysis blocked' in texts(at)
    assert 'live_impact_results' not in at.session_state


def test_failed_intervention_ui_never_claims_measured_effect(tmp_path):
    at=host(tmp_path);click(at,'Compare Four Methods')
    at.session_state['_test_resources'].fail=True
    click(at,'Analyze Evidence Impact')
    assert 'No valid intervention pair' in texts(at)
    assert any(x.label=='Failed / Unavailable' and int(x.value)>0 for x in at.metric)


def test_passage_removal_preserves_other_text_and_empty_query(tmp_path):
    at=host(tmp_path)
    original=at.session_state['live_passages_data'][1]['text']
    next(b for b in at.button if b.key=='btn_remove_passage_0').click().run()
    assert not at.exception
    assert at.session_state['live_passages_data'][0]['text']==original
    next(x for x in at.text_area if x.label=='Your query').set_value('').run()
    click(at,'Compare Four Methods')
    assert 'Please enter a question' in texts(at)
