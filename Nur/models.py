from django.db import models
from django.dispatch import receiver
from django.utils.timezone import now
from django.db.models.signals import post_save
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
    address = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_password_reset = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.last_password_reset:
            self.last_password_reset = now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} : {self.email}"

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

# Product Models
class Product(models.Model):
    user = models.ForeignKey("Nur.CustomUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Nur.Category", on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=50, null=True, blank=True)
    index = models.CharField(max_length=50, unique=True, db_index=True, help_text="Unique identifier for the product")
    colour = models.ForeignKey("Nur.Colour", on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(max_digits=15, decimal_places=2, help_text="Current product price")
    cost_price = models.DecimalField(max_digits=15, decimal_places=2, help_text="Product cost price")  # Add this field
    up_to = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], help_text="Maximum quantity available")
    sold = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], help_text="Total quantity sold")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title or 'Unnamed Product'} - {self.colour.name} (Category: {self.category.name})"

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
    location = models.CharField(max_length=50)
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

# Transaction of Clients  Loan/Paid
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('loan', 'Loan'),
        ('repay', 'Repay'),
    ]
    user = models.ForeignKey("Nur.CustomUser", on_delete=models.CASCADE)
    client = models.ForeignKey("Nur.Client", on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
@receiver(post_save, sender=Transaction)
def update_client_balance(sender, instance, created, **kwargs):
    if created:
        client = instance.client
        if instance.transaction_type == 'loan':
            client.balance += instance.amount
        elif instance.transaction_type == 'repay':
            client.balance -= instance.amount
        client.save()

    def __str__(self):
        return f"{self.client.name} - {self.transaction_type} - {self.amount}"
    

# Shop Part 
class ShopCategory(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class ShopProduct(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ShopCategory, on_delete=models.CASCADE, related_name='shop_products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    

class CartItem(models.Model):
    product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at  = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def total_price(self):
        return self.product.price * self.quantity

    def clean(self):
        if self.quantity > self.product.stock:
            raise ValidationError("Quantity exceeds available stock.")

    def save(self, *args, **kwargs):
        self.clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"



