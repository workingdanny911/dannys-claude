# Changelog

All notable changes to the sprint plugin templates.

Format: [Keep a Changelog](https://keepachangelog.com/)
Versioning: [Semantic Versioning](https://semver.org/)

- **Major**: Breaking changes to file structure
- **Minor**: New sections, updated rules
- **Patch**: Typo fixes, clarifications

---

## [1.8.0] - 2026-02-15

### Added

- **Scope Narrowing** section in INSTRUCTION-TEMPLATE.md: When a Feature is assigned
  but agent teams are not used, the agent narrows working scope to a single Task
- Solo agent scope guidance in add-backlog skill for the no-teams case

### Changed

- **Session Start Step 5**: "Otherwise → proceed directly" replaced with explicit
  scope narrowing reference
- **Session Start Step 3**: Feature assignment now references Step 5 for scope narrowing
- **Agent Session Lifecycle** in CONCEPTS.md: "Select Task" → "Determine Scope"
- **Agent Teams** in CONCEPTS.md: Added "Without teams" clause

---

## [1.6.0] - 2026-02-14

### Changed

- **Scope generalization**: Core rules generalized from "Task" to "assignment"
  — same rules now naturally apply to Feature and Task scope without exceptions
- **Session Start**: "Find your task" → "Determine your assignment" with parallelism
  assessment built into the flow (Step 5)
- **WIP Limit**: "1 task at a time" → "1 assignment at a time"
- **Completing Work**: "One session = One task" → "One session = One assignment"

### Added

- **Agent Teams** as top-level section (elevated from Plan Mode Rule subsection)
  — covers both Feature→Task and Task→Sub-task with execution tools,
  responsibilities, and lifecycle guidance
- Example 8 in EXAMPLES.md: Feature-level agent teams end-to-end scenario

### Removed

- Agent Teams subsection from Plan Mode Rule (moved to top-level, cross-referenced)

---

## [1.5.0] - 2026-02-09

### Changed

- **Agent Teams** section in INSTRUCTION-TEMPLATE.md: Reframed from speed-only ("Parallel Execution") to include quality benefits (cross-verification, independent testing, multi-perspective exploration)

### Added

- **Agent Teams** section in TASK-PLAN-TEMPLATE.md: Optional section with Purpose field (speed/quality/both) that agents must consider when writing plans
- **Agent Teams Consideration** in add-backlog and plan-backlog skills: Guidance to evaluate agent teams for both speed and quality during Feature/Task design
- **Agent Teams** concept in CONCEPTS.md: Defines agent teams with dual purpose (speed + quality), distinguishes from session-based multi-agent coordination
- Cross-reference from Multi-Agent Workflow to Agent Teams in INSTRUCTION-TEMPLATE.md

---

## [1.4.0] - 2026-02-08

### Added

- **Agent Teams (Parallel Execution)** section in INSTRUCTION-TEMPLATE.md: Guides agents to evaluate parallelizable sub-tasks during Plan Mode and use agent teams (TeamCreate, Task with team_name) when beneficial. Includes criteria for when to use/skip teams and required plan file documentation (team composition, dependencies, merge points).

---

## [1.3.0] - 2025-02-08

### Changed

- **Mandatory review before done**: Tasks must go through `review` status before `done`. Agents can no longer skip directly to `done`.
- **Completing a Task**: Renamed "Definition of Done" to "Self-Check". Steps now require `review` status, reporting to user, and requesting review.
- **HANDOFF.md flow**: Task completion moves to "In Review" (not "Recently Done").
- **Agent Session Lifecycle**: "Complete" step renamed to "Mark Review" in CONCEPTS.md.
- **Status descriptions**: `review` marked as mandatory step; `done` clarified as "User reviewed and approved".

### Added

- **Handling Review Tasks** section in INSTRUCTION-TEMPLATE.md: Defines agent behavior when encountering `review` tasks — explain work in detail, request user review, act on user decision (approve → done, request changes → improve).
- **Phase 3.5 User Review** in WORKFLOW-GUIDE.md: Documents the user review flow with examples.
