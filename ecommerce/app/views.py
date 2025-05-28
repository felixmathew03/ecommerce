from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Category, Product
from django.views.decorators.http import require_POST

# Homepage view
def index(request):
    
    return render(request, 'index.html')

# Admin 
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin/login.html', {'error': 'Invalid credentials or not an admin user.'})
    return render(request, 'admin/login.html')

@login_required(login_url='admin_login')
def admin_dashboard(request):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    categories=Category.objects.all()
    return render(request, 'admin/dashboard.html',{'categories':categories,'products':products})

@login_required(login_url='admin_login')
def add_category(request):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)
    error = None
    success = None
    if request.method == "POST":
        category_name = request.POST.get("category", "").strip()
        if category_name == "":
            error = "Category name cannot be empty."
        else:
            if Category.objects.filter(c_name__iexact=category_name).exists():
                error = "Category already exists."
            else:
                Category.objects.create(c_name=category_name)
                success = f"Category '{category_name}' added successfully."

    return render(request, 'admin/add_category.html', {'error': error, 'success': success})

@login_required(login_url='admin_login')
def add_product(request):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)

    categories = Category.objects.all()
    success = None
    error = None

    if request.method == "POST":
        name = request.POST.get("p_name", "").strip()
        desc = request.POST.get("p_description", "").strip()
        price = request.POST.get("p_price")
        stock = request.POST.get("p_stock")
        category_id = request.POST.get("category")
        image = request.FILES.get("p_image")

        if not all([name, desc, price, category_id]):
            error = "Please fill all required fields."
        else:
            try:
                category = Category.objects.get(id=category_id)
                product = Product.objects.create(
                    p_name=name,
                    p_description=desc,
                    p_price=price,
                    p_stock=stock or 0,
                    category=category,
                    p_image=image
                )
                success = f"Product '{product.p_name}' added successfully."
            except Category.DoesNotExist:
                error = "Invalid category selected."

    return render(request, 'admin/add_product.html', {
        'categories': categories,
        'success': success,
        'error': error
    })

@require_POST
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('admin_dashboard')  # or the relevant view name where you list products

@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    return redirect('admin_login')
