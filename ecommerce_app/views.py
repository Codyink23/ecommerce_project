from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib import messages
from django.conf import settings 
from .forms import *
import json
import requests
from django.db.models import Avg
from django.http import JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
import random
import math
import string



from django.shortcuts import redirect

# from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def index(request):
    s_product = Product.objects.all()[:16]
    latest_product = Product.objects.all().order_by("-created_at")[:8]
    context = {
        'product': s_product,
        'products': latest_product
    }
    return render(request, 'index.html', context)




def blog(request):
    blog = Blog.objects.all()[:3]
    featured_products = Product.objects.filter(is_available=True)[:3]

    
    context = {
        'is_featured':  featured_products,
        'blog': blog,
      
        
    }
    return render(request, 'blog.html', context)

def blog_single(request, pk):
    single_blog = get_object_or_404(Blog, id=pk)
    context = {
        'blog_single': single_blog
    }
    return render(request, 'blog-detail.html', context)

def contact(request):
    if request.method == 'POST':
       contact_us = ContactForm(request.POST)
       if contact_us.is_valid():
           contact_us.save(commit=False)
           subject = contact_us.cleaned_data['subject']
           email_subject = f'{subject}: FROM ECommerce Website'
           name = contact_us.cleaned_data['name']
           email = contact_us.cleaned_data['email']
           message = contact_us.cleaned_data['message']
           email_data = {
                'subject' : subject,
                'name' : name,
                'email' : email,
                'message' : message,
            }
           html_message = render_to_string('contact_us_template.html', email_data)
           plain_message = strip_tags(html_message)
           from_email = email 
           recepient_list = [settings.EMAIL_HOST_USER, ]
           try:
                email_message = EmailMessage(email_subject, plain_message, to=recepient_list, from_email=from_email)
                email_message.send()
                contact_us.save() 
                messages.success(request, 'Message sent successfully')
           except:
                messages.error(request, 'Failed to send message')
  

           
    else:
        contact_us = ContactForm()       

    context = {
        'contact': contact_us
    }   
    
    return render(request, 'contact.html', context)

def product(request):
    products = Product.objects.all()
    
    context = {
        'product': products
    }
    return render(request, 'shop.html', context)

def product_detail(request, pk):
      
      
    product_single = get_object_or_404(Product, id=pk)
    
    review = Review.objects.filter(product=product_single).order_by('-created_at')
    average_rating = Review.objects.filter(product=product_single).aggregate(rating=Avg('rating'))
    review_form = ReviewForm()
    
    make_review = True
    
    if request.user.is_authenticated:
        user_review_count = Review.objects.filter(user=request.user, product=product_single).count()
        
        if user_review_count > 0:
            make_review = False
    
    
    
    # Filter method for related products 
    products = Product.objects.filter(category=product_single.category).exclude(id=pk)
    
    # End of filter method for related products
    
    context = {
        'single': product_single,
        'review': review,
        'make_review': make_review,
        'average_rating': average_rating,
        'review_form': review_form,
        'products': products
    }
    return render(request, 'detail.html', context)

def add_review(request, id):
    products = Product.objects.get(id=id)
    user = request.user
    
    review = Review.objects.create(
        user=user,
        product = products,
        review = request.POST['review'],
        rating = request.POST['rating']
    )
    
    context = {
        'user': user.username,
        'review':  request.POST['review'],
        'rating': request.POST['rating'],
    }
    
    average_rating = Review.objects.filter(product=products).aggregate(rating=Avg('rating'))
    
    return JsonResponse(
        {
        'bool': True,
        'context': context,
        'average_rating': average_rating
        
        }
        
    )



