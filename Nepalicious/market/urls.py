from django.urls import path
from . import views
#  For PASSWORD RESET
from django.contrib.auth import views as auth_views


urlpatterns = [
    # For marketplace
    path('marketplace', views.marketplace, name='marketplace'),
    path('addProduct', views.addProduct, name='addProduct'),
    path('productDetail/<int:product_id>', views.productDetail, name='productDetail'),
    path('cart', views.cart_view, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

]
