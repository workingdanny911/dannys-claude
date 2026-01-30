---
name: update-version
description: "Apply latest sprint-init template changes to existing sprints. Updates only rules/guidelines sections while preserving user data (Features, Tasks, tables). Triggers: 'update sprint', 'upgrade sprint', 'update template', 'update sprint version'"
---

# Sprint Update Version Skill

Apply template updates to existing sprints when sprint-init templates are updated.

---

## Core Principles

1. **Data preservation first** - Feature, Task, and table data must never be lost
2. **Update rules/guidelines only** - Replace only workflow, rules, and instruction sections
3. **Preview required** - User approval after reviewing diff before changes
4. **Backup required** - Always create backup for rollback capability

---

## Workflow

### Phase 1: Detect Sprint and Check Version

1. **Check sprint files**
   - Verify BACKLOG.md, HANDOFF.md, INSTRUCTION.md exist
   - If not found: "Sprint not detected. Please specify the path."

2. **Check version file**
   - Read `.sprint-version` file
   - If not found: "No version info. Proceeding as first-time update."

3. **Check latest version**
   - Read version from `## Version` section in `../init/SKILL.md`

4. **Report version comparison**
   ```
   Current sprint version: 1.0.0
   Latest template version: 1.1.0

   Update required. Would you like to preview the changes?
   ```

---

### Phase 2: Diff Preview

Distinguish between **rules sections** and **data sections** in each file.

#### Section Classification Rules

| File | Rules Sections | Data Sections (Preserve) |
|------|----------------|--------------------------|
| BACKLOG.md | Legend, Numbering, Status & Transitions, Archiving | `## Features` content, `## Done` content |
| HANDOFF.md | Before You Start, WIP Limit, Quick Actions | Data rows in each table |
| INSTRUCTION.md | Entire file | Custom sections (## headers not in template) |

#### Diff Display Format

```markdown
## Update Preview

### INSTRUCTION.md
**Changes:**
- Session Start procedure updated
- Context Compaction Recovery section modified

### BACKLOG.md
**Changes:**
- Status & Transitions diagram modified

**Preserved (user data):**
- Features: N items
- Done: N completion records

### HANDOFF.md
**Changes:**
- Quick Actions procedure updated

**Preserved (user data):**
- In Progress: N rows
- In Review: N rows
- Recently Done: N rows
- Dependencies: N rows
- Blockers: N rows
```

---

### Phase 3: User Confirmation

After showing changes, confirm:

```
Proceed with the above updates?
- Yes: Proceed
- No: Cancel
- Specific files only: Enter filename (e.g., INSTRUCTION.md only)
```

---

### Phase 4: Backup and Execute Update

#### 4.1 Create Backup

```
refs/archive/_backup-v{current-version}/
├── BACKLOG.md
├── HANDOFF.md
├── INSTRUCTION.md
└── .sprint-version (if exists)
```

> If no version file: `_backup-legacy/`

#### 4.2 Merge Files

**BACKLOG.md merge:**
```
1. Extract data:
   - From "## Features" line to just before "## Done" → features_data
   - From "## Done" line to just before "## Archiving" → done_data
2. From new template:
   - From start to just before "## Features" → header (rules)
   - From "## Archiving" line to end → footer (rules)
3. Merge: header + "## Features\n" + features_data + "## Done\n" + done_data + footer
```

**HANDOFF.md merge:**
```
1. For each table section (In Progress, In Review, Recently Done, Dependencies, Blockers):
   - Find table header (| ... | ... |)
   - Skip separator (|---|---|)
   - Extract non-empty data rows below
2. Insert data rows into corresponding table in new template (just below separator)
```

**INSTRUCTION.md merge:**
```
1. Detect custom sections in current file:
   - Find "## " headers not in template
   - Extract those section contents
2. Replace with new template
3. If custom sections exist, append at end:
   ---

   ## Custom Sections (Preserved)

   [custom section content]
```

#### 4.3 Update Version File

```
{new version}
```

---

### Phase 5: Completion Report

```
Sprint update complete!

Version: {previous} → {new version}
Backup: refs/archive/_backup-YYYYMMDD/

Updated files:
✓ INSTRUCTION.md
✓ BACKLOG.md (N Feature data preserved)
✓ HANDOFF.md (N table rows preserved)

Restore from backup if issues occur.
```

---

## Error Handling

| Situation | Response |
|-----------|----------|
| Sprint detection failed | "Cannot find sprint files (BACKLOG.md, HANDOFF.md)." |
| No version file | "First-time update. Updating from legacy → latest version." |
| Already latest version | "Already on latest version (v{version}). Force update?" |
| File structure issue | "Cannot find '## Features' section in BACKLOG.md. Manual check required." |

---

## Dependencies

- `/sprint:init` - Template source (includes version info)

**Path resolution (relative to this SKILL.md file):**
1. This file's directory: `update-version/`
2. Move to parent: `skills/`
3. Enter init: `skills/init/`

**Reference files:**
- Version info: `../init/SKILL.md` `## Version` section
- Template files: `../init/assets/templates/*.md`

---

## Related Skills

- `/sprint:init` - Sprint initialization (template source)
- `/sprint:add-backlog` - Add backlog items
- `/sprint:plan-backlog` - Design backlog items in detail
