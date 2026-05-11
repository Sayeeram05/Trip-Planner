# Trip Planner

Django-based trip planner website with admin panel, packages, categories, and enquiry flow.

This README provides a full deployment guide for:

1. Render (Django + Gunicorn + persistent SQLite)
2. Cloudflare (DNS + SSL + edge security)

## 1. Prerequisites

Before deployment, make sure you have:

1. A GitHub repository with this project code.
2. A Render account.
3. A Cloudflare account and a domain name in GoDaddy.
4. Local Python environment ready for testing.

## 2. How SQLite is configured in this project

Database behavior is controlled by environment variables:

1. `DATABASE_URL` (optional)
2. `SQLITE_PATH` (recommended)

Resolution order:

1. If `DATABASE_URL` is set, Django uses it.
2. If `DATABASE_URL` is empty, Django uses `SQLITE_PATH`.
3. If `SQLITE_PATH` is also empty, fallback is `db.sqlite3` in project root.

For Render production, use a persistent disk path:

1. `SQLITE_PATH=/var/data/db.sqlite3`

## 3. Local verification before deployment

Run these steps locally first:

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Configure `.env` with SQLite:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=
SQLITE_PATH=db.sqlite3
ALLOWED_HOSTS=127.0.0.1,localhost
```

3. Run checks and migrations:

```bash
python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
```

4. Start app and confirm local health:

```bash
python manage.py runserver
```

Open:

1. `http://127.0.0.1:8000/`
2. `http://127.0.0.1:8000/healthz/`

## 4. Render deployment with persistent SQLite (step-by-step)

### Step 1: Create the Render web service

1. Go to Render dashboard.
2. Click New + and select Web Service.
3. Connect your GitHub repository.
4. Select this project repository.
5. Use the existing `render.yaml` if prompted.

### Step 2: Add persistent disk for SQLite

1. Open your Render service.
2. Go to Disks.
3. Add a disk with:
   - Name: `trip-planner-data`
   - Mount path: `/var/data`
   - Size: `1 GB` or higher

Why this matters:

1. SQLite on Render without persistent disk can be lost on restart/redeploy.
2. `/var/data` persists across deployments.

### Step 3: Configure Render environment variables

Set these in Render Environment:

```env
DEBUG=False
DATABASE_URL=
SQLITE_PATH=/var/data/db.sqlite3
ALLOWED_HOSTS=your-render-service.onrender.com,yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://your-render-service.onrender.com,https://yourdomain.com,https://www.yourdomain.com
RENDER_EXTERNAL_HOSTNAME=your-render-service.onrender.com
SECRET_KEY=your-production-secret-key
```

Notes:

1. Keep `DATABASE_URL` empty for SQLite mode.
2. Do not quote values in Render UI unless needed.

### Step 4: Deploy and initialize database

1. Trigger first deploy from Render.
2. Open Render Shell for the service.
3. Run:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py check --deploy
```

### Step 5: Validate Render app

Confirm:

1. Site opens on `your-render-service.onrender.com`.
2. Admin opens at `/snh-portal/`.
3. Health endpoint returns JSON on `/healthz/`.
4. Static files and images load.

## 5. Cloudflare setup (step-by-step)

### Step 1: Add domain to Cloudflare

1. Add your domain in Cloudflare.
2. Copy the two Cloudflare nameservers shown after domain onboarding.

### Step 2: Update nameservers in GoDaddy

1. Sign in to GoDaddy.
2. Go to `My Products`.
3. For your domain, click `DNS`.
4. Open the `Nameservers` section and click `Change`.
5. Choose `I'll use my own nameservers`.
6. Enter the two Cloudflare nameservers exactly as provided.
7. Save changes.
8. Return to Cloudflare and wait until domain status becomes Active.

Notes:

1. Nameserver propagation can take from a few minutes up to 24-48 hours.
2. During propagation, DNS may resolve intermittently.

### Step 3: Configure DNS records in Cloudflare

In Cloudflare DNS, add:

1. CNAME for `@` pointing to `your-render-service.onrender.com` (or use flattening).
2. CNAME for `www` pointing to `your-render-service.onrender.com`.
3. Set both to Proxied (orange cloud).

### Step 4: Configure SSL/TLS

1. Set SSL/TLS mode to Full (strict).
2. In Edge Certificates, enable Always Use HTTPS.
3. Optionally enable Automatic HTTPS Rewrites.

### Step 5: Optional redirect rule

1. Pick canonical host strategy:
   - `yourdomain.com` to `www.yourdomain.com`, or
   - `www.yourdomain.com` to `yourdomain.com`
2. Add one redirect rule in Cloudflare Rules.

### Step 6: Update app host settings

Ensure Render env values include your final domain set:

1. `ALLOWED_HOSTS` includes `yourdomain.com` and `www.yourdomain.com`.
2. `CSRF_TRUSTED_ORIGINS` includes HTTPS origins for both hosts.

## 6. Post-deploy production checklist

Verify after each deployment:

1. `DEBUG=False` is active.
2. HTTPS works and HTTP redirects to HTTPS.
3. Forms submit without CSRF errors.
4. Enquiries are saved in SQLite.
5. Admin login works.
6. Restart Render service and confirm data still exists.
7. Confirm SQLite file remains at `/var/data/db.sqlite3`.

## 7. Release workflow for every update

1. Develop and test locally.
2. Run migrations locally and review schema changes.
3. Push to GitHub main branch.
4. Render auto-deploy runs.
5. Run `python manage.py migrate` in Render Shell if needed.
6. Smoke test key pages and admin.
7. Verify logs and error rate.

## 8. Troubleshooting

### Issue: Data disappears after deploy

Cause:

1. SQLite file is not on persistent disk.

Fix:

1. Confirm disk mounted at `/var/data`.
2. Set `SQLITE_PATH=/var/data/db.sqlite3`.
3. Redeploy and migrate again.

### Issue: CSRF error in production forms

Fix:

1. Add exact HTTPS domain(s) in `CSRF_TRUSTED_ORIGINS`.
2. Redeploy after env update.

### Issue: DisallowedHost error

Fix:

1. Add domain(s) to `ALLOWED_HOSTS`.
2. Include Render hostname plus custom domains.

## 9. Security notes

1. Use a strong production `SECRET_KEY`.
2. Do not commit real secrets to repository.
3. Keep `DEBUG=False` in production.
4. Rotate email and API credentials periodically.
