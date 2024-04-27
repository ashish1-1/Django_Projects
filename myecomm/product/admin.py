from django.contrib import admin
from .models import Product, Category, ProductImages, Review
# Register your models here.



class ProductImageAdmin(admin.StackedInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(ProductImages)
admin.site.register(Review)
