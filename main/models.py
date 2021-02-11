from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    status = models.CharField(max_length=255)


class UserSettings(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    avatar = models.FileField(null=True, blank=True)


class OffersType(models.Model):
    name = models.CharField(max_length=255)


class TypeActives(models.Model):
    name = models.CharField(max_length=255)


class Actives(models.Model):
    name = models.CharField(max_length=255)
    avg_price = models.FloatField()
    description = models.CharField(max_length=255)
    is_active = models.BooleanField()
    type = models.ForeignKey(to=TypeActives, on_delete=models.CASCADE)


class Offers(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    active = models.ForeignKey(to=Actives, on_delete=models.CASCADE)
    type = models.ForeignKey(to=OffersType, on_delete=models.CASCADE)
    price = models.FloatField()
    is_closed = models.BooleanField()


class Portfolio(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    active = models.ForeignKey(to=Actives, on_delete=models.CASCADE)
    count = models.IntegerField()
