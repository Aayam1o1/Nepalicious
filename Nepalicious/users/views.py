from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from django.contrib import messages

#update_auth_hass used to change password
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from users.models import *
from restaurant.models import *
from django.db import transaction
from django.contrib.auth.models import User,Group
import sweetify
import re

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
            if user.is_superuser:
                login(request, user)
                sweetify.success(request, f"logged in as admin")
                return redirect('adminHome')
            elif user.usersdetail.hasBlockedUser == True:
                sweetify.error(request, 'Your account has been blocked.')
                return redirect('login')
            
            else:
                
                login(request, user)

            
                try:
                    user_profile = usersDetail.objects.get(user=user)
                    user_type = user_profile.requestedGroup
                    sweetify.success(request, f"Logged in as {username}.")
                except usersDetail.DoesNotExist:
                    sweetify.warning(request, f"User profile not found for {username}")
                return redirect('index')

        else:
            sweetify.error(request, 'Username or Password is incorrect')

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
            
            if User.objects.filter(email=request.POST.get('email')).exists():
                sweetify.error(request, "Email already registered!")
                return redirect('register')
            if 'contact_number' in request.POST:
                contact_number = request.POST.get('contact_number')
                if not re.match(r'^(98|97)\d{8}$', contact_number):
                    sweetify.error(request,"Invalid contact number")
                    return redirect('register')
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
                userDetails = usersDetail(user=user, address = request.POST.get('address'), phone_number = request.POST.get('contact_number'), restaurant_name = request.POST.get('restaurant_name'), requestedGroup = userRequestedGroup)
                userDetails.save()
                
                if not userRequestedGroup or userRequestedGroup== "User":
                    group, create = Group.objects.get_or_create(name = 'user')
                    user.groups.add(group)
                
                
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
                    if not userRequestedGroup or userRequestedGroup == "User":
                        pass
                    else:
                        images=request.FILES.getlist('documentImage')

                        for img in images:
                            documentImg = userDocument(user=user, documentImage=img)
                            documentImg.save()
                        sweetify.success(request,"Account Created for " + username + " Please wait before we verify.")
                    
                else:
                    group, create = Group.objects.get_or_create(name = 'user')
                    user.groups.add(group)
                    sweetify.success(request,"Account Created for " + username)
                print("Choosen Group is: ", userRequestedGroup)
                return redirect('login')
        
        else:
            messasg_error = next(iter(form.errors.values()))[0]     # Retrieving the first error message from the form errors
            sweetify.error(request, messasg_error)

     
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



#for displaying users in admin dashboard
@login_required(login_url='login')
@user_passes_test(is_superuser)
def adminDashboard(request):
    
    if request.method == 'POST':
        print("CLICKED")
        
        if "block" in request.POST:
            username = request.POST.get("username")
            user = User.objects.get(username=username)
            userDetail = usersDetail.objects.get(user=user)
            UserEmail = request.POST.get("email")
            print("EMAIL" , UserEmail)
            userDetail.hasBlockedUser = True
            print("BLOCKED", userDetail.hasBlockedUser)
            userDetail.save()
            
            send_mail(
                "Account Blocked",
                "Your account has been blocked. Please contact your admin for more information :(",
                "nepalicious.webapp@gmail.com",
                [UserEmail],
                fail_silently=False,
                )
            sweetify.success(request, 'User Blocked successfully')
        
        elif "unblock" in request.POST:
            username = request.POST.get("username")
            user = User.objects.get(username=username)
            userDetail = usersDetail.objects.get(user=user)
            UserEmail = request.POST.get("email")
            userDetail.hasBlockedUser = False
            
            send_mail(
                "Account Unblocked",
                "Your account has been unblocked. You may now use the features of the webapp Nepalicious :)",
                "nepalicious.webapp@gmail.com",
                [UserEmail],
                fail_silently=False,
                )
            userDetail.save()
            sweetify.success(request, 'User Unblocked successfully')
    
    requestedUserType = usersDetail.objects.all() 
    
    allApprovedUsers = User.objects.filter(groups__name__in=['chef', 'vendor', 'user', 'restaurant'])
    
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
        'requestedRestaurant' : requestedRestaurant,
        'allApprovedUsers': allApprovedUsers,
        
    }
    
    return render(request, 'admin/adminDashboard.html', context)

