# Operational value and cost model

Planning scenario: one small AWS account in us-east-1, one selected bucket, one scan per day, 30 days. All economic figures below are **illustrative assumptions**, not measured production benefits or an AWS bill. Rates reviewed October 16, 2026. Reproduce the arithmetic with `python scripts/value_model.py`; exact output is in `examples/value-model.json`.

## Time savings calculation

| Work per run | Manual workflow (assumed) | With checker (assumed) |
|---|---:|---:|
| Collect five configuration checks | 10 minutes | Automated |
| Interpret evidence and triage | 5 minutes | 5 minutes |
| Total human time | 15 minutes | 5 minutes |

Thirty runs × (15 − 5) minutes = **300 minutes / 5 hours released per month**, a **66.7% reduction in human time for these five checks**. At an assumed $60/hour this is **$300/month of staff capacity**, not cash savings or reduced headcount. Initial setup, exception investigation, false positives and maintenance can reduce or eliminate this benefit. The model does not replace a full human security review. Local synthetic timings in `examples/offline-benchmark.json` are measured separately and must never be used as real AWS latency.

Sensitivity: at 10/5 manual/automated minutes, 2.5 hours/month; at 15/5, 5 hours; at 30/5, 12.5 hours. These are scenarios, not observations. A pilot should time the same scope manually and automatically, include review and exception handling, and report median/p95 across representative runs.

## Monthly infrastructure estimate

No free-tier credits are deducted. The current template uses Arm64, 256 MB, AWS-managed S3/SNS KMS keys and a legacy EventBridge scheduled rule. It creates no customer-managed KMS key and no VPC/NAT gateway. Monitoring is optional.

| Component | Assumed usage | Unit rate (USD) | Estimated USD/month |
|---|---|---:|---:|
| Lambda Arm compute | 30 × 30 seconds × 0.25 GB | 0.0000133334/GB-second | 0.003000 |
| Lambda requests | 30 | 0.20/million | 0.000006 |
| S3 report PUTs | 60 | 0.005/1,000 | 0.000300 |
| S3 Standard report storage | 0.006 GB-month (60 × 100 KB, full month upper allowance) | 0.023/GB-month | 0.000138 |
| S3 read allowance | 1,000 GET-equivalent billable reads | 0.0004/1,000 | 0.000400 |
| KMS symmetric requests | 1,000 (allowance includes SNS/data-key reuse variability) | 0.03/10,000 | 0.003000 |
| SNS publish | 30 messages below 64 KB | 0.50/million | 0.000015 |
| SNS email | 30 deliveries to one confirmed recipient | 2.00/100,000 | 0.000600 |
| CloudWatch Logs ingest | 0.01 GB | 0.50/GB | 0.005000 |
| Logs stored | 0.01 GB-month upper allowance | 0.03/GB-month | 0.000300 |
| SQS requests | 100 requests across failure queues | 0.40/million | 0.000040 |
| EventBridge scheduled rule | 30 invocations on legacy scheduled rule | no additional rule charge | 0 |
| **Base subtotal** | Small daily pilot, outputs enabled | | **0.012799** |
| Optional custom metrics | 3 full-month metrics | 0.30/metric-month | 0.90 |
| Optional dashboard | 1 | 3.00/dashboard-month | 3.00 |
| Optional standard alarms | 2 | 0.10/alarm-month | 0.20 |
| **With optional monitoring** | Before credits, taxes and exclusions | | **4.112799** |

Round **up to the next cent** for planning budgets of **about $0.02/month base or $4.12 with monitoring** under this scenario, not a price guarantee. Some configuration APIs may be free; the S3 read line is a planning allowance. Billing units/GB conventions, hourly metric proration and actual service request mix can change totals. For a pilot, set a **$5/month review threshold**, not an enforced spending cap. Monitoring fixed charges dominate this small model. A customer-managed KMS key would add a key-storage charge and needs a separate estimate.

The estimate excludes the existing EC2/RDS/data workload, existing CloudTrail charges, cross-region/internet transfer, extra console reads, retries beyond these allowances, additional recipients, account-wide telemetry and labor. Retried Lambda execution can duplicate S3 objects and SNS delivery. The 30-second billed duration is an assumption; the timeout is 300 seconds. A pilot must measure actual duration and API counts and use AWS Cost Explorer/Calculator before expansion. No cloud resources have been deployed for this submission.

## Security value and success criteria

| Measure | Current evidence | Pilot acceptance target (not measured) |
|---|---|---|
| Rule correctness | Three synthetic scenarios and automated boundary/error tests | Preserve regression suite and review real exceptions |
| Evidence visibility | UNKNOWN remains separate from PASS, with incomplete coverage | Investigate every UNKNOWN within 1 business day |
| Report generation | Deterministic JSON/MD/HTML reports | Every completed scan has both stored JSON and HTML |
| Scheduled execution | Daily/weekly SAM design, disabled by default | 7 expected daily runs observed, no unexplained gap |
| Notification | Summary preview and mock API contracts | One deliberately triggered finding reaches one confirmed recipient |
| Runtime/cost | Offline timings and this scenario model | p95 scan under 60 seconds at declared small scope; review bill against $5 threshold |
| Human efficiency | Assumed 15 to 5 minutes per run | Measure on identical scope before claiming savings |

Daily cadence creates an intended next-run detection opportunity within roughly one day plus processing/delivery, assuming a successful scan. It does not establish a guaranteed incident detection SLA. No missed-run detector is currently implemented.

## Pricing sources

AWS pricing is regional and can change. These primary sources support the selected rate assumptions:
- [AWS Lambda pricing](https://aws.amazon.com/lambda/pricing/)
- [Amazon S3 pricing](https://aws.amazon.com/s3/pricing/) and [AWS S3 cost example](https://docs.aws.amazon.com/solutions/latest/live-streaming-on-aws-with-amazon-s3/cost-example-1.html)
- [AWS KMS pricing](https://aws.amazon.com/kms/pricing/)
- [SNS pricing](https://aws.amazon.com/sns/pricing/) and [SNS billing FAQ](https://aws.amazon.com/sns/faqs/)
- [CloudWatch pricing](https://aws.amazon.com/cloudwatch/pricing/)
- [SQS pricing](https://aws.amazon.com/sqs/pricing/)
- [EventBridge pricing](https://aws.amazon.com/eventbridge/pricing/). This template uses a scheduled rule, not EventBridge Scheduler or custom PutEvents.
