# 录制全过程：原版 Slides + 英文逐字稿 + 中文操作

适用版本：原版 12 页 PDF 的补全稿 `slides/MedTech-Security-Baseline-Slides.pdf`。本稿不要求增加 slides。建议录成 16–18 分钟，整段不超过 20 分钟。时间表是排练目标，不是自动计时结果；如果实际低于 15 分钟，在 demo 中多解释证据和结果，不要用静默凑时长。

需要无中文提示的照读版，打开 [RECORDING_SCRIPT_EN.md](RECORDING_SCRIPT_EN.md)。

**怎么用：只读英文引用块。中文、时间、按钮名和操作提示不读。** 你可以一个人讲完整段，也可以两人按实际安排分讲。不要把建议的讲解分工说成代码贡献分工。

## 0. 先把桌面准备好，暂时不要录

1. 使用这个工作目录的文件，或解压最新 ZIP。不要用 `slides/original/` 里的旧 PDF，也不要打开没有同步修改的在线 Google Slides。
2. 在同一个 Chrome 窗口准备三个标签，按这个顺序摆好：
   - 标签 1：`slides/MedTech-Security-Baseline-Slides.pdf`。可以把 PDF 拖入 Chrome。使用 PDF 工具栏的页码框跳页。
   - 标签 2：`demo/index.html`。双击或拖入 Chrome。本地页面不需要登录、服务器或 AWS。
   - 标签 3：`demo/reports/misconfigured.html`。这是和 demo 配套的完整报告，提前打开，避免录制时找下载文件。
3. 在 Mac Chrome 中，Command+1/2/3 可以切换这三个标签。若窗口还有其他标签，先把这三个移到最左侧，避免序号不一致。
4. 把这份讲稿放在另一个窗口、另一块屏幕或手机上。英文是逐字稿，不需要把讲稿展示给观众。
5. 关闭不相关标签，打开“勿扰”，隐藏个人聊天和通知。浏览器缩放先用 100%；如果 demo 证据太小，调到 110% 或 125%，然后试滚动看一遍。
6. 到标签 2，点击 **Misconfigured**，再点击 **Findings & actions**。根用户 `root` 的 CRITICAL 发现应排在最前，通常已经默认选中。
7. 滚到网页顶部；到标签 3 确认报告能打开；回标签 1 的第一页。三个页面都加载好后再录。
8. 录十秒测试：说一句英文，切一次 PDF/demo，停止后回放，确认声音和文字清楚，再正式录制。

### 可选：准备一个实际执行 Python 的终端

网页是录好的结果回放。为了展示实际代码执行，可以在 slide 8 的 demo 最后加约 30–45 秒终端演示。它是加分展示选择，不是必须项。先在录制前试运行，不要现场安装依赖。

这台电脑已经准备好了 Python 3.12 环境。在终端分别执行：

```bash
cd '/Users/xinyizhang/Documents/ChatGPT/ds面试/Cloud_Security_Capstone'
source build/venv312/bin/activate
python -m medtech.cli demo misconfigured --out reports/recording
```

如果你在另一台电脑使用 ZIP，应先按 README 创建环境，不能假设 `build/venv312/` 存在于 ZIP。录制时只重跑最后一行，不要展示本机路径、安装过程或历史命令。

期望看到：`status: FAIL`，0 PASS、6 FAIL、0 UNKNOWN、1 NOT_APPLICABLE，`sns: PREVIEW_ONLY`。退出码 1 是发现失败配置的设计结果，不是程序崩溃。需要时可预先清空终端显示，只保留命令和结果。

## 1. 如何开始录制

在 Mac 可以按 **Shift+Command+5** 打开录屏工具，选择录制整个屏幕或选定区域，在“选项”里选择麦克风。先用十秒试录确认实际录到了声音。不要仅凭麦克风已选中就假设录制成功。

正式录制开始时：标签 1、第一页已经展示，鼠标不要挡标题。停 1–2 秒，然后开始讲。每次翻页后停约半秒再开口。切页面前先说过渡句。

