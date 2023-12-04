from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('test', views.test, name='test'),
]