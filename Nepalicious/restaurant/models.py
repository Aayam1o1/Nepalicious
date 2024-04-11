from django.db import models
from django.contrib.auth.models import User
from users.models import *
# Create your models here

 #Category choices
types = (
    ('Thakali', 'Thakali'),
    ('Newari', 'Newari'),
    ('Newari', 'Sherpa'),
    ('Tamang', 'Tamang'),
    ('Nepali ', 'Nepali')
)

class addRestaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurantDescription = models.TextField()
    restaurantType = models.CharField(max_length=100, choices=types)
    
    def __str__(self):
        users_detail = self.user.usersdetail
        return users_detail.restaurant_name if users_detail else 'No restaurant name'
    
class restaurantImage(models.Model):
    addRestaurant = models.ForeignKey(addRestaurant, related_name ='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurantImage/')
    
    def __str__(self):
        return f"{self.addRestaurant.user.usersdetail.restaurant_name} - {self.pk}"
    
class Location(models.Model):
    restaurant = models.ForeignKey(addRestaurant, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    map_addres = models.TextField(blank=True)
    def __str__(self):
        return f"{self.restaurant.user.usersdetail.restaurant_name} - Latitude: {self.latitude}, Longitude: {self.longitude}"
    
    
class restaurantFeedback(models.Model):
    restaurant = models.ForeignKey(addRestaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField(blank=True)
    rating = models.FloatField()

    def __str__(self):
        return f"{self.restaurant.user.usersdetail.restaurant_name} - {self.user.username}"
