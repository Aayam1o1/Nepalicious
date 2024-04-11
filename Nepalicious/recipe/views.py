from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Count, Q
from market.models import *
import random
from django.db.models import Sum, F, Avg
import sweetify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404

def recipe(request):
    recipe_list = addRecipe.objects.filter(cuisineType='Newari').order_by('-id')[:4]
    top_four_recipe = addRecipe.objects.annotate(num_likes=Count('likedislikerecipe', filter=models.Q(likedislikerecipe__choice='like'))).order_by('-num_likes')[:4]
    latest_recipe = addRecipe.objects.all().order_by('-id')
    
    
    search = request.GET.get('search_for')
    cuisineType = request.GET.get('cuisineType')
    print("cuisineType", cuisineType)
    print("search", search)
    
    if search and cuisineType == "Cuisine Type":
        if search:
            latest_recipe = latest_recipe.filter(
                Q(recipeName__icontains=search) |
                Q(user__username__icontains=search)  # Filter by username
            ).distinct()
    elif cuisineType != "Cuisine Type" and search == "":
        latest_recipe = latest_recipe.filter(Q(cuisineType__icontains=cuisineType))
    elif (search != "" and search is not None) and (cuisineType != "Cuisine Type" or cuisineType is not None):
        latest_recipe = latest_recipe.filter(
                (Q(recipeName__icontains=search) |
                Q(user__username__icontains=search)) and Q(cuisineType__icontains=cuisineType)  # Filter by username
            ).distinct()
    else:
        latest_recipe = addRecipe.objects.all()
        print("No search query provided.")
    
    
    paginator = Paginator(latest_recipe, 10)  # 10 recipes per page
    page = request.GET.get('page')
    try:
        latest_recipe = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_recipe = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_recipe = paginator.page(paginator.num_pages)
    
    
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
           
            # STEP 3: Choose tags
            recipeProductTags = []
            # Check if each checkbox is checked and add its value to the tag list
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

            sweetify.success(request, "Sucessfully added recipe")
            return redirect('recipe')
        
        else:
            errors = form.errors.as_data()
            for field, error_list in errors.items():
                for error in error_list:
                    sweetify.error(request, f"{field}: {error}")
            
    else:
        form = addRecipeForm()
        
    context = {
        'form': form,
        
    }
        
    return render(request, 'recipe/addRecipe.html', context)


# for recipe descriptiion.
def recipeDetail(request, recipe_id):
    
    recipetList = addRecipe.objects.all()
    if not recipetList:

        if not (request.user.is_superuser or request.user == recipetList.user):
            raise Http404("Room not found")

        recipetList = get_object_or_404(addRecipe, pk=recipe_id)
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
    
    
    recipeIngredientString = recipeDetail.recipeIngredient
            
    # Split the rules string into individual rules and append them to the list
    recipeIngredient = recipeIngredientString.split(", ")
    
    
    #to get the image of the recipe
    recipedetailForImage = get_object_or_404(addRecipe, id=recipe_id)

    recipe_image = recipeImage.objects.filter(addRecipe = recipedetailForImage)
    
    
    if request.user.is_authenticated:
        saved_recipe = savedRecipe.objects.filter(user=request.user, recipe=recipeDetail).first()
        # Check if the recipe has been liked by the current user
        liked_recipe = LikeDislikeRecipe.objects.filter(user=request.user, recipe=recipeDetail, choice='like').exists()
        
        disliked_recipe = LikeDislikeRecipe.objects.filter(user=request.user, recipe=recipeDetail, choice='dislike').exists()
    else:
        saved_recipe = False
        disliked_recipe = False
        liked_recipe = False
    print("saved recipe id: ", saved_recipe)
    # Retrieve comments related to the specific recipe
    feedback_comments = recipeFeedback.objects.filter(recipe=recipeDetail)
    
    

    total_likes = LikeDislikeRecipe.objects.filter(recipe=recipeDetail, choice='like').count()
    
    
    # for similar recipe
    cuisine_type = recipeDetail.cuisineType
    similar_recipes = addRecipe.objects.filter(cuisineType=cuisine_type).exclude(id=recipe_id)    
    
    similar_recipes = similar_recipes.order_by('-id')[:4]
    
    
    # for tags
    recipe_tags = recipeDetail.recipeProductTags.strip("[]").replace("'", "").replace(", ", " ")
    # Get all products
    all_products = addProducts.objects.filter(isdeleted = False, productStock__gt = 0)
    
    filtered_products = [product for product in all_products if product.productCategory in recipe_tags]
    
    # Shuffle the filtered products and select the first two
    random.shuffle(filtered_products)
    selected_products = filtered_products[:2]    
    
    avg_rating = 0
    for product in selected_products:
        # Calculate average rating for each product
        avg_rating = product.productfeedback_set.aggregate(Avg('rating'))['rating__avg']
        product.avg_rating = avg_rating  # Add avg_rating attribute to product instance
    
    videos = [recipeDetail.video] if recipeDetail.video else []
    
    context = {
        'recipetList': recipetList,
        'recipedetailForImage' : recipedetailForImage,
        'recipe_image' : recipe_image,
        'recipeDetail': recipeDetail,
        'recipeSteps': recipeSteps,
        'recipeIngredient': recipeIngredient,
        'feedback_comments': feedback_comments,
        'saved_recipe': saved_recipe,
        'liked_recipe': liked_recipe,
        'disliked_recipe': disliked_recipe,
        'total_likes': total_likes,
        'selected_products': selected_products,
        'similar_recipes': similar_recipes,
        'avg_rating': avg_rating,
        'videos': videos
    }
    
    return render(request, 'recipe/recipeDetail.html', context)


