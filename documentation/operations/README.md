# Operations Guide
Status: 🟢 STABLE
Last Updated: 2026-04-01

Details operational commands and infrastructure dependencies to successfully maintain the GLTive engine locally.

## Infrastructure Overview

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| `db` | `postgres:16-alpine` | `5432` | Primary database |
| `redis` | `redis:7-alpine` | `6379` | Cache and task queue broker |

## Environment Commands

Start background instances:
```bash
docker compose up -d
```

Stop background instances:
```bash
docker compose stop
```

## Migration Commands

Create new migrations:
```bash
python manage.py makemigrations
```

Apply migrations logic to DB:
```bash
python manage.py migrate
```

List missing/applied migrations:
```bash
python manage.py showmigrations
```

Validate application components dynamically:
```bash
python manage.py check
```

## Common Issues & Fixes
- **PostgreSQL connection refused**: Run `docker compose up -d` to verify containers are awake.
- **Migration conflicts**: Attempt a safe reversal to a common point, delete the offending parallel file, and remigrate cleanly. Avoid manually editing migration files unless strictly necessary.
- **Celery import errors**: Async engines must connect to Redis. Docker must be running to spin up Celery tasks effectively.

## Related Documents
- [Development Guide](../development/README.md)
