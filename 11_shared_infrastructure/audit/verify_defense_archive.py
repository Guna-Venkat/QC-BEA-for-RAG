"""Offline byte/hash/cohort/navigation checks. No model, retrieval or statistical execution."""
from pathlib import Path
import csv,json,hashlib,ast,re,os,argparse,collections,itertools
from urllib.parse import unquote
O=Path(__file__).resolve().parents[2];R=O.parent;A=O/'11_shared_infrastructure/audit';assert O.name=='FINAL_PROJECT_MAIN'
args=argparse.ArgumentParser(description=__doc__);args.add_argument('--compare-originals',action='store_true');opt=args.parse_args()
M=list(csv.DictReader((O/'PROVENANCE_MANIFEST.csv').open()));P=json.load((A/'source_to_final_paths.json').open());V=json.load((A/'local_code_views.json').open())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(s):return json.load((O/P.get(s,s)).open())
def tab(s):return list(csv.DictReader((O/P.get(s,s)).open()))
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def write(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
C=[]
def check(n,ok,detail=''):C.append(dict(check=n,passed=bool(ok),detail=detail))
check('all canonical source files match manifest SHA',all((O/r['current_final_path']).is_file() and sha(O/r['current_final_path'])==r['sha256'] for r in M),len(M))
if opt.compare_originals:
 rr=[r for r in M if not r['original_repo_path'].startswith(('FINAL_PROJECT_MAIN/','https://','http://'))]
 check('external source comparisons unchanged',all((R/r['original_repo_path']).is_file() and sha(R/r['original_repo_path'])==r['sha256'] for r in rr),len(rr))
# Every file present before this pass survives, including old manifest via its exact backup.
before=read('11_shared_infrastructure/audit/before_defense_inventory.json');actions=read('11_shared_infrastructure/audit/defense_path_plan.json');preserved=[]
retirements=json.load((A/'cleanup_retirements.json').open()) if (A/'cleanup_retirements.json').exists() else []
retired={x['path']:x for x in retirements}
for x in before:
 p=A/'before_defense_provenance.csv' if x['path']=='PROVENANCE_MANIFEST.csv' else O/actions[x['path']]
 if not p.is_file():
  rel=str(p.relative_to(O));receipt=retired.get(rel)
  if not receipt or receipt['sha256']!=x['sha256']:preserved.append(x['path'])
 elif sha(p)!=x['sha256']:preserved.append(x['path'])
check('pre-pass research content preserved; generated-metadata retirement explicitly logged',not preserved,dict(files=len(before),failures=preserved))
notebooks=[r for r in M if r['current_final_path'].endswith('.ipynb')]
check('all notebooks byte-identical to recorded source',all(sha(O/r['current_final_path'])==r['sha256'] for r in notebooks),len(notebooks))
for r in notebooks:json.load((O/r['current_final_path']).open())
check('notebook JSON parses without execution',True,len(notebooks))
links=[p for p in O.rglob('*') if p.is_symlink()]
check('all symlink targets remain inside curated folder',all(p.resolve().is_relative_to(O) for p in links),len(links))
check('all symlink views/compatibility paths resolve',all(p.exists() for p in links),[str(p.relative_to(O)) for p in links if not p.exists()])
syntax=[];sources={r['current_final_path'] for r in M if r['current_final_path'].endswith('.py') and not r['scientific_status'].startswith('PAPER_')}
for p in sources:
 try:ast.parse((O/p).read_text())
 except Exception as e:syntax.append([p,str(e)])
check('copied algorithm/module syntax valid',not syntax,dict(files=len(sources),errors=syntax))
official=[]
for lock in (O/'1_problem_and_baselines/baselines').glob('*/UPSTREAM_SOURCE_LOCK.json'):
 d=json.load(lock.open())
 for r in d['files']:
  p=lock.parent/'upstream_source'/r['path'];data=p.read_bytes()
  official.append(sha(p)==r['sha256'] and hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==r['git_blob_sha'])
check('official baseline source SHA256 and Git blob identities',bool(official) and all(official),len(official))

check('numbered code views preserve exact module bytes',all((O/view).is_symlink() and sha(O/view)==sha(O/P[s]) for s,view in V.items()),len(V))
idx=list(csv.DictReader((A/'code_symbol_index.csv').open()));bad=[]
for x in idx:
 p=O/x['path'];t=ast.parse(p.read_text());sym=x['symbol'].split('.')
 matches=[n for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef)) and n.name==sym[0]]
 if len(sym)==2:matches=[z for n in matches if isinstance(n,ast.ClassDef) for z in n.body if isinstance(z,(ast.FunctionDef,ast.AsyncFunctionDef)) and z.name==sym[1]]
 if not any(n.lineno==int(x['line']) and n.end_lineno==int(x['end_line']) for n in matches):bad.append(x['symbol'])
