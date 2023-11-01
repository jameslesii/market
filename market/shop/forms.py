from django import forms
from django.contrib.auth.models import User
from .models import * 
from . models import Product

class LoginForm(forms.Form): 
    username = forms.CharField() 
    password=forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput) 
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput) 
    class Meta:
        model = User 
        fields = ('username', 'first_name','last_name', 'email') 
        def clean_password2(self): 
            cd = self.cleaned_data 
            if cd['password'] != cd['password2']: 
                raise forms.ValidationError('Passwords don\'t match.') 
                return cd['password2']
            
class SellItemForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['ProductCategory','ProductName','ProductImage','ProductPrice','ProductDescription','ProductQuantity','ProductLocation','ProductStatus']
        
class PostJobForm(forms.ModelForm):
    class Meta:
        model = job
        fields = ['job','JobLocation','jobDescription']

class msgForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = []
        