# Trip Planner

Django-based trip planner website with admin panel, packages, categories, and enquiry flow.

This README provides a full deployment guide for:

1. Render Free Tier (Django + Gunicorn + SQLite)
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

For the current Render free-tier setup in this repo, SQLite uses an ephemeral path:

1. `SQLITE_PATH=/var/data/db.sqlite3`

Free-tier note:

1. Render free services do not support persistent disks.
2. That means SQLite data can be reset on redeploy or restart.
3. If you need persistent production data, upgrade Render plan or move to a managed database.

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
USE_CLOUDFLARE_R2=False
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

## 4. Render deployment with free-tier SQLite (step-by-step)

### Step 1: Create the Render web service

1. Go to Render dashboard.
2. Click New + and select Web Service.
3. Connect your GitHub repository.
4. Select this project repository.
5. Use the existing `render.yaml` if prompted.

### Step 2: Understand the free-tier SQLite limitation

1. Render free services do not support disks in blueprint deploys.
2. This repo is configured to use SQLite on the service filesystem instead.
3. That filesystem is not persistent across redeploys or restarts.
4. This setup is acceptable for demos or temporary testing, not durable production storage.

### Step 3: Configure Render environment variables

Set these in Render Environment:

```env
DEBUG=False
DATABASE_URL=
SQLITE_PATH=/opt/render/project/src/db.sqlite3
ALLOWED_HOSTS=your-render-service.onrender.com,yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://your-render-service.onrender.com,https://yourdomain.com,https://www.yourdomain.com
RENDER_EXTERNAL_HOSTNAME=your-render-service.onrender.com
SECRET_KEY=your-production-secret-key
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=change-this-password
```

Notes:

1. Keep `DATABASE_URL` empty for SQLite mode.
2. Do not quote values in Render UI unless needed.
3. The superuser variables are only needed if you want Render to create the admin user automatically.
4. On free tier, `SQLITE_PATH` should not point to `/var/data` because there is no mounted disk.

### Step 4: Deploy and initialize database

1. This project is configured for Render free plan where Shell is unavailable.
2. On each deploy/start, Render will run migrations first.
3. Render will then try `python manage.py createsuperuser --noinput`.
4. If the superuser already exists, startup continues because the command is wrapped with `|| true`.
5. After that, Gunicorn starts the Django app.

The startup command used by this repo is:

```bash
python manage.py migrate && (python manage.py createsuperuser --noinput || true) && gunicorn Main.wsgi:application --bind 0.0.0.0:$PORT
```

Build command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

### Step 5: Validate Render app

Confirm:

1. Site opens on `your-render-service.onrender.com`.
2. Admin opens at `/snh-portal/`.
3. Health endpoint returns JSON on `/healthz/`.
4. Static files and images load.
5. You can log in with the superuser credentials from Render environment variables.
6. Expect SQLite data to be lost on full redeploy/restart on free tier.

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

## 5A. Cloudflare R2 setup for uploaded images (recommended)

Use this section to move Django media uploads from local storage to Cloudflare R2 while keeping static files on WhiteNoise.

### Step 1: Create R2 bucket

1. In Cloudflare dashboard, open R2.
2. Create a bucket (example: `trip-planner-media`).
3. Keep the bucket name for Render env `CLOUDFLARE_R2_BUCKET_NAME`.

### Step 2: Create R2 API token

1. In Cloudflare, create an R2 API token with bucket-level read/write access.
2. Copy the Access Key ID and Secret Access Key.
3. Save them securely; add them only in Render environment variables.

### Step 3: Configure custom media domain

1. Add DNS record in Cloudflare for `media.yourdomain.com`.
2. Configure Cloudflare R2 custom domain for the bucket to use that host.
3. Ensure HTTPS works on `https://media.yourdomain.com`.

### Step 4: Add Render environment variables

Set these in Render Environment:

