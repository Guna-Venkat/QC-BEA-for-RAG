from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASETS = ('HotpotQA', 'QASPER', 'SciFact')
PRIMARY_METHODS = ('RAW_SKIP', 'FIXED_SENTENCE', 'QBGF_FULL', 'BEA_QBGF_V1', 'BEA_V2')
METHODS = ('RAW_SKIP', 'FIXED_SENTENCE', 'H3', 'QBGF_FULL', 'NONE')
ALL_METHODS = ('RAW_SKIP', 'FIXED_SENTENCE', 'H3', 'QBGF_FULL', 'BEA_QBGF_V1', 'BEA_V2', 'NONE')
BUDGETS = (256, 1024)

# User-facing color semantics defined by the CS787 research protocol
COLORS = {
    'SELECTED': '#10b981',       # Green: selected into prompt
    'OMITTED': '#94a3b8',        # Grey: omitted / dropped
    'DECISIVE': '#3b82f6',       # Blue: decisive ground-truth carrier
    'WARNING': '#f59e0b',        # Orange: budget / stopping threshold alert
    'HARMFUL': '#ef4444',        # Red: harmful under leave-one-out intervention
    'HELPFUL': '#10b981',        # Green: helpful under LOO
    'NEUTRAL': '#94a3b8',        # Slate: neutral under LOO
    
    # Method-specific palette
    'RAW_SKIP': '#f59e0b',
    'FIXED_SENTENCE': '#22c3ad',
    'H3': '#818cf8',
    'QBGF_FULL': '#38bdf8',
    'BEA_QBGF_V1': '#f97316',
    'BEA_V2': '#8b5cf6',
    'NONE': '#64748b',
    'MINILM_RERANK': '#ec4899',
    'BM25': '#f59e0b',
    'SFR': '#22c3ad',
    'Qwen': '#22c3ad',
    'Mistral': '#f59e0b',
    'Llama': '#818cf8',
}

# Clear human-readable method labels
LABELS = {
    'RAW_SKIP': 'Whole Passages',
    'FIXED_SENTENCE': 'Best Sentences',
    'QBGF_FULL': 'QBGF',
    'BEA_QBGF_V1': 'BEA-V1',
    'BEA_V2': 'BEA-V2',
    'NONE': 'No Evidence',
    'H3': 'Hierarchy (H3)',
    'C2': 'Top-8 Sentences (C2)',
    'MINILM_RERANK': 'MiniLM Cross-Encoder',
    'BM25_PLAIN_RAG': 'BM25 Whole Passages',
}

EXPLANATIONS = {
    'RAW_SKIP': 'Whole passages in retrieval order. Includes full passages until the token budget is exhausted; skips oversized candidates.',
    'FIXED_SENTENCE': 'Ranks exact source sentences by dense query similarity. Fills the token budget with top sentences and restores original passage order.',
    'QBGF_FULL': 'Query-Conditioned Budgeted Granularity Fusion. Selects a representation fidelity (DROP, 1/2/4/8 sentences, or FULL) per passage via exact knapsack optimization.',
    'BEA_QBGF_V1': 'Budget-Aware Evidence Allocation (v1). Dynamically adds evidence incrementally based on marginal relevance/coverage gain and stops early when gain/cost drops below a threshold.',
    'BEA_V2': 'Usefulness-Weighted Allocation (v2). Weights marginal incremental evidence by a learned Leave-One-Out helpfulness probability P_help.',
    'NONE': 'Direct reader generation without external evidence (reader parameter knowledge baseline).',
    'H3': 'Hierarchical heuristic control: query-ranked sentences from top-3 passages plus fine spans from remaining candidates.',
    'C2': 'Top-eight query-ranked exact sentences with prefix packing.',
    'MINILM_RERANK': 'Cross-encoder control reranking all candidate sentences using ms-marco-MiniLM-L-6-v2.',
    'BM25_PLAIN_RAG': 'Baseline whole-passage RAG using lexical BM25 retrieval rather than SFR embeddings.'
}

