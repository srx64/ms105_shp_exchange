import os
import time
import django
import pandas
import logging


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exchange_engine.settings')
django.setup()

from main.models import Stocks, Order, User, Quotes


def price_bot():
    logging.basicConfig(format='', level=logging.INFO)
    try:
        logging.info('Бот начал работу')
        files = next(os.walk('data/'))[2]
        min_file_length = min([len(open(f'data/{file}', 'r').readlines()) for file in files])
        user = User.objects.get(username='admin')
        AMOUNT = 10000
        for i in range(min_file_length):
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
                quote = Quotes(stock=stock, price=price)
                quote.save()
            time.sleep(30)
    except KeyboardInterrupt:
        logging.info('Бот остановлен пользователем')


if __name__ == "__main__":
    price_bot()
