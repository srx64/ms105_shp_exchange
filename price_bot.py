import os
import time
from math import sin, pi

from random import randint, choice, random

import django
import pandas
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exchange_engine.settings')
django.setup()

from main.models import Stocks, Order, User, Quotes


class NeutralFigureOne:
    @staticmethod
    def generate(_price):
        price = _price - _price * 0.05
        return price


class NeutralFigureTwo:
    @staticmethod
    def generate(_price):
        price = _price + _price * 0.05
        return price


class DowngradingFigureOne:
    @staticmethod
    def generate(_price):
        cut = randint(1, 5) * pi / 180
        price = _price - _price * sin(cut)
        return price


class DowngradingFigureTwo:
    @staticmethod
    def generate(_price):
        cut = randint(1, 5) * pi / 180
        price = _price - _price * sin(cut) * random()
        return price


class RaisingFigureOne:
    @staticmethod
    def generate(_price):
        cut = randint(1, 5) * pi / 180
        price = _price + _price * sin(cut)
        return price


class RaisingFigureTwo:
    @staticmethod
    def generate(_price):
        cut = randint(1, 5) * pi / 180
        price = _price + _price * sin(cut) * random()
        return price


class Figures:
    @staticmethod
    def set_figures(du, tendency):
        raising_figures = [RaisingFigureOne, RaisingFigureTwo]
        neutral_figures = [NeutralFigureOne, NeutralFigureTwo]
        downgrading_figures = [DowngradingFigureOne, DowngradingFigureTwo]
        data = []
        figures = []
        duration = []
        if tendency == 'raising':
            for i in range(du):
                figures.append(choice(raising_figures))
            for i in range(len(figures)):
                randomized = randint(1, 10)
                if randomized <= 3:
                    figures.insert(i, choice(downgrading_figures))
                elif 6 >= randomized >= 3:
                    figures.insert(i, choice(neutral_figures))
        elif tendency == 'downgrading':
            for i in range(du):
                figures.append(choice(downgrading_figures))
            for i in range(len(figures)):
                randomized = randint(1, 10)
                if randomized <= 3:
                    figures.insert(i, choice(raising_figures))
                elif 6 >= randomized >= 3:
                    figures.insert(i, choice(neutral_figures))
        for i in figures:
            duration.append(randint(2, 6))
        data.append(figures)
        data.append(duration)
        return data


class Tendencies:
    @staticmethod
    def choose_tendency():
        data = []
        tendencies = ['raising', 'downgrading']
        data.append(choice(tendencies))
        data.append(randint(5, 10))
        data.append([])
        return data


class MainCycle:
    @staticmethod
    def begin(am, us):
        user = us
        AMOUNT = am
        timer = 30  # потом придумаем ввод через админ - панель или около того
        stocks = Stocks.objects.all()
        data = [['none', 0, []] for _ in range(len(Stocks.objects.all()))]
        while True:
            for stock in stocks:
                info = data[stock.pk - 1]
                tendency = info[0]
                duration = info[1]
                if Quotes.objects.filter(stock=stock):
                    last_price = Quotes.objects.filter(stock=stock).last().price
                else:
                    last_price = randint(42, 5000)
                if duration == 0:
                    info = Tendencies.choose_tendency()
                    data[stock.pk - 1] = info
                else:
                    if info[2] == []:
                        info[2] = Figures.set_figures(duration, tendency)
                    else:
                        pack = []
                        figures = info[2][0]
                        duration = info[2][1]
                        result = next((x for x in range(len(duration)) if duration[x] > 0), 'not found')
                        if result == 'not found':
                            info[1] = 0
                        else:
                            duration[result] -= 1
                            price = figures[result].generate(last_price)
                            Order.objects.create(user=user, stock=stock, type=True, price=price, amount=AMOUNT, is_closed=True)
                            Order.objects.create(user=user, stock=stock, type=False, price=price, amount=AMOUNT, is_closed=True)
                            Order.objects.create(user=user, stock=stock, type=True, price=price, amount=AMOUNT * 10, is_closed=False)
                            Order.objects.create(user=user, stock=stock, type=False, price=price, amount=AMOUNT * 10, is_closed=False)
                            Quotes.objects.create(stock=stock, price=price)
                            stock.price = price
                            stock.save()
                        pack.append(figures)
                        pack.append(duration)
                        info[2] = pack
            time.sleep(timer)


def price_bot():
    logging.basicConfig(format='', level=logging.INFO)
    try:
        logging.info('Бот начал работу')
        files = next(os.walk('data/'))[2]
        min_file_length = min([len(open(f'data/{file}', 'r').readlines()) for file in files])
        user = User.objects.get(username='admin')
        AMOUNT = 10000
        for i in range(min_file_length - 1):
            for file in files:
                df = pandas.read_csv(f'data/{file}', nrows=1, skiprows=i, sep=';')
                name = df.iloc[0][0]
                if name[len(name) - 3:] != '-RM':
                    name = name.split('.')[1].split(':')[0]
                else:
                    name = name[:-3]
                stock = Stocks.objects.get(name=name)
                price = df.iloc[:, [7]][df.iloc[:, [7]].columns[0]][0]
                Order.objects.create(user=user, stock=stock, type=True, price=price, amount=AMOUNT, is_closed=True)
                Order.objects.create(user=user, stock=stock, type=False, price=price, amount=AMOUNT, is_closed=True)
                Order.objects.create(user=user, stock=stock, type=True, price=price, amount=AMOUNT * 10, is_closed=False)
                Order.objects.create(user=user, stock=stock, type=False, price=price, amount=AMOUNT * 10, is_closed=False)
                Quotes.objects.create(stock=stock, price=price)
                stock.price = price
                stock.save()
            time.sleep(30)
        MainCycle.begin(AMOUNT, user)

    except KeyboardInterrupt:
        logging.info('Бот остановлен пользователем')


if __name__ == "__main__":
    price_bot()