如果老师指定了别的录制工具，保留下面的展示顺序，使用指定工具即可。Canvas 已查看的作业页没有额外规定视频格式或录制软件。

## 2. 一眼看懂的录制顺序

| 目标时间 | 画面 | 主要内容 |
|---|---|---|
| 0:00–0:50 | Slide 1 | 作者、Engineer Option A、离线范围 |
| 0:50–1:45 | Slide 2 | MedTech 问题与人工检查痛点 |
| 1:45–2:40 | Slide 3 | 自动化机会和 UNKNOWN |
| 2:40–4:00 | Slide 4 | EventBridge/Lambda/读 API/报告/通知 |
| 4:00–5:00 | Slide 5 | 权限、账号和输出开关 |
| 5:00–6:45 | Slide 6 | 五类检查及判断边界 |
| 6:45–7:45 | Slide 7 | 错误处理与证据完整性 |
| 7:45–12:00 | Slide 8，然后标签 2/3 | 三场景、输入、证据、通知、报告；可选 CLI |
| 12:00–12:45 | Slide 9 | 结果如何交给审核者 |
| 12:45–14:30 | Slide 10 | 测试、时间和费用模型 |
| 14:30–15:30 | Slide 11 | 试点和后续改进 |
| 15:30–16:15 | Slide 12 | 收尾 |

不用硬追每个时间点。以自然语速、清楚的操作和总时长 15–20 分钟为准。

## Slide 1 — MedTech Security Baseline Checker

**操作：** 标签 1，第一页。指一下你们的名字，不点击任何链接。约 50 秒。

> Hello, we are Charlotte Zhang and Nana Ge. Our project is the MedTech Security Baseline Checker, for the Cloud Security Engineer track, Option A.
>
> The tool makes five recurring AWS configuration checks repeatable and easier to investigate. It uses Python and boto3, produces structured evidence, and includes a Lambda-based deployment design.
>
> We will explain the problem, architecture, control logic, demonstration, and operational value. Today's demonstration is offline and uses synthetic AWS responses. We have not deployed the stack to AWS or sent real notifications. PASS applies only to our selected technical baseline and configured scope.
>
> Let us start with the problem.

## Slide 2 — Cloud configuration changes need repeatable security review

**操作：** 翻到第二页。鼠标从左到右指出三个区域，重点是人工工作重复、证据需要解释。约 55 秒。

> MedTech's AI teams create and change training buckets, identities, and compute resources. Those changes create recurring questions about access, preventive controls, and administrative logging.
>
> A reviewer can inspect these settings manually, but repeatedly collecting the same evidence takes effort. Inconsistent notes also make it harder to compare runs or understand what was actually checked.
>
> Our checker collects that evidence in a consistent format, identifies baseline gaps, and explains why they were flagged. Findings still need contextual review. For example, an open security-group rule alone does not prove internet reachability.
>
> This makes a small, clearly defined baseline a useful automation opportunity.

## Slide 3 — Make five technical controls repeatable and reviewable

**操作：** 翻到第三页。指 Scope、Evidence、Unknowns 三行即可，不逐行念表格。约 55 秒。

> This comparison shows what the checker adds to a reviewer-led workflow. Its scope is explicit: an account, selected regions, and selected buckets. It does not claim to assess every resource in the organization.
>
> Each finding includes a resource, status, reason, evidence, and suggested next step. Reports make those results portable and comparable across runs.
>
> UNKNOWN is particularly important. If a permission error prevents a configuration read, the checker cannot conclude that the resource passed. It preserves the evidence gap and marks coverage incomplete.
>
> We have measured offline behavior, but have not measured production time savings or detection latency. The later value model states its assumptions separately.

## Slide 4 — Read-only scanning, gated cloud delivery

**操作：** 翻到第四页。顺着左侧 EventBridge → 中间 Lambda → 上方 AWS services → 右侧 S3/SNS/CloudWatch 说明。图上输出是连接关系；实际执行顺序用话说明。约 80 秒。

