from django.db.models.signals import post_save

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    status = models.CharField(max_length=255, default='')
    balance = models.FloatField(default=100000)
    short_balance = models.FloatField(default=-100000)
    is_debt = models.BooleanField(default=False)


class UserSettings(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', max_length=255, null=True, blank=True)


class Stocks(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_active = models.BooleanField()


class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    stock = models.ForeignKey(to=Stocks, on_delete=models.CASCADE)
    type = models.BooleanField()  # покупка - 0; продажа - 1
    price = models.FloatField()
    amount = models.IntegerField(default=1)
    is_closed = models.BooleanField(default=False)
    date_closed = models.DateTimeField(default=None, null=True)


class Portfolio(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    stock = models.ForeignKey(to=Stocks, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    percentage = models.FloatField(default=0)


class Quotes(models.Model):
    stock = models.ForeignKey(to=Stocks, on_delete=models.CASCADE)
    price = models.FloatField()
    date = models.DateTimeField(default=timezone.now)


class LeverageData(models.Model):
    stock = models.ForeignKey(to=Stocks, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    ratio = models.IntegerField(default=1)
