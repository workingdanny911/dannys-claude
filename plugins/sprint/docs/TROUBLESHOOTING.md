# Sprint Plugin - Troubleshooting Guide

## Common Issues

### Q: Says it can't find Sprint files

**Symptom**:
```
Sprint not detected.
```

**Cause**:
- BACKLOG.md, HANDOFF.md not in current directory
- Wrong path

**Solution**:
```
# 1. Check Sprint location
ls sprints/

# 2. Navigate to correct path
cd sprints/my-sprint/

# 3. Or specify path directly
/sprint:add-backlog
> Which sprint? (enter path)
sprints/my-sprint/
```

---

### Q: Task is too large to complete in one session

**Symptom**:
- Context compaction occurs during session
- Work gets interrupted

**Cause**:
- Task size too large

**Solution**:

1. **Mark current Task as blocked**
   ```markdown
   - [ ] T1.1: Big Task `blocked` → needs breakdown
   ```

2. **Break down with /sprint:plan-backlog**
   ```
   /sprint:plan-backlog T1.1

   → Break into Sub-tasks
   - [ ] T1.1.1: Part 1
   - [ ] T1.1.2: Part 2
   - [ ] T1.1.3: Part 3
   ```

3. **Task sizing guide**
   - Explainable in 2-3 sentences? → Good
   - Needs a paragraph? → Too Big

---

### Q: Multiple agents modified the same file

**Symptom**:
- BACKLOG.md content conflict
- Other agent's changes overwritten

**Cause**:
- Concurrent modification
- Didn't check latest version

**Solution**:

1. **Re-read file immediately**
   ```
   Re-check BACKLOG.md, HANDOFF.md
   ```

2. **Re-apply only your changes**
   - Restore other agent's content
   - Add only your changes

3. **Prevention**
   - Modify only your area (assigned Task, your row)
   - Always read latest version before modifying

---

### Q: Lost track of work after context compaction

**Symptom**:
- Claude suddenly forgets work content
- Asks "What were we doing?"

**Cause**:
- Context compaction in long session

**Solution**:

```
# Recovery order
1. Read INSTRUCTION.md (guidelines)
2. Read BACKLOG.md (find my Task)
3. Read HANDOFF.md (current status)
4. Read active/F{n}-*.md (work context) ← Key!

# Verify
- Maintain same agent name
- Continue in-progress Task
- Do NOT claim new Task
```

**Prevention**:
- Update `active/` files frequently
- Record important decisions immediately in `refs/decisions/`

---

### Q: How do I clean up a completed Feature?

**Solution**:

```markdown
# 1. Archive active context
active/F1-*.md → refs/archive/F1-auth.md (move as-is)

# 2. Add Lessons Learned section to archived file
# 3. Finalize Decisions Made section in archived file
# 4. Sprint-wide insights only → refs/decisions/_sprint.md or refs/lessons/_sprint.md

# 5. Clean BACKLOG.md
# Remove Feature section, add one-line to Done:
- F1: Authentication - completed 2024-01-28
rm active/F1-authentication.md
```

---

### Q: Plan file not referenced in next session

**Symptom**:
- After Plan approval and starting work, Plan content is unknown

**Cause**:
- Plan file lacks sufficient context

**Solution**:

Plan file must include:

```markdown
# Sprint Context (REQUIRED)
- Sprint Path: sprints/my-sprint/
- Feature: F1
- Task: T1.2
- Files to Reference:
  - refs/designs/F1-feature.md
  - src/services/auth.ts

# Work Context
Current state: ...
Decisions from previous Task: ...
```

### Q: Agent doesn't adopt persona personality

**Symptom**:
Agent starts a session but doesn't follow persona guidelines.

**Cause**:
- `personas/` directory doesn't exist in the sprint
- Persona file name doesn't match agent name (e.g., `#rook` needs `personas/rook.md`)
- Sprint was created before persona system was added

**Solution**:
1. Check if `personas/` directory exists in your sprint
2. Verify file name matches: `personas/{agent-name}.md`
3. If missing, copy persona files from plugin assets or run `/sprint:update-version`

---

### Q: How to create a custom persona

Create a new `.md` file in your sprint's `personas/` directory:

1. Copy an existing persona file as a starting point
2. Update the frontmatter (`name`, `description`, `traits`)
3. Rewrite the system prompt sections (Decision Making, Communication Style, Domain Expertise, Quirks)
4. Use it with: `@INSTRUCTION.md #your-persona-name`

---

### Q: Persona auto-matching chose wrong persona

**Symptom**:
When starting without a name, the suggested persona doesn't fit the task.

**Solution**:
1. Decline the suggestion
2. Specify the persona explicitly: `@INSTRUCTION.md #preferred-name`
3. Auto-matching uses task type and content analysis — it's a suggestion, not a requirement

---

## Skill-Specific Issues

### /sprint:init

**Q: What if I init where a Sprint already exists?**

