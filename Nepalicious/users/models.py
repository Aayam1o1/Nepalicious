from django.db import models
from django.contrib.auth.models import User


class usersDetail(models.Model):
   """
   In Django, when you define a ForeignKey or OneToOneField in a model, the related 
   objects are accessible using a lowercased version of the target model's name. 
   This is part of Django's default naming conventions.
   """
   
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   address = models.CharField(max_length=50,blank=False)
   phone_number = models.CharField(null=True, blank=False, max_length=10)
   requestedGroup = models.CharField(max_length=50,blank=False, default ='user')
   
   def __str__(self):
        return f"{self.user.username}'s Details"
     
# to save default picture
def defaultProfilePicture():
    return '../static/images/defaultUserProfilePictures/defaultProfile.jpg'
 
 #for uplaoded user profile picture
class UserProfilePicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profileImage = models.ImageField(default=defaultProfilePicture, blank=True, upload_to='userProfilePictures')

    def __str__(self):
        return f'{self.user.username} Profile Picture'
   
   
class userDocument(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    documentImage = models.ImageField(null=False, blank=False, upload_to='documents')
    
    def __str__(self):
        return f'{self.user.username} documents'
    