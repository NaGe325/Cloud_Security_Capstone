from copy import deepcopy
import json
from pathlib import Path
import pytest
from jsonschema import validate
from medtech.checks import Scanner, full_management_events
from medtech.config import Scope
from medtech.offline import Offline
from medtech.report import report
from medtech.delivery import deliver, notification
from medtech.html_report import render_html
from medtech.lambda_handler import handler
from medtech.cli import main

ROOT = Path(__file__).resolve().parents[1]
REGION = "us-east-1"


def fixture(name="compliant"):
    return json.loads((ROOT / "medtech" / "fixtures" / f"{name}.json").read_text())


def run(data):
    with Offline(data) as provider:
        scope = Scope.from_dict(data["scope"])
        return report(scope, Scanner(provider, scope).run(), "SIMULATED", "test-run", data["timestamp"])


def call(data, service, operation):
    return next(c for c in data["clients"][f"{service}:{REGION}"] if c["operation"] == operation)


def select(result, control, resource=None):
    return next(f for f in result["findings"] if f["control_id"] == control and (resource is None or f["resource"] == resource))


@pytest.mark.parametrize("scenario,counts,status", [
    ("compliant", {"PASS":6,"FAIL":0,"UNKNOWN":0,"NOT_APPLICABLE":1}, "PASS"),
    ("misconfigured", {"PASS":0,"FAIL":6,"UNKNOWN":0,"NOT_APPLICABLE":1}, "FAIL"),
])
def test_end_to_end(scenario, counts, status):
    data = run(fixture(scenario))
    assert data["summary"]["counts"] == counts
    assert data["summary"]["status"] == status
    assert len(data["summary"]["controls"]) == 5
    validate(data, json.loads((ROOT / "report.schema.json").read_text()))


def test_account_bpa_overrides_bucket():
    data = fixture("misconfigured")
    call(data,"s3control","get_public_access_block")["response"]["PublicAccessBlockConfiguration"] = dict.fromkeys(["BlockPublicAcls","IgnorePublicAcls","BlockPublicPolicy","RestrictPublicBuckets"],True)
    assert select(run(data),"S3_PUBLIC_ACCESS")["status"] == "PASS"


def test_combined_partial_bpa():
    data = fixture("misconfigured")
    for service, flags in [("s3",["BlockPublicAcls","IgnorePublicAcls"]),("s3control",["BlockPublicPolicy","RestrictPublicBuckets"])]:
        call(data,service,"get_public_access_block")["response"]["PublicAccessBlockConfiguration"].update(dict.fromkeys(flags,True))
    assert select(run(data),"S3_PUBLIC_ACCESS")["status"] == "PASS"


@pytest.mark.parametrize("good_bucket,expected", [(True,"PASS"),(False,"UNKNOWN")])
def test_unreadable_account_bpa(good_bucket, expected):
    data = fixture("compliant" if good_bucket else "misconfigured")
    c = call(data,"s3control","get_public_access_block")
    c.pop("response"); c["error"] = "AccessDenied"
    assert select(run(data),"S3_PUBLIC_ACCESS")["status"] == expected


@pytest.mark.parametrize("algorithm,expected", [("AES256","FAIL"),("aws:kms","PASS"),("aws:kms:dsse","PASS")])
def test_encryption(algorithm, expected):
    data = fixture()
    call(data,"s3","get_bucket_encryption")["response"]["ServerSideEncryptionConfiguration"]["Rules"][0]["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"] = algorithm
    assert select(run(data),"S3_ENCRYPTION")["status"] == expected


def test_missing_encryption_config_is_not_unencrypted():
    data = fixture()
    c=call(data,"s3","get_bucket_encryption"); c.pop("response"); c["error"]="ServerSideEncryptionConfigurationNotFoundError"
    f=select(run(data),"S3_ENCRYPTION")
    assert f["status"] == "FAIL"
    assert "SSE-S3 is still encryption" in f["reason"]


@pytest.mark.parametrize("service,operation,control,resource", [
    ("s3","get_bucket_encryption","S3_ENCRYPTION",None),
    ("iam","get_account_summary","IAM_MFA","root"),
    ("ec2","describe_security_groups","EC2_ADMIN_PORTS",None),
])
@pytest.mark.parametrize("error", ["AccessDenied","ThrottlingException","InternalError"])
def test_aws_errors_are_unknown(service,operation,control,resource,error):
    data=fixture(); c=call(data,service,operation); c.pop("response"); c["error"]=error
    result=run(data)
    assert select(result,control,resource)["status"]=="UNKNOWN"
    assert result["summary"]["coverage"]=="INCOMPLETE"
    assert result["summary"]["status"]=="INCOMPLETE"
    assert notification(result) is not None


