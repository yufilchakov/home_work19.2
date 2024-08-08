from django.contrib import admin
from product.models import Category, Product, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description',)
    
    
@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'version_number', 'version_name', 'current_version_indicator',)
