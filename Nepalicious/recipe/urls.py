from django.urls import path, include
from . import views

urlpatterns = [
    path('recipe', views.recipe, name='recipe'),
    path('addRecipe', views.add_Recipe, name='addRecipe'),
    path('recipeDetail/<int:recipe_id>', views.recipeDetail, name='recipeDetail'),
    path('viewSavedRecipe', views.viewSavedRecipe, name='viewSavedRecipe'),
    path('savedRecipe/<int:recipe_id>', views.save_recipe, name='savedRecipe'),
    path('deleteSavedRecipe/<int:saved_recipe_id>', views.deleteSavedRecipe, name='deleteSavedRecipe'),
    path('submit_review_recipe/<int:recipe_id>/', views.submit_review_recipe, name='submit_review_recipe'),
    path('likeRecipe/<int:recipe_id>/like/', views.like_recipe, name='like_recipe'),
    path('dislikeRecipe/<int:recipe_id>/dislike/', views.dislike_recipe, name='dislike_recipe'),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),


]