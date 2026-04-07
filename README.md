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

### [explain](plugins/explain/skills/explain/SKILL.md)

Explain any subject — architecture, technical concepts, decision options, project progress, business domains — using storytelling, diagrams, and examples. Starts with a high-level overview, then explores multiple facets. Hallucination-forbidden: every claim backed by a source or marked as inference.

**Skills:**

| Command | Description |
|---------|-------------|
| `/explain:explain` | Explain a subject with sources, diagrams, and examples |

**Triggers:** `explain`, `설명해줘`, `알려줘`, `이해하고 싶어`, `뭐야`, `어떻게 동작해`

### [cai](plugins/cai/README.md)

Context As Infrastructure — persistent, structured memory for AI coding agents that scales from 10K to 1M+ LOC. Based on [arXiv:2602.20478](https://arxiv.org/abs/2602.20478). Rules-first architecture (AI drives maintenance, zero commands to memorize) with drift detection hook as safety net.

**Skills:**

| Command | Description |
|---------|-------------|
| `/cai:cai-init` | Initialize CAI in a project (runs onboarding pipeline) |
| `/cai:cai-onboard` | Analyze codebase and generate initial context |
| `/cai:cai-add-spec` | Create or update a technical specification |
| `/cai:cai-add-decision` | Record an architecture decision (ADR) |
| `/cai:cai-add-roadmap` | Record a future plan or initiative |
| `/cai:cai-add-agent` | Create a custom domain agent |
| `/cai:cai-drift-check` | Detect and fix stale specifications |
| `/cai:cai-capture-lesson` | Record a failure mode or non-obvious pattern |
| `/cai:cai-upgrade` | Upgrade plugin to latest version |

**Generated Structure:**

```
project-root/
├── CLAUDE.md                  # Developer-owned (identity + context summary)
├── AGENTS.md                  # Codex compatibility entry point
├── .claude/
│   ├── rules/cai.md           # Auto-loaded rules engine (Layer 1)
│   ├── agents/                # Onboarding + persistent + custom domain agents
│   └── settings.json          # PreToolUse drift-warning hook (Layer 2)
├── tools/
│   ├── cai.py                 # CLI for AI consumption (search, budget, impact)
│   └── drift-warning.js       # Real-time stale-spec detector
└── context/                   # Knowledge base (7 document types)
    ├── project.md, glossary.md
    ├── decisions/  issues/  conventions/
    ├── specs/{module}/{component}.md
    └── roadmap/{planned,exploring,completed}/
```

### [codebase-x-ray](plugins/codebase-x-ray/README.md)

Analyze famous open-source codebases (DOOM, Redis, Bitcoin, PostgreSQL, …) and generate book-length technical biographies that teach software engineering through real code. Language-agnostic, output follows user's language, with two-layer verification to prevent hallucination.

**Skills:**

| Command | Description |
|---------|-------------|
| `/codebase-x-ray:analyze` | Full pipeline: research → analysis → writing → assembled book |

**Usage:**

```
"x-ray redis"
"DOOM x-ray해줘"
"x-ray redis at ~/research/redis"
"continue ~/research/redis"    # resume interrupted session
```

**Pipeline:**

```
ANALYSIS                            WRITING
  Phase 0a  Web research              Phase 4  Chapter design
  Phase 0b  Semantic anchors          Phase 5  Per-chapter writing (parallel)
  Phase 1   Directory survey          Phase 6  Cross-chapter review
  Phase 2   Boundary synthesis        Verifier Final audit
  Phase 3   Module deep dive (∥)           ↓
  Verifier  Structural audit          build.sh → book.md + book.pdf
       ↓
  Artifact Store (reusable)
```

**Generated Structure:**

```
{project_root}/
├── manifest.md                # Progress tracking (crash recovery)
├── source/                    # Cloned repository
├── references/                # Papers, slides, downloaded materials
├── checkpoints/               # Per-phase outputs (phase0a, phase1/*, phase2, …)
├── artifacts/modules/         # Reusable deep-dive artifacts
└── output/
    ├── 00-prologue.md ... NN-{chapter}.md
    ├── build.sh               # cat + pandoc assembly
    └── book.md                # Final assembled book
```

## License

MIT
