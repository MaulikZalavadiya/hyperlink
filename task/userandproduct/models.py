from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    GENDER = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    name = models.TextField(max_length=500, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER)
    limit = models.IntegerField(default=2)


class Product(models.Model):
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(100), MaxValueValidator(1500000)])
    coupon = models.ForeignKey('Coupon', related_name='rel_coupon_product', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    discount_type = (
        ("Flat", "Flat"),
        ("Percentage", "Percentage"),
    )
    coupon_code = models.CharField(max_length=50, unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1500000)])
    discount_type = models.CharField(max_length=50, choices=discount_type, default='Flat')
    limit = models.IntegerField(default=1)

    def __str__(self):
        return self.coupon_code
