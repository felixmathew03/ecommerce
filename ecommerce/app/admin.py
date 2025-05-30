from django.contrib import admin
from .models import Category, Product, Customer, Order, OrderItem, Cart, CartItem
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)