"""One-time source-path organization; never rewrites research Python bytes."""
import hashlib
import json
from pathlib import Path

FINAL = Path(__file__).resolve().parents[2]
SRC = FINAL / '11_shared_infrastructure/runtime/src'
MAP = {
    'week0': ('dataset_diagnostics', 'Dataset adapters, evidence utilization and layer diagnostics'),
    'week2': ('context_budget_surfaces', 'Fixed-context response sweeps and query feature extraction'),
    'week3': ('context_oracle_analysis', 'Oracle ceilings, epsilon targets and context heterogeneity'),
    'week4': ('query_context_allocation', 'Query-conditioned context allocation models and feature ablations'),
    'week5': ('content_aware_allocation', 'Passage-transformer allocation and regret prediction'),
    'week6': ('passage_routing', 'Semantic passage routing and learned passage importance'),
    'week7': ('adaptive_routing_policies', 'Routing-aware budgets, continuation and fidelity policies'),
    'week9': ('evidence_representation', 'Retrieval, sentence suppression and frozen execution support'),
    'week10': ('reader_diagnostics', 'Reader and evidence-utilization root-cause diagnostics'),
    'week11': ('granularity_study', 'Matched retrieval, hierarchy, budgets, readers and granularity experiments'),
    'week12': ('budgeted_evidence_fusion', 'QBGF, exact packing, controlled evaluation and frozen protocol'),
    'week12_extension': ('baseline_comparisons', 'Matched passage baselines and specialist SARA comparisons'),
    'week12_attribution': ('evidence_attribution', 'No-refill evidence deletion and downstream-utility analysis'),
    'week12_confirmation': ('frozen_confirmation', 'Frozen final-method guards, execution and confirmation reporting'),
    'week12_final_review.py': ('final_method_review.py', 'Final selection and method-review checks'),
    'post_w12': ('exploratory_allocation', 'BEA-v1, learned-helpfulness BEA-v2 and qualitative case studies'),
}
NESTED = {
    'adaptive_routing_policies/w7a': ('modular_routing', 'Compose budget allocation with semantic routing'),
    'adaptive_routing_policies/w7b': ('routing_budget_surfaces', 'Routing-aware context response surfaces'),
    'adaptive_routing_policies/w7c': ('semantic_sufficiency', 'Retrieval-aware sufficiency prediction'),
    'adaptive_routing_policies/w7c2': ('utility_continuation', 'Utility-aware ranking and continuation'),
    'adaptive_routing_policies/w7c3': ('anchor_deviation', 'Anchor-and-deviate budget policies'),
    'adaptive_routing_policies/w7d': ('generator_aligned_routing', 'Generator-aligned cross-encoder fidelity routing'),
    'adaptive_routing_policies/w7e': ('multifidelity_representation', 'Multi-fidelity source representation and allocation'),
    'content_aware_allocation/w5c': ('representation_adaptation', 'Representation adaptation and content-aware training diagnostics'),
}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def move(old_rel, name, purpose):
    old = SRC / old_rel
    new = old.with_name(name)
    if old.is_symlink():
        assert old.resolve() == new.resolve(), old
        return None
    assert old.exists() and not new.exists(), old
    paths = [old] if old.is_file() else sorted(p for p in old.rglob('*') if p.is_file() and not p.is_symlink())
    before = [(p, sha(p)) for p in paths]
    old.rename(new)
    old.symlink_to(new.name, target_is_directory=new.is_dir())
    for p, h in before:
        assert sha(p) == h, p
    return dict(old_path=str(old.relative_to(FINAL)), new_path=str(new.relative_to(FINAL)),
                purpose=purpose, compatibility_alias=str(old.relative_to(FINAL)),
                files_preserved=len(before), content_hashes_unchanged=True,
                files=[dict(legacy_path=str(p.relative_to(FINAL)), sha256=h) for p,h in before])

receipt = FINAL / '11_shared_infrastructure/audit/source_name_migration.json'
if receipt.exists():
    raise SystemExit('Migration already recorded; inspect its receipt instead of repeating it.')
records=[]
for old,(new,purpose) in MAP.items():
    row=move(old,new,purpose)
    if row: records.append(row)
for old,(new,purpose) in NESTED.items():
    row=move(old,new,purpose)
    if row: records.append(row)
receipt.write_text(json.dumps(dict(scope='FINAL_PROJECT_MAIN only', architecture_changes=0,
    research_source_byte_changes=0, old_imports_preserved=True, moves=records),indent=2)+'\n')
lines=['# Source code by research purpose', '',
       'The physical folders below are grouped by what the code does. No research Python content was rewritten.', '',
       '**Compatibility:** `week*`, `w7*`, `w5c`, and `post_w12` entries are relative links to the renamed folders. '
       'Keep them: frozen notebooks, source-hash registries, historical paths and Python imports still use those names. '
       'Use the descriptive folders for browsing; keep existing import statements when executing historical experiments. '
       'Do not mix descriptive and legacy import names in one process, since Python can create separate module objects.', '',
       '| Folder | Responsibility | Compatibility name |', '|---|---|---|']
for old,(new,purpose) in MAP.items():
    lines.append(f'| [{new}]({new}) | {purpose} | `{old}` |')
lines += ['', '## Core implementation entry points', '',
    '- [QBGF and baseline evidence selection](budgeted_evidence_fusion/algorithm.py): exact serialization, sentence packing, fidelity options and multiple-choice knapsack.',
    '- [Source segmentation and hierarchy](granularity_study/hierarchy.py): source-exact evidence units.',
    '- [Frozen reader](budgeted_evidence_fusion/reader.py): prompt/token construction and generation.',
    '- [BEA-v1](exploratory_allocation/bea_qbgf/allocator.py): bottom-up marginal allocation.',
    '- [BEA-v2](exploratory_allocation/bea_v2/allocator.py): helpfulness-weighted transitions.',
    '- [Canonical predictor features](exploratory_allocation/bea_v2/data.py): the outcome-free feature schema used in training.',
    '- [Attribution](evidence_attribution/experiment.py) and [confirmation](frozen_confirmation/confirmation_runner.py) retain their distinct protocols.', '',
    '## Adaptive routing subpackages', '', '| Folder | Purpose | Legacy name |', '|---|---|---|']
for old,(new,purpose) in NESTED.items():
    path=str(Path(old).with_name(new))
    lines.append(f'| [{path}]({path}) | {purpose} | `{old}` |')
lines += ['', '## What was deliberately preserved', '',
    'No function, class, model, parameter, algorithm, prompt, split, result, notebook, scoring rule or dependency architecture was changed. '
    'The existing `utils`, `metrics`, `model` and baseline bindings retain their roles. '
    'Method-specific evidence folders elsewhere in this archive still point to the same files through compatibility links. '
    'This is a naming and navigation migration, not a claim that every historical experiment can be rerun from this archive alone.', '',
    'Migration hashes: [source_name_migration.json](../../../audit/source_name_migration.json).']
# SRC is runtime/src; audit is two levels up.
lines[-1] = 'Migration hashes: [source_name_migration.json](../../audit/source_name_migration.json).'
(SRC/'README.md').write_text('\n'.join(lines)+'\n')
for filename in ('README.md','CODE_MAP.md'):
    p=FINAL/filename
    p.write_text(p.read_text()+'\n## Source folders named by purpose\n\nSee [src/README.md](src/README.md) for the descriptive code layout and preserved historical import links.\n')
print(json.dumps(dict(renamed_entries=len(records), preserved_files=sum(r['files_preserved'] for r in records), receipt=str(receipt)),indent=2))
