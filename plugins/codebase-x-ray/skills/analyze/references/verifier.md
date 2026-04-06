# Verifier: Structural Audit

> **Output language**: Write in the language specified in the sub-agent prompt's meta block. Keep code snippets, file paths, and technical terms as-is.

---

## Role

This Verifier performs a **structural audit**. Verification of individual `code_derived` claims at the file/line level is the responsibility of Phase 3 sub-agent's self-verify. The Verifier checks whether self-verify was properly performed and whether there are any issues with the overall structure.

---

## Audit Items

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

### 6. Cross-Module Consistency

- Are multiple artifacts describing the same file or struct differently
- Are inter-module dependency descriptions bidirectionally consistent (if A→B is described, B should also mention its relationship with A)

---

## Additional Audit After Phase 6

At the Phase 6 final audit, inspect the following in addition to the items above:

### 7. Terminology Consistency

- Is the same concept being called different names across chapters
- Especially module names, core data structure names, and design pattern nomenclature

### 8. Cross-Chapter Reference Verification

- Do references like "X, which we examined in Chapter N" actually exist in that chapter
- Are there any broken references

### 9. New Claims Added During Writing

- Have factual assertions appeared in chapters that were not in the artifacts
- Do newly added claims have appropriate provenance tags
- Specifically scrutinize technical claims the Writing agent added ad hoc

---

## Output

Render the result as one of the following verdicts:

**PASS** — No structural issues. Proceed to the next phase.

**WARN** — Attach a list of minor issues. May proceed to the next phase, but issues are recorded.
- Examples: synthesized ratio between 35-40%, minor terminology inconsistencies

**HARD_FAIL** — Present the list of artifacts/chapters requiring rework with specific reasons.
- Examples: mass-missing provenance tags, numerous non-existent files found in sampling, self-verify not performed
