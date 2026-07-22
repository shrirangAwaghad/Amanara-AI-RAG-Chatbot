import sys
from pathlib import Path

# Add the src directory to Python's module search path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from amanara.ui.app import app

app()