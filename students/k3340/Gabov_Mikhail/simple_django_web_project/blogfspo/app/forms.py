from django import forms
from .models import Car, CarOwner

class PostForm(forms.ModelForm):

    class Meta:
        model = Car
        template_name = 'car_create.html'

        fields = [
            'brand',
            'model',
            'color',
            'license_plate'
        ]