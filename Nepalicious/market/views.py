from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Sum, F, Avg
import json
import requests
from django.http import HttpResponse
from django.db import transaction
import sweetify
from django.core.mail import send_mail


# Create your views here.
def marketplace(request):
    productList = addProducts.objects.all()
    
    for product in productList:
        # Calculate average rating for each product
        avg_rating = product.productfeedback_set.aggregate(Avg('rating'))['rating__avg']
        product.avg_rating = avg_rating  # Add avg_rating attribute to product instance
        
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
     
    # Calculate average rating
    avg_rating = productFeedback.objects.filter(product=productDetail).aggregate(Avg('rating'))['rating__avg']
    

    # Retrieve comments related to the specific product
    feedback_comments = productFeedback.objects.filter(product=productDetail) 
    # Count the number of reviews
    num_reviews = feedback_comments.count()
    context = {
        'productList': productList,
        'productdetailForImage' : productdetailForImage,
        'product_image' : product_image,
        'productDetail': productDetail,
        # 'feedback_form' : feedback_form,
        'feedback_comments': feedback_comments,
        'num_reviews': num_reviews,
        'avg_rating': avg_rating,
    }
    
    return render(request, 'marketplace/productDetail.html', context)



def submit_review_product(request, product_id):
    # getting the url fort the same webpage
    url  = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            # to check if review is already submitted
            reviews = productFeedback.objects.get(user__id=request.user.id, product__id = product_id)
            form = FeedbackForm(request.POST, instance=reviews)
            form.save()
            sweetify.success(request, 'Thank you, Your review has been updated')
            return redirect(url)
        except:
            form = FeedbackForm(request.POST)
            if form.is_valid():
                data = productFeedback()
                data.rating = form.cleaned_data['rating']
                data.feedback = form.cleaned_data['feedback']
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                sweetify.success(request, 'Thank you, Your review has been submitted')
                return redirect(url)

def delete_comment_product(request, comment_id):
    url  = request.META.get('HTTP_REFERER')

    # Fetch the comment object to be deleted
    comment = get_object_or_404(productFeedback, id=comment_id)

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

# for add to cart button
def add_to_cart(request, product_id):
    product = get_object_or_404(addProducts, id=product_id)

    # Get or create the user's cart
    user_cart, created = Cart.objects.get_or_create(user=request.user)

    new_address = request.user.usersdetail.address
    new_number = request.user.usersdetail.phone_number   
    seller = product.user
    
    print('seller', seller)
    # Check if the product is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=user_cart, product=product, seller=seller)

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
    
    user_cart.new_address = new_address
    user_cart.new_number = new_number
    
    user_cart.save()

   
    sweetify.success(request, "Product added to the cart successfully.")
    return redirect('marketplace')