@pytest.mark.parametrize("proto,low,high,cidr,expected", [
    ("tcp",22,22,"0.0.0.0/0","FAIL"),("6",0,65535,"::/0","FAIL"),
    ("-1",None,None,"::/0","FAIL"),("udp",3389,3389,"::/0","FAIL"),
    ("tcp",443,443,"0.0.0.0/0","PASS"),("icmp",-1,-1,"0.0.0.0/0","PASS"),
    ("tcp",22,22,"10.0.0.0/8","PASS"),("tcp",3389,3389,"fd00::/8","PASS"),
])
def test_security_group_rule_semantics(proto,low,high,cidr,expected):
    data=fixture(); rule={"IpProtocol":proto}
    if low is not None: rule.update(FromPort=low,ToPort=high)
    rule["Ipv6Ranges" if ":" in cidr else "IpRanges"]=[{"CidrIpv6" if ":" in cidr else "CidrIp":cidr}]
    call(data,"ec2","describe_security_groups")["response"]["SecurityGroups"][0]["IpPermissions"]=[rule]
    assert select(run(data),"EC2_ADMIN_PORTS")["status"]==expected


def test_ec2_second_page_not_missed():
    data=fixture(); first=call(data,"ec2","describe_security_groups")
    second=deepcopy(first); second["params"]={"NextToken":"page2"}
    second["response"]["SecurityGroups"][0]["GroupId"]="sg-22222222222222222"
    second["response"]["SecurityGroups"][0]["IpPermissions"][0]["IpRanges"][0]["CidrIp"]="0.0.0.0/0"
    first["response"]["NextToken"]="page2"
    data["clients"][f"ec2:{REGION}"].append(second)
    assert select(run(data),"EC2_ADMIN_PORTS","sg-22222222222222222")["status"]=="FAIL"


def test_iam_user_and_mfa_pagination():
    data=fixture(); calls=data["clients"][f"iam:{REGION}"]
    listing=call(data,"iam","list_users")
    second_user=listing["response"]["Users"].pop()
    listing["response"].update(IsTruncated=True,Marker="page2")
    calls.insert(2,{"operation":"list_users","params":{"Marker":"page2"},"response":{"Users":[second_user],"IsTruncated":False}})
    mfa=call(data,"iam","list_mfa_devices"); devices=mfa["response"]["MFADevices"]
    mfa["response"]={"MFADevices":[],"IsTruncated":True,"Marker":"mfa2"}
    calls.insert(calls.index(mfa)+1,{"operation":"list_mfa_devices","params":{"UserName":"analyst","Marker":"mfa2"},"response":{"MFADevices":devices,"IsTruncated":False}})
    result=run(data)
    assert select(result,"IAM_MFA","analyst")["status"]=="PASS"
    assert select(result,"IAM_MFA","service-backend")["status"]=="NOT_APPLICABLE"


def test_login_profile_denied_not_service_account():
    data=fixture(); c=call(data,"iam","get_login_profile"); c.pop("response"); c["error"]="AccessDenied"
    data["clients"][f"iam:{REGION}"]=[c for c in data["clients"][f"iam:{REGION}"] if c["operation"]!="list_mfa_devices"]
    assert select(run(data),"IAM_MFA","analyst")["status"]=="UNKNOWN"


@pytest.mark.parametrize("mutation", ["stopped","delivery_error","data_only","write_only","no_global","no_trail"])
def test_cloudtrail_nonqualifying(mutation):
    data=fixture(); status=call(data,"cloudtrail","get_trail_status")["response"]
    selectors=call(data,"cloudtrail","get_event_selectors")["response"]["EventSelectors"][0]
    if mutation=="stopped": status["IsLogging"]=False
    if mutation=="delivery_error": status["LatestDeliveryError"]="AccessDenied"
    if mutation=="data_only": selectors["IncludeManagementEvents"]=False
    if mutation=="write_only": selectors["ReadWriteType"]="WriteOnly"
    if mutation=="no_global": call(data,"cloudtrail","describe_trails")["response"]["trailList"][0]["IncludeGlobalServiceEvents"]=False
    if mutation=="no_trail":
        c=call(data,"cloudtrail","describe_trails"); c["response"]["trailList"]=[]
        data["clients"][f"cloudtrail:{REGION}"]=[c]
    assert select(run(data),"CLOUDTRAIL_LOGGING")["status"]=="FAIL"


