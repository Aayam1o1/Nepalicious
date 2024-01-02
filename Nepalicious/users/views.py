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

# render index page
def index(request):
    return render(request, 'landingPage/index.html')  

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
            
            #Getting profilePicture
            profilePicture = request.FILES.get('profileImg', None)
            
            #transcation holds the process until the process is completed
            #and only lets the process complete when all the conditions are met
            #if condition are not met it undo all the changes made
            with transaction.atomic():
                user = form.save()
                # saving details of the user
                userDetails = usersDetail(user=user, address = request.POST.get('address'), requestedGroup = request.POST.get('requestedGroup'))
                userDetails.save()
                
                 #Creating an instance and saving it to the database is necessary
                # to persist the user's profile picture information. In the first case, we save the user's uploaded picture,
                # and in the second case, we save a default picture or an empty picture, 
                # indicating that the user did not provide a custom profile picture.

                # Without creating and saving an instance,
                # the information about the user's profile picture 
                # (whether it's a custom picture or default) won't be stored in the database,
                # and you won't be able to retrieve it later when needed.

                if profilePicture:
                    profilePictureInstance = UserProfilePicture(user=user, profileImage=profilePicture)
                    profilePictureInstance.save()
                else:
                    # If no picture is uploaded, use the default picture
                    profilePictureInstance = UserProfilePicture(user=user)
                    profilePictureInstance.save()

                if request.FILES:
                
                    images=request.FILES.getlist('documentImg')

                    for img in images:
                        documentImg = userDocument(user=user, documentImage=img)
                        documentImg.save()
                    messages.success(request,"Account Created for " + username + " Please wait before we verify.")
                    
                else:
                    group, create = Group.objects.get_or_create(name = 'user')
                    user.groups.add(group)
                    messages.success(request,"Account Created for " + username)
                
                return redirect('login')
            
    context={
        'form': form
    }
                    
    return render(request, 'login-Register/register.html', context)


#Logout
def logoutUser(request):
    logout(request)
    return redirect('login')

def is_superuser(user):
    return user.is_superuser




@login_required(login_url='login')
@user_passes_test(is_superuser)
def adminDashboard(request):
    
    # IF  APPROVED
    if request.method == 'POST' and 'approve' in request.POST:
        if 'group' in request.POST:
            username = request.POST.get('user')
            user = User.objects.get(username=username)
            userGroup = request.POST.get('group')
            group, created = Group.objects.get_or_create(name=userGroup)
            user.groups.add(group)
                
        else:
            pass
    
    # allUser = User.objects.filter(groups__name__in=['chef', 'restaurant', 'vendor', 'user'])
    # totalUsers = User.objects.filter(groups__name__in=['chef', 'restaurant', 'vendor','user']).count()
    
    
    
    requestedUserType = usersDetail.objects.all()
    
    totalChef = User.objects.filter(groups__name='chef').exclude(is_superuser=True).count()
    totalRestaurant = User.objects.filter(groups__name='restaurant').exclude(is_superuser=True).count()
    totalVendor = User.objects.filter(groups__name='vendor').exclude(is_superuser=True).count()
    requestedRestaurant = usersDetail.objects.filter(requestedGroup='restaurant')
    print(requestedRestaurant)
    
    context = {
        'requestedUserType': requestedUserType,
        'totalChef' : totalChef,
        'totalRestaurant' : totalRestaurant,
        'totalVendor' : totalVendor,
        'requestedRestaurant' : requestedRestaurant
        
    }
    
    return render(request, 'admin/adminDashboard.html', context)


def userRequests(request, userID):
    
    if request.method == 'POST':
        if "approve" in request.POST:
            if "user" in request.POST:
                username = request.POST.get("user")
                user = User.objects.get(username=username)

                UserEmail = user.email
                
                # CODE FOR allocating DIFF USER group
                # FOR VENDOR group
                group, created = Group.objects.get_or_create(name='vendor')
                user.groups.add(group)

                # Sending mail after user is approved
                send_mail(
                "Account Approved",
                "Your account has been approved on Nepalicious.",
                "nepalicious.webapp@gmail.com",
                [UserEmail],
                fail_silently=False,
                )
                return redirect('adminHome')
            
        else:
            if "user" in request.POST:
                username = request.POST.get("user")
                user = User.objects.get(username=username)
                UserEmail = user.email 
                # Sending mail after user is approved
                send_mail(
                    "Account Rejected",
                    "Your account has been rejected on Nepalicious.",
                    "nepalicious.webapp@gmail.com",
                    [UserEmail],
                    fail_silently=False,)
                user.delete()
                return redirect('adminHome')
    
    print("USER ID IS: ", userID)
    
    userData = get_object_or_404(User, id=userID)
    
    document = userDocument.objects.filter(user=userData)
    
    requestedUserType = usersDetail.objects.all()
    
    context = {
        'requestedUserType': requestedUserType,
        'document': document,
        'userData': userData,
    }
    
    return render(request, 'admin/userRequests.html', context)