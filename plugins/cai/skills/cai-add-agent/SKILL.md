---
name: cai-add-agent
description: "Use when creating a custom domain agent. Triggers: 'cai-add-agent', 'agent 추가', 'domain agent', 'add agent', '에이전트 추가', '에이전트 생성'"
---
# CAI Add Agent

## Overview

Creates a new project-specific agent definition file and optionally registers it in the rules file's agent routing trigger table.

## When to Use

- A recurring domain-specific task is identified that benefits from a dedicated agent
- User wants to create a custom agent for a specific area of the codebase
- Action routing: "새 agent 필요" triggers this skill

## Workflow

### 1. Gather Agent Information

Collect the following (from conversation context or by asking the user):

| Field | Description | Required |
|-------|-------------|----------|
| Name | Agent identifier in kebab-case (e.g., `payment-expert`) | Yes |
| Role | What this agent does (1-2 sentences) | Yes |
| Trigger patterns | When should this agent be invoked | Yes |
| File areas | Which files/directories this agent is responsible for | Yes |
| Domain knowledge | Specialized knowledge this agent needs | No |
| Referenced specs | Context docs this agent should read | No |

### 2. Generate Agent File

Create `.claude/agents/{name}.md` following Interface Contract 0.3 format:

```yaml
---
name: {name}
description: "{trigger description}"
model: inherit
---
# {Agent Display Name}

## Role & Scope
{Role description, available tools, authority boundaries}

## Inputs
{What this agent receives: file paths, previous agent outputs, etc.}

## Process
{Step-by-step work procedure}

## Domain Knowledge
{Agent-specific expertise relevant to its domain}

## Output Format
{Exact format of artifacts and where they are stored}

## Referenced Specs
{List of context docs this agent should read}

## Constraints
{What this agent must NOT do}
```

### 3. Register in Trigger Table (Optional)

Ask the user: "Add this agent to the routing trigger table in cai.md?"

If yes, add a row to the `PROJECT-SPECIFIC` section of `.claude/rules/cai.md`:

```markdown
<!-- PROJECT-SPECIFIC:START -->
## [PROJECT-SPECIFIC] Agent routing trigger table

| Trigger Pattern | Agent | Description |
|----------------|-------|-------------|
| {existing rows} |
| {new trigger pattern} | {agent-name} | {brief description} |

<!-- PROJECT-SPECIFIC:END -->
```

### 4. Confirm

Present the generated agent file to the user for review. Write to disk only after approval.

## Agent Invocations

This skill does not invoke other agents. It generates agent definition files directly.

## Output

| Artifact | Path | Format |
|----------|------|--------|
| Agent definition | `.claude/agents/{name}.md` | Markdown with YAML frontmatter (Interface Contract 0.3) |
| Trigger table row | `.claude/rules/cai.md` | Appended to PROJECT-SPECIFIC section |

## Error Handling

| Error | Action |
|-------|--------|
| Agent with same name already exists | Ask user: update existing or choose a different name |
| `.claude/agents/` directory does not exist | Create it before writing |
| Rules file has no PROJECT-SPECIFIC section | Add the section markers and trigger table |
| User provides insufficient role description | Ask clarifying questions about the agent's purpose and scope |
