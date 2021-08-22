from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Coupon, User
from .forms import CreateUser, ProductForm
from django.utils import timezone
from datetime import date


def register(request):
    form = CreateUser()
    if request.method == "POST":
        form = CreateUser(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, "user is created for " + username)
            return redirect("login")
    context = {
        "form": form,
    }
    return render(request, "register.html", context)


def login(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("mainpage")
        else:
            messages.info(request, "Username or Password is incorrect")
    return render(request, "login.html", context)

@login_required(login_url="login")
def dashboard(request):
    coupon = Coupon.objects.all()

    return render(
        request,
        "dashboard.html",
        {
            "coupon": coupon,
        },
    )


@login_required(login_url="login")
def mainpage(request):
    coupon_code = Coupon.objects.all()
    form = ProductForm()
    if request.method == "POST":
        user = request.user
        form = ProductForm(request.POST)
        if form.is_valid():
            coupon = form.cleaned_data.get("coupon")
            price = form.cleaned_data.get("price")
            to_apply_promocode = True
            if not coupon.end_date > timezone.now():
                to_apply_promocode = False
                msg = 'coupon is expired'
            elif (not coupon.limit > 0) or (not user.limit > 0):
                to_apply_promocode = False
                msg = 'you can not apply coupon code'
            else:
                pass

            if to_apply_promocode:
                if coupon.discount_type == 'Flat':
                    price = price - coupon.discount
                if coupon.discount_type == 'Percentage':
                    price = (price * coupon.discount) / 100

            today = date.today()

            if today == user.birthdate:
                price = price * 0.1

            if to_apply_promocode:
                product = form.save(commit=False)
                product.user = user
                product.price = price
                product.coupon = coupon
                coupon.limit = coupon.limit - 1
                coupon.save()
                limit = user.limit - 1
                User.objects.filter(id=user.id).update(limit=limit)
                product.save()
                messages.success(request, "sucess")
            if not to_apply_promocode:
                messages.error(request, msg)
            return redirect("mainpage")
    context = {
        "coupon_code": coupon_code,
        "form": form,
    }
    return render(request, "user.html", context)


def logout(request):
    logout(request)
    return redirect("login")
