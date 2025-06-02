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
    
class Address(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='addresses')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_line1}, {self.city} ({self.customer.cust_name})"
    
class OrderStatus(models.TextChoices):
    PROCESSING = 'Processing', _('Processing')
    PACKED = 'Packed', _('Packed')
    SHIPPED = 'Shipped', _('Shipped')
    DELIVERED = 'Delivered', _('Delivered')
    CANCELLED = 'Cancelled', _('Cancelled')

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey('Address', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=[('cod', 'Cash on Delivery'), ('online', 'Online')])
    status = models.CharField(
        max_length=50,
        choices=OrderStatus.choices,
        default=OrderStatus.PROCESSING
    )

    def __str__(self):
        return f"Order #{self.id} - {self.customer.cust_username}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    
    def get_total_items(self):
        return self.items.count() 

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.price_at_order

    def __str__(self):
        return f"{self.quantity} × {self.product.p_name}"

class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.cust_username}'s Cart"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} × {self.product.p_name}"

    def get_total_price(self):
        return self.quantity * self.product.p_price

class Favourite(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='favourites')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.cust_username}'s Favourites"

    def get_total_items(self):
        return self.items.count()  


class FavouriteItem(models.Model):
    favourite = models.ForeignKey(Favourite, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.p_name}"