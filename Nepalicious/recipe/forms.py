from django.forms import ModelForm, ChoiceField, Select, MultipleChoiceField
from django.contrib.auth.forms import User
from django import forms
from .models import *



class addRecipeForm(ModelForm):
    recipeName = forms.CharField(
        label = 'Recipe Name',
        max_length = 50,
        widget=forms.TextInput(attrs={'placeholder': 'Recipe Name', 'class' : 'border-2 border-gray-400 rounded-xl p-2 mt-2 mb-5 w-[25rem] bg-gray-100 '})
    )
    
    recipeDescription = forms.CharField(
        label = 'Recipe Description',
        max_length = 400,
        widget=forms.Textarea(attrs={'placeholder': 'Product Description', 'class': 'border-2 border-gray-400 rounded-xl p-2 mt-2 mb-5 w-[25rem] bg-gray-100', 'rows': 6, 'cols': 60})    )
    
    cuisineType = forms.ChoiceField(
        choices=cuisine,
        widget=forms.Select(attrs={'class': 'border-2 border-gray-400 rounded-xl p-2 mt-2 mb-5 w-[25rem] bg-gray-100'}),
        required=True
    )
    
    
    class Meta:
        model = addRecipe
        fields = ['recipeName', 'recipeDescription', 'cuisineType' ]
        
        
class FeedbackForm(forms.ModelForm):
    feedback = forms.CharField(
        label='',  # Set the label for the 'feedback' field to an empty string
        widget=forms.Textarea(attrs={'placeholder': 'Your feedback...', 'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'rows': 4, 'cols': 60}),
    )

    class Meta:
        model = recipeFeedback
        fields = ['feedback']
