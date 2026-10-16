# English speaker notes

Suggested talk/demo: 14 minutes 35 seconds, plus 2–3 minutes Q&A. Rehearse to stay within 15–20 minutes. Role split is a suggestion; verify your actual contributions.

## Slide 1

[0:40] We are Charlotte Zhang and Nana Ge. Our project is a security compliance checker for MedTech's AI infrastructure, following Engineer Option A. It automates five configuration questions and produces evidence for a security reviewer. Today we demonstrate the implemented scanner entirely offline. The cloud deployment design is included, but no real AWS deployment, schedule execution or email delivery has been performed. PASS refers only to the declared technical baseline and scope.

Sources: https://github.com/georgewerbacher/cmu-cloud-sec-documentation/blob/main/pages/capstone/capstone_engineer.md
https://github.com/NaGe325/Cloud_Security_Capstone

## Slide 2

[0:55] MedTech's AI teams work with data buckets, identities and compute resources. A configuration may change between manual reviews. Repeating a small set of questions is useful, but reviewers still need to decide whether a finding is relevant to patient data or actual exposure. We selected five checks because they are repeatable and explainable. The checker supports human judgment by collecting consistent configuration evidence. It does not read patient objects or change assessed resources. Our goal is to reduce repeated collection work while making evidence gaps visible.

Sources: https://github.com/georgewerbacher/cmu-cloud-sec-documentation/blob/main/pages/capstone/capstone_engineer.md
https://github.com/NaGe325/Cloud_Security_Capstone

## Slide 3

[0:55] The checker uses explicit scope rather than claiming to discover every resource. Five control groups can yield multiple results, such as separate root and console-user MFA findings. Reports retain status, reason, evidence and suggested next steps. The important design choice is that uncertainty is a first-class result. An access-denied error does not become a pass. Human review remains in the workflow. Later we show an illustrative time model, with the assumptions stated openly rather than claiming measured production savings.

Sources: https://github.com/georgewerbacher/cmu-cloud-sec-documentation/blob/main/pages/capstone/capstone_engineer.md
https://github.com/NaGe325/Cloud_Security_Capstone

## Slide 4

[1:15] EventBridge invokes the Lambda function on a daily or weekly schedule. Lambda reads configuration from S3, IAM, EC2 and CloudTrail using scoped permissions. It evaluates five control groups and constructs structured findings. In the AWS branch, enabled report writes happen first, then an SNS summary when there are failures or unknowns, then optional metrics. SNS contains summary counts and a report pointer, not detailed evidence. Separate failure queues cover EventBridge delivery and exhausted Lambda asynchronous failures. Every output is independently controlled. The schedule and cloud operations are disabled by default. No cloud execution is claimed today.

Sources: https://github.com/georgewerbacher/cmu-cloud-sec-documentation/blob/main/pages/capstone/capstone_engineer.md
https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/
https://github.com/NaGe325/Cloud_Security_Capstone

## Slide 5

[1:10] The live entry point verifies the STS caller account before scanning and S3 calls include the expected bucket owner. The sample SAM stack targets one existing bucket in its deployment region. The Python scope can include additional regions or buckets, but policies must be extended at the same time. Read, report-write, notification and metrics permissions are distinct. These choices align with the Security Pillar principles of identity, traceability, automation and data protection. The deployment plan is staged: validate the smallest scope before enabling outputs and scheduling. Effective IAM, SCP and KMS behavior still needs a live pilot. The retained report bucket also needs deliberate cleanup after a stack is removed.

Sources: https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/
https://github.com/NaGe325/Cloud_Security_Capstone

## Slide 6

[1:30] The first check combines account and bucket Block Public Access flags. A failure is a preventive baseline gap, not proof of public readability. The second checks default KMS encryption; SSE-S3 remains valid encryption but does not meet our stricter project policy. MFA checks root and console-login users. A service user without a console profile is not applicable, and enrollment does not prove sign-in enforcement. EC2 checks direct IPv4 and IPv6 /0 rules covering ports 22 or 3389. It does not prove network reachability or inspect MySQL exposure. CloudTrail needs logging, global events, complete read/write management-event coverage and no reported delivery error. These five groups satisfy the engineering scope. Severity is project triage, not CVSS or a legal conclusion.

Sources: https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html
https://github.com/NaGe325/Cloud_Security_Capstone

## Slide 7

[1:05] Service errors produce UNKNOWN and retain the reason, while independent checks continue. Inventory pagination must complete before we draw inventory conclusions. Known API errors are handled explicitly; unexpected programming errors propagate rather than becoming misleading compliance results. The SDK has bounded retries. Report-delivery failures also propagate: JSON may have uploaded before HTML fails, and an asynchronous retry can duplicate output. A stable finding ID helps compare findings, but it is not durable delivery deduplication. Our tests block AWS transport, and offline fixtures use dummy credentials. Current alarms cover errors or unknown findings, but have no notification actions and cannot detect a missed scheduled run.

