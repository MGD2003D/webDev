from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Owner, CarOwner, Car, DriverLicense, User

# Register your models here.
admin.site.register(Owner)
admin.site.register(CarOwner)
admin.site.register(Car)
admin.site.register(DriverLicense)

@admin.register(User)
class BaseUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('passport_number', 'address', 'nationality'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'passport_number', 'address', 'nationality', 'is_active', 'is_staff', 'is_superuser')