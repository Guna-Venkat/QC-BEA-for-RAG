"""UI-only check: no retrieval, model loading, generation or research writes."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 page=b.new_page(viewport=dict(width=1440,height=1000))
 page.goto('http://localhost:8527')
 page.get_by_text('Workspace Navigation',exact=True).wait_for(timeout=60000)
 checks=[]
 for label in ['Start Here','Compare Methods','How the Algorithms Work','Live Lab']:
  page.get_by_text(label,exact=True).first.click()
  page.wait_for_timeout(1800)
  assert page.locator('[data-testid="stException"]').count()==0,(label,page.locator('body').inner_text()[-1200:])
  assert 'Primary research artifact verification failed' not in page.locator('body').inner_text()
  checks.append(dict(workspace=label,status='PASSED'))
  page.screenshot(path=str(ROOT/'verification'/('workspace_'+label.lower().replace(' ','_')+'.png')),full_page=True)
 # Browser starts on the preserved original preset, never the grouped alternative.
 page.get_by_role('button',name='Budget-sensitive multi-aspect question',exact=True).click()
 page.wait_for_timeout(1000)
 assert page.locator('[data-testid="stTextArea"]').filter(has_text='Passage 15').count()==1
 assert page.locator('[data-testid="stException"]').count()==0
 b.close()
(ROOT/'verification/browser_results.json').write_text(json.dumps(checks,indent=2))
print('All four copied-app workspaces passed; original 15-passage preset loads.')
