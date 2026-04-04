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

## Production Deployment

### Required Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DJANGO_SETTINGS_MODULE` | Yes | Must be `config.settings.production` |
| `DJANGO_SECRET_KEY` | Yes | Minimum 50 chars, cryptographically random |
| `DJANGO_ALLOWED_HOSTS` | Yes | Comma-separated allowed hostnames |
| `DATABASE_NAME` | Yes | PostgreSQL database name |
| `DATABASE_USER` | Yes | PostgreSQL user |
| `DATABASE_PASSWORD` | Yes | PostgreSQL password |
| `DATABASE_HOST` | Yes | PostgreSQL host |
| `DATABASE_PORT` | No | Default: 5432 |
| `REDIS_URL` | Yes | Redis connection URL |
| `CORS_ALLOWED_ORIGINS` | Yes | Comma-separated allowed origins (no wildcards) |
| `SECURE_SSL_REDIRECT` | No | Default: True. Set to False if SSL terminates at proxy |

### Production Bootstrap Sequence

```bash
# 1. Set environment variables (see .env.example)
export DJANGO_SETTINGS_MODULE=config.settings.production

# 2. Run migrations
python manage.py migrate

# 3. Collect static files
python manage.py collectstatic --noinput

# 4. Bootstrap module permissions
python manage.py bootstrap_stock_permissions

# 5. Verify system
python manage.py check --deploy

# 6. Start application
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Security Notes

- Production startup will **fail** if `DJANGO_SECRET_KEY` is missing or shorter than 50 characters
- JWT signing uses Django's `SECRET_KEY` — a strong key ensures strong JWT tokens
- CORS is strict by default — no wildcard origins allowed
- SSL redirect is enabled by default — disable only behind a reverse proxy that handles SSL
- All cookies are `Secure` and `HttpOnly` flagged

## Related Documents
- [Development Guide](../development/README.md)
