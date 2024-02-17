from django.shortcuts import render

# Create your views here.
# render header
def recipe(request):
    return render(request, 'recipe/recipe.html')

def addRecipe(request):
    return render(request, 'recipe/addRecipe.html')