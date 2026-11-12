"""One-time defense-navigation migration; mutations confined to FINAL_PROJECT_MAIN."""
from pathlib import Path
import json,csv,hashlib,re,os,shutil
O=Path(__file__).resolve().parents[2];A=O/'11_shared_infrastructure/audit';assert O.name=='FINAL_PROJECT_MAIN'
if (A/'defense_migration_complete.json').exists():raise SystemExit('Migration already complete; run the verifier instead.')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
M=list(csv.DictReader((O/'PROVENANCE_MANIFEST.csv').open()));oldP=json.loads((O/'shared/audit/source_to_final_paths.json').read_text())
initial=[p for p in O.rglob('*') if p.is_file() and not p.is_symlink() and not p.is_relative_to(A)]
js(A/'before_defense_inventory.json',[dict(path=str(p.relative_to(O)),sha256=sha(p),bytes=p.stat().st_size) for p in initial])
shutil.copyfile(O/'PROVENANCE_MANIFEST.csv',A/'before_defense_provenance.csv')
links=[(str(p.relative_to(O)),str(p.resolve().relative_to(O))) for p in O.rglob('*') if p.is_symlink()]
js(A/'before_defense_links.json',links)
G=['1_problem_and_baselines','2_adaptive_evidence_quantity','3_evidence_identity_and_routing','4_multigranular_evidence_study','5_qbgf','6_downstream_utility_attribution','7_bea_v1','8_bea_v2','9_minilm_reranker','10_final_method_comparison','11_shared_infrastructure','12_report_support']
T={'01_problem_and_motivation':G[0],'02_parent_architecture_and_baselines':G[0],'03_adaptive_evidence_quantity':G[1],'04_evidence_identity_and_routing':G[2],'05_granularity_study':G[3],'06_qbgf':G[4],'07_downstream_utility_attribution':G[5],'08_bea_v1':G[6],'09_bea_v2':G[7],'10_reranker_baseline':G[8],'11_final_cross_method_comparison':G[9]}
def group(s,old=''):
 if s=='W12-POST/config.json' or s=='W12-POST/REPORTING_PATCH.json':return G[6]
 if s.startswith('Baselines/'):return G[0]
 for pre,g in T.items():
  if old.startswith(pre+'/'):return g
 l=s.lower()
 if any(x in l for x in ['minilm','reranker_baseline']):return G[8]
 if any(x in l for x in ['final_case_study','final_query_level']):return G[9]
 if any(x in l for x in ['bea_v2','bea_qbgf_v2']):return G[7]
 if any(x in l for x in ['bea_qbgf','pilot_aspect']):return G[6]
 if 'attribution' in l or re.search(r'week12_[jkl]_',l):return G[5]
 if 'week12' in l or 'week13' in l:return G[4]
 if 'week11' in l:return G[3]
 if re.search('week[6789]|week10',l):return G[2]
 if re.search('week[2345]',l):return G[1]
 return G[0]
