---
name: analyze
description: >
  A skill that deeply analyzes famous open-source codebases and generates a technical biography-style book.
  Use when studying the architecture/design philosophy of projects like Doom, Bitcoin, Redis, libuv, PostgreSQL.
  Trigger on requests such as "analyze ~~", "create a walkthrough for ~~", "write ~~ as an architecture book",
  "codebase analysis", "project walkthrough", "x-ray", "codebase x-ray".
  Analysis results are stored in a reusable artifact store for future use without re-analysis.
---

# Codebase X-Ray

A system that produces a **technical biography**-style book about the architecture/design of famous open-source projects.

Goal: "What problem did this system solve, with what philosophy, and what trade-offs did it accept?"
Sub-goal: "What software engineering principles and patterns are at work in this code?"

This book does not merely explain code — it **teaches software engineering through real code**. Even in C code from 1993, GoF design patterns, SOLID principles, and architecture patterns are alive and well. After reading this book, the reader should be able to recognize "ah, so that's that pattern" in other codebases too.

---

## Core Principles

1. **Analysis and writing are completely separated.** Analysis extracts facts; writing selects facts. Doing both at once lets narrative logic contaminate analytical completeness.

2. **Hallucination is absolutely forbidden.** Every claim carries a provenance tag. Analysis agents self-verify, and the Verifier performs a structural audit.

3. **The Artifact Store is permanent.** Once a project is analyzed, it is reused without re-analysis. The Writing Pipeline can be re-run at any time.

4. **Actively seek discrepancies between official narrative and code.** The points where design intent diverges from actual implementation make the most interesting chapters.

5. **Output language follows the user's request language.** If the user requests in Korean, output in Korean; English for English; Japanese for Japanese. Detected at initialization, recorded as `output_language`, and passed in the meta block of every sub-agent prompt. Code snippets, file paths, and technical terms (struct names, etc.) always remain in their original language.

6. **The reader is a developer studying the code.** They read on their phone during a commute. It must be easy and engaging. Code snippets require `output_language` comments. Use `> **📌 ...**: ...` inline callout boxes for terminology, analogies, modern-tech comparisons, and anecdotes. Short paragraphs, many subheadings.

7. **Uncover software engineering patterns and principles from the code.** Identify design patterns (GoF, etc.), architecture patterns, OO principles (SOLID, etc.), and system design principles in the code. Connect them using `> **📐 Design Pattern**: ...` callout boxes. Patterns operate regardless of language. The goal is to enable readers to "recognize this pattern in other codebases too."

---

## Provenance Tag Rules

Attach an inline tag to every claim. The Verifier rejects any claim without a tag.

```
[provenance:code_derived file:src/ae.c:L42]      ← directly verified from code
[provenance:author_stated source:"URL or source"] ← author/official documentation
[provenance:synthesized]                          ← our interpretation/inference
```

`code_derived` must include a file path and line number.

---

## Directory Structure

The skill itself:
```
codebase-x-ray/skills/analyze/
├── SKILL.md               ← this file (orchestrator)
└── references/
    ├── phase0-research.md     ← Web research + Semantic anchor extraction
    ├── phase1-2-survey.md     ← Directory survey + Boundary synthesis
    ├── phase3-deep-dive.md    ← Module deep dive + Self-verify
    ├── phase4-6-writing.md    ← Chapter design + Writing + Assembly
    ├── verifier.md            ← Structural audit
    ├── chapter-template.md    ← Chapter structure guide
    └── artifact-format.md     ← Artifact prose format + examples
```

Project directory created at runtime:
```
{project_root}/
├── manifest.md            ← Progress state + project info (key to restarts)
├── source/                ← cloned repository
├── references/            ← downloaded materials from web research (papers, slides, images, etc.)
│   └── sources.md         ← URL list + downloaded file mapping
├── checkpoints/
│   ├── phase0a.md
│   ├── phase0b.md
│   ├── phase1/{dirname}.md
│   ├── phase2.md
│   ├── phase4.md
│   ├── verify_phase3_pass1_{batch_num}.md
│   ├── verify_phase3_pass2.md
│   ├── verify_phase6_pass1_{batch_num}.md
│   └── verify_phase6_pass2.md
├── artifacts/
│   └── modules/{module}.md
└── output/
    ├── 00-prologue.md       ← independent file per chapter
    ├── 01-{chapter}.md
    ├── 02-{chapter}.md
    ├── ...
    ├── build.sh             ← chapter assembly + PDF conversion script
    └── book.md              ← output of build.sh
```

---

## Full Pipeline Overview

