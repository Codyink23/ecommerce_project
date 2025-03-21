from django.shortcuts import render, redirect
from ecommerce_app.models import *
from django.db.models import Sum
from userauth.models import User
from selleradmin.forms import AddProductForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from selleradmin.decorators import admin_required

import datetime


# Create your views here.

@admin_required
def dashboard(request):
    revenue = Cartorder.objects.aggregate(price=Sum("price"))
    total_orders_count = Cartorder.objects.all()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    new_customers = User.objects.all().order_by("-id")
    latest_orders = Cartorder.objects.all().order_by("-id")
    
    this_month = datetime.datetime.now().month
    
    monthly_revenue = Cartorder.objects.filter(order_date__month=this_month).aggregate(price=Sum("price"))
    print(monthly_revenue)
    
    context = {
        'revenue': revenue,
        'total_orders_count': total_orders_count,
        'all_products': all_products,
        'all_categories': all_categories,
        'new_customers': new_customers,
        'latest_order': latest_orders,
        'monthly_revenue': monthly_revenue,
    }
    return render(request, 'admin/seller-dashboard.html', context)

@admin_required
def product(request):
    all_products = Product.objects.all().order_by("-id")
    all_categories = Category.objects.all()
    
    context = {
        'all_products': all_products,
        'all_categories': all_categories,

    }
    return render(request, 'admin/order-product.html', context)

@admin_required
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES) 
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            return redirect("selleradmin:products")
    else:
        form = AddProductForm()
    context = {
        'form': form
    }    
    return render(request, 'admin/add-product.html', context)    
 
 
 
@admin_required      
def edit_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=product) 
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            return redirect("selleradmin:edit-product", product.id)
    else:
        form = AddProductForm(instance=product)
    context = {
        'form': form,
        'product': product,
    }    
    return render(request, 'admin/edit-product.html', context)    


@admin_required
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect("selleradmin:products")


@admin_required
def orders(request):
    order = Cartorder.objects.all()
    context = {
        'order': order,
    }
    return render(request, 'admin/customer-order.html', context)



@admin_required
def orders_detail(request, id):
    # order = Cartorder.objects.get(id=id)
    order = Cartorder.objects.filter(id=id).first()  # .first() returns None if not found

    order_items = CartOrderProduct.objects.filter(order=order)
    context = {
        'order': order,
        'order_items': order_items, 
    }
    return render(request, 'admin/order-detail.html', context)        

@csrf_exempt
def change_order_status(request, id):
    order = Cartorder.objects.get(id=id)
    if request.method == 'POST':
        status = request.POST.get('status')
        order.product_status = status
        order.save()
        messages.success(request, f"Order status changed to {status}")
    
    return redirect("selleradmin:order-detail", order.id)
@admin_required
def shop_page(request):
    products = Product.objects.all()
    revenue = Cartorder.objects.aggregate(price=Sum("price"))
    total_sales = CartOrderProduct.objects.filter(order__paid_status=True).aggregate(quantity=Sum("quantity"))
    
    context = {
        'products': products,
        'revenue': revenue,
        'total_sales': total_sales
    }
    return render(request, 'admin/shop.html', context)

@admin_required
def reviews(request):
    review = Review.objects.all()
    context = {
        'review': review
    }
    return render(request, 'admin/review.html', context)
