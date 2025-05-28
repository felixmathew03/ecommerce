from django.db import models

# Create your models here.

class Category(models.Model):
    c_name=models.CharField(max_length=255,unique=True)
    
    def __str__(self):
        return self.c_name
    
class Product(models.Model):
    p_name = models.CharField(max_length=200)
    p_description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Better to rename this to 'category'
    p_price = models.DecimalField(max_digits=10, decimal_places=2)  # Recommended field for price
    p_stock = models.PositiveIntegerField(default=0)  # Optional: stock quantity
    p_image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.p_name
    