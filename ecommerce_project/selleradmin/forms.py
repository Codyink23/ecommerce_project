from ecommerce_app.models import Product
from django import forms

class AddProductForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Product Name', 'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter Product Description', 'class': 'form-control'}))
    price = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Enter Product Price', 'class': 'form-control'}))
    quantity = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Enter Product Quantity', 'class': 'form-control'}))
    image= forms.ImageField(widget=forms.FileInput(attrs={'placeholder': 'Enter Product Image', 'class': 'form-control'}))
    image_two= forms.ImageField(widget=forms.FileInput(attrs={'placeholder': 'Enter Product Image', 'class': 'form-control'}))
    image_three= forms.ImageField(widget=forms.FileInput(attrs={'placeholder': 'Enter Product Image', 'class': 'form-control'}))
    
    class Meta:
        model = Product
        fields = [
            'name',
            'image',
            'image_two',
            'image_three',
            'description',
            'price',
            'quantity',
            'category',
        ]