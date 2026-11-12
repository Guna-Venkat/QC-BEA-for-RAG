"""Conservative in-folder cleanup and baseline documentation; no experiments."""
from pathlib import Path
import csv,json,hashlib,os,shutil,re,ast
from urllib.parse import unquote
O=Path(__file__).resolve().parents[2];R=O.parent;A=O/'11_shared_infrastructure/audit';B=O/'1_problem_and_baselines/baselines';assert O.name=='FINAL_PROJECT_MAIN'
M=list(csv.DictReader((O/'PROVENANCE_MANIFEST.csv').open()));P=json.load((A/'source_to_final_paths.json').open());sourcepaths={r['current_final_path'] for r in M}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def put(p,t):p=O/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t.rstrip()+'\n')
def link(s,title=None,doc='README.md'):
 q=P.get(s,s);return '['+(title or Path(q).name)+']('+os.path.relpath(O/q,(O/doc).parent).replace(' ','%20')+')'
def alias(path,source):
 p=O/path;t=O/P.get(source,source);p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():p.symlink_to(os.path.relpath(t,p.parent))
 return path
# Log before removal. These paths contain generated old navigation/metadata only.
retire=[]
for stem in ['12_report_support/previous_navigation','11_shared_infrastructure/audit/previous_pass','11_shared_infrastructure/previous_interface_docs']:
 for p in (O/stem).rglob('*'):
  if not p.is_file() or p.is_symlink():continue
  rel=str(p.relative_to(O));assert rel not in sourcepaths,('Scientific manifest artifact cannot be removed',rel)
  retire.append(dict(path=rel,sha256=sha(p),bytes=p.stat().st_size,reason='Superseded generated navigation/audit metadata; current manifest, defense maps and detailed action logs retained'))
# Disposable caches only, never raw results or fold models.
for p in O.rglob('*'):
 if p.is_dir() and not p.is_symlink() and p.name in ['__pycache__','.pytest_cache','.ipynb_checkpoints','.ruff_cache','.mypy_cache']:
  for q in p.rglob('*'):
   if q.is_file() and not q.is_symlink() and str(q.relative_to(O)) not in sourcepaths:retire.append(dict(path=str(q.relative_to(O)),sha256=sha(q),bytes=q.stat().st_size,reason='Regenerable interpreter/test/editor cache'))
receipt=A/'cleanup_retirements.json'
if receipt.exists():
 old=json.load(receipt.open());prior={x['path']:x for x in old};prior.update({x['path']:x for x in retire});retire=list(prior.values())
write(receipt,retire)
put('CLEANUP_LOG.md','# Cleanup record\n\nOnly FINAL_PROJECT_MAIN is modified. Superseded generated documentation/audit copies and disposable caches are retired only after checking they are absent from the scientific provenance manifest. Every removed path/hash/reason is logged in11_shared_infrastructure/audit/cleanup_retirements.json before removal. Current provenance, rename logs, frozen splits, notebooks, scientific source, fold predictors, query rows and statistics are retained. Official reference snapshots remain separate from project adaptations even when some files have identical bytes.\n')
for x in retire:
 p=O/x['path']
 if p.exists():assert not p.is_symlink() and sha(p)==x['sha256'];p.unlink()
for stem in ['12_report_support/previous_navigation','11_shared_infrastructure/audit/previous_pass','11_shared_infrastructure/previous_interface_docs']:
 for p in sorted((O/stem).rglob('*'),key=lambda p:len(p.parts),reverse=True):
  if p.is_dir() and not p.is_symlink():
   try:p.rmdir()
   except OSError:pass
 try:(O/stem).rmdir()
 except OSError:pass
# Move parent reference config clutter beside its own baseline; keep source bytes.
config_moves={}
for r in M:
 s=r['original_repo_path'];old=r['current_final_path']
 if s.startswith('Baselines/SARA-main/config/') and old.startswith('1_problem_and_baselines/configs/'):
  config_moves[old]='1_problem_and_baselines/baselines/1_sara/project_adaptation/configs/'+s.split('/config/',1)[1]
