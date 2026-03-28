---
name: explain
description: "Explain any subject — architecture, technical concepts, decision options, project progress, business domains — using storytelling, diagrams, and examples. Always starts with a high-level overview, then explores multiple facets. Triggers: 'explain', '설명해줘', '알려줘', '이해하고 싶어', '뭐야', '어떻게 동작해'"
---

# Explain Skill

Explain any subject deeply using storytelling, diagrams, and examples.

## Top-Level Principle

> **Hallucination is absolutely forbidden.**
>
> - Every statement must be backed by a source or clearly marked as inference.
> - If you don't know, say "I don't know."
> - If it's a guess, say "This is a guess."
> - Never present uncertainty as fact. No exceptions.

---

## Step 1: Classify Target & Gather Sources

### Target Classification

```
What is the user asking to understand?
|
+-- Code/Project -- Architecture, module, feature in current codebase
+-- Concept      -- Technical concept, pattern, framework, protocol
+-- Decision     -- Comparing options before making a choice
+-- Progress     -- Current work/project status
+-- Domain       -- Business domain, process, workflow
```

### Source Strategy

| Target Type | Sources |
|-------------|---------|
| Code/Project | Read code, git log, project docs, README, tests |
| Concept | Own knowledge + WebSearch for official docs/articles |
| Decision | Internal sources + external sources (mixed) |
| Progress | git log/diff, sprint files, issue tracker |
| Domain | Project docs + external domain references |

> **CRITICAL: Read ALL sources BEFORE generating any explanation.**
> Do not start explaining until sources are sufficiently gathered.

### Fact Verification

```
For every statement you are about to write:
|
+-- Confirmed by source?
|   +-- YES --> State as fact
|   +-- NO
|       +-- Reasonable inference with evidence?
|       |   +-- YES --> Mark "[inference]" and state the basis
|       |   +-- NO  --> Do not state it
|       |
|       +-- Can you verify it?
|           +-- YES --> Verify first, then state
|           +-- NO  --> State "not confirmed"
|
+-- Absolutely forbidden:
    +-- Mentioning APIs, functions, or files that don't exist
    +-- Stating guesses as facts
    +-- Writing uncertain content with confidence
    +-- Citing specific numbers or names without a source
```

---

## Step 2: Generate High-Level Overview

The overview is the core of this skill. It must be **thorough enough that someone with no background can understand the subject**.

### Structure

#### 1) Overview

- What is this? Why does it exist? What problem does it solve?
- Use **analogies and storytelling** to make it approachable
- No length limit — explain until it's understood
- Start from the background, build up gradually

#### 2) Multi-Facet Explanation Blocks

Examine the subject from **multiple perspectives (facets)**. Identify facets based on the target:

| Target Type | Candidate Facets |
|-------------|-----------------|
| Code/Project | Structure, data flow, dependencies, deployment, failure propagation |
| Concept | How it works, use cases, limitations, alternatives |
| Decision | Each option (mechanism, pros/cons, cost, risk) |
| Progress | Timeline, completion, changes made, what remains |
| Domain | Participants, process, rules, edge cases |

Facets are **not fixed** — choose what fits the subject. 1 facet or 10 facets, whatever is needed.

**Every facet block MUST include all three elements:**

```
+-------------------------------+
|  Story                        |  <-- The narrative from this perspective
|  - - - - - - - - - - - - - - |
|  Diagram(s)                   |  <-- Visualization (ASCII, UML, table)
|  - - - - - - - - - - - - - - |
|  Example(s)                   |  <-- Concrete scenarios, code samples
+-------------------------------+
```

- Multiple stories if one isn't enough
- Multiple diagrams if one isn't enough
- Multiple examples if one isn't enough
- **Sufficiency is the measure. No limits on quantity.**

#### 3) Key Concepts Map

Prerequisites — what you need to know to understand this subject.

- Each concept gets as much explanation as it needs (a sentence, a paragraph, or more)
- Not a glossary — an understanding aid

#### 4) Drill-Down (optional, user-initiated)

After the overview, if the user wants to go deeper into a specific part, explain that part with the same structure: story + diagrams + examples.

---

## Step 3: Automatic Depth Adjustment

```
Assess subject complexity:
|
+-- Simple (1 concept, 1-2 facets sufficient)
|   --> Overview + 1-2 facet blocks + concepts map
|
+-- Moderate (3-4 facets needed)
|   --> Overview + 3-4 facet blocks + concepts map
|
+-- Complex (whole system, multi-layer architecture)
    --> Overview + 5+ facet blocks + concepts map
    --> Additionally explain relationships between facets
```

**User overrides:**
- "deeper" / "more detail" --> Add facets, expand each block
- "briefly" / "summary only" --> Overview + 1-2 key facets

---

## Step 4: Diagram Guide

### Choosing Diagram Types

```
What are you trying to show?
|
+-- Relationships between components --> Component Diagram (box + arrow)
+-- Chronological flow               --> Sequence Diagram
+-- State transitions                 --> State Diagram
+-- Where data flows                  --> Flow Diagram
+-- Hierarchy / containment           --> Tree / Nested Box
+-- Comparison                        --> Table
+-- Physical layout / deployment      --> Deployment / Layout Diagram
```

### Diagram Rules

- ASCII diagrams use **English only** (Korean breaks monospace alignment)
- If a diagram gets too complex, split it into multiple diagrams
- Always explain **how to read the diagram** directly below it

---

## Step 5: Save (Optional)

After the explanation, ask if the user wants to save it as a document.

**If yes:**
1. Ask user for save location
2. Convert ASCII diagrams to Mermaid for the saved version
3. Add metadata header (date, target, type)

**ASCII to Mermaid mapping:**

| ASCII | Mermaid |
|-------|---------|
| Component diagram | `flowchart LR` |
| Sequence flow | `sequenceDiagram` |
| State diagram | `stateDiagram-v2` |
| Timeline / progress | `gantt` |
| Hierarchy | `flowchart TD` |

---

## Core Principles

| Principle | Description |
|-----------|-------------|
| **No hallucination** | Don't know → say so. Guess → say so. Top priority. |
| **Understanding over brevity** | Good explanation = understood, not short. No length limit. |
| **High-level first** | Always start with the big picture. Overview → facets → concepts → drill-down |
| **Story + Diagram + Example** | Every explanation block includes all three |
| **Sufficiency is the measure** | Stories, diagrams, examples — as many as needed |
| **Sources first** | Gather and read sources before explaining |
| **Flexible facets** | Choose perspectives that fit the subject. No fixed template. |
