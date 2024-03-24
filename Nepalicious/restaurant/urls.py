from django.urls import path
from . import views
#  For PASSWORD RESET
from django.contrib.auth import views as auth_views

urlpatterns = [
    # For restaurant
    path('restaurant', views.restaurant, name='restaurant'),
    path('addRestaurant', views.addRestaurant, name='addRestaurant'),

]