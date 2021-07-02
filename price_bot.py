import os
import time
from datetime import datetime
from math import sin, pi
from django.utils import timezone
from random import randint, choice, random, uniform
import django
import pandas
import logging

from rest_framework import status
from rest_framework.response import Response

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exchange_engine.settings')
django.setup()

from main.models import Stocks, Order, User, Quotes, Portfolio, Settings, LeverageData

NEED_RESTART = False
START_FORMULAS = False
SAVE = 0


class CrisisFigureOne:
    @staticmethod
    def generate(_price, stock_id):
        price = _price - _price * uniform(0.06667, 0.12245310)
        price = HandlingFunctions.check_price(price, stock_id)
        return price


class CrisisFigureTwo:
    @staticmethod
    def generate(_price, stock_id):
        price = _price - _price * uniform(0.08766755, 0.15809768576)
        price = HandlingFunctions.check_price(price, stock_id)
        return price


class CrisisFigureThree:
    @staticmethod
    def generate(_price, stock_id):
        price = _price - _price * uniform(0.15345336, 0.2578978)
        price = HandlingFunctions.check_price(price, stock_id)
        return price


class NeutralFigureOne:
    @staticmethod
    def generate(_price, stock_id):
        price = _price - _price * 0.015
        price = HandlingFunctions.check_price(price, stock_id)
        return price


class NeutralFigureTwo:
    @staticmethod
    def generate(_price, stock_id):
        price = _price + _price * 0.015
        price = HandlingFunctions.check_price(price, stock_id)
        return price


class DowngradingFigureOne:
    @staticmethod
    def generate(_price, stock_id):
        cut = uniform(0.64, 4.03) * pi / 180
        price = _price - _price * sin(cut)
        price = HandlingFunctions.check_price(price, stock_id)
        return price


class DowngradingFigureTwo:
    @staticmethod
    def generate(_price, stock_id):
        cut = uniform(0.84, 4.27) * pi / 180
        price = _price - _price * sin(cut) * random()
        price = HandlingFunctions.check_price(price, stock_id)
        return price


class DowngradingFigureThree:
    @staticmethod
    def generate(_price, stock_id):
        cut = uniform(1, 3.86) * pi / 180
        price = _price - _price * sin(cut) * uniform(0.67, 0.99)
        price = HandlingFunctions.check_price(price, stock_id)
        return price


class DowngradingFigureFour:
    @staticmethod
    def generate(_price, stock_id):
        price = _price - _price * uniform(0.02, 0.055)
        price = HandlingFunctions.check_price(price, stock_id)
        return price


class RaisingFigureOne:
    @staticmethod
    def generate(_price, stock_id):
        cut = uniform(0.64, 4.03) * pi / 180
        price = _price + _price * sin(cut)
        price = HandlingFunctions.check_price(price, stock_id)
        return price


class RaisingFigureTwo:
    @staticmethod
    def generate(_price, stock_id):
        cut = uniform(0.84, 4.27) * pi / 180
        price = _price + _price * sin(cut) * random()
        price = HandlingFunctions.check_price(price, stock_id)
        return price


class RaisingFigureThree:
    @staticmethod
    def generate(_price, stock_id):
        cut = uniform(1, 3.86) * pi / 180
        price = _price + _price * sin(cut) * uniform(0.67, 0.99)
        price = HandlingFunctions.check_price(price, stock_id)
        return price


class RaisingFigureFour:
    @staticmethod
    def generate(_price, stock_id):
        price = _price + _price * uniform(0.02, 0.055)
        price = HandlingFunctions.check_price(price, stock_id)
        return price


