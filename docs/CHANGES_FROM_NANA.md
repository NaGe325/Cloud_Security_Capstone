# 在 Nana 原项目基础上改了什么

对比基线：Nana 原仓库提交 `79d6c6e6a4a57d46495c8e77dea893503977b12e`。这里描述文件差异，不推断两位同学实际如何分工，也不把 AI 辅助工作记为某位同学独立完成。

## Nana 原来已经完成的部分

原项目已经有 Python/boto3 的五类检查、三种离线 fixture、JSON/Markdown/HTML 报告、Lambda 入口、SAM 模板、SNS/S3/CloudWatch 相关逻辑、88 项测试、交互 demo、12 页英文 PDF 和讲稿。不是从零重做，也不是我新增了这些核心能力。

## 核心实现未改

通过 Git 对比确认，以下路径相对于原始提交没有文件内容变化：

- `medtech/`：全部检查、报告、Lambda、交付和监控逻辑。
- `tests/`：原来的 88 项测试；我做的是重新运行和核验，没有把它们说成新增测试。
- `template.yaml`、`deploy/`：云架构配置和打包代码。
- `demo/`：交互网站代码、数据和报告。
- `report.schema.json`、`pyproject.toml`、原有运行／开发依赖。

没有真实部署 AWS、没有扫描真实账号、没有发邮件，也没有替你们提交 Canvas。

## 原版 slides 只修改四页

| 页 | 原版情况 | 补全内容 |
|---|---|---|
| 1 | 有项目标题和 Engineer Option A，没有两人姓名 | 在原版空白处补 Charlotte Zhang and Nana Ge |
| 6 | 流程末尾为 Measure 后 Notify，与 AWS 分支实际顺序不一致 | 改成第 4 步 Notify、第 5 步 Measure；原流程框和表格保留 |
| 9 | 有真实离线报告截图和三条重点发现 | 保留截图，并放大补出模拟 root 证据 `AccountMFAEnabled: 0` |
| 10 | 有 88 测试、3 场景、5 控制、0 部署，但缺时间和成本计算 | 保留四个指标，在下方补带假设的人工时间模型和云成本预算 |

第 2、3、4、5、7、8、11、12 页的内容流保持一致，且与原版渲染结果逐像素相同。原 PDF 保存在 `slides/original/`；`examples/slides-preservation.json` 记录哈希和保留检查。

曾经生成过一个重建版本。收到“用原版继续”的要求后，已弃用，不放入最终提交包。在线 Google Slides 没有同步修改；最终使用仓库 PDF。

## 新补的分析与提交材料

- `docs/VALUE_AND_COST.md` 与 `scripts/value_model.py`：可复算的时间／费用假设、敏感性和 AWS 来源。
- `docs/WELL_ARCHITECTED.md`：现有工程设计与 AWS 安全支柱原则的对应、取舍和限制。
- `docs/COURSE_ENVIRONMENT.md`：课程 Terraform 源码与五项检查的关系，区分静态源码、模拟数据和真实环境。
- `docs/PILOT_RUNBOOK.md`：未来真实 AWS 试点的顺序、验收证据和失败处理，不是已完成的云部署记录。
- `docs/RUBRIC_COVERAGE.md`：Engineer 要求和评分维度的证据索引，不是预计得分。
- `docs/QA_PREPARATION.md`、中文答辩速记、`RECORDING_WALKTHROUGH.md`：答辩准备、英文逐字稿和中文点按步骤。
- `docs/SUBMISSION.md`、AI 使用说明、README 更新：提交说明、材料索引和需要补充的历史记录边界。

## 新补的验证和辅助脚本

- 重新验证 Python 3.12 下的 88 项测试、cfn-lint 和三种 CLI 场景；报告与原例子逐字节一致。
- 保存当次验证记录和单独的本地模拟计时，未把本地计时说成真实 AWS 性能。
- 添加 `.github/workflows/offline-validation.yml`，让分支运行相同的离线检查。
- 添加 `scripts/verify_submission.py`、`package_submission.py`、`update_original_slides.py` 等复现／打包辅助脚本。这些辅助脚本不扩展五类检查的功能。
- 重新制作 ZIP 和 SHA256 校验文件，排除虚拟环境、Git 数据和本地构建目录。

## 交付位置

由于当前账号不能直接写 Nana 的仓库，修改放在 `xinyizh4-charlotte/Cloud_Security_Capstone` 的 `codex/capstone-submission` 分支，并创建了到原仓库的 [草稿 PR #1](https://github.com/NaGe325/Cloud_Security_Capstone/pull/1)。在 Nana 合并前，原仓库 main 不会自动包含这些修改。

一句话概括：**Nana 原来已经完成主要工程项目；我补齐评审发现的展示与证据缺项，验证原实现，并做了录制和提交准备。** 实际作者贡献需要你们自己据实说明。
