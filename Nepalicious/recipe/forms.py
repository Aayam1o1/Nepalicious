from django.forms import ModelForm, ChoiceField, Select, MultipleChoiceField
from django.contrib.auth.forms import User
from django import forms
from .models import *
from django.core.exceptions import ValidationError



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
    video = forms.CharField(
        label = 'Video URL',
        max_length = 500,
        widget=forms.TextInput(attrs={'placeholder': 'Add Video URL', 'class' : 'border-2 border-gray-400 rounded-xl p-2 mt-2 mb-5 w-[25rem] bg-gray-100 '}),
        required=False
    )
    
    def clean_video(self):
        video_url = self.cleaned_data.get('video')
        
        if video_url:
            supported_platforms = ['youtube.com', 'vimeo.com', 'dailymotion.com']  # Supported video platforms
            
            if not any(platform in video_url for platform in supported_platforms):
                raise ValidationError("Please provide a valid video URL from YouTube, Vimeo, or Dailymotion.")
        
        return video_url
    
    class Meta:
        model = addRecipe
        fields = ['recipeName', 'recipeDescription', 'cuisineType', 'video']
        
        
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = recipeFeedback
        fields = ['feedback']
        
class editRecipeForm(ModelForm):
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
    video = forms.CharField(
        label = 'Video URL',
        max_length = 500,
        widget=forms.TextInput(attrs={'placeholder': 'Add Video URL', 'class' : 'border-2 border-gray-400 rounded-xl p-2 mt-2 mb-5 w-[25rem] bg-gray-100 '}),
        required=False
    )
    
    def clean_video(self):
        video_url = self.cleaned_data.get('video')
        
        if video_url:
            supported_platforms = ['youtube.com', 'vimeo.com', 'dailymotion.com']  # Supported video platforms
            
            if not any(platform in video_url for platform in supported_platforms):
                raise ValidationError("Please provide a valid video URL from YouTube, Vimeo, or Dailymotion.")
        
        return video_url
    
    class Meta:
        model = addRecipe
        fields = ['recipeName', 'recipeDescription', 'cuisineType', 'video']      
