from django.shortcuts import render
from .models import Product, Category

# Create your views here.

def get_product(request, slug):
    try:
        product = Product.objects.filter(slug=slug)
    except Exception as e:
        print(e)
    context={
        'categories':Category.objects.all(),
        'product':product.first()
    }
    return render(request, 'product/product-detail.html', context=context)