> The proposed cloud workflow starts with an EventBridge rule for daily or weekly execution. It invokes a Python Lambda function that reads configuration through AWS APIs.
>
> The scanner evaluates S3, IAM, EC2, and CloudTrail settings. When outputs are enabled, the AWS branch writes JSON and HTML reports to S3, sends an SNS summary for failed or unknown findings, and then publishes optional metrics.
>
> The report bucket is private, KMS-encrypted, and requires secure transport. SNS carries summary counts and a report pointer rather than detailed evidence. CloudWatch provides logs and optional monitoring.
>
> Separate queues cover EventBridge delivery failures and exhausted Lambda asynchronous failures. Retries can still duplicate output, which remains a production improvement.
>
> The template is implemented, but real scheduling and cloud delivery remain unverified and are disabled by default. The next slide explains the permission boundaries.

## Slide 5 — Explicit scope and independently gated outputs

**操作：** 翻到第五页。指出 IAM+STS、S3+KMS、SNS+SQS 三行。约 60 秒。

> Configuration reads, report writes, notifications, and metrics have distinct permissions and enable switches.
>
> Before a real scan, STS verifies the expected AWS account. S3 requests specify the expected bucket owner. These checks reduce accidental scanning of the wrong scope.
>
> The command-line tool writes local reports. Lambda can use cloud outputs only when configured, and incoming events cannot expand scope or enable those operations.
>
> The sample template targets one existing bucket in the deployment region. Expanding scope requires matching policy changes. Deploying the stack would create real resources even if scanning stayed disabled, so deployment still requires a reviewed plan.
>
> These boundaries support a controlled pilot.

## Slide 6 — Five controls, evidence-backed findings

**操作：** 翻到第六页。先沿五步流程指一遍，再解释五行控制。这里最能体现技术理解，约 1 分 45 秒。

> The workflow collects configuration, evaluates the baseline, stores reports, notifies when needed, and publishes optional metrics. We implement five control groups.
>
> First, S3 public access checks the combined account and bucket Block Public Access flags. Failure indicates an incomplete preventive baseline, not proof of a data leak.
>
> Second, S3 encryption requires default SSE-KMS or DSSE-KMS. This is a stricter project policy. SSE-S3 remains valid encryption even though it fails this KMS baseline.
>
> Third, IAM MFA checks enrollment for root and users with console profiles. Enrollment does not prove enforcement. A service user without a console profile is not applicable to this check.
>
> Fourth, EC2 ingress checks direct internet-wide IPv4 or IPv6 rules covering ports twenty-two or thirty-three eighty-nine. Routing and public IPs also affect actual reachability.
>
> Finally, CloudTrail checks active management-event logging, read and write coverage, global events, and the reported delivery condition.
>
> Five groups produce seven demo results because root, a console user, and a service user have separate MFA results. Severity guides project triage rather than establishing a complete risk or compliance judgment.

## Slide 7 — Unknown evidence stays unknown

**操作：** 翻到第七页。先指左边错误处理，再指右边安全边界。约 60 秒。

> The checker distinguishes confirmed failures from unavailable evidence. Expected AWS errors become UNKNOWN, while independent checks continue. Inventory pagination must complete before an inventory conclusion is drawn.
>
> Retries are bounded. Unexpected program errors and delivery failures propagate rather than becoming misleading passes.
>
> Partial delivery remains possible: JSON might upload before HTML fails, and a retry can duplicate output. Durable deduplication is not implemented.
>
> Offline mode blocks AWS transport. The scanner reads configuration, does not read patient objects, and makes no automatic remediation. Optional alarms have no notification actions and cannot detect missed runs.
>
> We will now demonstrate confirmed gaps, passing results, and incomplete evidence.

## Slide 8 — Three scenarios, one reproducible checker

**操作：** 先停留第八页读下面开场，再 Command+2 切到本地 demo。不要点击在线链接，以免遇到登录页。整个环节约 4 分钟，可选终端会增加约 30–45 秒。