```
ANALYSIS PIPELINE
  Phase 0a → Web Research
  Phase 0b → Semantic Anchor Extraction
  Phase 1  → Directory Survey (parallel Agents)
  Phase 2  → Boundary Synthesis
  Phase 3  → Module Deep Dive (parallel Agents) + Self-Verify
  Verifier Pass 1 → Per-artifact audit (parallel batches)
  Verifier Pass 2 → Cross-module audit (single Agent)
        ↓
  ARTIFACT STORE (reusable)
        ↓
WRITING PIPELINE
  Phase 4  → Chapter Design
  Phase 5  → Per-Chapter Writing (parallel Agents)
  Phase 6  → Cross-chapter Review → Final Book
  Verifier Pass 1 → Per-chapter audit (parallel batches)
  Verifier Pass 2 → Cross-chapter audit (single Agent)
```

---

## Execution Flow

This section provides step-by-step instructions for the main Claude Code session to follow. Execute each step in order.

### Start: Initialization

1. The user provides a **project_name** (e.g., redis, doom, sqlite). Extract it from their request.

2. Ask the user for a **project root path** — a single directory where everything will live.
   Example: `~/research/redis`, `/tmp/doom-study`

3. **Detect output_language**: Detect the language of the user's request. "DOOM 분석해줘" → Korean, "analyze DOOM" → English. Record in manifest.md and pass in the meta block of every sub-agent prompt.

4. Check if `{project_root}/manifest.md` exists:
   - **If yes**: Read it and follow the restart protocol (see "Restart Protocol" section below)
   - **If no**: Continue to step 5.

5. Create the project directory structure:
   ```
   {project_root}/
   ├── source/              ← repo will be cloned here
   ├── references/          ← downloaded materials from web research
   ├── checkpoints/
   │   └── phase1/
   ├── artifacts/
   │   └── modules/
   └── output/
   ```

6. **Clone the repository** into `{project_root}/source/`:
   - If the user provided a repo URL or local path, use that.
   - If only a project name was given, infer the GitHub URL for well-known projects:
     - redis → `https://github.com/redis/redis`
     - doom → `https://github.com/id-Software/DOOM`
     - sqlite → `https://github.com/sqlite/sqlite`
     - libuv → `https://github.com/libuv/libuv`
     - bitcoin → `https://github.com/bitcoin/bitcoin`
     - For others, ask the user.
   - Confirm the URL with the user before cloning.

7. Create manifest.md:

```markdown
# Codebase X-Ray: {project_name}
- project: {project_name}
- language: {output_language}
- repo: {project_root}/source
- project_root: {project_root}
- started: {current date/time}

## Progress
```

**Path convention**: Throughout the pipeline, paths are relative to `{project_root}`:
- `source/` → the cloned repo (used as `repo` in all sub-agent prompts)
- `checkpoints/` → phase checkpoint files
- `artifacts/modules/` → module deep dive artifacts
- `output/` → chapter files, build.sh, book.md

---

### Phase 0a: Web Research

1. Read `references/phase0-research.md` from this skill.
2. Compose the sub-agent prompt from the Phase 0a section content.
3. Dispatch the Agent:
   - prompt: Phase 0a instructions + project info + meta block
   - **Instruct the sub-agent to Write results directly to `{project_root}/checkpoints/phase0a.md`**.
   - The sub-agent returns only a completion summary to the main session.
4. Add to manifest.md: `- Phase 0a: complete`

---

### Phase 0b: Semantic Anchor Extraction

1. Read the Phase 0b section from `references/phase0-research.md`.
2. Read `checkpoints/phase0a.md`.
3. Dispatch the Agent:
   - prompt: Phase 0b instructions + full Phase 0a results + repo path + meta block
   - This agent needs to read repo files directly, so specify the repo path.
   - **Instruct the sub-agent to Write results directly to `checkpoints/phase0b.md`**.
4. Update manifest.md.

---

### Phase 1: Directory Survey (Parallel)

1. Check the repo's top-level directory listing (`ls` or Glob).
   - **Exclude**: `.git`, `.github`, `.vscode`, `node_modules`, `vendor`, `build`, `dist`, and other non-source directories
   - **Include**: Source code, tests, documentation, build configuration, and other directories needed to understand the project's structure
   - Top-level files (Makefile, README, etc.) were already covered in Phase 0b, so no separate agent is needed
2. Read the Phase 1 section from `references/phase1-2-survey.md`.
3. Read the worldview paragraph and Phase 1-3 caveats from `checkpoints/phase0b.md`.
4. **Dispatch one Agent per directory in parallel:**
   - Call all Agents simultaneously in a single response.
   - Each agent prompt: Phase 1 instructions + worldview + caveats + assigned directory path + meta block
   - Each agent reads the files in its assigned directory directly.
   - **Instruct each sub-agent to Write directly to `checkpoints/phase1/{dirname}.md`**.
