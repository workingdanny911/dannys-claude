# Decisions

Decision records for features and sprint-wide.

## Files

| File | Purpose |
|------|---------|
| `_sprint.md` | Sprint-wide decisions (rare, cross-feature) |
| `F{n}-{name}.md` | Feature-specific decisions |

## Naming Convention

- `_sprint.md` - Sprint-wide (created by sprint-init)
- `F{n}-{feature-name}.md` - Per-feature (e.g., `F1-user-auth.md`)

## When to Create

**Feature file**: When a feature is **completed**, move decisions from `active/F{n}-*.md` here.

**Sprint file**: Only for decisions that affect multiple features or the entire sprint.

## Template

```markdown
# F{n}: {Feature Name} - Decisions

| Decision | Rationale | Date |
|----------|-----------|------|
| Use JWT for auth | Stateless, scales well | 2024-01-28 |
```
