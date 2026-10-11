# English demo walkthrough

Allocate about 3–4 minutes within the 12-slide, 15–20-minute presentation. Open the demo from slide 8 or 12. The hosted link currently requires the owner's signed-in session; for an offline backup, open `demo/index.html` from the extracted ZIP.

## Opening

“This demo uses synthetic AWS responses and recorded outputs from the actual Python checker. It does not access AWS, change infrastructure or send email. I will show a confirmed failure, a passing baseline and an incomplete scan.”

## 1. Misconfigured

Select **Misconfigured**. Point to 0 passed, 6 failed, 0 unknown and 1 not applicable. Select root MFA and inspect evidence, severity and the recommended next step. Explain that root MFA is CRITICAL, four failures are HIGH and the stricter S3 KMS baseline gap is MEDIUM.

Open **Input configuration** to show the AWS-shaped fixture. Open **Notification preview**: delivery is PREVIEW_ONLY; its summary avoids sending detailed findings. Download JSON or HTML to show that results are portable.

“A failed BPA baseline does not prove actual public access. Likewise, an open security-group rule is not proof of network reachability. These findings direct further review.”

## 2. Compliant

Select **Compliant**. Show 6 passed and 1 not applicable. The service identity has no console login profile. The alert is NOT_REQUIRED.

“PASS means this baseline passed within the configured scope. It does not certify HIPAA compliance or every AWS resource.”

## 3. Incomplete

Select **Incomplete**. Show 5 passed, 1 unknown and 1 not applicable. The S3 encryption read returns AccessDenied. Select that finding and show the captured error.

“The assessed pass rate is 100 percent because every assessed result passed. Coverage is still incomplete. The checker refuses to convert missing evidence into a pass.”

## Execute the scanner locally

Unlike the website replay, these commands execute the same scanner used by the live entry point, using boto3 Stubber and no network transport:

```bash
python -m medtech.cli demo compliant --out reports
python -m medtech.cli demo misconfigured --out reports
python -m medtech.cli demo incomplete --out reports
```

Expected exit codes are 0, 1 and 2, respectively. Do not run them as a success-only shell chain. Each produces deterministic JSON, Markdown, HTML and delivery-preview files.

## Closing

“The evidence demonstrates working offline checks and report generation. The Lambda handler, daily/weekly EventBridge design, encrypted report storage, optional monitoring and SNS summary path are implemented and tested with mocks. A real authorized cloud pilot is still needed to verify IAM, scheduling, cloud delivery, scale and cost.”
