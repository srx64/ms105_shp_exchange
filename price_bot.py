import os
import time
from datetime import datetime
from math import sin, pi

from random import randint, choice, random, uniform

import django
import pandas
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exchange_engine.settings')
django.setup()

from main.models import Stocks, Order, User, Quotes, Portfolio


class CrisisFigureOne:
    @staticmethod
    def generate(_price):
        price = _price - _price * uniform(0.30, 0.39)
        return price


class CrisisFigureTwo:
    @staticmethod
    def generate(_price):
        price = _price - _price * uniform(0.40, 0.49)
        return price


class CrisisFigureThree:
    @staticmethod
    def generate(_price):
        price = _price - _price * uniform(0.50, 0.59)
        return price


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


class DowngradingFigureThree:
    @staticmethod
    def generate(_price):
        cut = randint(1, 5) * pi / 180
        price = _price - _price * sin(cut) * uniform(0.8, 0.99)
        return price


class DowngradingFigureFour:
    @staticmethod
    def generate(_price):
        price = _price - _price * uniform(0.02, 0.09)
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


class RaisingFigureThree:
    @staticmethod
    def generate(_price):
        cut = randint(1, 5) * pi / 180
        price = _price + _price * sin(cut) * uniform(0.8, 0.99)
        return price


class RaisingFigureFour:
    @staticmethod
    def generate(_price):
        price = _price + _price * uniform(0.02, 0.09)
        return price


class Figures:
    @staticmethod
    def set_figures(du, tendency):
        raising_figures = [RaisingFigureOne, RaisingFigureTwo, RaisingFigureThree, RaisingFigureFour]
        neutral_figures = [NeutralFigureOne, NeutralFigureTwo]
        downgrading_figures = [DowngradingFigureOne, DowngradingFigureTwo, DowngradingFigureThree, DowngradingFigureFour]
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

    @staticmethod
    def get_crisis_figure():
        crisis_figures = [CrisisFigureOne, CrisisFigureTwo, CrisisFigureThree]
        randomized = choice(crisis_figures)
        return randomized


class HandlingFunctions:
    @staticmethod
    def get_last_price(stock):
        if Quotes.objects.filter(stock=stock):
            last_price = Quotes.objects.filter(stock=stock).last().price
        else:
            last_price = randint(42, 5000)
        return last_price

    @staticmethod
    def generate_orders(user, stock, price, AMOUNT):
        Order.objects.create(user=user, stock=stock, type=True, price=price, amount=AMOUNT, is_closed=True)
        Order.objects.create(user=user, stock=stock, type=False, price=price, amount=AMOUNT, is_closed=True)
        Order.objects.create(user=user, stock=stock, type=True, price=price, amount=AMOUNT * 10, is_closed=False)
        Order.objects.create(user=user, stock=stock, type=False, price=price, amount=AMOUNT * 10, is_closed=False)
        Quotes.objects.create(stock=stock, price=price)
        stock.price = price
        stock.save()
        portfolio, created = Portfolio.objects.get_or_create(user=user, stock=stock)
        portfolio.count = 100000
        portfolio.save()


class Tendencies:
    @staticmethod
    def choose_tendency():
        data = []
        tendencies = ['raising', 'downgrading']
        data.append(choice(tendencies))
        data.append(randint(5, 10))
        data.append([])
        return data

    @staticmethod
    def crisis_check(c_begin, c_end, stock, user, AMOUNT, last_price):
        now = datetime.now()
        if c_end >= now <= c_begin:
            figure = Figures.get_crisis_figure()
            price = figure.generate(last_price)
            HandlingFunctions.generate_orders(user, stock, price, AMOUNT)
            return True
        else:
            return False


class MainCycle:
    @staticmethod
    def begin(am, us, t, c_b, c_e):
        user = us
        AMOUNT = am
        timer = t
        stocks = Stocks.objects.all()
        data = [['none', 0, []] for _ in range(len(Stocks.objects.all()))]
        while True:
            for stock in stocks:
                info = data[stock.pk - 1]
                tendency = info[0]
                duration = info[1]
                last_price = HandlingFunctions.get_last_price(stock)
                if not Tendencies.crisis_check(c_b, c_e, stock, user, AMOUNT, last_price):
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
                            index = next((x for x in range(len(duration)) if duration[x] > 0), 'not found')
                            if index == 'not found':
                                info[1] = 0
                            else:
                                duration[index] -= 1
                                price = figures[index].generate(last_price)
                                HandlingFunctions.generate_orders(user, stock, price, AMOUNT)
                            pack.append(figures)
                            pack.append(duration)
                            info[2] = pack
                time.sleep(timer)


def price_bot():
    logging.basicConfig(format='', level=logging.INFO)
    try:
        crisis_start = datetime.now()
        crisis_end = datetime.now()  # потом сделаем ввод через админ - панель или около того
        logging.info('Бот начал работу')
        files = next(os.walk('data/'))[2]
        min_file_length = min([len(open(f'data/{file}', 'r').readlines()) for file in files])
        user = User.objects.get(username='admin')
        AMOUNT = 10000
        timer = 30  # потом придумаем ввод через админ - панель или около того
        crisis_interruption = 0
        for i in range(min_file_length - 1):
            if crisis_interruption == 0:
                for file in files:
                    df = pandas.read_csv(f'data/{file}', nrows=1, skiprows=i, sep=';')
                    name = df.iloc[0][0]
                    if name[len(name) - 3:] != '-RM':
                        name = name.split('.')[1].split(':')[0]
                    else:
                        name = name[:-3]
                    stock = Stocks.objects.get(name=name)
                    portfolio, created = Portfolio.objects.get_or_create(user=user, stock=stock)
                    portfolio.count = 100000
                    portfolio.save()
                    price = df.iloc[:, [7]][df.iloc[:, [7]].columns[0]][0]
                    last_price = HandlingFunctions.get_last_price(stock)
                    if not Tendencies.crisis_check(crisis_start, crisis_end, stock, user, AMOUNT, last_price):
                        HandlingFunctions.generate_orders(user, stock, price, AMOUNT)
                    else:
                        crisis_interruption = 1
                time.sleep(timer)
            else:
                break
        MainCycle.begin(AMOUNT, user, timer, crisis_start, crisis_end)

    except KeyboardInterrupt:
        logging.info('Бот остановлен пользователем')


if __name__ == "__main__":
    price_bot()
