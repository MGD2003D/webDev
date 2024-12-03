from django import forms
from .models import Car, CarOwner, Owner, User
from django.contrib.auth.forms import UserCreationForm

class CarCreateForm(forms.ModelForm):

    class Meta:
        model = Car

        fields = [
            'brand',
            'model',
            'color',
            'license_plate'
        ]

class OwnerCreateForm(forms.ModelForm):

    class Meta:
        model = Owner

        fields = [
            'last_name',
            'first_name',
            'birth_date'
        ]

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'email',
            'passport_number',
            'address',
            'nationality',
            'birth_date',
        ]