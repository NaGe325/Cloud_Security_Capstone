"""Build a portable ZIP without credentials, VCS data or build environments."""
from pathlib import Path
import hashlib
import zipfile

ROOT = Path(__file__).resolve().parents[1]
# Explicit inclusion avoids accidentally distributing local credentials or old ZIPs.
FOLDERS = ("medtech", "tests", "docs", "demo", "examples", "deploy", "slides", "scripts", ".github")
FILES = ("README.md", ".gitignore", "config.example.json", "pyproject.toml", "requirements.txt", "requirements-dev.lock", "requirements-slides.txt", "report.schema.json", "template.yaml")
EXCLUDED_PARTS = {"__pycache__", ".pytest_cache", "package", "node_modules", ".DS_Store"}
output = ROOT / "downloads/medtech-compliance-checker.zip"
paths = [ROOT / name for name in FILES if (ROOT / name).is_file()]
for folder in FOLDERS:
    for path in (ROOT / folder).rglob("*"):
        if path.is_file() and not path.is_symlink() and not EXCLUDED_PARTS.intersection(path.relative_to(ROOT).parts) and path.suffix != ".pyc":
            paths.append(path)
output.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(paths):
        info = zipfile.ZipInfo(path.relative_to(ROOT).as_posix(), date_time=(2026, 10, 16, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, path.read_bytes())
digest = hashlib.sha256(output.read_bytes()).hexdigest()
output.with_suffix(output.suffix + ".sha256").write_text(f"{digest}  {output.name}\n")
print(f"Packaged {len(paths)} files: {output}")
print(f"SHA256 {digest}")