check('function/class line index matches actual AST',not bad,dict(symbols=len(idx),failures=bad))
loc=read('11_shared_infrastructure/audit/central_method_locators.json')
for x in loc:
 fields=['source','entry','config','nb','result','stats']
 good=all((O/P.get(x[k],x[k])).is_file() for k in fields) and (O/x['g']/'README.md').is_file() and (O/x['g']/'docs/1_equations_to_code.md').is_file()
 check(x['name']+' has main code/runner/config/notebook/result/statistics/README',good,{k:P.get(x[k],x[k]) for k in fields})
f=read('results/week12/W13_FINAL_METHOD_FREEZE.json');sp=read('results/week12/qbgf/v3/protocol/W12_SPLIT_FREEZE.json')
check('final freeze SHA unchanged',sha(O/P['results/week12/W13_FINAL_METHOD_FREEZE.json'])=='d0188a3582d6aead0a3a31f9f15bad9b51a88a6b475b05ac79ae38e58f05366b')
check('split payload and registered hash unchanged',sp['split_hash']==digest({k:v for k,v in sp.items() if k!='split_hash'})=='78f5ace11f9080d05dda12716e634020711182f721ac562dc81d19bad6c1c117')
check('frozen method/model/precision/budgets',f['method']=='FIXED_SENTENCE' and f['tokenizer']['id']=='Qwen/Qwen3-8B' and f['reader']=='BASE_FP16' and f['budgets']==[256,1024] and not f.get('retain_lora',False))
check('exact frozen five confirmation systems',[x[0] for x in f['confirmation_methods']]==['NONE','RAW_SKIP','FIXED_SENTENCE','H3','QBGF_FULL'])
counts=[]
for d,rr in sp['datasets'].items():
 for role,rows in rr.items():counts.append(dict(dataset=d,role=role,queries=len(rows),groups=len({x['group'] for x in rows})))
 for a,b in itertools.combinations(['TRAIN','VAL','CONFIRM'],2):
  check(d+' '+a+'/'+b+' ID and group separation',not {x['query_id'] for x in rr[a]}&{x['query_id'] for x in rr[b]} and not {x['group'] for x in rr[a]}&{x['group'] for x in rr[b]})
 check(d+' freeze confirmation membership',set(f['confirmation_ids'][d])=={x['query_id'] for x in rr['CONFIRM']})
check('QASPER no fresh confirmation',not sp['datasets']['QASPER']['CONFIRM'] and sp['QASPER_TEST_permanently_closed'])
cohort=read('results/post_w12/bea_qbgf/v3/PILOT_COHORT.json')['selected'];pilot={(d,x['query_id']):x for d,rr in cohort.items() for x in rr}
for pre,methods in [('results/post_w12/bea_v2/posthoc_tau8e5/rows/',['FIXED_SENTENCE','QBGF_FULL','BEA_QBGF_V1','BEA_V2']),('W12-POST/results/minilm_reranker/rows/',['MINILM_CE_SENTENCE'])]:
 rr=[read(s) for s in P if s.startswith(pre) and s.endswith('.json')];expected={(d,q,m,b) for d,q in pilot for m in methods for b in [256,1024]}
 check(pre+' exact grid/checksums/budget/group',len(rr)==len(expected) and {tuple(r['key']) for r in rr}==expected and all(r['checksum']==digest(r['row']) and r['row']['evidence_tokens']<=r['key'][3] and r['row']['cluster_id']==pilot[r['key'][0],r['key'][1]]['group'] for r in rr),len(rr))
expanded=read('results/post_w12/bea_qbgf/v3/expanded/EXPANDED_COHORT.json')['selected']
for stage,co in [('pilot',cohort),('expanded',expanded)]:
 pre='results/post_w12/bea_qbgf/v3/'+stage+'/rows/';rr=[read(s) for s in P if s.startswith(pre) and s.endswith('.json')]
 expected={(d,x['query_id'],m,b) for d,qs in co.items() for x in qs for m in ['FIXED_SENTENCE','QBGF_FULL','BEA_QBGF'] for b in [256,1024]}
 check('restored V1 '+stage+' raw grid/checksums',len(rr)==len(expected) and {tuple(r['key']) for r in rr}==expected and all(r['checksum']==digest(r['row']) for r in rr),len(rr))
