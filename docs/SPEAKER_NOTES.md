## Slide 1
Introduce the MedTech AI scenario and the five-control technical baseline. The project is implemented in Python with boto3. Today’s demonstration is entirely offline: no real account scans, deployments, resource changes or email. Explain that PASS means the configured technical baseline passed within the stated scope, not HIPAA compliance. Transition to the operational problem. Suggested time: 1 minute.

## Slide 2
Explain how AI infrastructure introduces repeatable configuration questions around access, identity, network ingress and audit logging. The tool supports human review with evidence rather than replacing a full security assessment. Avoid declaring that any single configuration necessarily constitutes a breach. Transition: repeatability is the automation opportunity. Suggested time: 1 minute.

## Slide 3
Compare repeatable scanning with a reviewer-led workflow. The checker takes an explicit account, region and bucket scope. It produces stable findings and reports. No production time-savings or latency benchmark has been measured. UNKNOWN is essential: lack of read access must never become an implicit pass. Transition to the planned cloud architecture. Suggested time: 1 minute.

## Slide 4
Walk from EventBridge to Lambda, read-only APIs and independently gated outputs. The SAM template configures daily or weekly scheduling, disabled by default. JSON and HTML can go to a private KMS-encrypted bucket; SNS carries only counts and a report pointer. Optional metrics and alarms exist, but no alarm notification actions or missed-run detector are configured. Failure queues are separate for invocation delivery and Lambda execution. No AWS deployment was performed. Suggested time: 1.5 minutes.

## Slide 5
Distinguish scanner read permissions from report-write, SNS-publish and metrics permissions. Account identity is checked through STS before a real scan. S3 requests constrain the expected bucket owner. The CLI only writes local files; Lambda controls cloud outputs through explicit environment flags. Deployment itself would create billable resources, even if scanning is disabled. Transition to the control logic. Suggested time: 1 minute.

## Slide 6
Explain the five original controls: S3 Block Public Access, default KMS encryption, root and console-user MFA, administrative ingress, and active CloudTrail management-event logging. S3 SSE-S3 remains valid encryption but fails this project’s stricter KMS baseline. A public ingress rule is not proof of internet reachability. Five control groups generate seven demo results because root and console identities are separate and a service user is not applicable. Suggested time: 2 minutes.

## Slide 7
Explain PASS, FAIL, UNKNOWN and NOT_APPLICABLE. Service errors retain uncertainty, independent controls continue, and unexpected program errors fail explicitly. Delivery failures propagate and retries may duplicate outputs; durable deduplication remains future work. The scanner makes no automatic changes to assessed resources. The incomplete fixture shows why evidence coverage and assessed pass rate must remain separate. Transition to the demo. Suggested time: 1 minute.

## Slide 8
Open the linked interactive demo. Start with Misconfigured: inspect root MFA, its observed evidence and recommended action; show the notification preview. Switch to Compliant: six pass and one N/A. Switch to Incomplete: five pass and one unknown despite 100 percent of assessed items passing. Open input configuration and download a report. Clarify that the website replays recorded Python results; the CLI performs a real offline execution with boto3 Stubber. Keep a local demo backup. Suggested time: 3.5 minutes.

## Slide 9
This screenshot is from the newly generated HTML report, not a mocked visual. Findings are prioritized by failure severity, with evidence and recommended next steps. The actual SNS preview includes summary counts and a report reference, not the detailed resource evidence. No email has been sent. Open the full downloadable HTML for readable details. Transition to validation. Suggested time: 1 minute.

## Slide 10
Report only measured evidence: 88 automated tests passed, three reproducible scenarios, five control groups, zero real AWS deployments. Tests cover rule edges, exceptions, pagination, identity safety and mocked delivery. Browser checks cover scenario changes, tabs, downloads and narrow layouts. Offline validation does not prove live IAM effectiveness, production performance, scheduling or email delivery. No fixed cost or time-savings claim is made. Suggested time: 1 minute.

## Slide 11
Prioritize a small authorized AWS pilot before broadening scope. Validate read permissions, KMS policies, output delivery, quotas and actual costs. Then add schedule-aware liveness, deduplication and more AI-specific controls. Expansion to more accounts and regions requires explicit scope and policies. Any remediation should involve human approval. Suggested time: 1 minute.

## Slide 12
Close with the core outcome: five technical controls, reproducible evidence, honest uncertainty and reviewable reports. The project includes runnable code, test results, fixtures, cloud deployment configuration and this demonstration link. Reiterate that it is not a HIPAA certification and has not been deployed to AWS. Invite questions or reopen the demo. Suggested time: 1 minute.