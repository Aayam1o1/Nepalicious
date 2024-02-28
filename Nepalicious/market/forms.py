from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django import forms
from .models import *


class addProductForm(ModelForm):
    class Meta:
        model = addProducts
        widgets = {
            'productDescription': forms.Textarea(attrs={'rows':4, 'cols':15}),
            'productPrice': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
            'productStock': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
        }
        exclude = ('user',)
        fields = "__all__"