
import runpy
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
APP_PATH = SRC_DIR / "amanara" / "ui" / "app.py"

# Make the Amanara package importable during deployment.
sys.path.insert(0, str(SRC_DIR))

# Execute the Streamlit UI.
runpy.run_path(str(APP_PATH), run_name="__main__")
