import os
import datetime
import django
import pytz

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exchange_engine.settings')
django.setup()

from main.models import Stocks, Candles, Quotes


def generate(candles, candles_len, stock, time, spec, last):
    one = []
    shift = candles[0].date - candles[0].date
    i = last[spec-1]
    while i < candles_len:
        if candles_len >= 2:
            shift += candles[i + 1].date - candles[i].date
            if shift.seconds <= time:
                one.append(candles[i].price)
            else:
                if len(one) > 0:
                    shift = candles[1].date - candles[1].date
                    candle = Candles(
                        high=max(one),
                        low=min(one),
                        date=datetime.datetime.now(pytz.timezone('Europe/Moscow')),
                        type=spec,
                        open=one[0],
                        close=one[-1],
                        stock=stock
                    )
                    last[spec-1] = i
                    candle.save()
                    one = []

            if i == candles_len - 2:
                return last
            i += 1


def candles_bot():
    types = [60, 300, 900, 1800, 3600]
    try:
        print("Бот начал работу")
        data = [[0, 0, 0, 0, 0] for _ in range(len(Stocks.objects.all()))]
        while True:
            for stock in Stocks.objects.all():
                if Quotes.objects.filter(stock=stock):
                    info = data[stock.pk - 1]
                    candles = list(Quotes.objects.filter(stock=stock))
                    candles_len = len(candles)
                    for i in range(len(types)):
                        info = generate(candles, candles_len, stock, types[i], i+1, info)
    except KeyboardInterrupt:
        print("Бот остановлен пользователем")


if __name__ == "__main__":
    candles_bot()
