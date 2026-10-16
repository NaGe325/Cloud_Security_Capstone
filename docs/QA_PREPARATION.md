# Presenter Q&A

Suggested split: Charlotte presents problem, architecture and security decisions (slides 1–5); Nana presents implementation, demo, value and next steps (slides 6–12). Adjust roles to match your actual contributions; this is a rehearsal suggestion, not a claim about authorship of individual code.

1. **Why these five controls?** They cover repeatable access, identity, administrative ingress and audit questions relevant to MedTech. Five satisfies Engineer Option A. RDS, role-policy review and AI-specific checks are explicitly outside this version.
2. **Is this the actual instructor AWS account?** No. The demo uses synthetic AWS-shaped fixtures with real boto3 clients intercepted by Stubber. Terraform source observations are documented separately.
3. **Is a failed S3 public-access check proof of a data leak?** No. It checks preventive flags at account/bucket layers, not effective public readability. Policy, ACL, access-point and object review remain necessary.
4. **Is SSE-S3 unencrypted?** No. AES256/SSE-S3 is valid encryption. Our KMS baseline is deliberately stricter; that is a project policy, not a universal HIPAA requirement.
5. **Does enrolled MFA guarantee enforcement?** No. Root and console-user enrollment are observed; federation, session policies and MFA enforcement need separate review.
6. **Does a security-group rule prove reachability?** No. Routing, public IPs, NACLs and resource attachment also matter. We flag direct /0 rules for 22/3389 only.
7. **Why UNKNOWN?** An unreadable configuration is insufficient evidence. Unknowns keep coverage incomplete, even if all other assessed checks pass.
8. **How is severity chosen?** This project triages root MFA failure as critical, public-prevention/console MFA/admin ingress/trail gaps as high, and the stricter KMS baseline as medium. Reviewers must adjust for actual data, exposure and compensating controls; these are not CVSS scores.
9. **What happens when only part of delivery succeeds?** The error propagates. JSON might already exist when HTML fails. A retry may create duplicates; durable idempotency is future work.
10. **Did you deploy scheduling or send email?** No. The SAM configuration and mock delivery are implemented. The permitted demo/walkthrough shows the design; live IAM, schedules and email require a pilot.
11. **What does it cost?** At the declared 30-run small-scope scenario, about $0.02/month base and $4.12 with optional monitoring, before credits and exclusions. These are estimates, not a bill. Dashboard/metric/alarm charges dominate; see VALUE_AND_COST.md for all inputs and sources.
12. **What time does it save?** Assuming 15 manual minutes and 5 minutes of review per daily run, 30 runs release 5 staff hours/month. Human review remains necessary. Actual savings need a same-scope pilot; local mocked latency does not establish cloud performance.
13. **Why not use AWS Config or Security Hub?** Those are sensible managed alternatives for broader governance. This capstone demonstrates transparent, testable automation for a small explicit baseline, not an enterprise replacement.
14. **How does it scale?** Current scans are sequential, one account with explicit regions/buckets. Lambda timeouts, inventory pagination and quotas limit scale. Add scoped fan-out, rate control and idempotency before organization-wide rollout.
15. **How do you update controls?** Version the baseline, change pass/fail semantics deliberately, add regression cases for relevant real failures, regenerate reports and document changed interpretation. Do not silently redefine historical pass rates.
16. **Does a passing report establish HIPAA compliance?** No. It answers five configuration questions within declared scope. Healthcare compliance also requires organizational, contractual and operational evidence beyond these checks.
17. **What is the first production improvement?** A small authorized pilot to validate effective permissions and delivery, followed by missed-run detection and duplicate suppression. Alarms currently have no automatic notification actions.
18. **How do you know the implementation works?** Use the current saved pytest output, deterministic scenario comparisons and template lint in examples/submission-validation.json. These prove offline behavior and static contracts, not live cloud operation.

Rehearsal target: 15–17 minutes speaking/demo, leaving 2–3 minutes for questions within a 20-minute slot. Keep the demo below five minutes. Prepare the local backup before presenting. Avoid opening real account credentials or sensitive report identifiers during screen share.
