from django.db import models

# Create your models here.


class Products(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    discount_price = models.FloatField()
    category = models.CharField(max_length=255)
    description = models.TextField()
    image = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} - {self.category}"