syms=[(p,p.resolve()) for p in O.rglob('*') if p.is_symlink()]
for old,new in config_moves.items():
 p=O/old;q=O/new;q.parent.mkdir(parents=True,exist_ok=True)
 if p!=q:
  if p.exists():
   if q.exists():assert sha(q)==sha(p);p.unlink()
   else:p.rename(q)
  else:assert q.is_file(),('Missing moved config',old,new)
for p,target in syms:
 rel=str(target.relative_to(O))
 if rel in config_moves:
  p.unlink();p.symlink_to(os.path.relpath(O/config_moves[rel],p.parent))
# Update authored links only; original scientific source Markdown stays byte-exact.
for p in O.rglob('*.md'):
 if p.is_symlink() or str(p.relative_to(O)) in sourcepaths or '/upstream_source/' in str(p.relative_to(O)):continue
 text=p.read_text()
 def replace(m):
  raw=m[1];t=unquote(raw.split('#')[0]);q=(p.parent/t).resolve(strict=False)
  try:rel=str(q.relative_to(O))
  except ValueError:return m[0]
  return ']('+os.path.relpath(O/config_moves[rel],p.parent).replace(' ','%20')+')' if rel in config_moves else m[0]
 updated=re.sub(r'\]\(([^\n)]+)\)',replace,text)
 if updated!=text:p.write_text(updated)
for r in M:
 if r['current_final_path'] in config_moves:
  r['pre_baseline_cleanup_path']=r['current_final_path'];r['current_final_path']=config_moves[r['current_final_path']];r['new_filename']=Path(r['current_final_path']).name;r['renamed_inside_final_main']=r['new_filename']!=r['original_filename']
 else:r['pre_baseline_cleanup_path']=''
P={r['original_repo_path']:r['current_final_path'] for r in M}
plan=json.load((A/'defense_path_plan.json').open());write(A/'defense_path_plan.json',{s:config_moves.get(d,d) for s,d in plan.items()})
write(A/'baseline_config_moves.json',config_moves)
# Register official code and preserved paper sources without pretending they generated project scores.
registered=set(P)
def register(src,dst,method,reason,status='PAPER_UPSTREAM_REFERENCE_NOT_PROJECT_RESULT'):
 if src in registered:return
 p=O/dst;assert p.is_file();r={k:'' for k in M[0]};r.update(current_final_path=dst,original_repo_path=src,original_filename=Path(src).name,new_filename=p.name,conceptual_group='1_problem_and_baselines',chronological_phase='PAPER_REFERENCE',method=method,scientific_status=status,reason_included=reason,sha256=sha(p),copied_exactly_from_source=True,renamed_inside_final_main=Path(src).name!=p.name,notes='Reference-only artifact; not a historical project-run implementation identity or benchmark result.',report_status='OFFICIAL_REFERENCE_SOURCE')
 M.append(r);P[src]=dst;registered.add(src)
