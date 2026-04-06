# Phase 0: Research & Semantic Anchor Extraction

> **Output language**: Write in the language specified in the sub-agent prompt's meta block. Keep code snippets, file paths, and technical terms as-is.

---

## Phase 0a: Web Research

### Purpose
Before reading any code, secure the "official narrative." This narrative becomes the baseline for comparison against code in Phase 0b.

### Source Types

**Tier 1 — Must read:**
- Writings authored directly by the creator (blog posts, whitepapers, presentation materials)
- Official internals/design documentation
- Primary sources explaining the project's origin story

**Tier 2 — Read selectively:**
- Commit messages (especially early commits, large-scale refactors)
- Mailing list archives
- Author interviews

**Tier 3 — Do not read:**
- Third-party code analyses/tutorials
- Introductory articles of the "How to understand X" variety

Reading Tier 3 sources degrades our analysis into merely confirming someone else's frame.

### Known Tier 1 Sources by Project

| Project | Key Sources |
|---------|-----------|
| Bitcoin | Satoshi Nakamoto whitepaper (bitcoin.org) |
| Redis | Salvatore Sanfilippo's blog (antirez.com) |
| PostgreSQL | PostgreSQL Internals official documentation |
| libuv | Bert Belder's presentation materials and interviews |
| Doom | Michael Abrash's Graphics Programming Black Book, Carmack .plan files |

### Output: `checkpoints/phase0a.md`

Write in free-form prose. Must include the following:

**Official narrative** — Why this project was born. The problem the author set out to solve, the technical and historical context of the time. Be as detailed as possible.

**Key design decisions** — Design decisions the author explicitly stated. Mark each decision with a `[provenance:author_stated source:"URL"]` tag indicating the source.

**Source list** — Tier, URL, and a summary of key insights drawn from each source.

**Unresolved questions** — Things not explained by the official narrative, things that must be verified by reading the code directly. These become the question list for Phase 0b.

---

## Phase 0b: Semantic Anchor Extraction

### Purpose
Understand the codebase's "worldview." The output of this phase is **injected as permanent context into all subsequent phases.**

This is not about exploring directory structure — it is about finding the core artifacts that reveal how this system models the world.

### What to Read

**Entry points** — `main.c`, `server.c`, `init.c`, and other execution starting points. "What does this system initialize, and in what order?" Initialization order is the most honest expression of the dependency structure.

**Core headers / core data structures** — Read `.h` files first. Data structures are the crystallization of design philosophy. Reading Redis's `server.h`, PostgreSQL's `nodes.h`, or libuv's `uv.h` reveals the types through which the system represents the world.

**Command/dispatch table** — Redis's `commands` array, PostgreSQL's plan node switch statement. "The surface area this system exposes to the outside world." The list of supported operations is the system's identity.

**Build system** — `Makefile`, `CMakeLists.txt`, `configure.ac`. What depends on what. The dependency graph is the most objective hint of module boundaries.

### Cross-referencing with Phase 0a

When reading each Semantic Anchor, cross-reference it against Phase 0a's official narrative:
- Does the design intent stated in the official narrative actually manifest in the code?
- If there is a discrepancy, where exactly does it diverge?

A discrepancy is not a bug. It is a trace of design evolution, evidence of a pragmatic compromise, or a moment where intentions were good but reality differed. These make for the most compelling chapter material in the book.

### Output: `checkpoints/phase0b.md`

Write in free-form prose. Must include the following:

**This system's worldview** — In one paragraph. "How does this system model the world?" This paragraph is injected first into every subsequent phase agent.

**Semantic Anchors** — Describe the discovered core artifacts in detail. For each anchor, explain the file path, line number, and the design philosophy it reveals. `[provenance:code_derived file:path:line]` tags are required.

**Official narrative vs code discrepancies** — Record every discovered discrepancy exhaustively. For each, describe the nature of the discrepancy (intentional evolution, documentation error, or an interesting tension), the related files, and what the discrepancy means for understanding the system.

**Caveats for Phases 1-3** — Things in this system's directory structure or naming conventions that are easy to misunderstand. Traps that subsequent agents might fall into.
