from django.contrib import admin

# Register your models here.
from market.models import *

# Register your models here.
admin.site.register(addProducts),
admin.site.register(productImage),
admin.site.register(Cart),
admin.site.register(CartItem)
admin.site.register(productFeedback)