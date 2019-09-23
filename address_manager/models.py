from django.db import models
from dynamic_scraper.models import Scraper, SchedulerRuntime
from scrapy_djangoitem import DjangoItem


class AddressUnitList(models.Model):
    choice = models.CharField(max_length=150)

    def __str__(self):
        return self.choice


class AddressWebsite(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    scraper = models.ForeignKey(Scraper, blank=True, null=True, on_delete=models.SET_NULL)
    scraper_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Address(models.Model):
    street_number = models.CharField(max_length=500)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True)
    unit_type = models.ForeignKey(AddressUnitList, on_delete=models.CASCADE, blank=False)
    unit_number = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    zipcode = models.CharField(max_length=50)
    source = models.ForeignKey(AddressWebsite, on_delete=models.CASCADE)
    checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)
    note = models.TextField(blank=True)
    
    def __str__(self):
        return self.source

    def pre_delete(sender, instance, using):
        if isinstance(instance, Address):
            if instance.checker_runtime:
                instance.checker_runtime.delete()


class AddressItem(DjangoItem):
    django_model = Address