def test_cloudtrail_uses_home_region():
    data=fixture(); calls=data["clients"][f"cloudtrail:{REGION}"]
    trail=calls[0]["response"]["trailList"][0]
    trail["HomeRegion"]="us-west-2"
    trail["TrailARN"]=trail["TrailARN"].replace(REGION,"us-west-2")
    calls[1]["params"]["Name"]=trail["TrailARN"]
    calls[2]["params"]["TrailName"]=trail["TrailARN"]
    data["clients"]["cloudtrail:us-west-2"]=calls[1:]
    data["clients"][f"cloudtrail:{REGION}"]=calls[:1]
    assert select(run(data),"CLOUDTRAIL_LOGGING")["status"]=="PASS"


def test_cloudtrail_denied_status():
    data=fixture(); c=call(data,"cloudtrail","get_trail_status"); c.pop("response"); c["error"]="AccessDeniedException"
    data["clients"][f"cloudtrail:{REGION}"]=[c for c in data["clients"][f"cloudtrail:{REGION}"] if c["operation"]!="get_event_selectors"]
    assert select(run(data),"CLOUDTRAIL_LOGGING")["status"]=="UNKNOWN"


@pytest.mark.parametrize("selectors,expected", [
    ({"EventSelectors":[{"ReadWriteType":"ReadOnly"},{"ReadWriteType":"WriteOnly"}]},True),
    ({"EventSelectors":[{"ReadWriteType":"All","ExcludeManagementEventSources":["kms.amazonaws.com"]}]},False),
    ({"AdvancedEventSelectors":[{"FieldSelectors":[{"Field":"eventCategory","Equals":["Management"]}]}]},True),
    ({"AdvancedEventSelectors":[{"FieldSelectors":[{"Field":"eventCategory","Equals":["Management"]},{"Field":"eventName","Equals":["CreateUser"]}]}]},False),
    ({},False),
])
def test_management_selectors(selectors,expected):
    assert full_management_events(selectors)==expected


def test_delivery_disabled_no_provider_needed():
    result=deliver(run(fixture("misconfigured")))
    assert result["s3"]=="DISABLED" and result["sns"]=="PREVIEW_ONLY"
    assert "analyst" not in result["notification_preview"]["Message"]
    assert notification(run(fixture())) is None


def test_s3_sns_writes_with_stubber():
    data=run(fixture("misconfigured")); bucket="medtech-report-demo"; topic="arn:aws:sns:us-east-1:123456789012:medtech"
    msg=notification(data,f"s3://{bucket}/reports/test-run.json")
    f={"clients":{
        f"s3:{REGION}":[{"operation":"put_object","params":{"Bucket":bucket,"Key":"reports/test-run.json","Body":json.dumps(data,sort_keys=True,indent=2).encode(),"ContentType":"application/json","ServerSideEncryption":"aws:kms","ExpectedBucketOwner":"123456789012"},"response":{}}],
        f"sns:{REGION}":[{"operation":"publish","params":{"TopicArn":topic,**msg},"response":{"MessageId":"offline-id"}}]}}
    f["clients"][f"s3:{REGION}"].append({"operation":"put_object","params":{"Bucket":bucket,"Key":"reports/test-run.html","Body":render_html(data).encode(),"ContentType":"text/html; charset=utf-8","ServerSideEncryption":"aws:kms","ExpectedBucketOwner":"123456789012"},"response":{}})
    with Offline(f) as provider:
        result=deliver(data,provider,REGION,bucket,topic,True,True)
    assert result["s3"]=="STORED" and result["sns"]=="PUBLISHED"


def test_delivery_failure_propagates_for_lambda_retry():
    data=run(fixture("misconfigured"))
    class Broken:
        def client(self,*args): return self
        def put_object(self,**kwargs): raise RuntimeError("simulated storage failure")
        def publish(self,**kwargs): pytest.fail("must store before alert")
    with pytest.raises(RuntimeError): deliver(data,Broken(),REGION,"bucket","topic",True,True)


def test_lambda_demo_ignores_event_and_write_flags(monkeypatch):
    monkeypatch.setenv("SCAN_MODE","demo"); monkeypatch.setenv("ENABLE_SNS_PUBLISH","true"); monkeypatch.setenv("ENABLE_S3_WRITE","true")
    result=handler({"SCAN_MODE":"aws","ENABLE_SNS_PUBLISH":True},None)
    assert result["report"]["mode"]=="SIMULATED"
    assert result["delivery"]["sns"]=="PREVIEW_ONLY"


def test_lambda_live_guard(monkeypatch):
    monkeypatch.setenv("SCAN_MODE","aws"); monkeypatch.delenv("ALLOW_AWS_READS",raising=False)
    with pytest.raises(ValueError): handler({},None)


