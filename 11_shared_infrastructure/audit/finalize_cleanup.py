"""Finalize cleanup metadata/docs only. No experiments and no writes outside final folder."""
from pathlib import Path
import json,hashlib,csv,os
O=Path(__file__).resolve().parents[2];A=O/'11_shared_infrastructure/audit';assert O.name=='FINAL_PROJECT_MAIN'
M=list(csv.DictReader((O/'PROVENANCE_MANIFEST.csv').open()));paths={x['current_final_path'] for x in M}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
retire=json.load((A/'cleanup_retirements.json').open());seen={x['path'] for x in retire};temp=[]
for p in (A/'cleanup_review').rglob('*'):
 if p.is_file() and not p.is_symlink():
  rel=str(p.relative_to(O));assert rel not in paths
  x=dict(path=rel,sha256=sha(p),bytes=p.stat().st_size,reason='Temporary paper-text extraction/render/download; final unchanged paper PDFs preserved in baseline folders')
  if rel not in seen:retire.append(x)
  temp.append(p)
(A/'cleanup_retirements.json').write_text(json.dumps(retire,indent=2)+'\n')
for p in temp:p.unlink()
for p in sorted((A/'cleanup_review').rglob('*'),key=lambda p:len(p.parts),reverse=True):
 if p.is_dir() and not p.is_symlink():p.rmdir()
