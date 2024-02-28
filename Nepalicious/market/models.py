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

 #Category choices
productTagChoice = (
    ('spice', 'spice'),
    ('pots', 'pots'),
    ('knifes', 'knifes'),
    ('appliance', 'appliance'),
)


# Create your models here.
class addProducts(models.Model):
    productName = models.CharField(max_length=100)
    producBrand = models.CharField(max_length=100)
    productDescription = models.TextField()
    productCategory = models.CharField(max_length=20,choices=productCategoryChoice, default='spicesFood')
    productTag = models.CharField(max_length=20,choices=productTagChoice, default='spice')
    productImage = models.ImageField(upload_to = "images/marketplace/productImage/")    
    productPrice = models.DecimalField(max_digits=10, decimal_places=2)
    productStock = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)