# admin side user request handling
def userRequests(request, userID):
    allApprovedUsers = User.objects.filter(groups__name__in=['chef', 'vendor', 'user', '', 'restaurant'])

    if request.method == 'POST':
        if "approve" in request.POST:
            if "user" in request.POST:
                username = request.POST.get("user")
                user = User.objects.get(username=username)

                UserEmail = user.email
                requestedGroup = request.POST.get("requestedGroup").lower()
                
                # CODE FOR allocating DIFF USER group
                # FOR VENDOR group
                group, created = Group.objects.get_or_create(name=requestedGroup)
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
                # Sending mail after user is rejected
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
    documentImages = userDocument.objects.filter(user=userID)
    
    # Fetch UserProfilePicture object for the userData
    userProfilePicture = UserProfilePicture.objects.filter(user=userData).first()
    document = userDocument.objects.filter(user=userData)
    
    requestedUserType = usersDetail.objects.all()
    print('userProfilePicture : ', userProfilePicture)
    context = {
        'requestedUserType': requestedUserType,
        'document': document,
        'userData': userData,
        'documentImages' : documentImages,
        'allApprovedUsers': allApprovedUsers,
        'userProfilePicture': userProfilePicture,
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
    
    # restaurant = None
    # if request.user.is_authenticated and request.user.groups.filter(name='restaurant').exists():
    #     try:
    #         restaurant = addRestaurant.objects.get(user=request.user)
    #     except addRestaurant.DoesNotExist:
    #         pass    
    context = {
        
        'profile_image_url': profile_image_url,
        # 'restaurant': restaurant, 
    }
    return render(request, 'profiles/profile.html', context)


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
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email')
            if User.objects.filter(email=request.POST.get('email')).exists():
                sweetify.error(request, "Email already registered!")
                return redirect('editprofile')
            #saving the updated data
            user.save()
            
            # UPDATING userdetail MODEL
            user.usersdetail = user.usersdetail

            
            user.usersdetail.phone_number = request.POST.get('phone_number')
            if not re.match(r'^(98|97)\d{8}$', user.usersdetail.phone_number):
                    sweetify.error(request,"Invalid contact number")
                    return redirect('editprofile')
            user.usersdetail.address = request.POST.get('address')
            user.usersdetail.restaurant_name = request.POST.get('restaurant_name', '')
            
            #saving the updated data
            user.usersdetail.save()
            msg = "Profile Updated"
            sweetify.success(request, 'Profile Updated')           
            return redirect('editprofile')   
        #  for uploading new profile picture
        if "saveImage" in request.POST:
            if request.FILES:
                # Saving user New profile
                user_profile = UserProfilePicture.objects.get(user=user)
                user_profile.profileImage  = request.FILES['img']
                user_profile.save()
                sweetify.success(request, 'Profile Picture Updated')
                return redirect('editprofile')   
            else:
                sweetify.info(request, "Please select an image first")
        # for setting default profile
        if "deleteImage" in request.POST:
            user_profile = UserProfilePicture.objects.get(user=user)
            user_profile.delete()
            # Saving user default profile
            user_default_profile_picture, created = UserProfilePicture.objects.get_or_create(user=user)

            if not created:
                user_default_profile_picture.profileImage = defaultProfilePicture()
                user_default_profile_picture.save()
          
            sweetify.success(request, 'Profile Picture updated.')         
            return redirect('editprofile')   
    
    context = {
        
        'profile_image_url': profile_image_url, 
    }
    return render(request, 'profiles/editprofile.html', context)

# for change password
def changePassword(request):
    if request.method == 'POST':
        if "user" in request.POST:
                username = request.POST.get('user')
                user = User.objects.get(username=username)


        if "changePassword" in request.POST:
            current_password = request.POST.get('currentPassword')
            new_password = request.POST.get('newpassword1')
            confirm_new_password = request.POST.get('newpassword2')


            if not request.user.check_password(current_password):
                sweetify.error(request, 'Current password is incorrect.')


            else:
                # If password doesnt match display error messaage
                if new_password != confirm_new_password:
                    sweetify.error(request, 'New password and confirm password do not match.')


                else:
                    # Change the password
                    request.user.set_password(new_password)
                    request.user.save()
                    sweetify.success(request, 'Password Changed')
                    
                    # Updating the session to prevent logout
                    update_session_auth_hash(request, request.user)
    return render(request, 'profiles/changepassword.html')


def pendingRequests(request):
    
    requestedUsers = User.objects.filter(groups__isnull=True).exclude(is_superuser=True)
        
    context = {
        'requestedUsers': requestedUsers,
    } 
    
    return render(request, 'admin/pendingRequests.html', context)


def contact_us(request):
    if request.method == 'POST':
        sender_email = request.POST.get('email')
        message = request.POST.get('message')
        subject = f'{sender_email}: {request.POST.get("subject")}' 

        print("email", sender_email)
        print("subject", subject)
        print("mess", message)
        
        try:
            send_mail(
                subject,
                message,
                sender_email,  # Set sender's email 
                ['nepalicious.webapp@gmail.com'],  # Set recipient's email
                fail_silently=False,
                
            )
            sweetify.success(request, 'Email sent successfully!')
            return redirect('contact_us')
        except Exception as e:
            sweetify.error(request, 'Failed to send email.')
            return redirect('contact_us')    
    return render(request, 'contact/contactus.html')