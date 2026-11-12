"""Demo-only source presets; original version preserved byte-for-byte."""
import json
from functools import lru_cache
from pathlib import Path
PRESET_DIR=Path(__file__).resolve().parents[1]/'assets/presets'

@lru_cache(maxsize=2)
def load_preset(version='original'):
    files={'grouped':'world_cup_grouped_v2.json','original':'world_cup.json'}
    if version not in files:raise ValueError('Unknown preset version')
    return json.loads((PRESET_DIR/files[version]).read_text())

def matching_preset(query,passages):
    for version in ['grouped','original']:
        p=load_preset(version)
        if query.strip()==p['query'] and list(passages)==p['passages']:return p
    return None

def is_preset(query,passages):return matching_preset(query,passages) is not None

def preset_cards(preset=None):
    p=preset or load_preset();titles=p.get('passage_titles',[f'Passage {i+1}' for i in range(len(p['passages']))])
    return [dict(id=i,title=titles[i],text=text) for i,text in enumerate(p['passages'])]

def passage_status(result):
    p=matching_preset(result['query'],result['passages'])
    if p is None:return []
    topics=p.get('diagnostic_passages',[dict(id='P7',topic='Tournament workload'),dict(id='P9',topic='Abandoned three-team format')])
    rows=[]
    for topic in topics:
        pid=topic['id'];ranked=next((x for x in result['ranking'] if x['unit']['document_id']==pid),None)
        candidate=ranked is not None and ranked['in_pool']
        chosen=[u for u in result['selection']['units'] if u['document_id']==pid]
        all_fine=[u for u in result['sentences'] if u['document_id']==pid]
        full=any(u['unit_type']=='PASSAGE' for u in chosen)
        allocation='NOT IN CANDIDATE POOL' if not candidate else 'DROPPED' if not chosen else 'SELECTED · FULL PASSAGE' if full else 'SELECTED · ALL SOURCE UNITS' if all_fine and len(chosen)==len(all_fine) else 'SELECTED · PARTIAL REPRESENTATION'
        option=next((o['label'] for o in result.get('qbgf_options',[]) if o['passage_id']==pid and o['selected']),None)
        rows.append(dict(Passage=pid,Topic=topic['topic'],Retrieval='RETRIEVED' if candidate else 'NOT RETRIEVED',Rank=ranked['rank'] if ranked else None,Allocation=allocation,Selected_units=len(chosen),QBGF_option=option or '—'))
    return rows
