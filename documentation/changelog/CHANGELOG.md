# Changelog

All notable changes to GLTive will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.2] - 2026-04-02
### Fixed
- **Stock Module Final Contract Correction Pass:** Restored explicitly declared `is_active` fields back into all core definition blocks (Category, Brand, Vendor, ItemModel, Warehouse, StockItem) guaranteeing strict explicit structural alignment against dictionary checks.

## [0.3.1] - 2026-04-02
### Fixed
- **Stock Module Data Alignment Pass:** Hard-coupled models to the v1.0 Field Dictionary explicitly decoupling contract-violating behavior inherited historically via soft-delete mixins.
- Immutability strictly modeled on `StockMovement` purging `is_deleted` and `updated_at` mechanisms.
- Clean Status logic implemented for adjustments and events directly bypassing global soft-delete schemas.
- Future location hooks safely mapped into the Phase 1 `Warehouse` context schema via `location_reference_id`.
- Added missing recommended index patterns.

## [0.3.0] - 2026-04-02
### Added
- Stock Module Data Foundation implemented safely under `modules/stock/models`.
- 12 authoritative models explicitly capturing categories, items, warehouses, serial unit state routing, and structural thresholds without prematurely importing Service or API layers.
- Enforced hard `StockMovement` immutable tracking guarantees.
- Native `CompanyScopedModel` implementations with robust constraints mapped correctly inside the PostgreSQL infrastructure.

## [0.2.0] - 2026-04-02
### Added
- Core Access Foundation implementation.
- Minimal `Role` and `Permission` DB-backed structure mapping explicitly to companies.
- `TenantMiddleware` enforcing explicit `request.company` contexts on authenticated requests.
- Custom authentication endpoints (`login`, `refresh`, `logout`) wrapped in standard JSON response envelopes, with `company_id` mapped into JWT payloads.
- `CompanyScopedViewSet` base API class to strictly firewall querysets to the active tenant company.
- Immutable `AuditLog` models and `AuditService.log_event` hook for immutable global record keeping.

## [0.1.0] - 2026-03-31
### Added
- Backend foundation skeleton with modular monolith architecture
- Core module: BaseModel, AuditableModel, SoftDeleteModel, CompanyScopedModel
- Tenant and Company models with row-level isolation
- Custom User model with company association and UUID primary key
- JWT authentication foundation via SimpleJWT
- JWT token blacklist support
- Celery + Redis configuration with safe import handling
- Docker Compose local development setup (PostgreSQL 16, Redis 7)
- 5-language i18n foundation (az, ru, en, tr, ar)
- Stock module skeleton as bounded context placeholder
- Audit trail engine skeleton with immutable log contract
- API gateway with versioned routing (/api/v1/)
- Shared utilities: StandardPagination, exception handler, success/error response wrappers, base serializers
- Split settings: base, development, production
- Documentation infrastructure (this release)

### Architecture Decisions
- Django admin intentionally disabled — platform uses own admin UI
- django-modeltranslation removed — key-based i18n adopted
- Modular monolith pattern selected over microservices
- Row-level tenancy with CompanyScopedModel as platform standard
