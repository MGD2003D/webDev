from django.contrib import admin
from .models import Owner, CarOwner, Car, DriverLicense

# Register your models here.
admin.site.register(Owner)
admin.site.register(CarOwner)
admin.site.register(Car)
admin.site.register(DriverLicense)