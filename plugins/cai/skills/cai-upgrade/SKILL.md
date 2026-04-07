---
name: cai-upgrade
description: "Use when upgrading CAI to the latest version. Triggers: 'cai-upgrade', 'context upgrade', 'context 업그레이드', 'update CAI'"
---

# cai-upgrade — Upgrade CAI

## Overview

Upgrades the CAI infrastructure in a project to the latest plugin version. Performs section-based merge to preserve project-specific customizations while updating tool-managed content.

## When to Use

- A new version of the cai plugin is available.
- Developer says "upgrade CAI" or "cai-upgrade".
- After installing a plugin update.

## Workflow

### Step 1: Detect current version

Read `.claude/rules/cai.md` in the target project. This is the primary file for version detection. Also check if the project has the expected directory structure (`context/`, `tools/drift-warning.js`, `.claude/agents/`, `.claude/skills/`).

Read `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` to get the plugin version.

If the project does not appear to have CAI initialized, inform the developer and suggest running `cai-init` instead.

### Step 2: Fetch latest from plugin

Read the latest templates from the plugin source:
- `${CLAUDE_PLUGIN_ROOT}/templates/rules/cai.md` (latest rules)
- `${CLAUDE_PLUGIN_ROOT}/templates/tools/drift-warning.js` (latest hook)
- `${CLAUDE_PLUGIN_ROOT}/templates/AGENTS.md` (latest AGENTS.md)
- `${CLAUDE_PLUGIN_ROOT}/skills/` (latest skills)
- `${CLAUDE_PLUGIN_ROOT}/agents/` (latest agents)
- `${CLAUDE_PLUGIN_ROOT}/CHANGELOG.md` (version history)

Read `CHANGELOG.md` and extract all entries **after** the project's current version. These will be shown to the developer in Step 6.

### Step 3: Create backup

Create a timestamped backup of all files that will be modified:

```
.claude/backups/cai-{YYYY-MM-DD-HHmmss}/
  rules/cai.md
  tools/drift-warning.js
  AGENTS.md
  skills/   (all cai-* skill files)
  agents/   (all agent files)
```

Inform the developer of the backup location.

### Step 4: Section-based merge for rules file

Parse `.claude/rules/cai.md` using section markers:

1. **Extract PROJECT-SPECIFIC content**: Find everything between `<!-- PROJECT-SPECIFIC:START -->` and `<!-- PROJECT-SPECIFIC:END -->`. Save this content.

2. **Replace TOOL-MANAGED content**: Take the new `<!-- TOOL-MANAGED:START -->` ... `<!-- TOOL-MANAGED:END -->` block from the plugin template.

3. **Reattach PROJECT-SPECIFIC content**: Append the preserved PROJECT-SPECIFIC block after the new TOOL-MANAGED block.

4. If the project file has content outside both markers (custom sections added by the developer), preserve that content at the end of the file.

### Step 5: Update hook and AGENTS.md

- Replace `tools/drift-warning.js` with the latest version from the plugin.
- Replace `AGENTS.md` with the latest version from the plugin.

These files are fully tool-managed and contain no project-specific content.

### Step 6: Show changelog and diff preview

First, present the CHANGELOG entries since the project's current version:

```
📋 Changelog (v0.2.0 → v0.3.0):

### Improved — Confidence Pipeline
- verification-agent now recommends confidence promotion based on verification results ...
...

### Upgrade Notes
- To benefit from confidence promotion, re-verify existing specs via cai-onboard --incremental
```

Then present a clear diff of all changes:

1. **Rules file**: Show what changed in the TOOL-MANAGED section. Confirm PROJECT-SPECIFIC section is preserved (show it).
2. **Hook**: Show if the hook script changed.
3. **AGENTS.md**: Show if AGENTS.md changed.
4. **Skills**: List new, updated, and unchanged skills.
5. **Agents**: List new, updated, and unchanged agents.

Format the diff so the developer can review each change.

### Step 7: Developer approval

Ask the developer to approve the upgrade. Options:
- **Apply all** — apply every change.
- **Selective** — let the developer pick which files to update.
- **Abort** — cancel the upgrade (backup is kept).

Do not apply any changes without explicit approval.

### Step 8: Apply changes and update skills/agents

After approval:

1. Write the merged rules file.
2. Write the updated hook and AGENTS.md.
3. For each skill in the plugin's `skills/` directory:
   - If the skill exists in the project: overwrite with the latest version.
   - If the skill is new: ask "Add new skill `{name}`?"
4. For each agent in the plugin's `agents/` directory:
   - If the agent exists in the project: overwrite with the latest version.
   - If the agent is new: ask "Add new agent `{name}`?"
5. Never delete skills or agents that exist in the project but not in the plugin (these are custom project additions).

### Step 9: Post-upgrade summary

Report:
- Plugin version applied.
- Files updated.
- PROJECT-SPECIFIC content preserved.
- New skills/agents added (if any).
- Backup location for rollback.
- Upgrade Notes from CHANGELOG (if any) — especially post-upgrade actions like `cai-onboard --incremental`.

## Output

Updated files in the target project. Backup in `.claude/backups/`.

## Error Handling

- If section markers are missing in the existing rules file, treat the entire file as PROJECT-SPECIFIC and prepend the new TOOL-MANAGED section. Warn the developer.
- If backup creation fails, abort the upgrade.
- If any file write fails after approval, report the error and point to the backup for manual recovery.
