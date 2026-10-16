# Appendix: Generative AI Use Disclosure

**Project:** MedTech Security Baseline Checker

**Students:** Charlotte Zhang and Nana Ge

**Course route:** Cloud Security Engineer, Option A

**Prepared:** October 16, 2026

This appendix records the AI assistance supported by the available conversation and repository evidence. It separates the original project from the October 16 completion work. Nana's earlier tool/model details and original conversations have not been supplied, so this document does not represent those missing details as verified facts or a complete historical transcript.

## 1. Course disclosure requirement

The course syllabus permits generative AI assistance and requires acknowledgment of the tool and version, the exact prompts, and complete AI responses in an appendix. Students remain responsible for assessing the accuracy and applicability of the material they submit.

Source: [95-746 Cloud Security syllabus](https://docs.google.com/document/d/1R0i2W1b3I0vfMkByLVWrLroNgVLdEZTMxUxm4NnljsM/edit), provided by the students and read on October 16, 2026.

## 2. Assistance associated with Charlotte's October 16 session

### Formal English disclosure

Charlotte Zhang used OpenAI Codex to review the existing capstone repository against the course requirements and assist with preparing the final submission. Assistance included targeted revisions to the original presentation, supporting documentation, an illustrative time-and-cost analysis, an English recording script, offline validation, and submission packaging. The original security-checking implementation and existing test suite were retained. AI-assisted materials were checked through the verification steps documented below. The work did not include a live AWS deployment or actual SNS/email delivery. The exact deployed model version was not available in the session record.

### Tool and scope record

| Item | Available record |
|---|---|
| Tool | OpenAI Codex desktop |
| Model/version | The session identifies the assistant as GPT-6 based. The exact deployed model identifier/build is not exposed in the available record; it is not independently verified. |
| Date | October 16, 2026 |
| Inputs | Student-provided repository and course-guide links, syllabus, Canvas assignment information, and the existing project files |
| Uses | Requirement review; focused additions to the original PDF; time/cost scenario calculations; explanatory documentation; English recording manuscript; offline verification and packaging helpers |
| Extent of code changes | Added helper scripts and a CI workflow; did not change the original scanner, existing tests, demo application, SAM template or Lambda implementation |
| Final-reply translations | Preserved in the linked English exchange records below |
| Generated material | The submitted files, together with Git history, preserve the actual code, prose, slide edits and calculations used in the revised project |

The final PDF uses Nana's original 12-slide presentation directly. Only slides 1, 6, 9 and 10 received focused edits: author names, corrected Notify/Measure order, readable root-MFA evidence, and an explicitly illustrative time/cost explanation. The other eight pages retain the original content streams and rendered appearance. An earlier full rebuild was discarded and is not included in the final submission.

The recording follow-up produced an English read-aloud manuscript. Chinese rehearsal guides and a bilingual working walkthrough were subsequently removed from the submission files at the student's request. English translations of selected prompts and final AI replies are included below as disclosure records; the original-language text is excluded from this package.

## 3. Assistance associated with Nana's original project

The original project is recorded at commit `79d6c6e6a4a57d46495c8e77dea893503977b12e`, authored by **Na Ge** on **October 11, 2026**. It already contains the five-control implementation, three synthetic scenarios, reporting, Lambda/SAM design, tests, browser demo, original slides and speaker notes.

The baseline repository includes a slide-design-system provenance file referring to conversation `6acbe87a-46b4-83ea-9738-66119543c60e` and the SHA-256 of an uploaded design-system archive. Related notes describe applying that material to the presentation. This is provenance evidence; it does **not** by itself establish who used a particular AI tool, which model was selected, the exact prompts, or the complete responses. The referenced conversation could not be retrieved through the available connected account.

| Nana historical-record item | Current evidence/status |
|---|---|
| Original repository contribution | Verified by baseline commit and files |
| Design-source reference | Present in `docs/slide-design-system/SOURCE.txt` and `docs/SLIDE_DESIGN_NOTES.md` |
| AI tool(s) used by Nana | Not provided or independently established |
| Exact model/version | Not provided or independently established |
| Exact generation dates | Not established; the commit date is not treated as an AI-session date |
| Exact original prompts | Not available in the supplied repository |
| Complete original responses | Not available in the supplied repository |
| Attribution of original code to AI vs. student work | Cannot be determined from a Git author or commit message alone |

A separate [Nana historical record](ai-use/NANA_RECORD.md) gathers the available evidence and identifies the specific original records needed. No prompt has been invented to resemble what she might have asked, and no first-person declaration has been signed on her behalf.

## 4. English translations of selected prompts and responses

The following are English translations of selected student prompts and assistant replies. All original-language text has been removed from this English-only package at the student's request. These translations are not verbatim original transcripts and do not replace the original records required by the syllabus. Earlier versions remain in Git history.

### Exchange C1: Complete the existing repository

**English translation (edited for clarity):**

> Please review the existing repository against the instructor's requirements and complete the remaining work using this repository as the foundation. Does it already satisfy the assignment requirements? My goal is to earn full marks.

**Subsequent clarification:**

**English translation (edited for clarity):**

> If the repository already includes a presentation, please use the original slides and continue completing the remaining work from that version.

**English translation of the final conversational reply:** [AI_RESPONSE.md](ai-use/AI_RESPONSE.md).

**Material used:** focused PDF edits, economic model, explanatory/supporting documentation, verification/packaging helpers, and the updated project ZIP. The grade request was not treated as evidence that a score could be guaranteed.

### Exchange C2: Recording manuscript and walkthrough

**English translation (edited for clarity):**

> Please prepare a complete presentation script and a step-by-step walkthrough explaining what to show and how to demonstrate the project. Please also identify the changes you made to Nana's original work.

**English translation of the final conversational reply:** [RECORDING_RESPONSE.md](ai-use/RECORDING_RESPONSE.md).

**Material used in the current package:** `docs/RECORDING_SCRIPT_EN.md` and supporting English demo/slide notes. The Chinese working rehearsal files mentioned in the historical reply were removed later; their names in that reply describe the earlier exchange, not current file links.

### Exchange C3: Remove Chinese rehearsal material

**English translation (edited for clarity):**

> Please check whether the submission contains any Chinese-language presentation scripts. If it does, please remove them, as I am preparing the assignment for submission.

**English translation of the final conversational reply:** [CLEANUP_RESPONSE.md](ai-use/CLEANUP_RESPONSE.md).

**Material used:** removal of the Chinese/bilingual rehearsal guides; preservation of English narration and, at that stage, original-language AI disclosure records (subsequently translated for this package); refreshed ZIP and checksum. Core implementation and slide content did not change.

### Exchange C4: Prepare this appendix, including Nana's section

**English translation (edited for clarity):**

> Please prepare an appendix documenting prior AI use, including a section for Nana's use of AI.

**English translation of the final conversational reply:** [APPENDIX_RESPONSE.md](ai-use/APPENDIX_RESPONSE.md).

**Material used:** this appendix, Nana's evidence-based historical section, and the record index. Historical gaps remain disclosed rather than filled with reconstructed prompts.

These records provide English translations of selected requests and final conversational replies used for the documented revisions. They are not an export of every earlier advisory exchange, progress update, tool trace, or Nana's historical sessions. The complete generated files are available in the project, but generated files and a Git patch are not substitutes for missing original chat transcripts.

## 5. Verification performed during the assisted revision

The following are recorded checks performed in the assisted workflow, not claims that either student independently performed each check:

- On Python 3.12.15, the original **88 tests passed**. The existing test suite was rerun, not newly authored in this revision.
- `cfn-lint` passed for the unchanged SAM template.
- All three CLI scenarios reproduced the committed JSON, Markdown, HTML and delivery-preview files byte for byte, with expected exit codes 0, 1 and 2.
- The model calculation is reproducible and explicitly labels human timing, workload size and cloud runtime as assumptions. It does not claim measured cloud bills or measured labor savings.
- The original presentation was preserved except for the four documented pages; preservation checks and visual review were performed.
- No real AWS deployment, live account scan, actual SNS/email delivery or Canvas submission was performed by the assistant.

Evidence: `examples/submission-validation.json`, `examples/test-results-current.txt`, `examples/offline-benchmark.json`, `examples/value-model.json`, `examples/slides-preservation.json` and the branch history.

## 6. Student review and remaining historical records

Both students are responsible for understanding the submitted implementation and narration, checking references and calculations, identifying their actual contributions, and confirming that all AI use has been disclosed. This document does not state that those student confirmations have already occurred.

To complete the syllabus's historical-record requirement, add Nana's original tool/model labels, exact prompts and complete responses, plus any other earlier AI sessions used in submitted work. Preserve the original wording rather than writing plausible replacement prompts. Add the records to the index when available. If a record is unavailable, state that limitation honestly; do not describe the historical appendix as complete.

## 7. Record locations

- [Nana's original-project record and missing-record status](ai-use/NANA_RECORD.md)
- [Current implementation final response](ai-use/AI_RESPONSE.md)
- [Recording-guide final response](ai-use/RECORDING_RESPONSE.md)
- [Submission-cleanup final response](ai-use/CLEANUP_RESPONSE.md)
- [Appendix-preparation final response](ai-use/APPENDIX_RESPONSE.md)
- [Machine-readable record index](ai-use/RECORD_INDEX.json)
- [Original design-system provenance](slide-design-system/SOURCE.txt)
