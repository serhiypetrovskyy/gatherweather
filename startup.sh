
#!/bin/bash

# Set the environment variables
export LANG=C.UTF-8

# Start Gunicorn
gunicorn -b 0.0.0.0:8000 --timeout 600 your_project_name.wsgi &

# Start Celery Worker
celery -A your_project_name worker -l info &

# Start Celery Beat
celery -A your_project_name beat -l info
