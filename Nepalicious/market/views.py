from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages

# Create your views here.
def marketplace(request):
    return render(request, 'marketplace/marketplace.html')

# for adding products for markteplace
def addProduct(request):
    
    # getting data from forms.py
    if request.method == 'POST':
        form = addProductForm(request.POST, request.FILES)
        productName = request.POST.get('productName')
        productBrand = request.POST.get('productBrand')
        productDescription = request.POST.get('productDescription')
        productPrice = request.POST.get('productPrice')
        productStock = request.POST.get('productStock')
        
        
        if form.is_valid():
            instance = form.save(commit=False) #commit=False helps to not to save the form
            instance.user = request.user
            instance.save()
            
            messages.success(request, "Sucessfully added product")
            
             # Redirect to a page or route after successfully adding a product
            return redirect('../static/marketplace/marketplace.html') 
            
    return render(request, 'marketplace/addProduct.html')