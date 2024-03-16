from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Sum, F


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

    # Check if the product is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=user_cart, product=product)

    # If the item is already in the cart, increase the quantity
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    else:
        # Set the initial quantity to 1 for a newly added item
        cart_item.quantity = 1
        cart_item.save()

    # Update the total amount in the cart
    user_cart.total_amount = CartItem.objects.filter(cart=user_cart).aggregate(total=Sum(F('product__productPrice') * F('quantity')))['total']
    user_cart.save()

    messages.success(request, "Product added to the cart successfully.")
    return redirect('marketplace')



def cart_view(request):
    if request.method == 'POST':
        # Get or create the user's cart
        user_cart, created = Cart.objects.get_or_create(user=request.user)

        # Iterate through products in the cart and update quantities
        for cart_item in CartItem.objects.filter(cart=user_cart):
            new_quantity = int(request.POST.get(f"quantityInput-{cart_item.product.id}", 1))

            # Ensure the new quantity is within the limits (1 to product stock)
            new_quantity = max(1, min(new_quantity, cart_item.product.productStock))

            # Update the quantity in the cart item
            cart_item.quantity = new_quantity
            cart_item.save()

        messages.success(request, "Cart updated successfully.")

    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = user_cart.cartitem_set.all()  # Retrieve all cart items for the user's cart

    context = {
        'cart_items': cart_items,
        'user_cart': user_cart
    }

    return render(request, 'marketplace/cart.html', context)

# for update cart button
def update_cart(request):
    if request.method == 'POST':
        # Print request.POST data
        print(f"POST data: {request.POST}")

        # Get or create the user's cart
        user_cart, created = Cart.objects.get_or_create(user=request.user)

        
        print(user_cart)

        # Initialize the total amount
        total_amount = 0
        
        if "delete" in request.POST:
            pId = request.POST.get('delete')
            item_to_delete = CartItem.objects.filter(product_id=pId).first()
            print(item_to_delete)
            if item_to_delete:
                item_price = item_to_delete.product.productPrice
                print("item_price", item_price)
                # Delete the item from the cart
                item_to_delete.delete()

                # Recalculate the total amount
                user_cart.total_amount -= item_price * item_to_delete.quantity
                if user_cart.total_amount < 0:
                    user_cart.total_amount = 0
                
                # Save the cart
                user_cart.save()

                
                # user_cart.save()
            
            

        # Iterate through products in the cart and update quantities
        for cart_item in user_cart.cartitem_set.all():
            print("cart items: ", cart_item.quantity)
            # Modify the cart_item_id to use the product ID
            cartID = str(cart_item.product.id)
            new_quantity = request.POST.get('quantityInput-'+ cartID)
            print('quantityInput-'+ cartID)
            
            if new_quantity == None:
                oldQuantity = cart_item.quantity
                # Update the quantity in the cart item
                cart_item.quantity = oldQuantity
                cart_item.save()
            else:
                cart_item.quantity = new_quantity
                cart_item.save()
                
            user_cart.update_total_amount()
                
                
    return redirect('cart')



