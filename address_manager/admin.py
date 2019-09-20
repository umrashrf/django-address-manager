from django.contrib import admin

from .models import AddressUnitList, AddressWebsite, Address

admin.site.register(AddressUnitList)
admin.site.register(AddressWebsite)
admin.site.register(Address)
