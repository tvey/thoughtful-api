web: gunicorn core.wsgi:application --log-file=-

release: django-admin migrate --no-input && django-admin collectstatic --no-input
