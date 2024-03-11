from django.urls import path, include
from . import views

urlpatterns = [
    path('recipe', views.recipe, name='recipe'),
    path('addRecipe', views.add_Recipe, name='addRecipe'),
    path('recipeDetail/<int:recipe_id>', views.recipeDetail, name='recipeDetail'),
]