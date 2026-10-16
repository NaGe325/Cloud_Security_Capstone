# English read-aloud script

Read the narration paragraphs. Headings are directions, not spoken words. About 1,700 words including the optional CLI segment. Use RECORDING_WALKTHROUGH.md for the exact clicks.


## Slide 1 — MedTech Security Baseline Checker

Hello, we are Charlotte Zhang and Nana Ge. Our project is the MedTech Security Baseline Checker, for the Cloud Security Engineer track, Option A.

The tool makes five recurring AWS configuration checks repeatable and easier to investigate. It uses Python and boto3, produces structured evidence, and includes a Lambda-based deployment design.

We will explain the problem, architecture, control logic, demonstration, and operational value. Today's demonstration is offline and uses synthetic AWS responses. We have not deployed the stack to AWS or sent real notifications. PASS applies only to our selected technical baseline and configured scope.

Let us start with the problem.

## Slide 2 — Cloud configuration changes need repeatable security review

MedTech's AI teams create and change training buckets, identities, and compute resources. Those changes create recurring questions about access, preventive controls, and administrative logging.

A reviewer can inspect these settings manually, but repeatedly collecting the same evidence takes effort. Inconsistent notes also make it harder to compare runs or understand what was actually checked.

Our checker collects that evidence in a consistent format, identifies baseline gaps, and explains why they were flagged. Findings still need contextual review. For example, an open security-group rule alone does not prove internet reachability.

This makes a small, clearly defined baseline a useful automation opportunity.

## Slide 3 — Make five technical controls repeatable and reviewable

This comparison shows what the checker adds to a reviewer-led workflow. Its scope is explicit: an account, selected regions, and selected buckets. It does not claim to assess every resource in the organization.

Each finding includes a resource, status, reason, evidence, and suggested next step. Reports make those results portable and comparable across runs.

UNKNOWN is particularly important. If a permission error prevents a configuration read, the checker cannot conclude that the resource passed. It preserves the evidence gap and marks coverage incomplete.

We have measured offline behavior, but have not measured production time savings or detection latency. The later value model states its assumptions separately.

## Slide 4 — Read-only scanning, gated cloud delivery

The proposed cloud workflow starts with an EventBridge rule for daily or weekly execution. It invokes a Python Lambda function that reads configuration through AWS APIs.

The scanner evaluates S3, IAM, EC2, and CloudTrail settings. When outputs are enabled, the AWS branch writes JSON and HTML reports to S3, sends an SNS summary for failed or unknown findings, and then publishes optional metrics.

The report bucket is private, KMS-encrypted, and requires secure transport. SNS carries summary counts and a report pointer rather than detailed evidence. CloudWatch provides logs and optional monitoring.

Separate queues cover EventBridge delivery failures and exhausted Lambda asynchronous failures. Retries can still duplicate output, which remains a production improvement.

The template is implemented, but real scheduling and cloud delivery remain unverified and are disabled by default. The next slide explains the permission boundaries.

## Slide 5 — Explicit scope and independently gated outputs

Configuration reads, report writes, notifications, and metrics have distinct permissions and enable switches.

Before a real scan, STS verifies the expected AWS account. S3 requests specify the expected bucket owner. These checks reduce accidental scanning of the wrong scope.

The command-line tool writes local reports. Lambda can use cloud outputs only when configured, and incoming events cannot expand scope or enable those operations.

The sample template targets one existing bucket in the deployment region. Expanding scope requires matching policy changes. Deploying the stack would create real resources even if scanning stayed disabled, so deployment still requires a reviewed plan.

These boundaries support a controlled pilot.

## Slide 6 — Five controls, evidence-backed findings

The workflow collects configuration, evaluates the baseline, stores reports, notifies when needed, and publishes optional metrics. We implement five control groups.

First, S3 public access checks the combined account and bucket Block Public Access flags. Failure indicates an incomplete preventive baseline, not proof of a data leak.

Second, S3 encryption requires default SSE-KMS or DSSE-KMS. This is a stricter project policy. SSE-S3 remains valid encryption even though it fails this KMS baseline.

Third, IAM MFA checks enrollment for root and users with console profiles. Enrollment does not prove enforcement. A service user without a console profile is not applicable to this check.

Fourth, EC2 ingress checks direct internet-wide IPv4 or IPv6 rules covering ports twenty-two or thirty-three eighty-nine. Routing and public IPs also affect actual reachability.

Finally, CloudTrail checks active management-event logging, read and write coverage, global events, and the reported delivery condition.

Five groups produce seven demo results because root, a console user, and a service user have separate MFA results. Severity guides project triage rather than establishing a complete risk or compliance judgment.

## Slide 7 — Unknown evidence stays unknown

The checker distinguishes confirmed failures from unavailable evidence. Expected AWS errors become UNKNOWN, while independent checks continue. Inventory pagination must complete before an inventory conclusion is drawn.

Retries are bounded. Unexpected program errors and delivery failures propagate rather than becoming misleading passes.

Partial delivery remains possible: JSON might upload before HTML fails, and a retry can duplicate output. Durable deduplication is not implemented.

Offline mode blocks AWS transport. The scanner reads configuration, does not read patient objects, and makes no automatic remediation. Optional alarms have no notification actions and cannot detect missed runs.