class Figures:
    @staticmethod
    def set_figures(du, tendency):
        raising_figures = [RaisingFigureOne, RaisingFigureTwo, RaisingFigureThree, RaisingFigureFour]
        neutral_figures = [NeutralFigureOne, NeutralFigureTwo]
        downgrading_figures = [DowngradingFigureOne, DowngradingFigureTwo, DowngradingFigureThree,
                               DowngradingFigureFour]
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
    def get_figure(f_t):
        crisis_figures = [CrisisFigureOne, CrisisFigureTwo, CrisisFigureThree]
        raising_figures = [RaisingFigureOne, RaisingFigureTwo, RaisingFigureThree, RaisingFigureFour]
        neutral_figures = [NeutralFigureOne, NeutralFigureTwo]
        downgrading_figures = [DowngradingFigureOne, DowngradingFigureTwo, DowngradingFigureThree,
                               DowngradingFigureFour]
        randomized = 0
        num = randint(1, 13)
        if f_t == 'raising':
            if 13 >= num >= 10:
                randomized = choice(neutral_figures)
            else:
                randomized = choice(raising_figures)
        elif f_t == 'downgrading':
            if 13 >= num >= 10:
                randomized = choice(neutral_figures)
            else:
                randomized = choice(downgrading_figures)
        elif f_t == 'crisis':
            randomized = choice(crisis_figures)
        return randomized


