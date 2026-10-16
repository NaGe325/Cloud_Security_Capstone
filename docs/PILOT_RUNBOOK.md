# Implementation and acceptance walkthrough

The submission demonstrates an offline implementation and cloud deployment design. These steps describe a future authorized pilot. No live AWS commands are executed by the offline verification scripts.

## Local preparation

1. Install locked dependencies and the project using the README instructions.
2. Run `python scripts/verify_submission.py` for test suite, template lint and reproducible demo output checks.
3. Run `python deploy/build_package.py`, then `sam build --template-file template.yaml` on a machine with SAM and its build prerequisites. SAM build itself remains unverified in this submission.
4. Review template.yaml: one bucket in one account/region, 256 MB Arm Lambda, 300-second timeout, separate failure queues, private encrypted reports, 14-day summary logs and 30-day report expiration.

## Pilot sequence and acceptance evidence

| Stage | Configuration / action | Evidence required |
|---|---|---|
| 1. Review | Choose isolated account and existing bucket; inspect least-privilege role and KMS/SCP restrictions | Signed-off account/region/bucket scope and policy review |
| 2. Deploy design | Review SAM change set; initially retain demo defaults, no schedule or email endpoint | Stack resource list and rollback status; no claim that defaults cost nothing |
| 3. Enable reads | ScanMode=aws, AllowAwsReads=true, correct ScanBucketName | STS account match, five control groups, explicit UNKNOWN on insufficient permissions |
| 4. Enable report writes | EnableReportWrite=true | JSON and HTML objects under reports/, KMS encryption, private access and matching run IDs |
| 5. Enable notifications | Review one EmailEndpoint, confirm subscription, EnableNotifications=true | One approved test finding yields summary and working report pointer, without detailed evidence in email |
| 6. Enable schedule | EnableSchedule=true; rate(1 day) or rate(7 days) | Rule configuration plus expected Lambda runs and stored reports; observe seven daily runs for pilot target |
| 7. Optional monitoring | EnableMonitoring=true | Dashboard, three metrics, two alarms; inspect console because AlarmActions are empty |
| 8. Fault exercise | Denied configuration read, report write failure, Lambda error in safe test scope | UNKNOWN behavior, propagated failure, failure-queue evidence and no false STORED claim |
| 9. Cost/runtime review | Measure billed duration, API usage and retry behavior | Same-scope human timing comparison, p95, Cost Explorer review versus illustrative $5/month threshold |

## Operator response

- FAIL: read restricted evidence and validate context. Root MFA has highest triage priority. Confirm compensating controls before changing resources.
- UNKNOWN: investigate identity, permissions, region and resource existence; rerun after access is fixed. Never treat lack of evidence as compliance.
- Delivery error: inspect Lambda logs and relevant failure queue. JSON may exist without HTML, and retries can duplicate notifications. Reconcile by run ID and finding ID.
- Missing scheduled run: manually compare expected schedule to run/report timestamps. The current alarms do not detect liveness; add a separate detector before production.
- Stop/rollback: disable schedule first, disable output flags and reads, review change set or delete stack when appropriate. Report bucket is retained, so separately review its retention and cleanup. Do not delete evidence merely to clear an alert.

Scope expansion requires both configuration AND policy updates. More accounts/regions require additional identity, throttling and scale testing. This project does not implement automatic remediation or HIPAA certification.
