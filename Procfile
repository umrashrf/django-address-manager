release: python manage.py migrate dynamic_scraper --noinput && python manage.py migrate --noinput
web: gunicorn address_manager.wsgi