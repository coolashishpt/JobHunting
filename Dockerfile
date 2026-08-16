FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install build deps and clean apt caches
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc && rm -rf /var/lib/apt/lists/*

# Install python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app

# Collect static files
ENV DJANGO_SETTINGS_MODULE=jobhunting.settings
ENV PYTHONUNBUFFERED=1
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000
CMD ["gunicorn", "jobhunting.wsgi:application", "--bind", "0.0.0.0:8000"]
