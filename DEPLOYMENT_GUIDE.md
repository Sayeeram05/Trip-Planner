# Trip Planner Deployment Guide

This guide deploys your stack in this order:
1. Render (Django app + SQLite on Render Disk)
2. Cloudflare (DNS + SSL + security)

## Architecture (step-by-step image)

```mermaid
flowchart LR
    U[User Browser] --> C[Cloudflare]
   C --> R[Render: Django + Gunicorn]
   R --> S[Render Disk: SQLite db.sqlite3]
```

## Stage 1: Development Readiness

1. Ensure your local `.env` has all values from `.env.example`.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Verify project health locally:
   - `python manage.py check`
   - `python manage.py migrate`
   - `python manage.py collectstatic --noinput`
4. Confirm health endpoint works:
   - `http://127.0.0.1:8000/healthz/`

## Stage 2: Render SQLite Disk (Database persistence)

1. In Render, open your Web Service.
2. Add a persistent disk:
   - Name: `trip-planner-data`
   - Mount path: `/var/data`
   - Size: 1 GB (or more)
3. Set environment variable:
   - `SQLITE_PATH=/var/data/db.sqlite3`
4. Keep `DATABASE_URL` empty unless you intentionally use a SQLite URL.
5. Deploy once so the app creates/uses the SQLite file on the mounted disk.

## Stage 3: Render Django App

1. Push this repository to GitHub.
2. In Render, create a new **Web Service** from your repo.
3. Render will detect [render.yaml](render.yaml).
4. In Render environment variables, set:
   - `SQLITE_PATH` = `/var/data/db.sqlite3`
   - `ALLOWED_HOSTS` = `your-render-service.onrender.com,yourdomain.com,www.yourdomain.com`
   - `CSRF_TRUSTED_ORIGINS` = `https://your-render-service.onrender.com,https://yourdomain.com,https://www.yourdomain.com`
   - `RENDER_EXTERNAL_HOSTNAME` = `your-render-service.onrender.com`
5. Deploy the service.
6. Open Render Shell and run:
   - `python manage.py migrate`
   - `python manage.py createsuperuser`
7. Validate:
   - Home page loads
   - Admin works at `/snh-portal/`
   - Health endpoint returns JSON at `/healthz/`

## Stage 4: Cloudflare Domain + SSL

1. Add your domain to Cloudflare.
2. Update your domain nameservers at your registrar to Cloudflare nameservers.
3. In Cloudflare DNS:
   - Add `CNAME` for `@` to `your-render-service.onrender.com` (or use flattening).
   - Add `CNAME` for `www` to `your-render-service.onrender.com`.
   - Set both records to **Proxied** (orange cloud).
4. SSL/TLS mode:
   - Set to **Full (strict)**.
5. In Cloudflare Edge Certificates:
   - Enable **Always Use HTTPS**.
6. In Cloudflare Rules:
   - Optional: redirect `www` to apex or apex to `www` (pick one canonical host).

## Stage 5: Production Validation Checklist

1. `DEBUG=False` in Render.
2. App responds over HTTPS only.
3. Admin login works through Cloudflare domain.
4. Images and static files load correctly.
5. New enquiry submissions save in DB.
6. No CSRF errors on forms.
7. Health endpoint returns `{"status": "ok"}`.
8. Restart the Render service and confirm data still exists (proves disk persistence).

## Stage 6: Continuous Deployment Workflow

1. Develop locally and test.
2. Push to GitHub main branch.
3. Render auto-deploys from GitHub.
4. Post-deploy checks:
   - `python manage.py check --deploy`
   - smoke-test key pages.
5. Rollback from Render if needed.

## Recommended release order (every update)

1. Database migration prep (`makemigrations`/`migrate` review)
2. Push code
3. Render deploy
4. Run migrations on Render shell
5. Smoke test via Cloudflare domain
6. Confirm analytics/logs and error rate
7. Verify SQLite file remains on `/var/data/db.sqlite3`

## Notes for this project

- The app now supports both:
   - `SQLITE_PATH` (recommended for Render Disk)
   - `DATABASE_URL` (optional, for SQLite URL usage)
- Production security settings are automatically enabled when `DEBUG=False`.
- Static assets use WhiteNoise compressed manifest storage for deployment.
- Do not use ephemeral SQLite at `/app` in production; use Render Disk path under `/var/data`.
