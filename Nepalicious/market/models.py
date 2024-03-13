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

    def __str__(self):
        return f"Cart for {self.user.username}"