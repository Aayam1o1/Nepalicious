from django.urls import path
from . import views
#  For PASSWORD RESET
from django.contrib.auth import views as auth_views

urlpatterns = [
    # For Login and Register
    path('register', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('index', views.index, name='index'),
    path('adminHome', views.adminDashboard, name='adminHome'),
    path('userRequests/<int:userID>/', views.userRequests, name='userRequests'),
    
    
    
]

