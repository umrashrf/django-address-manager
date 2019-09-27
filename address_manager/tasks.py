from celery.task import task
from django.db.models import Q
from dynamic_scraper.utils.task_utils import TaskUtils
from address_manager.models import AddressWebsite, Address


@task()
def run_spiders():
    t = TaskUtils()
    kwargs = {
        'scrape_me': True,
    }
    args = (Q(name='Address'),)
    t.run_spiders(AddressWebsite, 'scraper', 'scraper_runtime', 'hydro_quebec_spider', *args, **kwargs)


@task()
def run_checkers():
    t = TaskUtils()
    kwargs = {
        'check_me': True,
    }
    args = (Q(id__gt=100),)
    t.run_checkers(Address, 'address_website__scraper', 'checker_runtime', 'hydro_quebec_checker', *args, **kwargs)
