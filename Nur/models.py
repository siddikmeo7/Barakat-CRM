from django.db import models
from django.contrib.auth.models import AbstractUser

# User
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)
    country = models.OneToOneField("Nur.Country",on_delete=models.CASCADE)
    city = models.OneToOneField("Nur.City",on_delete=models.CASCADE)
    region = models.OneToOneField("Nur.Region",on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Country(models.Model):
    name = models.CharField(max_length=50)

class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.OneToOneField("Nur.Country",on_delete=models.CASCADE)

class Region(models.Model):
    name = models.CharField(max_length=50)
    city = models.OneToOneField("Nur.City",on_delete=models.CASCADE)

# Product
class Product(models.Model):
    category = models.ForeignKey("Nur.Category",on_delete=models.CASCADE)
    index =  models.CharField(max_length=50)
    colour = models.ForeignKey("Nur.Colour",on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    up_to = models.DecimalField(max_digits=15, decimal_places=2)
    sold = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Category(models.Model):
    name = models.CharField(max_length=50)

class Colour(models.Model):
    name = models.CharField(max_length=50)

# Sklad
class Sklad(models.Model):
    name = models.CharField(max_length=50)

class SkladProduct(models.Model):
    sklad = models.ForeignKey("Nur.Sklad",on_delete=models.CASCADE)
    product = models.ForeignKey("Nur.Product",on_delete=models.CASCADE)