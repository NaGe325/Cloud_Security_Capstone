# Engineer Option A requirement and rubric coverage

Primary guide: [Cloud Security Engineer](https://github.com/georgewerbacher/cmu-cloud-sec-documentation/blob/main/pages/capstone/capstone_engineer.md), reviewed October 16, 2026. This is a coverage checklist, not a predicted grade. Delivery and Q&A cannot be verified from repository files.

| Requirement | Implementation / evidence | Presentation location | Limit |
|---|---|---|---|
| 3–5 security items | medtech/checks.py, five control groups | 6 | Narrow configuration baseline |
| Daily/weekly execution | template.yaml, ScheduleExpression / EnableSchedule | 4–5 | Implemented design, not observed cloud runs |
| SNS/email notifications | medtech/delivery.py, mock tests, delivery previews | 4, 8–9 | No real send or subscription confirmation |
| Simple report | report.py, html_report.py, examples/ | 8–9 | Synthetic data |
| Lambda design | lambda_handler.py | 4–7 | Demo default, real execution unverified |
| Trigger and deployment design | template.yaml, deploy/build_package.py, PILOT_RUNBOOK.md | 4–5, 11 | SAM deploy unverified |
| Basic error handling | UNKNOWN, pagination, retries, output exceptions and queues | 7 | Duplicate delivery and liveness remain risks |
| Problem, pain points, benefits | VALUE_AND_COST.md | 2–3, 10 | Savings labeled as assumptions |
| Input, processing, output demonstration | demo/, three CLI scenarios | 8–9 | Local fallback avoids hosted access dependency |
| Value, cost and success metrics | value_model.py, value-model.json, VALUE_AND_COST.md | 10 | Production targets distinct from measurements |
| Future enhancements / scaling | README limits, QA_PREPARATION.md | 11 | No broad coverage claims |
| 10–12 slides, names and context | Updated original PDF, preserved source, English notes | 1–12 | Rehearse actual timing |

## Rubric evidence

- **Solution Design (30):** architecture and data flow, explicit service roles, meaningful trust boundaries, alternatives and trade-offs in WELL_ARCHITECTED.md.
- **Technical Understanding (25):** five defined baselines, API evidence, IAM scope, MFA/encryption/reachability caveats and failure behavior.
- **Implementation Plan (20):** SAM design, safe staged pilot, rollback and acceptance evidence in PILOT_RUNBOOK.md.
- **Demo/Walkthrough (15):** reproducible compliant/misconfigured/incomplete scenarios, readable key finding and output, local fallback.
- **Professional Quality (10):** consistent 12-slide deck, author names, source notes, concise speaking script, citations, explicit estimates and AI-use disclosure.

Outstanding student actions: review and accept the content, reconcile earlier AI-use records, rehearse, verify contributions/names, and submit through Canvas. No repository can guarantee a score or a live presentation result.