K={
'results/week2/processed/oracle_vs_static_summary.json':G[1]+'/results/1_primary/1_fixed_k_oracle_qasper_summary.json',
'results/week4/processed/model_comparison.csv':G[1]+'/results/1_primary/2_query_conditioned_controller_results.csv',
'results/week5/content_allocator/tables/main_results.csv':G[1]+'/results/1_primary/3_content_aware_controller_results.csv',
'results/week6/passage_routing/tables/w6_main_results.csv':G[2]+'/results/1_primary/1_passage_identity_routing_results.csv',
'results/week7/w7c2_utility_ranking/tables/w7c2_main_dev_results.csv':G[2]+'/results/1_primary/2_utility_aware_budget_ranking_results.csv',
'results/week11/multigranular/v1/final_report/main_granularity_summary_df.csv':G[3]+'/results/1_primary/1_multigranular_budget_results.csv',
'results/week11/multigranular/v1/final_report/matched_reader_summary_df.csv':G[3]+'/results/1_primary/2_matched_reader_results.csv',
'results/week12/qbgf/v3/analysis/summary.csv':G[4]+'/results/1_primary/1_qbgf_validation_and_ablation_summary.csv',
'results/week12/qbgf/v3/analysis/primary_comparisons.csv':G[4]+'/results/3_statistics/1_validation_and_query_conditioning_paired_tests.csv',
'results/week12/qbgf/v3/analysis/fusion_diagnostic_comparisons.csv':G[4]+'/results/2_ablations/2_sentence_and_passage_fusion_paired_tests.csv',
'results/week12/W13_FINAL_METHOD_FREEZE.json':G[4]+'/results/4_frozen_decision/1_fixed_sentence_final_policy_freeze.json',
'results/week12/final_confirmation/v1/summary.csv':G[4]+'/results/5_reserved_confirmation/1_frozen_system_confirmation_results.csv',
'results/week12/final_confirmation/v1/contrasts.csv':G[4]+'/results/5_reserved_confirmation/2_confirmation_paired_tests.csv',
'results/week12/attribution/v1/analysis/unit_importance.csv':G[5]+'/results/1_primary/1_query_level_loo_unit_importance.csv',
'results/week12/attribution/v1/analysis/unit_summary.csv':G[5]+'/results/1_primary/2_helpful_neutral_harmful_summary.csv',
'results/week12/attribution/v1/analysis/relevance_utility.csv':G[5]+'/results/3_statistics/1_relevance_downstream_utility_correlations.csv',
'results/post_w12/bea_qbgf/v3/pilot/summary.csv':G[6]+'/results/1_primary/1_bea_v1_pilot_quality_results.csv',
'results/post_w12/bea_qbgf/v3/pilot/evidence_behavior.csv':G[6]+'/results/4_diagnostics/1_bea_v1_pilot_allocation_efficiency.csv',
'results/post_w12/bea_qbgf/v3/pilot/paired_comparisons.csv':G[6]+'/results/3_statistics/1_bea_v1_pilot_paired_tests.csv',
'results/post_w12/bea_qbgf/v3/expanded/summary.csv':G[6]+'/results/2_expanded/1_bea_v1_expanded_quality_results.csv',
'results/post_w12/bea_v2/v3/utility_model/fold_metrics.csv':G[7]+'/results/1_phelp_model/1_group_crossfit_predictor_metrics.csv',
'results/post_w12/bea_v2/v3/calibration/threshold_summary.csv':G[7]+'/results/2_calibration_failed/1_original_grid_mechanical_results.csv',
'results/post_w12/bea_v2/v3/calibration/resolution/threshold_summary.csv':G[7]+'/results/2_calibration_failed/2_resolution_grid_mechanical_results.csv',
'results/post_w12/bea_v2/v3/CALIBRATION_TERMINATED.json':G[7]+'/results/2_calibration_failed/3_calibration_failed_terminated.json',
'results/post_w12/bea_v2/posthoc_tau8e5/POSTHOC_SUMMARY.csv':G[7]+'/results/3_posthoc_reader_run/1_bea_v2_posthoc_quality_results.csv',
'results/post_w12/bea_v2/posthoc_tau8e5/POSTHOC_PAIRED_COMPARISONS.csv':G[7]+'/results/3_posthoc_reader_run/2_bea_v2_posthoc_paired_tests.csv',
'W12-POST/results/minilm_reranker/analysis/SUMMARY.csv':G[8]+'/results/1_primary/1_minilm_matched_quality_results.csv',
'W12-POST/results/minilm_reranker/analysis/FINAL_COMPARISON.csv':G[9]+'/results/1_quality_comparison.csv',
'W12-POST/results/minilm_reranker/analysis/EFFICIENCY.csv':G[9]+'/results/2_efficiency_comparison.csv',
'W12-POST/results/minilm_reranker/analysis/PAIRED_COMPARISONS.csv':G[9]+'/results/3_paired_statistical_comparisons.csv',
'W12-POST/results/minilm_reranker/analysis/POINT_ESTIMATE_WINS.json':G[9]+'/results/4_descriptive_point_winner_summary.json',
}
NB={
'week12_A_qbgf_algorithm.ipynb':(G[4],'1_qbgf_algorithm'), 'week12_B_baseline_qualification.ipynb':(G[4],'2_baseline_qualification'), 'week12_C_validation_surface.ipynb':(G[4],'3_qbgf_validation_surface'), 'week12_C_EXT_baseline_extension.ipynb':(G[4],'4_budget_matched_baseline_extension'), 'week12_D_qbgf_ablations.ipynb':(G[4],'5_qbgf_query_and_fusion_ablations'), 'week12_H_validation_analysis.ipynb':(G[4],'6_qbgf_validation_analysis'), 'week12_I_week13_freeze.ipynb':(G[4],'7_final_policy_freeze'), 'week12_M_final_confirmation.ipynb':(G[4],'8_reserved_confirmation'),
'BEA_QBGF.ipynb':(G[6],'1_bea_v1_exploratory_pipeline'), 'BEA_QBGF_V2.ipynb':(G[7],'1_bea_v2_phelp_and_calibration'), 'BEA_QBGF_V2_POSTHOC_TAU8E5.ipynb':(G[7],'2_bea_v2_posthoc_tau8e5'), 'BaselineComparison_MiniLM.ipynb':(G[8],'1_minilm_baseline_comparison'), 'FINAL_QUERY_LEVEL_CASE_STUDY.ipynb':(G[9],'2_qualitative_case_analysis')}
# Freeze old canonical -> new canonical mapping before mutating any file.
byold={}
for r in M:byold.setdefault(r['current_final_path'],[]).append(r)
move={};seen={}
for old,rr in byold.items():
 r=rr[0];s=r['original_repo_path'];g=group(s,old);p=Path(old);name=p.name
 explicit=next((K[x['original_repo_path']] for x in rr if x['original_repo_path'] in K),None)
 if explicit:d=explicit
 elif old.startswith('shared/runtime/'):d=old.replace('shared/runtime/',G[10]+'/runtime/',1)
 elif name.endswith('.ipynb'):
  if Path(s).name in NB:g,n=NB[Path(s).name];d=g+'/notebooks/'+n+'.ipynb'
  else:
   stem=re.sub(r'^week\d+[a-z]?_(?:[A-Z0-9]+_)?','',Path(s).stem);d=g+'/notebooks/9_'+stem.lower()+'.ipynb'
 elif old.startswith('configs/'):
  stem=Path(s).stem.lower();stem=re.sub('^week\d+_','',stem);d=g+'/configs/1_'+stem+p.suffix
 elif old.startswith('report_sources/'):d=G[11]+'/source_reports/'+old.split('/',1)[1]
 elif old.startswith('shared/environment/'):d=G[10]+'/environment/'+name
 elif '/figures/' in old:d=g+'/figures/'+old.split('/',1)[1].replace('/figures/','/')
 elif p.suffix.lower() in ['.md','.txt','.rst']:d=g+'/docs/'+old.split('/',1)[1]
 else:
  tail=old.split('/',1)[1]
  if g==G[4]:
   for a,b in [('validation/','1_primary/w12_validation/'),('ablation/','2_ablations/'),('freeze/','4_frozen_decision/'),('confirmation/','5_reserved_confirmation/')]:
    if tail.startswith(a):tail=b+tail[len(a):];break
   else:tail='4_diagnostics/'+tail
  elif g==G[7]:
   for a,b in [('utility_model/','1_phelp_model/'),('predictor_protocol/','1_phelp_model/protocol/'),('calibration/','2_calibration_failed/'),('posthoc_reader_run/','3_posthoc_reader_run/')]:
    if tail.startswith(a):tail=b+tail[len(a):];break
  elif g==G[6]:tail=tail.replace('pilot/','1_primary/pilot/',1) if tail.startswith('pilot/') else tail.replace('expanded/','2_expanded/',1) if tail.startswith('expanded/') else '4_diagnostics/'+tail
  elif g==G[8]:tail='4_diagnostics/'+tail
  elif g==G[5]:tail='4_diagnostics/'+tail
  else:tail='1_primary/'+tail
  d=g+'/results/'+tail
 if d in seen and seen[d]!=r['sha256']:d=str(Path(d).with_name(Path(d).stem+'__'+r['sha256'][:8]+Path(d).suffix))
 move[old]=d;seen[d]=r['sha256']
