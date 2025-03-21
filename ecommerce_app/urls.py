from django.urls import path, include
from ecommerce_app import views

app_name = 'ecommerce_app'

urlpatterns = [
    path('', views.index, name='home' ),
    path('blog-single/<int:pk>/', views.blog_single, name='blog-single' ),
    path('blog/', views.blog, name='blog' ),
    path('contact/', views.contact, name='contact' ),
    path('product-detail/<int:pk>/', views.product_detail, name='product-detail' ),
    path('add-review/<int:id>/', views.add_review, name='add-review'),
    path('product/', views.product, name='product' ),
    path('cart/', views.cart, name='cart' ),
    path('home-two/', views.home_two, name='home-two' ),
    path('home-three/', views.home_three, name='home-three' ),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('search/', views.search_view, name='search'),
    path('delete-from-cart/', views.delete_item_from_cart, name='delete-from-cart'),
    path('update-cart/', views.update_from_cart, name='update_cart'),
    path('checkout/<oid>', views.checkout, name='checkout'),
    path('shipping-address/', views.address, name='shipping-address'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('save_checkout_info/', views.save_checkout_info, name='save_checkout_info'),
    # Add to Wishlist
    path('add-to-wishlist/', views.add_to_wishlist, name='add-to-wishlist'),
    
    # Add to Wishlist
    path('delete-from-wishlist/', views.delete_wishlist, name='delete-from-wishlist'),


    
    #Paypal Url
    path('paypal/', include('paypal.standard.ipn.urls')),
    
     path('payment-completed/<oid>/', views.paypal_completed_view, name='payment-completed'),
     path('payment-failed/', views.paypal_failed_view, name='payment-failed'),


#Customer Dashboard URls

path('dashboard/', views.customer_dashboard, name='seller_dashboard'),     
path('order-detail/<int:pk>/', views.order_detail, name='order-detail'),     
path('shipping-address/', views.address, name='shipping-address'),
path('chart/', views.chart, name='chart'),
    
    
    

    

]

