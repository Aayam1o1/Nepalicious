from django import forms
from .models import *


class addRestaurantForm(forms.ModelForm):
    
    restaurantDescription = forms.CharField(
        label = 'Recipe Description',
        max_length = 400,
        widget=forms.Textarea(attrs={'placeholder': 'Product Description', 'class': 'border-2 border-gray-400 rounded-xl p-2 mt-2 w-[25rem] bg-gray-100', 'rows': 6, 'cols': 60})    )
    
    restaurantType = forms.ChoiceField(
        choices=types,
        widget=forms.Select(attrs={'class': 'border-2 border-gray-400 rounded-xl p-2 w-[25rem] bg-gray-100'}),
        required=True
    )
    
    class Meta:
        model = addRestaurant
        fields = ['restaurantDescription', 'restaurantType']

       
class FeedbackForm(forms.ModelForm):
   
    class Meta:
        model = restaurantFeedback
        fields = ['feedback', 'rating']