import os
import time
from math import sin, pi
from typing import List

from django.utils import timezone
from random import randint, choice, random, uniform
import django
import pandas
import logging

from rest_framework import status
from rest_framework.response import Response

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exchange_engine.settings')
    django.setup()
except ImportError as exc:
    raise ImportError(
        "Couldn't import Django. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable? Did you "
        "forget to activate a virtual environment?"
    ) from exc

from main.models import Stocks, Order, User, Quotes, Portfolio, Settings, LeverageData

STOCKS_LIST = Stocks.objects.all()


class CrisisFigures:
    @staticmethod
    def small_crisis(last_price, stock_id):
        price = last_price - last_price * uniform(0.06667, 0.12245310)
        price = HandlingFunctions.check_price(price, stock_id)
        return price

    @staticmethod
    def medium_crisis(last_price, stock_id):
        price = last_price - last_price * uniform(0.08766755, 0.15809768576)
        price = HandlingFunctions.check_price(price, stock_id)
        return price

    @staticmethod
    def big_crisis(last_price, stock_id):
        price = last_price - last_price * uniform(0.15345336, 0.2578978)
        price = HandlingFunctions.check_price(price, stock_id)
        return price


class DowngradingFigures:
    @staticmethod
    def figure_one(last_price, stock_id):
        cut = uniform(0.64, 4.03) * pi / 180  # 1.1 - 7%
        price = last_price - last_price * sin(cut)
        price = HandlingFunctions.check_price(price, stock_id)
        return price

    @staticmethod
    def figure_two(last_price, stock_id):
        cut = uniform(0.84, 4.27) * pi / 180  # 1.4 - 7.4%
        price = last_price - last_price * sin(cut) * random()
        price = HandlingFunctions.check_price(price, stock_id)
        return price

    @staticmethod
    def figure_three(last_price, stock_id):
        cut = uniform(1, 3.86) * pi / 180  # 1.7 - 5%
        price = last_price - last_price * sin(cut) * uniform(0.67, 0.99)
        price = HandlingFunctions.check_price(price, stock_id)
        return price

    @staticmethod
    def figure_four(last_price, stock_id):
        price = last_price - last_price * uniform(0.02, 0.055)  # 2 - 5.5%
        price = HandlingFunctions.check_price(price, stock_id)
        return price


class RaisingFigures:
    @staticmethod
    def figure_one(last_price, stock_id):
        cut = uniform(0.64, 4.03) * pi / 180  # 1.1 - 7%
        price = last_price + last_price * sin(cut)
        price = HandlingFunctions.check_price(price, stock_id)
        return price

    @staticmethod
    def figure_two(last_price, stock_id):
        cut = uniform(0.84, 4.27) * pi / 180  # 1.4 - 7.4%
        price = last_price + last_price * sin(cut) * random()
        price = HandlingFunctions.check_price(price, stock_id)
        return price

    @staticmethod
    def figure_three(last_price, stock_id):
        cut = uniform(1, 3.86) * pi / 180  # 1.7 - 5%
        price = last_price + last_price * sin(cut) * uniform(0.67, 0.99)
        price = HandlingFunctions.check_price(price, stock_id)
        return price

    @staticmethod
    def figure_four(last_price, stock_id):
        price = last_price + last_price * uniform(0.02, 0.055)  # 2 - 5.5%
        price = HandlingFunctions.check_price(price, stock_id)
        return price


