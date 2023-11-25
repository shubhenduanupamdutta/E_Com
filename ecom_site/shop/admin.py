from django.contrib import admin
from .models import Order, Product
# Register your models here.

# customizing admin panel
admin.site.site_header = "E-commerce Site SomaShubh"
admin.site.site_title = "SomaShubh"
admin.site.index_title = "Manage SomaShubh Shop"


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'discount_price', 'category']
    list_filter = ['category']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'items', 'email', 'address', 'city', 'state',
                    'zip_code', 'created_at', 'total_price', 'payment_done']
    list_filter = ['payment_done', 'created_at']


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