5. Record the list of completed directories in manifest.md.

---

### Phase 2: Boundary Synthesis

1. Read all .md files under `checkpoints/phase1/`.
2. Read the Phase 2 section from `references/phase1-2-survey.md`.
3. Read `checkpoints/phase0b.md`.
4. Dispatch the Agent:
   - prompt: Phase 2 instructions + Phase 0b worldview/discrepancies + full Phase 1 report + meta block
   - **Instruct the sub-agent to Write directly to `checkpoints/phase2.md`**.
5. Update manifest.md.

---

### Phase 3 Preparation: Module Identification

**The main session performs this step directly. No sub-agent needed.**

1. Read `checkpoints/phase2.md`.
2. Identify the semantic module list from the document — module name, included files, reason for existence.
3. Record the module list in manifest.md:
   ```
   - Modules: [module1], [module2], [module3], ...
   ```

---

### Phase 3: Module Deep Dive (Parallel)

1. Read `references/phase3-deep-dive.md` and `references/artifact-format.md`.
2. Read `checkpoints/phase0a.md` (web research — author statements/design decisions).
3. Read the worldview + official narrative vs. code discrepancies from `checkpoints/phase0b.md`.
4. **Dispatch one Agent per module in parallel:**
   - Each agent prompt: Phase 3 instructions + artifact format + worldview + discrepancy info + **relevant author statements from Phase 0a** + the module's Phase 2 info (name, file list, interfaces) + repo path + meta block
   - Each agent reads repo files directly, performs analysis, then self-verifies.
   - **Instruct each sub-agent to Write directly to `artifacts/modules/{module_safe_name}.md`**.
   - module_safe_name: lowercase, spaces replaced with underscores
5. Record the list of completed modules in manifest.md.

---

### Verifier: Phase 3 Structural Audit

1. Read `references/verifier.md`.

2. **Pass 1 — Per-Artifact Audit (parallel batches):**
   - Divide the artifact list into batches of 3–4 artifacts each: `ceil(total_artifacts / 4)` batches.
   - **Dispatch one Agent per batch in parallel:**
     - Each agent prompt: Pass 1 instructions (items 1–5) from verifier.md + assigned artifact file paths + repo path + specify "Phase 3 Pass 1"
     - **Provide paths so the sub-agent can Read artifact files directly.**
     - Instruct each sub-agent to Write results directly to `checkpoints/verify_phase3_pass1_{batch_num}.md`.
   - Read all Pass 1 results and collect per-artifact verdicts.
   - **HARD_FAIL artifacts**: Re-run Phase 3 only for the flagged modules, then re-run Pass 1 only for those artifacts.
   - Repeat until no HARD_FAIL remains.
   - Update manifest.md: `- Verify Phase 3 Pass 1: complete`

3. **Pass 2 — Cross-Module Audit (single agent):**
   - Dispatch one Agent:
     - prompt: Pass 2 instructions (item 6) from verifier.md + all artifact file paths + repo path + specify "Phase 3 Pass 2"
     - **Provide paths so the sub-agent can Read artifact files directly.**
     - Instruct the sub-agent to Write results directly to `checkpoints/verify_phase3_pass2.md`.
   - Check results:
     - **PASS** or **WARN**: Proceed to next phase.
     - **HARD_FAIL**: Re-run Phase 3 for the flagged modules, then re-run from Pass 1.
   - Update manifest.md: `- Verify Phase 3 Pass 2: complete`

---

### Phase 4: Chapter Design

1. Read the Phase 4 section from `references/phase4-6-writing.md`.
2. Read `checkpoints/phase0b.md`.
3. Dispatch the Agent:
   - prompt: Phase 4 instructions + worldview + artifact file path list + meta block
   - **Provide paths so the sub-agent can Read artifact files directly**.
   - Instruct the sub-agent to Write results directly to `checkpoints/phase4.md`.
4. Update manifest.md.

---

### Phase 5 Preparation: Chapter List Extraction

**The main session performs this step directly.**

1. Read `checkpoints/phase4.md`.
2. Identify the chapter list, order, and which artifacts each chapter will use.
3. Record in manifest.md:
   ```
   - Chapters: [chapter1 title], [chapter2 title], ...
   ```

---

### Phase 5: Per-Chapter Writing (Parallel)

