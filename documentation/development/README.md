# Development Guide
Status: 🟢 STABLE
Last Updated: 2026-04-01

This guide covers necessary dependencies, local operational steps, and coding expectations required to contribute safely to the platform backend.

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.10+ | Local interpreter |
| Docker Desktop | Latest | Environment containers |
| Git | Latest | Version control |
| PostgreSQL | 16 | Ran virtually via Docker Compose |

## Local Setup
1. **Clone the repository**: Ensure you have correct SSH keys initialized.
2. **Copy `.env.example` to `.env`**: Configure local credentials.
3. **Start infrastructure**: 
   ```bash
   docker compose up -d
   ```
4. **Create virtual environment**: Follow standard `python -m venv venv` steps.
5. **Install dependencies**:
   ```bash
   pip install -r requirements/development.txt
   ```
6. **Run migrations**:
   ```bash
   python manage.py migrate
   ```
7. **Run server**:
   ```bash
   python manage.py runserver
   ```
8. **Verify environment**:
   ```bash
   python manage.py check
   ```

## Coding Standards
- Always inherit `core.models.base.BaseModel` or `core.models.base.CompanyScopedModel`.
- **No business logic in `views.py` or `serializers.py`**. Use the `services/` layer.
- All displayable strings must use **i18n keys** (no hardcoded text).
- All write operations must emit audit events.
- Enforce formatting using `Black` and `Ruff`.

## Git Commit Format
Use predictable syntax to streamline changelogs:
```
<type>: <short description>
```
**Types**: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`

> ⚠️ **WARNING:** What NOT to commit
> `.env`, `__pycache__`, `venv/`, `*.sqlite3`, `node_modules/`, build artifacts, logs, database files.

## Related Documents
- [Operations Guide](../operations/README.md)
