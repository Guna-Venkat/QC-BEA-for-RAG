"""Grouped sources and compact presentation; no inference or gold-based tuning."""
import hashlib,json
from pathlib import Path
import pytest
from demo.constants import ROOT
from demo.live.preset import load_preset,is_preset,preset_cards
from demo.live.presentation import reader_answer_pair
from demo.live.bea_adapter import V2_THRESHOLD
from demo.live.resources import LiveResources


def test_original_preserved_and_reference_unchanged():
    p=load_preset('grouped');old=load_preset('original')
    assert len(p['passages'])==5 and len(old['passages'])==15
    assert p['query']==old['query'] and p['reference']==old['reference']
    assert hashlib.sha256((ROOT/'demo/assets/presets/world_cup.json').read_bytes()).hexdigest()==p['source_provenance']['original_sha256']
    assert is_preset(old['query'],old['passages']) and is_preset(p['query'],p['passages'])


def test_lengths_with_actual_qwen_tokenizer():
    p=load_preset('grouped');tok=LiveResources().tokenizer()
    assert len(preset_cards(p))==5
    for i,meta in enumerate(p['passage_metadata']):
        n=len(tok.encode(p['passages'][i],add_special_tokens=False))
        assert n==meta['source_tokens'] and 200<=n<=350
        assert preset_cards(p)[i]['title']==meta['title']


def test_every_grouped_character_is_from_retained_source_spans():
    p=load_preset('grouped');old=load_preset('original');mapping=p['source_provenance']['source_mapping']
    for m in mapping:
        assert old['passages'][int(m['original_passage_id'][1:])-1][m['start_char']:m['end_char']]==m['text']
        assert p['passages'][int(m['new_passage_id'][1:])-1][m['new_start_char']:m['new_end_char']]==m['text']
    for i,text in enumerate(p['passages'],1):
        parts=[m['text'] for m in mapping if m['new_passage_id']==f'P{i}']
        assert text=='\n\n'.join(parts)
    # Retained spans + omission receipts cover all non-whitespace original text.
    for i,text in enumerate(old['passages'],1):
        covered=set()
        for m in mapping+p['source_provenance']['omitted_segments']:
            if m['original_passage_id']==f'P{i}':covered.update(range(m['start_char'],m['end_char']))
        assert all(j in covered or c.isspace() for j,c in enumerate(text))


def test_required_query_components_remain_in_source():
    p=load_preset('grouped');text=' '.join(p['passages'])
    for fact in ['48 teams','12 groups of 4','top 2','8 best third-place','round of 32',
                 '16 groups of 3','64 to 104','7 to 8','39 days','collusion','penalty shootouts',
                 'United States','Mexico','Canada']:
        assert fact in text
    assert V2_THRESHOLD==8e-5


def test_answer_cards_wrap_and_escape_without_code_blocks():
    markup=reader_answer_pair('<script>alert(1)</script>\nA long answer.', 'Another answer.', .441,.478)
    assert '<script>' not in markup and '&lt;script&gt;' in markup
    assert '0.441' in markup and '0.478' in markup
    assert 'overflow-wrap:anywhere' in markup and 'white-space:pre-wrap' in markup
    assert 'grid-template-columns' in markup and 'overflow-x:hidden' in markup
    assert '<code' not in markup and 'Original Reader Answer' in markup and 'Reader Answer After Removal' in markup


def test_default_restored_to_original_fifteen_passages():
    assert load_preset()==load_preset('original')
    assert len(preset_cards())==15


def test_reader_cards_inherit_theme_foreground_without_white_background():
    markup=reader_answer_pair('Visible original','Visible removal',.4,.5)
    assert 'background:var(--secondary-background-color,#f8fafc)' not in markup
    assert 'color:inherit;background:rgba(148,163,184,.08)' in markup
    assert '.loo-answer-body{color:inherit;' in markup
    assert '.loo-answer-score{font-variant-numeric:tabular-nums;color:inherit;' in markup
