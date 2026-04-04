# Changelog

All notable changes to GLTive will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Replaced hardcoded "core.User" with settings.AUTH_USER_MODEL
  in audit/models/log.py

## [0.8.1] - 2026-04-04
### Fixed
- Stock routes now protected with PermissionGuard (was AuthGuard-only)
- API client: added 401 interceptor with silent token refresh and queued retry
- API client: refresh failure triggers forced logout via callback
- Auth provider: registers logout callback with API client for 401 recovery
- Auth session: permissions array honestly empty (backend JWT does not include
  role permissions — only admin bypass active, documented explicitly)
- Permission hooks: documented that fine-grained non-admin checks will activate
  when backend provides permission source
- frontend/README.md rewritten as GLTive-specific documentation with honest
  auth model, permission model, and "what is / is not included" sections
- Design note: visual refinement will be guided by Google Stitch separately

## [0.8.0] - 2026-04-04
### Added
- GLTive Web UI Foundation (React + TypeScript + Vite + TailwindCSS)
- App shell: collapsible sidebar, topbar, responsive layout
- Design system: 14 shared UI components (Button, Input, Select, TextArea,
  Checkbox, Modal, DataTable, Badge, Card, Skeleton, EmptyState, PageHeader,
  Spinner, Toast)
- Auth/JWT foundation: in-memory token storage, login/logout flow, auth context
- Permission-aware rendering: usePermission hook, CanAccess wrapper, route guards
- API client: Axios with auth header injection, error normalization, TanStack Query
- i18n foundation: 5 languages (EN, AZ, RU, TR, AR) with RTL switching for Arabic
- Routing: React Router with lazy loading, AuthGuard, PublicGuard, PermissionGuard
- Stock module placeholder pages: dashboard, categories, items, movements
- Dark/light theme with system preference detection and persistence
- Language switcher with localStorage persistence

## [0.7.3] - 2026-04-04
### Fixed
- Production SECRET_KEY enforcement: startup fails explicitly if key is missing or weak
- Production CORS: resolved TODO, now env-driven with no wildcard default
- Added SECURE_PROXY_SSL_HEADER, SECURE_SSL_REDIRECT, HttpOnly cookies for production
- All paginated stock querysets now have explicit deterministic ordering
  (eliminates UnorderedObjectListWarning)
- Development settings use clearly labeled insecure fallback secret

### Added
- Production deployment runbook in operations documentation
- .env.example updated with production-specific variables and security notes

## [0.7.2] - 2026-04-04
### Added
- CompanyResolveMixin: resolves request.company after DRF JWT authentication,
  before permission checks — fixes architectural gap where TenantMiddleware
  ran before DRF decoded JWT tokens, leaving request.company=None for all
  JWT-authenticated requests
- CompanyScopedAPIView: base APIView class with company resolution for
  command-style endpoints (receive, issue, transfer, adjustments, alerts, dashboard)
- Stock permission bootstrap management command (bootstrap_stock_permissions)
  - 9 permission codes seeded idempotently: stock.view, stock.manage,
    stock.master.manage, stock.receive, stock.issue, stock.transfer,
    stock.adjust, stock.alert.manage, stock.history.view
- Critical automated test coverage for stock module (33 tests):
  - Service tests: receive, issue, transfer, adjustment, deactivation blocking
  - API tests: auth/permission enforcement, tenant isolation, exception mapping,
    command endpoints, lookup endpoints, bootstrap verification
  - Cross-company boundary tests for transfer and serialized issue flows

### Fixed
- All stock APIViews now use CompanyScopedAPIView instead of bare APIView
- All stock lookup/movement ViewSets now include CompanyResolveMixin
- Movement history view: replaced function-local Q import with top-level import
- Removed orphan helper function from movements view

## [0.7.1] - 2026-04-04
### Fixed
- All post-operation stock item fetches now use company-scoped lookups
  (pk + company=request.company) for defense-in-depth tenant safety
- Alert evaluation after stock operations now wrapped in safe handler —
  alert failure cannot break a successful main mutation response
- Adjustment confirm follow-up now uses bulk company-scoped fetch
  instead of N individual pk-only queries
- Design decision documented: alert evaluation is intentionally post-transaction
  and failure-isolated from the primary stock mutation

## [0.7.0] - 2026-04-04
### Added
- Stock Exception Mapping: StockValidationError→400, StockNotFoundError→404,
  StockConflictError→409, StockDeactivationBlockedError→409
- Stock API Layer: 40+ endpoints covering all stock operations
- Master Data CRUD APIs: Categories, Brands, Vendors, ItemModels, Warehouses, StockItems
- Stock Command APIs: Receive, Issue, Transfer (quantity + serialized)
- Adjustment APIs: create session, upsert lines, confirm, cancel
- Alert APIs: list, acknowledge, resolve
- Dashboard APIs: summary, recent movements, low stock items
- Movement History API: read-only list and detail
- Lookup APIs: 6 lightweight dropdown endpoints
- Permission enforcement on every endpoint with granular stock permission codes
- Alert evaluation automatically triggered after all stock-changing operations
- Company-scoped tenant isolation on every queryset and every write operation

### Changed
- Updated shared exception handler to catch stock domain exceptions
- Registered stock API routes under /api/v1/stock/
- Updated stock module documentation to reflect API implementation

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
