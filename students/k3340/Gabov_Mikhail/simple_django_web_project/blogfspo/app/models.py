from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class Owner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner')
    last_name = models.CharField(max_length=30, null=False)
    first_name = models.CharField(max_length=30, null=False)
    birth_date = models.DateField(null=True)
    cars = models.ManyToManyField('Car', through='CarOwner')

    def __str__(self):
        return f"({self.id}): {self.first_name} {self.last_name}"

class Car(models.Model):
    license_plate = models.CharField(max_length=15, null=False)
    brand = models.CharField(max_length=20, null=False)
    model = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=20, null=True)
    owners = models.ManyToManyField(Owner, through='CarOwner')

    def __str__(self):
        # return "{} {}".format(self.brand, self.model)
        return f"CarID({self.id}): {self.brand} {self.model}"

class CarOwner(models.Model):
    owner_id = models.ForeignKey(Owner, null=True, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car, null=True, on_delete=models.CASCADE)
    date_start = models.DateField(null=False)
    date_end = models.DateField(null=True)

    def __str__(self):
        return f"OwnerID{self.owner_id} | {self.car_id}"

class DriverLicense(models.Model):
    owner_id = models.ForeignKey(Owner, null=False, on_delete=models.CASCADE)
    driver_license = models.CharField(max_length=10, null=False)
    type = models.CharField(max_length=10, null=False)
    date_issued = models.DateField(null=False)

class User(AbstractUser):
    passport_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"