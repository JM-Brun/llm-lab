"""Make the site build tools importable from the site regression tests."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "site" / "tools"))
