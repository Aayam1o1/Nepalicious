from django.db import models
from django.contrib.auth.models import User
# Create your models here
class Search(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurantaddress = models.CharField(max_length=200, null = True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    date =  models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.restaurantaddress
    