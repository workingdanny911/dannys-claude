# Phase 1-2: Directory Survey & Boundary Synthesis

> **Output language**: Write in the language specified in the sub-agent prompt's meta block. Keep code snippets, file paths, and technical terms as-is.

---

## Phase 1: Directory Survey

### Purpose
Identify the role of each top-level directory. This phase is preparatory work for discovering semantic module boundaries. **Directory boundary ≠ module boundary**. Always keep this in mind during analysis.

### Required Context

This analysis requires:
- The **worldview paragraph** from Phase 0b
- The **caveats for Phases 1-3** from Phase 0b
- The assigned directory path

### What to Analyze

**Role of this directory** — Start with one sentence, but explain sufficiently. Not simply "networking code" but rather "handles everything from client connection establishment to request parsing and response serialization, delegating actual I/O multiplexing to ae.c."

**Key files** — The 3-5 most important files. Selection criteria: most frequently referenced, or contains the core abstractions of this directory. For each file, explain why it is key and what concepts it encapsulates. `[provenance:code_derived file:path:line]` tags.

**Dependency relationships** — What does this directory depend on, and what depends on this directory? Describe both direction and rationale.

**Oddities and interesting findings** — Files whose role differs from their name, unexpected dependencies, aspects that conflict with the Phase 0b worldview. Never omit this section. It is not "none" — actively search for them.

### Output: `checkpoints/phase1/{dirname}.md`

Free-form prose. Include all four items above, but do not be constrained by format. The more information, the higher the quality of Phase 2 Boundary Synthesis.

---

## Phase 2: Boundary Synthesis

### Purpose
Consolidate all Phase 1 reports to identify **semantic module boundaries**. These become the units for Phase 3 Deep Dive and the foundation of the book's chapter structure.

### What Is a Semantic Module

Not a directory boundary, but a **boundary of responsibility**.

Criteria for a good module boundary:
- Does it have a single raison d'être
- High cohesion within the boundary — are things that change together in the same module
- A clear interface to the outside of the boundary

Example — the case of Redis:
```
Directory-based (incorrect decomposition):
  src/networking/, src/server.c, src/ae.c, src/t_*.c ...

Semantic modules (correct decomposition):
  Event Loop      ← ae.c + platform-specific implementations (multiple files, one responsibility)
  Command Engine  ← parts of server.c + commands.c
  Data Model      ← t_string.c, t_list.c, t_hash.c ... (multiple files)
  Persistence     ← rdb.c, aof.c
  Replication     ← replication.c
  Networking      ← networking.c + connection abstraction
```

### Analysis Procedure

Synthesize all dependency information from Phase 1 and mentally construct a connectivity graph. Strongly connected component clusters are module candidates. For each cluster:

1. Can you write "the raison d'être of this cluster in one sentence"? If not, further decomposition is needed.
2. Do the files within the cluster actually change together? Refer to commit history if available.
3. Is the cluster's external interface clear?

### Output: `checkpoints/phase2.md`

Write in free-form prose. Must include the following:

**Identified module list** — For each module:
- Name
- Raison d'être in one sentence
- Included files
- Key interfaces exposed externally
- Notable relationships with other modules

This list becomes the sub-agent execution plan for Phase 3.

**Insights on dependency structure** — Structural patterns discovered in the overall module graph. Which module is the central hub, are there surprising dependencies, and how does this structure reveal the system's design philosophy.

**Connection to Phase 0b discrepancies** — How do the official narrative vs code discrepancies found in Phase 0b manifest in the module boundary analysis? Pay particular attention to cases where unexpected module boundaries are either the cause or consequence of a discrepancy.
