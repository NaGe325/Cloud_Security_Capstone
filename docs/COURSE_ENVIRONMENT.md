# Relationship to the instructor environment

Project route: **Cloud Security Engineer, Option A: Security Compliance Checker**. Authors: Charlotte Zhang and Nana Ge. This tool automates five technical questions in the MedTech scenario. It does not claim the Analyst route's 15 CCM controls or the Architect route's full infrastructure design.

Instructor source: [main.tf](https://github.com/georgewerbacher/cmu-cloud-sec-documentation/blob/main/pages/capstone/main.tf), read October 16, 2026. Observations below are **static source observations**, not proof of a successful deployment or the current state of an AWS account.

| Instructor Terraform configuration | Current checker relationship | Interpretation |
|---|---|---|
| `public_data_pab` disables bucket-level flags; `public_data_policy` allows anonymous reads/listing | S3_PUBLIC_ACCESS | Account-level protection may still block access. Checker evaluates combined flags, not effective policy/ACL authorization. Bucket is tagged Public, so review intended use before treating it as PHI exposure. |
| `ai_training_encryption` uses AES256 | S3_ENCRYPTION | Encrypted with SSE-S3. Fails this project's stricter KMS baseline, not proof of missing encryption or a HIPAA violation. |
| IAM users and access keys are declared, no user MFA enrollment in this file | IAM_MFA, limited | Only root/console-login enrollment is checked. Source omission is not proof of actual MFA state. Root state cannot be inferred from this template. API-only users are N/A for this check. |
| `web_sg` permits TCP 22 from 0.0.0.0/0 | EC2_ADMIN_PORTS | Detected if scanning this group. Further reachability analysis remains manual. |
| `main_trail` selects WriteOnly management events | CLOUDTRAIL_LOGGING | Does not meet this project's full read/write management-event baseline, even if logging is active. |
| Developer `Action:*`, `Resource:*`; broad EC2 role policy | Outside five-control scope | Least-privilege review is an explicit future extension. |
| RDS publicly_accessible=true, storage_encrypted=false; database SG opens 3306 | Outside five-control scope | Database encryption, connectivity and secrets management require separate checks. Current port check only covers 22/3389. |
| Patient bucket versioning suspended; logs bucket lifecycle 7 days | Outside five-control scope | Retention, recovery and classification need context-specific human review. |

The synthetic `misconfigured` fixture is an independent teaching scenario. It sets a nonlogging trail and root MFA absent; these are not observations from the instructor Terraform or a live account. Its bucket/SG/account identifiers are invented. `COMPLETE_WITHIN_SCOPE` means the selected five checks returned determinate results for configured resources, not complete AWS inventory or healthcare compliance.

No `terraform apply` is needed for the offline walkthrough. An authorized live pilot should use a safe existing lab account, explicit scan scope and reviewed read policies. Never present mocked delivery as a real email or deployed schedule.
