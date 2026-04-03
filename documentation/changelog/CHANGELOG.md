# Changelog

All notable changes to GLTive will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Replaced hardcoded "core.User" with settings.AUTH_USER_MODEL
  in audit/models/log.py

## [0.6.0] - 2026-04-04
### Added
- Stock Service Layer Part 3: Adjustment, Alert, and Dashboard Services
  - StockAdjustmentService: create_adjustment_session, upsert_adjustment_lines, confirm_adjustment_session, cancel_adjustment_session
  - StockAlertService: evaluate_alerts_for_stock_item, acknowledge_alert, resolve_alert
  - StockDashboardService: get_summary, get_recent_movements, get_low_stock_items
- Adjustment confirmation now creates adjustment_plus and adjustment_minus stock movements atomically
- Auto-generated adjustment session codes with collision retry handling
- Alert flood prevention to avoid duplicate open events for the same stock item and alert type
- Standardized dashboard service return format using plain Python dict/list structures
### Changed
- Stock module documentation updated to reflect completed service layer implementation
## [0.5.1] - 2026-04-03
### Fixed
- Serialized issue now validates quantity_available >= requested count before
  processing units — prevents bypassing reserved quantity semantics
- Serialized transfer now validates source quantity_available >= requested count
  before processing units — prevents bypassing reserved quantity semantics
- Serialized receive now wraps StockSerialUnit.objects.create() with IntegrityError
  catch — concurrent serial_number/asset_tag race converts to clean StockConflictError
  instead of leaking raw DB IntegrityError
- All stock mutation operations now capture before_snapshot (locked state) and
  after_snapshot for enterprise-grade audit traceability
- All stock mutation operations now set updated_by=actor on mutated StockItem rows
- No model changes, no migration changes

## [0.5.0] - 2026-04-03
### Added
- Stock Service Layer Part 2: Core Stock Operations
  - StockItemService: create, update, deactivate, recalculate_available_quantity
  - StockReceiveService: receive_quantity_stock, receive_serialized_stock
  - StockIssueService: issue_quantity_stock, issue_serialized_stock
  - StockTransferService: transfer_quantity_stock, transfer_serialized_stock
- All quantity/state mutations use transaction.atomic + select_for_update
- Immutable StockMovement records created via .objects.create() only
- StockSerialUnit lifecycle: in_stock on receive, issued on issue, warehouse reassignment on transfer
- Paired transfer_out/transfer_in movements for warehouse transfers
- Race-safe target StockItem find-or-create in transfer flows (IntegrityError catch + re-fetch)
- All duplicate checks aligned with DB UniqueConstraint conditions (is_deleted=False)
- Audit trail via AuditService.log_event for all state changes
### Fixed
- Removed unused `from django.db import transaction` in category_service.py (Part 1 cleanup)

## [0.4.1] - 2026-04-03
### Fixed
- Aligned all service-level duplicate checks with actual DB UniqueConstraint
  conditions (is_deleted=False only, not is_active=True+is_deleted=False)
  Affected: CategoryService, BrandService, VendorService, ItemModelService,
  WarehouseService — prevents IntegrityError from constraint mismatch
- Added composite identity validation (company+category+normalized_model_name+brand)
  in ItemModelService create and update — prevents DB IntegrityError on the
  unique_active_item_model_identity_per_company constraint
- Hardened WarehouseService.create_warehouse first-default logic against
  concurrency race condition using select_for_update row lock before
  default-state decision
- Cleaned up lazy inline imports in WarehouseService (moved to top-level imports)
- No model changes, no migration changes

## [0.4.0] - 2026-04-03
### Added
- Stock Service Layer Part 1: Master Data Services (CategoryService, BrandService,
  VendorService, ItemModelService, WarehouseService)
- Company-scoped business validation for create, update, and deactivation operations
- Deactivation block rules preventing unsafe master data deactivation
- Audit trail integration via existing AuditService.log_event for all state changes
- Domain exception hierarchy (StockServiceError, StockNotFoundError, StockValidationError,
  StockConflictError, StockDeactivationBlockedError)
- Service utility helpers: snapshot serializer, entity fetcher, normalization functions
- Warehouse default-swap logic with transaction.atomic and select_for_update safety
- ItemModel tracking_type immutability enforcement after creation
- Category cyclic hierarchy detection with depth limit

## [0.3.3] - 2026-04-02
### Fixed
- Replaced all hardcoded "core.User" FK references in stock models
  with settings.AUTH_USER_MODEL (affected: adjustment.py, alert.py,
  movement.py) — aligns with platform-wide Django best practice
- Added explicit ordering = ["-created_at"] to StockAlertEvent Meta
- Added explicit ordering = ["-created_at"] to StockAdjustmentSession Meta

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
