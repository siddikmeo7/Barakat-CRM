from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
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
    address = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_password_reset = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.last_password_reset:
            self.last_password_reset = now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} : {self.email}"
    
from django.db import models

class Client(models.Model):
    user = models.ForeignKey("Nur.CustomUser", on_delete=models.CASCADE, related_name="clients")
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2,default=0)
    
    def __str__(self):
        return self.name

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
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

# Location Models
class Country(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey("Nur.Country", on_delete=models.CASCADE, related_name="cities")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (Country: {self.country.name})"

# Product Models
class Product(models.Model):
    user = models.ForeignKey("Nur.CustomUser",on_delete=models.CASCADE)
    category = models.ForeignKey("Nur.Category", on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=50, null=True, blank=True)
    index = models.CharField(max_length=50, unique=True, db_index=True, help_text="Unique identifier for the product")
    colour = models.ForeignKey("Nur.Colour", on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(max_digits=15, decimal_places=2, help_text="Current product price")
    up_to = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], help_text="Maximum quantity available")
    sold = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], help_text="Total quantity sold")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def sell(self, quantity):
        if quantity > self.up_to:
            raise ValidationError("Not enough stock available to sell this quantity.")
        self.sold += quantity
        self.up_to -= quantity
        self.save()

    def get_revenue(self):
        return self.sold * self.price

    def __str__(self):
        return f"{self.title} ({self.index})"

class Category(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Colour(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Sklad (Warehouse) Models
class Sklad(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class SkladProduct(models.Model):
    sklad = models.ForeignKey("Nur.Sklad", on_delete=models.CASCADE, related_name="sklad_products")
    product = models.ForeignKey("Nur.Product", on_delete=models.CASCADE, related_name="sklad_products")
    quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.sklad.name} - {self.product.title or 'Unnamed Product'}"
    
class Order(models.Model):
    user = models.ForeignKey("Nur.CustomUser", on_delete=models.CASCADE)
    client = models.ForeignKey("Nur.Client", on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey("Nur.Product", on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField(default=0)
    price_at_purchase = models.DecimalField(max_digits=15, decimal_places=2)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')])

    def __str__(self):
        return f"Order #{self.id} - {self.client.name}"