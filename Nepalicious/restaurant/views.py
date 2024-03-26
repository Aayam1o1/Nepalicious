from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

from .models import *
from .forms import *
import folium
import geocoder

# Create your views here.
def restaurant(request):
    restaurant_list = addRestaurant.objects.all()
    
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
                restaurantImage.objects.create(addRecipe=instance, image=image)
                
            print('selected restarunt image: ', restaurant_image)
    
            instance.save()
            
            
            
            location = Location.objects.create(restaurant=instance, latitude=latitude, longitude=longitude)
            print(location)
            

            messages.success(request, "Sucessfully added Restaurant!!")    
        else:
            print(form.errors)
            
    else:
        form = addRestaurantForm()
    
    
    context = {
        'form': form,
    }    
    return render(request, 'restaurant/addRestaurant.html', context)