@pytest.mark.parametrize("scenario,exit_code",[("compliant",0),("misconfigured",1)])
def test_cli_demo_files(tmp_path,scenario,exit_code):
    assert main(["demo",scenario,"--out",str(tmp_path)])==exit_code
    assert (tmp_path/f"{scenario}.md").exists()
    assert json.loads((tmp_path/f"{scenario}.json").read_text())["mode"]=="SIMULATED"


def test_cli_cloud_guard(tmp_path):
    with pytest.raises(SystemExit) as exc: main(["scan","--config","not-read.json"])
    assert exc.value.code==2


@pytest.mark.parametrize("key,value",[("account_id","bad"),("regions",[]),("regions",["us-east-1","us-east-1"]),("buckets",{}),("buckets",{"bad_bucket":"us-east-1"}),("buckets",{"valid-bucket":"us-west-2"})])
def test_scope_validation(key,value):
    data=fixture()["scope"]; data[key]=value
    with pytest.raises(ValueError): Scope.from_dict(data)


def test_ids_stable_across_status_change():
    assert [f["id"] for f in run(fixture())["findings"]]==[f["id"] for f in run(fixture("misconfigured"))["findings"]]


def test_unknown_never_hidden_by_fail():
    data=fixture("misconfigured"); c=call(data,"s3","get_bucket_encryption"); c.pop("response"); c["error"]="AccessDenied"
    result=run(data)
    assert result["summary"]["status"]=="FAIL" and result["summary"]["coverage"]=="INCOMPLETE"


def test_empty_inventories_are_not_applicable():
    data=fixture(); calls=data["clients"][f"iam:{REGION}"]
    calls[1]["response"]={"Users":[],"IsTruncated":False}
    data["clients"][f"iam:{REGION}"]=calls[:2]
    call(data,"ec2","describe_security_groups")["response"]={"SecurityGroups":[]}
    result=run(data)
    assert select(result,"IAM_MFA","iam-user-inventory")["status"]=="NOT_APPLICABLE"
    assert select(result,"EC2_ADMIN_PORTS")["status"]=="NOT_APPLICABLE"


def test_missing_root_summary_unknown():
    data=fixture(); call(data,"iam","get_account_summary")["response"]={"SummaryMap":{}}
    assert select(run(data),"IAM_MFA","root")["status"]=="UNKNOWN"


def test_bpa_missing_both_layers_is_fail():
    data=fixture()
    for service in ("s3","s3control"):
        c=call(data,service,"get_public_access_block"); c.pop("response"); c["error"]="NoSuchPublicAccessBlockConfiguration"
    assert select(run(data),"S3_PUBLIC_ACCESS")["status"]=="FAIL"


def test_partial_inventory_failure_not_pass():
    data=fixture(); first=call(data,"ec2","describe_security_groups")
    first["response"]["NextToken"]="next"
    data["clients"][f"ec2:{REGION}"].append({"operation":"describe_security_groups","params":{"NextToken":"next"},"error":"RequestLimitExceeded"})
    assert select(run(data),"EC2_ADMIN_PORTS")["status"]=="UNKNOWN"


def test_advanced_read_write_union():
    selectors={"AdvancedEventSelectors":[{"FieldSelectors":[{"Field":"eventCategory","Equals":["Management"]},{"Field":"readOnly","Equals":[value]}]} for value in ["true","false"]]}
    assert full_management_events(selectors)
    selectors["AdvancedEventSelectors"][0]["FieldSelectors"][0]["Equals"]=["Data"]
    assert not full_management_events(selectors)


def test_live_lambda_path_with_fake_provider(monkeypatch):
    import medtech.lambda_handler as module
    data=fixture("misconfigured")
    with Offline(data) as provider:
        provider.verify_account=lambda scope: None
        monkeypatch.setattr(module,"AWS",lambda:provider)
        monkeypatch.setenv("SCAN_MODE","aws"); monkeypatch.setenv("ALLOW_AWS_READS","true")
        monkeypatch.setenv("SCAN_SCOPE_JSON",json.dumps(data["scope"])); monkeypatch.setenv("AWS_REGION",REGION)
        monkeypatch.setenv("ENABLE_S3_WRITE","false"); monkeypatch.setenv("ENABLE_SNS_PUBLISH","false")
        result=handler({},None)
    assert result["report"]["summary"]["counts"]["FAIL"]==6
    assert result["delivery"]["sns"]=="PREVIEW_ONLY"


