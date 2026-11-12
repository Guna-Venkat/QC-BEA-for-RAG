"""Escaped, responsive live-answer cards. No scoring or algorithm behavior."""
from html import escape

def reader_answer_pair(original,ablated,original_score,ablated_score):
    def card(label,answer,score,style):
        value=f'{score:.3f}' if score is not None else 'Unavailable'
        text=escape(str(answer or 'Reader output unavailable'))
        return (f'<article class="loo-answer-card {style}"><header><strong>{label}</strong>'
                f'<span class="loo-answer-score">Score {value}</span></header>'
                f'<div class="loo-answer-body">{text}</div></article>')
    return '''<style>
.loo-answer-pair{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin:8px 0 12px}
.loo-answer-card{min-width:0;border:1px solid #dbe4ec;border-top:3px solid #64748b;border-radius:10px;padding:14px 16px;color:inherit;background:rgba(148,163,184,.08)}
.loo-answer-card.after{border-top-color:#0d9488}
.loo-answer-card header{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px;font-size:.88rem;margin-bottom:10px}
.loo-answer-score{font-variant-numeric:tabular-nums;color:inherit;opacity:.85;font-size:.82rem}
.loo-answer-body{color:inherit;white-space:pre-wrap;overflow-wrap:anywhere;word-break:normal;font-size:.95rem;line-height:1.55;max-height:18rem;overflow-y:auto;overflow-x:hidden}
@media(max-width:750px){.loo-answer-pair{grid-template-columns:minmax(0,1fr)}}
</style><section class="loo-answer-pair" aria-label="Reader answers before and after evidence removal">'''+card('Original Reader Answer',original,original_score,'before')+card('Reader Answer After Removal',ablated,ablated_score,'after')+'</section>'
