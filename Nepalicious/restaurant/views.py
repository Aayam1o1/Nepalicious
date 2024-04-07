from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import *
import folium
import geocoder
from django.db.models import Sum, F, Avg
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def restaurant(request):
    restaurant_list = addRestaurant.objects.all()
    items_per_page = 4
    
    page = request.GET.get('page', 1)
    
    
     # Create a Paginator object
    paginator = Paginator(restaurant_list, items_per_page)

    try:
        # Get the current page
        restaurant_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, delivering the first page
        restaurant_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range, delivering the last page of results
        restaurant_list = paginator.page(paginator.num_pages)
    # Get the current page number from the request's GET parameters
    page = request.GET.get('page', 1)
    
    
    for restaurant in restaurant_list:
        # Calculate average rating for each product
        avg_rating = restaurant.restaurantfeedback_set.aggregate(Avg('rating'))['rating__avg']
        restaurant.avg_rating = avg_rating  # Add avg_rating attribute to product instance
       
        
    context = {
        'restaurantList': restaurant_list
    }
    
    return render(request, 'restaurant/restaurant.html', context)

def addRestaurantdetail(request):
    if request.method == 'POST':
        form = addRestaurantForm(request.POST, request.FILES)
        if form.is_valid():
             # Save latitude and longitude
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            print('lat:', latitude)
            print('long:', longitude)
            
            instance = form.save(commit=False)
            instance.user = request.user
            print('user', instance.user)
            
            # for saving restaurant type
            selected_restaurant_type = form.cleaned_data['restaurantType']
            instance.restaurantType = selected_restaurant_type
            
            print('selected restarunt type:: ', selected_restaurant_type)
            instance.save()

            # for images
            restaurant_image = request.FILES.getlist('restaurantImage')
            for image in restaurant_image:
                restaurantImage.objects.create(addRestaurant=instance, image=image)
                
            print('selected restarunt image: ', restaurant_image)
    
            instance.save()
            
            
            
            location = Location.objects.create(restaurant=instance, latitude=latitude, longitude=longitude)
            print(location)
            

            messages.success(request, "Sucessfully added Restaurant!!")   
            return redirect('restaurant') 
        else:
            print(form.errors)
            
    else:
        form = addRestaurantForm()
    
    
    context = {
        'form': form,
    }    
    return render(request, 'restaurant/addRestaurant.html', context)


def view_details(request, restaurant_id):
    restaurant = get_object_or_404(addRestaurant, pk=restaurant_id)
    print('sure')
    
    return redirect('restaurant_detail', restaurant_id=restaurant_id)
    
def restaurant_detail(request, restaurant_id):
    
    # Retrieve the restaurant object
    restaurant = addRestaurant.objects.get(pk=restaurant_id)
    # Access the related images
    restaurant_images = restaurant.images.all()
    
    #getting location for map    
    restaurant_location = Location.objects.filter(restaurant=restaurant).first()
    
    feedback_comments = restaurantFeedback.objects.filter(restaurant=restaurant) 
     # Calculate average rating
    avg_rating = restaurantFeedback.objects.filter(restaurant=restaurant).aggregate(Avg('rating'))['rating__avg']
    
    # Count the number of reviews
    num_reviews = feedback_comments.count()
    
    if restaurant_location:
        # Create a map centered at the restaurant's location
        maps = folium.Map(location=[restaurant_location.latitude, restaurant_location.longitude], zoom_start=12)
        
         # Add a marker for the restaurant's location
        marker_popup = f"<div style='width: 90px;'>{restaurant.user.usersdetail.restaurant_name}<br>{restaurant.user.usersdetail.address}</div>"
        folium.Marker([restaurant_location.latitude, restaurant_location.longitude], 
                  tooltip='Click for details', 
                  popup=marker_popup, max_width=400).add_to(maps)
        
        # Get the HTML representation of the map
        maps = maps._repr_html_()
        
        coordinates = {
        'latitude': restaurant_location.latitude,
        'longitude': restaurant_location.longitude
    }
    else:
        # If no location is available, provide a default map centered at a specific location
        maps = folium.Map(location=[27.7172, 85.3240], zoom_start=14)._repr_html_()
        
    
    filtered_restaurant = list(addRestaurant.objects.filter(restaurantType=restaurant.restaurantType).exclude(id=restaurant_id))
    random.shuffle(filtered_restaurant) 
    
    category_restaurants = filtered_restaurant[:4]
    
    for cat_restaurant in category_restaurants:
        avg_rating_category = restaurantFeedback.objects.filter(restaurant=cat_restaurant).aggregate(Avg('rating'))['rating__avg']
        cat_restaurant.avg_rating = avg_rating_category
        
    context = {
        'restaurant': restaurant,
        'restaurant_images': restaurant_images,
        'maps': maps,
        'coordinates': coordinates,
        'feedback_comments': feedback_comments,
        'avg_rating': avg_rating,
        'num_reviews': num_reviews,
        'filtered_restaurant': filtered_restaurant,
        'category_restaurants': category_restaurants,

    }

    return render(request, 'restaurant/restaurantDetail.html', context)


def submit_review_restaurant(request, restaurant_id):
    # getting the url fort the same webpage
    url  = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            # to check if review is already submitted
            reviews = restaurantFeedback.objects.get(user__id=request.user.id, restaurant__id = restaurant_id)
            form = FeedbackForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you, Your review has been updated')
            return redirect(url)
        except:
            form = FeedbackForm(request.POST)
            if form.is_valid():
                data = restaurantFeedback()
                data.rating = form.cleaned_data['rating']
                data.feedback = form.cleaned_data['feedback']
                data.restaurant_id = restaurant_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you, Your review has been submitted')
                return redirect(url)
            

def delete_comment_restaurant(request, comment_id):
    url  = request.META.get('HTTP_REFERER')

    # Fetch the comment object to be deleted
    comment = get_object_or_404(restaurantFeedback, id=comment_id)

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
