import os
import csv
import time
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exchange_engine.settings')
django.setup()

from main.models import Stocks, Order, User, Quotes


def price_bot():
    user = User.objects.get(username='admin')
    with open('data/OZON2015-2021.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        AMOUNT = 10000
        flag = False
        for line in reader:
            if flag:
                row = line[0].split(';')
                if row[len(row) - 3:] != '-RT':
                    name = row[0].split('.')[1].split(':')[0]
                else:
                    name = row[0][:-3]
                stock = Stocks.objects.get(name=name)
                price = row[7]
                sale_order = Order(user=user, stock=stock, type=True, price=price, amount=AMOUNT, is_closed=True)
                sale_order.save()
                purchase_order = Order(user=user, stock=stock, type=False, price=price, amount=AMOUNT, is_closed=True)
                purchase_order.save()
                quote = Quotes(stock=stock, price=price)
                quote.save()
                time.sleep(30)
            flag = True


if __name__ == "__main__":
    price_bot()
