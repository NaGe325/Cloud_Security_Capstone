# MedTech AWS security baseline report

Five technical controls only; not a HIPAA compliance determination. PASS applies only to this baseline and explicit scope.

Run: `demo-misconfigured` · Mode: **SIMULATED** · Time: 2026-10-11T12:00:00+00:00
Result: **FAIL** · Coverage: **COMPLETE_WITHIN_SCOPE**

Counts: {"PASS": 0, "FAIL": 6, "UNKNOWN": 0, "NOT_APPLICABLE": 1}
Assessed-resource pass rate: 0.0% (excludes UNKNOWN and NOT_APPLICABLE).

| Control | Resource | Region | Result | Risk | Explanation |
|---|---|---|---|---|---|
| CLOUDTRAIL_LOGGING | regional-management-events | us-east-1 | FAIL | HIGH | No proven qualifying active trail; inspect management-event coverage and delivery status. |
| EC2_ADMIN_PORTS | sg-0123456789abcdef0 | us-east-1 | FAIL | HIGH | Internet-wide administrative port rule found; actual reachability is not tested. |
| IAM_MFA | analyst | global | FAIL | HIGH | Console IAM user has no enrolled MFA. |
| IAM_MFA | root | global | FAIL | CRITICAL | Root MFA enrollment baseline (centralized root credential removal needs manual exception review). |
| IAM_MFA | service-backend | global | NOT_APPLICABLE | INFORMATIONAL | No console login profile observed; API-key/STS MFA enforcement is outside scope. |
| S3_ENCRYPTION | medtech-demo-patient-data | us-east-1 | FAIL | MEDIUM | Default encryption does not meet the project KMS baseline; SSE-S3 is still encryption. |
| S3_PUBLIC_ACCESS | medtech-demo-patient-data | us-east-1 | FAIL | HIGH | Public-access prevention baseline is incomplete; this does not prove data is public. |

## Remediation proposals (never applied automatically)

- **regional-management-events**: Enable a covering trail with logging, global events, all read/write management events, and healthy delivery.
- **sg-0123456789abcdef0**: Restrict administrative ingress to approved sources or use Systems Manager Session Manager.
- **analyst**: Enroll MFA for this console user; prefer federation and verify sign-in enforcement separately.
- **root**: Protect root access with MFA or document and verify centralized root credential removal.
- **medtech-demo-patient-data**: Review KMS key policy/cost, then configure SSE-KMS or DSSE-KMS; assess existing objects separately.
- **medtech-demo-patient-data**: Review access requirements, then enable all four effective Block Public Access flags; inspect policies/ACLs separately.
