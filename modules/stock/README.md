<!-- Purpose: Documentation for Module 01 — Stock / Inventory Foundation -->
# Module 01 — Stock / Inventory Foundation

First business module of the GLTive platform. Provides the foundation for
asset and lifecycle management.

## Scope (when implemented)

- Stock item categories (hierarchical)
- Brands and vendor references
- Item models (serialized vs quantity-based)
- Warehouses
- Stock items (warehouse-level tracking)
- Stock serial units
- Stock movements (immutable history)
- Stock adjustment sessions
- Stock alerts

## Status

**Placeholder** — structural skeleton only. Models, services, and API
endpoints will be implemented in a subsequent step per the
Module 01 Data Model and API Contract documents.

## Architecture Rules

- All models inherit from `core.models.base.CompanyScopedModel`
- Business logic in `services/`, not in views
- Serialized and quantity-based logic separated in service layer
- Stock movements are immutable (no update/delete)
- All write operations emit audit events
