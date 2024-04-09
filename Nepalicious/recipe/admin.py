from django.contrib import admin
from embed_video.admin import AdminVideoMixin
# Register your models here.
# Register your models here.
from recipe.models import *

# Register your models here.
class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass


admin.site.register(addRecipe),
admin.site.register(recipeImage),
admin.site.register(recipeFeedback)
admin.site.register(savedRecipe)
admin.site.register(LikeDislikeRecipe)