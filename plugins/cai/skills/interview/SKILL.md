---
name: interview
description: "Use when gathering information from the user through conversational dialogue — onboarding context collection, spec scope clarification, decision rationale gathering. Triggers: 'interview', 'cai-interview'"
---
# CAI Interview

## Overview

A conversational skill for extracting knowledge from the user that code analysis cannot reveal. **The main agent runs this directly** and MUST NOT dispatch it as a subagent — doing so severs the user's conversational context.

Other cai skills (`cai-onboard`, `cai-add-spec`, `cai-add-decision`, `cai-add-roadmap`, etc.) delegate to this skill whenever they need user input.

## When to Use

- `cai-onboard`: After automated analysis, collect human-only knowledge (vision, decision rationale, future plans, unwritten conventions).
- `cai-add-spec`: When spec scope or intent is ambiguous, clarify with the user.
- `cai-add-decision`: Gather rationale, alternatives, trade-offs.
- `cai-add-roadmap`: Gather motivation and priority.
- Any other cai workflow that needs user input.

## Inputs (from caller)

The calling skill must specify before the interview begins:

1. **Goal** — What you are trying to learn (e.g., "project vision and target users").
2. **What is already known** — Drafts from automated analysis, facts found in code. Prevents asking what you already know.
3. **Output target** — Which file(s) the answers will land in.
4. **Optional seed questions** — A suggested question flow. Not required.

## Core Principles

> HARD RULE: The main agent runs the interview directly. Never dispatch a subagent via Task — interviews only make sense inside the current user conversation.

- **One question per message** — Never list multiple questions in one message. Users get overwhelmed and answer carelessly. If a topic needs more depth, split it into follow-ups.
- **Multiple choice preferred** — Use `(a) (b) (c)` format whenever possible. Reserve open-ended questions for genuinely open prompts (e.g., "What are you building?").
  - Bad: "What is the goal of this project?"
  - Good: "What kind of project is this? (a) internal tool (b) SaaS (c) open source (d) other"
- **Show what you found, then confirm** — "Git history suggests these decisions: [list]. Are they correct?" Present discoveries first, then ask for confirmation.
- **Incremental capture** — As soon as you receive an answer, write it to the relevant file, then move on. Do NOT batch answers and write at the end.
- **Accept short answers** — "yes", "no", "b", "2" are all valid. Do not demand longer responses.
- **Move on immediately** — If the user says "don't know" / "skip" / "none", advance to the next question. No insistence.
- **Be flexible** — Reorder or drop prepared questions when answers point elsewhere. Conversation flow beats script.
- **YAGNI ruthlessly** — Short answer means stop digging. Collect the minimum necessary.
- **No artificial cap** — There is no fixed question limit. Ask exactly what the goal needs and no more.
- **Follow the user's language preference** — Conduct the interview in whatever language the user is currently using with you (or as configured in their preferences). Do not hardcode a language. Match their choice every turn.

## Anti-Patterns (forbidden)

| Anti-Pattern | Why It's Bad |
|---|---|
| Listing several questions in one message | User is overwhelmed; most get ignored or answered carelessly. |
| "Tell me about your project" | Too broad. User doesn't know where to start. |
| Long summaries echoed back after each answer | Token waste. The user knows what they said. |
| Explaining "why I'm asking this" with every question | Just ask. |
| Re-confirming earlier answers | "You said SaaS earlier, right?" — wastes time. |
| Asking about things automated analysis already knows | If you have it from analysis, just confirm — don't re-ask. |
| Dispatching the interview as a subagent | Breaks user context. Never do this. |

## Process

1. **Frame** (one message) — Briefly state the goal and expected scope. Not a question.
   - Example: "Code analysis found N modules and M decisions. Now I'll ask a few things code can't tell me."
2. **Ask → Wait → Capture → Next** loop:
   - One question → wait for answer → immediately update the target file → next question.
3. **Stop when done** — When the caller's stated goal is satisfied, stop. An optional final "anything else?" is allowed once.
4. **Hand back** — Return the collected answers and the list of files created/updated to the calling skill.

## Knowledge Only Humans Can Provide

| Knowledge Type | Why Code Can't Tell Us | Typical Target |
|---|---|---|
| Decision rationale | Git shows *what*, not *why* | `context/decisions/*.md` |
| Project vision | No code artifact captures long-term goals | `context/project.md` |
| External constraints | Compliance, SLA, budget — not in code | `context/project.md` / `issues/` |
| Future plans | Plans exist before code | `context/roadmap/` |
| Domain terminology | Business language ≠ code naming | `context/glossary.md` |
| Team conventions (unwritten) | Not yet codified | `context/conventions/` |
| Spec scope/intent | User intent is invisible in code | spec frontmatter / body |

## Constraints

- If the caller has not specified where answers will be written, ask the caller to clarify before starting.
- Do NOT fabricate answers when the user declines. Leave the field empty or remove the section.
- When user statements conflict with auto-generated drafts, **the user wins**.
- No code modifications during the interview. Only context document updates.
