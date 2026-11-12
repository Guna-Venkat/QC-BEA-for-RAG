"""Launch the copied Evidence Lab; all imports resolve inside this bundle."""
import runpy,sys
from pathlib import Path
application=Path(__file__).resolve().parent/'application'
sys.path.insert(0,str(application))
runpy.run_path(str(application/'demo/app.py'),run_name='__main__')
