from django.shortcuts import render
from product.models import Product, Category
from django.http import JsonResponse
# Create your views here.

def home(request):
    context = {'products': Product.objects.all(), 'category':Category.objects.all()}
    return render(request, 'home/index.html', context=context)


def cart(request):
    return render(request, 'home/cart.html')

def contact(request):
    return render(request, 'home/contact.html')

def blog(request):
    return render(request, 'home/blog.html')

def checkout(request):
    return render(request, 'home/checkout.html')
