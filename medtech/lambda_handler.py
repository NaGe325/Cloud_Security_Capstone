"""EventBridge entry point. Event contents cannot enable cloud access or delivery."""
import json
import logging
import os
from pathlib import Path
import uuid
from .aws import AWS
from .checks import Scanner
from .config import Scope
from .delivery import deliver
from .offline import Offline
from .monitoring import publish_metrics
from .report import report

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
ROOT = Path(__file__).resolve().parent


def handler(event, context):
    # Ignore event-supplied scope/delivery options. Only operator environment controls mode.
    mode = os.environ.get("SCAN_MODE", "demo")
    if mode == "demo":
        scenario = os.environ.get("DEMO_SCENARIO", "misconfigured")
        if scenario not in ("compliant", "misconfigured", "incomplete"):
            raise ValueError("invalid demo scenario")
        with Offline(ROOT / "fixtures" / f"{scenario}.json") as provider:
            scope = Scope.from_dict(provider.fixture["scope"])
            data = report(scope, Scanner(provider, scope).run(), "SIMULATED", f"demo-{scenario}", provider.fixture["timestamp"])
        metrics = publish_metrics(data)
        delivery = deliver(data)  # No provider passed: even enabled env flags cannot write in demo mode.
    elif mode == "aws" and os.environ.get("ALLOW_AWS_READS") == "true":
        scope = Scope.from_dict(json.loads(os.environ["SCAN_SCOPE_JSON"]))
        provider = AWS()
        provider.verify_account(scope)
        data = report(scope, Scanner(provider, scope).run(), "AWS_READ_ONLY_SCAN", uuid.uuid4().hex)
        delivery = deliver(data, provider, os.environ["AWS_REGION"], os.environ.get("REPORT_BUCKET"),
                           os.environ.get("SNS_TOPIC_ARN"), os.environ.get("ENABLE_S3_WRITE") == "true",
                           os.environ.get("ENABLE_SNS_PUBLISH") == "true")
        metrics = publish_metrics(data, provider, os.environ["AWS_REGION"], os.environ.get("ENABLE_METRICS") == "true")
    else:
        raise ValueError("cloud scan requires SCAN_MODE=aws and ALLOW_AWS_READS=true")
    log.info(json.dumps({"run_id": data["run_id"], "summary": data["summary"], "delivery": {k: v for k, v in delivery.items() if k != "notification_preview"}}))
    return {"report": data, "delivery": delivery, "metrics": metrics}