check('shared exact matched source pool inventory',sum(s.startswith('results/post_w12/bea_qbgf/v3/cache/problems/') for s in P)==150)
rawsource=[read(s) for s in P if s.startswith('results/post_w12/bea_qbgf/v3/cache/problems/')]
check('matched source pool checksums and membership',{tuple(r['key']) for r in rawsource}==set(pilot) and all(r['checksum']==digest(r['row']) for r in rawsource))
folds=read('results/post_w12/bea_v2/v3/CROSSFIT_FOLDS.json')['assignments']
for d,rr in cohort.items():
 grouped=collections.defaultdict(set)
 for x in rr:grouped[x['group']].add(folds[d][x['query_id']])
 check(d+' V2 held-out group isolation',all(len(v)==1 for v in grouped.values()) and set(folds[d])=={x['query_id'] for x in rr})
models=read('results/post_w12/bea_v2/v3/utility_model/MODELS.json')
check('P_help model bundle hashes without loading',all(sha(O/P['results/post_w12/bea_v2/v3/'+p])==h for p,h in models['files'].items()),len(models['files']))
p=read('results/post_w12/bea_qbgf/v3/BEA_QBGF_V1_FREEZE.json')['identity']['parameters']
check('V1 effective frozen hyperparameters documented',p['tau_stop']==.01 and p['tau_expand']==.01 and p['eta_cov']==.5 and p['lambda_red']==.5 and p['tau_context']==.05)
check('V2 termination artifact preserved','CALIBRATION_FAILED_TERMINATED' in str(read('results/post_w12/bea_v2/v3/CALIBRATION_TERMINATED.json')))
r=tab('results/post_w12/bea_v2/v3/calibration/resolution/threshold_summary.csv');check('all four prespecified resolution points ineligible',len(r)==4 and all(x['eligible']=='False' for x in r))
check('post-hoc threshold not silently calibrated',read('W12-POST/bea_v2_posthoc_config.json')['threshold']==8e-5)
r=tab('W12-POST/results/minilm_reranker/analysis/PAIRED_COMPARISONS.csv');check('recorded MiniLM family24 and no Holm discoveries',len(r)==24 and all(float(x['holm_p'])>.05 and int(x['exploratory_family_size'])==24 for x in r))
# Read stored numerical source fields, without recalculating task metrics or bootstrap statistics.
x=read('results/week2/processed/oracle_vs_static_summary.json');check('early defense scalars have machine evidence',x['n_questions']==231 and x['mean_static_sara_k8_f1']==.395 and x['mean_oracle_sara_f1']==.5008)
gen=read('results/week12/qbgf/v3/protocol/protocol_config.json')['generation'];check('documented generation caps match frozen config',gen['max_context']==8192 and gen['max_new_tokens_qa']==128 and gen['max_new_tokens_verification']==16 and not gen['do_sample'])
# Only current authored navigation is checked; historical source prose is intentionally untouched.
sourcepaths={r['current_final_path'] for r in M};bad=[];nlinks=0;docs=[]
for p in O.rglob('*.md'):
 rel=str(p.relative_to(O))
 if p.is_symlink() or rel in sourcepaths or rel.startswith(('12_report_support/previous_navigation/','11_shared_infrastructure/audit/previous_pass/','11_shared_infrastructure/previous_interface_docs/')):continue
 docs.append(rel)
 for target in re.findall(r'\]\(([^\n)]+)\)',p.read_text()):
  t=unquote(target.split('#')[0])
  if not t or re.match(r'[a-zA-Z]+://',t) or t.startswith('mailto:'):continue
  nlinks+=1
  if not (p.parent/t).exists():bad.append(dict(document=rel,target=target))
check('all current defense/navigation links resolve',not bad,dict(documents=len(docs),links=nlinks,broken=bad))
check('no unresolved function placeholders in current maps',all('UNRESOLVED symbol' not in (O/p).read_text() for p in docs))
# Missing historical outputs are stated honestly; absence is a limit, not a fabricated success.
missing=[]
for s in ['results/week12/qbgf/v3/validation/C/rows','results/week12/qbgf/v3/validation/D/rows','results/week12/final_confirmation/v1/rows','results/week12/attribution/v1/perturbations']:
 p=R/s;missing.append(dict(original_path=s,exists=p.exists(),files=sum(q.is_file() for q in p.rglob('*')) if p.exists() else 0))
