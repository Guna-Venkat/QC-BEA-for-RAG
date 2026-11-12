"""Number final-archive source paths chronologically; preserve all Python bytes/imports."""
from pathlib import Path
import hashlib,json
F=Path(__file__).resolve().parents[2]
S=F/'11_shared_infrastructure/runtime/src'
RECEIPT=F/'11_shared_infrastructure/audit/source_numbering.json'
GROUPS=[
 ('dataset_diagnostics','01_dataset_diagnostics','W0'),
 ('context_budget_surfaces','02_context_budget_surfaces','W2'),
 ('context_oracle_analysis','03_context_oracle_analysis','W3'),
 ('query_context_allocation','04_query_context_allocation','W4'),
 ('content_aware_allocation','05_content_aware_allocation','W5'),
 ('passage_routing','06_passage_routing','W6'),
 ('adaptive_routing_policies','07_adaptive_routing_policies','W7'),
 ('evidence_representation','08_evidence_representation','W9'),
 ('reader_diagnostics','09_reader_diagnostics','W10'),
 ('granularity_study','10_granularity_study','W11'),
 ('budgeted_evidence_fusion','11_budgeted_evidence_fusion','W12 core / C-D'),
 ('baseline_comparisons','12_baseline_comparisons','W12 C-EXT'),
 ('final_method_review.py','13_final_method_review.py','W12 H-I freeze'),
 ('evidence_attribution','14_evidence_attribution','W12 J-K-L'),
 ('frozen_confirmation','15_frozen_confirmation','W12 M'),
 ('exploratory_allocation','16_exploratory_allocation','POST-W12'),
 ('utils','17_shared_utilities','Shared support; not a new week'),
]
NESTED=[
 ('07_adaptive_routing_policies/modular_routing','01_modular_routing','W7-A'),
 ('07_adaptive_routing_policies/routing_budget_surfaces','02_routing_budget_surfaces','W7-B'),
 ('07_adaptive_routing_policies/semantic_sufficiency','03_semantic_sufficiency','W7-C'),
 ('07_adaptive_routing_policies/utility_continuation','04_utility_continuation','W7-C2'),
 ('07_adaptive_routing_policies/anchor_deviation','05_anchor_deviation','W7-C3'),
 ('07_adaptive_routing_policies/generator_aligned_routing','06_generator_aligned_routing','W7-D'),
 ('07_adaptive_routing_policies/multifidelity_representation','07_multifidelity_representation','W7-E'),
 ('05_content_aware_allocation/representation_adaptation','01_representation_adaptation','W5-C'),
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if RECEIPT.exists():raise SystemExit('Numbering already recorded; no repeat migration needed.')
# Snapshot existing source bytes through their current descriptive paths.
files=[p for p in S.rglob('*') if p.is_file() and not p.is_symlink() and p.suffix=='.py']
before={str(p.relative_to(F)):sha(p) for p in files}
records=[]
for old,new,period in GROUPS+NESTED:
 p=S/old;q=p.with_name(new)
 assert p.exists() and not p.is_symlink() and not q.exists(),p
 p.rename(q);p.symlink_to(q.name,target_is_directory=q.is_dir())
 records.append(dict(previous_path=str(p.relative_to(F)),numbered_path=str(q.relative_to(F)),period=period,compatibility_alias_retained=True))
for p,h in before.items():assert sha(F/p)==h,p
# Update only the authored navigation document, not scientific source/documents.
r=S/'README.md';text=r.read_text()
text=text.replace('# Source code by research purpose','# Source code in chronological order')
text=text.replace('The physical folders below are grouped by what the code does. No research Python content was rewritten.',
 'The physical folders below are numbered in week order and named by research purpose. Two-digit prefixes keep file-browser sorting correct. No research Python content was rewritten.')
# Longer nested path strings first, so links can then receive the top-level prefix.
for old,new,period in NESTED:
 name=Path(old).name
 text=text.replace(name,new)
for old,new,period in sorted(GROUPS,key=lambda x:len(x[0]),reverse=True):
 # Avoid replacing a partial Python identifier such as the word "utils" in prose.
 text=text.replace('['+old+']','['+new+']').replace('('+old+')','('+new+')').replace('('+old+'/', '('+new+'/')
 text=text.replace('`'+old+'`','`'+new+'`')
 # Nested table rows show composite source paths.
 text=text.replace('['+old+'/', '['+new+'/')
text += '\n## Numbered reading order\n\n| Order / path | Original phase |\n|---|---|\n'
for old,new,period in GROUPS:text+=f'| [{new}]({new}) | {period} |\n'
text += '\nWeek 1 baseline code remains in the archive’s Baselines binding and baseline library; absent week packages were not invented. '
text += 'Numbering is a reading order, not a change to the experiment protocol. The W12 freeze review precedes attribution and final confirmation. '
text += 'Old descriptive names and week names are import/navigation aliases; keep them. Numbered paths are intended for browsing, while historical Python imports stay unchanged.\n'
r.write_text(text)
RECEIPT.write_text(json.dumps(dict(scope='FINAL_PROJECT_MAIN/src only; no demo/src exists',moves=records,python_files_checked=len(before),source_bytes_unchanged=True,imports_preserved=True,files=before),indent=2)+'\n')
print(json.dumps(dict(numbered_entries=len(records),source_files_checked=len(before),source_bytes_unchanged=True)))
