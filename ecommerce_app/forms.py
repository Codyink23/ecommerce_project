from django import forms
from .models import *

class ContactForm(forms.ModelForm):
       class Meta:
           model = Contact     
           fields = '__all__'
           exclude = ['created_at', 'updated_at', ]

           widgets = {
               'name': forms.TextInput(attrs={
                   'class' : 'form-control',
                   'placeholder': 'Enter your full name',
               }),
               'email': forms.EmailInput(attrs={
                   'class' : 'form-control',
                   'placeholder': 'Enter your email address',
                   
                   }),
               'subject': forms.TextInput(attrs={
                   'class' : 'form-control',
                   'placeholder': 'Enter your subject',
    
               }),
               'message': forms.Textarea(attrs={
                   'class' : 'form-control',
                   'placeholder': 'Enter your message',
               })
           } 
           
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review', 'rating', ]
        widgets = {
           'review': forms.Textarea(attrs={
                   'class' : 'form-control',
                   'placeholder': 'Enter your Review',
               }) 
        }
          
             