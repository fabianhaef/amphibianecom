from django.contrib import admin
from .models import Product, OrderItem, Order, LicenceVariations

admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(LicenceVariations)