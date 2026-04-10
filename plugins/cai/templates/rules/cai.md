<!-- TOOL-MANAGED:START -->
<!-- This section is managed by cai-upgrade. Do not edit manually. -->

# CAI System

## Configuration

Context directory: context
Source roots: [src/]

---

## Pre-work: Context loading

Before starting any task (code changes, analysis, design, review), load related context.
**Use `tools/cai.py` BEFORE exploring source code.** Do not skip this step — ad-hoc grep/glob misses context that only exists in documents (roadmap, decisions, rationale).

0. **CLI-first discovery** — run one of these based on task type:
   - Task described in words → `./tools/cai.py budget --task "<description>"`
   - Specific file/module work → `./tools/cai.py suggest <file|dir|module>`
   - Keyword search → `./tools/cai.py search "<keywords>"`
   Then read the documents the CLI recommends before touching source code.
1. Identify the relevant modules using **Source roots** above.
2. Search `context/specs/` for matching specs:
   - First, check specs with a `covers` field that includes the target path or module.
   - If none found, use convention-based mapping: `context/specs/{module}/` maps to `{source_root}/{module}/`.
3. If specs exist, read them and follow their patterns.
   - `confidence: draft` or `intent` — reference only; cross-check against source code.
   - `confidence: reviewed` or `verified` — follow as authoritative.
4. Check `context/conventions/` for applicable rules.
5. Check `context/issues/` — do not worsen known problems.
6. Check `context/decisions/` — respect accepted decisions.
7. For analysis or design tasks, also check `context/project.md` for project-level context.

---

## Post-work: Spec maintenance

After completing a code change (not during):

1. If the change contradicts an existing spec:
   - Propose: "This change diverges from `{spec_path}`. Update the spec?"
2. If a non-trivial pattern was created in an area with no spec:
   - Propose: "Document this as a new spec?"
3. Proposals happen **once**, after work is done. Never interrupt the workflow.

Format: one-line summary + approval request. No lengthy explanations.
If the developer declines, move on immediately.

---

## Knowledge capture protocol

When you discover any of the following during work, **do not interrupt**. Note it and propose at completion:

1. **New failure mode** (root cause found via debugging)
   - Propose: "Record this failure mode in `{issue_or_agent_spec}`?"
2. **Non-obvious pattern** (something that "must be done this way" to work)
   - Propose: "Add this pattern to `{convention_or_spec}`?"
3. **Architecture decision** (alternatives compared, one chosen)
   - Propose: "Record this as a decision?"
4. **Future plan discovered** (planned migration, deprecation, feature)
   - Propose: "Record this as a roadmap item?"

Format: one-line summary + approval request.
If declined, move on immediately.

---

## Stale awareness

When the drift-warning hook injects a stale warning:

1. Read the flagged spec, but **trust current code over outdated spec content**.
2. Complete your current task first.
3. After completion, propose: "This spec is outdated. Update it?"

---

## Context type behavior rules

| Type | Status/Level | Required behavior |
|------|-------------|-------------------|
| `project` | — | Understand project purpose and constraints |
| `decision` | accepted | Respect this decision. Do not reverse it. |
| `decision` | deprecated/superseded | No longer valid. Check `superseded_by`. |
| `spec` | — | Follow this pattern. |
| `convention` | — | Always apply this rule. |
| `issue` | — | Do not worsen this problem. |
| `glossary` | — | Use this term with this meaning. |
| `roadmap` | planned/in-progress | Be aware of this direction. Avoid large investments that conflict. |
| `roadmap` | exploring | Reference only. Not confirmed. |

---

## Hallucination prevention

- Do not make architectural claims not found in `context/` documents.
- If uncertain, say "This is not documented in specs" and read the source code.
- Never invent APIs, function signatures, or patterns that do not exist in the codebase.
- When a spec and code disagree, code is the source of truth.

---

## /compact handling

When `/compact` is invoked, include in the summary:
- Paths of context documents currently being worked with.
- Any pending spec update proposals not yet addressed.

---

## Action routing

When a proposal is approved, invoke the corresponding skill:

| Situation | Skill | Notes |
|-----------|-------|-------|
| Spec creation/update needed | cai-add-spec | Invokes spec-writer agent, then verification-agent |
| New decision discovered | cai-add-decision | Invokes cai:cai-interview skill for ADR details |
| Failure mode/pattern discovered | cai-capture-lesson | Routes to appropriate doc (issue/spec/convention) |
| New roadmap item discovered | cai-add-roadmap | Invokes cai:cai-interview skill for roadmap details |
| Stale spec needs update | cai-drift-check | Drift assessment then update proposal |
| New agent needed | cai-add-agent | Creates agent .md + adds trigger table row |

---

## Sub-Agent / Agent Teams — Mandatory CAI usage

The CAI protocol applies to **all execution contexts** without exception: direct sessions, Sub-Agents, and Agent Teams members.

When spawning a Sub-Agent or Agent Teams member, **always include the following in the prompt**:

> **CAI Protocol — follow before and after any code work.**
>
> This project has a `context/` knowledge base. You must use it — ad-hoc grep/glob misses architectural decisions, conventions, known issues, and rationale that only exist in context documents.
>
> **Pre-work (before touching source code):**
> 1. Run `./tools/cai.py budget --task "<your task>"` (or `suggest <target>` / `search "<keywords>"`) to discover relevant docs.
> 2. Read the recommended docs from `context/` — specs, conventions, decisions, issues.
> 3. Follow the rules in `.claude/rules/cai.md` (pre-work steps 1–7, context type behavior, hallucination prevention).
>
> **During work:**
> - `context/conventions/` — always apply matching rules.
> - `context/decisions/` (accepted) — do not reverse.
> - `context/issues/` — do not worsen known problems.
> - `context/specs/` — follow patterns (check `confidence` level).
>
> **Post-work:**
> - If your change contradicts a spec, propose an update.
> - If you created a non-trivial pattern with no spec, propose documenting it.

<!-- TOOL-MANAGED:END -->

<!-- PROJECT-SPECIFIC:START -->
<!-- This section is preserved by cai-upgrade. Safe to edit. -->

## Agent routing trigger table

<!-- Populated incrementally by cai-add-agent. The system works without entries here. -->
<!-- Example row:
| Pattern | Agent | Timing |
|---------|-------|--------|
| src/payment/** | payment-specialist | pre-change |
-->

<!-- PROJECT-SPECIFIC:END -->
