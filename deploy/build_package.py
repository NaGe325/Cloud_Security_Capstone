"""Prepare a local-only Lambda source folder. Does not deploy or contact AWS."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
destination = root / "deploy" / "package"
if destination.exists():
    shutil.rmtree(destination)  # Only this generated build directory.
destination.mkdir()
for folder in ("medtech",):
    shutil.copytree(root / folder, destination / folder, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
(destination / "requirements.txt").write_text((root / "requirements.txt").read_text())
print(f"Local Lambda source prepared: {destination}")
