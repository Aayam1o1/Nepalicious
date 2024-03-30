from django.urls import path
from . import views
#  For PASSWORD RESET
from django.contrib.auth import views as auth_views

urlpatterns = [
    # For restaurant
    path('restaurant', views.restaurant, name='restaurant'),
    path('addRestaurant', views.addRestaurantdetail, name='addRestaurant'),
    path('view_details/<int:restaurant_id>', views.view_details, name='view_details'),
    path('restaurant_detail/<int:restaurant_id>', views.restaurant_detail, name='restaurant_detail'),
    path('submit_review_restaurant/<int:restaurant_id>/', views.submit_review_restaurant, name='submit_review_restaurant'),
    path('delete_comment_restaurant/<int:comment_id>', views.delete_comment_restaurant, name='delete_comment_restaurant'),
]
