# Danny's Claude Plugins

A personal plugin marketplace for Claude Code.

## Installation

```bash
# Add marketplace
/plugin marketplace add dannys-claude https://github.com/workingdanny911/dannys-claude

# Install plugin
/plugin install sprint@dannys-claude
```

## Plugins

### [sprint](plugins/sprint/README.md)

Kanban-style sprint management for multi-agent collaboration.

**Skills:**

| Command | Description |
|---------|-------------|
| `/sprint:init` | Initialize sprint structure (BACKLOG.md, HANDOFF.md, INSTRUCTION.md) |
| `/sprint:add-backlog` | Add features/tasks through guided brainstorming |
| `/sprint:plan-backlog` | Break down items into actionable sub-tasks |
| `/sprint:review-backlog` | Quality review with type-specific checklists |
| `/sprint:update-version` | Update existing sprint to latest template |

**Commands:** 1:1 mapping to skills for `/sprint:` autocompletion

**Workflow:**

```
/sprint:init → /sprint:add-backlog → /sprint:plan-backlog → work → /sprint:review-backlog
```

**Generated Structure:**

```
sprints/<name>/
├── BACKLOG.md       # Feature → Task → Sub-task
├── HANDOFF.md       # Work board (In Progress / In Review)
├── INSTRUCTION.md   # Agent guidelines
└── refs/
    ├── designs/     # Feature design docs
    ├── plans/       # Task execution plans
    ├── decisions/   # Decision records
    └── lessons/     # Lessons learned
```

## License

MIT
