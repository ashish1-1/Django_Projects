from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('category/<slug>', views.shop, name='category'),
    path('product_price_filter/', views.product_price_filter, name='product_price_filter'),
    path('addToCart/',views.addToCart, name='addToCart'),

]
