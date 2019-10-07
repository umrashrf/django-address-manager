build:
	docker-compose build

start:
	docker-compose up -d

setup:
	docker-compose run web python manage.py migrate --no-input
	docker-compose run web python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@localhost', 'admin')"
	docker-compose run web python manage.py loaddata address_manager/fixtures/*.json

stop:
	docker-compose down

clean: stop
	docker-compose rm -f

reset: clean build start setup
	docker-compose logs -f
