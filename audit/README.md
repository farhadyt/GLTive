<!-- Purpose: Documentation for the audit trail engine -->
# Audit Trail Engine

The `audit/` package provides an immutable audit log for all critical state
changes across the platform.

## AuditLog Model Fields

| Field                | Type           | Description                                      |
|----------------------|----------------|--------------------------------------------------|
| `id`                 | UUID (PK)      | Auto-generated primary key (inherited from BaseModel) |
| `actor_user`         | FK → User      | User who performed the action (nullable)         |
| `company`            | FK → Company   | Company context for the event (nullable)         |
| `action_code`        | CharField(200)  | Dot-notation action identifier, e.g. `stock.category.created` |
| `target_entity_type` | CharField(150)  | Logical entity type, e.g. `stock_category`       |
| `target_entity_id`   | CharField(150)  | Identifier (usually UUID) of the affected entity |
| `before_snapshot`    | JSONField       | Serialized state of the entity before mutation (nullable) |
| `after_snapshot`     | JSONField       | Serialized state of the entity after mutation (nullable)  |
| `metadata`           | JSONField       | Additional structured context, e.g. movement IDs (nullable) |
| `created_at`         | DateTimeField   | Timestamp when the audit record was created (auto, inherited from BaseModel) |

## Immutability Guarantees

- `save()` raises `ValueError` if the record already exists (blocks updates)
- `delete()` raises `ValueError` unconditionally (blocks deletions)
- Once written, an AuditLog entry cannot be modified or removed

## Service Interface

All audit events are created through:

```python
from audit.services.logger import AuditService

AuditService.log_event(
    action_code="stock.category.created",
    target_entity_type="stock_category",
    target_entity_id="<uuid>",
    actor_user=user,
    company=company,
    before_snapshot=None,           # or dict
    after_snapshot={"field": "val"},
    metadata={"key": "value"},      # optional
)
```

## Status

Audit mechanism is implemented and actively used by the Stock Service Layer.
Additional modules will integrate as their service layers are built.

## Rules

- Audit records are **immutable** — no update, no delete
- Every write operation in the service layer **must** emit an audit event
- Audit service is called from the service layer, not from views or serializers
