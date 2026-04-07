# Verifier: Structural Audit

> **Output language**: Write in the language specified in the sub-agent prompt's meta block. Keep code snippets, file paths, and technical terms as-is.

---

## Role

This Verifier performs a **structural audit**. Verification of individual `code_derived` claims at the file/line level is the responsibility of Phase 3 sub-agent's self-verify. The Verifier checks whether self-verify was properly performed and whether there are any issues with the overall structure.

---

## Two-Pass Architecture

The audit is split into two passes to enable parallel execution:

- **Pass 1 (Per-Artifact)**: Items that can be checked independently per artifact/chapter. Run in parallel batches.
- **Pass 2 (Cross-Cutting)**: Items that require visibility across all artifacts/chapters. Run as a single agent after Pass 1 completes.

Pass 2 runs after all Pass 1 HARD_FAILs have been resolved (re-run + re-verify loop). By the time Pass 2 starts, all artifacts/chapters have passed Pass 1.

---

## Pass 1: Per-Artifact Audit

Each batch receives a subset of artifacts and checks items 1–5 independently.

### 1. Provenance Tag Format Validation

- Are all tags in the correct format:
  - `[provenance:code_derived file:{path}:L{number}]`
  - `[provenance:author_stated source:"{source}"]`
  - `[provenance:synthesized]`
- Does `code_derived` have both a file path and line number (not just format, but presence of both)
- Does `author_stated` have a source

### 2. Tag Completeness

- Are there factual claims missing tags
- Subjective interpretations or structural explanations do not require tags
- Specific facts like "this function does X" or "this field stores Y" must have tags

### 3. Synthesized Ratio

- Calculate the `synthesized` tag ratio per artifact
- **Warning if over 40%**: signals insufficient code-based analysis
- Artifacts with a high ratio likely need more code reading

### 4. File Existence Check (Sampling)

- Not a full audit but **sampling**: randomly select 20% of `code_derived` tags
- Verify that the referenced files actually exist in the repo
- If non-existent files are found in the sample, request re-verification of all `code_derived` tags in that artifact

### 5. Self-Verify Summary Check

- Does each Phase 3 artifact have a self-verify summary at the end
- Artifacts without a summary are assumed to have skipped self-verify and receive a warning

### Pass 1 Output

Render the result **per artifact** as one of:

**PASS** — No issues found for this artifact.

**WARN** — Minor issues found. List them. The artifact may proceed to Pass 2.
- Examples: synthesized ratio between 35-40%

**HARD_FAIL** — Critical issues found. List the specific problems.
- Examples: mass-missing provenance tags, numerous non-existent files in sampling, self-verify not performed

The batch-level verdict is the worst verdict among its artifacts. Include the per-artifact breakdown.

---

## Pass 2: Cross-Module Audit

Runs as a single agent after all Pass 1 HARD_FAILs have been resolved. All artifacts are included.

### 6. Cross-Module Consistency

- Are multiple artifacts describing the same file or struct differently
- Are inter-module dependency descriptions bidirectionally consistent (if A→B is described, B should also mention its relationship with A)

### Pass 2 Output

Render the result as one of:

**PASS** — No cross-module issues. Proceed to the next phase.

**WARN** — Minor inconsistencies found. List them. May proceed.

**HARD_FAIL** — Significant inconsistencies. List the affected artifact pairs with specific reasons.

---

## Additional Audit After Phase 6

At the Phase 6 final audit, the two-pass structure applies with expanded scope.

Pass 1 checks items 1–4 from the base audit (item 5 does not apply — chapters have no self-verify summary) **plus** item 9 below. Pass 2 checks items 7–8 below, plus item 6 from the base audit at the chapter level.

### Pass 1 (Per-Chapter): Items 1–4 + Item 9

#### 9. New Claims Added During Writing

- Have factual assertions appeared in chapters that were not in the artifacts
- Do newly added claims have appropriate provenance tags
- Specifically scrutinize technical claims the Writing agent added ad hoc

### Pass 2 (Cross-Chapter): Items 7–8

#### 7. Terminology Consistency

- Is the same concept being called different names across chapters
- Especially module names, core data structure names, and design pattern nomenclature

#### 8. Cross-Chapter Reference Verification

- Do references like "X, which we examined in Chapter N" actually exist in that chapter
- Are there any broken references

Pass 2 also re-checks items from the base audit (item 6) at the chapter level.

---

## Output

Each pass renders its own verdict. The **overall verdict** for the verification step is determined by:

1. If any Pass 1 artifact has HARD_FAIL → address those first (re-run Phase 3/5 for affected modules/chapters, then re-run Pass 1 for them)
2. Once Pass 1 clears → run Pass 2
3. The final verdict is Pass 2's verdict (which subsumes Pass 1 results)

Verdict definitions:

**PASS** — No structural issues. Proceed to the next phase.

**WARN** — Attach a list of minor issues. May proceed to the next phase, but issues are recorded.
- Examples: synthesized ratio between 35-40%, minor terminology inconsistencies

**HARD_FAIL** — Present the list of artifacts/chapters requiring rework with specific reasons.
- Examples: mass-missing provenance tags, numerous non-existent files found in sampling, self-verify not performed
