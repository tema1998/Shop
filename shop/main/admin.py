from django.contrib import admin

from .models import Categories, Products, Basket


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Categories, CategoriesAdmin)


class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'price', 'stock', 'available', 'created_at', 'updated_at']
    list_filter = ['available', 'created_at', 'updated_at']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Products, ProductsAdmin)


class BasketAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'amount']
admin.site.register(Basket, BasketAdmin)