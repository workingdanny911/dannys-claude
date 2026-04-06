# Codebase X-Ray

Analyze famous open-source codebases and generate technical biography books that teach software engineering through real code.

## Overview

Codebase X-Ray reads an entire codebase — DOOM, Redis, Bitcoin, libuv, PostgreSQL, or any project — and produces a book-length analysis in technical biography format. The output teaches software engineering patterns and principles through real code, not textbook abstractions.

### What It Produces

- **14+ chapter book** in the user's language (auto-detected)
- Each chapter: 3,000-10,000 words with annotated code, diagrams, and anecdotes
- **📌 Explanation boxes** for terminology, analogies, and modern tech comparisons
- **📐 Design pattern boxes** mapping code to GoF patterns, SOLID principles, architecture patterns
- **Mermaid diagrams** (2+ per chapter): class, sequence, state, dependency graphs
- **Provenance tags** on every factual claim for verifiability

### Key Design Decisions

- **Analysis and writing are completely separated.** Analysis extracts facts; writing selects and narrates them. Artifact store is permanent and reusable.
- **No hallucination.** Self-verify (Layer 1) + structural audit (Layer 2). Every `code_derived` claim must have file path and line number.
- **Language-agnostic.** Works on C, Python, Rust, Go, Java, TypeScript — any language. Patterns are universal.
- **Output language follows user.** Request in Korean → Korean book. Request in English → English book.

### Generated Structure

User provides a project name (e.g., `redis`), then a root path (e.g., `~/research/redis`). Everything lives under that root:

```
{project_root}/
├── manifest.md              # Progress tracking + project info
├── source/                  # Cloned repository
├── references/              # Downloaded materials (papers, slides, images, etc.)
│   └── sources.md           # URL list + downloaded file mapping
├── checkpoints/
│   ├── phase0a.md           # Web research (author statements, anecdotes)
│   ├── phase0b.md           # Semantic anchors (worldview, discrepancies)
│   ├── phase1/{dir}.md      # Directory surveys
│   ├── phase2.md            # Module boundary synthesis
│   ├── phase4.md            # Chapter design (epistemological order)
│   ├── verify_phase3.md     # Structural audit results
│   └── verify_phase6.md     # Final audit results
├── artifacts/modules/
│   └── {module}.md          # Deep dive artifacts (reusable)
└── output/
    ├── 00-prologue.md       # Individual chapter files
    ├── 01-{chapter}.md
    ├── ...
    ├── build.sh             # Assembly script (cat + pandoc PDF)
    └── book.md              # Final assembled book
```

---

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| analyze | `codebase-x-ray:analyze` | Full pipeline: research → analysis → writing |

---

## Pipeline

```
ANALYSIS PIPELINE
  Phase 0a → Web Research (author statements, Tier 1 sources)
  Phase 0b → Semantic Anchor Extraction (worldview, discrepancies)
  Phase 1  → Directory Survey (parallel agents)
  Phase 2  → Boundary Synthesis (semantic modules)
  Phase 3  → Module Deep Dive (parallel agents) + Self-Verify
  Verifier → Structural Audit
        ↓
  ARTIFACT STORE (permanent, reusable)
        ↓
WRITING PIPELINE
  Phase 4  → Chapter Design (epistemological order)
  Phase 5  → Per-Chapter Writing (parallel agents)
  Phase 6  → Cross-chapter Review (edit in place)
  Verifier → Final Audit
        ↓
  build.sh → book.md + book.pdf
```

### Crash Recovery

`manifest.md` tracks all progress. If a session dies mid-pipeline:
1. Start a new session
2. Point to the same `output_dir`
3. Pipeline resumes from the last completed phase
4. Parallel phases (1, 3, 5) resume only missing items

### Writing-Only Re-run

To regenerate chapters without re-analyzing:
1. Delete `checkpoints/phase4.md`, `checkpoints/verify_phase6.md`, and `output/` files
2. Remove Phase 4+ entries from `manifest.md`
3. Re-run — resumes from Phase 4 using existing artifacts

---

## Usage

```
# Just give a project name — the skill asks for a root path, then clones automatically
"x-ray redis"
"DOOM x-ray해줘"

# Provide root path upfront
"x-ray redis at ~/research/redis"

# Resume interrupted session
"continue ~/research/redis"
"~/research/redis 이어서 해줘"
```

### Orchestration Model

The **main Claude Code session** is the orchestrator. It reads SKILL.md and dispatches sub-agents for each phase. Sub-agents write results directly to files and return only summaries. This keeps the main session's context clean.

For parallel phases (1, 3, 5), multiple agents run simultaneously — one per directory, module, or chapter.

---

## Verification

### Layer 1: Self-Verify
Each Phase 3 agent reads the files it cited before finishing. Unverifiable claims are removed or re-tagged as `[provenance:synthesized]`.

### Layer 2: Structural Audit
A separate Verifier agent runs after Phase 3 and Phase 6:
- Provenance tag format validation
- File existence sampling (20% of `code_derived` tags)
- Synthesized ratio monitoring (warn if >40%)
- Cross-module consistency
- Term consistency and chapter cross-references (Phase 6)

---

## References

| File | Purpose |
|------|---------|
| `references/phase0-research.md` | Web research + semantic anchor extraction |
| `references/phase1-2-survey.md` | Directory survey + boundary synthesis |
| `references/phase3-deep-dive.md` | Module deep dive + self-verify + pattern mapping |
| `references/phase4-6-writing.md` | Chapter design, writing principles, cross-chapter review |
| `references/verifier.md` | Structural audit criteria |
| `references/chapter-template.md` | Chapter structure, diagram guide, callout boxes |
| `references/artifact-format.md` | Artifact prose format + example |
