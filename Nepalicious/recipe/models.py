from django.db import models
from django.db import models
from django.contrib.auth.models import User


 #Category choices
cuisine = (
    ('Thakali', 'Thakali'),
    ('Newari', 'Newari'),
    ('Sherpa', 'Sherpa'),
    ('Tamang', 'Tamang'),
    ('Nepali ', 'Nepali')
)


# Create your models here.
class addRecipe(models.Model):
    recipeName = models.CharField(max_length=100)
    recipeDescription = models.TextField()
    cuisineType = models.CharField(max_length=100, choices=cuisine)
    recipeIngredient = models.TextField(blank=True)
    recipeSteps = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipeProductTags = models.TextField(blank=False)

    
    
class recipeImage(models.Model):
    addRecipe = models.ForeignKey(addRecipe, related_name ='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/recipe/recipeImage/')
    
    def __str__(self):
        return f"{self.addRecipe.recipeName} - {self.pk}"
    
class recipeFeedback(models.Model):
    recipe = models.ForeignKey(addRecipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField(blank=True)
    
    
    def __str__(self):
        return f"{self.recipe.recipeName} - {self.user.username}"
    
class savedRecipe(models.Model):
    recipe = models.ForeignKey(addRecipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.recipe.recipeName} - {self.user.username}"
    
class LikeDislikeRecipe(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]

    recipe = models.ForeignKey(addRecipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.CharField(max_length=7, choices=CHOICES)

    def __str__(self):
        return f"{self.recipe.recipeName} - {self.choice} - {self.user.username}"