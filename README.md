# Hernandez development
# AgriScan+

AgriScan+ is a Django-based, web-first rice farm management system with AI-assisted disease detection and three-mode yield prediction.

## What This Project Does

- Detect rice diseases from leaf images
- Predict yield using farm and planting context
- Manage fields, plantings, treatments, harvests, and logs
- Enforce role-based access for Admin, Technician, and Farmer users
- Provide factual harvest reports and analytics for decision support

## Tech Stack

- Python (3.10+ recommended)
- Django
- MySQL 8.x
- TensorFlow / TensorFlow Lite
- scikit-learn, pandas, numpy
- PyTorch + torchvision (CNN yield path)
- Tailwind CSS (template styling)

## Quick Start (Local Development)

From the project root (same folder as manage.py):

```bash
# 1) Create a virtual environment (isolates dependencies per project)
python -m venv venv

# 2) Activate the environment
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Linux / macOS
source venv/bin/activate

# 3) Install Python dependencies
pip install -r requirements.txt

# 4) Apply database migrations
python manage.py migrate

# 5) Create an admin account for first login
python manage.py createsuperuser

# 6) Run development server
python manage.py runserver
```

Open: http://127.0.0.1:8000

For production deployment and updates, see
[deployment.md](./deployment.md). The documented CloudPanel/Gunicorn update
sequence is currently manual; it should not be described as CI/CD until an
automated pipeline with protected deployment secrets is configured.

For the terminal-only administrator creation workflow, see
[create-admin.md](./create-admin.md).

## Frontend CSS (Tailwind Watch)

For development, run Tailwind in watch mode in a separate terminal so template/style changes compile automatically.

Windows PowerShell (multi-line):

```powershell
.\tailwindcss.exe `
  --input polls\static\polls\css\input.css `
  --output polls\static\polls\css\tailwind.css `
  --content "./templates/*.html","./templates/**/*.html" `
  --watch
```

One-line equivalent:

```powershell
.\tailwindcss.exe --input polls\static\polls\css\input.css --output polls\static\polls\css\tailwind.css --content "./templates/*.html","./templates/**/*.html" --watch
```

Tip: Keep this watcher running while `python manage.py runserver` is running.

## Required Configuration

Current defaults are set in mysite/settings.py. Before production use:

- Set DEBUG = False
- Set a strong SECRET_KEY
- Set ALLOWED_HOSTS
- Configure secure database credentials
- Configure email credentials via environment variables
- Configure dual-model yield runtime settings via environment variables (checkpoint, device, fallback toggle)
- Use System Settings for business toggles (email enable, CNN enable)

Recommended environment variables:

```env
DEBUG=False
SECRET_KEY=replace-with-strong-secret
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
APP_BASE_URL=https://your-domain.com
DB_NAME=agriscan_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
EMAIL_ENABLED=True
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_app_password
YIELD_CNN_ENABLED=True
YIELD_CNN_CHECKPOINT_PATH=models/rice_yield_CNN.pth
YIELD_CNN_DEVICE=cpu
```

Configuration rule of thumb:

- Environment variables: secrets and infrastructure/runtime configuration
  - SMTP credentials
  - model checkpoint path
  - model device (cpu/cuda)
- System Settings (admin UI): business toggles and operational controls
  - `email_enabled`
  - `yield_cnn_enabled`

Fallback behavior:

- `EMAIL_ENABLED` and `YIELD_CNN_ENABLED` are used only when the `SiteSetting` row is missing or unavailable.

## Key Features

### Disease Detection

- Image upload/capture workflow
- AI classification of rice diseases
- Confidence and severity tracking
- Detection history and detail views

### Yield Prediction

- Two entry modes:
  - from detection (auto-filled context)
  - direct/manual input
- Three model modes:
  - Linear Regression (tabular agronomic features)
  - CNN Yield (canopy image + area/date/growth context)
  - Ensemble (weighted blend of CNN + Linear outputs)
- Historical production-aware prediction flow for Linear Regression
- Real-time historical yield calculation in form UX

Prediction results are estimates and remain available through the dedicated Yield
Prediction workflow. They are not mixed into the factual harvest summary or
harvest-based report totals.

Formula used in UI and validation flow:

$$
  ext{Historical Yield (tons/ha)} = \frac{\text{Historical Production (tons)}}{\text{Field Area (ha)}}
$$

### Field and Planting Management

- Field CRUD with ownership controls
- Planting records linked to fields and varieties
- Farm size auto-updates through model signal workflow

### Reports and Analytics

The Reports page uses active `HarvestRecord` data for its production metrics
within the selected date range, barangay filter, and role scope. Its summary
statistics are:

- Total Harvest Records
- Total Harvest Area (ha)
- Total Production (tons)
- Average Actual Yield (tons/ha)

