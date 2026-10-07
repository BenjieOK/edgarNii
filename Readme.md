# Nii Kpakpo Campaign Site

Django site for campaign content, pages, contact messages, and admin-managed homepage sections.

## Local Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Create a local environment file:

   ```bash
   cp .env.example .env
   ```

   For local SQLite development, keep `DB_ENGINE` empty.

4. Apply migrations and load starter content:

   ```bash
   python manage.py migrate
   python seed_data.py
   python manage.py createsuperuser
   ```

5. Run the app:

   ```bash
   python manage.py runserver
   ```

## Supabase Database Setup

Supabase provides a managed PostgreSQL database. This Django app can keep using SQLite locally and use Supabase by setting environment variables in staging/production.

1. Create a Supabase project.
2. Open the project database connection settings and copy the Postgres host, database, user, password, and port.
3. Set these variables in your deployment environment:

   ```bash
   DJANGO_SECRET_KEY=<strong-production-secret>
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=<your-domain>,<your-app-host>
   DB_ENGINE=postgres
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=<supabase-database-password>
   DB_HOST=<supabase-postgres-host>
   DB_PORT=5432
   DB_SSLMODE=require
   ```

4. Install dependencies, then run:

   ```bash
   python manage.py migrate
   python seed_data.py
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

   `collectstatic` gathers static files into `staticfiles/`, which WhiteNoise serves directly — Supabase only hosts the database, so the Django app itself still needs to run somewhere (Render, Railway, Fly.io, etc.) with `DJANGO_DEBUG=False`.

Use the Supabase database password only on the server or deployment platform. Do not commit `.env` files or passwords.

## Environment Guide

Local development:
Use SQLite by leaving `DB_ENGINE` blank. Keep `DJANGO_DEBUG=True` and `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1`.

Staging:
Use a separate Supabase project or database branch if available. Set `DJANGO_DEBUG=False`, use a staging-only `DJANGO_SECRET_KEY`, and set `DJANGO_ALLOWED_HOSTS` to the staging domain.

Production:
Use the production Supabase project, `DJANGO_DEBUG=False`, a unique secret key, and only the live domain/app host in `DJANGO_ALLOWED_HOSTS`. Run migrations during deployment before serving traffic.
