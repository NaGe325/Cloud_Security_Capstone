"""Read-only security checks. API errors remain UNKNOWN, never false PASS."""
from botocore.exceptions import BotoCoreError, ClientError
from .report import finding

BPA = ("BlockPublicAcls", "IgnorePublicAcls", "BlockPublicPolicy", "RestrictPublicBuckets")
ERRORS = (ClientError, BotoCoreError)


def error_code(exc):
    return exc.response["Error"]["Code"] if isinstance(exc, ClientError) else type(exc).__name__


def optional(call, absent, **params):
    try:
        return call(**params)
    except ClientError as exc:
        if error_code(exc) in absent:
            return {}
        raise


def all_pages(client, operation, result, **params):
    # Consume all pages before reporting inventory PASS; errors bubble to scope UNKNOWN.
    return [v for page in client.get_paginator(operation).paginate(**params) for v in page.get(result, [])]


class Scanner:
    def __init__(self, provider, scope):
        self.provider, self.scope = provider, scope
        self.findings = []

    def add(self, *args, **kwargs):
        self.findings.append(finding(*args, **kwargs))

    def guarded(self, control, resource, region, fn):
        try:
            fn()
        except ERRORS as exc:
            self.add(control, resource, region, "UNKNOWN", "INFORMATIONAL", "AWS evidence unavailable; review permissions, throttling, region, or resource deletion.", {"error_code": error_code(exc)})

    def run(self):
        for bucket, region in self.scope.buckets.items():
            for control, fn in (("S3_PUBLIC_ACCESS", self.s3_public), ("S3_ENCRYPTION", self.s3_encryption)):
                self.guarded(control, bucket, region, lambda f=fn: f(bucket, region))
        self.guarded("IAM_MFA", "root", "global", self.root_mfa)
        self.guarded("IAM_MFA", "iam-user-inventory", "global", self.iam_users)
        for region in self.scope.regions:
            self.guarded("EC2_ADMIN_PORTS", "security-group-inventory", region, lambda: self.ec2(region))
            self.guarded("CLOUDTRAIL_LOGGING", "regional-management-events", region, lambda: self.cloudtrail(region))
        return self.findings

    def s3_public(self, bucket, region):
        s3 = self.provider.client("s3", region)
        params = {"Bucket": bucket, "ExpectedBucketOwner": self.scope.account_id}
        # Missing configurations are known false; denied reads are unknown. A fully
        # protective known layer is sufficient even if the other layer is unreadable.
        layers, errors = {}, {}
        for label, client, kwargs in (("bucket", s3, params), ("account", self.provider.client("s3control", region), {"AccountId": self.scope.account_id})):
            try:
                layers[label] = optional(client.get_public_access_block, {"NoSuchPublicAccessBlockConfiguration"}, **kwargs).get("PublicAccessBlockConfiguration", {})
            except ERRORS as exc:
                errors[label] = error_code(exc)
        effective = {k: any(layer.get(k, False) for layer in layers.values()) for k in BPA}
        evidence = {"layers": layers, "effective_known_flags": effective, "read_errors": errors}
        if all(effective.values()):
            status, reason = "PASS", "All four Block Public Access flags enforced by the account/bucket combination."
        elif errors:
            status, reason = "UNKNOWN", "Cannot resolve effective Block Public Access because a layer is unreadable."
        else:
            status, reason = "FAIL", "Public-access prevention baseline is incomplete; this does not prove data is public."
        self.add("S3_PUBLIC_ACCESS", bucket, region, status, "HIGH", reason, evidence,
                 "Review access requirements, then enable all four effective Block Public Access flags; inspect policies/ACLs separately.")

    def s3_encryption(self, bucket, region):
        response = optional(self.provider.client("s3", region).get_bucket_encryption,
                            {"ServerSideEncryptionConfigurationNotFoundError"}, Bucket=bucket, ExpectedBucketOwner=self.scope.account_id)
        rules = response.get("ServerSideEncryptionConfiguration", {}).get("Rules", [])
        algorithms = [r.get("ApplyServerSideEncryptionByDefault", {}).get("SSEAlgorithm") for r in rules]
        ok = bool(algorithms) and all(a in ("aws:kms", "aws:kms:dsse") for a in algorithms)
        self.add("S3_ENCRYPTION", bucket, region, "PASS" if ok else "FAIL", "MEDIUM",
                 "Default encryption meets the project KMS baseline." if ok else "Default encryption does not meet the project KMS baseline; SSE-S3 is still encryption.",
                 {"default_algorithms": algorithms or ["implicit SSE-S3"]},
                 "Review KMS key policy/cost, then configure SSE-KMS or DSSE-KMS; assess existing objects separately.")

    def root_mfa(self):
        summary = self.provider.client("iam", self.scope.regions[0]).get_account_summary()["SummaryMap"]
        enabled = summary.get("AccountMFAEnabled")
        status = "UNKNOWN" if enabled not in (0, 1) else "PASS" if enabled == 1 else "FAIL"
        self.add("IAM_MFA", "root", "global", status, "CRITICAL", "Root MFA enrollment baseline (centralized root credential removal needs manual exception review).",
                 {"AccountMFAEnabled": enabled}, "Protect root access with MFA or document and verify centralized root credential removal.")

    def iam_users(self):
        iam = self.provider.client("iam", self.scope.regions[0])
        users = all_pages(iam, "list_users", "Users")
        if not users:
            self.add("IAM_MFA", "iam-user-inventory", "global", "NOT_APPLICABLE", "INFORMATIONAL", "No IAM users found; federation/Identity Center MFA is outside scope.")
        for user in users:
            name = user["UserName"]
            self.guarded("IAM_MFA", name, "global", lambda: self.user_mfa(iam, name))

    def user_mfa(self, iam, name):
        login = optional(iam.get_login_profile, {"NoSuchEntity"}, UserName=name)
        if not login:
            self.add("IAM_MFA", name, "global", "NOT_APPLICABLE", "INFORMATIONAL", "No console login profile observed; API-key/STS MFA enforcement is outside scope.")
            return
        devices = all_pages(iam, "list_mfa_devices", "MFADevices", UserName=name)
        self.add("IAM_MFA", name, "global", "PASS" if devices else "FAIL", "HIGH", "Console IAM user has enrolled MFA." if devices else "Console IAM user has no enrolled MFA.",
                 {"console_login": True, "mfa_device_count": len(devices)}, "Enroll MFA for this console user; prefer federation and verify sign-in enforcement separately.")

    def ec2(self, region):
        groups = all_pages(self.provider.client("ec2", region), "describe_security_groups", "SecurityGroups")
        if not groups:
            self.add("EC2_ADMIN_PORTS", "security-group-inventory", region, "NOT_APPLICABLE", "INFORMATIONAL", "No security groups in this region.")
        for group in groups:
            exposed = []
            for rule in group.get("IpPermissions", []):
                proto = str(rule["IpProtocol"])
                ports = [p for p in (22, 3389) if proto == "-1" or (proto in ("tcp", "6", "udp", "17") and rule.get("FromPort", 65536) <= p <= rule.get("ToPort", -1))]
                cidrs = [v["CidrIp"] for v in rule.get("IpRanges", []) if v["CidrIp"] == "0.0.0.0/0"]
                cidrs += [v["CidrIpv6"] for v in rule.get("Ipv6Ranges", []) if v["CidrIpv6"] == "::/0"]
                if ports and cidrs:
                    exposed.append({"protocol": proto, "ports": ports, "cidrs": cidrs})
            self.add("EC2_ADMIN_PORTS", group["GroupId"], region, "FAIL" if exposed else "PASS", "HIGH",
                     "Internet-wide administrative port rule found; actual reachability is not tested." if exposed else "No direct /0 IPv4/IPv6 SSH or RDP ingress rule found.",
                     {"exposed_rules": exposed}, "Restrict administrative ingress to approved sources or use Systems Manager Session Manager.")

    def cloudtrail(self, region):
        trails = self.provider.client("cloudtrail", region).describe_trails(includeShadowTrails=True).get("trailList", [])
        candidates, errors = [], []
        for trail in trails:
            if not (trail.get("IsMultiRegionTrail") or trail.get("HomeRegion") == region):
                continue
            arn = trail["TrailARN"]
            try:
                home = self.provider.client("cloudtrail", trail["HomeRegion"])
                status = home.get_trail_status(Name=arn)
                selectors = home.get_event_selectors(TrailName=arn)
                management = full_management_events(selectors)
                ok = status.get("IsLogging") is True and not status.get("LatestDeliveryError") and management and trail.get("IncludeGlobalServiceEvents") is True
                candidates.append({"trail_arn": arn, "home_region": trail["HomeRegion"], "is_logging": status.get("IsLogging"),
                                   "global_service_events": trail.get("IncludeGlobalServiceEvents"), "full_management_events": management,
                                   "delivery_error_present": bool(status.get("LatestDeliveryError")), "qualifies": ok})
            except ERRORS as exc:
                errors.append({"trail_arn": arn, "error_code": error_code(exc)})
        passed = any(v["qualifies"] for v in candidates)
        state = "PASS" if passed else "UNKNOWN" if errors else "FAIL"
        self.add("CLOUDTRAIL_LOGGING", "regional-management-events", region, state, "HIGH",
                 "At least one qualifying active trail covers this region." if passed else "No proven qualifying active trail; inspect management-event coverage and delivery status.",
                 {"trails": candidates, "read_errors": errors}, "Enable a covering trail with logging, global events, all read/write management events, and healthy delivery.")


def full_management_events(selectors):
    """Accept provably complete management selectors; custom filters stay nonqualifying."""
    reads, writes = False, False
    for s in selectors.get("EventSelectors", []):
        if s.get("IncludeManagementEvents", True) and not s.get("ExcludeManagementEventSources"):
            reads |= s.get("ReadWriteType", "All") in ("All", "ReadOnly")
            writes |= s.get("ReadWriteType", "All") in ("All", "WriteOnly")
    for s in selectors.get("AdvancedEventSelectors", []):
        fields = s.get("FieldSelectors", [])
        category = [f for f in fields if f.get("Field") == "eventCategory"]
        if len(category) != 1 or category[0] != {"Field": "eventCategory", "Equals": ["Management"]}:
            continue
        rest = [f for f in fields if f.get("Field") != "eventCategory"]
        if not rest:
            reads, writes = True, True
        elif len(rest) == 1 and rest[0].get("Field") == "readOnly" and set(rest[0]) == {"Field", "Equals"}:
            reads |= "true" in rest[0]["Equals"]
            writes |= "false" in rest[0]["Equals"]
    return reads and writes
