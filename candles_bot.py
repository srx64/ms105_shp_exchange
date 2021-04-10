import os
import datetime
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exchange_engine.settings')
django.setup()

from main.models import Stocks, Candles, Quotes

def generate(candles, candles_len, stock, time, spec):
    one = []
    shift = candles[1].date - candles[1].date
    i = 0
    while i < candles_len:
        shift += candles[i + 1].date - candles[i].date
        if shift.seconds <= time:
            one.append(candles[i].price)
        else:
            shift = candles[1].date - candles[1].date
            candle = Candles(high=max(one), low=min(one), date=datetime.datetime.now(), type=spec, open=one[0], close=one[-1], stock=stock)
            candle.save()
            one = []
        i += 1







def candles_bot():
    ozon = Stocks.objects.get(name='OZON')
    candles = list(Quotes.objects.filter(stock=ozon))
    candles_len = len(candles)
    try:
        generate(candles, candles_len, ozon, 60, 1)
    except:
        pass
    try:
        generate(candles, candles_len, ozon, 300, 2)
    except:
        pass
    try:
        generate(candles, candles_len, ozon, 900, 3)
    except:
        pass
    try:
        generate(candles, candles_len, ozon, 1800, 4)
    except:
        pass
    try:
        generate(candles, candles_len, ozon, 3600, 5)
    except:
        pass





if __name__ == "__main__":
    candles_bot()