# Generated prior navigation is historical, not the current defense guide.
for p in initial:
 old=str(p.relative_to(O))
 if old in move or old=='PROVENANCE_MANIFEST.csv':continue
 if old.startswith('shared/audit/'):d=G[10]+'/audit/previous_pass/'+old.split('shared/audit/',1)[1]
 elif old.startswith('shared/'):d=G[10]+'/previous_interface_docs/'+old.split('shared/',1)[1]
 else:d=G[11]+'/previous_navigation/'+old
 move[old]=d
js(A/'defense_path_plan.json',move)
actions=[]
for old,d in move.items():
 src=O/old;dst=O/d;h=sha(src);dst.parent.mkdir(parents=True,exist_ok=True)
 if src!=dst:
  if dst.exists():assert sha(dst)==h;src.unlink();action='unified byte-identical duplicate'
  else:src.rename(dst);action='moved/renamed'
 else:action='preserved'
 assert sha(dst)==h;actions.append(dict(old_path=old,new_path=d,action=action,sha256=h))
# Rewire every captured internal compatibility link to its moved canonical file.
def remap(path):
 if path in move:return move[path]
 for pre,to in [('shared/runtime',G[10]+'/runtime'),('shared/audit',G[10]+'/audit/previous_pass')]:
  if path==pre or path.startswith(pre+'/'):return to+path[len(pre):]
 return path
for old,target in links:
 src=O/old;d=O/remap(old);t=O/remap(target)
 if src.is_symlink():src.unlink()
 d.parent.mkdir(parents=True,exist_ok=True)
 if not d.exists():d.symlink_to(os.path.relpath(t,d.parent),target_is_directory=t.is_dir())
