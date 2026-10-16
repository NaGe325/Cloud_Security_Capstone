"""Reproduce the illustrative economics. No network, AWS calls or dependencies."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def calculate():
    # us-east-1 planning inputs, USD, before free-tier credits. Not a bill.
    runs = 30
    costs = {
        "lambda_compute": runs * .25 * 30 * .0000133334,
        "lambda_requests": runs * .20 / 1_000_000,
        "s3_report_puts": 2 * runs * .005 / 1000,
        "s3_report_storage": .006 * .023,
        "s3_read_request_allowance": 1000 * .0004 / 1000,
        "kms_request_allowance": 1000 * .03 / 10000,
        "sns_publish": runs * .50 / 1_000_000,
        "sns_email_one_recipient": runs * 2 / 100000,
        "cloudwatch_log_ingestion": .01 * .50,
        "cloudwatch_log_storage": .01 * .03,
        "sqs_request_allowance": 100 * .40 / 1_000_000,
        "eventbridge_legacy_scheduled_rule": 0,
    }
    base = sum(costs.values())
    optional = {"three_custom_metrics": 3 * .30, "one_dashboard": 3.0, "two_standard_alarms": 2 * .10}
    return {
        "classification": "ILLUSTRATIVE_ESTIMATE_NOT_MEASURED_AWS_COST",
        "region": "us-east-1", "pricing_review_date": "2026-10-16", "currency": "USD",
        "assumptions": {"runs_per_30_days": runs, "memory_gb": .25,
            "assumed_billed_duration_seconds": 30, "manual_minutes_per_run": 15,
            "automated_human_review_minutes_per_run": 5, "labor_usd_per_hour": 60},
        "monthly_cost_components": costs,
        "base_monthly_usd": round(base, 6),
        "optional_monitoring_components": optional,
        "with_monitoring_monthly_usd": round(base + sum(optional.values()), 6),
        "illustrative_monthly_hours_released": runs * (15 - 5) / 60,
        "illustrative_monthly_capacity_value_usd": runs * (15 - 5) / 60 * 60,
        "exclusions": ["free-tier credits", "taxes", "human setup and maintenance",
            "existing assessed workloads and CloudTrail storage", "internet egress",
            "unbounded retries, SNS duplicates, extra metrics, console/API reads"],
    }

if __name__ == "__main__":
    print(json.dumps(calculate(), indent=2, sort_keys=True))
