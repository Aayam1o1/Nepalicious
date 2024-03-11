from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages


# Crpath('removeRecipe', views.remove_Recipe, name='removeRecipe'),h('removeRecipe', views.remove_Recipe, name='removeRecipe'),e your views here.

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


# for recipe descriptiion.
def recipeDetail(request, recipe_id):
    
    recipetList = addRecipe.objects.all()
    
    # to get the details of the product
    recipeDetail = get_object_or_404(addRecipe, id=recipe_id)
    
    
    # for steps
    recipeStepsString = recipeDetail.recipeSteps
    
   # Split by commas and then combine steps that were split incorrectly
    recipeSteps = []
    current_step = ""
    for step in recipeStepsString.split(','):
        current_step += step.strip()
        if current_step.endswith('.'):
            recipeSteps.append(current_step)
            current_step = ""
        else:
            current_step += ', '

    # Remove empty strings
    recipeSteps = [step for step in recipeSteps if step]
     
    # for ingredients
    
    # STEP 4: Add Rules for your room
    recipeIngredientString = recipeDetail.recipeIngredient
            
    # Split the rules string into individual rules and append them to the list
    recipeIngredient = recipeIngredientString.split(", ")
    
    
    #to get the image of the recipe
    recipedetailForImage = get_object_or_404(addRecipe, id=recipe_id)

    recipe_image = recipeImage.objects.filter(addRecipe = recipedetailForImage)
    
    # for feedback
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)

        if feedback_form.is_valid():
            # Create a new feedback object and associate it with the current recipe and user
            new_feedback = feedback_form.save(commit=False)
            new_feedback.recipe = recipeDetail
            new_feedback.user = request.user
            new_feedback.save()

            # Redirect to the same recipe detail page after submitting feedback
            return redirect('recipeDetail', recipe_id=recipe_id)
    else:
        feedback_form = FeedbackForm()
    
    # Retrieve comments related to the specific recipe
    feedback_comments = recipeFeedback.objects.filter(recipe=recipeDetail)
    
    context = {
        'recipetList': recipetList,
        'recipedetailForImage' : recipedetailForImage,
        'recipe_image' : recipe_image,
        'recipeDetail': recipeDetail,
        'recipeSteps': recipeSteps,
        'recipeIngredient': recipeIngredient,
        'feedback_form': feedback_form,
        'feedback_comments': feedback_comments,

    }
    
    return render(request, 'recipe/recipeDetail.html', context)