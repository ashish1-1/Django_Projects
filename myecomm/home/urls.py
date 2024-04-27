from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('shop-cart/',views.cart, name='cart'),
    path('contact/',views.contact, name='contact'),
    path('blog/',views.blog, name='blog'),
    path('checkout/',views.checkout, name='checkout'),

]