# Sprint Instructions

> Guidelines for agents working on this sprint.
> Start a session with: `@INSTRUCTION.md #agent-name`

---

## Team

| Agent | Primary Focus |
|-------|--------------|
| #danny | F1: Payment Integration |
| #agent-1 | F2: Order Management |

---

## Session Start

When you receive `@INSTRUCTION.md #agent-name`:

1. **Identify yourself** as `#agent-name`
2. **Read required files**:
   - `BACKLOG.md` - Find your task
   - `HANDOFF.md` - Current status, **Dependencies**, **Blockers**
   - `refs/decisions/F{n}-*.md` - Feature decisions
   - `active/F{n}-*.md` - Feature context
3. **Check Dependencies** - Is your task blocked?
4. **Find your task**:
   - Already assigned? Continue it.
   - Nothing assigned? Claim from your focus area first.
5. **State your task** before starting

---

## Multi-Agent Coordination

### Ownership Rules

| Area | Owner | Others |
|------|-------|--------|
| BACKLOG.md | 자기 Task만 수정 | 읽기만 |
| HANDOFF.md | 자기 row만 수정 | Dependencies 확인 |
| active/F1-* | #danny | 읽기만 |
| active/F2-* | #agent-1 | 읽기만 |
| refs/ | 자기 Feature만 | 읽기만 |

### Cross-Feature Dependencies

T2.4 (Order Cancel) → T1.3 (Webhook) 의존 관계:

```
#agent-1 작업 순서:
1. T2.1 ✓
2. T2.2 (현재)
3. T2.3
4. T2.4 ← T1.3 완료 대기

#danny 작업 순서:
1. T1.1 ✓
2. T1.2 (현재)
3. T1.3 ← 완료 시 #agent-1에게 T2.4 unblock
4. T1.4
```

### Handoff Protocol

**#danny → #agent-1 handoff 시:**

1. T1.3 완료 후 HANDOFF.md Dependencies 업데이트
   ```markdown
   | T2.4 | T1.3 | T1.3 done | ✅ Unblocked |
   ```

2. `refs/decisions/F1-decisions.md`에 인터페이스 문서화
   ```markdown
   ## Refund API Interface
   POST /api/payments/refund
   { orderId, amount, reason }
   ```

3. 세션 종료 - #agent-1이 다음 세션에서 확인

---

## WIP Limit

**1 task per agent**

- #danny: F1 Task 1개
- #agent-1: F2 Task 1개

### Blocked 상태 처리

Task가 blocked되면:
1. Blockers 테이블에 기록
2. **다른 Task claim 금지** (WIP 제한)
3. blocking task owner와 조율

---

## Session End

1. **Update BACKLOG.md** - 자기 Task만
2. **Update HANDOFF.md** - 자기 row만, Dependencies 확인
3. **Update active/** - 자기 Feature만
4. **Check unblocked tasks** - 내 완료로 unblock된 것 표시

---

## Context Compaction Recovery

컨텍스트 압축 시:

1. Re-read: INSTRUCTION.md → BACKLOG.md → HANDOFF.md → active/
2. **같은 #agent-name 유지**
3. **진행 중이던 Task 계속** (새 Task claim 금지)
4. Dependencies 재확인

---

## Core Principles

1. **Own Your Lane** - 자기 영역만 수정
2. **Communicate via Files** - active/, refs/에 기록
3. **Respect Dependencies** - Blocked 확인 후 시작
4. **One Session = One Task** - 완료 후 세션 종료
