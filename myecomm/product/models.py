from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to='categories')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.category_name


class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    product_desc = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    numReview = models.IntegerField(null=True, blank=True, default=0)
    countInStock = models.IntegerField(null=True, blank=True, default=0)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product_name


class ProductImages(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    product_image = models.ImageField(upload_to='product')

class Review(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)


    def __str__(self) -> str:
        return self.rating
