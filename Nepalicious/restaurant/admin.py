from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(addRestaurant),
admin.site.register(Location),
admin.site.register(restaurantImage)
admin.site.register(restaurantFeedback)