# Contalink Test - Backend

REST API for invoice consultation with a background job that sends a daily top 10 sales email.

## Requirements

- Docker and Docker Compose
- **(Alternative for manual setup) Python 3.12+ and access to a Redis instance**

## Quick Start (Docker)

1. Clone the repository:
```bash
   git clone https://github.com/Abbygor/contalink-test-backend.git
   cd contalink-test-backend
```

2. Create your `.env` file from the example:
```bash
   cp .env.example .env
```

3. Edit `.env` and set the required values. At minimum, you must set:
   - `DJANGO_SECRET_KEY` — any random string for local development
   - `DATABASE_PASSWORD` — the database password provided by Contalink

   See [Environment Variables](#environment-variables) for the full list.

4. Start all services:
```bash
   docker-compose up --build
```

The API will be available at `http://localhost:8000`.

## Manual Setup (without Docker)

If you prefer to run the project without Docker:

1. Create and activate a virtual environment:
```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .\.venv\Scripts\Activate.ps1  # Windows
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Make sure Redis is running locally on port 6379. With Docker:
```bash
   docker run -d --name redis -p 6379:6379 redis:7-alpine
```

4. Update `.env` to point to local Redis:
```bash
    REDIS_URL=redis://localhost:6379/0
    CELERY_BROKER_URL=redis://localhost:6379/1
    CELERY_RESULT_BACKEND=redis://localhost:6379/2
```
5. Run the API:
```bash
   python manage.py runserver
```

6. In separate terminals, run the Celery worker and beat:
```bash
   celery -A config worker --loglevel=info --pool=solo
   celery -A config beat --loglevel=info
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django secret key | Required |
| `DJANGO_DEBUG` | Enable debug mode | `False` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `DATABASE_HOST` | PostgreSQL host | Required |
| `DATABASE_PORT` | PostgreSQL port | `5432` |
| `DATABASE_NAME` | Database name | Required |
| `DATABASE_USER` | Database user | Required |
| `DATABASE_PASSWORD` | Database password | Required |
| `REDIS_URL` | Redis URL for cache | Required |
| `CELERY_BROKER_URL` | Redis URL for Celery broker | Required |
| `CELERY_RESULT_BACKEND` | Redis URL for Celery results | Required |
| `CELERY_BEAT_HOUR` | Hour to send the daily email | `8` |
| `CELERY_BEAT_MINUTE` | Minute to send the daily email | `0` |
| `CORS_ALLOWED_ORIGINS` | Allowed CORS origins | Empty |
| `EMAIL_BACKEND` | Email backend class | Console backend |
| `EMAIL_HOST` | SMTP host | Empty |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_HOST_USER` | SMTP user | Empty |
| `EMAIL_HOST_PASSWORD` | SMTP password | Empty |
| `EMAIL_USE_TLS` | Use TLS for SMTP | `True` |
| `EMAIL_FROM` | Sender email address | Required |
| `EMAIL_TO` | Recipient email address | Required |

### Email Configuration

By default, `.env.example` uses the console backend, which prints emails to the worker's logs instead of sending them. This is convenient for local development and avoids requiring real SMTP credentials to run the project.
```bash
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```
To send real emails, switch to the SMTP backend and configure the SMTP variables:
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
EMAIL_FROM=your-email@gmail.com
EMAIL_TO=recipient@example.com
```
For Gmail, you need to generate an App Password from your Google account settings (2FA must be enabled).
## Running Tests

Tests are hermetic and do not require Redis or database access:

```bash
pytest
```

With verbose output:

```bash
pytest -v
```

## Project Structure

```
contalink-test-backend/
├── apps/
│   └── invoices/          # Main domain app
│       ├── api/           # HTTP layer (views, serializers, urls, cache)
│       ├── tests/         # Tests for services, views, and tasks
│       ├── apps.py
│       ├── models.py      # Invoice model
│       ├── services.py    # Business logic
│       └── tasks.py       # Celery tasks
├── config/                # Django project config
│   ├── celery.py          # Celery initialization
│   ├── settings.py        # Django settings
│   └── urls.py            # Root URL config
├── .dockerignore
├── .env.example
├── .gitignore
├── conftest.py            # Pytest fixtures (root)
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── pytest.ini
├── requirements.txt
└── README.md
```
## Services

When running with Docker Compose, four services are orchestrated:

- **redis**: Cache and Celery broker (port 6379)
- **api**: Django REST API (port 8000)
- **worker**: Celery worker that processes background tasks
- **beat**: Celery beat scheduler that triggers the daily email task

## API Endpoints

### `GET /api/invoices/`

Returns a paginated list of invoices filtered by date range.

**Query parameters:**
- `start_date` (required): Start date in `YYYY-MM-DD` format
- `end_date` (required): End date in `YYYY-MM-DD` format

**Example:**

```bash
curl "http://localhost:8000/api/invoices/?start_date=2022-01-01&end_date=2022-01-31"
```

**Response:**

```json
{
  "count": 1234,
  "next": "http://localhost:8000/api/invoices/?page=2&...",
  "previous": null,
  "results": [
    {
      "id": 1,
      "invoice_number": "C30471",
      "total": "14.45",
      "invoice_date": "2022-01-17T09:27:44-06:00",
      "status": "Vigente"
    }
  ]
}
```