```env
USE_CLOUDFLARE_R2=True
CLOUDFLARE_MEDIA_DOMAIN=media.yourdomain.com
CLOUDFLARE_R2_BUCKET_NAME=trip-planner-media
CLOUDFLARE_R2_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
CLOUDFLARE_R2_MEDIA_LOCATION=uploads
CLOUDFLARE_R2_ACCESS_KEY_ID=your-r2-access-key-id
CLOUDFLARE_R2_SECRET_ACCESS_KEY=your-r2-secret-access-key
```

Notes:

1. Keep `CLOUDFLARE_MEDIA_DOMAIN` without path.
2. `CLOUDFLARE_R2_MEDIA_LOCATION` is optional; set empty if you do not want a prefix.
3. Keep `USE_CLOUDFLARE_R2=False` in local development unless local env has valid R2 credentials.

### Step 5: Deploy and verify new uploads

1. Trigger Render deploy.
2. Upload one new image in each admin model:
   - Hero image
   - Category image
   - Package cover image
   - Package gallery image
3. Confirm files appear in R2 bucket under the configured prefix.
4. Open website pages and verify image URLs load from `https://media.yourdomain.com/...`.

### Step 6: Scope of this rollout

1. This setup moves only new uploads to R2.
2. Existing local files are not migrated automatically.
3. If old files must be preserved on cloud, run a one-time backfill later.

## 6. Post-deploy production checklist

Verify after each deployment:

1. `DEBUG=False` is active.
2. HTTPS works and HTTP redirects to HTTPS.
3. Forms submit without CSRF errors.
4. Enquiries are saved in SQLite.
5. Admin login works.
6. Confirm SQLite file is created at `/opt/render/project/src/db.sqlite3` while the instance is running.
7. If persistent data is required, move off free tier or use an external DB.

## 7. Release workflow for every update

1. Develop and test locally.
2. Run migrations locally and review schema changes.
3. Push to GitHub main branch.
4. Render auto-deploy runs.
5. Render startup automatically runs migrations and attempts superuser creation.
6. Smoke test key pages and admin.
7. Verify logs and error rate.

## 8. Troubleshooting

### Issue: Data disappears after deploy

Cause:

1. Render free tier does not provide a persistent disk.

Fix:

1. This is expected on free tier with SQLite.
2. Upgrade Render plan and add a disk, or move to a managed database.
3. For temporary testing only, redeploy and let startup recreate the database.

### Issue: CSRF error in production forms

Fix:

1. Add exact HTTPS domain(s) in `CSRF_TRUSTED_ORIGINS`.
2. Redeploy after env update.

### Issue: DisallowedHost error

Fix:

1. Add domain(s) to `ALLOWED_HOSTS`.
2. Include Render hostname plus custom domains.

### Issue: Superuser was not created

Fix:

1. Set `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, and `DJANGO_SUPERUSER_PASSWORD` in Render.
2. Trigger a redeploy or restart.
3. Check deploy logs for the `Superuser created successfully.` message.

### Issue: New image uploads fail with AccessDenied or Signature mismatch

Fix:

1. Verify `CLOUDFLARE_R2_ACCESS_KEY_ID` and `CLOUDFLARE_R2_SECRET_ACCESS_KEY` in Render.
2. Confirm `CLOUDFLARE_R2_ENDPOINT_URL` is exactly `https://<account-id>.r2.cloudflarestorage.com`.
3. Ensure token scope includes read/write permissions on the target bucket.
4. Redeploy after updating env variables.

### Issue: Image URL still points to `/media/` instead of media subdomain

Fix:

1. Verify `USE_CLOUDFLARE_R2=True` in Render.
2. Ensure `CLOUDFLARE_MEDIA_DOMAIN` is set (example: `media.yourdomain.com`).
3. Upload a new image after deploy and retest.

## 9. Security notes

1. Use a strong production `SECRET_KEY`.
2. Do not commit real secrets to repository.
3. Keep `DEBUG=False` in production.
4. Rotate email and API credentials periodically.
