from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.CharField(max_length=255, default='path/to/default/image.jpg')
    
    def __str__(self):
        return self.name