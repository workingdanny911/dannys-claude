---
name: cai-init
description: "Use when setting up CAI for a project. Triggers: 'CAI setup', 'cai-init', 'context initialize', 'CAI 세팅', 'context 초기화'"
---

# cai-init — Initialize CAI

## Overview

Sets up the CAI infrastructure in a target project. Creates directory structure, copies rules/hooks/skills/agents, and triggers onboarding.

## When to Use

- First time setting up CAI in a project.
- Developer says "set up CAI" or "cai-init".
- Use `--new` flag for brand-new projects with no existing code.
- Use `--force` flag to overwrite existing files (skip protection disabled).

## Workflow

### Step 1: Detect project root

Confirm the current working directory is the project root. Look for signals: `.git/`, `package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, or similar. If uncertain, ask the developer.

### Step 2: Check existing context

Check if `context/` directory already exists.
- If it exists and `--force` is not set: warn the developer and ask whether to proceed (skip existing files) or abort.
- If it exists and `--force` is set: proceed, overwriting all files.

### Step 3: Create directory structure

Copy the directory scaffold from the plugin templates:

```
${CLAUDE_PLUGIN_ROOT}/templates/context/ → context/
```

This creates:
- `context/.gitkeep`
- `context/decisions/.gitkeep`
- `context/issues/.gitkeep`
- `context/conventions/.gitkeep`
- `context/specs/.gitkeep`
- `context/roadmap/planned/.gitkeep`
- `context/roadmap/exploring/.gitkeep`
- `context/roadmap/completed/.gitkeep`

### Step 4: Copy rules file

```
${CLAUDE_PLUGIN_ROOT}/templates/rules/cai.md → .claude/rules/cai.md
```

Create `.claude/rules/` directory if it does not exist. Do not overwrite if the file already exists (skip with notice), unless `--force`.

### Step 5: Copy hook script

```
${CLAUDE_PLUGIN_ROOT}/templates/tools/drift-warning.js → tools/drift-warning.js
```

Create `tools/` directory if it does not exist. Do not overwrite if the file already exists (skip with notice), unless `--force`.

### Step 6: Copy AGENTS.md

```
${CLAUDE_PLUGIN_ROOT}/templates/AGENTS.md → AGENTS.md
```

Do not overwrite if the file already exists (skip with notice), unless `--force`.

### Step 7: Copy daily-use skills

Copy these 7 skills from the plugin to the target project:

```
${CLAUDE_PLUGIN_ROOT}/skills/cai-onboard/SKILL.md    → .claude/skills/cai-onboard/SKILL.md
${CLAUDE_PLUGIN_ROOT}/skills/cai-add-spec/SKILL.md   → .claude/skills/cai-add-spec/SKILL.md
${CLAUDE_PLUGIN_ROOT}/skills/cai-add-decision/SKILL.md → .claude/skills/cai-add-decision/SKILL.md
${CLAUDE_PLUGIN_ROOT}/skills/cai-add-agent/SKILL.md  → .claude/skills/cai-add-agent/SKILL.md
${CLAUDE_PLUGIN_ROOT}/skills/cai-add-roadmap/SKILL.md → .claude/skills/cai-add-roadmap/SKILL.md
${CLAUDE_PLUGIN_ROOT}/skills/cai-capture-lesson/SKILL.md → .claude/skills/cai-capture-lesson/SKILL.md
${CLAUDE_PLUGIN_ROOT}/skills/cai-drift-check/SKILL.md → .claude/skills/cai-drift-check/SKILL.md
```

Create `.claude/skills/` directories as needed. Skip existing files with notice unless `--force`.

### Step 8: Copy agents

Copy all 10 agents from the plugin to the target project:

```
${CLAUDE_PLUGIN_ROOT}/agents/structure-scanner.md      → .claude/agents/structure-scanner.md
${CLAUDE_PLUGIN_ROOT}/agents/module-analyst.md         → .claude/agents/module-analyst.md
${CLAUDE_PLUGIN_ROOT}/agents/draft-generator.md        → .claude/agents/draft-generator.md
${CLAUDE_PLUGIN_ROOT}/agents/relationship-mapper.md    → .claude/agents/relationship-mapper.md
${CLAUDE_PLUGIN_ROOT}/agents/convention-extractor.md   → .claude/agents/convention-extractor.md
${CLAUDE_PLUGIN_ROOT}/agents/constitution-assembler.md → .claude/agents/constitution-assembler.md
${CLAUDE_PLUGIN_ROOT}/agents/verification-agent.md     → .claude/agents/verification-agent.md
${CLAUDE_PLUGIN_ROOT}/agents/context-gardener.md       → .claude/agents/context-gardener.md
${CLAUDE_PLUGIN_ROOT}/agents/code-reviewer.md          → .claude/agents/code-reviewer.md
${CLAUDE_PLUGIN_ROOT}/agents/spec-writer.md            → .claude/agents/spec-writer.md
```

Create `.claude/agents/` directory if needed. Skip existing files with notice unless `--force`.

### Step 9: Propose settings.json hook registration

Read `.claude/settings.json` if it exists. Propose adding the drift-warning hook:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "command": "node tools/drift-warning.js \"$TOOL_INPUT\""
      }
    ]
  }
}
```

If `.claude/settings.json` already exists with other hooks, propose **merging** the new hook into the existing `PreToolUse` array. Show the proposed change and ask for approval. Do **not** modify settings.json without explicit approval.

### Step 10: Propose CLAUDE.md additions

Do **not** modify CLAUDE.md directly. Propose adding a `Context Infrastructure` section:

```markdown
## Context Infrastructure
This project uses CAI.
- Knowledge base: context/
- Rules: .claude/rules/cai.md
- Drift detection: tools/drift-warning.js
```

Show the proposed block and ask the developer to add it. If CLAUDE.md does not exist, propose creating one with this content plus a basic project section.

### Step 11: Auto-trigger cai-onboard

After setup is complete:
- If `--new` flag was provided: skip onboarding, inform the developer that context will be built as the project grows.
- Otherwise: automatically invoke the `cai-onboard` skill to analyze the existing codebase and generate initial context documents.

## Output

Files created/copied as listed above. Summary of what was created, what was skipped, and any pending proposals (settings.json, CLAUDE.md).

## Error Handling

- If a copy fails, report the error and continue with remaining files.
- Never leave a half-initialized state — if critical files (rules, context directory) fail, abort and clean up.
- If `${CLAUDE_PLUGIN_ROOT}` cannot be resolved, report the error clearly.
