"""Download pinned, licensed baseline reference source only. No installs or execution."""
from pathlib import Path
import urllib.request,json,hashlib,concurrent.futures,time,subprocess
O=Path(__file__).resolve().parents[2];assert O.name=='FINAL_PROJECT_MAIN'
BASE=O/'1_problem_and_baselines/baselines'
def get(url,limit=6_000_000):
 for attempt in range(3):
  try:
   run=subprocess.run(['curl','--fail','--silent','--show-error','--location','--max-time','20','--proto','=https','--proto-redir','=https','--header','User-Agent: CS787-source-provenance-audit',url],capture_output=True,check=True)
   if len(run.stdout)>limit:raise ValueError('Reference file exceeds size cap: '+url)
   return run.stdout
  except Exception:
   if attempt==2:raise
   time.sleep(1)

def jget(url):return json.loads(get(url))
repos=[('1_sara','Ahren09/SARA','main'),('2_recomp','carriex/recomp','main'),('3_llmlingua2','microsoft/LLMLingua','v0.2.2')]
for folder,repo,ref in repos:
 print('Fetching official source metadata:',repo,ref,flush=True)
 out=BASE/folder/'upstream_source';out.mkdir(parents=True,exist_ok=True)
 lock=out.parent/'UPSTREAM_SOURCE_LOCK.json'
 if lock.exists():
  obj=json.load(lock.open());print(repo,'already pinned',obj['commit'],flush=True);continue
 try:
  actual_ref=ref
  try:commit=jget('https://api.github.com/repos/'+repo+'/commits/'+ref)['sha']
  except Exception:
   if ref!='v0.2.2':raise
   actual_ref='main';commit=jget('https://api.github.com/repos/'+repo+'/commits/main')['sha']
  commit_record=jget('https://api.github.com/repos/'+repo+'/git/commits/'+commit)
  tree_sha=commit_record['tree']['sha']
  tree=jget('https://api.github.com/repos/'+repo+'/git/trees/'+tree_sha+'?recursive=1')
  if tree.get('truncated'):raise ValueError('Truncated source tree; cannot silently curate incomplete listing')
  def choose(item):
   p=item['path'];low=p.lower()
   if item['type']!='blob' or item.get('size',0)>1_000_000 or '..' in Path(p).parts:return False
   if repo=='Ahren09/SARA':return (p.startswith('src/') and p.endswith('.py')) or (p.startswith('config/') and p.endswith(('.yaml','.yml','.json'))) or p in ['README.md','LICENSE','LICENSE.txt','CITATION.cff','pyproject.toml','requirements.txt','Dockerfile']
   if repo=='carriex/recomp':return p.endswith('.py') or p in ['README.md','LICENSE','requirements.txt','CITATION.cff']
   return (p.startswith('llmlingua/') and p.endswith('.py')) or p in ['README.md','LICENSE','SECURITY.md','CITATION.cff','pyproject.toml','setup.py','setup.cfg','requirements.txt'] or (p.startswith('experiments/llmlingua2/') and p.endswith(('.py','.yaml','.yml','.json','.md')))
  selected=[x for x in tree['tree'] if choose(x)];saved=[]
  def fetch(item):
   p=item['path'];url='https://raw.githubusercontent.com/'+repo+'/'+commit+'/'+p;b=get(url)
   q=out/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
   return dict(path=p,url=url,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),git_blob_sha=item['sha'])
  with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
   for n,row in enumerate(pool.map(fetch,selected),1):
    saved.append(row)
    if n%20==0:print(repo,'source files',n,'/',len(selected),flush=True)
  license_files=[r['path'] for r in saved if Path(r['path']).name.lower().startswith('license')]
  if not license_files:raise ValueError('Official source license absent; do not label archive ready')
  obj=dict(repository='https://github.com/'+repo,requested_ref=ref,resolved_ref=actual_ref,commit=commit,source_tree_sha=tree_sha,retrieval='HTTPS pinned raw source; no installed package or model weights',license_files=license_files,files=sorted(saved,key=lambda x:x['path']),status='PINNED_REFERENCE_SOURCE_NOT_A_NEW_BENCHMARK_RUN',notes='Current upstream source snapshot is not asserted to be the historical project execution revision. LLMLingua tag fallback, if present, is reference-only and package0.2.2 remains the project qualification identity.')
  lock.write_text(json.dumps(obj,indent=2)+'\n');print(repo,'PINNED',commit,'files',len(saved),'bytes',sum(x['bytes'] for x in saved),flush=True)
 except Exception as e:
  err=dict(repository='https://github.com/'+repo,requested_ref=ref,error=type(e).__name__,message=str(e),status='SOURCE_FETCH_INCOMPLETE_NO_RESULTS_INVENTED')
  (out.parent/'SOURCE_FETCH_STATUS.json').write_text(json.dumps(err,indent=2)+'\n');print(err,flush=True)
