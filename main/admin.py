from django.contrib import admin
from main.models import User, Order, Stocks, Settings, Portfolio, LeverageData, Quotes, Candles, CandlesData

admin.site.register(User)
admin.site.register(Order)
admin.site.register(Stocks)
admin.site.register(Quotes)
admin.site.register(Candles)
admin.site.register(Settings)
admin.site.register(Portfolio)
admin.site.register(CandlesData)
admin.site.register(LeverageData)
