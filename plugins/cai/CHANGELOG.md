# Changelog

## [0.3.0] - 2026-04-07

### Improved — Confidence Pipeline
- verification-agent now recommends confidence promotion based on verification results (draft → verified/reviewed)
- Removed "NEVER higher than draft" constraints from spec-writer and module-analyst
- cai-onboard E3 automatically applies promotion recommendations after verification
- cai-add-spec Step 5 applies verification-agent's recommended confidence level

### Improved — Spec Depth
- Signatures table: exported functions now require parameter types and return types
- Data Model section: entity/aggregate fields, types, and constraints
- Behavioral Flow: numbered call-chain level descriptions replacing summary-level "Key Behaviors"

### Improved — Tag Generation
- Minimum 5 meaningful tags required per spec (domain, functional, technology, Korean synonyms)
- `auto-generated` tag prohibited — causes search noise across all CLI commands

### Improved — CLI Search Quality
- budget: added body content matching (0-4 points), reusing existing `find_by_content` logic
- budget: confidence weight expanded (verified=5, reviewed=3, draft=0, intent=-1)
- budget: draft penalty multiplier (×0.6) reduces noise from unverified docs
- budget: issue type_score 1→3, roadmap type_score 0→2
- budget: graph expansion follows `depends_on`/`related_specs` links from high-relevance docs (cross-cutting support)
- search: score < 2 results filtered out as noise
- suggest: stop-tag filtering prevents generic tag snowball expansion
- All commands: STOP_TAGS filter excludes "auto-generated", "generated", "draft" from tag scoring

### Added — Module Relationships Spec
- relationship-mapper now generates `context/specs/_relationships.md`
- Dependency graph, inter-module data flows (types/events/calls), and cross-cutting scenarios
- Enables budget graph expansion to surface related modules for cross-module tasks

### Improved — cai-upgrade
- Now reads CHANGELOG.md and presents version changelog before applying updates
- Post-upgrade summary includes Upgrade Notes

### Upgrade Notes
- Run `cai-upgrade` to update agents, skills, and cai.py
- Existing context documents are unchanged (backward compatible)
- To benefit from confidence promotion, re-verify existing specs via `cai-onboard --incremental` or `cai-drift-check`
- To generate `_relationships.md` for existing projects, run `cai-onboard --incremental`

## [0.2.0] - 2026-03-28

- Replaced context-interviewer agent with interview skill
- Added cai.py CLI tool

## [0.1.0] - 2026-02-15

- Initial release
