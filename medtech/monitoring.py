"""Optional CloudWatch metrics. Disabled unless the operator explicitly opts in."""
NAMESPACE = "MedTech/SecurityBaseline"


def publish_metrics(data, provider=None, region=None, enabled=False):
    if not enabled:
        return {"status": "DISABLED"}
    if provider is None or not region:
        raise ValueError("metrics require an AWS provider and region")
    counts = data["summary"]["counts"]
    provider.client("cloudwatch", region).put_metric_data(Namespace=NAMESPACE, MetricData=[
        {"MetricName": "FailedFindings", "Value": counts["FAIL"], "Unit": "Count"},
        {"MetricName": "UnknownFindings", "Value": counts["UNKNOWN"], "Unit": "Count"},
        {"MetricName": "CompletedRuns", "Value": 1, "Unit": "Count"},
    ])
    return {"status": "PUBLISHED", "namespace": NAMESPACE}
