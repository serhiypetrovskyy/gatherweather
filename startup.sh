
#!/bin/bash

# Set the environment variables
export LANG=C.UTF-8

# Start Gunicorn
gunicorn -b 0.0.0.0:8000 --timeout 600 WeatherReminder.wsgi &

# Start Celery Worker
celery -A WeatherReminder worker -l info &

# Start Celery Beat
celery -A WeatherReminder beat -l info
