# Phase 3: Module Deep Dive

> **Output language**: Write in the language specified in the sub-agent prompt's meta block. Keep code snippets, file paths, and technical terms as-is.

### Purpose
Deeply analyze each module to produce artifacts that serve as raw material for the Writing Pipeline. The output of this phase determines the book's content. Depth is quality.

### Required Context

This analysis requires:
- **Author statements/design decisions** from Phase 0a (to directly connect with code)
- The **worldview paragraph** from Phase 0b
- The complete **official narrative vs code discrepancies** from Phase 0b
- The module's **raison d'être, file list, and interface information** from Phase 2

### Analysis Items

**1. Why Does This Module Exist**

Start from Phase 2's one-sentence summary and expand with concrete historical and technical context. If Phase 0a contains author statements, connect them directly. Imagining "what would happen if this module didn't exist" makes the reason for existence sharper.

**2. Core Data Structures**

Select 2-4 important structs/types. Selection criteria:
- Best reveals this module's worldview
- Most frequently referenced
- Whose field composition itself embodies design decisions

Analyze each data structure in depth:
- What real-world concept does it model
- Why this field composition — the meaning of fields that **are** present AND the meaning of fields that **are not**
- If this type has evolved (cross-version changes, comments as reference), how has it evolved

`[provenance:code_derived file:path:line]` tags are required.

**3. Core Algorithms/Execution Flows**

Trace the execution flow of 2-4 key functions. Not simply "this function does X" but rather:
- Why does it execute in this order
- What case does each branch handle
- What invariant does it try to maintain
- Where does it sacrifice correctness for performance, or vice versa

**4. Boundary**

State explicitly what this module knows and does not know. "What it does not know" is especially important — what is intentionally delegated externally reveals the module's design philosophy.

Example: libuv's Event Loop knows "when an I/O event occurs" but does not know "what to do with that event." This boundary is libuv's core abstraction.

**5. Trade-offs**

What this design gave up and what it gained. This is the chapter's climax. State explicitly in the form "gave up A, gained B," and find evidence in the code.

Examples of good trade-off analysis:
- Redis Event Loop: "Gave up multi-core utilization, gained simplicity and predictable latency. Evidence: ae.c's setsize parameter is a file descriptor count, not a concurrent thread count."
- Doom BSP: "Gave up runtime map modification flexibility, gained O(1) rendering order determination. Evidence: maps ship as BSP-compiled .wad files."

**6. Deepening Official Narrative Discrepancies**

Directly verify in code the discrepancies related to this module from Phase 0b, and analyze them more deeply. Formulate hypotheses about why the discrepancy occurred, and find evidence in the code that validates or refutes each hypothesis.

**7. Cross-references**

Relationships with other modules that carry design significance beyond simple dependency. Example: libuv's Thread Pool is the Event Loop's "philosophical compromise" — the point where a pure async model breaks down in the face of CPU-bound work.

**8. Software Engineering Pattern/Principle Mapping**

Identify **design patterns, architecture patterns, and software engineering principles** found in this module and connect them to code. These patterns operate clearly even in C code — even if the language is not OO, the design thinking can be OO.

Below is a **reference list** of identification targets. Look for what fits the project's language and era, but also record any patterns you discover that are not on this list.

**Design Patterns (GoF etc.)**
Strategy, Command, State, Observer, Object Pool, Flyweight, Facade, Iterator, Template Method, Adapter, Builder, Factory, Singleton, Decorator, Proxy, Chain of Responsibility, Mediator, Visitor ...

**Architecture Patterns**
Layered Architecture, Data-Driven Design, Plugin Architecture, Event Loop, Pipe and Filter, Microkernel, MVC/MVP/MVVM, Repository, CQRS, Actor Model, Deterministic Simulation, ECS (Entity-Component-System) ...

**Principles and Disciplines**
SOLID (SRP, OCP, LSP, ISP, DIP), Separation of Concerns, Information Hiding, Fail Fast, Convention over Configuration, Composition over Inheritance, Law of Demeter, DRY, YAGNI, Tell Don't Ask, Principle of Least Surprise ...

When identifying each pattern/principle:
1. **State the pattern name** and its standard definition
2. **Point to the implementation in code** specifically (file, line, type, function)
3. **Why this pattern** — if alternative interpretations are possible, explain why this pattern is a better fit
4. **Language-specific implementation techniques** — how is this pattern expressed in the project's language
   - C: function pointers, struct puns, macros, opaque pointers
   - Python: duck typing, decorators, metaclasses, protocols
   - JavaScript/TypeScript: closures, prototype chains, module patterns
   - Rust: traits, enum dispatch, lifetimes, ownership
   - Go: interfaces, goroutines/channels, embedding
   - Java/Kotlin: interfaces, abstract classes, annotations
   - etc. — analyze according to the project's language

**Caveats — Hallucination Prevention:**
- Not every pattern exists in every module. Record **only what is actually found** in the module.
- Do not force-fit. Do not assert a pattern without clear evidence in the code.
- **Do not fabricate patterns or principles that do not exist.** Use only standard nomenclature. If unsure of the name, it is better to describe it as "this code employs a design technique that ~."
- Some modules may yield zero patterns. That is fine — "none found" is better than "forced matching."

### Output: `artifacts/modules/{module}.md`

Free-form prose + provenance tags. See `references/artifact-format.md` for format.

No length limit. The more you write, the richer the raw material for the Writing Pipeline.

---

## Self-Verify

After analysis is complete, perform this before declaring done:

1. Identify all `[provenance:code_derived]` claims in this artifact.
2. **Open and verify** the file and line specified in each claim.
3. On discrepancy:
   - Find the correct location and fix the tag, or
   - If unverifiable, remove the claim or change it to `[provenance:synthesized]`.
4. Append a verification summary at the end of the artifact:

```
## Self-Verify Summary
- code_derived claims: {N} verified
- Tags corrected: {N}
- Claims removed: {N}
```

An artifact returned without self-verify will be flagged as a warning by the Verifier.
