from django import forms
from .models import Car

class PostForm(forms.ModelForm):

    class Meta:
        model = Car
        template_name = 'car_create.html'

        fields = [
            'brand',
            'model',
            'color',
            'owners',
            'license_plate'
        ]