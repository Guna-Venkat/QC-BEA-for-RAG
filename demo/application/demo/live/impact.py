"""Strict custom-input comparisons and no-refill LOO; session-only outputs."""
import copy
import time
from collections import Counter
import numpy as np
from src.week12.protocol import digest
from src.week12.reader import parse_label, LABELS
from .segmentation import DEFAULT as SEGMENTATION, documents as source_documents, annotate
from .bea_adapter import run_bea_v1, run_bea_v2
from .inference import generate, request, lock, VERSION

QA_LOO_EPSILON = .01
LOO_CONVENTION = 'delta = ablated score - original score'
CANONICAL_METHODS = ('FIXED_SENTENCE', 'QBGF', 'BEA_V1', 'BEA_V2')
METHOD_NAMES = dict(FIXED_SENTENCE='Best Sentences', QBGF='QBGF', BEA_V1='BEA-V1', BEA_V2='BEA-V2')
METHOD_EXPLANATIONS = dict(
    FIXED_SENTENCE='Canonical query-SFR sentence ranking and exact token-budget packing.',
    QBGF='Canonical SFR fidelity options and exact multiple-choice cost-state dynamic programming.',
    BEA_V1='Canonical relevance, aspect coverage and redundancy transitions; frozen tau=.01.',
    BEA_V2='Exploratory BEA-v2: saved cross-fit model ensemble, canonical P_help-weighted allocation, tau=0.00008; not a calibrated deployment policy.')


def normalize_answer(text):
    import re, string
    text = ''.join(c for c in str(text).lower() if c not in string.punctuation)
    return ' '.join(re.sub(r'\b(a|an|the)\b', ' ', text).split())


def score_answer(prediction, reference, task_format='qa'):
    if prediction is None or not str(prediction).strip():
        return dict(score=None, metric='Unavailable', valid=False, details='Reader output unavailable')
    if not reference or not str(reference).strip():
        return dict(score=None, metric='Unavailable', valid=False, details='Reference unavailable')
    if task_format == 'verification':
        if reference.strip() not in LABELS:
            raise ValueError('Reference must be exactly SUPPORT, REFUTE or NOT_ENOUGH_INFO')
        label = parse_label(str(prediction))
        correct = label == reference.strip()
        return dict(score=float(correct), metric='Categorical Accuracy', valid=True,
                    predicted_label=label, gold_label=reference.strip(), is_correct=correct,
                    invalid_output=label == 'INVALID_OUTPUT')
    if task_format != 'qa':
        raise ValueError('Unknown task format')
    pn, gn = normalize_answer(prediction), normalize_answer(reference)
    a, b = pn.split(), gn.split()
    overlap = sum((Counter(a) & Counter(b)).values())
    precision = overlap/len(a) if a else float(not b)
    recall = overlap/len(b) if b else float(not a)
    f1 = 2*precision*recall/(precision+recall) if precision+recall else 0.
    return dict(score=f1, f1=f1, precision=precision, recall=recall,
                exact_match=pn == gn, metric='Token F1', valid=True)


def classify_loo_effect(delta, task_format='qa', epsilon=QA_LOO_EPSILON):
    if delta is None or not np.isfinite(delta):
        return 'UNAVAILABLE', '#f59e0b'
    tolerance = 0. if task_format == 'verification' else epsilon
    if delta < -tolerance:
        return 'HELPFUL', '#10b981'
    if delta > tolerance:
        return 'HARMFUL', '#ef4444'
    return 'NO_MEASURABLE_CHANGE', '#94a3b8'


def comparison_input_id(query, passages, budget, task_format, resources, segmentation=SEGMENTATION):
    return digest(dict(version=VERSION, query=query.strip(), passages=[p.strip() for p in passages],
                       budget=budget, task=task_format, segmentation=segmentation,
                       reader=resources.inference_identity(),
                       scoring_model=getattr(resources,'cfg',{}).get('models',{}).get('SFR'),
                       scoring='SFR cosine, width 10'))


def _unavailable(method, budget, reason):
    return dict(method=method, name=METHOD_NAMES[method], status='UNAVAILABLE', error=reason,
                answer=None, evaluation=None, units=[], evidence_tokens=0, budget=budget,
                explanation=METHOD_EXPLANATIONS[method])


