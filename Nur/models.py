from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator

# User
class CustomUser(AbstractUser):
    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                r'^\+?1?\d{9,15}$',
                message="Enter a valid phone number (e.g., +123456789)."
            )
        ]
    )
    country = models.ForeignKey("Nur.Country", on_delete=models.CASCADE, related_name="users",null=True,blank=True)
    city = models.ForeignKey("Nur.City", on_delete=models.CASCADE, related_name="users", null=True, blank=True)
    region = models.ForeignKey("Nur.Region", on_delete=models.CASCADE, related_name="users",null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_password_reset = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.last_password_reset:
            self.last_password_reset = now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} : {self.email}"
    
class Profile(models.Model):
    user = models.OneToOneField(
        'Nur.CustomUser', on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="images/profile_pics/", blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

# Location Models
class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey("Nur.Country", on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        return f"{self.name} (Country: {self.country.name})"

class Region(models.Model):
    name = models.CharField(max_length=50)
    city = models.ForeignKey("Nur.City", on_delete=models.CASCADE, related_name="regions")

    def __str__(self):
        return f"{self.name} (City: {self.city.name})"

# Product Models
class Product(models.Model):
    category = models.ForeignKey("Nur.Category", on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=50, null=True, blank=True)
    index = models.CharField(max_length=50, unique=True, db_index=True, help_text="Unique identifier for the product")
    colour = models.ForeignKey("Nur.Colour", on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(max_digits=15, decimal_places=2, help_text="Current product price")
    up_to = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], help_text="Maximum quantity available")
    sold = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], help_text="Total quantity sold")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title or 'Unnamed Product'} - {self.colour.name} (Category: {self.category.name})"

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Colour(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Sklad (Warehouse) Models
class Sklad(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SkladProduct(models.Model):
    sklad = models.ForeignKey("Nur.Sklad", on_delete=models.CASCADE, related_name="sklad_products")
    product = models.ForeignKey("Nur.Product", on_delete=models.CASCADE, related_name="sklad_products")

    def __str__(self):
        return f"{self.sklad.name} - {self.product.title or 'Unnamed Product'}"