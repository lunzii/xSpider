
python manage.py celery worker --loglevel=info

lsof -i -n -P | grep 8000