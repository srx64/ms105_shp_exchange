from django.db.models.signals import post_save

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    status = models.CharField(max_length=255, default='')
    balance = models.FloatField(default=100000)


class UserSettings(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/')

    def create_avatar(sender, instance, created, **kwargs):
        if created:
            user_setting = UserSettings(user_id=instance, avatar='avatars/preset.jpg')
            user_setting.save()
    post_save.connect(create_avatar, sender=User)


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