SOURCES = {
    'retrieval_pilot': 'results/week11/multigranular/v1/retrieval/retrieval_summary_df.csv',
    'retrieval_manifest': 'results/week11/multigranular/v1/retrieval/manifest.json',
    'reader_pilot': 'results/week11/multigranular/v1/reader_granularity/audited_summary.csv',
    'reader_manifest': 'results/week11/multigranular/v1/reader_granularity/manifest.json',
    'reader_pairs': 'results/week11/multigranular/v1/reader_granularity/named_reader_comparisons.csv',
    'reader_interactions': 'results/week11/multigranular/v1/reader_granularity/named_reader_granularity_interactions.csv',
    'reader_compliance': 'results/week11/multigranular/v1/reader_granularity/label_compliance_diagnostic_summary.csv',
    'reader_panel': 'results/week10/root_cause/v1/full_reader_panel_summary.csv',
    'reader_panel_ci': 'results/week10/root_cause/v1/full_reader_bootstrap.csv',
    'w10_protocol': 'results/week10/root_cause/v1/protocol.json',
    'extension': 'results/week12/qbgf/v3/c_extension/v1/analysis/merged_validation_summary.csv',
    'specialists': 'results/week12/qbgf/v3/c_extension/v1/analysis/specialist_references.csv',
    'gold_overlap': 'results/week12/attribution/v1/analysis/gold_overlap.csv',
    'retention': 'results/week12/attribution/v1/analysis/finite_retention_summary.csv',
    'w10_runner': 'src/week10/root_cause/runner.py',
    'w11_runner': 'src/week11/runner.py',
    'w10': 'results/week10/root_cause/v1/retrieval_summary.csv',
    'w11': 'results/week11/multigranular/v1/granularity_budget/c_summary_df.csv',
    'validation': 'results/week12/qbgf/v3/analysis/summary.csv',
    'primary': 'results/week12/qbgf/v3/analysis/primary_comparisons.csv',
    'fusion': 'results/week12/qbgf/v3/analysis/fusion_diagnostic_comparisons.csv',
    'confirmation': 'results/week12/final_confirmation/v1/summary.csv',
    'contrasts': 'results/week12/final_confirmation/v1/contrasts.csv',
    'consistency': 'results/week12/final_confirmation/v1/validation_comparison.csv',
    'units': 'results/week12/attribution/v1/analysis/unit_importance.csv',
    'profiles': 'results/week12/attribution/v1/analysis/query_profiles.csv',
    'correlations': 'results/week12/attribution/v1/analysis/relevance_utility.csv',
    'qualitative': 'results/week12/attribution/v1/analysis/qualitative_candidates.json',
    'freeze': 'results/week12/W13_FINAL_METHOD_FREEZE.json',
    'freeze_copy': 'results/week12/qbgf/v3/W13_FINAL_METHOD_FREEZE.json',
    'split': 'results/week12/qbgf/v3/protocol/W12_SPLIT_FREEZE.json',
    'code': 'src/week12/algorithm.py',
}

FREEZE_SHA = 'd0188a3582d6aead0a3a31f9f15bad9b51a88a6b475b05ac79ae38e58f05366b'


def calculate_utilization(tokens_used: int, budget: int) -> float:
    """Calculate token utilization percentage rounded to 1 decimal place.
    
    Canonical test cases verified:
    245 / 256   -> 95.7%
    251 / 256   -> 98.0%
    255 / 256   -> 99.6%
    242 / 256   -> 94.5%
    245 / 1024  -> 23.9%
    965 / 1024  -> 94.2%
    0 / 256     -> 0.0%
    256 / 256   -> 100.0%
    1024 / 1024 -> 100.0%
    """
    if budget <= 0:
        return 0.0
    return round((tokens_used / budget) * 100.0, 1)

