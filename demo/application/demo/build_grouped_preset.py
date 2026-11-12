"""Deterministic source-only regrouping. No models, scoring or answer generation."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def build():
    from transformers import AutoTokenizer
    path=ROOT/'assets/presets/world_cup.json'
    original=json.loads(path.read_text());old=original['passages']
    tok=AutoTokenizer.from_pretrained(ROOT/'assets/live_tokenizer',local_files_only=True)
    def segment(i,start=None,end=None):
        text=old[i-1];a=text.index(start) if start else 0;b=text.index(end,a) if end else len(text)
        while a<b and text[a].isspace():a+=1
        while b>a and text[b-1].isspace():b-=1
        return dict(original_passage_id=f'P{i}',start_char=a,end_char=b,text=text[a:b])
    groups=[
      ('Tournament Expansion and Group Structure',[segment(5),segment(6),segment(1,'The tournament was the first FIFA')]),
      ('Tournament Workload',[segment(7),segment(12)]),
      ('Three-Team Format and Collusion',[segment(8),segment(9)]),
      ('Host Countries and Venues',[segment(1,'It was jointly hosted','The tournament was the first FIFA'),
          segment(13,'The opening match'),segment(14,end='The match schedule overlapped'),segment(15)]),
      ('Additional Tournament Information',[segment(2),segment(10),segment(11,end='Medical treatment:')]),
    ]
    passages=[];mapping=[];info=[];retained={i:[] for i in range(1,16)}
    for i,(title,parts) in enumerate(groups,1):
        body='\n\n'.join(p['text'] for p in parts);passages.append(body);cursor=0
        for part in parts:
            n=len(part['text']);mapping.append(dict(part,new_passage_id=f'P{i}',new_start_char=cursor,new_end_char=cursor+n))
            retained[int(part['original_passage_id'][1:])].append((part['start_char'],part['end_char']))
            cursor+=n+2
        info.append(dict(id=f'P{i}',title=title,source_tokens=len(tok.encode(body,add_special_tokens=False)),
                         standalone_evidence_tokens=len(tok.encode(body+'\n\n',add_special_tokens=False)),
                         original_sections=[p['original_passage_id'] for p in parts]))
    omitted=[]
    for i,text in enumerate(old,1):
        cursor=0
        for a,b in sorted(retained[i])+[(len(text),len(text))]:
            if text[cursor:a].strip():omitted.append(dict(original_passage_id=f'P{i}',start_char=cursor,end_char=a,text=text[cursor:a]))
            cursor=max(cursor,b)
    result=dict(original,name='World Cup — Grouped Passage Demo',preset_id='world-cup-grouped-v2',
        description='World Cup example using five longer source passages for interactive evidence-allocation experiments.',
        classification='DEMO-ONLY REGROUPED SOURCE PRESET',passages=passages,
        passage_titles=[x[0] for x in groups],passage_metadata=info,
        diagnostic_passages=[dict(id='P2',topic='Tournament workload'),dict(id='P3',topic='Abandoned three-team format')],
        source_provenance=dict(original_file='world_cup.json',original_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            grouping_rule='Topic-based source spans, selected before method/output evaluation. No invented/padded facts.',
            quotation_rule='Each blank-line section is a separate retained source span, not a claim of one continuous original quotation.',
            source_mapping=mapping,omitted_segments=omitted),
        tokenizer=json.loads((ROOT/'assets/live_tokenizer/source.json').read_text())['model'])
    assert all(200<=x['source_tokens']<=400 for x in info),info
    for m in mapping:
        assert old[int(m['original_passage_id'][1:])-1][m['start_char']:m['end_char']]==m['text']
        assert passages[int(m['new_passage_id'][1:])-1][m['new_start_char']:m['new_end_char']]==m['text']
    (ROOT/'assets/presets/world_cup_grouped_v2.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(info,ensure_ascii=False,indent=2))
if __name__=='__main__':build()
