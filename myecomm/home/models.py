from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from product.models import Product

# Create your models here.
class SaleOrder(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    taxPrice = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) 
    shippingPrice = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0.0)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDeliver = models.BooleanField(default=False)
    deliverAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.created_at)



class OrderLines(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(SaleOrder, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    qty =  models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self) -> str:
        return self.name
    
class ShippingAddress(BaseModel):
    order = models.OneToOneField(SaleOrder, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    postalCode = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=120, null=True, blank=True)
    shippingPrice = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self) -> str:
        return self.address