We will now demonstrate confirmed gaps, passing results, and incomplete evidence.

## Slide 8 — Three scenarios, one reproducible checker

This demonstration uses synthetic AWS responses and recorded outputs from the actual Python checker. The browser replays those results; it does not execute Python or connect to AWS. I will show the input, a confirmed failure, the notification preview, and the difference between a passing and an incomplete scan.

### 8A: Misconfigured summary

We start with the misconfigured scenario. The report contains zero passing results, six confirmed baseline failures, zero unknowns, and one result that is not applicable. These are seven resource-level results across five control groups, rather than seven independent controls.

### 8B: Root MFA evidence

The first item is root MFA, which receives critical triage priority in this project. The observed value is AccountMFAEnabled equal to zero. The report preserves that evidence and recommends protecting root access with MFA, or verifying a documented centralized root-credential removal arrangement where appropriate.

The reviewer should validate the account context before making changes. This is a synthetic configuration finding, not an observed account compromise.

### 8C: Input configuration

This tab shows the AWS-shaped input configuration behind the scenario. The complete fixture records the responses used by the offline scanner. Using fixed input and run identifiers makes the reports reproducible and allows us to test the same behavior repeatedly.

### 8D: Notification preview

The notification is preview-only. Its subject indicates a failed baseline, and its body includes summary counts rather than detailed evidence. No email has been sent. A report pointer is populated when real report storage succeeds; in this offline preview, no S3 report has been stored.

### 8E: Compliant scenario

In the compliant scenario, all six assessed results pass and one service identity is not applicable because it has no console login profile. No failure or unknown notification is required. PASS means this selected baseline passed within the configured scope; it does not certify all AWS resources or HIPAA compliance.

### 8F: Incomplete scenario

The incomplete scenario is different. Five assessed results pass, but the S3 encryption read returns AccessDenied. The checker records UNKNOWN because it lacks enough evidence to decide whether that baseline passed or failed.

The assessed pass rate can still be one hundred percent because unknown and not-applicable results are excluded from that denominator. Coverage remains incomplete. A high pass rate must never hide an evidence gap.

### 8G: Standalone HTML report

The results are portable. I can download the HTML report or the JSON evidence. Here is the same misconfigured-scenario report in its standalone HTML form. It retains the overall result, scope, individual findings, evidence, and suggested actions so a reviewer can investigate outside this interface.

### 8H: Optional executable CLI

Unlike the browser replay, this command actually runs the Python scanner using boto3 Stubber responses. It generates the local reports and returns the expected failed-baseline result. It still performs no live AWS calls or cloud delivery. Exit code one represents confirmed findings, not a crash.

### Return to slide 9

These scenarios show a confirmed gap, a passing baseline, and an evidence gap. Let us return to the slides and summarize what the security reviewer receives.

## Slide 9 — Prioritize the risk, inspect the evidence

This slide summarizes the review workflow. The report screenshot shows six failed results. Root MFA receives the highest triage priority, followed by examples such as console-user MFA and administrative ingress.

The enlarged evidence makes one observation readable: AccountMFAEnabled equals zero in the synthetic fixture. It connects a specific configuration fact to a suggested next action.

The notification summarizes the result, while the report preserves the detail for investigation. We will now explain the validation and estimated operational value.

## Slide 10 — Validation and estimated operational value

We separate measured validation from estimated value. We have eighty-eight passing tests, three reproducible scenarios, five control groups, and zero real AWS deployments. The template check and report comparisons also passed. These checks do not establish production performance or cloud delivery.

For time savings, assume fifteen manual minutes per run, including five minutes to interpret evidence. Automation retains those five review minutes. Across thirty runs, the ten-minute difference releases five hours per month, a sixty-six-point-seven percent reduction for these checks.

At an assumed sixty dollars per hour, that represents three hundred dollars of staff capacity, not measured savings or a payroll reduction. Setup and maintenance are excluded.

The cost model assumes one small account and bucket in Northern Virginia, thirty daily runs, two hundred fifty-six megabytes of Arm memory, and thirty seconds per run. Rounded-up monthly budgets are about two cents base, or four dollars twelve with optional monitoring.

These are estimates before credits, taxes, and stated exclusions. Assumptions, arithmetic, and AWS sources are included in the repository. A pilot must measure actual cost, runtime, and review effort.

## Slide 11 — A bounded path to production

Our next step is a small authorized pilot. We would validate effective permissions, KMS policies, report storage, one approved notification recipient, and actual scheduled execution. We would measure runtime and cost for that scope.

Operational improvements include durable deduplication, partial-delivery recovery, and missed-run detection. Current alarms do not establish schedule liveness.

Later checks could cover SageMaker settings, KMS policies, federated MFA, RDS, and CloudTrail data events or freshness. More accounts and regions would require matching permissions and scale tests.

Human review remains necessary before any remediation.

## Slide 12 — Summary

To conclude, this project implements five repeatable AWS configuration controls, preserves reviewable evidence, and makes uncertainty visible.

The repository includes runnable offline code, reproducible scenarios, reports, tests, and a cloud deployment design. A real pilot remains necessary to validate permissions, scheduling, delivery, scale, and economic assumptions.

The result is a consistent starting point for reviewing MedTech's AI infrastructure. Thank you for watching.
