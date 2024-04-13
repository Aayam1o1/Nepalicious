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
    path('update_cart/', views.update_cart, name='update_cart'),
    path('submit_review_product/<int:product_id>/', views.submit_review_product, name='submit_review_product'),
    path('delete_comment_product/<int:comment_id>', views.delete_comment_product, name='delete_comment_product'),
    path('order_history', views.order_history, name='order_history'),
    path('pending_orders', views.pending_orders, name='pending_orders'),
    path('vendor_order', views.vendor_order, name='vendor_order'),
    path('your_product', views.your_product, name='your_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    
    # FOR PAYMENT
    path('initiate', views.initkhalti, name='initiate'),
    path('cash_on_delivery', views.cash_on_delivery, name='cash_on_delivery'),

    path('paymentSucessful', views.verifyKhalti, name='paymentSucessful'),
    path('error', views.error, name='error'),

    #for checkout update address and number
    path('checkout', views.checkout, name='checkout')
]
