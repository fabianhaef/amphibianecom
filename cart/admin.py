from django.contrib import admin
from .models import Product, OrderItem, Order, LicenceVariation

admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(LicenceVariation)
