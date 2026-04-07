# CAI -- Context As Infrastructure

**Persistent, structured memory for AI coding agents that scales from 10K to 1M+ lines of code.**

AI coding agents lose memory between sessions. Every new conversation starts from scratch -- conventions forgotten, past decisions ignored, known issues repeated. A single `CLAUDE.md` works for small projects, but breaks down at scale.

CAI solves this by treating project documentation as **infrastructure** -- living, machine-readable artifacts that AI agents depend on to produce correct, convention-adherent code. Architecture decisions, module specs, coding conventions, known failure modes, and future plans are captured in plain markdown and loaded automatically.

---

## Table of Contents

- [Background and Motivation](#background-and-motivation)
- [How It Works](#how-it-works)
- [Quick Start](#quick-start)
- [The Developer Experience](#the-developer-experience)
- [CLI Tool](#cli-tool)
- [Skills Reference](#skills-reference)
- [Agents Reference](#agents-reference)
- [Context Document Types](#context-document-types)
- [Directory Structure](#directory-structure)
- [Design Decisions](#design-decisions)
- [Versioning and Upgrade](#versioning-and-upgrade)
- [References](#references)

---

## Background and Motivation

### The Research Foundation

CAI builds on the research by Aristidis Vasilopoulos ([arXiv:2602.20478](https://arxiv.org/abs/2602.20478)), which presents a three-component *codified context infrastructure* developed during construction of a 108,000-line C# distributed system across 283 development sessions:

1. **A constitution** (~660 lines, hot memory) -- always loaded, encoding conventions and orchestration protocols
2. **19 specialized domain-expert agents** (~9,300 lines) -- invoked per task via trigger tables
3. **34 on-demand specification documents** (~16,250 lines, cold memory) -- retrieved as needed

The paper demonstrated four distinct mechanisms by which codified context improves development outcomes: specifications as inter-session coordination documents (74 sessions of consistent behavior), captured experience preventing repeated trial-and-error (10+ subsequent sessions), documentation as an investment converting one-time effort into persistent velocity, and embedded domain knowledge enabling collaborative debugging of subtle cross-cutting bugs.

A key finding: **over 50% of effective agent specifications are domain knowledge** (code patterns, failure modes, architectural constraints), not behavioral instructions.

### What CAI Generalizes

The paper's architecture was validated on a single developer, single project (C# game), and single tool (Claude Code). CAI generalizes it along every axis:

| Dimension | Paper | CAI |
|-----------|-------|-----|
| Language | C# | Any |
| Scale | 108K LOC | 10K -- 1M+ LOC |
| Team size | 1 | 1 -- 10+ |
| Tool | Claude Code | Claude Code + Codex |
| Domain | Game dev | Any |

The core insight remains the same: as projects grow in complexity, agents lose coherence and developers are pulled back into resolving routine errors. Persistent, machine-readable specifications keep agents producing correct output even as the codebase scales.

---

## How It Works

CAI implements a 3-layer architecture where each layer provides a different guarantee:

```
                        ┌─────────────────────┐
                        │    AI Session        │
                        └────┬───────────┬─────┘
                             │           │
               always loaded │           │ on file edit
                             ▼           ▼
                ┌────────────────┐  ┌────────────────┐
                │  Layer 1       │  │  Layer 2       │
                │  Rules File    │  │  Hook          │
                │  (engine)      │  │  (safety net)  │
                └───────┬────────┘  └────────────────┘
                        │
                        │ when approved
                        ▼
                ┌────────────────┐
                │  Layer 3       │
                │  Skills        │
                │  (escape hatch)│
                └────────────────┘
```

### Layer 1: Rules File (Engine)

`.claude/rules/cai.md` is loaded automatically every session. It defines all AI behaviors:

- **Pre-work**: Read relevant specs before editing code
- **Post-work**: Propose spec updates after changes
- **Knowledge capture**: Record decisions, failure modes, and patterns
- **Stale awareness**: Trust code over outdated specs
- **Action routing**: Map situations to the correct skill

The rules file is the heart of the system. The AI reads it, follows it, and the developer never has to invoke commands manually.

### Layer 2: Hook (Safety Net)

A `PreToolUse` hook fires on every file edit. If the file being modified has a related spec that is stale (source changed since `last_synced`), the hook injects a warning into the session. No LLM calls, millisecond latency. This catches cases where the AI skips a rule -- because instruction following is never 100%.

### Layer 3: Skills (Escape Hatch)

Explicit commands developers can invoke when needed. In practice, the AI calls most of these internally. The developer's role is to approve or decline proposals.

### Knowledge Taxonomy

Project knowledge is classified along a **temporal axis**. Each type triggers different AI behavior:

| Temporal Axis | Type | AI Behavior |
|---------------|------|-------------|
| Identity | `project` | Understand the project's purpose and constraints |
| Past | `decision` (accepted) | Respect this decision. Do not reverse it. |
| Past | `decision` (deprecated) | No longer valid. Follow `superseded_by`. |
| Present | `spec` | Follow this pattern. |
| Present | `convention` | Always apply this rule. |
| Present | `issue` | Do not make this problem worse. |
| Present | `glossary` | Use this term with this meaning. |
| Future | `roadmap` (planned) | Be aware of this direction. Avoid conflicting investments. |
| Future | `roadmap` (exploring) | Reference only. Not confirmed. |

Seven document types, each with a clear contract the AI must follow.

### Drift Detection

The primary failure mode is **stale specs**. Agents trust documentation absolutely, so an outdated spec is worse than no spec at all. CAI builds three layers of defense:

1. **Hook (real-time)** -- Checks `last_synced` vs. git history on every file edit
2. **Rules instruction (AI-initiated)** -- AI proposes spec updates after code changes
3. **`/cai-drift-check` (full scan)** -- Walks all context documents, classifies each as STALE / POSSIBLY STALE / REVIEW SUGGESTED

Stale detection uses `covers` fields when present, falls back to convention-based directory mapping, and flags time-based staleness for documents without source mappings.

---

## Quick Start

### Installation

Install CAI as a Claude Code plugin.

### For an existing project

```
/cai-init
```

The onboarding pipeline runs in four phases:

| Phase | What Happens | Interaction |
|-------|-------------|-------------|
| 1. Auto-analysis | Scan directory structure, analyze each module, cross-validate claims | Automatic |
| 2. Draft generation | Generate decisions, issues, and project.md from git history and code | Automatic |
| 3. Validation interview | Verify drafts with developer, capture knowledge code cannot reveal | Interactive |
| 4. Synthesis | Map inter-module dependencies, extract conventions, propose CLAUDE.md updates | Automatic |

All generated documents start with `confidence: draft`. The developer reviews and promotes them.

### For a new project

```
/cai-init --new
```

Since there is no code to analyze, the system starts with an interview:
1. "What are you building?" -- generates `project.md`
2. "What is the tech stack?" -- generates initial conventions
3. "Key architecture decisions?" -- generates `decisions/*.md`
4. "Known risks or constraints?" -- generates `issues/*.md`

Specs created for new projects use `confidence: intent` (planned but not yet implemented).

### Resume interrupted onboarding

```
/cai-onboard --resume
```

Output files serve as checkpoints. The pipeline skips phases whose artifacts already exist.

---

## The Developer Experience

The design goal is **zero commands to memorize**. The AI drives maintenance; the developer approves or declines.

```
Day 1:
  Developer: "Set up codified context for this project"
  AI:        (analyzes codebase, asks a few questions, sets everything up)
  Developer: Just answers the questions.

Day 2 onward:
  Developer: "Add refund support to the payment module"
  AI:        (automatically reads relevant specs, follows conventions, implements)
  AI:        "Should I update the payment spec with the refund flow?"
  Developer: "yes"

Occasionally:
  AI:        "The auth spec is outdated. Should I update it?"
  Developer: "yes"

Commands the developer must memorize: none.
What the developer manages: CLAUDE.md (which they already maintain).
```

The AI proposes context updates at the right moments -- after completing work, when it discovers a failure mode, when it makes an architecture decision. Proposals are one-line summaries with an approval prompt. If the developer says no, the AI moves on immediately.

---

## CLI Tool

`tools/cai.py` is a Python CLI designed for **AI consumption** (not human use). The AI invokes it via Bash to search, analyze, and manage context documents.

### Commands

#### Search and Discovery

```bash
# Find context related to a file, directory, or module
python tools/cai.py suggest src/auth/service.ts

# Keyword/concept search across all context
python tools/cai.py search "refund webhook"

# Task-based budget: top N most relevant documents
python tools/cai.py budget --task "add refund flow to payment module" -n 5

# Impact analysis: what modules are affected by a change
python tools/cai.py impact src/auth/service.ts
```

#### Status and Management

```bash
# Health overview: document counts, type distribution, stale ratio
python tools/cai.py status

# Filtered document listing
python tools/cai.py list --type spec --tag auth

# Show source changes since last spec sync
python tools/cai.py diff context/specs/auth/_overview.md

# Validate frontmatter schemas (with optional auto-fix)
python tools/cai.py validate --fix

# Update a document's last_synced to today
python tools/cai.py update-synced context/specs/auth/_overview.md
```

All commands support `--json` for structured output. Default output is text optimized for AI parsing, with relevance levels (high/medium/low) and inline snippets.

---

## Skills Reference

| Skill | Description | Called By | Frequency |
|-------|-------------|-----------|-----------|
| `cai-init` | Initialize codified context in a project | Developer | Once |
| `cai-onboard` | Analyze codebase and generate initial context | AI (inside cai-init) | Once |
| `cai-add-spec` | Create or update a technical specification | AI (post-work proposal) | Often |
| `cai-add-decision` | Record an architecture decision (ADR) | AI (knowledge capture) | Occasionally |
| `cai-drift-check` | Detect and fix stale specifications | AI (on stale detection) | Automatic |
| `cai-capture-lesson` | Record a failure mode or non-obvious pattern | Developer | Rare |
| `cai-upgrade` | Upgrade plugin to latest version | Developer | Rare |
| `cai-add-agent` | Create a new custom domain agent | Developer or AI | Rare |
| `cai-add-roadmap` | Record a future plan or initiative | AI (knowledge capture) | Rare |

Most skills are called by the AI internally. The rules file defines **when** each skill fires; the skill defines **how** it executes; agents define **who** does the work.

---

## Agents Reference

Agents are autonomous workers defined as markdown files in `.claude/agents/`. Each declares a domain scope, available tools, permissions, relevant Tier 3 documents, output expectations, and -- critically -- **domain knowledge** that constitutes over half of a mature agent's content.

### Onboarding Pipeline Agents

These run during `cai-onboard` to bootstrap context from an existing codebase:

| Agent | Role | Phase |
|-------|------|-------|
| `structure-scanner` | Analyze directory/file structure, identify module boundaries | 1 (auto) |
| `module-analyst` | Analyze internals of a single module (runs N in parallel) | 1 (auto) |
| `draft-generator` | Generate decisions, issues, project.md from git history and code analysis | 2 (auto) |
| `context-interviewer` | Validate drafts, interview developer for knowledge code cannot reveal | 3 (interactive) |
| `relationship-mapper` | Map inter-module dependencies and data flows | 4 (auto) |
| `convention-extractor` | Extract recurring patterns (naming, error handling, etc.) | 4 (auto) |
| `constitution-assembler` | Synthesize all outputs and propose CLAUDE.md updates | 4 (auto) |

### Persistent Agents

These remain active after onboarding and run during normal development:

| Agent | Role | Invoked |
|-------|------|---------|
| `verification-agent` | Cross-validate spec claims against source code in an independent context window | On every spec create/update |
| `context-gardener` | Update stale specs, propose new specs, prune resolved issues and completed roadmaps | Post-change |
| `code-reviewer` | Detect convention violations in changed code | Post-change |
| `spec-writer` | Read source code and write specs, verify consistency with existing specs | Ad-hoc |
| `context-interviewer` | Author documents requiring human knowledge (ADRs, roadmaps) via interview | Ad-hoc |

Projects can also define **custom domain agents** (e.g., `payment-specialist`, `auth-reviewer`) that accumulate domain-specific failure modes and code patterns over time, following the emergence pattern described in the paper.

### Domain Knowledge Accumulation

Agent specifications grow organically through an emergence pattern:

1. A general-purpose agent works on a domain
2. Repeated failures occur in the same area
3. Root causes and fixes are captured in the agent's Failure Modes table
4. Subsequent sessions benefit from pre-loaded knowledge

The standard format for capturing failure knowledge:

```markdown
## Known Failure Modes
| Symptom | Cause | Fix |
|---------|-------|-----|
| Webhook retries loop | Refund sync processing >30s | Switch to async queue |
| Desync on crits | Using local time | Use GetSyncedTime() |
```

---

## Context Document Types

All context documents use YAML frontmatter for metadata. Common required fields across all types:

| Field | Type | Description |
|-------|------|-------------|
| `type` | enum | `decision`, `issue`, `spec`, `convention`, `roadmap`, `glossary`, `project` |
| `tags` | string[] | Keyword tags (primary search index) |
| `last_synced` | date | Last date spec and code were synchronized (tool-managed) |

### Type-Specific Fields

**Specs** add `level` (project/module/component), `confidence` (intent/draft/reviewed/verified), optional `covers` (source file globs), and for module overviews: `components`, `exports`, `depends_on`.

**Decisions** add `status` (proposed/accepted/deprecated/superseded) and optional `superseded_by`.

**Roadmaps** add `status` (exploring/planned/in-progress/completed), optional `target` (e.g., "2026-Q3"), and `related_specs`.

**Issues** add `severity` (low/medium/high/critical).

### Confidence Levels

| Value | Meaning | When Assigned |
|-------|---------|---------------|
| `intent` | Not yet implemented; this is the plan | New project onboarding |
| `draft` | Auto-generated from code analysis, unverified | Existing project onboarding |
| `reviewed` | Developer has read and confirmed | After developer review |
| `verified` | Validated by tests or execution | After test pass |

AI behavior adapts to confidence: `intent` documents are treated as target designs that may not match reality; `draft` documents require cross-referencing with source code before trusting.

---

## Directory Structure

After running `/cai-init`, the following structure is created in your project:

```
project-root/
├── CLAUDE.md                           # Developer owns (project identity + context summary)
├── AGENTS.md                           # Codex compatibility layer
│
├── .claude/
│   ├── rules/
│   │   └── cai.md                      # Auto-loaded rules engine (Layer 1)
│   ├── skills/
│   │   ├── cai-init/SKILL.md
│   │   ├── cai-onboard/SKILL.md
│   │   ├── cai-add-spec/SKILL.md
│   │   ├── cai-add-decision/SKILL.md
│   │   ├── cai-add-agent/SKILL.md
│   │   ├── cai-add-roadmap/SKILL.md
│   │   ├── cai-capture-lesson/SKILL.md
│   │   ├── cai-drift-check/SKILL.md
│   │   └── cai-upgrade/SKILL.md
│   ├── agents/
│   │   ├── structure-scanner.md        # Onboarding (tool-managed)
│   │   ├── module-analyst.md
│   │   ├── draft-generator.md
│   │   ├── context-interviewer.md
│   │   ├── relationship-mapper.md
│   │   ├── convention-extractor.md
│   │   ├── constitution-assembler.md
│   │   ├── verification-agent.md       # Persistent (generated, then dev-owned)
│   │   ├── context-gardener.md
│   │   ├── code-reviewer.md
│   │   ├── spec-writer.md
│   │   └── {custom-domain-agents}.md
│   └── settings.json                   # Hook registration
│
├── tools/
│   ├── cai.py                          # CLI tool (tool-managed)
│   ├── drift-warning.js                # PreToolUse hook (Layer 2)
│   └── requirements.txt                # pyyaml
│
└── context/                            # Project knowledge base (generated, then dev-owned)
    ├── project.md                      # Project identity, vision, constraints
    ├── glossary.md                     # Domain terminology (Ubiquitous Language)
    ├── decisions/                      # ADRs (chronological, append-only)
    │   ├── 001-chose-postgresql.md
    │   └── 002-event-driven-arch.md
    ├── issues/                         # Known issues and tech debt
    │   └── perf-n-plus-one.md
    ├── conventions/                    # Coding conventions and patterns
    │   ├── error-handling.md
    │   └── api-design.md
    ├── specs/                          # Technical specifications (hierarchical)
    │   ├── _overview.md                # Project-level architecture
    │   └── {module}/
    │       ├── _overview.md            # Module design
    │       └── {component}.md          # Component detail
    └── roadmap/                        # Future plans (by status)
        ├── planned/
        ├── exploring/
        └── completed/
```

### Ownership Zones

| Zone | Files | Who Manages | cai-upgrade Behavior |
|------|-------|-------------|---------------------|
| Developer-owned | `CLAUDE.md`, `CLAUDE.local.md` | Developer | Never touched |
| Tool-owned | `.claude/rules/cai.md`, skills, onboarding agents, `tools/` | CAI | Updated |
| Generated then dev-owned | `context/**`, persistent agents, `AGENTS.md` | Developer (after initial generation) | Preserved |

### Convention-Based Mapping

When a spec does not declare an explicit `covers` field, CAI infers source file associations from directory structure:

```
context/specs/auth/_overview.md    -->  src/auth/**
context/specs/auth/jwt-service.md  -->  src/auth/jwt*.ts
```

Source roots are configurable for monorepos and non-standard layouts:

```markdown
<!-- .claude/rules/cai.md header -->
Context directory: context
Source roots: [src/, packages/*/src/]
```

---

## Design Decisions

The full design specification is at [docs/designs/v2.md](docs/designs/v2.md). Key decisions include:

| Decision | Rationale |
|----------|-----------|
| Rules-first architecture (not skill-first) | The AI drives maintenance automatically. Developers should not need to memorize commands. |
| `covers` field is optional | Convention-based mapping prevents `covers` itself from becoming a drift source. |
| Constitution = CLAUDE.md + rules file | No separate constitution file. Uses existing Claude Code mechanisms. |
| CLAUDE.md is developer-owned; tool only proposes | Clear ownership prevents conflicts. |
| Section-based merge for upgrades | Preserves project-specific customizations while updating tool-managed sections. |
| Hook as instruction backup | Instruction following is never 100%. A physical hook provides a deterministic safety net. |
| `confidence: intent` for new projects | Distinguishes "planned but not implemented" from "auto-generated and unverified". |
| Trigger table is optional | Not every project needs custom domain agents. The table grows incrementally via `cai-add-agent`. |
| Symptom-Cause-Fix as standard format | Empirically the most useful knowledge format from the paper's 283 sessions. |

---

## Versioning and Upgrade

Run `/cai-upgrade` to update CAI to the latest version.

### How it works

1. Fetch latest version from the repository
2. Create a backup for rollback
3. **Section-based merge** on `cai.md`:
   - `TOOL-MANAGED` sections (pre-work, post-work, knowledge capture, action routing, hallucination prevention) are **replaced** with the new version
   - `PROJECT-SPECIFIC` sections (trigger table, custom rules) are **preserved**
4. Show diff preview of what changes and what is preserved
5. Apply after developer approval
6. Offer new agent templates if available
7. Output migration guide for breaking changes

```markdown
<!-- Section markers in cai.md -->
<!-- TOOL-MANAGED:START -->
This section is managed by cai-upgrade. Do not edit manually.
...
<!-- TOOL-MANAGED:END -->

<!-- PROJECT-SPECIFIC:START -->
This section contains project-specific configuration. Preserved by cai-upgrade.
...
<!-- PROJECT-SPECIFIC:END -->
```

The `context/` directory, `CLAUDE.md`, and all developer-owned files are never modified by upgrades.

---

## Codex Support

The `context/` directory contains plain markdown readable by any tool. For OpenAI Codex, which cannot read `.claude/` files, CAI generates an `AGENTS.md` at the project root as an entry point:

```markdown
# AGENTS.md

## Project Knowledge Base
This project uses a codified context system.
All project knowledge is in the `context/` directory.

### Quick reference
- Project overview: context/project.md
- Architecture: context/specs/_overview.md
- Conventions: context/conventions/
- Decisions: context/decisions/
- Known issues: context/issues/
```

---

## References

- **Paper**: Vasilopoulos, A. "Codified Context: Infrastructure for AI Agents in a Complex Codebase." arXiv:2602.20478 (2025). [https://arxiv.org/abs/2602.20478](https://arxiv.org/abs/2602.20478)
- **Design Specification**: [docs/designs/v2.md](docs/designs/v2.md)
- **CLI Design**: [docs/designs/cli-design.md](docs/designs/cli-design.md)
- **Interface Contract**: [docs/interface-contract.md](docs/interface-contract.md)

---

## License

See [LICENSE](LICENSE) for details.
