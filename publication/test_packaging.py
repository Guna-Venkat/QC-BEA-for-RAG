"""Small stdlib packaging tests; no inference or Git changes."""
import importlib.util,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('readiness',ROOT/'publication/check_readiness.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class PackagingTests(unittest.TestCase):
 def test_recursive_requirements_comments_and_cycles(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/'a.txt').write_text('# comment\n-r b.txt\nnumpy==1.26.4\n');(p/'b.txt').write_text('-r a.txt\njoblib==1.6.0\n')
   self.assertEqual(m.requirement_lines(p/'a.txt'),['joblib==1.6.0','numpy==1.26.4'])
 def test_inventory_preserves_internal_links_and_ignores_environment(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/'module.py').write_text('x=1\n');(p/'alias.py').symlink_to('module.py')
   (p/'.venv').mkdir();(p/'.venv/python').symlink_to('/usr/bin/python3')
   paths=m.inventory(p);self.assertIn(p/'alias.py',paths);self.assertFalse(any('.venv' in x.parts for x in paths))
 def test_git_preserves_exact_scientific_line_endings(self):
  self.assertIn("* -text",(ROOT/".gitattributes").read_text())
 def test_all_large_files_have_exact_lfs_rules(self):
  rules=(ROOT/'.gitattributes').read_text()
  for rel in m.LFS_PATHS:self.assertIn('/'+rel+' filter=lfs diff=lfs merge=lfs -text',rules)
 def test_license_scope_and_upstream_licenses_preserved(self):
  self.assertTrue((ROOT/'LICENSE').read_text().startswith('MIT License'))
  self.assertIn('project-authored software and documentation only',(ROOT/'THIRD_PARTY_NOTICES.md').read_text())
  for method in ['1_sara','2_recomp','3_llmlingua2']:
   self.assertTrue((ROOT/'1_problem_and_baselines/baselines'/method/'upstream_source/LICENSE').is_file())
 def test_standalone_environment_precedes_legacy_environment(self):
  s=(ROOT/'demo/launch.sh').read_text()
  self.assertLess(s.index('$DEMO_BUNDLE/../.venv/bin/python'),s.index('$DEMO_BUNDLE/../../demo/.venv/bin/python'))
if __name__=='__main__':unittest.main()
