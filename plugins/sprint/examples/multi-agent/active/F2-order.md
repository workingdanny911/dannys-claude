# F2: Order Management - Active Context

> Owner: #agent-1

## Current Status

- **Task**: T2.2: Create Order API
- **Started**: 2024-01-28

## Progress

### Completed
- [x] T2.1: Order Model & Migration
  - Order table created
  - OrderItem table created
  - Status: pending, paid, cancelled, refunded

### In Progress
- [ ] T2.2: Create Order API
  - [x] POST /api/orders route
  - [x] Input validation
  - [ ] Transaction handling
  - [ ] Inventory check logic

### Remaining
- [ ] T2.3: Get Order API
- [ ] T2.4: Cancel Order API (blocked - waiting for T1.3)
- [ ] T2.5: Review & Refactor

## Decisions

| Decision | Reason | Date |
|----------|--------|------|
| Order ID = UUID v4 | Agreed with #danny, easy tracking | 2024-01-28 |
| Order status = pending on creation | Pre-payment state | 2024-01-28 |
| Inventory deduction after payment confirmed | No rollback needed on payment failure | 2024-01-28 |

## Coordination with #danny

### Agreed
- Order ID format: UUID v4 (done)
- Payment integration flow:
  1. T2.2: Create Order (status: pending)
  2. T1.2: Create PaymentIntent (orderId in metadata)
  3. T1.3: Webhook updates Order status → paid

### Pending
- T2.4 (Cancel Order) needs T1.3 (Webhook) complete
- Waiting for Refund logic interface

## Files

```
src/models/order.ts
src/models/orderItem.ts
src/routes/order.ts
src/services/order.service.ts
migrations/20240128_create_orders.ts
```

## Notes

### Order Status Flow
```
pending ──► paid ──► shipped ──► delivered
    │         │
    │         ▼
    │      refunded
    │
    ▼
 cancelled
```

### T2.4 Blocked Reason
- Order cancellation requires payment refund
- Refund API needed from Stripe Webhook (T1.3)
- Unblocks when #danny completes T1.3