def your_recipe(request):
    if request.method == 'POST':
        if "edit" in request.POST:
            recipe_id = request.POST.get("recipe_id")
            return redirect("edit_recipe", recipe_id)
        
    user = request.user
    latest_recipe = addRecipe.objects.filter(user=user)
    
    items_per_page = 4
    
    page = request.GET.get('page', 1)
    
    # Create a Paginator object
    paginator = Paginator(latest_recipe, items_per_page)

    try:
        # Get the current page
        latest_recipe = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        latest_recipe = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page of results
        latest_recipe = paginator.page(paginator.num_pages)
    
    context = {
        'latest_recipe': latest_recipe,
    }
    
    return render(request, 'recipe/yourRecipe.html', context)

def delete_recipe(request, recipe_id):
    url  = request.META.get('HTTP_REFERER')
    recipe = addRecipe.objects.get(id=recipe_id)
    if request.method == 'POST':
        try:
            recipe.delete()
            sweetify.success(request, "Recipe has been deleted successfully", timer=3000)
            return redirect(url)
        except Exception as e:
            messages.error(request, f"Error deleting Recipe: {str(e)}")
            return redirect(url)
    return redirect(url)

    
def edit_recipe(request, recipe_id):
    recipe_instance = get_object_or_404(addRecipe, pk=recipe_id)
    if not recipe_instance:

        if not (request.user.is_superuser or request.user == recipe_instance.user):
            raise Http404("Room not found")

        recipe_instance = get_object_or_404(addRecipe, pk=recipe_id)
    else:
        pass
    recipeStepsString = recipe_instance.recipeSteps
    recipeSteps = []
    current_step = ""
    for step in recipeStepsString.split(','):
        current_step += step.strip()
        if current_step.endswith('.'):
            recipeSteps.append(current_step)
            current_step = ""
        else:
            current_step += ', '    
            
    recipeIngredientString = recipe_instance.recipeIngredient     
    # Split the rules string into individual rules and append them to the list
    recipeIngredient = recipeIngredientString.split(", ")   
                 
    if request.method == 'POST':
        # If it's a POST request, process the form data
        form = editRecipeForm(request.POST, instance=recipe_instance)
  
        
        if form.is_valid():
            form.save()
            steps_string = request.POST.get('steps', '')
            ingredients_string = request.POST.get('ingredients', '')
            
            print('steps:::', steps_string)
            print('ingree', ingredients_string)
            
            if steps_string:
                print('steps', steps_string)
                
                steps = steps_string.split(", ")
                recipe_instance.recipeSteps = ", ".join(steps)            
        
                # Save the instance again to update the fields
                recipe_instance.save()
            else:
                sweetify.error(request, 'There was an error adding the recipe steps')
                
            
            if ingredients_string:
                #step4: Add ingredients for the recipe
                ingredients = ingredients_string.split(", ")
                recipe_instance.recipeIngredient = ", ".join(ingredients)
                recipe_instance.save()

                
            else:
                sweetify.error(request, 'There was an error adding the recipe ingredients')
                
            #for image
            new_images = request.FILES.getlist('recipeImage')

            # Get the list of existing images
            old_images = recipe_instance.images.all()
                        
            if new_images:
                for old_image in old_images:
                    if old_image.image not in new_images:
                        old_image.delete()

                for uploaded_file in new_images:
                    recipeImage.objects.create(addRecipe=recipe_instance, image=uploaded_file)
            else:
                sweetify.error(request, 'There was an error uplodaing image.')
            sweetify.success(request, "Successfully edited Recipe")
            return redirect('recipeDetail', recipe_id=recipe_instance.id)
        else:
            sweetify.error(request, 'Form is not valid')
            
    else:
        # If it's not a POST request, populate the form with instance data
        form = editRecipeForm(instance=recipe_instance)
        
    
    context = {
        'form': form,
        'recipe_instance': recipe_instance,
        'recipeSteps': recipeSteps,  
        'recipeIngredient': recipeIngredient
    }    
    
    return render(request, 'recipe/editRecipe.html', context)
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
            sweetify.success(request, 'Thank you, Your review has been updated')
            return redirect(url)
        except:
            form = FeedbackForm(request.POST)
            if form.is_valid():
                data = recipeFeedback()
                data.feedback = form.cleaned_data['feedback']
                data.recipe_id = recipe_id
                data.user_id = request.user.id
                data.save()
                sweetify.success(request, 'Thank you, Your review has been submitted')
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
                sweetify.success(request, 'Successfully Liked')
                
            elif existing_like.choice == 'dislike':
                    # If the recipe is not disliked, create and save the LikeDislikeRecipe object with choice='dislike'
                    existing_like.choice = 'like'
                    existing_like.save()
                    sweetify.success(request, 'Recipe Dislike changed to Like successfully')
            
            elif existing_like.choice == 'like':
                existing_like.delete()
                sweetify.success(request, 'Recipe like removed')

            else:
                if existing_like.choice != 'dislike':
                    existing_like.choice = 'like'
                    existing_like.save()
                    sweetify.success(request, 'Recipe Like changed successfully')
                
                
            
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
                    sweetify.success(request, 'Recipe Like changed to Dislike successfully')
                    
                elif existing_like.choice == 'dislike':
                    # If the recipe is not disliked, create and save the LikeDislikeRecipe object with choice='dislike'
                    
                    existing_like.delete()
                    sweetify.success(request, 'Recipe Dislike removed successfully.')    


            else:
                #If the recipe is not disliked, create and save the LikeDislikeRecipe object with choice='dislike'
                LikeDislikeRecipe.objects.create(user=user, recipe=recipe, choice='dislike')
                sweetify.success(request, 'Recipe Disliked')
                
                
            return redirect(url)
        
        except addRecipe.DoesNotExist:
            # Handle the case where the recipe with the given ID does not exist
            sweetify.error(request, 'Recipe does not exist')
        
    return redirect(url)


def delete_comment(request, comment_id):
    url  = request.META.get('HTTP_REFERER')

    # Fetch the comment object to be deleted
    comment = get_object_or_404(recipeFeedback, id=comment_id)

    # Check if the logged-in user is the owner of the comment
    if comment.user == request.user:
        # Delete the comment
        comment.delete()
        sweetify.success(request, 'Comment deleted')
    else:
        sweetify.failure(request, 'There was an error deleting the comment')
        
        pass

    # Redirect back to the page where the comment was deleted from
    return redirect(url)
