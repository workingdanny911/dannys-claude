# Coding Guidelines

Guidelines for software development backlog items.

## Task Breakdown Considerations

### What makes a good coding Task?
- One API endpoint or route
- One component or module
- One bug fix (specific, isolated)
- One test suite for a specific feature
- One refactoring target (one file or one pattern)

### What's too big?
- "Implement the entire authentication system" → Break into login, signup, password reset, etc.
- "Add all API endpoints" → One endpoint per Task
- "Write all tests" → Tests per feature/module

## Quality Checklist

When adding coding tasks, consider:

- [ ] Is the task testable?
- [ ] Are acceptance criteria clear?
- [ ] Are dependencies identified?
- [ ] Is the scope well-defined?

## Type-Specific Fields

For coding Features, consider adding:

```markdown
**Tech Stack**: [relevant technologies]
**Testing**: Unit | Integration | E2E
**Dependencies**: [external libs, APIs]
```

## Reference

For testing guidelines, see: `project-init/assets/coding/testing-guidelines.md`
