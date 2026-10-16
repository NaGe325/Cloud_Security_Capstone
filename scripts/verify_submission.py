"""Offline submission checks. No deployment, real AWS scanning or notifications."""
import json
import platform
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run(args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True)

def main():
    results = {"date_utc": datetime.now(timezone.utc).isoformat(), "python": platform.python_version(),
               "scope": "offline tests, template lint and deterministic reports only", "checks": []}
    test = run([sys.executable, "-m", "pytest", "--cov=medtech", "--cov-report=term-missing"])
    (ROOT / "examples/test-results-current.txt").write_text(test.stdout + test.stderr)
    results["checks"].append({"name": "pytest", "exit_code": test.returncode, "log": "examples/test-results-current.txt"})
    lint = run([sys.executable, "-c", "import sys; from cfnlint.runner import main; sys.exit(main())", "template.yaml"])
    results["checks"].append({"name": "cfn-lint", "exit_code": lint.returncode, "output": lint.stdout + lint.stderr})
    with tempfile.TemporaryDirectory() as tmp:
        for scenario, code in (("compliant", 0), ("misconfigured", 1), ("incomplete", 2)):
            result = run([sys.executable, "-m", "medtech.cli", "demo", scenario, "--out", tmp])
            comparisons = {}
            for suffix in ("json", "md", "html", "delivery.json"):
                generated = Path(tmp) / f"{scenario}.{suffix}"
                comparisons[suffix] = generated.is_file() and generated.read_bytes() == (ROOT / "examples" / generated.name).read_bytes()
            good = result.returncode == code and all(comparisons.values())
            results["checks"].append({"name": scenario, "exit_code": 0 if good else 1,
                "cli_exit_code": result.returncode, "expected_cli_exit_code": code, "byte_identical": comparisons})
    value = run([sys.executable, "scripts/value_model.py"])
    good = value.returncode == 0 and json.loads(value.stdout) == json.loads((ROOT / "examples/value-model.json").read_text())
    results["checks"].append({"name": "value-model", "exit_code": 0 if good else 1})
    results["cloud_deployment"] = "NOT_PERFORMED"
    results["real_notifications"] = "NOT_SENT"
    results["status"] = "PASS" if all(c["exit_code"] == 0 for c in results["checks"]) else "FAIL"
    (ROOT / "examples/submission-validation.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    return 0 if results["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