def cart_view(request):
    user_cart = Cart.objects.filter(user=request.user).first()
    cart_item = CartItem.objects.filter(cart=user_cart)
    
    # if request.method == 'POST':
    #     print("AAAAAAAAAAAAAAA")
    #     # Get or create the user's cart
    #     user_cart_filter = user_cart

    #     # Iterate through products in the cart and update quantities
    #     for cart_items in CartItem.objects.filter(cart=user_cart_filter):
    #         new_quantity = int(request.POST.get(f"quantityInput-{cart_items.product.id}", 1))

    #         # Ensure the new quantity is within the limits (1 to product stock)
    #         new_quantity = max(1, min(new_quantity, cart_items.product.productStock))

    #         # Update the quantity in the cart item
    #         cart_items.quantity = new_quantity
    #         cart_items.save()
    #         cart_item.append(cart_items)
        
    #     messages.success(request, "Cart updated successfully.")
    # print("cart_itemcart_itemcart_itemcart_itemcart_itemcart_itemcart_item: ", cart_item)
    context = {

        'user_cart': user_cart,
        'cart_item' : cart_item,
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



def initkhalti(request):
    
    user = request.user.username
    userinfo = request.user
    contact = userinfo.usersdetail.phone_number
    email = userinfo.email

    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    
    return_url = request.POST.get('return_url')
    purchase_order_id = request.POST.get('purchase_order_id')
    amount = request.POST.get('amount')
    print(amount)

    payload = json.dumps({
        "return_url": return_url,
        "website_url": "http://127.0.0.1:8000",
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "test",
        "customer_info": {
            "name": user,
            "email": email,
            "phone": contact,
        }
    })
    headers = {
        'Authorization': 'key 74a324b745f74fa8aa2d8be8128e5ede', 
        'Content-Type': 'application/json',
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    new_res = json.loads(response.text)
    
    
    if new_res['payment_url']:
        
        return redirect(new_res['payment_url'])
        # return redirect("verify")
    else:
        messages.error(request, "Something went wrong.")
        return redirect("error")
    # payment_url = new_res.get('payment_url')
       
    # except Exception as e:
    #     print("Error occurred during payment initiation:", e)
    #     return HttpResponse("An error occurred during payment initiation")
     

    

def verifyKhalti(request):
    print('url hai::')
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    
    if request.method == 'GET':
        headers = {
            'Authorization': 'key 74a324b745f74fa8aa2d8be8128e5ede',
            'Content-Type': 'application/json',
        }
        pidx = request.GET.get('pidx')
        payload = json.dumps({
        'pidx': pidx
        })
        print('payload re hai:: ', payload)
        res = requests.request('POST',url,headers=headers,data=payload)
        new_res = json.loads(res.text)
        
        
        if new_res['status'] == 'Completed':
            try:
                # Get user's cart
                buyer = request.user
                cart = Cart.objects.get(user=buyer)
                cartItems = CartItem.objects.filter(cart=cart) # Assuming you want the first cart item
                
                # for cartItem in cartItems:
                #     product = cartItem.product
                #     seller = cartItem.product.user
                #     quantity = cartItem.quantity
                #     ordered_phone_number = cart.new_number
                #     ordered_address = cart.new_address
            
               
                with transaction.atomic():
                    print("Transaction started")  # Add this line for debugging
                    
                    new_order = order.objects.create(
                        buyer = buyer, 
                        total_amount=cart.total_amount,
                        ordered_phone_number = cart.new_number,
                        ordered_address = cart.new_address,
                    )
                    
                    # Loop through each cart item and create orderDetail instances
                    for cart_item in cartItems:
                        product = cart_item.product
                        quantity = cart_item.quantity
                        seller = cart_item.seller
                        total_each_product = product.productPrice * quantity
                        is_completed ='Shipping Pending'
                        
                        
                        #decrease quantity
                        product.productStock -= quantity
                        product.save()
                        
                        print("Seller:", seller.username)
                        orderDetail.objects.create(
                            order_for = new_order,
                            seller = seller,
                            product = product,
                            quantity= quantity,
                            total_each_product=total_each_product,
                            is_completed = is_completed
                        )           
                
                        
                    # Create orders directly from cart items
                    new_order.save()
                    # Clear the cart
                    cart.delete()
                    # cart.cartitem_set.all().delete()

            # Redirect  to payment success page
                    return render(request, 'payment/paymentsuccessful.html')
            
            
            except Exception as e:
                print("Error in transaction:", str(e))
                # Rollback transaction
                transaction.rollback()
                return redirect('error')
                
        else:
            return redirect('error')

    else:
        return redirect('error')
    


def checkout(request):
    if request.method == 'POST':
    
        
        user_cart, created = Cart.objects.get_or_create(user=request.user)

        # # Check if the cart is empty
        # if not user_cart.products.exists():
        #     # If the cart is empty, redirect the user back to the cart page
        #     return redirect('cart')

        # Update the address and number in the cart
        # if user_cart.products.exists():
        new_address = request.POST.get('address')
        new_number = request.POST.get('phone_number')
        
        # Update the address and number in the cart
        user_cart.new_address = new_address
        user_cart.new_number = new_number
        user_cart.save()
        return redirect('cart')
       
        
    return render(request, 'marketplace/cart.html')


def error(request):
    return render(request, "Payment/error.html")




def order_history(request):
    
    user= request.user
    orders = order.objects.filter(buyer=user)
    
    #retreving order id
    order_ids = orders.values_list('id', flat=True)
    orderlist = orderDetail.objects.filter(order_for__in=order_ids)
    
    context = {
        'user': user,
        'orders': orders,
        'orderlist': orderlist,     
       
    }
    return render(request, 'profiles/paymentHistory.html', context)


def pending_orders(request):
    if request.method == 'POST' and 'Update' in request.POST:
        status =  request.POST.get("status")
        orderID =  request.POST.get("order_id")
        quantity =  int(request.POST.get("productQuantity"))
        orderdetails =  orderDetail.objects.get(pk=orderID)
        UserEmail = orderdetails.order_for.buyer.email 
        
        print('email', UserEmail)
        print('quantity', quantity)
        print('orderDetails', orderdetails.id)
        if status == "Shipping Completed":
            orderdetails.is_completed = "Shipping Completed"
            
            print('order details complete', orderdetails.is_completed)
            orderdetails.save()
            print('sureee') 
            message = f"""Dear {orderdetails.order_for.buyer.username}, 
                Your order id - {orderdetails.id} - {orderdetails.product.productName} has been delivered. 
                Your paid amount is {orderdetails.total_each_product}. 
                Please contact our customer support for further information 
                Contact Number: 9840033590 
                
                Regards,
                [Nepalicious]"""
                
                
            # Sending mail after user is approved
            send_mail(
            "Your ordered item has been deliverd.",
            message,
            "nepalicious.webapp@gmail.com",
            [UserEmail],
            fail_silently=False,
            )
            
        elif status == 'Shipping Canceled':
            orderdetails.is_completed = 'Shipping Canceled'
            productID = orderdetails.product.id
            
            # updating quanity again
            productDetails = addProducts.objects.get(pk=productID)
            productDetails.productStock += quantity
            orderdetails.save()
            productDetails.save()
            message = f"""Dear {orderdetails.order_for.buyer.username},
            Your order id - {orderdetails.id} - {orderdetails.product.productName} delivery has been cancelled. 
            Your paid amount {orderdetails.total_each_product} will be refunded. 
            Please contact our customer support for further information 
            Contact Number: 9840033590 
                
                Regards,
                [Nepalicious]"""
            # Sending mail after user is approved
            send_mail(
            "Your item delivery has been cancelled.",
            message,
            "nepalicious.webapp@gmail.com",
            [UserEmail],
            fail_silently=False,
            )
            print("kal")
        
    seller = request.user
    sold_products = orderDetail.objects.filter(seller=seller)
    
    
        
    
    context = {
        'seller': seller,
        'sold_products': sold_products,
        
    }
    return render(request, 'profiles/pendingOrder.html', context)