checks=[]
trees={'1_sara':'ba245c46f46dc9e3f997c5e0d87c68c6fa768f33','2_recomp':'8d28ac466cd4751fae0f413f8458289731110e1d','3_llmlingua2':'c3d07a0d2c64c4ce179413870f371d3ba375a378'}
for lock in sorted(B.glob('*/UPSTREAM_SOURCE_LOCK.json')):
 d=json.load(lock.open());assert d['repository'] in ['https://github.com/Ahren09/SARA','https://github.com/carriex/recomp','https://github.com/microsoft/LLMLingua']
 # Correct the saved tree identity from GitHub git/commits/<pinned commit>, retain old value.
 if d['source_tree_sha']!=trees[lock.parent.name]:
  d['previous_recorded_source_tree_sha']=d['source_tree_sha'];d['source_tree_sha']=trees[lock.parent.name]
  d['tree_identity_verified_against']=d['repository'].replace('https://github.com/','https://api.github.com/repos/')+'/git/commits/'+d['commit'];d['tree_identity_checked_on']='2026-11-07';write(lock,d)
 failures=[];syntax=[]
 for x in d['files']:
  p=lock.parent/'upstream_source'/x['path'];b=p.read_bytes()
  if sha(p)!=x['sha256'] or hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=x['git_blob_sha']:failures.append(x['path'])
  if p.suffix=='.py':
   try:ast.parse(b.decode())
   except SyntaxError as e:syntax.append(dict(path=x['path'],line=e.lineno,error=e.msg))
  register(x['url'],str(p.relative_to(O)),lock.parent.name,'Official licensed source, pinned commit and Git blob identity; not installed or executed')
 check=dict(baseline=lock.parent.name,repository=d['repository'],commit=d['commit'],git_tree=d['source_tree_sha'],files=len(d['files']),content_hash_and_git_blob_failures=failures,reference_source_syntax_findings=syntax,license_files=d['license_files']);checks.append(check)
 assert not failures
write(A/'baseline_upstream_checks.json',checks)
# Paper copies are exact source artifacts; copyright remains with their original owners.
papers=[('Baselines/papers/SARA.pdf','1_sara','sara_arxiv_2507_05633_v1.pdf'),('Baselines/papers/ICLR-2024-recomp-improving-retrieval-augmented-lms-with-context-compression-and-selective-augmentation-Paper-Conference.pdf','2_recomp','recomp_iclr_2024.pdf')]
for src,folder,name in papers:
 dst='1_problem_and_baselines/baselines/'+folder+'/paper/'+name;q=O/dst;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/src,q);assert sha(q)==sha(R/src);register(src,dst,folder,'Original locally supplied paper retained verbatim for literature-result provenance','PAPER_REFERENCE_NOT_PROJECT_RESULT')
