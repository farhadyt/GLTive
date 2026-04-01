# Changelog

All notable changes to GLTive will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