Detailed report sections include actual yield by rice variety, rice production by
barangay, monthly detection breakdown, disease frequency, and detection details.
CSV and PDF exports use the same harvest summary and section definitions as the
Reports page. Disease frequency excludes unclassified or rejected scans, while
full detection details retain active records, including unclassified records,
for traceability.

Model metadata such as model version, model accuracy, detectable classes, and
last scan belongs to Dashboard > System Information rather than the
harvest-focused Reports summary.

### Role-Based Access Control (RBAC)

- Admin: full access
- Technician: operational access across farmers
- Farmer: own data only

### Notification and Announcement Delivery Policy (Current)

Current implementation is intentionally simple (no Celery/Redis worker). Email work
is started after a successful database commit in a lightweight background thread,
so settings saves and notification creation do not wait for SMTP delivery:

- System Settings updates create in-app notifications immediately.
- Notification email delivery runs in the background after commit.
- Announcement email delivery follows the same background pattern.
- When Email Notifications is disabled, in-app notifications continue to work
  while outgoing email is skipped.
- System Settings links are included only for administrator recipients; farmers
  and technicians receive an awareness message because the page is
  administrator-only.

Because these threads are process-local and non-durable, a Gunicorn restart or
process crash can interrupt an email. Use Celery + Redis (or another durable
worker) when guaranteed delivery and retries are required.

Email troubleshooting:

- The System Settings page shows whether email delivery is disabled, ready, or
  missing SMTP configuration.
- Detailed failures remain available in the Django/Gunicorn error logs without
  exposing SMTP credentials.

System Settings UX:

- The save loader uses staged progress steps and remains visible for a minimum
  display interval so fast responses do not make the animation flash.
- Email readiness is shown in the Email Notifications section, not inside the
  visual save loader.

- Immediate Publish:
  - sends announcement email (if email is enabled and SMTP is configured)
  - creates in-app advisory notification
  - announcement becomes visible to target users
- Scheduled Publish:
  - does not send announcement email
  - creates in-app advisory notification when schedule becomes due
  - announcement becomes visible when publish time is due

Scheduling behavior note:

- Due scheduled dispatch runs through normal app traffic.
- If there is no incoming request around the due time, notification creation can be delayed until the next request.

## Project Structure

```text
mysite/
|-- manage.py
|-- requirements.txt
|-- mysite/              # Django settings, urls, wsgi, asgi
|-- polls/               # Main app (models, views, forms, services)
|-- templates/           # UI templates
|-- models/              # ML artifacts (.tflite, .joblib, metadata)
|-- dataset/             # Training/evaluation data assets
`-- media/               # Uploaded files (detections, knowledge images)
```

## Useful Commands

```bash
# Validate Django project configuration
python manage.py check

# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run tests (if test suite exists)
python manage.py test
```

## API Snapshot

Example internal endpoint:

```http
GET /api/planting/<id>/
```

Typical response fields:

```json
{
  "area": 5.0,
  "variety": "Rc222",
  "planting_date": "2026-01-15",
  "growth_duration_days": 120,
  "historical_production_tons": 10.5,
  "historical_yield_tons_per_ha": 2.1,
  "field_name": "Rice Field A"
}
```

## Testing Checklist (Manual)

- Create/edit/delete field and verify farm size recomputes
- Run detection and open yield prediction from detection context
- Verify locked auto-filled fields and editable historical fields
- Confirm real-time yield auto-calc on production input
- Validate RBAC behavior by role (Admin/Technician/Farmer)

## Troubleshooting

### CNN model not available in Yield Tool

- Ensure `models/rice_yield_CNN.pth` exists.
- Ensure `torch`/`torchvision` are installed in the active environment.
- Check System Settings: `yield_cnn_enabled` is ON.
- If System Settings row is absent, verify `YIELD_CNN_ENABLED=True` in env for fallback behavior.

### Signals not firing for farm size

- Confirm polls.apps.PollsConfig is in INSTALLED_APPS
- Confirm signals are imported in PollsConfig.ready()

### Yield auto-calc not updating

- Check browser console for JavaScript errors
- Ensure area and production fields have numeric values
- Reset manual-edit state in the yield field if present

### Empty planting options

- Confirm planting records exist
- Confirm role-based queryset filtering is correct for the logged-in user

### Emails not sending

- Check System Settings: `email_enabled` is ON.
- If SiteSetting row is absent, verify env fallback `EMAIL_ENABLED=True`.
- Verify SMTP values (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`).
- For announcements, email is sent only for Immediate Publish.
- Scheduled Publish is notification-only by current system policy.

## Security Notes

- Do not commit real email app passwords, database passwords, or secret keys
- Rotate any credential that was exposed in repository history
- Keep DEBUG=False in production

## License

Proprietary - Department of Agriculture

## Maintainer Notes

- Keep this README focused on operational setup and core workflows
- Put deep technical docs in documentation.md 
Version: 1.6.0
Last updated: 2026-04-01
