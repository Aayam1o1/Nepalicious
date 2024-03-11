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
    
    def __str__(self):
        return self.recipeName
    
    
class recipeImage(models.Model):
    addRecipe = models.ForeignKey(addRecipe, related_name ='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/recipe/recipeImage/')
    
    
class recipeFeedback(models.Model):
    recipe = models.ForeignKey(addRecipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField(blank=True)
    