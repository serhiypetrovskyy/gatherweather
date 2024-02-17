export LANG=C.UTF-8

celery -A config worker -l INFO -B & gunicorn --bind=0.0.0.0 --timeout 600 config.wsgi