1. Read the Phase 5 section from `references/phase4-6-writing.md` and `references/chapter-template.md`.
2. Read `checkpoints/phase0b.md`.
3. Read `checkpoints/phase4.md` (chapter plan + order).
4. **Dispatch one Agent per chapter in parallel:**
   - Each agent prompt: Phase 5 instructions + chapter template + worldview + the relevant chapter plan (excerpted from phase4.md) + full chapter order (for preceding/following context) + artifact file paths for the chapter + meta block
   - **Instruct each sub-agent to Read artifacts directly and Write results to `output/{NN}-{chapter_safe_name}.md`**.
   - NN is the chapter sequence number determined in Phase 4 (00, 01, 02, ...)
5. Record the list of completed chapters in manifest.md.

---

### Phase 6: Cross-chapter Review

Phase 6 is **editing**, not assembly. Physical assembly is handled by build.sh.

1. Read the Phase 6 section from `references/phase4-6-writing.md`.
2. Dispatch the Agent:
   - prompt: Phase 6 instructions + chapter file path list under `output/` + `checkpoints/phase4.md` path + worldview + meta block
   - **Instruct the sub-agent to Read chapter files directly and Edit the chapter files directly** if issues are found.
   - Return a review summary to the main session.
3. Generate build.sh (see below).
4. Execute build.sh to produce `output/book.md`.
5. Update manifest.md.

### build.sh Generation

The main session generates `output/build.sh` during Phase 6:

```bash
#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

# Assemble chapter files in numerical order
cat [0-9][0-9]-*.md > book.md
echo "book.md generated: $(wc -w < book.md) words"

# PDF conversion (if pandoc is available)
if command -v pandoc &>/dev/null; then
  pandoc book.md \
    -o book.pdf \
    --pdf-engine=xelatex \
    --toc \
    --toc-depth=3 \
    -V geometry:margin=1in \
    -V fontsize=11pt \
    -V mainfont="Noto Sans" \
    2>/dev/null && echo "book.pdf generated" \
    || echo "WARNING: PDF conversion failed. book.md is fine."
else
  echo "pandoc not found. Only book.md was generated."
fi
```

---

### Verifier: Phase 6 Final Audit

1. Read `references/verifier.md`.

2. **Pass 1 — Per-Chapter Audit (parallel batches):**
   - Divide the chapter list into batches of 3–4 chapters each: `ceil(total_chapters / 4)` batches.
   - **Dispatch one Agent per batch in parallel:**
     - Each agent prompt: Pass 1 instructions (items 1–4 base audit + item 9 new claims) from verifier.md + assigned chapter file paths + artifact file paths (for item 9 cross-reference) + repo path + specify "Phase 6 Pass 1"
     - Note: Item 5 (Self-Verify Summary) is Phase 3-specific and does not apply to chapters.
     - **Provide paths so the sub-agent can Read chapter files directly.**
     - Instruct each sub-agent to Write results directly to `checkpoints/verify_phase6_pass1_{batch_num}.md`.
   - Read all Pass 1 results and collect per-chapter verdicts.
   - **HARD_FAIL chapters**: Re-run Phase 5 only for flagged chapters, then re-run Pass 1 for those chapters.
   - Repeat until no HARD_FAIL remains.
   - Update manifest.md: `- Verify Phase 6 Pass 1: complete`

3. **Pass 2 — Cross-Chapter Audit (single agent):**
   - Dispatch one Agent:
     - prompt: Pass 2 instructions (items 6–8: cross-module consistency, terminology, cross-chapter references) from verifier.md + all chapter file paths + repo path + specify "Phase 6 Pass 2"
     - **Provide paths so the sub-agent can Read chapter files directly.**
     - Instruct the sub-agent to Write results directly to `checkpoints/verify_phase6_pass2.md`.
   - Check results:
     - **PASS** or **WARN**: Complete
     - **HARD_FAIL**: Re-run Phase 5 for flagged chapters → Re-run Phase 6 → Re-run Verifier
   - Update manifest.md: `- Verify Phase 6 Pass 2: complete`

4. Record "COMPLETE" in manifest.md.
5. Notify the user of completion and ask if PDF conversion is needed.

---

## Sub-agent Prompt Composition Guide

All sub-agent prompts are composed of 3 blocks:

### 1. Context Block

From Phase 0b onward, **always include the worldview paragraph first**. This is the shared foundational understanding for all agents.

```
## Context

### Worldview of This System
{worldview paragraph from checkpoints/phase0b.md}

### Prior Results
{previous results needed for this phase}

### Target
{directory/module/chapter this agent will analyze}

### Project Info
- project: {name}
- repo: {path}
```

### 2. Instructions Block

Include the relevant section from the references/ file **verbatim**. Do not summarize.

