# Least privilege and deployment boundaries

The checker does not require AdministratorAccess or the entire managed SecurityAudit policy. `template.yaml` implements conditional permissions; default demo mode has no scanner, report-write, SNS-publish or metric permissions. Logs and failure handling remain available in a deployed stack.

| Action | Resource boundary | Purpose |
|---|---|---|
| sts:GetCallerIdentity | No explicit allow required | Verify expected account |
| s3:GetBucketPublicAccessBlock | Exact configured bucket ARN | Bucket BPA |
| s3:GetEncryptionConfiguration | Exact configured bucket ARN | Default encryption |
| s3:GetAccountPublicAccessBlock | `*`, account API | Account BPA; IAM prefix is s3, SDK service s3control |
| iam:GetAccountSummary, iam:ListUsers | `*` | Root MFA and paginated inventory |
| iam:GetLoginProfile, iam:ListMFADevices | Current account `user/*` | Console users, including IAM paths |
| ec2:DescribeSecurityGroups | `*` with RequestedRegion | Security group inventory |
| cloudtrail:DescribeTrails | `*` with RequestedRegion | Regional and shadow trails |
| cloudtrail:GetTrailStatus, cloudtrail:GetEventSelectors | Current account `trail/*`, any region | Read at each trail's home region |
| logs:CreateLogStream, logs:PutLogEvents | Dedicated pre-created log group and streams | Summary logging |
| sqs:SendMessage | Dedicated Lambda failure queue | Exhausted asynchronous failures |
| s3:PutObject, optional | Report bucket `reports/*` | JSON and HTML only |
| kms:GenerateDataKey, optional S3 | `*` plus ViaService, CallerAccount and object-path encryption context | AWS-managed S3 KMS key; no decrypt permission |
| sns:Publish, optional | Dedicated topic ARN | Summary notification |
| kms:GenerateDataKey/Decrypt, optional SNS | `*` plus service, account and topic encryption context | Encrypted topic publishing |
| cloudwatch:PutMetricData, optional | `*` with namespace MedTech/SecurityBaseline | Three custom metrics |

Some account/list/describe actions do not support narrower resource ARNs. AWS-managed KMS key IDs are not statically fixed, so use service/account/context restrictions. For a dedicated customer-managed key, restrict to its exact ARN and review its key policy. IAM allows do not override explicit denies from SCPs, boundaries, session or resource policies; UNKNOWN remains possible.

The example CloudTrail permissions do not include another account's organization trail ARN. Add only specifically authorized organization trails when needed. Do not replace uncertainty with administrator permissions.

`deploy/read-only-policy.example.json` is an example for an explicitly scoped local scan. Replace all example account, bucket and region values. It grants no patient-object reads, remediation, identity changes or SNS publishing.

Deployment permissions are different from the Lambda execution role: SAM/CloudFormation needs resource creation, IAM role/pass-role and artifact upload permissions. This project does not grant them. Deployment needs explicit authorization and review of its change set and costs. A nonempty EmailEndpoint can send a subscription-confirmation email independently of EnableNotifications.

The report bucket uses BucketOwnerEnforced, all BPA flags, a TLS-only policy and SSE-KMS. The AWS-managed S3 key supports the intended same-account flow; cross-account readers require redesign. Bucket Keys are not enabled. Enabling them changes the KMS encryption context from object ARN to bucket ARN and requires a matching policy update.

EnableMonitoring also creates a dashboard and alarms; it does not configure AlarmActions or missed-run detection. Provisioning and running these resources may incur charges.

References: [S3 SSE-KMS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html), [SNS encryption permissions](https://docs.aws.amazon.com/sns/latest/dg/sns-enable-encryption-for-topic.html), [SAM schedule DLQ](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-scheduledeadletterconfig.html).
