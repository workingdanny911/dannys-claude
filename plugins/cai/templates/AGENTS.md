# AGENTS.md

## Project Knowledge Base

This project uses a **CAI (Context as Infrastructure)** system.
All project knowledge is in the `context/` directory.

### Quick reference

- Project overview: context/project.md
- Architecture: context/specs/_overview.md
- Conventions: context/conventions/
- Decisions: context/decisions/
- Known issues: context/issues/
- Roadmap: context/roadmap/
- Glossary: context/glossary.md

### How to use

**Before** modifying any file, follow the CAI pre-work protocol:

1. Run `./tools/cai.py budget --task "<your task>"` to discover relevant context docs.
   - For specific file/module work: `./tools/cai.py suggest <file|dir|module>`
   - For keyword search: `./tools/cai.py search "<keywords>"`
   - For change impact analysis: `./tools/cai.py impact <file|dir|module>`
2. Read the recommended docs from `context/`.
3. Follow the full rules in `.claude/rules/cai.md`.

**During** work:

- Follow conventions in `context/conventions/`.
- Respect accepted decisions in `context/decisions/`.
- Do not worsen known issues in `context/issues/`.
- Follow patterns in `context/specs/` (check `confidence` level — `reviewed`/`verified` are authoritative, `draft`/`intent` are reference only).
- Use domain terms as defined in `context/glossary.md`.

**After** work:

- If your change contradicts an existing spec, propose an update.
- If you created a non-trivial pattern with no spec, propose documenting it.
