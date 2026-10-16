"""Measure local synthetic scanner execution; never measures live AWS latency."""
import json
import platform
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path
from medtech.config import Scope
from medtech.checks import Scanner
from medtech.offline import Offline
from medtech.report import report

ROOT = Path(__file__).resolve().parents[1]
results = {}
for scenario in ("compliant", "misconfigured", "incomplete"):
    samples = []
    for _ in range(5):
        start = time.perf_counter()
        with Offline(ROOT / "medtech/fixtures" / f"{scenario}.json") as provider:
            scope = Scope.from_dict(provider.fixture["scope"])
            data = report(scope, Scanner(provider, scope).run(), "SIMULATED", f"demo-{scenario}", provider.fixture["timestamp"])
        samples.append(round(time.perf_counter() - start, 6))
        expected = json.loads((ROOT / "examples" / f"{scenario}.json").read_text())
        assert data == expected, f"Report mismatch: {scenario}"
    results[scenario] = {"runs": 5, "seconds": samples, "median_seconds": round(statistics.median(samples), 6), "matches_committed_report": True}
print(json.dumps({"mode": "OFFLINE_SYNTHETIC_NOT_AWS_LATENCY", "timestamp": datetime.now(timezone.utc).isoformat(),
    "python": platform.python_version(), "platform": platform.platform(), "includes": "boto3 client construction, Stubber setup, scanner and report construction",
    "excludes": "real network latency, report file I/O, cloud delivery, human review", "scenarios": results}, indent=2))