write(A/'defense_checks.json',C);write(A/'cohort_counts.json',counts);write(A/'unavailable_original_outputs.json',missing)
failed=[c for c in C if not c['passed']];summary=dict(checks=len(C),passed=len(C)-len(failed),failed=failed,notebooks_preserved=len(notebooks),code_source_files=len(sources),code_views=len(V),source_records=len(M),function_symbols=len(idx),navigation_links=nlinks,restored_source_records=len(list(csv.DictReader((A/'restored_defense_artifacts.csv').open()))),experiments_executed=0,algorithm_logic_changes=0,notebook_content_changes=0)
write(A/'defense_verification_summary.json',summary)
# Final A–K report, with exact first-open locations and remaining limits.
def link(s,label=None):
 p=P.get(s,s);return '['+(label or Path(p).name)+']('+p.replace(' ','%20')+')'
rows=[]
for x in loc:
 rows.append('| '+x['name']+' | '+link(V.get(x['source'],P[x['source']]))+' | '+link(x['result'])+' | '+link(x['nb'])+' |')
text='''# Defense-readiness reorganization report

## A. Structure

```text
FINAL_PROJECT_MAIN/
├── CODE_MAP.md / NOTEBOOK_MAP.md / ALGORITHM_DEFENSE_GUIDE.md
├── RESULTS_INDEX.md / IMPORTANT_NUMBERS.md
├── DATASET_AND_EXPERIMENT_SETUP.md
├── 1_problem_and_baselines/
├── 2_adaptive_evidence_quantity/
├── 3_evidence_identity_and_routing/
├── 4_multigranular_evidence_study/
├── 5_qbgf/
├── 6_downstream_utility_attribution/
├── 7_bea_v1/
├── 8_bea_v2/
├── 9_minilm_reranker/
├── 10_final_method_comparison/
├── 11_shared_infrastructure/
└── 12_report_support/
```

Methods expose code/configs/notebooks/results/docs and figures where available. The source package layout is canonical under11_shared_infrastructure/runtime; local numbered code files are internal links to it, not invented algorithm splits.

## B–E. Major moves, code/results and notebooks

Motivation and SARA parent references were combined into1. Earlier week-first experiments map to2–4. QBGF validation/ablation/freeze/confirmation is in5. Attribution/V1/V2/MiniLM/final comparison are in6–10. Shared source/env/audit records and historical report support are11–12.

Examples of canonical code movement:

- shared/runtime/src/week12/algorithm.py →11_shared_infrastructure/runtime/src/week12/algorithm.py; defense view5_qbgf/code/1_qbgf_and_sentence_allocator.py.
- shared/runtime/src/post_w12/bea_qbgf/allocator.py →11_shared_infrastructure/runtime/src/post_w12/bea_qbgf/allocator.py; defense view7_bea_v1/code/1_dynamic_marginal_allocator.py.
- shared/runtime/src/post_w12/bea_v2/models.py →11_shared_infrastructure/runtime/src/post_w12/bea_v2/models.py; defense view8_bea_v2/code/2_group_crossfit_phelp_models.py.
- shared/runtime/W12-POST/reranker_baseline/minilm_reranker.py →11_shared_infrastructure/runtime/W12-POST/reranker_baseline/minilm_reranker.py; defense view9_minilm_reranker/code/1_cross_encoder_sentence_reranker.py.

Key results were numbered in reading order: QBGF validation summary, query-conditioning/primary contrasts, sentence/passage fusion comparisons, frozen policy and reserved confirmation; V1 pilot/expansion/efficiency; V2 predictor metrics/calibration failure/post-hoc reader outcomes; MiniLM quality and final matched quality/efficiency/statistics/winner metadata.

The full actual old→new path and hash log is [defense_reorganization_actions.csv](11_shared_infrastructure/audit/defense_reorganization_actions.csv). It supplies the exact mapping for every moved artifact, including original report/notebook names. No scientific CSV was filtered/rebuilt to imitate a requested filename. Multi-method tables retain all original rows and precision.

Notebook locations and original paths are listed in [NOTEBOOK_MAP.md](NOTEBOOK_MAP.md) and its machine-readable inventory. All original notebook cells, flags, outputs and bytes are unchanged. The final comparison notebook is the same canonical MiniLM notebook, linked from10 for convenience.

## F. Restored missing evidence

Real V1 pilot/expanded query rows and exact150matched source pools were copied read-only from their original results/post_w12/bea_qbgf/v3 namespaces. Pilot/expanded rows live under7_bea_v1/results/5_query_level; matched source pools under11_shared_infrastructure/data/matched_source_pools. Every original/new path, reason and SHA is in [restored_defense_artifacts.csv](11_shared_infrastructure/audit/restored_defense_artifacts.csv). No model/retrieval/statistical result was regenerated.

## G–H. Open these first

| Method | Primary implementation view | Primary stored result | Notebook |
| --- | --- | --- | --- |
'''+ '\n'.join(rows)+'''

Equation→function→line maps are under each central method’s docs/1_equations_to_code.md. CODE_MAP is the quick reference; ALGORITHM_DEFENSE_GUIDE explains equations, steps, complexity, hyperparameters, strengths, limits and forbidden claims. IMPORTANT_NUMBERS contains recorded source-linked defense tables.

## H2. Baseline references and cleanup

Official licensed SARA, RECOMP and LLMLingua source subsets are pinned under1_problem_and_baselines/baselines. Their source hashes/Git blob identities and repository/tree commits are verified separately. Project adaptations and result links are separate from published paper results. RECOMP was not a matched project evaluation; LLMLingua-2 qualification is not a full W12 quality result.

Obsolete generated navigation/audit copies were retired with pre-deletion hashes/reasons in cleanup_retirements.json. Research records, notebooks and fold predictors were not deleted. A local .gitignore excludes regenerable caches and large external checkpoints, not scientific result tables or query-level rows. The parent folder remains ignored by the outer repository until that outer rule is changed separately.

See [CLEANUP_AND_BASELINES_REPORT.md](CLEANUP_AND_BASELINES_REPORT.md) and the [baseline library](1_problem_and_baselines/baselines/README.md).

## I. Remaining problems

Full original W12 C/D validation row directories, reserved-confirmation answer rows and attribution perturbation/generation outputs are missing. Recorded aggregate tables, statistical outputs, original reconstruction/closeout receipts and checksum inventories remain. A code view cannot repair missing historical evidence; independent raw rescoring is blocked until a genuine backup is restored.

External corpora, pinned reader/retriever weights, adapted SARA checkpoint/projector and the historical environment/source revision are not a complete portable bundle. Guarded archived notebooks are not guaranteed fresh launchers; many saved full/install flags are alreadyTrue. Obsolete generated guides/audit generations were removed with explicit retirement receipts; retained source reports can embed historical paths. Current navigation and verifier supersede old instructions.

No central algorithm ownership was invented: method-local files reference their actual shared modules. Byte-identity deduplication is not a claim of statistical/experimental equivalence. No unresolved distinct-result duplicate was silently merged in this pass.

## J. Safety and verification

No files outside FINAL_PROJECT_MAIN were modified, renamed, moved or deleted. Algorithm equations, parameters, tie behavior, datasets, metrics, statistics, prompts, token budgets and result bytes were not changed. Notebooks were not edited or executed. No model, retrieval, calibration, training or statistical experiment ran.

'''+f"Checks passed: **{summary['passed']}/{summary['checks']}**; notebook source hashes preserved: **{summary['notebooks_preserved']}**; source Python files syntax checked: **{summary['code_source_files']}**; real numbered code views: **{summary['code_views']}**; function/class symbols indexed: **{summary['function_symbols']}**; navigation links checked: **{summary['navigation_links']}**. Detailed checks: [defense_verification_summary.json](11_shared_infrastructure/audit/defense_verification_summary.json).\n\n"+'''
## K. Assessment

**NO for unconditional readiness as the sole evidence repository for all four requested purposes**, because independent defense of missing historical raw outputs remains limited.

- Presentation navigation: ready, with scientific-status/cohort caveats.
- Code explanation: ready for inspected central algorithms; exact modules/functions/equations are mapped.
- Final report: ready to write a carefully scoped report from recorded sources, explicitly disclosing raw-output gaps.
- Results defense: recorded tables/statistics can be shown and matched exploratory rows verified; full original W12/confirmation row-level verification remains incomplete.

The navigation problem is addressed. Missing historical evidence was documented rather than fabricated.
'''
(O/'DEFENSE_READINESS_REPORT.md').write_text(text)
# Ensure final report links too, before emitting complete file-integrity snapshot.
for t in re.findall(r'\]\(([^\n)]+)\)',text):
 if not (O/unquote(t.split('#')[0])).exists():raise ValueError('Final report link missing: '+t)
with (A/'file_integrity.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['path','bytes','sha256']);w.writeheader()
 for p in sorted(O.rglob('*')):
  if p.is_file() and not p.is_symlink() and p!=A/'file_integrity.csv':w.writerow(dict(path=str(p.relative_to(O)),bytes=p.stat().st_size,sha256=sha(p)))
print(json.dumps(summary,indent=2))
if failed:raise SystemExit('Metadata checks failed; inspect the detailed audit before declaring readiness.')
