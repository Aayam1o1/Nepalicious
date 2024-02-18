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

# render header
def header(request):
    return render(request, 'headerFooter/header.html')

#Login
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
            
        if user is not None:
            login(request, user)
            
            # Check if the user is an admin
            if user.username == "admin":
                return redirect('adminHome')
            else:
                try:
                    user_profile = usersDetail.objects.get(user=user)
                    user_type = user_profile.requestedGroup
                    messages.success(request, f"Logged in as {username}. User type: {user_type}")
                except usersDetail.DoesNotExist:
                    messages.warning(request, f"User profile not found for {username}")
                return redirect('index')

        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, 'login-Register/login.html')



# REGISTER
def registerUser(request):
    form = CreateUserForm()

    # Get the requested group
    if "UserRequestedGroup" in request.POST:
        userRequestedGroup = request.POST.get('UserRequestedGroup')

    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)
        
        if form.is_valid():
            #Getting Username
            username = form.cleaned_data.get('username')
            
            #Getting profilePicture
            profilePicture = request.FILES.get('profileImg')
            print("This is: ",profilePicture)
            #transcation holds the process until the process is completed
            #and only lets the process complete when all the conditions are met
            #if condition are not met it undo all the changes made
            with transaction.atomic():
                user = form.save()
                # saving details of the user
                userDetails = usersDetail(user=user, address = request.POST.get('address'), phone_number = request.POST.get('contact_number'),requestedGroup = userRequestedGroup)
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
                    print("Xa rw?")
                    images=request.FILES.getlist('documentImage')

                    for img in images:
                        documentImg = userDocument(user=user, documentImage=img)
                        documentImg.save()
                    messages.success(request,"Account Created for " + username + " Please wait before we verify.")
                    
                else:
                    group, create = Group.objects.get_or_create(name = 'user')
                    user.groups.add(group)
                    messages.success(request,"Account Created for " + username)
                print("Choosen Group is: ", userRequestedGroup)
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

# Profile
@login_required(login_url='login')
def profile(request):
    #getting profile image for displating
    profile_image_url = None
    try:
        profile_image_url = request.user.userprofilepicture.profileImage.url
    except UserProfilePicture.DoesNotExist:
        pass

    context = {
        
        'profile_image_url': profile_image_url, 
    }
    return render(request, 'profiles/profile.html')


#edit profile page
@login_required(login_url='login')
def editprofile(request):
    #getting profile image for displating
    profile_image_url = None
    try:
        profile_image_url = request.user.userprofilepicture.profileImage.url
    except UserProfilePicture.DoesNotExist:
        pass
    
    if request.method == 'POST':
        if "user" in request.POST:
                username = request.POST.get('user')
                user = User.objects.get(username=username)
                
        if "update" in request.POST:
            # UPDATING USER MODEL
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            #saving the updated data
            user.save()
            
            # UPDATING userdetail MODEL
            user.usersdetail = user.usersdetail
            user.usersdetail.phone_number = request.POST.get('phone_number')
            user.usersdetail.address = request.POST.get('address')
            
            #saving the updated data
            user.usersdetail.save()
            msg = "Profile Updated"
            messages.success(request, 'Profile Updated')           
               
        #  for uploading new profile picture
        if "saveImage" in request.POST:
            # Saving user New profile
            user_profile = UserProfilePicture.objects.get(user=user)
            user_profile.profileImage  = request.FILES['img']
            user_profile.save()
            messages.success(request, 'Profile Picture Updated')
        
        # for setting default profile
        if "deleteImage" in request.POST:
            user_profile = UserProfilePicture.objects.get(user=user)
            user_profile.delete()
            # Saving user default profile
            user_default_profile_picture, created = UserProfilePicture.objects.get_or_create(user=user)

            if not created:
                user_default_profile_picture.profileImage = defaultProfilePicture()
                user_default_profile_picture.save()
          
            messages.success(request, 'Profile Picture updated.')         
                
    context = {
        
        'profile_image_url': profile_image_url, 
    }
    return render(request, 'profiles/editprofile.html', context)

def changePassword(request):
    return render(request, 'profiles/changepassword.html')