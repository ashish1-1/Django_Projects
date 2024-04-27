from django.contrib import admin
from . models import OrderLines, SaleOrder, ShippingAddress
# Register your models here.

admin.site.register(OrderLines)
admin.site.register(ShippingAddress)

@admin.register(SaleOrder)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'created_at',
        'totalPrice'
    ]

