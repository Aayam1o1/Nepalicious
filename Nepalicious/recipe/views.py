from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages


# Create your views here.

def recipe(request):
    recipe_list = addRecipe.objects.all()
    
    context = {
        'recipeList': recipe_list
    }
    return render(request, 'recipe/recipe.html', context)


def add_Recipe(request):
    if request.method == 'POST':
        form = addRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            
            # Sterp 1 Handle cusine type
            selected_cuisine_type = form.cleaned_data['cuisineType']
            
            instance.cuisineType = selected_cuisine_type
            instance.save()
            
            #step2: image handle for the recipe
            recipe_image = request.FILES.getlist('recipeImage')
            for image in recipe_image:
                recipeImage.objects.create(addRecipe=instance, image=image)
            
            # STEP 3: Add steps for your recipe
            steps_string = request.POST.get('steps')
            
            # Split the rules string into individual rules and append them to the list
            steps = steps_string.split(", ")
            instance.recipeSteps = ", ".join(steps)            
            
            #step4: Add ingredients for the recipe
            ingredients_string = request.POST.get('ingredients')
            ingredients = ingredients_string.split(", ")
            instance.recipeIngredient = ", ".join(ingredients)

            # Save the instance again to update the fields
            instance.save()

            messages.success(request, "Sucessfully added recipe")
            return redirect('recipe')
        
        else:
            print(form.errors)
            
    else:
        form = addRecipeForm()
        
    context = {
        'form': form,
        
    }
        
    return render(request, 'recipe/addRecipe.html', context)