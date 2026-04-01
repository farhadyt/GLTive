# Architecture Overview
Status: 🟢 STABLE
Last Updated: 2026-04-01

This section details the core structural design of the GLTive platform, outlining the boundaries, tech stack mapping, and architectural decisions.

## Document Directory

| Document | Status | Description |
|----------|--------|-------------|
| Tenant Data Isolation | 🔵 PLANNED | Row-level isolation policies and Company management |
| Permission Engine | 🔵 PLANNED | Role-based and attribute-based access controls |
| Audit Trail System | 🔵 PLANNED | Immutable state change tracking mechanism |
| Licensing & Activation | 🔵 PLANNED | Vendor-controlled module payload signing |

## Key Architectural Decisions
- **Django 5.x + DRF Backend**: Foundation for APIs and scalable domain logic.
- **PostgreSQL 16 Database**: Primary operational persistence layer.
- **Modular Monolith Pattern**: Strict bounded contexts instead of fully decoupled microservices.
- **Row-level Multi-Tenancy**: Data isolated logically using the `company_id` column.
- **JWT Authentication**: Cross-platform stateless stateless sessions with blacklist.
- **Key-based i18n**: Platform natively supports en, az, ru, tr, ar natively using JSON localization keys instead of database column translation.
- **Django Admin Intentionally Disabled**: GLTive enforces its own vendor administration UI.
- **LLM-agnostic AI Layer**: 🔵 PLANNED for abstract model routing.

> ℹ️ **NOTE:** Full Architectural Decision Records (ADRs) will be added incrementally as specific infrastructure is introduced.

## Related Documents
- [Master Architecture Document](../../about/Master%20Foundation%20Architecture%20Document%20v1.0.txt)
