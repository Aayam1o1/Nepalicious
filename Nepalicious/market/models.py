from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


 #Category choices
productCategoryChoice = (
    ('spicesFood', 'SpicesFood'),
    ('pansPots', 'PansPots'),
    ('knifes', 'knifes'),
    ('electricAppliance', 'electricAppliance'),
    ('cleaningAppliance', 'cleaningAppliance')
)



# Create your models here.
class addProducts(models.Model):
    productName = models.CharField(max_length=100)
    productBrand = models.CharField(max_length=100)
    productDescription = models.TextField()
    productCategory = models.CharField(max_length=100, choices=productCategoryChoice)
    productPrice = models.DecimalField(max_digits=10, decimal_places=2)
    productStock = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isdeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.productName
    
    
class productImage(models.Model):
    addProducts = models.ForeignKey(addProducts, related_name ='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/marketplace/productImage/')
    
    def __str__(self):
        return f"{self.addProducts.productName} - {self.pk}"
    
class productFeedback(models.Model):
    product = models.ForeignKey(addProducts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField(blank=True)
    rating = models.FloatField()
        
    def __str__(self):
        return f"{self.product.productName} - {self.user.username}"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('addProducts')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    new_address = models.CharField(max_length=100, blank = True, default='')
    new_number = models.CharField(max_length=10, blank = True, default='')
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def update_total_amount(self):
        # Calculate total amount based on the quantity of each item in the cart
        total = sum(item.product.productPrice * item.quantity for item in self.cartitem_set.all())
        self.total_amount = total
        self.save()
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('addProducts', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Add a quantity field
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_cart_items')    
    
    def __str__(self):
        return f"{self.quantity} x {self.product.productName} in Cart for {self.cart.user.username}"
    

class order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_phone_number = models.CharField(max_length=10)    
    ordered_address = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    buy_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order for {self.buyer.username} - {self.id}"
    
    
    
class orderDetail(models.Model):
    complete_choice = (
        ('Delivery Canceled', 'Delivery Canceled'),
        ('Delivery Completed', 'Delivery Completed'),
        ('Delivery Pending', 'Delivery Pending'),
    )
    order_for = models.ForeignKey(order, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='seller')
    product = models.ForeignKey('addProducts', on_delete=models.CASCADE, related_name='ordered_products')
    quantity = models.PositiveIntegerField() 
    total_each_product = models.DecimalField(max_digits=10, decimal_places=2) 
    is_completed = models.CharField(max_length=120, choices=complete_choice, default='Delivery Pending')

    def __str__(self):
        return f"Order details for {self.order_for} - {self.id}"