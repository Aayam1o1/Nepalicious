from django.urls import path, include
from . import views

urlpatterns = [
    path('recipe', views.recipe, name='recipe'),
    path('addRecipe', views.add_Recipe, name='addRecipe'),
    path('recipeDetail/<int:recipe_id>', views.recipeDetail, name='recipeDetail'),
    path('viewSavedRecipe', views.viewSavedRecipe, name='viewSavedRecipe'),
    path('savedRecipe/<int:recipe_id>', views.save_recipe, name='savedRecipe'),
    path('deleteSavedRecipe/<int:saved_recipe_id>', views.deleteSavedRecipe, name='deleteSavedRecipe'),

]