> This demonstration uses synthetic AWS responses and recorded outputs from the actual Python checker. The browser replays those results; it does not execute Python or connect to AWS. I will show the input, a confirmed failure, the notification preview, and the difference between a passing and an incomplete scan.

### Demo 8A — 确认错误配置场景，约 25 秒

**你做：** 标签 2 → 滚到顶部 → 点击 **Misconfigured** → 点击 **Findings & actions**。

**画面应该看到：** FAIL；Passed 0、Failed 6、Unknown 0、Not applicable 1。

> We start with the misconfigured scenario. The report contains zero passing results, six confirmed baseline failures, zero unknowns, and one result that is not applicable. These are seven resource-level results across five control groups, rather than seven independent controls.

### Demo 8B — 展示最重要的发现与原始证据，约 35 秒

**你做：** 往下滚到 **Prioritized findings**。选中资源为 **root**、严重性为 **CRITICAL** 的 MFA 行。默认通常已经选中；不要误选资源名为 analyst 的 HIGH 行。

**画面应该看到：** 右边资源 root、建议行动、**OBSERVED EVIDENCE** 中 `AccountMFAEnabled: 0`。

> The first item is root MFA, which receives critical triage priority in this project. The observed value is AccountMFAEnabled equal to zero. The report preserves that evidence and recommends protecting root access with MFA, or verifying a documented centralized root-credential removal arrangement where appropriate.
>
> The reviewer should validate the account context before making changes. This is a synthetic configuration finding, not an observed account compromise.

### Demo 8C — 展示输入，约 25 秒

**你做：** 点 **Input configuration**。先指简明输入列表；可点击 **Inspect the complete AWS response fixture** 展开 JSON，停 2–3 秒后折叠。不用在视频里逐行解释 JSON。

> This tab shows the AWS-shaped input configuration behind the scenario. The complete fixture records the responses used by the offline scanner. Using fixed input and run identifiers makes the reports reproducible and allows us to test the same behavior repeatedly.

### Demo 8D — 展示通知预览，约 25 秒

**你做：** 点 **Notification preview**。

**画面应该看到：** Delivery 为 `PREVIEW_ONLY`；Subject 为 `MedTech baseline: FAIL`。在这个离线 demo 中 `report_uri` 可以是 null，因为没有上传 S3。

> The notification is preview-only. Its subject indicates a failed baseline, and its body includes summary counts rather than detailed evidence. No email has been sent. A report pointer is populated when real report storage succeeds; in this offline preview, no S3 report has been stored.

### Demo 8E — 切换全部通过场景，约 25 秒

**你做：** 滚回顶部 → 点 **Compliant**。看上方计数，再滚到 **Notification preview**；如果不在这个 tab，就手动点一下。

**画面应该看到：** 6 PASS、0 FAIL、0 UNKNOWN、1 N/A；通知为 `NOT_REQUIRED`。

> In the compliant scenario, all six assessed results pass and one service identity is not applicable because it has no console login profile. No failure or unknown notification is required. PASS means this selected baseline passed within the configured scope; it does not certify all AWS resources or HIPAA compliance.

### Demo 8F — 切换证据不完整场景，约 40 秒

**你做：** 滚到顶部 → 点 **Incomplete** → 点 **Findings & actions**。网页切换场景不会自动切换 tab，所以这一步不要省略。选中 UNKNOWN 的 S3 encryption 行，或确认它已默认选中。

**画面应该看到：** 5 PASS、0 FAIL、1 UNKNOWN、1 N/A；证据有 `AccessDenied`。

> The incomplete scenario is different. Five assessed results pass, but the S3 encryption read returns AccessDenied. The checker records UNKNOWN because it lacks enough evidence to decide whether that baseline passed or failed.
>
> The assessed pass rate can still be one hundred percent because unknown and not-applicable results are excluded from that denominator. Coverage remains incomplete. A high pass rate must never hide an evidence gap.

