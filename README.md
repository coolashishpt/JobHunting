# JobHunting

A server-rendered job-hunting platform built with Django and Bootstrap. This project implements candidate and recruiter workflows (profiles, job posting, applications), resume upload and management, application tracking, and basic notifications. It is configured for local development with SQLite and supports a production-ready deployment using Docker Compose, Redis, Celery, and Gunicorn.

## Features
- User registration, login, logout, and password reset (Django auth)
- Candidate and recruiter roles (Profile model)
- Candidate profile: skills, experience, location, resume upload
- Job posting, editing, publishing, and closing (recruiter)
- Job search with filters: location, skills, salary, job type, remote
- Apply for jobs and track application status
- Recruiter dashboard: view applicants, change status, add feedback
- Candidate dashboard: saved jobs, application history, recruiter feedback
- Email notifications for application status changes (Celery tasks)
- Local MEDIA file handling and static assets (Bootstrap)

## Technology stack
- Python 3.11, Django 5.1
- PostgreSQL encouraged for production (SQLite used for dev)
- Celery + Redis for async tasks (email sending)
- Gunicorn as WSGI server
- Docker & Docker Compose for development/production orchestration
- Bootstrap for server-rendered UI

## Getting started (local, without Docker)
1. Clone the repository and create a virtualenv:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate    # Windows
   source .venv/bin/activate   # macOS / Linux
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy environment example and set values:
   ```bash
   cp .env.example .env
   # Edit .env to set DJ_SECRET_KEY and other production values
   ```
4. Run migrations and create a superuser:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Run the dev server:
   ```bash
   python manage.py runserver 127.0.0.1:8000
   ```
6. Open http://127.0.0.1:8000 in your browser. Admin is at `/admin/`.

## Environment variables
Use `.env` (see `.env.example`) for configuration. Important variables:
- DJ_SECRET_KEY - Django secret key
- DJ_DEBUG - `True` or `False`
- DJ_ALLOWED_HOSTS - comma separated hosts (e.g. `localhost,127.0.0.1`)
- DJ_DEFAULT_FROM_EMAIL - default sender address
- DJ_EMAIL_HOST, DJ_EMAIL_PORT, DJ_EMAIL_HOST_USER, DJ_EMAIL_HOST_PASSWORD, DJ_EMAIL_USE_TLS/SSL - SMTP settings (optional)
- DJ_CELERY_BROKER_URL, DJ_CELERY_RESULT_BACKEND - Celery broker/back-end (defaults to Redis)

By default the project uses Django's console email backend for development.

## Running async tasks (Celery)
This project uses Celery to deliver application notification emails asynchronously.

Locally using Docker Compose (recommended):
```bash
# starts Redis, web and worker
docker compose up --build
```
Or manually:
1. Start Redis (e.g., `docker run -p 6379:6379 redis:7`).
2. Start a Celery worker from the project root:
   ```bash
   celery -A jobhunting worker --loglevel=info
   ```

When application status changes the notification is queued as a Celery task.

## Running with Docker Compose
The repository includes `docker-compose.yml` to run services:
- redis: message broker
- web: Django + Gunicorn
- worker: Celery worker

Bring up services:
```bash
docker compose up --build
```
Data persisted to named volumes for static and media files.

## Database & production notes
- SQLite is used for quick local dev. For production, switch to PostgreSQL and update `DATABASES` in settings or use `DATABASE_URL` environment style.
- Set `DJ_DEBUG=False`, configure `DJ_ALLOWED_HOSTS`, `DJ_SECRET_KEY`, and real SMTP settings.
- Secure Redis in production; run Celery workers with appropriate concurrency and monitoring.
- Consider using S3 or another object store for persistent MEDIA in production.

## Tests
Run Django tests locally:
```bash
python manage.py test
```

## Common commands
- Run migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`
- Collect static: `python manage.py collectstatic --noinput`
- Run management command inside Docker: `docker compose run --rm web python manage.py <command>`

## Contributing
Contributions welcome. Create issues for bugs or feature requests, branch from `main`, and open a PR against the repository.

## License
This repository does not include a license file. Add an appropriate open-source license before publishing publicly.

---

If you'd like, I can also add a short deployment guide (systemd + Gunicorn + nginx) or switch the README to include a README-specific badge and quick-start script. Let me know which extra docs to add.