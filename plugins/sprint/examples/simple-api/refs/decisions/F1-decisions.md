# F1: User Authentication - Decisions

## Decision Log

### 2024-01-27: JWT vs Session

**Context**: Authentication method selection

**Options**:
1. JWT (stateless)
2. Session (server-side)

**Decision**: JWT

**Rationale**:
- Stateless → Easy horizontal scaling
- Considering mobile app support
- Preparing for microservices architecture

---

### 2024-01-27: Token Validity Period

**Context**: Setting Access/Refresh Token validity

**Decision**:
- Access Token: 15 minutes
- Refresh Token: 7 days

**Rationale**:
- Short Access Token → Minimize damage if stolen
- Refresh Token maintains UX

---

### 2024-01-28: Refresh Token Rotation

**Context**: Refresh Token reuse policy

**Decision**: Apply rotation (issue new token each time)

**Rationale**:
- Prevent reuse of stolen Refresh Token
- Additional security layer
