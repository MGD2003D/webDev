from django import forms
from .models import Car, CarOwner, Owner

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