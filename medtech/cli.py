"""Offline first command line; live scan is opt-in and never publishes."""
import argparse
import json
from pathlib import Path
import uuid
from .aws import AWS
from .checks import Scanner
from .config import Scope
from .delivery import deliver
from .offline import Offline
from .report import report, markdown
from .html_report import render_html

ROOT = Path(__file__).resolve().parent


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    demo = commands.add_parser("demo", help="fully offline AWS response replay")
    demo.add_argument("scenario", choices=("compliant", "misconfigured", "incomplete"))
    demo.add_argument("--out", type=Path, default=Path("reports"))
    aws = commands.add_parser("scan", help="explicitly authorized read-only AWS scan")
    aws.add_argument("--config", type=Path, required=True)
    aws.add_argument("--allow-aws-read", action="store_true")
    aws.add_argument("--out", type=Path, default=Path("reports"))
    args = parser.parse_args(argv)
    if args.command == "demo":
        with Offline(ROOT / "fixtures" / f"{args.scenario}.json") as provider:
            scope = Scope.from_dict(provider.fixture["scope"])
            data = report(scope, Scanner(provider, scope).run(), "SIMULATED", f"demo-{args.scenario}", provider.fixture["timestamp"])
        name = args.scenario
    else:
        if not args.allow_aws_read:
            parser.error("live reads disabled; --allow-aws-read requires prior account-owner authorization")
        scope = Scope.from_dict(json.loads(args.config.read_text()))
        provider = AWS()
        provider.verify_account(scope)
        data = report(scope, Scanner(provider, scope).run(), "AWS_READ_ONLY_SCAN", uuid.uuid4().hex)
        name = data["run_id"]
    args.out.mkdir(parents=True, exist_ok=True)
    delivery = deliver(data)
    (args.out / f"{name}.json").write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    (args.out / f"{name}.md").write_text(markdown(data))
    (args.out / f"{name}.delivery.json").write_text(json.dumps(delivery, indent=2, sort_keys=True) + "\n")
    (args.out / f"{name}.html").write_text(render_html(data))
    print(json.dumps({"report": str(args.out / f"{name}.json"), "summary": data["summary"], "sns": delivery["sns"]}, indent=2))
    # FAIL takes precedence over UNKNOWN, while coverage stays explicitly incomplete.
    return 1 if data["summary"]["counts"]["FAIL"] else 2 if data["summary"]["counts"]["UNKNOWN"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
