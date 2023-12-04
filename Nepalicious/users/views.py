from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from django.contrib import messages

#update_auth_hass used to change password
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from users.models import *
from django.db import transaction
from django.contrib.auth.models import User,Group

# SEND MAIL
from django.core.mail import send_mail
# Create your views here.

#Login
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
            
            
        if user is not None:
            login(request, user)
             
            return redirect('index')

        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, 'login-Register/login.html')



# REGISTER
def registerUser(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            #Getting Username
            username = form.cleaned_data.get('username')
            #transcation holds the process until the process is completed
            #and only lets the process complete when all the conditions are met
            #if condition are not met it undo all the changes made
            with transaction.atomic():
                user = form.save()
                # saving details of the user
                userDetails = userDetail(user=user, contactNumber = request.POST.get('contactNumber'))
                userDetails.save()
                return redirect('login')
            
    context={
        'form': form
    }
                    
    return render(request, 'login-Register/register.html', context)


#Logout
def logoutUser(request):
    logout(request)
    return redirect('login')
