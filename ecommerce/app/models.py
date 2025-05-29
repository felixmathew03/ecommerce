from django.db import models
from django.utils.translation import gettext_lazy as _

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

class Customer(models.Model):
    cust_name=models.CharField(max_length=255)
    cust_phone=models.IntegerField()
    cust_email=models.EmailField(max_length=255,unique=True)
    cust_username=models.CharField(max_length=255)
    cust_password=models.TextField(max_length=255)
    

class OrderStatus(models.TextChoices):
    PROCESSING = 'Processing', _('Processing')
    SHIPPED = 'Shipped', _('Shipped')
    DELIVERED = 'Delivered', _('Delivered')
    CANCELLED = 'Cancelled', _('Cancelled')

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=OrderStatus.choices,
        default=OrderStatus.PROCESSING
    )

    def __str__(self):
        return f"Order #{self.id} - {self.customer.cust_username}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.price_at_order

    def __str__(self):
        return f"{self.quantity} × {self.product.p_name}"
