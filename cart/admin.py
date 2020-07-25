from django.contrib import admin
from .models import (
    Product, OrderItem, Order, LicenceVariation, Address
)


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'address_line_1',
        'address_line_2',
        'city',
        'zip_code',
        'address_type',
    ]


admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(LicenceVariation)
admin.site.register(Address, AddressAdmin)
