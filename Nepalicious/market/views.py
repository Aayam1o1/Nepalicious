from django.shortcuts import render, redirect, get_object_or_404
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


# for product descriptiion.
def productDetail(request, product_id):
    
    productList = addProducts.objects.all()
    
    # to get the details of the product
    productDetail = get_object_or_404(addProducts, id=product_id)
    
    
    #to get the image of the product
    productdetailForImage = get_object_or_404(addProducts, id=product_id)

    product_image = productImage.objects.filter(addProducts = productdetailForImage)
    
    context = {
        'productList': productList,
        'productdetailForImage' : productdetailForImage,
        'product_image' : product_image,
        'productDetail': productDetail,
    }
    
    return render(request, 'marketplace/productDetail.html', context)


# for add to cart button
def add_to_cart(request, product_id):
    product = get_object_or_404(addProducts, id=product_id)

    # Get or create the user's cart
    user_cart, created = Cart.objects.get_or_create(user=request.user)

    # Add the selected product to the cart
    user_cart.products.add(product)

    messages.success(request, "Product added to the cart successfully.")
    return redirect('marketplace')

# for cart operations
def cart_view(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    products_in_cart = user_cart.products.all()
    
    context = {
        'products_in_cart': products_in_cart,
    }

    
    for product_in_cart in products_in_cart:
        print(f"Product Name: {product_in_cart.productName}")
        print(f"Product Brand: {product_in_cart.productBrand}")
        print(f"Product Price: {product_in_cart.productPrice}")
        print(f"Product Images: {[image.image.url for image in product_in_cart.images.all()]}")
    return render(request, 'marketplace/cart.html', context)
