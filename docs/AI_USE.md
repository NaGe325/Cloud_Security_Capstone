# Generative AI assistance disclosure

Project: MedTech Security Baseline Checker. Authors: Charlotte Zhang and Nana Ge.

## Current revision, October 16, 2026

Tool: OpenAI Codex desktop. The session identifies the assistant as GPT-6 based. The exact deployed model build identifier is not exposed in this session and has not been invented. Students should retain the model label/version displayed in their application with their submission records.

AI assistance covered: reviewing the supplied course requirements and repository, making focused additions to the original 12-slide PDF and English notes, creating the explicit economic scenario and supporting documents, adding offline verification/packaging scripts and a CI workflow, running tests, and preparing a reviewable Git change. The five-control scanner logic and existing fixtures remain unchanged in this revision.

Exact task prompt:

> 好的 现在给我补全剩下的内容 都在这个repo的基础上（这个repo完成老师要求了吧 我要拿100分）

User clarification (exact):

> 原本有slides 是吗 那你就哦那个原版的 接着继续完成就可以的

The final deliverable follows this clarification. An earlier full rebuild is a discarded local intermediate, excluded from the final package. Eight original pages remain unchanged, and only four receive focused text edits.

The complete final conversational response for this revision is saved in [AI_RESPONSE.md](AI_RESPONSE.md). The complete generated artifacts are the files in this revision, including `scripts/update_original_slides.py` (exact slide changes), `docs/SPEAKER_NOTES.md` (complete speaking notes), `docs/`, the model script/output and the submitted deck. A Git patch preserves the complete source changes; it is not a substitute for earlier missing chat transcripts. Tool checks establish the stated offline behavior; they do not prove student understanding, production operation or a grade.

## Earlier assistance and record boundary

The original repository already includes a referenced AI conversation/design-system source and a generated presentation. This revision cannot reconstruct earlier exact prompts, complete responses or exact tool versions. The review conversation before this implementation also informed the gap list. Students must attach their original relevant records when submitting AI-assisted content under the syllabus policy. Do not describe this appendix as a complete history until those records have been reconciled.

Student review still required: confirm the report interpretations, estimates, sources, contribution descriptions and presentation claims. No claim is made that students have already performed that review. No full HIPAA compliance, live AWS deployment or guaranteed score is claimed.
