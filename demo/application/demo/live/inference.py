"""Session-only, content-addressed live reader requests. Never reads a reference."""
import copy
from contextlib import nullcontext
from src.week12.protocol import digest
from src.week12.reader import prompt_ids

VERSION = 'live-reader-request-v3'


def lock(resources):
    return getattr(resources, 'lock', nullcontext())


def request(resources, query, selection, task_type='freeform_qa'):
    if task_type not in ('freeform_qa', 'verification'):
        raise ValueError('Unsupported reader task')
    identity = copy.deepcopy(resources.inference_identity())
    tok = resources.tokenizer()
    labels = identity['labels']
    ids = prompt_ids(tok, query, task_type, selection['evidence_ids'], labels)
    contract = dict(version=VERSION, reader=identity, task_type=task_type, prompt_ids=ids)
    key = digest(contract)
    return dict(request_id=key, contract=contract, prompt_hash=digest(ids),
                prompt_ids=ids, prompt_text=tok.decode(ids, skip_special_tokens=False),
                evidence_hash=digest(selection['evidence_ids']),
                selected_unit_ids=[u['unit_id'] for u in selection['units']],
                evidence_tokens=selection['evidence_tokens'])


def generate(resources, query, selection, task_type='freeform_qa', enabled=True, cache=None):
    """Only complete, verified receipts may be reused; failures are never cached."""
    with lock(resources):
        if not enabled:
            return dict(status='UNAVAILABLE', prediction=None, error='Live reader disabled', receipt=None)
        req = request(resources, query, selection, task_type)
        key = VERSION + ':' + req['request_id']
        entry = cache.get(key) if cache is not None else None
        if (isinstance(entry, dict) and entry.get('version') == VERSION
                and entry.get('request_id') == req['request_id']
                and entry.get('checksum') == digest(entry.get('response'))
                and entry.get('response', {}).get('prediction')):
            return dict(status='COMPLETE', **copy.deepcopy(entry['response']),
                        receipt=dict(req, cache_hit=True))
        try:
            response = resources.generate(query, selection, task_type=task_type)
            if 'raw_prediction' in response and not (response.get('raw_prediction') or '').strip():
                raise ValueError('Reader returned an empty output')
            if response.get('prompt_hash') != req['prompt_hash']:
                raise ValueError('Reader prompt differs from the prepared request')
            from .engine import safe_answer
            answer = safe_answer(response.get('prediction') or '')
            if not answer:
                raise ValueError('Reader returned no usable answer')
            # Keep hidden thinking out of all displayed response fields.
            response = dict(response, prediction=answer, raw_prediction=answer)
        except Exception as exc:
            return dict(status='FAILED', prediction=None, error=str(exc), receipt=dict(req, cache_hit=False))
        if cache is not None:
            cache[key] = dict(version=VERSION, request_id=req['request_id'],
                              response=copy.deepcopy(response), checksum=digest(response))
            while len(cache) > 128:
                cache.pop(next(iter(cache)))
        return dict(status='COMPLETE', **response, receipt=dict(req, cache_hit=False))