if (A/'cleanup_review').exists():(A/'cleanup_review').rmdir()
summary=json.load((A/'cleanup_summary.json').open());summary['temporary_review_files_removed']=len(temp);summary['total_retirement_records']=len(retire)
(A/'cleanup_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
# Explicit upstream limitations retain provenance rather than silently repairing official source.
base=O/'1_problem_and_baselines/baselines'
(base/'UPSTREAM_LIMITATIONS.md').write_text('''# Reference-source limitations

Official snapshots are pinned, licensed subsets, not bundled datasets/weights or proof of a working installed environment. Full upstream examples/images/data may not be included; use the original repository links for those reference-only assets.

The pinned SARA snapshot contains a pre-existing syntax error in src/visual/plot_generalization_base_model.py around line94. It is an ancillary plotting file, not a tested project allocator or the SARA CLI. Its source was preserved exactly and the finding recorded in baseline_upstream_checks.json. It was not silently repaired or presented as a successful reproduction. RECOMP and selected LLMLingua source parse statically; no dependency imports/models/evaluations were run.

Three distinct identities must remain separate: published paper version, pinned current official reference source, and project execution adaptation/checkpoint. Equal source-file bytes do not establish equal evaluated systems. Original code licenses apply to code; paper copyrights and model/dataset terms remain their own.
''')
report='''# Cleanup and baseline-library report

All changes are confined to **FINAL_PROJECT_MAIN/**. The original repository and its outer .gitignore are untouched. No model was loaded, no environment installed, and no experiment/statistical result was generated.

## Cleanup

- Removed45superseded generated navigation/audit/interface files:2,781,283bytes (~2.65MiB). These were absent from the scientific provenance manifest; pre-deletion path/hash/reason receipts are retained.
- Removed temporary paper extraction/render/download intermediates after copying the final unchanged papers into the baseline library.
- Preserved scientific source, all50original notebooks, query-level rows, source pools, fold models, figures, result/statistics tables, frozen splits and current provenance/action logs.
- Moved59SARA parent configs from the generic configs list into baselines/1_sara/project_adaptation/configs, preserving contents and rewiring internal references. This cleans navigation without discarding reference configurations.
- Most of the archive’s remaining size is essential evidence, not a disposable cache. No large scientific data folder was deleted or hidden wholesale.

Exact removals: [cleanup_retirements.json](11_shared_infrastructure/audit/cleanup_retirements.json). Config moves: [baseline_config_moves.json](11_shared_infrastructure/audit/baseline_config_moves.json).

## Baseline organization

[Open the baseline library](1_problem_and_baselines/baselines/README.md).

| Baseline | Original source/reference | Project integration/results |
| --- | --- | --- |
| SARA | Official Ahren09/SARA pinned source, license, unchanged paper, literature-only Table1 excerpt | Preserved adaptation/loader, specialist runner, real2010query-level BM25/SFR k5/n10 records; QASPER adapted-Mistral specialist, not matched Qwen256/1024 |
| RECOMP | Official carriex/recomp source, license, unchanged ICLR paper, literature-only Table2 excerpt | No matched project evaluation; no invented score |
| LLMLingua-2 | Official microsoft/LLMLingua v0.2.2 source, license, unchanged ACL paper | Actual project compressor wrapper and smaller-mBERT qualification receipt; no full W12 quality/confirmation result |
| BM25/SFR RAG controls | Actual project retrieval, RAW_SKIP/sentence/hierarchy code and frozen config | Recorded merged validation and paired-extension tables; explicitly budget-matched RAW_SKIP |
| MiniLM | Official checkpoint reference and one canonical project implementation | Links to matched exploratory quality/efficiency/statistics; no duplicate implementation |

Each external baseline has README, upstream_source, UPSTREAM_SOURCE_LOCK.json, original license and an isolated PAPER_RESULTS_REFERENCE.md. Published-paper values remain literature references, not project benchmark rows. See [baseline results index](1_problem_and_baselines/baselines/BASELINE_RESULTS_INDEX.md).

Pinned source commits:

- SARA:639f5f48b86672c270046141f44a1b5eab6c8b96.
- RECOMP:51d4432151efb3275257a9407dc71d1e5ec6634d.
- LLMLingua:v0.2.2 /a411a3fa61df74411157b2512b592d5357bd8f17.

All203selected upstream source/config/license files were checked against SHA256 and Git blob IDs. Saved tree-hash metadata was corrected from commit IDs to actual Git tree IDs, retaining the previous value for audit. The official SARA ancillary plotting-file syntax issue is recorded, not fixed or hidden. Current source snapshots are not asserted to be historical execution revisions.

## Local .gitignore

[FINAL_PROJECT_MAIN/.gitignore](.gitignore) excludes regenerable Python/test/notebook caches, local environments, large external checkpoint/embedding-database files and temporary review output. It deliberately keeps scientific CSV/JSON/query results, frozen identities, notebooks, figures, provenance and *.joblib predictors visible.

The parent repository currently ignores the entire final folder. A nested .gitignore cannot override that outer exclusion. This task leaves the outer file unchanged; lifting that exclusion later is a separate action.

## Verification and remaining limits

The current metadata verifier checks source preservation, moved links, notebooks, frozen identities, matched rows, model hashes, official source blob identities and active navigation. Details are in [defense_verification_summary.json](11_shared_infrastructure/audit/defense_verification_summary.json). No claim of full execution/testing of imported models is made.

Missing historical W12 validation/confirmation raw outputs and attribution perturbation receipts remain unresolved. External model weights/data/environment remain external. Cleanup does not manufacture missing historical evidence or make the archive a complete independent reproduction bundle.
'''
for a,b in [('Removed45','Removed 45'),('all50','all 50'),('Moved59','Moved 59'),('real2010query-level','real 2,010 query-level'),('All203selected','All 203 selected'),('SARA:639','SARA: 639'),('RECOMP:51','RECOMP: 51'),('LLMLingua:v','LLMLingua: v')]:report=report.replace(a,b)
(O/'CLEANUP_AND_BASELINES_REPORT.md').write_text(report)
(O/'CLEANUP_LOG.md').write_text('# Cleanup log\n\nSee [CLEANUP_AND_BASELINES_REPORT.md](CLEANUP_AND_BASELINES_REPORT.md), [retirement receipts](11_shared_infrastructure/audit/cleanup_retirements.json), and [config move map](11_shared_infrastructure/audit/baseline_config_moves.json). Only generated redundant metadata/temporary files were deleted; scientific sources/results were preserved. No files outside FINAL_PROJECT_MAIN changed.\n')
for name,add in [
 ('README.md','\nBaseline references, project adapters/results and local ignore policy are documented in [CLEANUP_AND_BASELINES_REPORT.md](CLEANUP_AND_BASELINES_REPORT.md) and the [baseline library](1_problem_and_baselines/baselines/README.md).\n'),
 ('CODE_MAP.md','\n## Original baseline sources and project integrations\n\nSee the [baseline library](1_problem_and_baselines/baselines/README.md) for pinned SARA/RECOMP/LLMLingua source, original licenses/papers, project adapters and recorded results. Official source snapshots are reference artifacts, not substitutions for the evaluated project implementation.\n'),
 ('RESULTS_INDEX.md','\n## Original baselines and recorded baseline outcomes\n\n[Baseline results index](1_problem_and_baselines/baselines/BASELINE_RESULTS_INDEX.md) links actual matched RAG and specialist SARA records. Published-paper outcomes are isolated in per-baseline PAPER_RESULTS_REFERENCE.md files; RECOMP and qualified-only LLMLingua do not receive invented project scores.\n'),
 ('REORGANIZATION_LOG.md','\nThe final cleanup retired superseded generated guides/audits and moved parent-SARA configs beside its baseline. Exact retirement/move receipts and source-reference validation are recorded in CLEANUP_AND_BASELINES_REPORT.md. Current scientific artifacts were not removed.\n')]:
 p=O/name;text=p.read_text()
 if add.strip() not in text:p.write_text(text+add)
# Rewrite the current dependency note to remove references to deleted old generators.
p=O/'DEPENDENCY_AUDIT.md';s=p.read_text().replace('Historical migration/verification scripts are archived underaudit/previous_pass and12_report_support/previous_navigation; do not run obsolete paths after reorganizing. Use the new verifier only for metadata.', 'Superseded generated navigation/audit generations were removed with explicit retirement receipts. Use the current verifier for metadata only.')
s+='\nOfficial baseline source is pinned and verified separately; see [upstream limitations](1_problem_and_baselines/baselines/UPSTREAM_LIMITATIONS.md). Third-party reference code is not a claim of successful installation or reproduced paper performance.\n' if 'UPSTREAM_LIMITATIONS.md' not in s else ''
p.write_text(s)
print('Final cleanup report and baseline navigation complete.')
