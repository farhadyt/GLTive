<!-- Purpose: Documentation for the modules directory structure -->
# Modules

The `modules/` directory contains all bounded-context business modules of the GLTive platform.

Each module is a self-contained Django app with its own:
- `models/` — database models (company-scoped)
- `services/` — business logic layer
- `api/` — serializers, views, and URL routes
- `migrations/` — database migrations
- `README.md` — module documentation

## Current Modules

| Module   | Status      | Description                    |
|----------|-------------|--------------------------------|
| `stock/` | Placeholder | Stock / Inventory Foundation   |

## Rules

1. Each module **must** be a separate Django app under `modules/`
2. Models **must** inherit from `core.models.base.CompanyScopedModel`
3. No direct cross-module model imports — use service interfaces
4. Business logic goes in `services/`, **not** in views or serializers
5. All state changes **must** emit audit events
6. All user-facing strings **must** use i18n translation keys

## Future Modules (not yet implemented)

- Asset Lifecycle
- Procurement
- Ticketing / Service Management
- Infrastructure / Endpoint
- Network / Connectivity
- Monitoring / Observability
- Security / SOC