**如果时间够：** 往下滚到 **03 / COMPARE THE OUTCOMES**，指一下 Incomplete 的 100% 和 incomplete 状态。不要停留过久。

### Demo 8G — 展示可导出的报告，约 25 秒

**你做：** 滚回顶部 → 点 **Misconfigured** → 点 **Findings & actions** → 点 **Download HTML**。随后 Command+3 切到提前打开的 `demo/reports/misconfigured.html`。

**注意：** 下载文件可能只保存、不自动打开。提前打开的标签 3 是同一场景的配套报告，不要说它是刚刚生成的新 AWS 扫描。

> The results are portable. I can download the HTML report or the JSON evidence. Here is the same misconfigured-scenario report in its standalone HTML form. It retains the overall result, scope, individual findings, evidence, and suggested actions so a reviewer can investigate outside this interface.

### 可选 Demo 8H — 展示 Python 实际执行，约 30–45 秒

**你做：** 切到提前准备好的终端，只执行：

```bash
python -m medtech.cli demo misconfigured --out reports/recording
```

**展示结果后读：**

> Unlike the browser replay, this command actually runs the Python scanner using boto3 Stubber responses. It generates the local reports and returns the expected failed-baseline result. It still performs no live AWS calls or cloud delivery. Exit code one represents confirmed findings, not a crash.

**不要做：** 不跑 `scan --allow-aws-read`、不部署 SAM、不填邮箱、不去 AWS 控制台制造漏洞，也不现场跑完整测试套件占时间。

### Demo 结束过渡

**你做：** 回 Chrome → Command+1 → PDF 页码框输入 9。

> These scenarios show a confirmed gap, a passing baseline, and an evidence gap. Let us return to the slides and summarize what the security reviewer receives.

## Slide 9 — Prioritize the risk, inspect the evidence

**操作：** 第九页。指原有报告截图，再指右下角放大的 `AccountMFAEnabled: 0`。约 45 秒。

> This slide summarizes the review workflow. The report screenshot shows six failed results. Root MFA receives the highest triage priority, followed by examples such as console-user MFA and administrative ingress.
>
> The enlarged evidence makes one observation readable: AccountMFAEnabled equals zero in the synthetic fixture. It connects a specific configuration fact to a suggested next action.
>
> The notification summarizes the result, while the report preserves the detail for investigation. We will now explain the validation and estimated operational value.

## Slide 10 — Validation and estimated operational value

**操作：** 第十页。先指上面的 88/3/5/0，再左下时间、右下费用。不要逐位读小数；说预算 $0.02 和 $4.12 即可。约 1 分 45 秒。

> We separate measured validation from estimated value. We have eighty-eight passing tests, three reproducible scenarios, five control groups, and zero real AWS deployments. The template check and report comparisons also passed. These checks do not establish production performance or cloud delivery.
>
> For time savings, assume fifteen manual minutes per run, including five minutes to interpret evidence. Automation retains those five review minutes. Across thirty runs, the ten-minute difference releases five hours per month, a sixty-six-point-seven percent reduction for these checks.
>
> At an assumed sixty dollars per hour, that represents three hundred dollars of staff capacity, not measured savings or a payroll reduction. Setup and maintenance are excluded.
>
> The cost model assumes one small account and bucket in Northern Virginia, thirty daily runs, two hundred fifty-six megabytes of Arm memory, and thirty seconds per run. Rounded-up monthly budgets are about two cents base, or four dollars twelve with optional monitoring.
>
> These are estimates before credits, taxes, and stated exclusions. Assumptions, arithmetic, and AWS sources are included in the repository. A pilot must measure actual cost, runtime, and review effort.

## Slide 11 — A bounded path to production

**操作：** 第十一页。从右边试点开始，接着中间运维、左边扩展。约 60 秒。

