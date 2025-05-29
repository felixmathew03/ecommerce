from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adminn/login/', views.admin_login, name='admin_login'),
    path('adminn/dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('adminn/logout/', views.admin_logout, name='admin_logout'),
    path('adminn/addcategory/', views.add_category, name='add_category'),
    path('adminn/add-product/', views.add_product, name='add_product'),
    path('adminn/add-product/', views.add_product, name='add_product'),
    path('adminn/orders/', views.view_orders, name='view_orders'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('signup/', views.signup,name='signup'),
    path('login/', views.customer_login,name='login'),
    path('logout/', views.customer_logout,name='logout'),
    path('profile/', views.customer_profile, name='customer_profile'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders-lists/', views.orders_list, name='orders_list'),
    path('edit-customer/', views.edit_customer, name='edit_customer'),
]