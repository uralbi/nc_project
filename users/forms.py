import re
from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, label='Username', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100, label='Username', widget=forms.TextInput(
        attrs={'class': 'reg-form'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'reg-form'}))
    password1 = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput(
        attrs={'class': 'reg-form'}))
    password2 = forms.CharField(max_length=100, label='Confirm password', widget=forms.PasswordInput(
        attrs={'class': 'reg-form'}))
    # captcha = CaptchaField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProductForm(forms.ModelForm):
    class Meta:
       model = Products
       fields = ['city', 'product', 'price', 'main_category',
                 'sub_category', 'description', 'photo1', 'photo2', 'photo3', 'photo4' ]

    def clean_title(self):
        product = self.cleaned_data['product']
        if re.match(r'\d', product):
            raise ValidationError('Cannot start with numbers')
        return product