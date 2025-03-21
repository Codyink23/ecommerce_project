from django.contrib import messages
from django.shortcuts import redirect

def admin_required(required):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser != True:
            messages.warning(request, 'You are not authorized to access this page.')
            return redirect('ecommerce_app:home')
        return required(request, *args, **kwargs)
        
    return wrapper    