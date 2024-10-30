from django.contrib import admin
from .models import Product, Vehicle, Customer, Order, Invoice

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['header', 'oem_number', 'price', 'stock']
    search_fields = ['header', 'oem_number']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'total_price', 'created_at', 'get_products']
    search_fields = ['order_number', 'customer__name']
    filter_horizontal = ('products',)

    def get_products(self, obj):
        return ", ".join([product.part_number for product in obj.products.all()])
    get_products.short_description = 'Ordered Products'

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'vat_exempt']
    list_filter = ['vat_exempt']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['order', 'created_at', 'total_price']