def test_live_cli_with_fake_provider(monkeypatch,tmp_path):
    import medtech.cli as module
    data=fixture()
    config=tmp_path/"scope.json"; config.write_text(json.dumps(data["scope"]))
    with Offline(data) as provider:
        provider.verify_account=lambda scope: None
        monkeypatch.setattr(module,"AWS",lambda:provider)
        assert main(["scan","--config",str(config),"--allow-aws-read","--out",str(tmp_path/"report")])==0


@pytest.mark.parametrize("actual,expected,raises",[("123456789012","123456789012",False),("999999999999","123456789012",True)])
def test_account_identity_guard(actual,expected,raises):
    from medtech.aws import AWS
    data={"clients":{f"sts:{REGION}":[{"operation":"get_caller_identity","params":{},"response":{"Account":actual,"UserId":"example","Arn":f"arn:aws:iam::{actual}:user/test"}}]}}
    with Offline(data) as provider:
        aws=AWS.__new__(AWS); aws.client=provider.client
        scope=Scope.from_dict({"account_id":expected,"regions":[REGION],"buckets":{"example-bucket":REGION}})
        if raises:
            with pytest.raises(ValueError): aws.verify_account(scope)
        else: aws.verify_account(scope)


def test_client_factory_retries_and_reuse(monkeypatch):
    from medtech.aws import AWS
    import medtech.aws as module
    calls=[]
    class Session:
        def client(self,*args,**kwargs): calls.append((args,kwargs)); return object()
    monkeypatch.setattr(module.boto3,"Session",Session)
    provider=AWS()
    assert provider.client("s3",REGION) is provider.client("s3",REGION)
    assert len(calls)==1
    assert calls[0][1]["config"].retries["total_max_attempts"]==4


@pytest.mark.parametrize("service",["s3","sns"])
def test_delivery_missing_config_fails(service):
    with pytest.raises(ValueError): deliver(run(fixture("misconfigured")),enable_s3=service=="s3",enable_sns=service=="sns")


def test_offline_network_hook_blocks():
    with pytest.raises(RuntimeError): Offline.block_network()


def test_invalid_demo_scenario(monkeypatch):
    monkeypatch.setenv("SCAN_MODE","demo"); monkeypatch.setenv("DEMO_SCENARIO","../secrets")
    with pytest.raises(ValueError): handler({},None)


def test_invalid_region():
    data=fixture()["scope"]; data["regions"]=["not-a-region"]
    with pytest.raises(ValueError): Scope.from_dict(data)


def test_multiple_regions_no_iam_duplicates():
    data=fixture(); data["scope"]["regions"].append("us-west-2")
    data["clients"]["ec2:us-west-2"]=[{"operation":"describe_security_groups","params":{},"response":{"SecurityGroups":[]}}]
    data["clients"]["cloudtrail:us-west-2"]=[{"operation":"describe_trails","params":{"includeShadowTrails":True},"response":{"trailList":[]}}]
    result=run(data)
    assert len([f for f in result["findings"] if f["control_id"]=="IAM_MFA" and f["resource"]=="root"])==1
    trails=[f for f in result["findings"] if f["control_id"]=="CLOUDTRAIL_LOGGING"]
    assert {(f["region"],f["status"]) for f in trails}=={("us-east-1","PASS"),("us-west-2","FAIL")}


def test_sns_publish_failure_propagates():
    data=run(fixture("misconfigured")); topic="arn:aws:sns:us-east-1:123456789012:medtech"
    f={"clients":{f"sns:{REGION}":[{"operation":"publish","params":{"TopicArn":topic,**notification(data)},"error":"AuthorizationError"}]}}
    from botocore.exceptions import ClientError
    with Offline(f) as provider:
        with pytest.raises(ClientError): deliver(data,provider,REGION,topic=topic,enable_sns=True)


def test_nonqualifying_single_region_trail_not_counted():
    data=fixture(); c=call(data,"cloudtrail","describe_trails")
    c["response"]["trailList"][0].update(HomeRegion="us-west-2",IsMultiRegionTrail=False)
    data["clients"][f"cloudtrail:{REGION}"]=[c]
    assert select(run(data),"CLOUDTRAIL_LOGGING")["status"]=="FAIL"


def test_timeouts_become_unknown_without_false_pass():
    from botocore.exceptions import ReadTimeoutError
    data=fixture()
    class TimeoutProvider:
        def client(self,*args): return self
        def get_account_summary(self): raise ReadTimeoutError(endpoint_url="https://offline.invalid")
    scanner=Scanner(TimeoutProvider(),Scope.from_dict(data["scope"]))
    scanner.guarded("IAM_MFA","root","global",scanner.root_mfa)
    assert scanner.findings[0]["status"]=="UNKNOWN"
    assert scanner.findings[0]["evidence"]["error_code"]=="ReadTimeoutError"
