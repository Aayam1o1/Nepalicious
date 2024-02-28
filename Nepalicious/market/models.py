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

    productImage = models.ImageField(upload_to = "images/marketplace/productImage/")    
    productPrice = models.DecimalField(max_digits=10, decimal_places=2)
    productStock = models.IntegerField()
    productImage = models.ImageField(upload_to = "images/marketplace/productImage/", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.productName