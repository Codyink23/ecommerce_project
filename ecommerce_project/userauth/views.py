from django.shortcuts import render
from userauth.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.hashers import check_password



# Create your views here.

def signup(request):
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Hey {username}, Your account was successfully registered")
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("ecommerce_app:home")
            
    else:    
    
      form = UserRegisterForm()
    
    context = {
        'form': form,
    }
    return render(request, 'create-account.html', context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('ecommerce_app:home')
    
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'User logged in successfully')

            return redirect('ecommerce_app:home')
        else:
            messages.error(request, 'Email or password is Invalid')
    return render(request, 'login.html', )   

def logout_view(request):
    logout(request)
    messages.success(request, 'You logged out successfully')

    return redirect('ecommerce_app:home')     

def change_password(request):
    user = request.user
    
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_password')
        
        if confirm_new_password != new_password:
            messages.error(request, "The passwords didn't match")
            return redirect('userauth:change_password')
        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully")
            return redirect('userauth:change_password')
        else:
            messages.error(request, "Old password is incorrect")
            return redirect('userauth:change_password')
    
    return render(request, 'change_password.html')    