**Answer**: Asks if you want to overwrite existing files. Recommend selecting "No".

---

### /sprint:add-backlog

**Q: Feature numbers are duplicating**

**Solution**: Check highest Feature number in BACKLOG.md, then +1

```markdown
# Existing
F1, F2, F3

# New addition
F4 (not F1, F2, F3)
```

---

### /sprint:plan-backlog

**Q: Work starts immediately after Plan approval**

**Cause**: Skill behavior error

**Correct behavior**:
- Plan approved → Update BACKLOG.md → **End session**
- Actual work in **next session** via `@INSTRUCTION.md`

---

### /sprint:review-backlog

**Q: Can't find Task to review**

**Solution**:
1. Check for `done` status Tasks in BACKLOG.md
2. Provide exact Task ID (e.g., `T1.2`)

---

### /sprint:update-version

**Q: Says version file doesn't exist**

**Solution**:
- No `.sprint-version` file = treated as "legacy" version
- Proceeding with update auto-creates version file

---

## Advanced Issues

### Multi-Agent Synchronization

**Q: Agent work states don't match**

**Solution**:

1. **End all agent sessions**

2. **Manually clean BACKLOG.md, HANDOFF.md**
   ```markdown
   # Match actual state
   - [x] T1.1: Done `done`
   - [ ] T1.2: In progress #danny `in_progress`
   - [ ] T1.3: Not started `backlog`
   ```

3. **Clean In Progress table**
   ```markdown
   | Feature | Task | Persona | Started | Notes |
   |---------|------|---------|---------|-------|
   | F1 | T1.2 | #rook | 2024-01-28 | Actually in progress |
   ```

4. **Start new sessions for each agent**

---

### Large Sprint Management

**Q: Too many Features, hard to manage**

**Solution**:

1. **Regular archive of completed Features**
   ```
   refs/archive/F1-*.md
   refs/archive/F2-*.md
   ```

2. **Simplify BACKLOG.md**
   ```markdown
   ## Done
   - F1: Authentication - 2024-01-28
   - F2: User Profile - 2024-01-29

   ## Features
   ### F3: Payment (current)
   ...
   ```

3. **Consider Sprint separation**
   - Independent Feature groups → separate Sprints

---

### Performance Issues

**Q: Reading Sprint files takes too long**

**Solution**:

1. **Manage active/ file size**
   - Clean unnecessary content
   - Move history to refs/

2. **Clean BACKLOG.md**
   - Completed Features → archive
   - Done section → keep only last 3

3. **Organize refs/ folder**
   - Delete old plans/ files
   - Keep only organized items in archive/

---

## FAQ

### Q: Do I need Sprint for solo work?

**Answer**: Yes, still useful.
- Maintain context between sessions
- Track work progress
- Record decisions

### Q: Can I add Sprint to existing project?

**Answer**: Yes.
```
/sprint:init
→ Create in sprints/feature-x/
→ Existing code unchanged
→ Sprint is for work management only
```

### Q: How to integrate with Git?

**Answer**: Commit Sprint files to Git.
```bash
git add sprints/
git commit -m "Add sprint for feature X"
```

### Q: Accidentally changed Task status wrong

**Answer**: Manually edit BACKLOG.md.
```markdown
# Before (mistake)
- [x] T1.2: Not actually done `done`

# After (fixed)
- [ ] T1.2: Still in progress `in_progress`
```

### Worktree Mode Issues

**Q: Agent can't find sprint files in worktree**

**Cause**: Sprint files are in Sprint Root (main worktree), not in feature worktree.

**Solution**: Agent must use Sprint Root absolute path from INSTRUCTION.md.
```
Sprint Root: /Users/.../sprints/my-sprint/
# Read: {sprintRoot}/BACKLOG.md, NOT ./BACKLOG.md
```

---

**Q: Worktree creation fails**

**Cause**: Branch already exists, or path conflict.

**Solution**:
```bash
# Check existing worktrees
git worktree list

# Check existing branches
git branch -a

# Remove stale worktree reference
git worktree prune
```

---

**Q: Merge conflict during Merge Task**

**Solution**:
1. Resolve conflicts in the worktree
2. Complete the merge
3. Then remove worktree
4. Do NOT remove worktree before resolving conflicts

---

**Q: How to switch from default to worktree mode?**

**Solution**: Edit `.sprint-config` manually:
```json
{
  "mode": "worktree",
  "sprintRoot": "/absolute/path/to/sprint/",
  "worktree": {
    "command": "git worktree add {path} -b {branch}",
    "pathPrefix": "../<project>-worktrees"
  }
}
```
Then add sprint path to `.gitignore`.

---

### Q: Need to reference Task from different Sprint

**Answer**: Record cross-reference in refs/decisions/_sprint.md
```markdown
## Cross-Sprint References
- F2 (payment-sprint) depends on F1.3 (auth-sprint)
```
