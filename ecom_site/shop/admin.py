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
    search_fields = ['title', 'category']
    actions = ['change_category_to_default']
    # Allowing only some of the fields to be  visible
    fields = ['title', 'price', 'discount_price', 'category', 'description']

    def change_category_to_default(self, request, queryset):
        queryset.update(category="default")

    change_category_to_default.short_description = "Default Category"


class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'items', 'email', 'address', 'city', 'state',
                    'zip_code', 'created_at', 'total_price', 'payment_done']
    list_filter = ['payment_done', 'created_at']
    search_fields = ['name', 'email', 'city', 'state']
    # Allowing only some of the fields to be visible
    fields = ['name', 'items', 'email', 'address', 'city', 'state']


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