class HandlingFunctions:

    @staticmethod
    def get_settings(stock_id):
        if Settings.objects.filter(stock_id=-1, name='algo_quotes'):
            setting = Settings.objects.filter(stock_id=-1, name='algo_quotes').last()
            return setting
        elif Settings.objects.filter(stock_id=stock_id, name='algo_quotes'):
            setting = Settings.objects.filter(stock_id=stock_id, name='algo_quotes').last()
            return setting
        return None

    @staticmethod
    def get_generation_type(stock_id):
        if Settings.objects.filter(stock_id=stock_id, name='algo_quotes'):
            setting = Settings.objects.filter(stock_id=stock_id, name='algo_quotes').last()
            if setting.data['generation_type'] == 'default':
                return 'default'
            else:
                return setting.data['generation_type']
        elif Settings.objects.filter(stock_id=-1, name='algo_quotes'):
            setting = Settings.objects.filter(stock_id=-1, name='algo_quotes').last()
            if setting.data['generation_type'] == 'default':
                return 'default'
            else:
                return setting.data['generation_type']
        return None

    @staticmethod
    def get_timer():
        setting = None
        if Settings.objects.filter(stock_id=-1, name='frequency_generating_quotes'):
            setting = Settings.objects.filter(stock_id=-1, name='frequency_generating_quotes').last()
        if setting is not None:
            timer = setting.data['timer']
        else:
            timer = 30
        return timer

    @staticmethod
    def get_pause(stock_id):
        setting = None
        if Settings.objects.filter(stock_id=-1, name='quotes_generation_switch'):
            setting = Settings.objects.filter(stock_id=-1, name='quotes_generation_switch').last()
        elif Settings.objects.filter(stock_id=stock_id, name='quotes_generation_switch'):
            setting = Settings.objects.filter(stock_id=stock_id, name='quotes_generation_switch').last()
        if setting is None:
            return False
        elif setting.data['is_stop']:
            return True
        else:
            return False

    @staticmethod
    def get_last_price(stock):
        if Quotes.objects.filter(stock=stock):
            last_price = Quotes.objects.filter(stock=stock).last().price
        else:
            last_price = randint(42, 5000)
        return last_price

    @staticmethod
    def generate_orders(user, stock, price, AMOUNT, line=-1):
        Order.objects.create(user=user, stock=stock, type=True, price=price, amount=AMOUNT, is_closed=True)
        Order.objects.create(user=user, stock=stock, type=False, price=price, amount=AMOUNT, is_closed=True)
        Order.objects.create(user=user, stock=stock, type=True, price=price, amount=AMOUNT * 10, is_closed=False)
        Order.objects.create(user=user, stock=stock, type=False, price=price, amount=AMOUNT * 10, is_closed=False)
        Quotes.objects.create(stock=stock, price=price, line=line)
        stock.price = price
        stock.save()
        portfolio, created = Portfolio.objects.get_or_create(user=user, stock=stock)
        portfolio.count = 100000
        portfolio.save()

    @staticmethod
    def check_price(_price, stock_id):
        setting = HandlingFunctions.get_settings(stock_id)
        max_price = 15000
        min_price = 500
        if setting is not None and setting.data['max_price'] is not None and setting.data['min_price'] is not None:
            max_price = setting.data['max_price']
            min_price = setting.data['min_price']
            if _price > max_price:
                _price = max_price - max_price * uniform(0.03, 0.1)
            elif _price < min_price:
                _price = min_price + min_price * uniform(0.03, 0.1)
        else:
            if _price > max_price:
                _price = max_price - max_price * uniform(0.03, 0.1)
            elif _price < min_price:
                _price = min_price + min_price * uniform(0.03, 0.1)
        HandlingFunctions.limits_check(stock_id, min_price, max_price)
        return _price

    @staticmethod
    def update_generation_type(data, current_line):
        for stock in Stocks.objects.all():
            settings_type = HandlingFunctions.get_generation_type(stock.pk)
            if settings_type is not None:
                data[stock.pk - 1][0] = settings_type
            elif current_line >= data[stock.pk - 1][1]:
                data[stock.pk - 1][0] = 'formula'
            else:
                data[stock.pk - 1][0] = 'default'
        return data

    @staticmethod
    def generation_available(stock, user, amount):
        return not HandlingFunctions.get_pause(stock.pk) and not Tendencies.settings_check(
            stock,
            user,
            amount,
            HandlingFunctions.get_last_price(stock),
            HandlingFunctions.get_timer()
        )

    @staticmethod
    def get_table_data(stock, data):
        info = data[stock.pk - 1]
        start = info[0]
        cur = info[1]
        limit = info[2]
        duration = info[3]
        return start, cur, limit, duration


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
    def opposite_tendency(tendency):
        if tendency == 'raising':
            tendency = 'downgrading'
        elif tendency == 'downgrading':
            tendency = 'raising'
        return tendency

    @staticmethod
    def settings_check(stock, user, AMOUNT, last_price, t):
        if HandlingFunctions.get_settings(stock.id) is not None:
            setting = HandlingFunctions.get_settings(stock.id)
            if setting.data['start_after_time'] is not None:
                if setting.data['start_after_time'] > 0:
                    setting.data['start_after_time'] -= t
                elif setting.data['duration'] is not None:
                    if setting.data['duration'] > 0:
                        setting.data['duration'] -= t
                        if setting.data['type'] is not None:
                            coefficient = setting.data['coefficient']
                            f_type = setting.data['type']
                            figure = Figures.get_figure(f_type)
                            price = figure.generate(last_price, stock.id) * coefficient
                            HandlingFunctions.generate_orders(user, stock, price, AMOUNT, t)
                    elif setting.data['duration'] <= 0:
                        return False
            elif setting.data['coefficient'] is not None and setting.data['type'] is None:
                return False
            elif setting.data['duration'] is not None:
                if setting.data['duration'] > 0:
                    setting.data['duration'] -= t
                    if setting.data['type'] is not None:
                        coefficient = setting.data['coefficient']
                        f_type = setting.data['type']
                        figure = Figures.get_figure(f_type)
                        price = figure.generate(last_price, stock.id) * coefficient
                        HandlingFunctions.generate_orders(user, stock, price, AMOUNT, t)
                elif setting.data['duration'] <= 0:
                    return False
            elif setting.data['coefficient'] is not None and setting.data['type'] is None:
                return False

            setting.save()
            return True
        else:
            return False


