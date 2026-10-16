# Automated AWS Security Compliance Checker for MedTech AI Infrastructure

CMU Cloud Security Engineer — Option A. Python 3.12+, boto3, five technical controls, reproducible offline scans, JSON/Markdown/HTML reports, and a gated Lambda deployment design.

**Verified offline; not deployed to AWS. No real account scans, resource changes or email.** A PASS applies only to this project's baseline and declared scope. These checks do not establish full HIPAA compliance.

## Presentation and downloads

Authors: **Charlotte Zhang and Nana Ge**. Final route: **Cloud Security Engineer, Option A**. See [submission guide](docs/SUBMISSION.md) and [rubric coverage](docs/RUBRIC_COVERAGE.md).

- [Final English slides PDF](slides/MedTech-Security-Baseline-Slides.pdf), updated directly from the original 12-slide PDF; [unchanged original source](slides/original/MedTech-Security-Baseline-Slides.pdf)
- [Complete project ZIP](downloads/medtech-compliance-checker.zip) and [SHA-256 checksum](downloads/medtech-compliance-checker.zip.sha256)
- [English speaker notes](docs/SPEAKER_NOTES.md)
- [Local demo instructions](demo/README.md)

## Run locally without an AWS account

Extract the project and enter its directory. Installing dependencies requires a Python package source; the demos then run offline without AWS credentials.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.lock
python -m pip install --no-deps -e .
python -m medtech.cli demo compliant --out reports
python -m medtech.cli demo misconfigured --out reports
python -m medtech.cli demo incomplete --out reports
```

Expected exit codes: **0** compliant, **1** misconfigured, **2** incomplete. Code 1 means confirmed baseline failures, not a crash. Code 2 means no FAIL but some UNKNOWN; argument errors also use argparse's code 2. Invalid configuration, identity mismatches and unexpected program errors raise explicitly.

Each run writes `<scenario>.json`, `.md`, `.html` and `.delivery.json`. The last contains delivery state and an SNS preview. `examples/` contains actual generated outputs. `requirements.txt` is sufficient for runtime; `requirements-dev.lock` adds pinned test and template-validation dependencies. SAM, Docker and AWS CLI are not needed for offline work.

[Hosted recorded demo](https://medtech-security-checker-demo.nage32519.chatgpt.site/) · [Earlier Google Slides version](https://docs.google.com/presentation/d/11W8AE5Fn5un-FhWMLC6scesZQe5N5m9bFQFXPzMcSjA/edit)

**Use the updated repository PDF for this submission.** Only slides 1, 6, 9 and 10 have focused edits; the other eight pages retain the original content streams and render identically. The earlier Google Slides and hosted website were not edited in this update. For a reliable demo, extract the ZIP and open `demo/index.html`.

The website replays recorded Python outputs. It does not execute Python or call AWS. For a local backup, open `demo/index.html`; its data and reports are included. The hosted site retains owner-private access, so presenting while signed in or using the local backup is currently necessary.

## Five control definitions

| Control | Pass rule | Failure severity | Interpretation |
|---|---|---|---|
| S3_PUBLIC_ACCESS | All four effective account/bucket BPA flags enabled | HIGH | Configuration baseline, not proof a bucket is publicly readable |
| S3_ENCRYPTION | Default algorithm `aws:kms` or `aws:kms:dsse` | MEDIUM | SSE-S3 is valid encryption but does not meet this stricter KMS baseline |
| IAM_MFA | Root MFA enabled; console-login IAM users have MFA registered | Root CRITICAL; user HIGH | No console profile means N/A; registration does not prove enforcement |
| EC2_ADMIN_PORTS | No inbound TCP/UDP/all-protocol rule exposes 22 or 3389 to `0.0.0.0/0` or `::/0` | HIGH | Rule exposure, not verified internet reachability |
| CLOUDTRAIL_LOGGING | A covering trail is logging, includes global service events and full read/write management events, and has no LatestDeliveryError | HIGH | Does not verify data events, freshness or complete audit compliance |

Severity is a project triage decision, not CVSS or a legal determination. No remediation is performed.

For S3 BPA, the two layers are combined flag by flag. If one known layer is sufficient, the result can PASS while retaining the other layer's error in evidence; otherwise incomplete evidence means UNKNOWN. Missing configuration is distinct from access denied. CloudTrail supports ordinary event selectors and unrestricted management advanced selectors. Complex restrictive selectors do not satisfy the full-management-events baseline. A known qualifying trail can support PASS even if another trail is unreadable; otherwise unresolved reads remain UNKNOWN.

## Findings and coverage

Every finding has a stable `id`, `control_id`, resource, region, status, severity, reason, evidence and remediation. See `report.schema.json` and the example JSON reports.

- PASS: evidence supports the defined baseline.
- FAIL: evidence identifies a baseline gap.
- UNKNOWN: permissions, throttling or another service error prevents a conclusion.
- NOT_APPLICABLE: for example, a service user without a console login profile.

Overall status is FAIL when any failure exists; otherwise UNKNOWN yields INCOMPLETE. Coverage remains incomplete even if FAIL is also present. Assessed pass rate is `PASS / (PASS + FAIL)`, excluding UNKNOWN and N/A. An empty denominator yields null. This is never a HIPAA compliance percentage. Five control groups generate seven demo results: separate root and console identities plus a non-applicable service user.

HTML and the website prioritize failures by severity, followed by unknowns. Evidence and suggested next steps remain visible. Reports contain identifiers and should be restricted outside this synthetic demo.

## Verify

```bash
python -m pytest --cov=medtech --cov-report=term-missing
python deploy/build_package.py
cfn-lint template.yaml
```

The current suite has 88 passing tests. Tests block AWS HTTP transport and validate boto3 request/response contracts with botocore Stubber. See `docs/VALIDATION.md` for measured results and limitations. `docs/DEMO.md` contains the English presentation walkthrough.

## Submission support and operational value

- [Value, time and cost model](docs/VALUE_AND_COST.md): explicit assumptions, rate sources, sensitivity and pilot targets. `python scripts/value_model.py` reproduces the numbers in [value-model.json](examples/value-model.json).
- [Current offline timings](examples/offline-benchmark.json): five local synthetic executions per scenario; not live AWS latency. Reproduce with `python scripts/benchmark_offline.py`.
- [Instructor environment relationship](docs/COURSE_ENVIRONMENT.md): distinguishes Terraform source observations from independent synthetic fixtures.
- [Well-Architected alignment](docs/WELL_ARCHITECTED.md), [pilot runbook](docs/PILOT_RUNBOOK.md) and [Q&A preparation](docs/QA_PREPARATION.md).
- [AI assistance disclosure](docs/AI_USE.md): includes the current task prompt and response, plus the boundary for earlier unrecorded sessions.

Illustrative economics: assume 15 manual minutes vs 5 human-review minutes per daily run. Thirty runs release **5 hours/month**, or **$300 of staff capacity at an assumed $60/hour**, excluding setup and maintenance. This is not measured savings. Under the declared small us-east-1 scenario, round-up planning budgets are **$0.02/month base** or **$4.12/month with optional monitoring**, before credits and exclusions. These are not actual bills or price guarantees.

Run `python scripts/verify_submission.py` after installing the project. It checks the regression suite, SAM lint, exact scenario reports and cost-model consistency without AWS access. Current evidence is saved under `examples/`. CI uses the same command on Python 3.12; a workflow file alone does not mean a hosted CI run has occurred. `python scripts/package_submission.py` rebuilds the portable ZIP and checksum without VCS data, environments or credentials.

## Real AWS scanning — only after explicit authorization

This was not performed. Read-only API access may still have quota, audit or cost implications.

1. Edit `config.example.json` with the expected account, explicit regions and bucket-to-region map. At least one bucket is required; discovery is not automatic.
2. Use short-lived SSO/assume-role credentials through the normal boto3 credential chain. Do not store keys in the project.
3. Review the read policy in `deploy/read-only-policy.example.json` and `docs/PERMISSIONS.md`.
4. Only after authorization, run:

```bash
python -m medtech.cli scan --config config.example.json --allow-aws-read --out reports
```

STS checks the expected account before scanning. S3 calls set ExpectedBucketOwner. The CLI only writes local reports and cannot send SNS or write S3 reports.

## Lambda and deployment configuration

`medtech.lambda_handler.handler` defaults to the offline misconfigured fixture. Events cannot change scope or enable cloud operations.

| Environment variable | Meaning |
|---|---|
| SCAN_MODE | `demo` by default; `aws` for explicitly enabled cloud reads |
| DEMO_SCENARIO | `compliant`, `misconfigured` or `incomplete` |
| ALLOW_AWS_READS | Only literal `true` permits AWS mode |
| SCAN_SCOPE_JSON | Required explicit scope in AWS mode |
| REPORT_BUCKET / SNS_TOPIC_ARN | Optional cloud destinations |
| ENABLE_S3_WRITE / ENABLE_SNS_PUBLISH | Only `true` enables the corresponding output |
| ENABLE_METRICS | Only `true` enables CloudWatch metrics in AWS mode |

Demo mode disables all cloud writes even if environment switches are set. Real S3 delivery writes JSON and escaped HTML with KMS encryption and expected owner checks. SNS carries summary counts and a report pointer, not detailed evidence. Optional metrics are FailedFindings, UnknownFindings and CompletedRuns in MedTech/SecurityBaseline.

The SAM template defaults to demo mode, disabled scheduling, no scan permissions, no report writes, no SNS publishing, no monitoring resources and an empty email endpoint. It defines a private KMS-encrypted report bucket with a 30-day lifecycle and retain-on-delete, an encrypted SNS topic, scoped conditional policies, 14-day logs, and separate failure queues for Lambda and EventBridge. Lambda uses 256 MB, a 300-second timeout and reserved concurrency of one.

**Deployment itself creates real, potentially billable resources even when feature switches are disabled. It has not been executed.** Authorized deployment preparation is:

```bash
python deploy/build_package.py
sam build --template-file template.yaml
sam deploy --guided
```

Keep defaults initially and review the change set. A later authorized cloud run requires `ScanMode=aws` and `AllowAwsReads=true`; report writes, notifications, schedule and monitoring have separate enable parameters. Schedule choices are `rate(1 day)` and `rate(7 days)`. A nonempty EmailEndpoint creates an SNS subscription and can send a confirmation email even if publishing is disabled; leave it empty unless explicitly authorized.

EnableMonitoring adds a dashboard and alarms for Lambda errors and unknown findings. AlarmActions are not configured, so these alarms do not send notifications. They do not detect missed runs. CompletedRuns is emitted only after preceding delivery succeeds. Metric failures propagate. Costs depend on use of Lambda, APIs, S3, KMS, SNS, CloudWatch and SQS; no fixed monthly estimate is claimed.

The template targets one existing bucket in its deployment region. Expand both SCAN_SCOPE_JSON and IAM policies for additional buckets or regions. Deleting the stack retains the report bucket; review retention before cleanup.

## Errors and limits

The SDK uses standard retries with at most four total attempts, a 3-second connection timeout and a 10-second read timeout. IAM and EC2 enumerate pages. Inventory read failure produces UNKNOWN rather than silently treating partial inventory as complete. Independent checks continue; unexpected program or response-shape errors fail explicitly.

S3, SNS or metric output failures raise. JSON may already have uploaded when HTML fails; SNS may have succeeded when metrics fail. Asynchronous retries can create duplicate reports or notifications. There is no durable idempotency or alert deduplication. Operators must inspect failure queues and logs; no external failure subscriptions are configured.

Important scope limits:

- Single account and explicit regions/buckets; no automatic complete asset discovery. General-purpose S3 only; not directory buckets, Access Points, MRAP, object ACL evaluation or a full organization-policy authorization analysis.
- Encryption checks only the default algorithm, not existing objects, key policy, rotation or customer-managed ownership. AWS-managed KMS keys are accepted.
- IAM checks registration, not Identity Center/SSO/IdP, role sessions or MFA enforcement. Centralized root-credential removal may require a documented exception; missing root MFA does not prove compromise.
- Security groups check direct `/0` CIDRs, not combined narrower ranges, prefix lists, ENIs, routing, NACLs or public IP reachability. UDP 22 is flagged conservatively.
- CloudTrail does not validate data events, Lake, log integrity/retention/encryption, latest delivery time or log contents. Historical delivery errors may need review. Organization trail permissions can yield UNKNOWN.
- Sequential scanning suits small environments. Large accounts may exceed the Lambda timeout; SDK retries are not an overall runtime guarantee.
- SAM build/deploy, live IAM/SCP/key policies, cloud delivery, schedule execution, email and production scale remain unverified. A real pilot requires explicit authorization.

## Project guide

`medtech/`: scanner, reporting and bundled fixtures. `tests/`: offline tests. `examples/`: generated evidence. `demo/`: self-contained static demo. `template.yaml`: deployment design. `deploy/`: local package builder and example read policy. `docs/`: architecture, permissions, validation, presentation and design notes.

The uploaded slide-design-system source is preserved under `docs/slide-design-system/`. English working notes describe how its CMU branding and hierarchy were applied; source material is retained unchanged for traceability.

## References

- [CMU Engineer Option A](https://github.com/georgewerbacher/cmu-cloud-sec-documentation/blob/main/pages/capstone/capstone_engineer.md)
- [AWS S3 Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)
- [AWS S3 security best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
- [boto3 CloudTrail status](https://docs.aws.amazon.com/boto3/latest/reference/services/cloudtrail/client/get_trail_status.html) and [selectors](https://docs.aws.amazon.com/boto3/latest/reference/services/cloudtrail/client/get_event_selectors.html)
- [boto3 IAM account summary](https://docs.aws.amazon.com/boto3/latest/reference/services/iam/client/get_account_summary.html)
