"""Only explicit opt-in writes. SNS payloads contain summary counts, never evidence."""
import json
from .html_report import render_html


def notification(data, report_uri=None):
    summary = data["summary"]
    if not (summary["counts"]["FAIL"] or summary["counts"]["UNKNOWN"]):
        return None
    return {"Subject": f"MedTech baseline: {summary['status']}",
            "Message": json.dumps({"run_id": data["run_id"], "status": summary["status"],
                                   "coverage": summary["coverage"], "counts": summary["counts"],
                                   "report_uri": report_uri, "notice": "Review restricted report. This is not a HIPAA compliance determination."}, sort_keys=True)}


def deliver(data, provider=None, region=None, bucket=None, topic=None, enable_s3=False, enable_sns=False):
    key = f"reports/{data['run_id']}.json"
    uri = f"s3://{bucket}/{key}" if bucket else None
    result = {"s3": "DISABLED", "sns": "NOT_REQUIRED", "report_uri": None}
    if enable_s3:
        if not bucket or provider is None or not region:
            raise ValueError("S3 delivery needs bucket, region, and provider")
        provider.client("s3", region).put_object(Bucket=bucket, Key=key,
            Body=json.dumps(data, sort_keys=True, indent=2).encode(), ContentType="application/json",
            ServerSideEncryption="aws:kms", ExpectedBucketOwner=data["scope"]["account_id"])
        html_key = f"reports/{data['run_id']}.html"
        provider.client("s3", region).put_object(Bucket=bucket, Key=html_key,
            Body=render_html(data).encode(), ContentType="text/html; charset=utf-8",
            ServerSideEncryption="aws:kms", ExpectedBucketOwner=data["scope"]["account_id"])
        result.update(s3="STORED", report_uri=uri, html_report_uri=f"s3://{bucket}/{html_key}")
    message = notification(data, result["report_uri"])
    if message:
        result["sns"] = "PREVIEW_ONLY"
        result["notification_preview"] = message
        if enable_sns:
            if not topic or provider is None or not region:
                raise ValueError("SNS delivery needs topic, region, and provider")
            provider.client("sns", region).publish(TopicArn=topic, **message)
            result["sns"] = "PUBLISHED"
    return result
