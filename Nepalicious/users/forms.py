from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django import forms


# form to store User data
class CreateUserForm(UserCreationForm):
    class Meta:
        model= User
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2']
        requestedGroup = forms.CharField(initial='user')
    