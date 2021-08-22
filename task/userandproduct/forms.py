from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Coupon, User
from django import forms
class CouponForm(ModelForm):
    class Meta:
        model = Coupon
        fields = "__all__"

class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('user',)

class CreateUser(UserCreationForm):
    GENDER = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    limit = forms.IntegerField(widget=forms.HiddenInput(), initial=5)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'birthdate', 'gender']
