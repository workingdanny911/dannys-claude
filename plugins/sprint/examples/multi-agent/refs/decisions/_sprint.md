# Sprint-wide Decisions

## Cross-Feature Agreements

### 2024-01-28: Order ID Format

**Participants**: #danny, #agent-1

**Decision**: UUID v4

**Rationale**:
- Guaranteed uniqueness
- URL-safe
- Easy tracking

**Used in**:
- F1: PaymentIntent metadata
- F2: Order.id

---

### 2024-01-28: Payment-Order Integration Flow

**Participants**: #danny, #agent-1

**Decision**:
```
1. Create Order (status: pending)
2. Create PaymentIntent (orderId in metadata)
3. Client processes payment
4. Webhook received → Order status: paid
```

**Rationale**:
- Async payment handling
- No Order rollback needed on payment failure

---

## Architectural Decisions

### 2024-01-27: API Response Format

**Decision**:
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

**Error case**:
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message"
  }
}
```

---

## Constraints

- All amounts: in cents (Stripe compatible)
- All timestamps: UTC ISO8601
- All IDs: UUID v4
