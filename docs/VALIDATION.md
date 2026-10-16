# Validation record

Date: 2026-10-11. macOS arm64, Python 3.12.10. Dependencies are pinned in requirements-dev.lock. All AWS interactions in this validation were mocked or disabled.

| Check | Measured result |
|---|---|
| Unit, API-contract and integration tests | 88 passed |
| Scanner statement coverage | 100% |
| Entire medtech package statement coverage | 370/371, 99.73% |
| Uncovered statement | CLI __main__ dispatch; separately exercised by subprocess demos |
| Compliant | 6 PASS, 0 FAIL, 0 UNKNOWN, 1 N/A; exit 0 |
| Misconfigured | 0 PASS, 6 FAIL, 0 UNKNOWN, 1 N/A; exit 1 |
| Incomplete | 5 PASS, 0 FAIL, 1 UNKNOWN, 1 N/A; exit 2 |
| Misconfigured severity | 1 CRITICAL, 4 HIGH, 1 MEDIUM |
| SNS preview | NOT_REQUIRED for compliant; PREVIEW_ONLY for failure and unknown |
| Mock output delivery | JSON + HTML S3 parameters, expected owner, encryption, summary SNS and optional metric payloads verified |
| Partial delivery | HTML failure after JSON upload propagates rather than claiming complete storage |
| Browser | Three scenarios, all tabs, JSON/HTML downloads, widths 1400/768/360; no JavaScript errors or horizontal overflow |
| Google Slides | 12 slides rendered and individually inspected; structural checker reported zero issues; native links on slides 8 and 12 |

Raw pytest output: examples/test-results.txt. Coverage: examples/coverage.json. Reproducibility, independent Lambda source-package and template-lint results: examples/integration-results.json. Packaging verification also records wheel execution outside the source tree.

The three fixtures use fixed timestamps, run IDs and synthetic identifiers. JSON, Markdown, HTML and delivery previews are byte-compared with examples on rerun. The scanner uses actual boto3 clients intercepted by botocore Stubber, including request-parameter and response-model validation. Tests block AWS HTTP transport; the offline provider has a separate before-send block.

The website is a recorded replay, not a hosted Python scanner. Its new version was published through Sites; that publication is unrelated to deploying AWS infrastructure.

Not verified: SAM CLI build/deploy, real CloudFormation resources, effective IAM/SCP/key policies, EventBridge timing, SNS confirmation/email, actual S3 storage, production scale or full HIPAA compliance. Passing mocks and static validation must not be described as a production deployment. Optional monitoring has no alarm notification actions or missed-run detector.

## October 16 submission revision

Current offline verification is saved in examples/submission-validation.json and examples/test-results-current.txt. On Python 3.12.15, all 88 tests passed, cfn-lint returned zero, and the CLI's JSON/MD/HTML/delivery outputs matched the committed examples byte for byte for all three scenarios (expected exit codes 0, 1, 2). The cost-model output also matched. Python 3.13.7 passed the same suite earlier during preparation. Five synthetic executions per scenario were measured separately in examples/offline-benchmark.json; these are not AWS latency measurements.

The revised 12-slide PPTX passed structural, geometry/font-declaration, native-table and Artifact Tool import checks. The PDF companion uses locally configured, bundled Open Sans and LibreOffice. All 12 final PDF pages were visually reviewed. These checks do not establish native Microsoft PowerPoint behavior. Earlier Google Slides and hosted-site validation above refers to the prior version; neither remote artifact was edited in this revision. Live AWS limitations remain unchanged.