def compare_four_methods(query, passages, budget, task_format='qa', user_reference=None,
                         resources=None, enable_models=False, segmentation=SEGMENTATION, cache=None):
    from .engine import validate
    query, passages = validate(query, passages, 'FIXED_SENTENCE', budget, 'SFR')
    if task_format not in ('qa', 'verification'):
        raise ValueError('Unknown task format')
    if task_format == 'verification' and user_reference and user_reference.strip() not in LABELS:
        raise ValueError('Reference must be exactly SUPPORT, REFUTE or NOT_ENOUGH_INFO')
    start = time.perf_counter()
    result = dict(version=VERSION, query=query, passages=passages, budget=budget,
                  task_format=task_format, segmentation=segmentation, user_reference=user_reference,
                  pool=[], sentences=[], methods={m:_unavailable(m,budget,'Enable Live Models: canonical comparison requires SFR scoring.') for m in CANONICAL_METHODS})
    if resources is None or not enable_models:
        result['elapsed_seconds'] = time.perf_counter()-start
        return result
    with lock(resources):
        tok = resources.tokenizer()
        if len(tok.encode(query, add_special_tokens=False)) > 512:
            raise ValueError('Keep the query below 512 reader tokens')
        result['run_id'] = comparison_input_id(query, passages, budget, task_format, resources, segmentation)
        from src.week11.hierarchy import build
        from src.week12.algorithm import choose, cosine, validate_spans
        from src.post_w12.bea_qbgf.allocator import aspects, signals
        docs = source_documents(passages, segmentation)
        all_units = annotate(build(docs, tok, dict(max_passage_tokens=256)), segmentation)
        all_passages = [u for u in all_units if u['unit_type']=='PASSAGE']
        if sum(u['token_count'] for u in all_passages) > 16000:
            raise ValueError('Use no more than 16,000 source tokens')
        try:
            qvec = resources.embed([query], 'query')[0]
            ps = cosine(qvec, resources.embed([p['source_text'] for p in all_passages], 'document'))
            ix = sorted(range(len(all_passages)), key=lambda i:(-ps[i], i))[:10]
            pool = [all_passages[i] for i in ix]; ps = [ps[i] for i in ix]
            parent_ids = {p['unit_id'] for p in pool}
            sentences = [u for u in all_units if u['unit_type']=='SENTENCE' and u['passage_id'] in parent_ids]
            vectors = resources.embed([s['source_text'] for s in sentences], 'document') if sentences else np.zeros((0,len(qvec)))
            ss = dict(zip([s['unit_id'] for s in sentences], cosine(qvec, vectors)))
        except Exception as exc:
            result['methods'] = {m:_unavailable(m,budget,f'Required SFR scoring failed: {exc}; no scorer substitution.') for m in CANONICAL_METHODS}
            result['elapsed_seconds'] = time.perf_counter()-start
            return result
        result.update(pool=pool, sentences=sentences, passage_scores=ps, sentence_scores=ss,
                      scorer='SFR cosine', device=getattr(resources,'device',None))
        bea_scores = None; bea_error = None
        try:
            av = resources.embed(aspects(query), 'query')
            bea_scores = signals(vectors, qvec, av)
        except Exception as exc:
            bea_error = f'Required aspect scoring failed: {exc}'
        for method in CANONICAL_METHODS:
            try:
                meta = {}
                if method in ('FIXED_SENTENCE','QBGF'):
                    sel = choose(pool, sentences, [], ps, ss, tok, budget, 'QBGF_FULL' if method=='QBGF' else method)
                elif method=='BEA_V1':
                    if bea_error:raise RuntimeError(bea_error)
                    sel = run_bea_v1(pool, sentences, bea_scores, tok, budget)
                    meta['execution_contract'] = sel['execution_contract']
                else:
                    sel, meta = run_bea_v2(pool, sentences, bea_scores, tok, budget, passage_scores=ps)
                validate_spans(sel['units'], docs)
                if sel['evidence_tokens'] > budget:raise ValueError('Evidence exceeds budget')
                response = generate(resources, query, sel, 'verification' if task_format=='verification' else 'freeform_qa', True, cache)
                answer = response.get('prediction')
                result['methods'][method] = dict(method=method, name=METHOD_NAMES[method], selection=sel,
                    units=sel['units'], budget=budget, evidence_tokens=sel['evidence_tokens'],
                    answer=answer, raw_prediction=answer, status=response['status'], reader_error=response.get('error'),
                    receipt=response.get('receipt'), execution_metadata=meta,
                    evaluation=score_answer(answer,user_reference,task_format) if answer and user_reference else None,
                    stop_reason=sel.get('stop_reason','BUDGET_PACKING'),
                    stopped_early=sel.get('stop_reason')=='LOW_MARGINAL_VALUE', explanation=METHOD_EXPLANATIONS[method])
            except Exception as exc:
                result['methods'][method] = _unavailable(method,budget,str(exc))
    result['elapsed_seconds'] = time.perf_counter()-start
    return result


