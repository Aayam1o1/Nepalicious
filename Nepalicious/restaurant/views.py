from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import *
import folium
import geocoder
from django.db.models import Sum, F, Avg, Q
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import sweetify
import re
from django.http import Http404
from django.contrib.auth.decorators import user_passes_test, login_required

def is_user(user):
    return user.groups.filter(name = 'restaurant').exists()
# Create your views here.
def restaurant(request):
    restaurant_list = addRestaurant.objects.all()
    
    search = request.GET.get('search_for')
    cuisineType = request.GET.get('cuisineType')
    print("search", search)
    
    if search:
        if search:
            restaurant_list = restaurant_list.filter(
                Q(user__usersdetail__restaurant_name__icontains=search) |
                Q(user__usersdetail__address__icontains=search)
            ).distinct()
        print("restaurant_list", restaurant_list)
        print("Search results count:", restaurant_list.count())  # Check the count of search results
    elif cuisineType:
        restaurant_list = restaurant_list.filter(Q(restaurantType__icontains=cuisineType))
    else:
        restaurant_list = addRestaurant.objects.all()
        print("No search query provided.")
        
    print("Final restaurant_list count:", restaurant_list.count()) 
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
    
    
    # for restaurant in restaurant_list:
    #     # Calculate average rating for each product
    #     avg_rating = restaurant.restaurantfeedback_set.aggregate(Avg('rating'))['rating__avg']
    #     restaurant.avg_rating = avg_rating  # Add avg_rating attribute to product instance
    
    
       
        
    context = {
        'restaurantList': restaurant_list
    }
    
    return render(request, 'restaurant/restaurant.html', context)

@login_required
@user_passes_test(is_user)
def addRestaurantdetail(request):
    if request.method == 'POST':
        form = addRestaurantForm(request.POST, request.FILES)
        if form.is_valid():
             # Save latitude and longitude
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            map_addres = request.POST.get('address')
            third_comma_index = map_addres.find(',', map_addres.find(',', map_addres.find(',') + 1) + 1)
            # Extract the substring up to the third comma
            map_addres = map_addres[:third_comma_index]
            
            
            print('lat:', latitude)
            print('long:', longitude)
            print('map_addres:', map_addres)
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
            
            
            location = Location.objects.create(restaurant=instance, latitude=latitude, longitude=longitude, map_addres=map_addres)
            print(location)
            
            user_detail = get_object_or_404(usersDetail, user=request.user)
            user_detail.address = map_addres
            user_detail.save()

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
    # restaurant = addRestaurant.objects.get(pk=restaurant_id)
    restaurant = get_object_or_404(addRestaurant, pk=restaurant_id)
    
    if not restaurant:
        if not (request.user.is_superuser or request.user.id == restaurant.user_id):
            raise Http404("Restaurant not found")
        restaurant = get_object_or_404(addRestaurant, pk=restaurant_id)

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
        marker_popup = f"<div style='width: 90px;'>{restaurant.user.usersdetail.restaurant_name}<br><strong>Address:</strong>{restaurant_location.map_addres}</div></div>"
        
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
            sweetify.success(request, 'Thank you, Your review has been updated')
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
                sweetify.success(request, 'Thank you, Your review has been submitted')
                return redirect(url)
            

def delete_comment_restaurant(request, comment_id):
    url  = request.META.get('HTTP_REFERER')

    # Fetch the comment object to be deleted
    comment = get_object_or_404(restaurantFeedback, id=comment_id)

    # Check if the logged-in user is the owner of the comment
    if comment.user == request.user:
        # Delete the comment
        comment.delete()
        sweetify.success(request, 'Comment deleted')
    else:
        sweetify.error(request, 'There was an error deleting the comment')
        pass

    # Redirect back to the page where the comment was deleted from
    return redirect(url)




