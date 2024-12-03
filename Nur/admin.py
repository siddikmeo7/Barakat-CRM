from django.contrib import admin
from .models import *

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number', 'address', 'created_at', 'last_password_reset']
    list_filter = ['country', 'city', 'address']
    search_fields = ['username', 'email', 'phone_number', 'address']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    list_filter = ['country']
    search_fields = ['name', 'country']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']
    search_fields = ['user__username', 'bio']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','index', 'category', 'price','created_at']
    list_filter = ['category', 'price']
    search_fields = ['name', 'category__name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Colour)
class ColourAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Sklad)
class SkladAdmin(admin.ModelAdmin):
    list_display = ['name',]
    search_fields = ['name',]


@admin.register(SkladProduct)
class SkladProductAdmin(admin.ModelAdmin):
    list_display = ['sklad', 'product', 'quantity']
    list_filter = ['sklad', 'product']
    search_fields = ['sklad__name', 'product__name']
