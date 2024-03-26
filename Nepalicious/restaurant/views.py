from django.shortcuts import render, redirect, HttpResponse
from .models import *
from .forms import *
import folium
import geocoder

# Create your views here.
def restaurant(request):
    return render(request, 'restaurant/restaurant.html')

def addRestaurant(request):
    # if request.method == 'POST':
    #     form = SearchForm(request.POST)
    #     if form.is_valid():
    #         restaurant_address = form.cleaned_data.get('restaurantaddress')
            
    #         print('restaurant', restaurant_address)
    #         if restaurant_address:
    #             search = Search.objects.create(user=request.user, restaurantaddress=restaurant_address)
    #             location = geocoder.osm(restaurant_address)
    #             search.latitude = location.lat
    #             search.longitude = location.lng
    #             search.user = request.user
    #             search.save()
    #             return redirect('addRestaurant')
    #         else:
    #             return HttpResponse("Restaurant address is required")

    # else:
    #     form =  SearchForm()
    
    # restaurantaddress = Search.objects.all().last()
    # #osm = open street maps
    # if restaurantaddress:
    #     location = geocoder.osm(restaurantaddress)
    #     lat = location.lat
    #     lng = location.lng
    #     country = location.country
    
    
    #     if lat == None or lng == None:
    #         if restaurantaddress:
    #             restaurantaddress.delete()
    #         return HttpResponse("Youre address input is invalid")
        
    # Creating map object
    #     maps = folium.Map(location=[27.7172, 85.3240], zoom_start=12)
    #     # folium.Marker([27.7198, 85.3133], tooltip='Click for more', popup='Dallu').add_to(maps)
        
    #     # folium.Marker([lat, lng], tooltip='Click for details', popup=country).add_to(maps)
    #     #getting html representation of map object
    #     maps = maps._repr_html_()
    # else:
    #     maps = folium.Map(location=[27.7172, 85.3240], zoom_start=12)._repr_html_()
    
    # context = {
    #     'maps': maps,
    #     'form': form,
    # }
    
    
    return render(request, 'restaurant/addRestaurant.html')