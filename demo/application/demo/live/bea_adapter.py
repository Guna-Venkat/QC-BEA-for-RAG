"""Canonical allocators with an explicit exploratory cross-fit ensemble for custom inputs.

User-authorized tau=8e-5. This does not change the research calibration outcome.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
from functools import lru_cache
import joblib
from src.post_w12.bea_v2.protocol import digest
from demo.constants import ROOT
from src.post_w12.bea_qbgf.allocator import allocate as canonical_bea_v1_allocate
from src.post_w12.bea_v2.allocator import allocate as canonical_bea_v2_allocate
from src.post_w12.bea_v2.data import feature_rows
from src.post_w12.bea_v2.protocol import FEATURES

V1_PARAMETERS = dict(eta_cov=.5, lambda_red=.5, min_parent_sentences=2,
                     tau_context=.05, tau_expand=.01, tau_stop=.01)


V2_THRESHOLD = 8e-5
V2_MODEL_ROOT = ROOT/'results/post_w12/bea_v2/v3'
V2_POLICY = 'equal-dataset mean of five-fold means; exploratory custom-input ensemble'


@lru_cache(maxsize=4)
def _load_ensemble(manifest_hash, inventory):
    bundles=[]
    for path,dataset,fold,expected in inventory:
        bundle=joblib.load(path)
        if (bundle.get('dataset')!=dataset or bundle.get('fold')!=fold
                or bundle.get('feature_names')!=FEATURES
                or bundle.get('feature_hash')!=digest(FEATURES)):
            raise ValueError('BEA-v2 model feature/fold identity mismatch')
        for target in ['HELPFUL','HARMFUL']:
            if target not in bundle['models']:
                raise ValueError('BEA-v2 predictor target missing')
            if getattr(bundle['models'][target], 'n_features_in_',len(FEATURES))!=len(FEATURES):
                raise ValueError('BEA-v2 predictor feature width changed')
        bundles.append(bundle)
    return bundles


def get_utility_model():
    manifest=V2_MODEL_ROOT/'utility_model/MODELS.json'
    if not manifest.is_file():raise RuntimeError('Saved BEA-v2 model manifest missing')
    raw=manifest.read_bytes();data=json.loads(raw)
    if data['feature_hash']!=digest(FEATURES):raise ValueError('BEA-v2 schema manifest mismatch')
    expected_files={f'utility_model/fold_{d}_{i}.joblib' for d in ['HotpotQA','QASPER','SciFact'] for i in range(5)}
    if set(data['files'])!=expected_files:raise ValueError('Expected all 15 saved BEA-v2 folds')
    inventory=[]
    for dataset in ['HotpotQA','QASPER','SciFact']:
        for fold in range(5):
            rel=f'utility_model/fold_{dataset}_{fold}.joblib';path=V2_MODEL_ROOT/rel
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=data['files'][rel]:
                raise ValueError('BEA-v2 saved model checksum mismatch: '+rel)
            inventory.append((str(path),dataset,fold,data['files'][rel]))
    manifest_hash=hashlib.sha256(raw).hexdigest()
    return dict(bundles=_load_ensemble(manifest_hash,tuple(inventory)),
                manifest_sha256=manifest_hash,files=data['files'],policy=V2_POLICY)


def extract_bea_v2_features(sentences, pool, scores, budget, passage_scores):
    rows = feature_rows(dict(sentences=sentences, pool=pool, scores=scores,
                             passage_scores=passage_scores), budget)
    return np.asarray([[r[f] for f in FEATURES] for r in rows], dtype=float).reshape(-1, len(FEATURES))


def compute_phelp_probabilities(sentences,pool,scores,budget,passage_scores):
    ensemble=get_utility_model()
    features=extract_bea_v2_features(sentences,pool,scores,budget,passage_scores)
    by_dataset={d:{'HELPFUL':[],'HARMFUL':[]} for d in ['HotpotQA','QASPER','SciFact']}
    for bundle in ensemble['bundles']:
        for target in ['HELPFUL','HARMFUL']:
            values=bundle['models'][target].predict_proba(features)[:,1] if len(features) else np.array([])
            if not np.isfinite(values).all() or np.any((values<0)|(values>1)):
                raise ValueError('BEA-v2 predictor returned invalid probabilities')
            by_dataset[bundle['dataset']][target].append(values)
    probabilities={target:np.mean([np.mean(by_dataset[d][target],axis=0)
                    for d in by_dataset],axis=0).tolist() for target in ['HELPFUL','HARMFUL']}
    metadata=dict(policy=V2_POLICY,models=15,feature_hash=digest(FEATURES),
                  manifest_sha256=ensemble['manifest_sha256'],model_files=ensemble['files'],
                  threshold=V2_THRESHOLD,calibration_status='FAILED; user-selected exploratory threshold',
                  harm_role='diagnostic only; allocator uses P_help * max(0, IG)')
    return probabilities['HELPFUL'],probabilities['HARMFUL'],metadata


def run_bea_v1(pool, sentences, scores, tok, budget):
    path = ROOT/'results/post_w12/bea_qbgf/v3/BEA_QBGF_V1_FREEZE.json'
    if not path.is_file():
        raise RuntimeError('Canonical BEA-v1 parameter freeze unavailable')
    parameters = json.loads(path.read_text())['identity']['parameters']
    if parameters != V1_PARAMETERS:
        raise RuntimeError('BEA-v1 parameter freeze differs from the reviewed contract')
    result = canonical_bea_v1_allocate(pool, sentences, scores, tok, budget, parameters)
    result['execution_contract'] = dict(parameters=parameters,
        freeze_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), scorer='SFR cosine')
    return result


def run_bea_v2(pool,sentences,scores,tok,budget,passage_scores):
    ph,pm,metadata=compute_phelp_probabilities(sentences,pool,scores,budget,passage_scores)
    params=dict(eta_cov=.5,lambda_red=.5,min_parent_sentences=2)
    result=canonical_bea_v2_allocate(pool,sentences,scores,dict(p_help=ph,p_harm=pm),
                                   tok,budget,params,threshold=V2_THRESHOLD)
    metadata.update(parameters=params,p_help=ph,p_harm=pm)
    return result,metadata
