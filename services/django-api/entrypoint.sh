#!/bin/sh
set -e

echo "Waiting for mysql..."
while ! nc -z mysql 3306; do
  sleep 1
done

echo "Waiting for redis..."
while ! nc -z redis 6379; do
  sleep 1
done

echo "Starting Django..."
cd /app
python manage.py makemigrations core || true
python manage.py migrate || true
python manage.py collectstatic --noinput || true
python manage.py runserver 0.0.0.0:8000
