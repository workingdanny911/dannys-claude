# Changelog

All notable changes to the sprint plugin templates.

Format: [Keep a Changelog](https://keepachangelog.com/)
Versioning: [Semantic Versioning](https://semver.org/)

- **Major**: Breaking changes to file structure
- **Minor**: New sections, updated rules
- **Patch**: Typo fixes, clarifications

---

## [1.3.0] - 2025-02-08

### Changed

- **Mandatory review before done**: Tasks must go through `review` status before `done`. Agents can no longer skip directly to `done`.
- **Completing a Task**: Renamed "Definition of Done" to "Self-Check". Steps now require `review` status, reporting to user, and requesting review.
- **HANDOFF.md flow**: Task completion moves to "In Review" (not "Recently Done").
- **Agent Session Lifecycle**: "Complete" step renamed to "Mark Review" in CONCEPTS.md.
- **Status descriptions**: `review` marked as mandatory step; `done` clarified as "User reviewed and approved".

### Added

- **Handling Review Tasks** section in INSTRUCTION-TEMPLATE.md: Defines agent behavior when encountering `review` tasks — explain work in detail, request user review, act on user decision (approve → done, request changes → improve).
- **Phase 3.5 User Review** in WORKFLOW-GUIDE.md: Documents the user review flow with examples.
