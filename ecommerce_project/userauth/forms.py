from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauth.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100, label='Username', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Username'
        }
    )) 
    email = forms.CharField(max_length=100, label='Email', widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Email'
        }
    ))
    password1 = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        }
    ))
    password2 = forms.CharField(max_length=100, label='Confirm Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        }
    ))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', ]

   