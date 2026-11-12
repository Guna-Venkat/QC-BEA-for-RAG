"""Chronological names for retained results/scripts; no source or result-byte edits."""
from pathlib import Path
import hashlib,json
F=Path(__file__).resolve().parents[2];RT=F/'11_shared_infrastructure/runtime'
RECEIPT=F/'11_shared_infrastructure/audit/results_scripts_numbering.json'
TOP={
'results':[
 ('week0','01_dataset_diagnostics','W0'),
 ('week2','02_context_budget_surfaces','W2'),
 ('week3','03_context_oracle_analysis','W3'),
 ('week4','04_query_context_allocation','W4'),
 ('week5','05_content_aware_allocation','W5'),
 ('week6','06_passage_routing','W6'),
 ('week7','07_adaptive_routing_policies','W7'),
 ('week11','10_granularity_study','W11'),
 ('week12','11_budgeted_evidence_fusion','W12 validation / attribution / confirmation'),
 ('post_w12','16_exploratory_allocation','POST-W12 BEA and qualitative comparison'),
 ('weekly_reports','17_chronological_reports','Retained historical reports, ordered by original week'),
],
'scripts':[
 ('week0','01_dataset_diagnostics','W0'),
 ('verify_week2.py','02_verify_context_budget_results.py','W2 verification'),
 ('build_week3_notebook.py','03_build_context_oracle_notebook.py','W3 notebook construction'),
 ('generate_final_report.py','03_generate_context_oracle_report.py','W3 oracle report; not the final whole-project report'),
 ('generate_week4_notebook.py','04_build_query_allocation_notebook.py','W4 notebook construction'),
 ('week5','05_content_aware_allocation','W5'),
 ('week6','06_passage_routing','W6'),
 ('week7','07_adaptive_routing_policies','W7'),
 ('week11','10_granularity_study','W11'),
 ('week12','11_budgeted_evidence_fusion','W12 runners / baseline extension / attribution / final confirmation'),
 ('week13','15_confirmation_legacy_entrypoints','Historical week13 confirmation wrapper; naming retained as compatibility'),
]}
NESTED=[
 ('results/07_adaptive_routing_policies/w7b_semantic_budget','01_routing_budget_surfaces','W7-B'),
 ('results/07_adaptive_routing_policies/w7c2_utility_ranking','02_utility_continuation','W7-C2'),
 ('results/11_budgeted_evidence_fusion/qbgf','01_fusion_validation','W12 C / C-EXT / D / H-I'),
 ('results/11_budgeted_evidence_fusion/attribution','02_evidence_attribution','W12 J-K-L'),
 ('results/11_budgeted_evidence_fusion/final_confirmation','03_final_confirmation','W12 M'),
 ('results/16_exploratory_allocation/bea_qbgf','01_bea_v1','POST-W12 BEA-v1'),
 ('results/16_exploratory_allocation/bea_v2','02_bea_v2','POST-W12 BEA-v2 calibration and exploratory comparison'),
 ('results/16_exploratory_allocation/final_case_study','03_qualitative_case_studies','POST-W12 qualitative comparison'),
 ('scripts/05_content_aware_allocation/w5c','01_representation_adaptation','W5-C'),
]
REPORTS=[
 ('week_00','01_dataset_diagnostics','W0'),
 ('week_01','02_baseline_references','W1'),
 ('week_02','03_context_budget_surfaces','W2'),
 ('week_03','04_context_oracle_analysis','W3'),
 ('week_04','05_query_context_allocation','W4'),
 ('week_05','06_content_aware_allocation','W5'),
 ('week_06','07_passage_routing','W6'),
 ('week_07','08_adaptive_routing_policies','W7'),
 ('week_11','09_granularity_study','W11'),
 ('week_12','10_evidence_fusion_and_attribution','W12'),
 ('week_13','11_historical_confirmation','Historical W13 reports'),
]
NESTED += [('results/17_chronological_reports/'+old,new,period) for old,new,period in REPORTS]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if RECEIPT.exists():raise SystemExit('Migration already recorded; no repeat required.')
before={str(p.relative_to(F)):sha(p) for group in TOP for p in (RT/group).rglob('*') if p.is_file()}
records=[]
def move(path,name,period):
 p=RT/path;q=p.with_name(name)
 assert p.exists() and not p.is_symlink() and not q.exists(),p
 p.rename(q);p.symlink_to(q.name,target_is_directory=q.is_dir())
 records.append(dict(previous_path=str(p.relative_to(F)),numbered_path=str(q.relative_to(F)),period=period,compatibility_alias_retained=True))
for group,entries in TOP.items():
 for old,new,period in entries:move(group+'/'+old,new,period)
for old,new,period in NESTED:move(old,new,period)
for rel,h in before.items():assert sha(F/rel)==h,rel
for group,entries in TOP.items():
 text=[f'# {group.capitalize()} in chronological order','',
       'Numbered paths are the reading order. Historical names remain relative compatibility links so existing notebook paths, imports, hashes and configured output locations continue to resolve. No code or result contents were changed.','',
       '| Numbered path | Original phase / purpose | Compatibility name |','|---|---|---|']
 for old,new,period in entries:text.append(f'| [{new}]({new}) | {period} | `{old}` |')
 text+=['','The top-level numbers align with the source guide where the corresponding group exists. Gaps mean this archive has no matching retained folder; they do not imply a new experiment or new data. Shared historical reports appear last.','',
         '## Numbered subgroups','','| Path | Phase / purpose |','|---|---|']
 for old,new,period in NESTED:
  if old.startswith(group+'/'):
   relative=str(Path(old).with_name(new).relative_to(group))
   text.append(f'| [{relative}]({relative}) | {period} |')
 if group=='scripts':text+=['','## Execution caution','',
   'This operation only renames retained script paths. It does not execute or qualify any runner. Keep existing recorded commands through their compatibility names for historical reproduction. Some historical scripts contain original-project absolute paths; numbering does not make them standalone archive executables. No script was run during this reorganization.']
 else:text+=['','## Scientific preservation','',
   'All retained CSV/JSON/figure/report bytes and frozen artifact names remain unchanged. Version directories and scientific identifiers such as `v3` and `W13_FINAL_METHOD_FREEZE.json` keep their meaning and names. This is a navigation change, not a reinterpretation or recomputation of results.']
 (RT/group/'README.md').write_text('\n'.join(text)+'\n')
RECEIPT.write_text(json.dumps(dict(scope='FINAL_PROJECT_MAIN results/scripts only',moves=records,existing_files_checked=len(before),all_existing_bytes_unchanged=True,experiments_executed=0,files=before),indent=2)+'\n')
for name in ['README.md','RESULTS_INDEX.md','CODE_MAP.md']:
 p=F/name
 p.write_text(p.read_text()+'\n## Numbered results and script navigation\n\nSee [results/README.md](results/README.md) and [scripts/README.md](scripts/README.md) for chronological names and preserved compatibility paths.\n')
print(json.dumps(dict(numbered_entries=len(records),existing_files_checked=len(before),all_existing_bytes_unchanged=True)))