def _score_intervention(row, reference, task):
    if row.get('status') != 'COMPLETE':
        row.update(original_score=None, ablated_score=None, loo_delta=None, effect='UNAVAILABLE',
                   effect_color='#f59e0b', explanation='Analysis unavailable: '+row.get('error','reader output missing'))
        return
    original = score_answer(row['original_answer'],reference,task)
    ablated = score_answer(row['ablated_answer'],reference,task)
    if not original['valid'] or not ablated['valid']:
        row['status']='FAILED';row['error']='A required reader output is unavailable'
        return _score_intervention(row,reference,task)
    delta = ablated['score']-original['score']
    effect, color = classify_loo_effect(delta,task)
    row.update(original_score=original['score'], ablated_score=ablated['score'], loo_delta=delta,
               effect=effect, effect_color=color, explanation=(f'Reference agreement changed from {original["score"]:.3f} '
               f'to {ablated["score"]:.3f} (ablated − original = {delta:+.3f}). '
               'This is an observed input-deletion effect, not proof of internal reasoning.'))


def analyze_evidence_impact(comparison_results, user_reference, top_n_units=1, resources=None,
                             enable_models=False, cache=None):
    from src.week12.algorithm import serialize
    if not user_reference or not user_reference.strip():
        raise ValueError('A reference answer is required for LOO scoring')
    query = comparison_results['query']; task = comparison_results.get('task_format','qa')
    if task=='verification' and user_reference.strip() not in LABELS:
        raise ValueError('Reference must be exactly SUPPORT, REFUTE or NOT_ENOUGH_INFO')
    if resources is None:raise ValueError('Exact tokenizer and reader identity are required')
    if top_n_units < 1:raise ValueError('Choose at least one deletion unit')
    output = dict(version=VERSION,run_id=comparison_results.get('run_id'),query=query,
                  user_reference=user_reference,task_format=task,impact_by_method={},cache=cache if cache is not None else {},
                  epsilon=0. if task=='verification' else QA_LOO_EPSILON, convention=LOO_CONVENTION,
                  sampling='First N selected units in source order; not exhaustive LOO')
    with lock(resources):
        tok=resources.tokenizer()
        for method in CANONICAL_METHODS:
            original=comparison_results.get('methods',{}).get(method,{})
            units=original.get('selection',{}).get('units',[])
            group=dict(method=method,name=METHOD_NAMES[method],units_analyzed=[],status='UNAVAILABLE')
            output['impact_by_method'][method]=group
            if not units:
                group['error']=original.get('error','No evidence selected');continue
            if len({u['unit_id'] for u in units})!=len(units):
                raise ValueError('Duplicate selected unit IDs')
            full=serialize(units,tok)
            if full['evidence_ids']!=original['selection']['evidence_ids']:
                raise ValueError('Original evidence serialization changed; rerun comparison')
            current=request(resources,query,full,'verification' if task=='verification' else 'freeform_qa')
            valid=(original.get('status')=='COMPLETE' and original.get('answer') and
                   original.get('receipt',{}).get('request_id')==current['request_id'])
            if not valid:
                group['error']='Original reader output/receipt unavailable or configuration changed; rerun comparison.'
                continue
            group.update(status='COMPLETE',original_answer=original['answer'],original_units=units,
                         original_serialized_text=full['text'],original_tokens=full['evidence_tokens'],
                         original_score=score_answer(original['answer'],user_reference,task)['score'],budget=comparison_results['budget'])
            for unit in units[:top_n_units]:
                remaining=[u for u in units if u['unit_id']!=unit['unit_id']]
                sel=serialize(remaining,tok)
                assert len(sel['units'])==len(units)-1
                response=generate(resources,query,sel,'verification' if task=='verification' else 'freeform_qa',enable_models,output['cache'])
                row=dict(unit_id=unit['unit_id'],unit=unit,text=unit['source_text'],method=method,
                    method_name=METHOD_NAMES[method],passage_id=unit['document_id'],token_count=unit['token_count'],
                    budget=comparison_results['budget'],original_units=units,original_serialized_text=full['text'],
                    original_tokens=full['evidence_tokens'],remaining_units=sel['units'],remaining_serialized_text=sel['text'],
                    remaining_tokens=sel['evidence_tokens'],ablated_tokens=sel['evidence_tokens'],ablated_sel=sel,
                    freed_tokens=full['evidence_tokens']-sel['evidence_tokens'],original_answer=original['answer'],
                    ablated_answer=response.get('prediction'),status=response['status'],error=response.get('error'),
                    original_receipt=original['receipt'],receipt=response.get('receipt'))
                _score_intervention(row,user_reference,task)
                group['units_analyzed'].append(row)
    return output


def rescore_existing_impact(impact_data,new_reference,task_format='qa'):
    if not new_reference or not new_reference.strip():return impact_data
    if task_format!=impact_data['task_format']:
        raise ValueError('Changing task requires a new comparison, not reference-only rescoring')
    result=copy.deepcopy(impact_data)
    result['user_reference']=new_reference
    for group in result.get('impact_by_method',{}).values():
        if group.get('original_answer'):
            group['original_score']=score_answer(group['original_answer'],new_reference,task_format)['score']
        for row in group.get('units_analyzed',[]):_score_intervention(row,new_reference,task_format)
    return result
