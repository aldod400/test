from django.db import models
from account.models import UserProfile
# Create your models here.

class Category(models.TextChoices):
    COMPUTERS = "Computers"
    FOOD      = "Food"
    HOME      = "Home"
    KIDS      = "Kids"


class Product(models.Model):
    name        = models.CharField(max_length=100, default="", blank=False)
    description = models.TextField(default="", blank=False)
    price       = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    brand       = models.CharField(max_length=200, default="", blank=False)
    category    = models.CharField(max_length=40, blank=False, choices=Category.choices)
    rating      = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    stock       = models.IntegerField(default=0)
    createdAt   = models.DateTimeField(auto_now_add=True)
    user        = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null = True)
    
    def __str__(self):
        return self.name