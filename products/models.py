from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("cupcakes", "Cupcakes"),
        ("cookies", "Cookies"),
        ("wedding", "Wedding Cakes"),
        ("birthday", "Birthday Cakes"),
        ("delivery", "Cake Deliveries"),
        ("decorating", "Cake Decorating"),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

# Create your models here.
