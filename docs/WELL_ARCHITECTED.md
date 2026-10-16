# Security design decisions and AWS Well-Architected alignment

This is an engineering design alignment, not a formal Well-Architected Review or compliance certification.

| Security Pillar design principle | Project decision / evidence | Trade-off / residual risk |
|---|---|---|
| Implement a strong identity foundation | STS account check, ExpectedBucketOwner, conditional read/write/SNS/metric policies in template.yaml | IAM/SCP/KMS effectiveness needs a live pilot; account-level list APIs need wildcard resources. |
| Enable traceability | Stable finding IDs, run IDs, structured reports, summary logs, CloudTrail baseline | No log-content audit, data-event verification or durable idempotency. |
| Automate security best practices | Five repeatable checks and daily/weekly EventBridge design | Narrow scope; scheduled rule disabled by default; missed-run detection is future work. |
| Protect data in transit and at rest | Private report bucket, TLS-only bucket policy, KMS report writes, encrypted SNS, redacted summary notifications | Reports still contain resource identifiers; key permissions need validation. |
| Keep people away from data | Read configuration APIs, no patient-object reads, human review of findings | Does not inspect actual PHI classification or object contents. |
| Prepare for security events | UNKNOWN, bounded retries, separate execution/invocation failure queues and proposed operator runbook | Alarms have no actions; operators must review them. No automated remediation. |

Choosing Lambda/SAM keeps this small configuration-checking workflow simple. Sequential scans and a 300-second timeout limit scale. A future account/region fan-out design should add a queue or state machine, idempotency and account-scoped role assumptions before claiming organization-wide coverage. Managed AWS Config/Security Hub are alternatives with broader controls and operating cost; this educational checker provides transparent, small-scope logic rather than recreating those platforms.

Primary source: [AWS Security Pillar design principles](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/design-principles.html). Framework mapping reviewed October 16, 2026.