class HandlingFunctions:
    @staticmethod
    def limits_check(stock_id, min_price, max_price):
        global NEED_RESTART
        quotes = list(Quotes.objects.filter(stock_id=stock_id))
        if len(quotes) > 1:
            shift = 0
            edited = list(reversed(quotes))
            for i in range(len(edited)):
                if i + 1 < len(edited):
                    if edited[i].price > max_price:
                        shift += (edited[i].date - edited[i+1].date).total_seconds()
                        if shift >= 15:
                            NEED_RESTART = True
                            shift = 0
                    elif edited[i].price < min_price:
                        shift += (edited[i].date - edited[i+1].date).total_seconds()
                        if shift >= 15:
                            NEED_RESTART = True
                            shift = 0

    @staticmethod
    def margin_call(user):
        """
        Margin call
        """
        if LeverageData.objects.filter(user=user):
            user_data = LeverageData.objects.get(user=user)
            if user.balance <= 0:
                for object in Order.objects.filter(user=user, stock=user_data.stock):
                    object.is_closed = True
                    object.save()

    @staticmethod
    def limit_order_counting(order):
        stock = Stocks.objects.get(id=order.stock_id)
        if Settings.objects.filter(stock_id=-1, name='short_switch'):
            setting = Settings.objects.filter(stock_id=-1, name='short_switch').last()
        elif Settings.objects.filter(stock_id=stock.id, name='short_switch'):
            setting = Settings.objects.filter(stock_id=stock.id, name='short_switch').last()
        type = order.type
        portfolio = Portfolio.objects.get(user_id=order.user_id, stock=order.stock_id)
        user = User.objects.get(id=order.user_id)
        order.is_limit = False

        if type == 0 and not portfolio.is_debt:
            if user.balance >= order.amount * order.price:

                portfolio.count += order.amount
                user.balance -= order.amount * order.price
            else:
                # обработать ошибку нехватки денег
                return Response({"detail": "incorrect data"}, status=status.HTTP_400_BAD_REQUEST)

        elif type == 1 and portfolio.count >= order.amount and not portfolio.is_debt:
            portfolio.count -= order.amount
            user.balance += order.amount * stock.price

        elif type == 1 and portfolio.count == 0 and not portfolio.is_debt:
            if (setting is None or setting.data['is_active']) or not setting.data['is_active']:
                if order.amount * order.price <= 100000 and portfolio.short_balance <= 0:
                    portfolio.short_balance += order.amount * order.price
                    portfolio.is_debt = True
                    portfolio.count = -order.amount
                else:
                    # обработать ошибку нельзя торговать шорт при переходе границы
                    return Response({"detail": "incorrect data"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # торговать в шорт не возможно
                return Response({"detail": "incorrect data"}, status=status.HTTP_400_BAD_REQUEST)

        elif type == 1 and portfolio.count < order.amount and portfolio.count != 0 and not portfolio.is_debt:
            if setting.data['is_active']:
                if (order.amount - portfolio.count) * order.price <= 100000 and portfolio.short_balance <= 0:
                    user.balance += portfolio.count * stock.price  # цена на данный момент
                    portfolio.is_debt = True
                    portfolio.count = portfolio.count - order.amount
                    portfolio.short_balance -= portfolio.count * stock.price
                else:
                    # обработать ошибку нельзя торговать шорт при переходе границы
                    return Response({"detail": "incorrect data"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # торговать в шорт не возможно
                return Response({"detail": "incorrect data"}, status=status.HTTP_400_BAD_REQUEST)

        elif type == 1 and portfolio.is_debt:
            if order.amount * order.price <= 100000 and portfolio.short_balance <= 0:
                portfolio.short_balance += order.amount * order.price
                portfolio.count -= order.amount
            else:
                # торговать в шорт невозможно
                return Response({"detail": "incorrect data"}, status=status.HTTP_400_BAD_REQUEST)

        elif type == 0 and portfolio.is_debt and portfolio.count < -order.amount:
            user.balance += (100000 - portfolio.short_balance) - order.amount * stock.price
            portfolio.count += order.amount

        elif type == 0 and portfolio.is_debt and portfolio.count == -order.amount:
            user.balance += (100000 - portfolio.short_balance) - order.amount * stock.price
            portfolio.count = 0
            portfolio.is_debt = False

        elif type == 0 and portfolio.is_debt and portfolio.count > -order.amount:
            if order.amount + portfolio.count * order.price < user.balance:
                user.balance += (
                                    100000 - portfolio.short_balance) - portfolio.count * stock.price
                portfolio.count = order.amount + portfolio.count
                portfolio.is_debt = False
                user.balance -= portfolio.count * order.price
            else:
                # обработать ошибку не хватки денег
                return Response({"detail": "incorrect data"}, status=status.HTTP_400_BAD_REQUEST)

        order.is_closed = True
        order.date_closed = timezone.now()
        user.save()
        order.save()
        portfolio.save()

        HandlingFunctions.margin_call(user)
        sred = portfolio.count
        portfolio.aver_price = ((portfolio.aver_price * (sred - order.amount)
                                 + abs(order.amount) * order.price) / max(abs(sred), 1) * bool(sred))
        portfolio.save()

    @staticmethod
    def limit_order_update():
        orders = Order.objects.filter(is_limit=True, is_closed=False)
        for order in orders:
            stock = Stocks.objects.get(id=order.stock_id)
            if order.amount != 0:
                if order.is_limit:
                    if order.type == 0:
                        if stock.price <= order.price:
                            HandlingFunctions.limit_order_counting(order)
                    else:
                        if stock.price >= order.price:
                            HandlingFunctions.limit_order_counting(order)

    @staticmethod
    def check_for_default():
        if Settings.objects.filter( name='algo_quotes'):
            for setting in Settings.objects.filter( name='algo_quotes'):
                if setting.data['generation_type'] is not None and setting.data['generation_type'] == 'default':
                    return True
        return False

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
    def get_stock_generation_type(stock_id):
        if Settings.objects.filter(stock_id=-1, name='algo_quotes'):
            setting = Settings.objects.filter(stock_id=-1, name='algo_quotes').last()
            if setting.data['generation_type'] is not None:
                if not HandlingFunctions.check_for_default():
                    return setting.data['generation_type']
                else:
                    return 'default'
        elif Settings.objects.filter(stock_id=stock_id, name='algo_quotes'):
            setting = Settings.objects.filter(stock_id=stock_id, name='algo_quotes').last()
            if setting.data['generation_type'] is not None:
                if not HandlingFunctions.check_for_default():
                    return setting.data['generation_type']
                else:
                    return 'default'
        return None

    @staticmethod
    def check_different_types():
        default = 0
        table = 0
        formula = 0
        if Settings.objects.filter(name='algo_quotes'):
            settings = Settings.objects.filter(name='algo_quotes')
            for setting in settings:
                s_type = setting.data['generation_type']
                if s_type is not None:
                    if s_type == 'default':
                        default += 1
                    elif s_type == 'table':
                        table += 1
                    elif s_type == 'formula':
                        formula += 1
            if HandlingFunctions.check_for_default():
                return False
            elif (default >= 1 and table >= 1 or formula >= 1) or table >= 1 and default >= 1 or formula >= 1:
                # print('Все путем')
                return True
            else:
                # print('Все путем, но немного другим')
                return False

    @staticmethod
    def get_table_generations(i, min_len):
        count = 0
        if Settings.objects.filter(name='algo_quotes'):
            settings = Settings.objects.filter(name='algo_quotes')
            for setting in settings:
                s_type = setting.data['generation_type']
                if s_type is not None:
                    if s_type == 'table':
                        count += 1
                    elif s_type == 'default' and i <= min_len:
                        count += 1
        return count

    @staticmethod
    def get_generation_type(stock_id):
        if Settings.objects.filter(stock_id=-1, name='algo_quotes'):
            setting = Settings.objects.filter(stock_id=-1, name='algo_quotes').last()
            if setting.data['generation_type'] == 'default':
                return 'default'
            else:
                return setting.data['generation_type']
        elif Settings.objects.filter(stock_id=stock_id, name='algo_quotes'):
            setting = Settings.objects.filter(stock_id=stock_id, name='algo_quotes').last()
            if setting.data['generation_type'] == 'default':
                return 'default'
            else:
                return setting.data['generation_type']
        return None

    @staticmethod
    def get_timer(stock_id):
        setting = None
        if Settings.objects.filter(stock_id=-1, name='frequency_generating_quotes'):
            setting = Settings.objects.filter(stock_id=-1, name='frequency_generating_quotes').last()
        elif Settings.objects.filter(stock_id=stock_id, name='frequency_generating_quotes'):
            setting = Settings.objects.filter(stock_id=stock_id, name='frequency_generating_quotes').last()
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
        # Order.objects.create(user=user, stock=stock, type=True, price=price, amount=AMOUNT, is_closed=True)
        # Order.objects.create(user=user, stock=stock, type=False, price=price, amount=AMOUNT, is_closed=True)
        # Order.objects.create(user=user, stock=stock, type=True, price=price, amount=AMOUNT * 10, is_closed=False)
        # Order.objects.create(user=user, stock=stock, type=False, price=price, amount=AMOUNT * 10, is_closed=False)
        Quotes.objects.create(stock=stock, price=price, line=line)
        stock.price = price
        stock.save()
        portfolio, created = Portfolio.objects.get_or_create(user=user, stock=stock)
        portfolio.count = 100000
        portfolio.save()
        HandlingFunctions.limit_order_update()
        print(datetime.now().minute, ':', datetime.now().second, 'created quote for ', stock.name, 'with price', price)

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

    @staticmethod
    def opposite_tendency(tendency):
        if tendency == 'raising':
            tendency = 'downgrading'
        elif tendency == 'downgrading':
            tendency = 'raising'
        return tendency


class MainCycle:
    @staticmethod
    def begin(am, us, t_stocks):
        global NEED_RESTART
        is_frozen = False
        user = us
        AMOUNT = am
        t = 30
        stocks = Stocks.objects.all()
        data = [['none', 0, []] for _ in range(len(Stocks.objects.all()))]
        f_generated = 0
        f_required = len(Stocks.objects.all()) - len(t_stocks)
        while True:
            print('Entered formulas')
            different_types = HandlingFunctions.check_different_types()
            for stock in stocks:
                info = data[stock.pk - 1]
                tendency = info[0]
                duration = info[1]
                last_price = HandlingFunctions.get_last_price(stock)
                t = HandlingFunctions.get_timer(stock.pk)
                is_frozen = HandlingFunctions.get_pause(stock.pk)
                # print('Formulas 1')
                if not is_frozen:
                    if not Tendencies.settings_check(stock, user, AMOUNT, last_price, t):
                        # print('Formula settings')
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
                                    # print('Formulas 2')
                                    if HandlingFunctions.get_stock_generation_type(stock.pk) != 'table' or START_FORMULAS and HandlingFunctions.get_stock_generation_type(stock.pk) != 'table':
                                        if stock not in t_stocks or t_stocks == []:
                                            if HandlingFunctions.get_settings(stock.pk) is not None and \
                                                HandlingFunctions.get_settings(stock.pk).data['coefficient'] is not None:
                                                coef = HandlingFunctions.get_settings(stock.pk).data['coefficient']
                                                price = figures[index].generate(last_price, stock.id) * coef
                                                if not NEED_RESTART:
                                                    HandlingFunctions.generate_orders(user, stock, price, AMOUNT, t)
                                                    f_generated += 1
                                                else:
                                                    f_tendency = info[0]
                                                    info = Tendencies.choose_tendency()
                                                    data[stock.pk - 1] = info
                                                    info[0] = Tendencies.opposite_tendency(f_tendency)
                                                    info[2] = Figures.set_figures(info[1], tendency)
                                                    NEED_RESTART = False
                                                    HandlingFunctions.generate_orders(user, stock, price, AMOUNT, t)
                                                    f_generated += 1
                                            else:
                                                # print('Formulas 3')
                                                price = figures[index].generate(last_price, stock.id)
                                                if not NEED_RESTART:
                                                    f_generated += 1
                                                    HandlingFunctions.generate_orders(user, stock, price, AMOUNT, t)
                                                else:
                                                    f_tendency = info[0]
                                                    info = Tendencies.choose_tendency()
                                                    data[stock.pk - 1] = info
                                                    info[0] = Tendencies.opposite_tendency(f_tendency)
                                                    info[2] = Figures.set_figures(info[1], tendency)
                                                    NEED_RESTART = False
                                                    HandlingFunctions.generate_orders(user, stock, price, AMOUNT, t)
                                                    f_generated += 1

                                print('Formula moment')
                                pack.append(figures)
                                pack.append(duration)
                                info[2] = pack
            print(f_generated)
            if data[0][2] != [] and f_generated != 0:
                time.sleep(t)
                if different_types or not different_types and f_generated >= f_required:
                    print('Я грохнулся')
                    break


def price_bot():
    logging.basicConfig(format='', level=logging.INFO)
    try:
        while True:
            logging.info('Бот начал работу')
            global SAVE
            global START_FORMULAS
            files = next(os.walk('data/'))[2]
            min_file_length = min([len(open(f'data/{file}', 'r').readlines()) for file in files])
            user = User.objects.get(username='admin')
            AMOUNT = 10000
            is_frozen = False
            settings_interruption = 0
            timer = 30
            is_exist = False
            gen_type = None
            # i = 0
            t_generated = 0
            t_required = 0
            t_stocks = []
            different_types = HandlingFunctions.check_different_types()
            while SAVE in range(min_file_length - 1) or gen_type == 'table' and not different_types:
                print(SAVE, '----')
                if not is_frozen:
                    if settings_interruption == 0:
                        for file in files:
                            df = pandas.read_csv(f'data/{file}', nrows=1, skiprows=SAVE, sep=';')
                            name = df.iloc[0][0]
                            if name[len(name) - 3:] != '-RM':
                                name = name.split('.')[1].split(':')[0]
                            else:
                                name = name[:-3]
                            stock = Stocks.objects.get(name=name)
                            print(stock)
                            price = df.iloc[:, [7]][df.iloc[:, [7]].columns[0]][0]
                            last_price = HandlingFunctions.get_last_price(stock)
                            timer = HandlingFunctions.get_timer(stock.pk)
                            is_frozen = HandlingFunctions.get_pause(stock.pk)
                            gen_type = HandlingFunctions.get_generation_type(stock.pk)
                            different_types = HandlingFunctions.check_different_types()
                            t_required = HandlingFunctions.get_table_generations(SAVE, min_file_length)
                            if Quotes.objects.filter(price=price, stock=stock, line=SAVE):
                                is_exist = True
                            if not Tendencies.settings_check(stock, user, AMOUNT, last_price, timer) and not is_exist \
                                or gen_type == 'table' or not START_FORMULAS and gen_type == 'default':
                                print('Table moment', t_generated, t_required)
                                HandlingFunctions.generate_orders(user, stock, price, AMOUNT, SAVE)
                                if stock not in t_stocks:
                                    t_stocks.append(stock)
                                t_generated += 1
                            elif gen_type != 'default':
                                settings_interruption = 1
                        if not is_exist or gen_type == 'table' and not different_types:
                            time.sleep(timer)
                    if not different_types or t_generated >= t_required or settings_interruption != 0:

                        t_generated = 0
                        # i += 1
                        SAVE += 1
                        if SAVE >= min_file_length:
                            t_stocks = []
                            START_FORMULAS = True
                        print('Я упал')
                        break
                    else:
                        # i += 1
                        SAVE += 1
            if gen_type != 'table' or different_types:
                MainCycle.begin(AMOUNT, user, t_stocks)

    except KeyboardInterrupt:
        logging.info('Бот остановлен пользователем')


if __name__ == "__main__":
    price_bot()
