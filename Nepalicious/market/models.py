from django.db import models
from django.db import models
from django.contrib.auth.models import User


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
    
    def __str__(self):
        return self.productName
    
    
class productImage(models.Model):
    addProducts = models.ForeignKey(addProducts, related_name ='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/marketplace/productImage/')
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('addProducts')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

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

    def __str__(self):
        return f"{self.quantity} x {self.product.productName} in Cart for {self.cart.user.username}"