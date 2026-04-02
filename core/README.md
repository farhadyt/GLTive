<!-- Purpose: Documentation for the core platform module -->
# Core Module

The `core/` package is the platform nucleus. It owns:

- **Base models** — UUID primary keys, timestamps, soft-delete, company-scoped mixins
- **Tenant / Company** — multi-tenant row-level isolation models
- **User** — custom user model extending Django's `AbstractUser`
- **Authentication** — JWT backend foundation
- **Permissions** — base permission classes for API access control
- **Middleware** — tenant resolution middleware

## Status

| Component         | Status      |
|-------------------|-------------|
| Base model mixins | Implemented |
| User model        | Implemented |
| Tenant/Company    | Implemented |
| Auth backend      | Implemented |
| Permissions       | Implemented |
| Tenant middleware | Implemented |

## Rules

- All business models across the platform **must** inherit from `core.models.base.BaseModel`
- Company-scoped models **must** use `CompanyScopedModel`
- No module should bypass tenant isolation
