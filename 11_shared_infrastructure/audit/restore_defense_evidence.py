"""Copy existing raw V1 and matched source evidence only; never regenerate data."""
from pathlib import Path
import json,csv,hashlib,os,shutil
O=Path(__file__).resolve().parents[2];R=O.parent;A=O/'11_shared_infrastructure/audit'
assert O.name=='FINAL_PROJECT_MAIN'
M=list(csv.DictReader((O/'PROVENANCE_MANIFEST.csv').open()));P=json.load((A/'source_to_final_paths.json').open());bysha={r['sha256']:r['current_final_path'] for r in M if '/5_query_level/' in r['current_final_path']}
added=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def add(src,dst,reason):
 if src in P:return
 p=R/src
 if not p.is_file():return
 h=sha(p);dst=bysha.get(h,dst);q=O/dst;q.parent.mkdir(parents=True,exist_ok=True)
 if not q.exists():shutil.copyfile(p,q)
 assert sha(q)==h;bysha[h]=dst;P[src]=dst
 row={k:'' for k in M[0]};row.update(current_final_path=dst,original_repo_path=src,original_filename=p.name,new_filename=q.name,conceptual_group='7_bea_v1',chronological_phase='POST-W12',method='BEA_QBGF_V1 / MATCHED_CONTROLS',scientific_status='POST_W12_EXPLORATORY',reason_included=reason,sha256=h,copied_exactly_from_source=True,renamed_inside_final_main=p.name!=q.name,notes='Copied read-only during defense-readiness pass; no inference or metric recomputation.',report_status='CANONICAL_SOURCE_ARTIFACT')
 M.append(row);added.append(dict(original_repo_path=src,current_final_path=dst,sha256=h,reason=reason))
 alias=O/'11_shared_infrastructure/runtime'/src
 if not alias.exists():alias.parent.mkdir(parents=True,exist_ok=True);alias.symlink_to(os.path.relpath(q,alias.parent))
for stage in ['pilot','expanded']:
 for p in (R/'results/post_w12/bea_qbgf/v3'/stage/'rows').glob('*.json'):
  add(str(p.relative_to(R)),'7_bea_v1/results/5_query_level/'+stage+'/'+p.name,'Preserve original query-level evidence/answers for pilot and expansion, separate from summaries')
cohort=json.load((O/P['results/post_w12/bea_qbgf/v3/PILOT_COHORT.json']).open())['selected'];members={(d,x['query_id']) for d,rr in cohort.items() for x in rr}
for p in (R/'results/post_w12/bea_qbgf/v3/cache/problems').glob('*.json'):
 v=json.load(p.open())
 if tuple(v['key']) in members:add(str(p.relative_to(R)),'11_shared_infrastructure/data/matched_source_pools/'+p.name,'Exact shared candidate passages, sentence offsets and semantic signals for the matched developmental cohort')
with (O/'PROVENANCE_MANIFEST.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(M[0]));w.writeheader();w.writerows(M)
(A/'source_to_final_paths.json').write_text(json.dumps(P,indent=2)+'\n')
with (A/'restored_defense_artifacts.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['original_repo_path','current_final_path','sha256','reason']);w.writeheader();w.writerows(added)
print('Restored source records:',len(added),'No generations executed.')
