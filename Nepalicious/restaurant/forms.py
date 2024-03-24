from django import forms
from .models import *


class SearchForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ['restaurantaddress', ]
        widgets = {
            'restaurantaddress': forms.TextInput(attrs={
                'placeholder': 'Search for city or address',
                'class': 'p-2.5 w-full z-20 text-sm text-gray-900 bg-gray-50 rounded-e-lg border-s-gray-50 border-s-2 border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-s-gray-700  dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:border-blue-500'
            }),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