src='https://aclanthology.org/2024.findings-acl.57.pdf';dst='1_problem_and_baselines/baselines/3_llmlingua2/paper/llmlingua2_acl_findings_2024.pdf';q=O/dst;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(A/'cleanup_review/llmlingua2_paper.pdf',q);register(src,dst,'LLMLINGUA2','Official ACL Anthology paper for reference, not a new project result','PAPER_REFERENCE_NOT_PROJECT_RESULT')
with (O/'PROVENANCE_MANIFEST.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(M[0]));w.writeheader();w.writerows(M)
write(A/'source_to_final_paths.json',P)
# Local baseline views use the one preserved project implementation/result source.
alias('1_problem_and_baselines/baselines/1_sara/project_adaptation/code','11_shared_infrastructure/runtime/Baselines/SARA-main/src')
for path,s in [
 ('1_problem_and_baselines/baselines/1_sara/project_adaptation/1_w12_sara_specialist_runner.py','src/week12_extension/specialists.py'),
 ('1_problem_and_baselines/baselines/1_sara/project_results/1_query_level_specialist_results.csv','results/week12/qbgf/v3/c_extension/v1/analysis/specialist_references.csv'),
 ('1_problem_and_baselines/baselines/1_sara/project_results/2_specialist_availability.csv','results/week12/qbgf/v3/c_extension/v1/analysis/baseline_availability.csv'),
 ('1_problem_and_baselines/baselines/3_llmlingua2/project_adapter/1_qwen_budgeted_compressor.py','src/week12/compression_runtime.py'),
 ('1_problem_and_baselines/baselines/3_llmlingua2/project_adapter/2_isolated_llmlingua_worker.py','scripts/week12/llmlingua_worker.py'),
 ('1_problem_and_baselines/baselines/3_llmlingua2/project_results/1_qualification_lock.json','results/week12/qbgf/v3/protocol/llmlingua_qualification_lock.json'),
 ('1_problem_and_baselines/baselines/4_rag_controls/code/1_retrieval_and_scoring.py','src/week12/laboratory.py'),
 ('1_problem_and_baselines/baselines/4_rag_controls/code/2_raw_skip_sentence_and_h3_allocator.py','src/week12/algorithm.py'),
 ('1_problem_and_baselines/baselines/4_rag_controls/code/3_bm25_retriever.py','src/week9/retrieval.py'),
 ('1_problem_and_baselines/baselines/4_rag_controls/configs/1_frozen_reader_retriever.yaml','configs/week12/protocol.yaml'),
 ('1_problem_and_baselines/baselines/4_rag_controls/project_results/1_merged_budget_matched_validation.csv','results/week12/qbgf/v3/c_extension/v1/analysis/merged_validation_summary.csv'),
 ('1_problem_and_baselines/baselines/4_rag_controls/project_results/2_registered_extension_statistics.csv','results/week12/qbgf/v3/c_extension/v1/analysis/paired_extension_comparisons.csv')]:
 if s in P:alias(path,s)
alias('1_problem_and_baselines/baselines/5_minilm_reference/code','9_minilm_reranker/code');alias('1_problem_and_baselines/baselines/5_minilm_reference/project_results','9_minilm_reranker/results')
# Current source versus project adaptation: a comparison of file bytes, not performance.
up=B/'1_sara/upstream_source';runtime=O/'11_shared_infrastructure/runtime/Baselines/SARA-main';comparison=[]
for p in runtime.rglob('*'):
 if not p.is_file() or p.is_symlink():continue
 rel=p.relative_to(runtime);u=up/rel
 comparison.append(dict(relative_path=str(rel),project_sha256=sha(p),official_sha256=sha(u) if u.is_file() else '',same_bytes=u.is_file() and sha(p)==sha(u),meaning='Project execution code retained independently of current official snapshot'))
with (B/'1_sara/project_adaptation/PROJECT_VS_UPSTREAM.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(comparison[0]));w.writeheader();w.writerows(comparison)
# Clean baseline guides: literature results never enter benchmark tables.
for folder,label,description,repo,code,project in [
 ('1_sara','SARA','Mixed explicit passages and compressed latent retrieval vectors; parent architecture, not the frozen final proposed policy.','https://github.com/Ahren09/SARA','upstream_source/src/run_sara.py','project_adaptation/1_w12_sara_specialist_runner.py'),
 ('2_recomp','RECOMP','Extractive/abstractive context compression and selective augmentation; motivation/reference, not a measured matched W12 arm.','https://github.com/carriex/recomp','upstream_source/run_extractive_compressor.py',None),
 ('3_llmlingua2','LLMLingua-2','Distilled token-classification prompt compression; the project qualified the smaller official multilingual BERT checkpoint.','https://github.com/microsoft/LLMLingua','upstream_source/llmlingua/prompt_compressor.py','project_adapter/1_qwen_budgeted_compressor.py')]:
 doc='1_problem_and_baselines/baselines/'+folder+'/README.md';d=json.load((B/folder/'UPSTREAM_SOURCE_LOCK.json').open())
 text='# '+label+' baseline reference\n\n'+description+'\n\n**Official source:** ['+repo.split('github.com/')[1]+']('+repo+'), pinned commit `'+d['commit']+'`. '+str(len(d['files']))+' selected code/config/license files are preserved byte-for-byte; this is a source subset, not weights or a full runnable environment. [Source lock](UPSTREAM_SOURCE_LOCK.json) records URLs, license paths, SHA256 and Git blob IDs.\n\n**Open official code:** ['+Path(code).name+']('+code+').\n\n'
 if project:text+='**Open project integration:** ['+Path(project).name+']('+project+'). The reference snapshot and project adaptation are not silently interchangeable.\n\n'
 if folder=='1_sara':text+='**Project results:** [query-level specialist records](project_results/1_query_level_specialist_results.csv) and [availability/scope](project_results/2_specialist_availability.csv). BM25/SFR SARA k5/n10 are QASPER adapted-Mistral specialist references (1005queries each), not matched Qwen256/1024 controls. Historical SFR-SARA k6 remains historical only. [Project-versus-upstream byte comparison](project_adaptation/PROJECT_VS_UPSTREAM.csv) explains shared/different files.\n\n**Paper results:** [literature-only reference](PAPER_RESULTS_REFERENCE.md); do not use these as project scores.\n'
 elif folder=='2_recomp':text+='**Project results:** no matched RECOMP evaluation is recorded in the project’s canonical W12 surface. Status is NOT_EVALUATED, not a zero and not a reproduction of the paper. Official source includes extractive scoring/training, abstractive training, QA and LM evaluation. Dataset/checkpoint downloads and dependencies are not bundled or installed.\n\n**Paper results:** [literature-only reference](PAPER_RESULTS_REFERENCE.md).\n'
 else:text+='**Project results:** [qualification lock](project_results/1_qualification_lock.json) records QUALIFIED for the mBERT MeetingBank checkpoint and package0.2.2. It is a technical qualification, not answer-quality performance. No full W12 LLMLINGUA2 quality row or confirmation arm is recorded. Do not invent one or label this an XLM-R-large reproduction.\n\n**Paper results:** [literature-only reference](PAPER_RESULTS_REFERENCE.md). Code-level MIT licensing does not redefine the paper’s copyright.\n'
 text+='\n**Execution:** this pass did not install packages, train, load models or run evaluations. The original upstream README describes its execution interface; project reproduction additionally needs its historical checkpoint/data/prompt/parser/environment identities. Published paper scores use different systems and protocols.\n'
 put(doc,text)
put('1_problem_and_baselines/baselines/1_sara/PAPER_RESULTS_REFERENCE.md','# SARA published-paper results — literature only\n\nSource: [local paper](paper/sara_arxiv_2507_05633_v1.pdf), arXiv:2507.05633v1 (8July2025), physical page5, Table1. [Paper record](https://arxiv.org/abs/2507.05633v1). These percentages are from the paper, not our W12 evaluation or a reproduction.\n\n| Paper system | QASPER F1 | QASPER ROUGE-L |\n| --- | ---: | ---: |\n| RAG |22.73|16.71|\n| SARA-CSI |38.83|41.52|\n| SARA-EMB |40.55|41.71|\n\nThe source paper version, reader, retrieval and evaluation protocol differ from this project’s frozen SFR/Qwen setup and adapted-Mistral references. Do not merge or directly rank these numbers against project validation/confirmation scores. Full paper tables remain in the unchanged PDF.')
put('1_problem_and_baselines/baselines/2_recomp/PAPER_RESULTS_REFERENCE.md','# RECOMP published-paper results — literature only\n\nSource: [ICLR2024 paper](paper/recomp_iclr_2024.pdf), physical page7, Table2. [Official paper](https://proceedings.iclr.cc/paper_files/paper/2024/file/bda88ed2892f5e61c9a9bf215c566913-Paper-Conference.pdf). The reader is Flan-UL2(20B); these are paper-reported HotpotQA results, not project runs.\n\n| Paper setting | Evidence tokens | EM | F1 |\n| --- | ---: | ---: | ---: |\n| Top5documents, no compression |684|32.80|43.90|\n| Learned extractive compressor |75|30.40|40.14|\n| Learned abstractive compressor |64|28.20|37.91|\n\nThis illustrates the paper’s quality/context trade-off under its own setup. It does not supply a missing matched RECOMP score for our project.')
put('1_problem_and_baselines/baselines/3_llmlingua2/PAPER_RESULTS_REFERENCE.md','# LLMLingua-2 paper claims — literature only\n\nSource: [ACL Findings2024 paper](paper/llmlingua2_acl_findings_2024.pdf), abstract on physical page1; [official publication](https://aclanthology.org/2024.findings-acl.57/).\n\nThe paper reports compression-method speedups of3×–6× and end-to-end speedups of1.6×–2.9× at2×–5×compression ratios in its experiments. These are not measurements on our server and must not be reused as project efficiency results.\n\nThe project qualified the official smaller mBERT checkpoint, not an automatic replication of the paper’s XLM-R-large results. Qualification alone is not a full quality experiment; the canonical W12 results do not contain an evaluated LLMLINGUA2 arm.')
put('1_problem_and_baselines/baselines/4_rag_controls/README.md','# Project RAG and simple granularity controls\n\nThese are project protocol controls, not claimed imports of a single new baseline paper. SFR is the pinned [Salesforce embedding model](https://huggingface.co/Salesforce/SFR-Embedding-Mistral); BM25 is the lexical retrieval control.\n\n- code/1_retrieval_and_scoring.py: Lab.prepare ranks the passage pool and scores source units.\n- code/2_raw_skip_sentence_and_h3_allocator.py: choose/serialize implement NONE, RAW_SKIP, FIXED_SENTENCE, C2 and H3; QBGF is separately explained in5_qbgf.\n- code/3_bm25_retriever.py: actual lexical scoring utility.\n- configs/: exact shared reader/retrieval protocol.\n- project_results/: recorded merged validation and paired extension tables, not recomputed here.\n\nBM25_PLAIN_RAG and SFR_PLAIN_RAG mean budget-matched RAW_SKIP whole-passage RAG at256/1024, not unrestricted full-context RAG. FIXED_SENTENCE has no top8 cap; C2 is the separate top8 control. H3 is the prevalidated hierarchical control. Reader/prompt/parser/budget identities remain frozen.\n\nThese controls are distinct from adapted-Mistral SARA specialist references and external paper-only RECOMP scores.')
put('1_problem_and_baselines/baselines/5_minilm_reference/README.md','# MiniLM reference baseline\n\nThe evaluated project implementation and results have one canonical home: [9_minilm_reranker](../../../9_minilm_reranker/README.md). Local code/results links point there without duplicating it.\n\n[Official checkpoint card](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2). The project freezes revision233902d25c440f23af6f7d6e94d2946bac0bee0a, FP32 CPU scoring, raw logits and max pair length512. This is a query–sentence cross-encoder relevance control, not a newly trained utility predictor. Refer to the recorded matched comparisons and uncertainty, not unrelated MS-MARCO model-card metrics.')
# Compact central index avoids burying actual baselines among all reference configs.
put('1_problem_and_baselines/baselines/README.md','# Baseline library\n\n| Baseline | What is preserved | Project evaluation status |\n| --- | --- | --- |\n| [SARA](1_sara/README.md) | Licensed official source, pinned commit, original paper, project adaptation and query results | QASPER adapted-Mistral k5/n10 specialist; not Qwen-budget matched |\n| [RECOMP](2_recomp/README.md) | Official source, license, original paper and clearly labelled paper results | Motivation/reference only; no matched W12 evaluation |\n| [LLMLingua-2](3_llmlingua2/README.md) | Official v0.2.2 source, license, paper, project wrapper and qualification receipt | Smaller mBERT qualified; no full W12 quality/confirmation arm |\n| [BM25/SFR RAG controls](4_rag_controls/README.md) | Actual frozen project code/config/result links | Budget-matched RAW_SKIP and simple granularity controls |\n| [MiniLM cross-encoder](5_minilm_reference/README.md) | Link to canonical project code/results and official checkpoint card | Post-W12 matched exploratory comparison |\n\nThree layers remain distinct: official publication/source; the project’s executed adaptation; recorded project results. No paper score was inserted into benchmark CSVs. Source locks include original licenses and exact content identities; model weights are not bundled. See BASELINE_RESULTS_INDEX.md.')
# Baseline table selects existing rows, without scoring or forming new averages.
s='results/week12/qbgf/v3/c_extension/v1/analysis/merged_validation_summary.csv';rr=list(csv.DictReader((O/P[s]).open()));rr=[r for r in rr if r['method'] in ['BM25_PLAIN_RAG','SFR_PLAIN_RAG']]
table='| Dataset | Method ID | Budget | n | Quality |\n| --- | --- | --- | --- | --- |\n'+'\n'.join('| '+' | '.join(r[k] for k in ['dataset','method','budget','n_queries','quality'])+' |' for r in rr)
doc='1_problem_and_baselines/baselines/BASELINE_RESULTS_INDEX.md'
put(doc,'# Recorded project baseline results\n\nSource: '+link(s,doc=doc)+'. The selected fields below are stored results, not a new evaluation or calculated average. BM25/SFR plain RAG are RAW_SKIP under a shared evidence budget.\n\n'+table+'\n\nSARA query-level k5/n10 results and scope: '+link('results/week12/qbgf/v3/c_extension/v1/analysis/specialist_references.csv',doc=doc)+' and '+link('results/week12/qbgf/v3/c_extension/v1/analysis/baseline_availability.csv',doc=doc)+'. These two1005-query QASPER specialist arms use adapted Mistral and are not budget-matched Qwen systems. No new aggregate statistic was computed.\n\nRECOMP has no matched project result. LLMLingua-2 has a qualification receipt, not a full W12 quality score. Published-paper numbers are isolated in each baseline’s PAPER_RESULTS_REFERENCE.md and must not enter project validation/confirmation tables. Historical parent RAG/SARA results and early fixed-k/oracle results remain in the adaptive-quantity section.')
put('1_problem_and_baselines/README.md','# Problem, parent architecture and baselines\n\nStart with the [baseline library](baselines/README.md) and [recorded baseline results](baselines/BASELINE_RESULTS_INDEX.md).\n\n- SARA: official pinned code/paper; separately preserved project adaptation and QASPER specialist query results.\n- RECOMP: official code/paper and literature results; no invented matched project score.\n- LLMLingua-2: official code/paper, project integration and smaller-mBERT qualification; no full W12 quality arm.\n- BM25/SFR plain RAG: actual shared project controls, explicitly RAW_SKIP budget matched.\n- MiniLM: links to its single canonical project implementation/results.\n\nOriginal upstream code is reference source, not a claim that the historical project used the latest upstream revision. Original code licenses remain attached. Source PDFs are unchanged; paper-reported outcomes are isolated from project results. Parent SARA reference configs were moved beside its project adaptation so the top-level configs area stays focused. No models or experiments ran in this cleanup.')
put('.gitignore','''# Local policy for FINAL_PROJECT_MAIN. The outer repository currently ignores
# this entire folder; this file takes effect when that outer exclusion is lifted.
# Keep scientific result tables, query rows, source pools, folds, *.joblib,
# notebooks, figures, freeze/protocol files and provenance manifests visible.
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.ipynb_checkpoints/
.venv/
venv/
sara_env/
node_modules/
.cache/
model_cache/
models_cache/
checkpoints/
*.safetensors
*.bin
*.pt
*.pth
*.ckpt
*.gguf
*.onnx
*.sqlite
*.sqlite3
*.db
*.partial
*.tmp
.DS_Store
/11_shared_infrastructure/audit/cleanup_review/
/11_shared_infrastructure/audit/file_integrity.csv
''')
# All approved source references and moved files are now in the updated manifest.
with (O/'PROVENANCE_MANIFEST.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(M[0]));w.writeheader();w.writerows(M)
write(A/'source_to_final_paths.json',P)
write(A/'cleanup_summary.json',dict(retired_generated_files=len(retire),retired_bytes=sum(x['bytes'] for x in retire),scientific_source_files_deleted=0,moved_parent_configs=len(config_moves),official_source_files=sum(x['files'] for x in checks),official_commits={x['baseline']:x['commit'] for x in checks},models_loaded=0,experiments_executed=0,changes_confined_to=str(O)))
print((A/'cleanup_summary.json').read_text())
