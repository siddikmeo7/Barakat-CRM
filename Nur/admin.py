from django.contrib import admin
from .models import *

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number', 'address', 'created_at', 'last_password_reset']
    list_filter = ['address']
    search_fields = ['username', 'email', 'phone_number', 'address']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('client', 'transaction_type', 'amount', 'created_at', 'user')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('client__name', 'user__username', 'comments')

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
