from django.contrib import admin
from main.models import User, Order, Stocks, Settings, Portfolio, LeverageData

admin.site.register(User)
admin.site.register(Order)
admin.site.register(Stocks)
admin.site.register(Settings)
admin.site.register(Portfolio)
admin.site.register(LeverageData)
