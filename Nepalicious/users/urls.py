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
    path('editprofile', views.editprofile, name='editprofile'),
    path('profile', views.profile, name='profile'),
    path('changePassword', views.changePassword, name='changePassword'),
    path('pendingRequests', views.pendingRequests, name='pendingRequests'),
    path('contact_us', views.contact_us, name='contact_us'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    
    path('reset_password', auth_views.PasswordResetView.as_view(
    template_name="login-Register/sentResetPassword.html"), 
    name="reset_password"),   
    
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(
    template_name="login-Register/resetPasswordSent.html"), 
    name="password_reset_done"), 
      
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    template_name="login-Register/resetPasswordConfirm.html"), 
    name="password_reset_confirm"), 
      
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(
    template_name="login-Register/resetPasswordComplete.html"),  
    name="password_reset_complete"),  
]