class Figures:

    def __init__(self):
        self.raising_figures = [
            RaisingFigures.figure_one,
            RaisingFigures.figure_two,
            RaisingFigures.figure_three,
            RaisingFigures.figure_four
        ]
        self.downgrading_figures = [
            DowngradingFigures.figure_one,
            DowngradingFigures.figure_two,
            DowngradingFigures.figure_three,
            DowngradingFigures.figure_four
        ]
        self.crisis_figures = [
            CrisisFigures.small_crisis,
            CrisisFigures.medium_crisis,
            CrisisFigures.big_crisis
        ]

    def set_figures(self, figures_amount, tendency):

        data = []
        figures = []
        duration = []
        if tendency == 'raising':
            for i in range(figures_amount):
                figures.append(choice(self.raising_figures))
            for i in range(len(figures)):
                randomized = randint(1, 10)
                if randomized <= 3:
                    figures.insert(i, choice(self.downgrading_figures))
        elif tendency == 'downgrading':
            for i in range(figures_amount):
                figures.append(choice(self.downgrading_figures))
            for i in range(len(figures)):
                randomized = randint(1, 10)
                if randomized <= 3:
                    figures.insert(i, choice(self.raising_figures))
        for i in figures:
            duration.append(randint(2, 6))
        data.append(figures)
        data.append(duration)
        return data

    def get_figure(self, f_t):
        randomized = 0
        num = randint(1, 13)
        if f_t == 'raising':
            if 13 >= num >= 9:
                randomized = choice(self.raising_figures)
        elif f_t == 'downgrading':
            if 13 >= num >= 9:
                randomized = choice(self.downgrading_figures)
        elif f_t == 'crisis':
            randomized = choice(self.crisis_figures)
        return randomized