# Preserve provenance for every renamed canonical artifact and alias source identity.
for r in M:
 old=r['current_final_path'];r['pre_defense_path']=old;r['current_final_path']=move[old];r['new_filename']=Path(move[old]).name;r['renamed_inside_final_main']=r['original_filename']!=r['new_filename'];r['conceptual_group']=group(r['original_repo_path'],old)
 if r['original_repo_path'].endswith('BEA_QBGF.ipynb'):r['conceptual_group']=G[6]
with (O/'PROVENANCE_MANIFEST.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(M[0]));w.writeheader();w.writerows(M)
P={r['original_repo_path']:r['current_final_path'] for r in M};js(A/'source_to_final_paths.json',P)
with (A/'defense_reorganization_actions.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(actions[0]));w.writeheader();w.writerows(actions)
# New local code views are internal symlinks to real modules, never invented split implementations.
code={
G[0]:[('1_sara_model_loader.py','Baselines/SARA-main/src/model/loader.py')],
G[1]:[('1_fixed_k_sweep.py','src/week2/sweep_runner.py'),('2_query_controller_models.py','src/week4/qcca_models.py'),('3_content_controller.py','src/week5/architecture.py')],
G[2]:[('1_passage_identity_routing.py','src/week6/routing.py')],
G[3]:[('1_multigranular_experiment_runner.py','src/week11/runner.py')],
G[4]:[('1_qbgf_and_sentence_allocator.py','src/week12/algorithm.py'),('2_validation_runner.py','src/week12/runner.py'),('3_candidate_and_evidence_lab.py','src/week12/laboratory.py'),('4_frozen_qwen_reader.py','src/week12/reader.py')],
G[5]:[('1_loo_perturbation_experiment.py','src/week12_attribution/experiment.py')],
G[6]:[('1_dynamic_marginal_allocator.py','src/post_w12/bea_qbgf/allocator.py'),('2_bea_v1_experiment_runner.py','src/post_w12/bea_qbgf/runner.py'),('3_semantic_resources.py','src/post_w12/bea_qbgf/resources.py')],
G[7]:[('1_usefulness_weighted_allocator.py','src/post_w12/bea_v2/allocator.py'),('2_group_crossfit_phelp_models.py','src/post_w12/bea_v2/models.py'),('3_loo_feature_data.py','src/post_w12/bea_v2/data.py'),('4_calibration_and_reader_stages.py','src/post_w12/bea_v2/stages.py'),('5_posthoc_reader_runner.py','src/post_w12/bea_v2_posthoc/runner.py')],
G[8]:[('1_cross_encoder_sentence_reranker.py','W12-POST/reranker_baseline/minilm_reranker.py'),('2_reranker_experiment_runner.py','W12-POST/reranker_baseline/runner.py'),('3_matched_comparison_analysis.py','W12-POST/reranker_baseline/analysis.py'),('4_frozen_reranker_protocol.py','W12-POST/reranker_baseline/protocol.py')],
G[9]:[('1_final_comparison_analysis.py','W12-POST/reranker_baseline/analysis.py')],
}
views={}
for g,items in code.items():
 for title,s in items:
  if s not in P:continue
  alias=O/g/'code'/title;target=O/P[s];alias.parent.mkdir(parents=True,exist_ok=True)
  if not alias.exists():alias.symlink_to(os.path.relpath(target,alias.parent))
  views[s]=str(alias.relative_to(O))
js(A/'local_code_views.json',views)
# Same final-comparison notebook, one canonical copy; two clear navigation entrances.
nb=P['W12-POST/BaselineComparison_MiniLM.ipynb'];alias=O/G[9]/'notebooks/1_final_baseline_comparison.ipynb';alias.parent.mkdir(parents=True,exist_ok=True);alias.symlink_to(os.path.relpath(O/nb,alias.parent))
# Local MiniLM statistics/efficiency refer to canonical five-method output, not fabricated duplicates.
for s,name in [('W12-POST/results/minilm_reranker/analysis/EFFICIENCY.csv','2_minilm_and_controls_efficiency.csv'),('W12-POST/results/minilm_reranker/analysis/PAIRED_COMPARISONS.csv','3_minilm_paired_comparisons.csv')]:
 a=O/G[8]/'results/1_primary'/name;a.parent.mkdir(parents=True,exist_ok=True);a.symlink_to(os.path.relpath(O/P[s],a.parent))
# Remove empty legacy shells only, preserving all file bytes and compatibility links.
for p in sorted([p for p in O.rglob('*') if p.is_dir() and not p.is_symlink()],key=lambda x:len(x.parts),reverse=True):
 try:p.rmdir()
 except OSError:pass
for g in G:(O/g).mkdir(exist_ok=True)
js(A/'defense_migration_complete.json',dict(source_records=len(M),canonical_source_files=len(byold),initial_physical_files=len(initial),moved_records=len(actions),algorithm_changes=0,notebook_content_changes=0,experiments_executed=0))
print((A/'defense_migration_complete.json').read_text())
