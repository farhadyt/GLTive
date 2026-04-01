<!-- Purpose: Documentation for the audit trail engine -->
# Audit Trail Engine

The `audit/` package provides an immutable audit log for all critical state
changes across the platform.

## Audit Payload (minimum fields per event)

| Field              | Description                          |
|--------------------|--------------------------------------|
| actor_user_id      | User who performed the action        |
| company_id         | Company context                      |
| action_code        | e.g., `stock.category.created`       |
| target_entity_type | e.g., `stock_item_categories`        |
| target_entity_id   | UUID of the affected entity          |
| request_summary    | Summary of the request               |
| result_summary     | Summary of the result                |
| timestamp          | When the action occurred             |

## Status

**Placeholder** — audit model and service will be implemented in a
subsequent step. The architecture is defined here to ensure all modules
emit audit events from day one.

## Rules

- Audit records are **immutable** — no update, no delete
- Every write endpoint listed in the API contract **must** emit an audit event
- Audit service is called from the service layer, not from views
