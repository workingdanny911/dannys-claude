---
name: init
description: Initialize a sprint with kanban-style structure for multi-agent collaboration. Use when user wants to start a sprint, set up sprint structure, or manage work with multiple agents. Triggers include "new sprint", "init sprint", "setup sprint", "start sprint", "스프린트 시작", "스프린트 초기화", "새 스프린트". Creates BACKLOG.md, HANDOFF.md, INSTRUCTION.md, and sets up active/, refs/designs/, refs/plans/ folders.
---

## Version

Current: **1.9.0**

> Update this version when templates change:
> - **Major** (2.0.0): Breaking changes to file structure
> - **Minor** (1.1.0): New sections, updated rules
> - **Patch** (1.0.1): Typo fixes, clarifications

# Sprint Initialization Skill

Initialize a sprint with kanban-style structure for multi-agent collaboration.

---

## Overview

This skill creates the **structure only** (empty backlog). Use `/sprint:add-backlog` to add work items.

**Generated structure:**
```
sprints/<sprint-name>/
├── BACKLOG.md          # Work items (Feature → Task → Sub-task)
├── HANDOFF.md          # Work Board (current status)
├── INSTRUCTION.md      # Agent guidelines
├── active/             # Feature-specific contexts (temporary)
└── refs/
    ├── designs/        # Feature design documents
    ├── plans/          # Task execution plans
    ├── decisions/      # Decisions (per-feature + _sprint.md for sprint-wide)
    ├── lessons/        # Lessons (per-feature + _sprint.md for sprint-wide)
    └── archive/        # Completed features (moved from BACKLOG.md)
```

---

## Workflow

### Phase 1: Gather Information

Ask the user:

1. **Sprint name** - What should we call this sprint?
   - Suggest kebab-case format (e.g., `payment-system`, `auth-refactor`)

2. **Location** - Where should we create it?
   - Default: `sprints/<sprint-name>/`
   - Allow custom path if needed

3. **Team** (optional) - Who will work on this?
   - Agent names: `#danny`, `#agent-1`, etc.
   - If not specified, use default `#agent`

4. **Mode** - How do you want to manage code?
   - `default` - Sprint and code in same working directory (existing behavior)
   - `worktree` - Each Feature gets its own git worktree
     - Sprint files stay in main worktree (Single Source of Truth)
     - Code work happens in separate worktrees per Feature
   - If worktree selected: Add sprint path to `.gitignore`

5. **Worktree creation method** (worktree mode only)
   - "How should worktrees be created?"
     - Default: `git worktree add` (recommended)
     - Custom: User provides command template
   - "Where should worktrees be placed?"
     - Suggest: `../<project>-worktrees/` (outside main repo)
     - Allow custom path prefix

### Phase 2: Create Structure

Create the following files from templates:

1. **BACKLOG.md** from `assets/templates/BACKLOG-TEMPLATE.md`
   - Empty backlog structure
   - Ready for features to be added

2. **HANDOFF.md** from `assets/templates/HANDOFF-TEMPLATE.md`
   - Work Board format
   - In Progress / In Review tables
   - WIP limit reminder

3. **INSTRUCTION.md** from `assets/templates/INSTRUCTION-TEMPLATE.md`
   - Multi-agent workflow
   - Session start/end procedures
   - If team specified, add team section

4. **active/** folder
   - Create empty folder
   - Add README explaining purpose

5. **refs/** structure
   - `refs/designs/` with README
   - `refs/plans/` with README
   - `refs/decisions/` with README + `_sprint.md` (sprint-wide decisions)
   - `refs/lessons/` with README + `_sprint.md` (sprint-wide lessons)
   - `refs/archive/` with README (for completed features)

6. **Version file**
   - Create `.sprint-version` with current template version (from ## Version section above)
   - Format: just the version number (e.g., `1.0.0`)

7. **.sprint-config**
   - JSON config storing sprint mode and worktree settings
   - Created for both modes (to make mode explicit)

   Default mode:
   ```json
   {
     "mode": "default"
   }
   ```

   Worktree mode:
   ```json
   {
     "mode": "worktree",
     "sprintRoot": "<absolute-path-to-sprint-dir>",
     "worktree": {
       "command": "git worktree add {path} -b {branch}",
       "pathPrefix": "../<project>-worktrees"
     }
   }
   ```

   - `worktree.command`: Worktree creation command
     - Default: `"git worktree add {path} -b {branch}"`
     - Custom example: `"./scripts/create-worktree.sh {branch} {path}"`
     - Placeholders: `{path}` = worktree path, `{branch}` = branch name
   - `worktree.pathPrefix`: Parent path where worktrees are created
     - Default: `"../<project>-worktrees"`
     - Feature worktrees are created under this path

**Worktree mode additional steps:**
- Add sprint path to project `.gitignore`
- Include Sprint Root absolute path + Worktree Mode section in INSTRUCTION.md

### Phase 3: Confirm

Show created structure and explain next steps:

**Default mode:**
```
Sprint created at: sprints/<sprint-name>/

Files:
- BACKLOG.md - Add work items with /sprint:add-backlog
- HANDOFF.md - Work board (current status)
- INSTRUCTION.md - Start work sessions with @INSTRUCTION.md #agent-name

Next steps:
1. Add work items: /sprint:add-backlog
2. Start working: @INSTRUCTION.md #your-name
```

**Worktree mode:**
```
Sprint created at: sprints/<sprint-name>/ (worktree mode)

Files:
- BACKLOG.md - Add work items with /sprint:add-backlog
- HANDOFF.md - Work board (current status)
- INSTRUCTION.md - Start work sessions with @INSTRUCTION.md #agent-name
- .sprint-config - Sprint configuration (mode: worktree)

Sprint path added to .gitignore (sprint files are not git-tracked).

Next steps:
1. Add work items: /sprint:add-backlog
2. Start working: @INSTRUCTION.md #your-name
```

---

## Assets

- `assets/templates/BACKLOG-TEMPLATE.md` - Backlog structure
- `assets/templates/HANDOFF-TEMPLATE.md` - Work Board template
- `assets/templates/INSTRUCTION-TEMPLATE.md` - Agent guidelines
- `assets/templates/FEATURE-DESIGN-TEMPLATE.md` - Feature design doc
- `assets/templates/TASK-PLAN-TEMPLATE.md` - Task plan doc
- `assets/templates/ACTIVE-FEATURE-TEMPLATE.md` - Active feature context
- `assets/refs/designs-README.md` - README for designs folder
- `assets/refs/plans-README.md` - README for plans folder
- `assets/refs/decisions-README.md` - README for decisions folder
- `assets/refs/lessons-README.md` - README for lessons folder
- `assets/refs/archive-README.md` - README for archive folder