def cart(request):
    cart_total_amount = 0
    # Debugging step: check if the cart data exists in session
    if 'cart_data_obj' in request.session:
        print(request.session['cart_data_obj'])  # Print the cart data
        for product_id, item in request.session['cart_data_obj'].items():
            price_str = item['price']
            
            # Clean the price
            cleaned_price = price_str.replace('\n', '').replace('\t', '').replace('₦', '').strip()
            
            # Handle empty price and conversion
            try:
                if cleaned_price:
                    cart_total_amount += int(item['quantity']) * float(cleaned_price)
                else:
                    cart_total_amount += int(item['quantity']) * 0.0  # Default to 0.0 if empty
            except ValueError:
                print(f"Invalid price format for product {product_id}. Skipping item.")
                cart_total_amount += int(item['quantity']) * 0.0  # Default to 0 if conversion fails
                
            print(cart_total_amount)    
            
            # Process the quantity and price
            quantity = int(item['quantity'])
            price = int(float(cleaned_price)) if cleaned_price else 0
            item['cleaned_price'] = price
            item['cleaned_quantity'] = quantity
            total_price = price * quantity
            item['total_price'] = total_price
            
            
            # Debugging prints
            print(total_price)
            print(type(item['cleaned_quantity']))
            print(type(price))
        
        return render(request, 'cart.html', {
            "cart_data": request.session['cart_data_obj'], 
            'totalcartItems': len(request.session['cart_data_obj']), 
            'cart_total_amount': cart_total_amount
        })
    else:
        print("No cart data in session.")  # Debugging output
        messages.warning(request, "Your cart is empty")
        return redirect('ecommerce_app:home')


def home_two(request):
    blog = Blog.objects.all()[:3]
    
    context = {
        'blog': blog
    }
    return render(request, 'home-02.html', context)

def home_three(request):
    m_product = Product.objects.all()[:16]
    context = {
        'product': m_product
    }
    return render(request, 'home-03.html', context)

# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
@csrf_protect
def add_to_cart(request):
    cart_product = {}
    # image = request.POST.get('image')  # Fetch the image data from the POST request
    # print("Image URL or Path:", image)
    cart_product[str(request.POST.get("id"))] = {
        'title' : request.POST['title'], 
        'quantity' : request.POST["quantity"], 
        'price' : request.POST["price"],
        'image' : request.POST["image"],
       
        
    }
    print(cart_product)
    if 'cart_data_obj' in request.session:
        if str(request.POST.get("id")) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.POST["id"])]['quantity'] = int(cart_product[str(request.POST["id"])]['quantity'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartItems': len(request.session['cart_data_obj'])  }) 


def search_view(request):
   query = request.GET.get("q", '')
       
   products = Product.objects.filter(name__icontains=query).order_by('-created_at') 
   
   context = {
       'products': products,
       'query': query,
    } 
   return render(request,'search.html', context)




# def delete_item_from_cart(request):
#     product_id = str(request.GET.get('id'))

#     if 'cart_data_obj' in request.session:
#         cart_data = request.session['cart_data_obj']
        
#         # print("Cart data before deletion:", cart_data)  # Debugging line

#         if product_id in cart_data:
#             del cart_data[product_id]
#             request.session['cart_data_obj'] = cart_data

#             # Recalculate the total cart amount and total number of items
#             cart_total_amount = 0
#             for item in cart_data.values():
#                 price_str = item['price'].replace('\n', '').replace('\t', '').replace('₦', '').strip()
#                 cleaned_price = float(price_str) if price_str else 0.0
#                 quantity = int(item['quantity'])
#                 item['cleaned_price'] = cleaned_price
#                 item['cleaned_quantity'] = quantity
#                 cart_total_amount += cleaned_price * quantity
#                 item['cleaned_price'] = cleaned_price
#                 item['cleaned_quantity'] = quantity
#                 total_price = cleaned_price * quantity
#                 item['total_price'] = total_price

#             # print("Cart data after deletion:", cart_data)  # Debugging line

#             context = {
#                 'data': cart_data,  # Ensure this is populated
#                 'totalcartItems': len(cart_data),
#                 'cart_total_amount': cart_total_amount
#             }
#             print("Cart data before rendering:", cart_data)  
#             # Return only the updated cart HTML (the part where the cart items are listed)
#             cart_html = render_to_string('cart-list.html', context)

#             return JsonResponse({
#                 'data': cart_html,  # Updated cart HTML
#                 'totalcartItems': len(cart_data),  # Updated total items count
#                 'cart_total_amount': cart_total_amount  # Updated total cart amount
#             })

#     return JsonResponse({'error': 'Product not found in cart'}, status=400)
          

def delete_item_from_cart(request):
    # Get the product ID from the GET request
    product_id = str(request.GET.get('id'))

    # Ensure the cart exists in the session
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        
        # Check if the product exists in the cart
        if product_id in cart_data:
            # Remove the product from the cart
            del cart_data[product_id]
            request.session['cart_data_obj'] = cart_data  # Save the updated cart back to the session

            # Recalculate the total cart amount and total number of items
            cart_total_amount = 0
            for item in cart_data.values():
                # Clean price and quantity
                price_str = item['price'].replace('\n', '').replace('\t', '').replace('₦', '').strip()
                cleaned_price = float(price_str) if price_str else 0.0
                quantity = int(item['quantity'])
                item['cleaned_price'] = cleaned_price
                item['cleaned_quantity'] = quantity

                # Recalculate total price for each item
                total_price = cleaned_price * quantity
                item['total_price'] = total_price

                # Add to the cart total amount
                cart_total_amount += total_price

            # Prepare the context for rendering the updated cart HTML
            context = {
                'cart_data': cart_data,  # Pass the updated cart data
                'totalcartItems': len(cart_data),  # Updated total items count
                'cart_total_amount': cart_total_amount  # Updated total cart amount
            }

            # Render the updated cart list HTML
            cart_html = render_to_string('cart-list.html', context)

            # Return updated cart HTML and total values
            return JsonResponse({
                'data': cart_html,  # Updated cart HTML
                'totalcartItems': len(cart_data),  # Updated total items count
                'cart_total_amount': cart_total_amount  # Updated total cart amount
            })

    # If the product is not found in the cart, return an error response
    return JsonResponse({'error': 'Product not found in cart'}, status=400)


EXCHANGE_RATE = 1600







# def update_from_cart(request):
#     # Get the product ID and quantity from the request
#     product_id = str(request.GET['id'])
#     product_qty = request.GET['quantity']
#     # Ensure the quantity is an integer
#     try:
#         product_qty = int(product_qty)
#     except ValueError:
#         return JsonResponse({"error": "Invalid quantity."})

#     # Check if the cart exists in the session
#     if 'cart_data_obj' in request.session:
#         cart_data = request.session['cart_data_obj']
        
#         # Check if the product is already in the cart
#         if product_id in cart_data:
#             # Update the product quantity
#             cart_data[product_id]['quantity'] = product_qty
#             request.session['cart_data_obj'] = cart_data  # Save the updated cart back to session

#             # Recalculate the total cart amount
#             cart_total_amount = 0
#             for item in cart_data.values():
#                 # Ensure the price is cleaned and converted to float
#                 price_str = item['price']  # Assuming price is stored as a string with currency symbols
#                 cleaned_price = price_str.replace('\n', '').replace('\t', '').replace('₦', '').strip()

#                 try:
#                     cleaned_price = float(cleaned_price)  
#                 except ValueError:
#                     return JsonResponse({"error": "Invalid price format."})

#                 quantity = item.get('quantity', 0)  

#                 if not isinstance(quantity, int):
#                     try:
#                         quantity = int(quantity)
#                     except ValueError:
#                         return JsonResponse({"error": "Invalid quantity format."})

#                 item_total_price = cleaned_price * quantity  

#                 # Store the cleaned total price
#                 item['total_price'] = item_total_price
#                 item['cleaned_price'] = cleaned_price  
#                 item['cleaned_quantity'] = quantity  

#                 cart_total_amount += item_total_price

#             print("Cart Data:", cart_data)

#             cart_data_html = render_to_string('cart-list.html', {
#                 "data": cart_data,
#                 'totalcartItems': len(cart_data),
#                 'cart_total_amount': cart_total_amount,
#             })
#             return JsonResponse({
#                 "data": cart_data_html,
#                 "totalcartItems": len(cart_data),
#                 "cart_total_amount": cart_total_amount,
#             })
            

#     return JsonResponse({"error": "Cart update failed."})


def update_from_cart(request):
    # Ensure the cart exists in the session
    if 'cart_data_obj' not in request.session:
        return JsonResponse({"error": "No cart found."})
    
    cart_data = request.session['cart_data_obj']
    
    # Get the product ID and quantity from the request
    product_id = request.GET.get('id')
    product_qty = request.GET.get('quantity')

    # Ensure the product ID and quantity exist
    if not product_id or not product_qty:
        return JsonResponse({"error": "Missing product ID or quantity."})

    # Ensure the quantity is an integer
    try:
        product_qty = int(product_qty)
    except ValueError:
        return JsonResponse({"error": "Invalid quantity."})

    # Check if the product is in the cart
    if product_id in cart_data:
        # Update the product quantity
        cart_data[product_id]['quantity'] = product_qty
        request.session['cart_data_obj'] = cart_data  # Save the updated cart back to session

        # Recalculate the total cart amount
        cart_total_amount = 0
        for item in cart_data.values():
            # Clean the price and ensure it's a float
            price_str = item['price']  # Assuming price is stored as a string with currency symbols
            cleaned_price = price_str.replace('\n', '').replace('\t', '').replace('₦', '').strip()

            try:
                cleaned_price = float(cleaned_price)  
            except ValueError:
                return JsonResponse({"error": "Invalid price format."})

            quantity = item.get('quantity', 0)  

            if not isinstance(quantity, int):
                try:
                    quantity = int(quantity)
                except ValueError:
                    return JsonResponse({"error": "Invalid quantity format."})

            item_total_price = cleaned_price * quantity  

            # Update the item's total price
            item['total_price'] = item_total_price
            item['cleaned_price'] = cleaned_price  
            item['cleaned_quantity'] = quantity  

            cart_total_amount += item_total_price

        # Render the updated cart HTML
        cart_data_html = render_to_string('cart-list.html', {
            'cart_data': cart_data,
            'totalcartItems': len(cart_data),
            'cart_total_amount': cart_total_amount,
        })
        
        return JsonResponse({
            "data": cart_data_html,
            "totalcartItems": len(cart_data),
            "cart_total_amount": cart_total_amount,
        })

    return JsonResponse({"error": "Product not found in cart."})



def save_checkout_info(request):
    cart_total_amount = 0
    total_amount = 0
    
    if request.method == "POST":
        full_name = request.POST['full-name']
        email = request.POST['email']
        mobile = request.POST['phone-no']
        address = request.POST['address']
        country = request.POST['country']
        city = request.POST['city']
        state = request.POST['state']
        
        request.session['full_name'] = full_name
        request.session['email'] = email
        request.session['mobile'] = mobile
        request.session['address'] = address
        request.session['country'] = country
        request.session['city'] = city
        request.session['state'] = state
        
        if 'cart_data_obj' in request.session:
            for product_id, item in request.session['cart_data_obj'].items():
               price_str = item['price']
            
            # Clean the price
               cleaned_price = price_str.replace('\n', '').replace('\t', '').replace('₦', '').strip()
               length = 8

               random_number = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            
          
               total_amount += int(item['quantity']) * float(cleaned_price)
            
            if request.user.is_authenticated:
                user = request.user
            else:
                user = None       
            
            order = Cartorder.objects.create(
                user = user,
                price = total_amount,
                full_name  = full_name,
                email = email,
                phone = mobile,
                address = address,
                city = city,
                state = state,
                country = country,
                
               ) 
            del request.session['full_name']
            del request.session['email']
            del request.session['mobile'] 
            del request.session['address']
            del request.session['country']
            del request.session['city']
            del request.session['state']    
             
            for product_id, item in request.session['cart_data_obj'].items(): 
              price_str = item['price']
        
              cleaned_price = price_str.replace('\n', '').replace('\t', '').replace('₦', '').strip()

              cart_total_amount += int(item['quantity']) * float(cleaned_price)

              cart_order_products = CartOrderProduct.objects.create(
                order=order,
                invoice_no = "INVOICE_NO" + str(random_number),
                item=item['title'],
                quantity = item['quantity'],
                image = item['image'],
                price = cleaned_price,
                total = float(item['quantity']) * float(cleaned_price)
                    
            )
            total_amount_dollars = cart_total_amount / 1900
            rounded_total = math.ceil(total_amount_dollars * 100) / 100
            print(f"Rounded total amount {rounded_total}")
   
            
            # Process the quantity and price
        
        return redirect('ecommerce_app:checkout', order.oid)    
    return redirect('ecommerce_app:checkout', order.oid)    
    
def checkout(request, oid):
    order = Cartorder.objects.get(oid=oid)
    order_items = CartOrderProduct.objects.filter(order=order)
    
    order_total_p = order.price * 100
    order_price_naira = order.price
    order_price_usd = order_price_naira / EXCHANGE_RATE  
    rounded_usd_price = math.ceil(order_price_usd * 100) / 100
    order.usd_price = rounded_usd_price
    order.save()  
    if request.method == 'POST':
        code = request.POST['code']
        coupon = Coupon.objects.filter(code=code, active=True).first()
        if coupon:
            if coupon in order.coupons.all():
                messages.warning(request, 'Coupon already activated or has been used previously')
                return redirect("ecommerce_app:checkout", order.oid)
            else:
               discount = order.price * coupon.discount / 100
               order.coupons.add(coupon)
               order.price -= discount
               order.saved += discount
               order.save()
               # Converter from naira to dolars for paypal
               order_price_naira = order.price
               order_price_usd = order_price_naira / EXCHANGE_RATE  
               rounded_usd_price = math.ceil(order_price_usd * 100) / 100
               order.usd_price = rounded_usd_price
               order.save()
                
               messages.success(request, 'Coupon activated ')
               return redirect("ecommerce_app:checkout", order.oid) 
        else:
               messages.error(request, 'Coupon does not exist !')
               return redirect("ecommerce_app:checkout", order.oid)      
    
    context = {
        'order': order,
        'order_items': order_items,
        'order_total': order_total_p,
    }
    return render(request, 'checkout.html', context)    


# @login_required(login_url='/login' )      
def paypal_completed_view(request, oid):
    order = Cartorder.objects.get(oid=oid)
    if order.paid_status == False:
        order.paid_status = True
        order.save()
    context = {
        'order': order,
    }    
    


          
    return render(request, 'payment_complete.html', context)


@login_required(login_url='/login' )  
def paypal_failed_view(request):
    return render(request, 'payment_failed.html')   


@login_required(login_url='/login' )  
def customer_dashboard(request):
    orders = Cartorder.objects.filter(user=request.user).order_by('-order_date')
    address = Address.objects.filter(user=request.user)
    
    context = {
        'orders': orders
    }
    return render(request, 'dashboard/index.html', context) 



def order_detail(request, pk):
    order = Cartorder.objects.get(user=request.user, id=pk)
    products = CartOrderProduct.objects.filter(order=order)
    
    context = {
        'products': products
    }
    return render(request, 'dashboard/order-detail.html', context)

def address(request):
    address = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        new_address = Address.objects.create(
            user=request.user,
            address=address,
            phone_no = phone,
        )
        messages.success(request, 'Address added successfully')
        return redirect('ecommerce_app:seller_dashboard')
    context = {
        'address': address
    }

    return render(request, 'dashboard/shipping-address.html', context)

@login_required(login_url='/login' )  
def wishlist(request):
    wishlist  = Wishlist.objects.all()
    context = {
        'wishlist': wishlist
    }
    return render(request, 'wishlist.html', context)

def add_to_wishlist(request):
    id = request.GET['id']
    product = Product.objects.get(id=id)
    context = {}
    
    wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
    print(f"Wishlist count: {wishlist_count}")
    
    if wishlist_count > 0:
        context = {
            'bool': True,
        }
    else:
        new_wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )  
        context = {
        'bool': True,
         }      
    return JsonResponse(context)

def delete_wishlist(request):
    id = request.GET['id']
    wishlist = Wishlist.objects.filter(user=request.user)
    product = Wishlist.objects.get(id=id)
    product.delete()
    
    context = {
        'bool': True,
        'wishlist': wishlist,
    }
    # wishlist_json = serializers.serialize('json', wishlist)
    # data = render_to_string('wishlist.html', context)
    data = render_to_string('wishlist_part.html', context)

    return JsonResponse({
                'data': data,
                'success': True,
                'message': 'Product successfully deleted from wishlist!'
            })



# def delete_wishlist(request):
#     if request.method == 'POST':
#         try:
#             wishlist_id = request.POST.get('id')
#             # Ensure the product belongs to the current user
#             product = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
#             product.delete()

#             # Get the updated wishlist for the user
#             wishlist = Wishlist.objects.filter(user=request.user)

#             # Render only the updated wishlist HTML section
#             context = {
#                 'wishlist': wishlist,
#             }
#             data = render_to_string('wishlist_part.html', context)  # Use a specific template for the wishlist part

#             return JsonResponse({
#                 'data': data,
#                 'success': True,
#                 'message': 'Product successfully deleted from wishlist!'
#             })
#         except Wishlist.DoesNotExist:
#             return JsonResponse({
#                 'success': False,
#                 'message': 'Product not found in wishlist.'
#             })
#     else:
#         return JsonResponse({
#             'success': False,
#             'message': 'Invalid request method. Use POST.'
#         })

def chart(request):
    return render(request, 'dashboard/chart.html')

