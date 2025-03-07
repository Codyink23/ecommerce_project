from django.contrib import messages
from .models import *
from django.shortcuts import render
import requests



def ecommerce_app(request):
    try:
        wishlist = Wishlist.objects.filter(user=request.user)
    except:
        messages.warning(request, "You are not allowed to view the Wishlist page without logging in.")
        wishlist = 0    
        
    return {
        'site_name': 'My Awesome Site',
        'wishlist': wishlist
    }