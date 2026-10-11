"""Safety contracts for a template that could later create real cloud resources."""
from pathlib import Path
from cfnlint.decode import decode

ROOT=Path(__file__).resolve().parents[1]


def test_template_safety_defaults():
    template, errors=decode(str(ROOT/"template.yaml"))
    assert not errors
    params=template["Parameters"]
    assert params["ScanMode"]["Default"]=="demo"
    assert params["EmailEndpoint"]["Default"]==""
    for name in ("AllowAwsReads","EnableReportWrite","EnableNotifications","EnableSchedule","EnableMonitoring"):
        assert params[name]["Default"]=="false"
    resources=template["Resources"]
    assert resources["EmailSubscription"]["Condition"]=="SubscribeEmail"
    bucket=resources["ReportBucket"]
    assert bucket["DeletionPolicy"]=="Retain"
    assert all(bucket["Properties"]["PublicAccessBlockConfiguration"].values())
    role=resources["CheckerRole"]["Properties"]
    policies=role["Policies"]
    assert [p["Fn::If"][0] for p in policies if "Fn::If" in p]==["CloudReadsEnabled","MonitoringEnabled","S3WriteEnabled","SNSPublishEnabled"]
    assert resources["Checker"]["Properties"]["EventInvokeConfig"]["MaximumRetryAttempts"]==2
