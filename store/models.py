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

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"