class PriceBot:

    def __init__(self) -> None:
        global STOCKS_LIST
        self.amount = 10000
        self.user = User.objects.get(username='admin')
        self.current_line = 1
        self.general_data = [['default', 600] for _ in range(len(Stocks.objects.all()))]
        self.table_data = [[0, 0, 0, 0] for _ in range(len(Stocks.objects.all()))]
        self.formulas_data = [['none', 0, []] for _ in range(len(Stocks.objects.all()))]
        self.general_data = HandlingFunctions.update_generation_type(self.general_data, self.current_line)
        self.files = next(os.walk('data/'))[2]

    def main_loop(self):
        while True:
            for stock in Stocks.objects.all():
                generation_type = self.general_data[stock.pk - 1][0]
                if generation_type == 'table':
                    print('Генерируем по странной таблице для', stock.name)
                    self.table_method(stock)
                elif generation_type == 'formula':
                    print('Генерируем по формулам для', stock.name)
                elif generation_type == 'default':
                    print('Генерируем стандартным методом для', stock.name)
                    self.default_method(stock)
                else:
                    logging.warning(
                        f'Неверно указан тип генерации для инструмента с названием {stock.name},'
                        f' генерация котировок не производится'
                    )
            time.sleep(HandlingFunctions.get_timer())
            self.current_line += 1

    def default_method(self, stock):
        if HandlingFunctions.generation_available(stock, self.user, self.amount):
            line_found = False
            for file in self.files:
                if not line_found:
                    df = pandas.read_csv(f'data/{file}', nrows=1, skiprows=self.current_line, sep=';')
                    name = df.iloc[0][0]
                    if name[:4] == 'MOEX':
                        name = name.split('.')[1].split(':')[0]
                    elif name[len(name) - 3:] == '-RM':
                        name = name[:-3]
                    if name == stock.name:
                        price = df.iloc[:, [7]][df.iloc[:, [7]].columns[0]][0]
                        HandlingFunctions.generate_orders(self.user, stock, price, self.amount, self.current_line)
                        line_found = True
                        logging.info('Добавлена новая котировка по таблице')

    def table_method(self, stock):
        if HandlingFunctions.generation_available(stock, self.user, self.amount):
            start, cur, limit, duration = HandlingFunctions.get_table_data(stock, self.table_data)
            line_found = False
            if duration == limit or duration == 0:
                self.table_data_refresh(stock)
            start, cur, limit, duration = HandlingFunctions.get_table_data(stock, self.table_data)
            for file in self.files:
                if not line_found:
                    df = pandas.read_csv(f'data/{file}', nrows=1, skiprows=cur, sep=';')
                    name = df.iloc[0][0]
                    if name[:4] == 'MOEX':
                        name = name.split('.')[1].split(':')[0]
                    elif name[len(name) - 3:] == '-RM':
                        name = name[:-3]
                    if name == stock.name:
                        price = df.iloc[:, [7]][df.iloc[:, [7]].columns[0]][0]
                        start, cur, limit, duration = HandlingFunctions.get_table_data(stock, self.table_data)
                        HandlingFunctions.generate_orders(
                            self.user, stock, price, self.amount, HandlingFunctions.get_timer()
                        )
                        duration -= 1
                        cur += 1
                        info = self.table_data[stock.pk - 1]
                        info[1] = cur
                        info[3] = duration


    def table_data_refresh(self, stock):
        start, cur, limit, duration = HandlingFunctions.get_table_data(stock, self.table_data)
        duration = randint(randint(5, 10), randint(10, 15))
        start = randint(0, self.general_data[stock.pk - 1][1] - duration)
        cur = start
        limit = cur + duration
        info = self.table_data[stock.pk - 1]
        info[0] = start
        info[1] = cur
        info[2] = limit
        info[3] = duration


def main():
    price_bot = PriceBot()
    price_bot.main_loop()


if __name__ == "__main__":
    main()
