from django.db import models
from django.contrib.auth.models import User

# Model representing individual clothing products
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('MEN', 'Men'),
        ('WOMEN', 'Women'),
        ('KIDS', 'Kids'),
    ]
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    image_url = models.URLField(blank=True, null=True) # Direct web links or 3D canvas resource keys

    def __str__(self):
        return self.name

# Model representing user checkouts and purchases
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Links directly to standard Django User SQL table
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Processing')

    # Shipping-related fields
    shipping_option = models.ForeignKey('ShippingOption', on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.TextField(blank=True, null=True)
    shipping_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    shipped_date = models.DateTimeField(blank=True, null=True)
    tracking_number = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class ShippingOption(models.Model):
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    estimated_days = models.IntegerField(default=3)
    carrier = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f"{self.name} — ₹{self.price} ({self.estimated_days}d)"