@login_required
@user_passes_test(is_user)
def edit_restaurant(request, restaurant_id):
    url  = request.META.get('HTTP_REFERER')
    try:
        restaurant = get_object_or_404(addRestaurant, pk=restaurant_id)
        if request.user == restaurant.user:
            if not restaurant:

                if not (request.user.is_superuser or request.user == restaurant.user):
                    raise Http404("Room not found")

            restaurant = get_object_or_404(addRestaurant, pk=restaurant_id)
            new_location = Location.objects.get(restaurant=restaurant)
            
            
            restaurant_location = Location.objects.filter(restaurant=restaurant).first()

            
            if restaurant_location:
                    # Create a map centered at the restaurant's location
                    maps = folium.Map(location=[restaurant_location.latitude, restaurant_location.longitude], zoom_start=12)
                    
                    # Add a marker for the restaurant's location
                    marker_popup = f"<div style='width: 90px;'>{restaurant.user.usersdetail.restaurant_name}<br><strong>Address:</strong>{restaurant_location.map_addres}</div></div>"

                    folium.Marker([restaurant_location.latitude, restaurant_location.longitude], 
                            tooltip='Click for details', 
                            popup=marker_popup, max_width=400).add_to(maps)
                    
                    # Get the HTML representation of the map
                    maps = maps._repr_html_()
                    
            else:
                    # If no location is available, provide a default map centered at a specific location
                maps = folium.Map(location=[27.7172, 85.3240], zoom_start=14)._repr_html_()
                
                
            if request.method == 'POST':

                form = editRestaurantForm(request.POST, instance=restaurant)
                restaurant_name = request.POST.get('restaurant_name')
                restaurant_number = request.POST.get('phone_number')
                latitude = request.POST.get('latitude')
                longitude = request.POST.get('longitude')
                map_addres = request.POST.get('address')
                third_comma_index = map_addres.find(',', map_addres.find(',', map_addres.find(',') + 1) + 1)
                map_addres = map_addres[:third_comma_index]
                print("map_addres:", map_addres)

                if latitude != '' and longitude != '':
                    print('lat:', latitude)
                    print('long:', longitude)
                    new_location.latitude = latitude
                    new_location.longitude = longitude
                    new_location.map_addres = map_addres
                    restaurant.user.usersdetail.address = map_addres
                    restaurant.user.usersdetail.save()                

                    new_location.save()
                
                
                if not re.match(r'^(98|97)\d{8}$', restaurant_number):
                        sweetify.error(request,"Invalid contact number")
                        return redirect(url)
                print('name', restaurant_name)
                print('number', restaurant_number)
                if form.is_valid():
                    form.save()
                    restaurant.user.usersdetail.restaurant_name = restaurant_name
                    restaurant.user.usersdetail.phone_number = restaurant_number
                    restaurant.user.usersdetail.save()                

                    new_images = request.FILES.getlist('restaurantImage')
                
                    # Get the list of existing images
                    old_images = restaurant.images.all()
                    
                    # Delete old images not included in the new se
                    # Handle restaurant images
                    if new_images:
                        print("print1")
                        for old_image in old_images:
                            if old_image.image not in new_images:
                                old_image.delete()
                                
                        for uploaded_file in new_images:
                            restaurantImage.objects.create(addRestaurant=restaurant, image=uploaded_file)
                    sweetify.success(request, "Resturant details updated successfully")
                    return redirect('restaurant_detail', restaurant_id=restaurant.id)
            else:
                form = editRestaurantForm(instance=restaurant)
        else:
            return render(request, '404.html')
    except addRestaurant.DoesNotExist:
        pass    
    
    context = {
        'form':form,
        'restaurant': restaurant, 
        'maps': maps,

    }
    
    
    return render(request, 'restaurant/editRestaurant.html', context)

@login_required
@user_passes_test(is_user)
def delete_restaurant(request, restaurant_id):
    url  = request.META.get('HTTP_REFERER')
    restaurant = addRestaurant.objects.get(id=restaurant_id)
    if request.method == 'POST':
        try:
            restaurant.delete()
            sweetify.success(request, "Restaurant has been deleted successfully", timer=3000)
            return redirect('restaurant')
        except Exception as e:
            sweetify.error(request, f"Error deleting Resturant: {str(e)}")
            return redirect(url)
    return redirect('restaurant')