> Our next step is a small authorized pilot. We would validate effective permissions, KMS policies, report storage, one approved notification recipient, and actual scheduled execution. We would measure runtime and cost for that scope.
>
> Operational improvements include durable deduplication, partial-delivery recovery, and missed-run detection. Current alarms do not establish schedule liveness.
>
> Later checks could cover SageMaker settings, KMS policies, federated MFA, RDS, and CloudTrail data events or freshness. More accounts and regions would require matching permissions and scale tests.
>
> Human review remains necessary before any remediation.

## Slide 12 — Summary

**操作：** 第十二页。保持结束页，不再次点击在线 demo。约 40–45 秒。

> To conclude, this project implements five repeatable AWS configuration controls, preserves reviewable evidence, and makes uncertainty visible.
>
> The repository includes runnable offline code, reproducible scenarios, reports, tests, and a cloud deployment design. A real pilot remains necessary to validate permissions, scheduling, delivery, scale, and economic assumptions.
>
> The result is a consistent starting point for reviewing MedTech's AI infrastructure. Thank you for watching.

**说完：** 保持结束页约 2 秒，停止录制。不要留下长时间找停止按钮的画面。

## 3. 录完只检查这六件事

1. 总时长在 15–20 分钟；没有把安装、等待或无关聊天录进去。
2. 麦克风全程有声，切屏时声音没有中断。
3. 五类检查和三种场景都讲到，root 和 AccessDenied 的证据清楚可见。
4. 明确说了“网页回放／离线模拟，未部署 AWS、未发真实邮件”。
5. 时间和成本都明确是带假设的模型，没有说成实测结果或完整 HIPAA 合规。
6. 提交的是补全后的 PDF、项目包和老师要求的视频／链接；上传后在 Canvas 核对成功状态。文件名可用 `MedTech_Capstone_Charlotte_Zhang_Nana_Ge.mp4`，但不要只改后缀来转换视频格式。

## 4. 演示出问题时可以直接说的话

**在线链接要求登录：** 不现场登录。切到本地 demo。

> I will use the self-contained local replay, which contains the same recorded scenario outputs and does not require network access.

**下载不自动打开：** 切标签 3。

> I have opened the same standalone report in another tab so we can inspect it directly.

**终端环境有问题：** 跳过可选终端，不现场修依赖。

> The reproducible commands and saved test evidence are included in the repository. The scenario walkthrough shows their recorded outputs.

**切场景后还在通知 tab：** 手动点 Findings & actions，继续讲，不用道歉重录整段。

**读错一句：** 停一秒，从这一句话重新开始；录后可以剪掉错误片段。不要因为小口误删掉整段 demo。

## 5. 不能说的六句话，以及准确说法

| 避免说 | 准确说法 |
|---|---|
| We deployed this to AWS. | We implemented and tested the offline checker and included a cloud deployment design. |
| This website scans AWS. | The website replays recorded offline scan outputs. |
| Our tool proves HIPAA compliance. | PASS applies only to this technical baseline and configured scope. |
| SSE-S3 means no encryption. | SSE-S3 is encrypted but does not meet our stricter KMS baseline. |
| We measured five hours of savings. | Under the stated timing assumptions, the model releases five hours per month. |
| UNKNOWN means secure. | UNKNOWN means there is insufficient evidence; coverage remains incomplete. |

## 6. 发音和术语备忘

- IAM：逐字母 I–A–M。
- MFA：M–F–A。
- S3：S three。
- EC2：E–C two。
- KMS：K–M–S。
- SNS：S–N–S。
- SQS：S–Q–S。
- boto3：可以说 “boto three”。
- Stubber：说明成 “mocked AWS responses” 也容易理解。
- PHI：protected health information；这份演示没有读取患者记录。

技术内容依据：原版 PDF、medtech/checks.py、medtech/cli.py、demo/index.html、demo/app.js、examples/*.json、template.yaml、docs/VALUE_AND_COST.md。成本来源和课程指南链接见 SPEAKER_NOTES.md。录制稿对应本仓库当前版本，不代表老师另行要求必须采用某种视频格式。