```
## Instructions

{full content of references/phase3-deep-dive.md}
```

### 3. Meta Block

```
## Meta

- Write all output in {output_language}. Keep code snippets and file paths in their original form.
- Include provenance tags in all output.
- Write results to {absolute path of output file}. Return only a completion summary to the main session.
- {If Phase 3} Perform self-verify after analysis is complete.
```

### Sub-agent Output Principle

**All sub-agents Write results directly to the designated file and return only a completion summary to the main session.**

Rationale: If a Phase 3 artifact is 5,000 words and a chapter is 3,000 words, returning all results to the main session wastes the context window unnecessarily. When sub-agents write files directly, the main session only needs to track "which files are complete."

Similarly, large inputs (full artifact lists, etc.) are not embedded directly in the prompt — instead, **provide file paths so the sub-agent can Read them directly**.

---

## Restart Protocol

manifest.md contains all progress state. When restarting after a session interruption:

1. Read `{project_root}/manifest.md`.
2. Check the Progress section for the last completed step.
3. Resume from the next step.

### Handling Partial Completion of Parallel Phases

Phases 1, 3, and 5 run multiple agents in parallel. If only some completed:

- **Phase 1**: Compare the file list in `checkpoints/phase1/` with the repo's directory list. Re-run only the missing ones.
- **Phase 3**: Compare the file list in `artifacts/modules/` with the module list in manifest.md. Re-run only the missing ones.
- **Phase 5**: Compare the `[0-9][0-9]-*.md` file list in `output/` with the chapter list in manifest.md. Re-run only the missing ones.
- **Verifier Pass 1** (Phase 3 or 6): Check which `verify_phase{N}_pass1_*.md` files exist in `checkpoints/`. Re-run only the missing batches.
- **Verifier Pass 2** (Phase 3 or 6): If `verify_phase{N}_pass2.md` does not exist but all Pass 1 files are present, run Pass 2 only.

### Re-running Only the Writing Pipeline

If the user wants to re-run only the Writing Pipeline (e.g., "I want to restructure chapters and rewrite"):
1. Delete `checkpoints/phase4.md`, `checkpoints/verify_phase6_pass1_*.md`, `checkpoints/verify_phase6_pass2.md`, and all files under `output/`.
2. Remove all entries after Phase 4 from the Progress section in manifest.md.
3. Re-running the skill will resume from Phase 4.

The Artifact Store (`artifacts/modules/`) is preserved, so no re-analysis is needed.

---

## Verification System: Self-Verify + Structural Audit

### Layer 1: Self-Verify

Each Phase 3 sub-agent performs this directly after completing analysis:
- Open and verify the file/line for every `code_derived` claim
- Fix tags or remove claims on discrepancy
- Include a verification summary at the end of the artifact

This is included in the sub-agent prompt's instructions block (`references/phase3-deep-dive.md`).

### Layer 2: Structural Audit (Two-Pass)

Performed by separate Verifier agents in two passes. Runs twice in the pipeline:
- **After Phase 3**: Targets all artifacts
- **After Phase 6**: Targets all chapters

Each run consists of:
- **Pass 1 (parallel batches)**: Per-artifact/chapter checks (items 1–5, item 9 for Phase 6). Batches of 3–4 artifacts/chapters run in parallel.
- **Pass 2 (single agent)**: Cross-cutting checks (item 6, items 7–8 for Phase 6). Runs only after all Pass 1 batches clear.

See `references/verifier.md` for detailed Verifier instructions.

Phases where the Verifier does not run:
- Phase 0a, 0b: Small output, low risk
- Phase 1: Intermediate data, implicitly verified in Phase 2
- Phase 2: Module boundary design, no provenance claims
- Phase 4: Chapter plan, no provenance claims
- Phase 5 individual chapters: Batch-checked by the Phase 6 Verifier

---

## Detailed Phase Instructions

Specific analysis/writing instructions for each phase are in the references/ files.
`references/` is located under the same directory as this skill's SKILL.md:

| Phase | File | Content |
|-------|------|---------|
| 0a, 0b | `references/phase0-research.md` | Web research, Semantic anchor extraction |
| 1, 2 | `references/phase1-2-survey.md` | Directory survey, Boundary synthesis |
| 3 | `references/phase3-deep-dive.md` | Module deep dive + Self-verify |
| 4, 5, 6 | `references/phase4-6-writing.md` | Chapter design, writing, review |
| Audit | `references/verifier.md` | Structural audit |
| Phase 5 | `references/chapter-template.md` | Chapter internal structure |
| Phase 3 | `references/artifact-format.md` | Artifact prose format |
