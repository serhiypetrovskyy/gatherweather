# Start Gunicorn
gunicorn --bind=0.0.0.0 --timeout 600 WeatherReminder.wsgi &

# Start Celery Worker
celery -A WeatherReminder worker -l info &

# Start Celery Beat
celery -A WeatherReminder beat -l info
