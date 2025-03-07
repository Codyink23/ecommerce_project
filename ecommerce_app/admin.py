from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Cartorder)
class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status', 'product_status']
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']

@admin.register(CartOrderProduct)    
class CartOrderProductAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'quantity', 'price', 'total',]

@admin.register(Address)    
class AddressAdmin(admin.ModelAdmin):
    list_display= ['user', 'address', 'phone_no', 'status',]    

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', ]

@admin.register(Category)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Contact)    
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject',]  

@admin.register(Review) 
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating']     
admin.site.register(Blog)
admin.site.register(Product)
admin.site.register(CartorderItem)
admin.site.register(Seller)
admin.site.register(Coupon)
    


