release: python manage.py migrate --noinput && python manage.py loaddata address_manager/fixtures/*.json
web: gunicorn address_manager.wsgi
