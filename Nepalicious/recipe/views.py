from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Count
from market.models import *
import random
from django.db.models import Sum, F, Avg
import sweetify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def recipe(request):
    recipe_list = addRecipe.objects.filter(cuisineType='Newari').order_by('-id')[:4]
    top_four_recipe = addRecipe.objects.annotate(num_likes=Count('likedislikerecipe', filter=models.Q(likedislikerecipe__choice='like'))).order_by('-num_likes')[:4]
    latest_recipe = addRecipe.objects.all().order_by('-id')
    
    items_per_page = 11
    
    page = request.GET.get('page', 1)
    
    
     # Create a Paginator object
    paginator = Paginator(latest_recipe, items_per_page)

    try:
        # Get the current page
        latest_recipe = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, delivering the first page
        latest_recipe = paginator.page(1)
    except EmptyPage:
        # If page is out of range, delivering the last page of results
        latest_recipe = paginator.page(paginator.num_pages)
    # Get the current page number from the request's GET parameters
    page = request.GET.get('page', 1)
    
    filtered_recipe = list(addRecipe.objects.all())
    random.shuffle(filtered_recipe)

    random_recipe = filtered_recipe[0] if filtered_recipe else None
    print(random_recipe)
    context = {
        'recipeList': recipe_list,
        'top_four_recipe': top_four_recipe,
        'latest_recipe': latest_recipe,
        'random_recipe': random_recipe
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
           
            # STEP 3: Choose Amenities
            recipeProductTags = []
            # Check if each checkbox is checked and add its value to the amenities list
            if "reicpeTag1" in request.POST:
                recipeProductTags.append(request.POST["reicpeTag1"])
            if "reicpeTag2" in request.POST:
                recipeProductTags.append(request.POST["reicpeTag2"])
            if "reicpeTag3" in request.POST:
                recipeProductTags.append(request.POST["reicpeTag3"])
            if "reicpeTag4" in request.POST:
                recipeProductTags.append(request.POST["reicpeTag4"])
            if "reicpeTag5" in request.POST:
                recipeProductTags.append(request.POST["reicpeTag5"])
            
            instance.recipeProductTags = recipeProductTags
                
            #saviing the tags
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
    saved_recipe = False 
    
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
    
    if request.user.is_authenticated:
        saved_recipe = savedRecipe.objects.filter(user=request.user, recipe=recipeDetail).first()
    else:
        saved_recipe = False
        
    print("saved recipe id: ", saved_recipe)
    # Retrieve comments related to the specific recipe
    feedback_comments = recipeFeedback.objects.filter(recipe=recipeDetail)
    
    
    # Check if the recipe has been liked by the current user
    liked_recipe = LikeDislikeRecipe.objects.filter(user=request.user, recipe=recipeDetail, choice='like').exists()
    
    disliked_recipe = LikeDislikeRecipe.objects.filter(user=request.user, recipe=recipeDetail, choice='dislike').exists()

    total_likes = LikeDislikeRecipe.objects.filter(recipe=recipeDetail, choice='like').count()
    
    
    # for similar recipe
    cuisine_type = recipeDetail.cuisineType
    similar_recipes = addRecipe.objects.filter(cuisineType=cuisine_type).exclude(id=recipe_id)    
    
    similar_recipes = similar_recipes.order_by('-id')[:4]
    
    
    # for tags
    recipe_tags = recipeDetail.recipeProductTags.strip("[]").replace("'", "").replace(", ", " ")
    # Get all products
    all_products = addProducts.objects.filter(isdeleted = False)
    
    filtered_products = [product for product in all_products if product.productCategory in recipe_tags]
    
    # Shuffle the filtered products and select the first two
    random.shuffle(filtered_products)
    selected_products = filtered_products[:2]    
    
    avg_rating = 0
    for product in selected_products:
        # Calculate average rating for each product
        avg_rating = product.productfeedback_set.aggregate(Avg('rating'))['rating__avg']
        product.avg_rating = avg_rating  # Add avg_rating attribute to product instance
    
    
    context = {
        'recipetList': recipetList,
        'recipedetailForImage' : recipedetailForImage,
        'recipe_image' : recipe_image,
        'recipeDetail': recipeDetail,
        'recipeSteps': recipeSteps,
        'recipeIngredient': recipeIngredient,
        'feedback_form': feedback_form,
        'feedback_comments': feedback_comments,
        'saved_recipe': saved_recipe,
        'liked_recipe': liked_recipe,
        'disliked_recipe': disliked_recipe,
        'total_likes': total_likes,
        'selected_products': selected_products,
        'similar_recipes': similar_recipes,
        'avg_rating': avg_rating
    }
    
    return render(request, 'recipe/recipeDetail.html', context)

#submt review
def submit_review_recipe(request, recipe_id):
    # getting the url fort the same webpage
    url  = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            # to check if review is already submitted
            reviews = recipeFeedback.objects.get(user__id=request.user.id, recipe__id = recipe_id)
            form = FeedbackForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you, Your review has been updated')
            return redirect(url)
        except:
            form = FeedbackForm(request.POST)
            if form.is_valid():
                data = recipeFeedback()
                data.feedback = form.cleaned_data['feedback']
                data.recipe_id = recipe_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you, Your review has been submitted')
                return redirect(url)
            

def save_recipe(request, recipe_id):
    url  = request.META.get('HTTP_REFERER')
    if request.method == 'POST':

        recipe = addRecipe.objects.get(pk=recipe_id)
        print('Recipe: ', recipe)
        
        
        # Check if the recipe is not already saved for the current user
        if not savedRecipe.objects.filter(user=request.user, recipe=recipe).exists():
            # If the recipe is not saved, create and save the savedRecipe object
            saved_recipe = savedRecipe.objects.create(user=request.user, recipe=recipe)
            print('Saved Recipe: ', saved_recipe)
            print('Recipe saved successfully')
            
            # Add a success message
            sweetify.success(request, 'Successfully saved')
            return redirect(url)
        else:
            print('Recipe already saved')
            # Add a warning message
            sweetify.warning(request, 'Recipe already saved')
        
        # Redirect to the same page
        return redirect('recipeDetail', recipe_id=recipe_id)

    
    return render(request, 'profiles/savedRecipe.html')


def viewSavedRecipe(request):
    saved_recipes = savedRecipe.objects.filter(user=request.user)
    
    context = {
        'saved_recipes': saved_recipes,
    }
    return render(request, 'profiles/savedRecipe.html', context)

def deleteSavedRecipe(request, saved_recipe_id):
    url  = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        saved_recipe = savedRecipe.objects.get(pk=saved_recipe_id)
        print('saved recipe: ', saved_recipe)
        
        if saved_recipe.user == request.user:
            saved_recipe.delete()
            sweetify.success(request, 'The recipe was removed from bookmark')
            return redirect(url)
    return render(request, 'profiles/savedRecipe.html')


# for like recipe
def like_recipe(request, recipe_id):
    url  = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            recipe = addRecipe.objects.get(pk=recipe_id)
            user = request.user
            
            # Check if the recipe is not already Liked for the current user
            existing_like = LikeDislikeRecipe.objects.filter(user=user, recipe=recipe).first()
            if not existing_like:
                # If the user already liked or disliked the recipe, update the choice to 'like'
                LikeDislikeRecipe.objects.create(user=user, recipe=recipe, choice='like')
                messages.success(request, 'Successfully Liked')
                
            elif existing_like.choice == 'dislike':
                    # If the recipe is not disliked, create and save the LikeDislikeRecipe object with choice='dislike'
                    existing_like.choice = 'like'
                    existing_like.save()
                    messages.success(request, 'Recipe Dislike changed to Like successfully')
            
            elif existing_like.choice == 'like':
                existing_like.delete()
                messages.success(request, 'Recipe like removed')

            else:
                if existing_like.choice != 'dislike':
                    existing_like.choice = 'like'
                    existing_like.save()
                    messages.success(request, 'Recipe Like changed successfully')
                
                
            
            return redirect(url)
        
        except addRecipe.DoesNotExist:
             # Handle the case where the recipe with the given ID does not exist
            # Add an appropriate error message
            messages.add_message(request, messages.ERROR, 'Recipe does not exist')
         
    return redirect(url)

def dislike_recipe(request, recipe_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            recipe = addRecipe.objects.get(pk=recipe_id)
            user = request.user
            
            existing_like = LikeDislikeRecipe.objects.filter(user=user, recipe=recipe).first()

            if existing_like:
                if existing_like.choice == 'like':

                    # If the recipe is liked, update the existing like to dislike
                    existing_like.choice = 'dislike'
                    existing_like.save()
                    messages.success(request, 'Recipe Like changed to Dislike successfully')
                    
                elif existing_like.choice == 'dislike':
                    # If the recipe is not disliked, create and save the LikeDislikeRecipe object with choice='dislike'
                    
                    existing_like.delete()
                    messages.success(request, 'Recipe Dislike changed to Like successfully')    


            else:
                #If the recipe is not disliked, create and save the LikeDislikeRecipe object with choice='dislike'
                LikeDislikeRecipe.objects.create(user=user, recipe=recipe, choice='dislike')
                messages.success(request, 'Successfully Disliked')
                
            
            
            
            # # Delete any existing saved entry for the recipe by the current user
            # saved_recipe = savedRecipe.objects.filter(user=user, recipe=recipe).first()
            # if saved_recipe:
            #     saved_recipe.delete()
            #     messages.success(request, 'Recipe unsaved due to Dislike')
                
            return redirect(url)
        
        except addRecipe.DoesNotExist:
            # Handle the case where the recipe with the given ID does not exist
            messages.error(request, 'Recipe does not exist')
        
    return redirect(url)


def delete_comment(request, comment_id):
    url  = request.META.get('HTTP_REFERER')

    # Fetch the comment object to be deleted
    comment = get_object_or_404(recipeFeedback, id=comment_id)

    # Check if the logged-in user is the owner of the comment
    if comment.user == request.user:
        # Delete the comment
        comment.delete()
        messages.success(request, 'Comment deleted')
    else:
        messages.MessageFailure(request, 'There was an error deleting the comment')
        print(messages)
        pass

    # Redirect back to the page where the comment was deleted from
    return redirect(url)
