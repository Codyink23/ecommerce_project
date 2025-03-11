from django.db import models
from userauth.models import User

from django.utils import timezone
from django.conf import settings
from django.utils.safestring import mark_safe 
import shortuuid
from shortuuidfield import ShortUUIDField
from shortuuid.django_fields import ShortUUIDField
import datetime


# Create your models here.
STATUS_CHOICES = (
    ("process", "processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
    
    
)
STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
    
    
)
RATING = (
    (1, "⭐☆☆☆☆"),
    (2, "⭐⭐☆☆☆"),
    (3, "⭐⭐⭐☆☆"),
    (4, "⭐⭐⭐⭐☆"),
    (5, "⭐⭐⭐⭐⭐"),
    
    
)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='uploads/')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.title 

class Product(models.Model):
    SIZE_S = 'Size S'
    SIZE_M = 'Size M'
    SIZE_L = 'Size L'
    SIZE_XL = 'Size XL'
    CHOICES = [
        ('SIZE_S', 'Size S'),
        ('SIZE_M', 'Size M'),
        ('SIZE_L', 'Size L'),
        ('SIZE_XL', 'Size XL'),
    ]
    
    RED = 'Red'
    BLUE = 'Blue'
    WHITE = 'White'
    GREY = 'Grey'
    GREEN = 'Green'
    BLACK = 'Black'
    C_CHOICES = [
        ('RED', 'Red'),
        ('GREEN', 'Green'),
        ('BLACK', 'Black'),
        ('BLUE', 'Blue'),
        ('WHITE', 'White'),
        ('GREY', 'Grey'),
    ]
    
    
    
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='uploads/')
    image_two = models.ImageField(upload_to='uploads/', default='files/images/banner-01.jpg')
    image_three = models.ImageField(upload_to='uploads/', default='files/images/banner-01.jpg')
    is_featured = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)


    
    description = models.TextField()
    size = models.CharField(max_length=50, choices=CHOICES, blank=True)
    color = models.CharField(max_length=50, choices=C_CHOICES, blank=True)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField( default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)  
    
    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=225, default='name')
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    
    
    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    
    class Meta:
        verbose_name_plural = 'Review'  
    
        
class Seller(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.TextField()
    address = models.CharField(max_length=100, default='123 CU Avenue')
    contact = models.CharField(max_length=100, default='12345678910')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name





class Cartorder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)  
    email = models.CharField(max_length=200, blank=True, null=True)  
    phone = models.CharField(max_length=200, blank=True, null=True) 
    
    address = models.CharField(max_length=200, blank=True, null=True) 
    city = models.CharField(max_length=200, blank=True, null=True) 
    state = models.CharField(max_length=200, blank=True, null=True) 
    country = models.CharField(max_length=200, blank=True, null=True) 
    

    
    price = models.DecimalField(max_digits=14, decimal_places=2)
    usd_price = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    saved = models.DecimalField(max_digits=14, decimal_places=2, default="0.00")
    coupons = models.ManyToManyField("ecommerce_app.Coupon", blank=True)
    
    shipping_method = models.CharField(max_length=200, blank=True, null=True) 
    tracking_id = models.CharField(max_length=200, blank=True, null=True) 
    tracking_website_address = models.CharField(max_length=200, blank=True, null=True) 

    
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(default=datetime.datetime.now())
    product_status = models.CharField(choices=STATUS_CHOICES, max_length=30, default='processing', null=True, blank=True)  
    sku = ShortUUIDField(null=True, blank=True, length=5, prefix="SKU", max_length=50, alphabet="1234567890") 
    oid = ShortUUIDField(null=True, blank=True, length=5, max_length=50, alphabet="1234567890")
    
    stripe_payment_intent = models.CharField(max_length=1000, blank=True, null=True) 
    
    

    
    class Meta:
        verbose_name_plural = 'Cart Order'  
    
    
class CartorderItem(models.Model):
    order = models.ForeignKey(Cartorder, on_delete=models.CASCADE)
    product_status = models.CharField(max_length=100)
    item = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    
    class Meta:
        verbose_name_plural = 'Cart Order Item'  
    
    def order_img(self):
        return  mark_safe('<img src="media/%s" width="50" height="50" />' % (self.image))
    
class CartOrderProduct(models.Model):
    order = models.ForeignKey(Cartorder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200, default="Cart Item")
    image = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    
    class Meta:
        verbose_name_plural = "Cart Order Product" 
        
    
class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Wishlist'
     

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    phone_no = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=300, null=True)
    status = models.BooleanField(default=False)


class Coupon(models.Model):
    code = models.CharField(max_length=50)  
    discount = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.code      
 


    
      
