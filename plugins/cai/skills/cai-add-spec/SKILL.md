---
name: cai-add-spec
description: "Use when creating or updating a spec document. Triggers: 'cai-add-spec', 'spec 생성', 'spec 추가', 'spec 업데이트', 'add spec', 'update spec'"
---
# CAI Add Spec

## Overview

Creates a new spec or updates an existing spec document, then validates it against source code via the verification agent.

## When to Use

- AI proposes spec creation after modifying a previously undocumented area
- AI proposes spec update after code changes diverge from existing spec
- User explicitly requests a spec for a file, module, or component
- Action routing: "spec 생성/수정 필요" triggers this skill

## Workflow

### 1. Determine Target

Identify the target file(s) or module to document. Resolve to a spec path using convention-based mapping:
- Module-level: `context/specs/{module}/_overview.md`
- Component-level: `context/specs/{module}/{component}.md`

If the target, scope, or intent is ambiguous (e.g., the user said "add a spec for auth" but the auth area spans multiple modules, or it is unclear which behaviors should be documented), invoke the `cai:cai-interview` skill before proceeding. Pass:
- **Goal**: Clarify spec scope and intent.
- **What is already known**: The candidate target paths and any existing specs nearby.
- **Output target**: This skill's working memory — answers will shape Step 2 onward, not a file directly.
- **Seed questions**: Which files/modules to cover; module vs. component level; any behaviors to emphasize or exclude.

Skip the interview when the target is unambiguous.

### 2. Check Existing Spec

```
Does a spec already exist for this target?
├── YES → Update Mode (Step 3a)
└── NO  → Create Mode (Step 3b)
```

### 3a. Update Mode (Diff-Based)

1. Read the existing spec
2. Read the current source code for the covered area
3. Identify differences between spec and code
4. Invoke the `spec-writer` agent with update instructions:
   - Provide the existing spec content
   - Provide a summary of code changes since `last_synced`
   - Instruct to update only the changed sections
5. Proceed to Step 4

### 3b. Create Mode

1. Determine spec level (`module` or `component`)
2. Determine parent spec (if component-level, parent is the module's `_overview.md`)
3. Invoke the `spec-writer` agent with creation instructions:
   - Provide the source file paths to cover
   - Provide the target spec path
   - Instruct to generate a complete spec with frontmatter conforming to Interface Contract 0.1
4. Proceed to Step 4

### 4. Verification (MANDATORY)

Invoke the `verification-agent` to cross-validate the new or updated spec against source code.

```
Verification passed?
├── YES → Step 5
└── NO  → Present issues to user. Options:
    ├── Fix and re-verify
    └── Accept with noted discrepancies (mark confidence: draft)
```

### 5. Finalize

1. Write the spec file to its target path
2. Update `last_synced` to today's date (ISO 8601: YYYY-MM-DD)
3. Apply verification-agent's recommended confidence level:
   - All claims confirmed → `verified`
   - Mostly confirmed (≥80%), 0 incorrect → `reviewed`
   - Any incorrect claims → `draft`
4. If component-level, ensure parent module's `_overview.md` lists this component in `components` field
5. Report completion to user

## Agent Invocations

- Agent: `spec-writer` — Reads source code and writes spec documents
  - Create: `Task("Create a new {level}-level spec for {target_path}. Source files: {file_list}. Write to: {spec_path}. Follow frontmatter schema from interface contract.", agent="agents/spec-writer.md")`
  - Update: `Task("Update spec at {spec_path}. Current spec: {spec_content}. Changes since last sync: {change_summary}. Update only changed sections.", agent="agents/spec-writer.md")`

- Agent: `verification-agent` — Validates spec claims against source code
  - Invocation: `Task("Verify spec at {spec_path} against source code. Check all claims for accuracy.", agent="agents/verification-agent.md")`

## Output

| Artifact | Path | Format |
|----------|------|--------|
| New/updated spec | `context/specs/{module}/_overview.md` or `context/specs/{module}/{component}.md` | Markdown with YAML frontmatter (Interface Contract 0.1) |

**Frontmatter example (new spec):**
```yaml
---
type: spec
level: module
tags: [auth, security]
last_synced: 2026-04-06
covers: [src/auth/]
confidence: draft
components: [login, refresh, oauth]
exports: [authenticate, refreshToken]
depends_on: [context/specs/database/_overview.md]
---
```

## Error Handling

| Error | Action |
|-------|--------|
| spec-writer produces empty or malformed output | Retry once. If still fails, report error and ask user to provide manual input. |
| verification-agent finds critical inaccuracies | Do NOT finalize. Present the inaccuracy report. Ask user to choose: fix or accept as draft. |
| Target module cannot be determined | Ask user to specify the module/component path explicitly. |
| Parent overview does not exist (component spec) | Create a minimal parent `_overview.md` first, then proceed. |
