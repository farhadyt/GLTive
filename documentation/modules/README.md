# Module Registry
Status: 🟡 IN PROGRESS
Last Updated: 2026-04-01

In GLTive, a "module" represents a structurally independent business capability (bounded context). Modules encapsulate their own domains but rely on the `core` layer for multi-tenancy, auth, and audit functions.

## Module Registry

| Module | Status | Phase | Description |
|--------|--------|-------|-------------|
| Stock/Inventory Foundation | 🟡 IN PROGRESS | Phase 1 | Asset warehousing and lifecycle foundation |
| Asset Management | 🔵 PLANNED | Phase 1 | Handover and deployment histories |
| Ticketing & Service | 🔵 PLANNED | Phase 2 | Helpdesk and approval workflows |
| Monitoring & Event | 🔵 PLANNED | Phase 2 | Alert intelligence and threshold parsing |
| AI Ops Copilot | 🔵 PLANNED | Phase 3 | Recommendation and automation assistant |

## Module Boundary Rules
1. **Physical isolation**: Each module is a separate Django app located under the `modules/` directory.
2. **Tenant scoping**: Models must inherit `CompanyScopedModel`.
3. **No direct crossover**: No direct cross-module model imports. Interactions happen via internal APIs or event hooks.
4. **Logic placement**: Business logic resides in `services/`, not in `views.py` or `serializers.py`!
5. **Auditing**: All write operations must emit immutable audit events.

## How to Add New Modules
1. Scaffold the app under `modules/<name>`.
2. Register the app Config in `config/settings/base.py` under `PLATFORM_APPS`.
3. Create `models/`, `services/`, `api/`, and `tests/` directories.
4. Integrate routing in `api/urls.py` via module namespace.
5. Create the module's documentation root.

> ⚠️ **WARNING:** When a module is implemented, its documentation must be created in the same commit.

## Related Documents
- [Architecture Guidelines](../architecture/README.md)
