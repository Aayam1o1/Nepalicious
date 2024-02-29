from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages

# Create your views here.
def marketplace(request):
    productList = addProducts.objects.all()
    
    context = {
        'productList': productList,
        
    }
    
    return render(request, 'marketplace/marketplace.html', context)

# for adding products for markteplace
def addProduct(request):
    
    # getting data from forms.py
    if request.method == 'POST':
        form = addProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            instance = form.save(commit=False) #commit=False helps to not to save the form
            instance.user = request.user
            
           # Handle productCategory field
            selected_category_name = form.cleaned_data['productCategory']
            
            # Set the selected category for the product
            instance.productCategory = selected_category_name
            

            instance.save()
            
            # Step 2: Image handle
            # Handle product images
            product_image = request.FILES.getlist('productImage')
            for image in product_image:
                productImage.objects.create(addProducts=instance, image=image)
                
            messages.success(request, "Sucessfully added product")
            
            # Redirect to a page or route after successfully adding a product
            return redirect('marketplace') 
        else:
            print("please")
            print(form.errors)
        
    else:
        form = addProductForm()
        
        
    context = {
        
        'form' : form,
    }
            
    return render(request, 'marketplace/addProduct.html', context)

def productDetail(request):
    
    productList = addProducts.objects.all()
    
    context = {
        'productList': productList,
        
    }
    
    return render(request, 'marketplace/productDetail.html', context)
