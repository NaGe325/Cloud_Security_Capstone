# MedTech AWS security baseline report

Five technical controls only; not a HIPAA compliance determination. PASS applies only to this baseline and explicit scope.

Run: `demo-compliant` · Mode: **SIMULATED** · Time: 2026-10-11T12:00:00+00:00
Result: **PASS** · Coverage: **COMPLETE_WITHIN_SCOPE**

Counts: {"PASS": 6, "FAIL": 0, "UNKNOWN": 0, "NOT_APPLICABLE": 1}
Assessed-resource pass rate: 100.0% (excludes UNKNOWN and NOT_APPLICABLE).

| Control | Resource | Region | Result | Risk | Explanation |
|---|---|---|---|---|---|
| CLOUDTRAIL_LOGGING | regional-management-events | us-east-1 | PASS | INFORMATIONAL | At least one qualifying active trail covers this region. |
| EC2_ADMIN_PORTS | sg-0123456789abcdef0 | us-east-1 | PASS | INFORMATIONAL | No direct /0 IPv4/IPv6 SSH or RDP ingress rule found. |
| IAM_MFA | analyst | global | PASS | INFORMATIONAL | Console IAM user has enrolled MFA. |
| IAM_MFA | root | global | PASS | INFORMATIONAL | Root MFA enrollment baseline (centralized root credential removal needs manual exception review). |
| IAM_MFA | service-backend | global | NOT_APPLICABLE | INFORMATIONAL | No console login profile observed; API-key/STS MFA enforcement is outside scope. |
| S3_ENCRYPTION | medtech-demo-patient-data | us-east-1 | PASS | INFORMATIONAL | Default encryption meets the project KMS baseline. |
| S3_PUBLIC_ACCESS | medtech-demo-patient-data | us-east-1 | PASS | INFORMATIONAL | All four Block Public Access flags enforced by the account/bucket combination. |

## Remediation proposals (never applied automatically)

