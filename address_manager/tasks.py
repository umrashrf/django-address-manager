from __future__ import absolute_import, unicode_literals
from django.db.models import Q
from dynamic_scraper.utils.task_utils import TaskUtils
from celery.decorators import task

from address_manager.models import AddressWebsite, Address

@task
def run_spiders():
    t = TaskUtils()
    kwargs = {
    }
    args = (Q(),)
    t.run_spiders(AddressWebsite, 'scraper', 'scraper_runtime', 'hydro_quebec', *args, **kwargs)

@task
def run_checkers():
    t = TaskUtils()
    kwargs = {
    }
    args = (Q(),)
    t.run_checkers(Address, 'source__scraper', 'checker_runtime', 'hydro_quebec_checker', *args, **kwargs)
