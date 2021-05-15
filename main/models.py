from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Модель пользователя

    :param balance: Баланс пользователя
    """

    status = models.CharField(max_length=255, default='')
    balance = models.FloatField(default=100000)
    avatar = models.ImageField(upload_to='avatars/', max_length=255, default='avatars/preset.jpg', null=True, blank=True)


class Stocks(models.Model):
    """
    Модель со всеми акциями

    :param index: Индекс акции
    :param name: Название акции
    :param description: Описание акции
    :param is_active: Поле, означающее, активна ли акция
    """

    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField()
    price = models.FloatField(default=0)


class Order(models.Model):
    """
    Модель со всеми ордерами (ордер - заявка на покупку или продажу акции)

    :param user: Ссылка на пользователя
    :param stock: Ссылка на акцию
    :param type: Тип ордера (false - покупка, true - продажа)
    :param price: Цена, по которой пользователь хочет купить или продать акцию
    :param amount: Количество акций, которое пользователь хочет купить или продать
    :param is_closed: Закрыт ли ордер
    :param date_closed: Дата закрытия ордера
    """

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    stock = models.ForeignKey(to=Stocks, on_delete=models.CASCADE)
    type = models.BooleanField()  # покупка - 0; продажа - 1
    price = models.FloatField()
    amount = models.IntegerField(default=1)
    is_closed = models.BooleanField(default=False)
    date_closed = models.DateTimeField(default=None, null=True)


class Portfolio(models.Model):
    """
    Портфолио пользователя

    :param user: Ссылка на пользователя
    :param stock: Ссылка на акцию
    :param count: Количество акций в портфеле
    :param percentage: Процент стоимости акции от стоимости всех акций
    :param short_balance: Баланс для торговли в шорт
    :param is_debt: Поле, означающее переход от торговли в шорт в торговлю в лонг
    """

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    stock = models.ForeignKey(to=Stocks, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    percentage = models.FloatField(default=0)
    short_balance = models.FloatField(default=-100000)
    is_debt = models.BooleanField(default=False)


class Quotes(models.Model):
    """
    Котировки акций

    :param stock: Ссылка на акцию
    :param price: Цена акции
    :param date: Дата и время создания котировки
    """

    stock = models.ForeignKey(to=Stocks, on_delete=models.CASCADE)
    price = models.FloatField()
    date = models.DateTimeField(default=timezone.now)


class LeverageData(models.Model):
    """
    Модель торговли с плечом

    :param stock: Ссылка на акцию
    :param user: Ссылка на пользователя
    :param ratio: Плечо
    """

    stock = models.ForeignKey(to=Stocks, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    ratio = models.IntegerField(default=1)


class Candles(models.Model):
    """
    Модель свечей

    :param open: Цена открытия
    :param close: Цена закрытия
    :param high: Максимальная цена
    :param low: Минимальная цена
    :param date: Дата
    :param stock: Ссылка на акцию
    :param type: Тип свечи (1 минута, 5 минут и т.д.)
    """

    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
    stock = models.ForeignKey(to=Stocks, on_delete=models.CASCADE)
    type = models.IntegerField(default=1)


class Statistics(models.Model):
    name = models.CharField(max_length=255, default='')
    open_orders = models.IntegerField(default=0)
    closed_orders = models.IntegerField(default=0)
    user_active = models.IntegerField(default=0)
    count_stocks = models.IntegerField(default=0)
    count_long = models.IntegerField(default=0)
    count_short = models.IntegerField(default=0)
    max_balance = models.IntegerField(default=0)
    the_richest = models.CharField(max_length=255, default='')


class Settings(models.Model):
    name = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    stock_id = models.IntegerField(default=0)
    data = models.JSONField()


class Cryptocurrencies(models.Model):
    name = models.CharField(max_length=255, default='')
    price = models.CharField(max_length=255, default='')
