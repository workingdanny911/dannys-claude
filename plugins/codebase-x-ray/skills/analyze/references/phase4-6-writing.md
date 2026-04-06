# Phase 4-6: Writing Pipeline

> **Output language**: Write in the language specified in the sub-agent prompt's meta block. Code snippets, file paths, and technical terms remain as-is.

---

## Phase 4: Chapter Design

### Purpose
Read the entire Artifact Store and determine the book's **epistemological order**. This is not a table of contents. It is the order in which the reader builds understanding.

A good chapter order means: concepts required to understand later chapters always appear earlier, there is a narrative flow throughout, and the most critical design decisions are positioned near the mid-point climax.

### Chapter Types

**Prologue** (required)
Why was this project born? What problem was it trying to solve? What can the reader gain from this book?

**Module Chapters**
Rearrange Phase 2's module list in epistemological order. Not simply by importance, but so that each preceding chapter prepares the reader to understand the next.

**Official Narrative vs Reality Chapter** (optional)
If any discrepancies discovered in Phase 0b/3 are significant and interesting enough, give them a standalone chapter. This becomes the book's most original content.

**Epilogue** (required)
How did this project's design decisions influence subsequent systems? What is the significance of this codebase in the history of software engineering?

### Output: `checkpoints/phase4.md`

**Chapter order and rationale** — Explain why this order was chosen. Describe inter-chapter dependencies and narrative flow.

**Per-chapter plan** — For each chapter:
- Title (a narrative title. Not "Event Loop" but "How a single thread handles the world")
- Narrative role of this chapter — What the reader understands after finishing it
- List of artifacts to use
- Concepts carried forward from the previous chapter, concepts handed off to the next
- Climax point — The chapter's most critical trade-off or insight

---

## Phase 5: Per-Chapter Writing

### Purpose
Write each chapter as actual book text.

### Required Context

The following are needed to carry out this writing:
- Phase 0b's **worldview paragraph**
- Phase 4's **plan for the current chapter**
- Phase 4's **full chapter order** (for understanding preceding and following context)
- **Artifacts** to be used in the current chapter

### Writing Principles

**Audience: A developer who wants to study the code, reading on their phone during a commute**
**Fun and understanding** take priority over academic depth. The reader has programming experience but is encountering this codebase for the first time. They read in spare moments as a hobby, so sections must not run long, and they should be able to pick up where they left off.

**Technical biography style + reading enjoyment**
You are not explaining code — you are narrating the life of this system. Unfold the moments when design decisions were made, when constraints became philosophy, when compromises were struck — **like a story**. Not dry analysis, but writing that makes the reader think "wow, that's how they thought about it."

**Code snippets must include comments in {output_language}**
Do not leave readers to decode code on their own. Add comments in {output_language} on key lines explaining "what this line does":

```c
// The start of Zone memory. Receive one massive block from the OS.
// From this moment on, DOOM never calls the OS's malloc again.
mainzone = (memzone_t *)I_ZoneBase(&size);
mainzone->size = size;  // Record the total size of this pool
```

Before and after code blocks, always explain in {output_language} "why this code matters" and "what the key point is here."

**"Why it's remarkable" first, code second**
Awe → code → understanding. First explain "why this is surprising" using contrasts with modern technology or analogies, then show the code, then after seeing the code, summarize "how this was made possible."

Bad order: Code → explanation → "Impressive, right?"
Good order: "Modern apps eat 8GB of RAM, but DOOM ran hell in 4MB." → code → "These 300 lines made that possible."

**Actively use anecdotes and episodes**
Human stories about the developers bring the technology to life:
- Carmack's 28-hour coding marathon
- The PU_DAVE tag (the moment Dave Taylor's name became fossilized in the code)
- Community reaction after the source was released
- Wrestling with the hardware constraints of the era

Insert anecdotes naturally at chapter openings or during trade-off explanations.

**Analogies and modern technology contrasts**
Connect abstract concepts to the reader's experience:
- "Zone Memory is like a private bank. After borrowing a large sum once from the central bank (the OS), it manages lending and reclamation internally."
- "A BSP tree is like a librarian. Once organized, any book can be found instantly."
- "What today's GPUs do, in 1993 the CPU had to do alone."

**Short paragraphs, many subheadings**
Break after 3-4 sentences. The more subheadings the better. The text should be easy to skim while scrolling. Cover only one idea per subheading.

**Trade-offs are the climax**
Each chapter builds toward its core trade-off. But deliver trade-offs **as stories**: "Carmack chose A. The cost was B. But that cost actually made C possible."

**Teach software engineering patterns and principles**
This book is not a code manual — it is **software engineering education through code**. When you discover design patterns, architecture patterns, or SOLID principles in the code, teach the reader using `> **📐 Design Pattern — {name}**: ...` callout boxes.

Key principles:
- Design patterns and engineering principles are at work in code of any language
- The goal is to help readers "recognize this pattern in other code"
- Pattern name + "why this code is that pattern" + "how it looks in other languages/frameworks"
- How this pattern was implemented using (or working around) features of the language is an interesting point
- 2-5 📐 boxes per chapter. Do not force-fit them.

**Diagrams are mandatory, not optional**
At least **2** Mermaid diagrams per chapter. Place diagrams before the text explanation so the reader sees the picture first. Diagram types to use:
- **Data structure relationships** (`graph TD/LR`) — relationships between structs, field-level connections
- **Execution flow** (`sequenceDiagram`) — function call order, inter-module interactions
- **State transitions** (`stateDiagram-v2`) — state machines, game state changes
- **Class/module diagrams** (`classDiagram`) — module structure, interface relationships, inheritance/implementation (express logical relationships even in non-OO languages)
- **Dependency/hierarchy** (`graph TD`) — dependency direction between modules, layer structure
- **Memory layout** (`graph LR`) — physical memory arrangement

For detailed guidelines and examples, see `references/chapter-template.md`'s "Diagram Guide."

### Output: `output/{NN}-{chapter}.md`

Completed chapter text. Markdown + Mermaid diagrams. No length limit.
NN is the chapter sequence number (00, 01, 02, ...). The numeric order of filenames is the chapter order.

---

## Phase 6: Cross-chapter Review

### Purpose
Review and **edit** all chapters. Physical assembly is handled by build.sh, so this phase focuses purely on editing.

### Review Checklist

**Narrative continuity** — Are the seams between chapters natural? Are concepts foreshadowed in earlier chapters adequately covered later? Are there unnecessary repetitions or broken connections?

**Terminology consistency** — Is the same concept being called different names across chapters?

**Cross-chapter references** — Naturally add references like "The Event Loop we explored in Chapter 4 reappears here."

**Final provenance tag check** — Are there any claims missing tags?

### Editing Approach

When issues are found, **edit the chapter file directly**. Chapter files exist independently as `output/{NN}-{chapter}.md`. After editing, run build.sh to regenerate book.md.

### Output

Edits to each chapter file + a review summary.
