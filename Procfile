web: gunicorn config.wsgi:application
worker: celery worker --app=stripe_pizza.taskapp --loglevel=info
