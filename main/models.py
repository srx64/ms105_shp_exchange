from django.db.models.signals import post_save

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    status = models.CharField(max_length=255)
    balance = models.IntegerField(null=True, default=100000)


class UserSettings(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    avatar = models.ImageField()

    def create_avatar(sender, instance, created, **kwargs):
        if created:
            user_setting = UserSettings(user_id=instance, avatar=None)
            user_setting.save()
    post_save.connect(create_avatar, sender=User)


class Stocks(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_active = models.BooleanField()


class Offers(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    stock = models.ForeignKey(to=Stocks, on_delete=models.CASCADE)
    type = models.BooleanField()  # покупка - 0; продажа - 1
    price = models.FloatField()
    is_closed = models.BooleanField()


class Portfolio(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    stock = models.ForeignKey(to=Stocks, on_delete=models.CASCADE)
    count = models.IntegerField()
