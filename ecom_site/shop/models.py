from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    discount_price = models.FloatField()
    category = models.CharField(max_length=255)
    description = models.TextField()
    image = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} - {self.category}"


class Order(models.Model):
    items = models.CharField(max_length=3000)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField()
    payment_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"
