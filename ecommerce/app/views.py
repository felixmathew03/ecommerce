from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Category, Product, Customer, OrderItem, Order
from django.views.decorators.http import require_POST
import bcrypt
from django.contrib import messages

def getuser(request):
    user=False

    if 'user' in request.session:
            user=True
    return user

# Homepage view
def index(request):
    if not getuser(request):
        return redirect(customer_login)
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    categories=Category.objects.all()
    return render(request, 'index.html',{
        'products':products,
        'categories':categories
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

#user section

def signup(request):    
    if request.method=="POST":
        name=request.POST['name']
        phno=request.POST['phno']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        cnf_password=request.POST['cnf_password']

        psw=password.encode('utf-8')
        salt=bcrypt.gensalt()            
        psw_hashed=bcrypt.hashpw(psw,salt)

        if password==cnf_password:
            data=Customer.objects.create(cust_name=name,cust_phone=phno,cust_email=email,cust_username=username,cust_password=psw_hashed.decode('utf-8'))
            data.save()
            messages.success(request, "Account created successfully pls login to continue !")  
        else:
            messages.warning(request, "Password Doesn't match !") 
        return redirect(signup)
    else:
        return render(request,"signup.html",{'user':getuser(request)})

def customer_login(request):
        if request.method=="POST":
            username=request.POST['username']
            password=request.POST['password']
            psw=password.encode('utf-8')
            try:
                data=Customer.objects.get(cust_username=username)
                if bcrypt.checkpw(psw,data.cust_password.encode('utf-8')):
                    request.session['user']=username
                    messages.success(request, "Login successfully completed!")
                else:
                    messages.warning(request, "Incorrect password!")
            except:
                messages.warning(request, "Incorrect Username!") 
        
            return redirect(customer_login)
        else:
            return render(request,"login.html",{'user':getuser(request)})

def customer_logout(request):
    if getuser(request):
        del request.session['user']
        return redirect(customer_login)
    else:
        return redirect(customer_login)

def customer_profile(request):
    customer = get_object_or_404(Customer, cust_username=request.session['user'])
    orders = Order.objects.filter(customer__cust_username=request.session['user']).order_by('-created_at')
    return render(request, 'customer_profile.html', {'customer': customer,'orders':orders})

def buy_now(request, product_id):
    if not getuser(request):
        messages.error(request, "You must be logged in to buy a product.")
        return redirect('login')

    # Get the logged-in customer
    customer = get_object_or_404(Customer, cust_username=request.session['user'])

    # Get the product
    product = get_object_or_404(Product, pk=product_id)

    # Optional: check for available stock here if needed

    # Create the order
    order = Order.objects.create(customer=customer)

    # Create the order item with quantity = 1
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1,
        price_at_order=product.p_price
    )

    messages.success(request, f"Order #{order.id} placed for {product.p_name}!")
    return redirect("order_confirmation",order_id=order.id)  # or 'order_confirmation', etc.

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id, customer__cust_username=request.session['user'])
    return render(request, 'order_confirmation.html', {'order': order})

def orders_list(request):
    orders = Order.objects.filter(customer__cust_username=request.session['user']).order_by('-created_at')
    return render(request, 'orders_list.html', {'orders': orders})

def edit_customer(request):
    username = request.session.get('user')
    if not username:
        return redirect('login')  

    customer = get_object_or_404(Customer, cust_username=username)

    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        phno = request.POST.get('phno', '').strip()
        email = request.POST.get('email', '').strip()

        if not name or not phno or not email:
            error = "All fields are required."
            return render(request, "edit_customer.html", {'customer': customer, 'error': error})

        try:
            phno = int(phno)
        except ValueError:
            error = "Phone number must be numeric."
            return render(request, "edit_customer.html", {'customer': customer, 'error': error})

        customer.cust_name = name
        customer.cust_phone = phno
        customer.cust_email = email
        customer.save()
        return redirect('customer_profile')  

    else:
        return render(request, "edit_customer.html", {'customer': customer})







# Admin section
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

@login_required(login_url='admin_login')
def view_orders(request):
    orders=Order.objects.all()
    return render(request,'admin/view_orders.html', {'orders': orders})

@require_POST
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('admin_dashboard')  # or the relevant view name where you list products

@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    return redirect('admin_login')
