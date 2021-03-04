from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    status = models.CharField(max_length=255, default='')
    balance = models.FloatField(default=100000)


class UserSettings(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    avatar = models.ImageField()


class Stocks(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_active = models.BooleanField()


class Offers(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    stock = models.ForeignKey(to=Stocks, on_delete=models.CASCADE)
    type = models.BooleanField()  # покупка - 0; продажа - 1
    price = models.FloatField()
    is_closed = models.BooleanField(default=False)


class Portfolio(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    stock = models.ForeignKey(to=Stocks, on_delete=models.CASCADE)
    count = models.IntegerField()
