# Sprint Plugin

Sprint management with kanban-style backlog for multi-agent collaboration in Claude Code.

## Overview

The Sprint plugin is a kanban-style work management system designed for Claude Code agents to collaborate on projects.

### Key Features

- **Hierarchical Work Structure**: Decompose work into Feature → Task → Sub-task
- **Multi-Agent Support**: Multiple Claude Code sessions can work simultaneously
- **WIP Limit**: 1 Task per agent (maintain focus)
- **Session-Based Work**: Complete one Task per session
- **Context Management**: Document structure for knowledge transfer between sessions

### Generated Structure

```
sprints/<sprint-name>/
├── BACKLOG.md          # Work items (Feature → Task → Sub-task)
├── HANDOFF.md          # Current status board
├── INSTRUCTION.md      # Agent guidelines
├── .sprint-version     # Template version tracking
├── active/             # In-progress Feature context
└── refs/
    ├── designs/        # Feature design documents
    ├── plans/          # Task execution plans
    ├── decisions/      # Decision records (_sprint.md for sprint-wide)
    ├── lessons/        # Lessons learned (_sprint.md for sprint-wide)
    └── archive/        # Completed Feature archive
```

---

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| init | `/sprint:init` | Initialize a new sprint with kanban structure |
| add-backlog | `/sprint:add-backlog` | Add features/tasks to backlog |
| plan-backlog | `/sprint:plan-backlog` | Design detailed sub-tasks for backlog items |
| review-backlog | `/sprint:review-backlog` | Review completed tasks/features |
| review-work | `/sprint:review-work` | Review and improve work in same session, then mark done |
| update-version | `/sprint:update-version` | Update sprint to latest template version |

---

## Quick Start

### 1. Initialize a Sprint

```
/sprint:init
```

Interactively set Sprint name and location.

### 2. Add Work Items

```
/sprint:add-backlog
```

Define Features and Tasks through brainstorming.

### 3. Start Working

```
@sprints/my-sprint/INSTRUCTION.md #danny
```

Start a session with an agent name and work on Tasks.

### 4. After Completion

End the session. Start a new session for the next Task.

---

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Sprint Lifecycle                         │
└─────────────────────────────────────────────────────────────────┘

  /sprint:init          /sprint:add-backlog       @INSTRUCTION.md
       │                       │                        │
       ▼                       ▼                        ▼
┌─────────────┐        ┌─────────────┐        ┌─────────────────┐
│ Create      │   ──▶  │ Add Feature │   ──▶  │ Work on Task    │
│ Sprint      │        │ Define Task │        │ (single session)│
└─────────────┘        └─────────────┘        └─────────────────┘
                              │                        │
                              │                        ▼
                              │               ┌─────────────────┐
                              │               │ Complete Task   │
                              │               │ Update HANDOFF  │
                              │               └─────────────────┘
                              │                        │
                              │   /sprint:review-backlog   │
                              │               │            │
                              ▼               ▼            ▼
                       ┌─────────────────────────────────────┐
                       │         Next Task or Done           │
                       └─────────────────────────────────────┘
```

---

## Task Status Flow

```
backlog ──────► in_progress ──────► review ──────► done
                    │                  │
                    ▼                  │
                 blocked ◄─────────────┘
                    │
                    ▼
                 backlog (when unblocked)
```

---

## Documentation

See the [docs/](./docs/) folder for detailed documentation:

- [CONCEPTS.md](./docs/CONCEPTS.md) - Core concepts explained
- [WORKFLOW-GUIDE.md](./docs/WORKFLOW-GUIDE.md) - Workflow guide
- [EXAMPLES.md](./docs/EXAMPLES.md) - Real-world examples
- [TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md) - Troubleshooting guide

---

## Best Practices

### Task Sizing

**Good Task Size**:
- Implement 1 API endpoint
- Write tests for 1 component
- Write 1 documentation page

**Too Large** (needs breakdown):
- "Implement entire auth system" → Break into Login API, Signup API, Token Refresh, etc.
- "Write all API docs" → Break by endpoint group

### Session Management

```
Start Session
    │
    ▼
@INSTRUCTION.md #agent-name
    │
    ▼
Complete 1 Task
    │
    ▼
End Session (do NOT auto-start next Task)
    │
    ▼
Start New Session (for next Task)
```

### Context Preservation

- `active/F{n}-*.md`: Real-time context for in-progress Features
- `refs/decisions/`: Decision records (answer "why?" later)
- `refs/lessons/`: Lessons learned (prevent repeated mistakes)

---

## License

MIT
