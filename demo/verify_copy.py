"""Read-only check of the copied demo payload; no inference or writes."""
import hashlib,json
from pathlib import Path
base=Path(__file__).resolve().parent
manifest=json.loads((base/'COPY_MANIFEST.json').read_text())
missing=[];changed=[]
for row in manifest['files']:
 p=base/manifest['bundle_root']/row['path']
 if not p.is_file():missing.append(row['path'])
 elif hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:changed.append(row['path'])
if missing or changed:raise SystemExit(json.dumps(dict(missing=missing,changed=changed),indent=2))
print(f"Verified {len(manifest['files'])} copied files. No missing or changed files.")
