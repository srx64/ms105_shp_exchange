from __future__ import annotations
import logging
import os
from typing import Tuple

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q, Max, QuerySet
from django.db.models.base import ModelBase
from django.utils import timezone

from exchange_engine.settings import DEFAULT_SHORT_BALANCE_VALUE


class User(AbstractUser):
    """
    Модель пользователя

    :param balance: Баланс пользователя
    """
    status = models.CharField(max_length=255, default='')
    balance = models.FloatField(default=100000)
    avatar = models.ImageField(
        upload_to='avatars',
        max_length=255,
        default=os.path.join('avatars', 'preset.jpg'),
        null=True,
        blank=True
    )

    @staticmethod
    def get_admin_Q() -> Q:
        """
        Критерии поиска админа

        Используется для всех внешних моделей, у которых поле пользователя называется `user`.
        """
        return Q(user=User.get_admin_user())

    @staticmethod
    def get_admin_local_Q() -> Q:
        """
        Критерии поиска админа по юзернейму.

        Используется только внутри класса :class:`User`.
        Для остальных случаев есть :meth:`get_admin_Q`
        """
        return Q(username='admin')

    @staticmethod
    def get_admin_user() -> User:
        """
        Получение объекта администратора

        :raises User.DoesNotExist: в случае, если админ не найден.
        """
        try:
            return User.objects.get(username='admin')
        except User.DoesNotExist as ex:
            logging.error('Не найден объект администратора биржи')
            raise ex

    @staticmethod
    def get_non_admin_users() -> QuerySet:
        """
        Получение количества пользователей биржи

        Админ за пользователя не считается =)
        """
        return User.objects.filter(~User.get_admin_local_Q())

    @staticmethod
    def get_active_users_count() -> int:
        """
        Получение количества активных пользователей биржи
        """
        return User.objects.filter(is_active=True).count()

    @staticmethod
    def get_richest_user() -> User:
        """
        Поиск юзера с самым большим балансом
        """
        max_balance = User.objects\
            .filter(~User.get_admin_local_Q())\
            .aggregate(Max('balance'))\
            ['balance__max']
        return User.objects.filter(balance=max_balance).first()


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

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_active_stocks_count() -> int:
        """
        Получение количества торгующихся на бирже инструментов

        Используется в статистике биржи
        """
        return Stocks.objects.filter(is_active=True).count()


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
    count = models.IntegerField(default=1, null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    date_closed = models.DateTimeField(default=None, null=True)

    def __str__(self) -> str:
        return f"{self.user} -> {self.stock} ({'BUY' if self.type else 'SELL'}). Price: {self.price:.2f}, execution: {self.count} / {self.amount}"

    @staticmethod
    def get_non_admin_orders() -> QuerySet:
        return Order.objects.filter(~get_user_model().get_admin_Q())

    @staticmethod
    def get_opened_orders_count() -> int:
        """
        Получение количества открытых ордеров

        Используется в статистике биржи
        """
        return Order.get_non_admin_orders().filter(is_closed=False).count()

    @staticmethod
    def get_closed_orders_count() -> int:
        """
        Получение количества закрытых ордеров

        Используется в статистике биржи
        """
        return Order.get_non_admin_orders().filter(is_closed=True).count()


class Portfolio(models.Model):
    """
    Запись об финансовом инструменте, находящемся в портфеле пользователя

    :param user: Ссылка на пользователя
    :param stock: Ссылка на акцию
    :param count: Количество акций в портфеле
    :param aver_price: Средняя цена покупки
    :param percentage: Процент стоимости акции от стоимости всех акций
    :param short_balance: Баланс для торговли в шорт
    :param is_debt: Поле, означающее переход от торговли в шорт в торговлю в лонг
    """

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    stock = models.ForeignKey(to=Stocks, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    aver_price = models.FloatField(default=0)
    percentage = models.FloatField(default=0)
    short_balance = models.FloatField(default=DEFAULT_SHORT_BALANCE_VALUE)
    is_debt = models.BooleanField(default=False)

    @staticmethod
    def get_user_portfolio(user: get_user_model()) -> QuerySet:
        """Получение портфеля пользователя"""
        return Portfolio.objects.filter(user=user)

    @staticmethod
    def is_long_only(portfolio: QuerySet) -> bool:
        """Определяем, есть ли в этом портфеле инструменты, торгуемые в шорт"""
        return portfolio.filter(short_balance__lte=DEFAULT_SHORT_BALANCE_VALUE).count() == 0

    @staticmethod
    def get_bull_bear_count() -> Tuple[int, int]:
        """
        Количество "быков" (пользователей, торгующих в лонг) и медведей (пользователей, торгующих в шорт)

        Возвращается количество портфелей (то есть идёт агрегация по пользователям)


        .. todo::
           Переписать на агрегации через ORM, чтобы работало быстрее

        """
        bull_count = bear_count = 0
        for user in get_user_model().get_non_admin_users():
            portfolio = Portfolio.get_user_portfolio(user)
            if Portfolio.is_long_only(portfolio):
                bull_count += 1
            else:
                bear_count += 1
        return bull_count, bear_count


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
    line = models.IntegerField(default=-1)


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
    """
    Общая статистика биржи

    :param name: имя поля статистики
    :param open_orders: количество открытых ордеров
    :param closed_orders: количество закрытых ордеров
    :param user_active: количество активных пользователей биржи
    :param count_stocks: количество торгуемых акций
    :param count_long: количество пользователей, торгующих только в лонг
    :param count_short: количество пользователей, торгующих как в лонг, так и в шорт
    :param max_balance: баланс самого богатого пользователя биржи
    :param the_richest: имя самого богатого пользователя биржи
    """
    open_orders = models.IntegerField(default=0)
    closed_orders = models.IntegerField(default=0)
    user_active = models.IntegerField(default=0)
    count_stocks = models.IntegerField(default=0)
    count_long = models.IntegerField(default=0)
    count_short = models.IntegerField(default=0)
    max_balance = models.IntegerField(default=0)
    the_richest = models.CharField(max_length=255, default='')

    @staticmethod
    def update_statistics() -> None:
        """
        Обновление статистики биржи

        Пересчитываются все параметры без исключения.
        """
        stat = Statistics.objects.get_or_create()[0]
        stat.open_orders = Order.get_opened_orders_count()
        stat.closed_orders = Order.get_closed_orders_count()
        stat.user_active = get_user_model().get_active_users_count()
        stat.count_stocks = Stocks.get_active_stocks_count()
        richest_user: User = get_user_model().get_richest_user()
        stat.count_long, stat.count_short = Portfolio.get_bull_bear_count()
        stat.max_balance = richest_user.balance
        stat.the_richest = richest_user.username
        stat.save()

    @staticmethod
    def get_all_stats():
        return Statistics.objects.all()


class Settings(models.Model):
    name = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    stock_id = models.IntegerField(default=0)
    data = models.JSONField()

    def __str__(self):
        return f'{self.description}: {self.data}'


class Cryptocurrencies(models.Model):
    name = models.CharField(max_length=255, default='')
    price = models.CharField(max_length=255, default='')
