---
name: cai-drift-check
description: "Use when checking spec freshness across the project. Triggers: 'cai-drift-check', 'drift 검사', 'stale 체크', 'drift check', '드리프트 검사', '문서 점검', 'spec 점검'"
---
# CAI Drift Check

## Overview

Scans all CAI documents, judges staleness using a 3-level system, detects undocumented high-churn areas, and generates a report with actionable proposals. Does NOT auto-modify any documents.

## When to Use

- Periodic health check of CAI (AI may suggest this proactively)
- Action routing: "stale spec 업데이트 필요" triggers this skill
- User explicitly requests a drift/freshness check
- Before major refactoring to understand which docs need attention

## Workflow

### 1. Parse All Context Documents

Read all `context/**/*.md` files and parse their YAML frontmatter. Extract:
- `type` — document type
- `last_synced` — last sync date
- `covers` — explicit file coverage (if present)
- `tags` — for cross-referencing
- Spec-specific: `level`, `confidence`, `components`, `depends_on`

Also read `Source roots` from `.claude/rules/cai.md` for convention-based mapping.

### 2. Stale Judgment (3 Levels)

For each document, apply the following judgment logic:

```
Document has `covers` field?
├── YES → Check covers paths with: git log --since="{last_synced}" -- {covers paths}
│         Files changed? → 🔴 STALE (confirmed: covered files changed since last sync)
│         No changes?   → 🟢 FRESH
│
└── NO → Attempt convention-based mapping
    ├── Spec with path-based mapping possible?
    │   (e.g., context/specs/auth/_overview.md → {source_root}/auth/**)
    │   Check mapped paths with: git log --since="{last_synced}" -- {mapped paths}
    │   Files changed? → 🟡 POSSIBLY STALE (inferred mapping, not explicit)
    │   No changes?   → 🟢 FRESH
    │
    └── No path mapping possible (decisions, conventions, etc.)
        last_synced older than 30 days? → 🟢 REVIEW SUGGESTED (time-based)
        Otherwise → 🟢 FRESH
```

### 3. Detect Spec-Less High-Churn Areas

Identify source files that are frequently modified but have no covering spec:

1. Get files with high commit frequency: `git log --since="30 days ago" --name-only --pretty=format:""`
2. Count modifications per file within source roots
3. Filter out files already covered by a spec (via `covers` or convention-based mapping)
4. Flag files with 5+ modifications and no spec coverage

### 4. Generate Report

> **CRITICAL**: This step produces a report ONLY. Do NOT automatically modify any documents.

```
Drift Check Report ({today's date})

🔴 STALE (code changed, spec outdated):
  {spec_path}
    covers: {covers value}
    changed files: {file} (+{added} -{removed})
    last_synced: {date} ({N} days ago)

🟡 POSSIBLY STALE (convention-based match):
  {spec_path}
    inferred: {mapped path pattern}
    changed files: {file} (+{added} -{removed})
    last_synced: {date} ({N} days ago)

🟢 REVIEW SUGGESTED (time-based):
  {doc_path}
    last_synced: {date} ({N} days ago)

⚠ Undocumented High-Churn Areas:
  {file_path} — {N} modifications in last 30 days, no covering spec
  → Spec creation recommended

Summary:
  🔴 {count} stale | 🟡 {count} possibly stale | 🟢 {count} review suggested
  ⚠ {count} undocumented high-churn areas
  ✓ {count} fresh documents
```

### 5. Propose Actions

For each non-fresh item, propose a specific action:

| Status | Proposed Action |
|--------|----------------|
| 🔴 STALE | "Update spec via cai-add-spec? Changes: {summary}" |
| 🟡 POSSIBLY STALE | "Review and update spec via cai-add-spec? Inferred changes: {summary}" |
| 🟢 REVIEW SUGGESTED | "Review document. Still accurate?" |
| ⚠ Undocumented | "Create spec via cai-add-spec for {area}?" |

Present each proposal for user approval. Only execute approved actions by invoking the appropriate skill (cai-add-spec for spec updates/creation).

## Agent Invocations

This skill does not directly invoke agents. It performs analysis using git commands and file parsing, then routes approved actions to other skills:

- Spec updates/creation: routes to cai-add-spec skill
- The cai-add-spec skill handles agent invocations (spec-writer, verification-agent)

## Output

| Artifact | Path | Format |
|----------|------|--------|
| Drift report | (displayed to user, not persisted) | Formatted text with emoji indicators |
| Updated specs (if approved) | Via cai-add-spec | Markdown with YAML frontmatter |

## Error Handling

| Error | Action |
|-------|--------|
| No context documents found | Inform user that CAI is empty. Suggest running cai-onboard. |
| Git not available or not a git repo | Fall back to time-based judgment only (all non-covers documents get REVIEW SUGGESTED if old enough) |
| Source roots not configured | Warn user and skip convention-based mapping. Only explicit `covers` matching works. |
| Frontmatter parse error on a document | Report the malformed file in the report and skip it |
| No stale documents found | Report "All documents are fresh" with summary counts |