Sources: https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/
https://github.com/NaGe325/Cloud_Security_Capstone

## Slide 8

[3:00 demo] Use the local demo as the reliable default; open demo/index.html before presenting. Start with Misconfigured. Show six failed results, one N/A, and no unknowns. Open root MFA, show AccountMFAEnabled equals zero, and inspect the recommended action. Show the SNS preview and make clear it has not been sent. Switch to Compliant: six PASS and one N/A. Switch to Incomplete: five PASS, one UNKNOWN and one N/A; encryption evidence is unavailable because of AccessDenied. Explain that 100 percent of assessed items passing still leaves incomplete evidence. Show the input fixture and download a JSON or HTML report. If useful, run the CLI command; it exits one for confirmed failures by design. The website replays recorded output; the CLI executes the real scanner against synthetic boto3 Stubber responses. Neither scans AWS.

Sources: https://medtech-security-checker-demo.nage32519.chatgpt.site/
https://github.com/NaGe325/Cloud_Security_Capstone

## Slide 9

[1:00] This table comes directly from examples/misconfigured.json, not an invented breach narrative. The root configuration indicates no enrolled MFA in the synthetic scenario. We triage it first because root has powerful account-level authority. The next action is contextual: protect root with MFA or verify and document centralized root credential removal where applicable. The reviewer should validate the actual account model before changing anything. Other gaps include console-user MFA, open administrative ingress, S3 preventive flags, the KMS baseline and logging coverage. Notifications carry counts rather than resource evidence. The full report remains the review artifact.

Sources: https://github.com/NaGe325/Cloud_Security_Capstone/blob/main/examples/misconfigured.json
https://github.com/NaGe325/Cloud_Security_Capstone

## Slide 10

[1:35] Here is a transparent planning model. Assume a manual workflow takes fifteen minutes: ten for collection and five for interpretation. With automation, retain five minutes of human review. Thirty daily runs release three hundred minutes, or five staff hours a month. That is a 66.7 percent reduction for this narrow workflow. At an assumed sixty dollars per hour it represents three hundred dollars of capacity, not an actual payroll saving. Neither human timing has been measured. Separately, the cloud model assumes one small account in us-east-1, thirty runs, 256 MB Arm and thirty seconds billed duration per run. Before free-tier credits, the base model rounds up to roughly two cents a month; three metrics, one dashboard and two alarms bring it to a rounded-up budget of about four dollars twelve. Existing workloads, taxes, transfer, extra retries and labor are excluded. Monitoring dominates this tiny scenario. A five-dollar review threshold is not an enforced cap. Measured evidence is the offline regression suite and reproducible outputs. Pilot targets are future acceptance criteria.

Sources: https://aws.amazon.com/lambda/pricing/
https://aws.amazon.com/s3/pricing/
https://aws.amazon.com/kms/pricing/
https://aws.amazon.com/sns/faqs/
https://aws.amazon.com/cloudwatch/pricing/
https://aws.amazon.com/sqs/pricing/
https://aws.amazon.com/eventbridge/pricing/
https://github.com/NaGe325/Cloud_Security_Capstone

## Slide 11

[1:00] First, review a safe isolated account, explicit bucket/region scope and policies. Deploy defaults only after reviewing the change set. Validate reads, then stored reports and one approved recipient, before enabling the schedule. Observe seven expected daily runs and examine actual cost, duration, unknowns and delivery evidence. These are proposed acceptance tests, not results we already have. After the pilot, add a missed-run detector and durable deduplication. Broader coverage requires matching IAM and scope updates, quota testing and a more scalable execution model. The instructor environment also has RDS and excessive-role-policy issues outside our five controls. Human approval remains necessary for remediation.

Sources: https://github.com/georgewerbacher/cmu-cloud-sec-documentation/blob/main/pages/capstone/capstone_engineer.md
https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/
https://github.com/NaGe325/Cloud_Security_Capstone

## Slide 12

[0:30 + 2:00 Q&A] We implemented five repeatable checks, made evidence and uncertainty explicit, and provided reports that support human triage. The offline demo and tests establish rule behavior within scope. The SAM design describes the path to a small cloud pilot. We do not claim complete AWS coverage or HIPAA certification. The next step is to validate real permissions, delivery, schedule execution and the economic assumptions. Thank you. We are ready for questions. AI assistance and sources are disclosed in the accompanying appendix.

Sources: https://github.com/georgewerbacher/cmu-cloud-sec-documentation/blob/main/pages/capstone/capstone_engineer.md
https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/
https://github.com/NaGe325/Cloud_Security_Capstone
