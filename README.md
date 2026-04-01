<!-- Purpose: Root documentation for the GLTive platform -->
# GLTive Platform

**Vendor-controlled, modular, on-premise deployable, AI-driven enterprise IT operations platform.**

## Architecture

- **Backend:** Django 5.x + Django REST Framework
- **Database:** PostgreSQL 16+
- **Cache / Queue:** Redis + Celery
- **Auth:** JWT-based authentication
- **Pattern:** Modular monolith with service-ready bounded contexts
- **Multi-tenancy:** Row-level tenant isolation
- **Localization:** Azerbaijani, Russian, English, Turkish, Arabic

## Project Structure

```
GLTive/
├── config/          # Django project configuration (settings, WSGI, ASGI, Celery)
├── core/            # Platform core: auth, tenancy, permissions, base models
├── modules/         # Bounded-context business modules
│   └── stock/       # Module 01: Stock / Inventory Foundation
├── shared/          # Shared utilities, mixins, base serializers, pagination
├── api/             # API gateway: versioned URL routing
├── audit/           # Immutable audit trail engine
├── localization/    # i18n locale files and translation infrastructure
├── ai/              # AI core infrastructure (future)
├── automation/      # Automation and workflow engine (future)
├── licensing/       # License and entitlement engine (future)
├── deployment/      # Deployment scripts, Docker configs
├── requirements/    # Python dependency files
└── about/           # Platform documentation and architecture specs
```

## Quick Start (Development)

```bash
# Copy environment template
cp .env.example .env

# Start infrastructure services
docker-compose up -d

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements/development.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

## Development Principles

1. **Capability-first design** — built around capabilities, not screens
2. **Multi-tenant by design** — tenant isolation from day one
3. **API-first** — all functionality exposed through versioned REST APIs
4. **Audit by default** — all critical state changes are audited
5. **Localization-ready** — no hardcoded strings, key-based translations
6. **Modular** — new modules must not break the core skeleton

## License

Proprietary — GLTive Platform. All rights reserved.
