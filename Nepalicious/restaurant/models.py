from django.db import models
from django.contrib.auth.models import User
from users.models import *
# Create your models here

 #Category choices
types = (
    ('Thakali', 'Thakali'),
    ('Newari', 'Newari'),
    ('Sherpa', 'Sherpa'),
    ('Tamang', 'Tamang'),
    ('Nepali ', 'Nepali')
)

class addRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurantDescription = models.TextField()
    restaurantType = models.CharField(max_length=100, choices=types)
    
    def __str__(self):
        users_detail = self.user.usersdetail
        return users_detail.restaurant_name if users_detail else 'No restaurant name'
    
class restaurantImage(models.Model):
    addRecipe = models.ForeignKey(addRestaurant, related_name ='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurantImage/')
    
class Location(models.Model):
    restaurant = models.ForeignKey(addRestaurant, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"Latitude: {self.latitude}, Longitude: {self.longitude}"

class Search(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurantaddress = models.CharField(max_length=200, null = True)
    latitudesearch = models.FloatField(null=True, blank=True)
    longitudesearh = models.FloatField(null=True, blank=True)
    date =  models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.restaurantaddress
    
    