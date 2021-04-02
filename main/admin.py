from django.contrib import admin
from main.models import UserSettings, Order, Stocks

admin.site.register(UserSettings)
admin.site.register(Order)
admin.site.register(Stocks)
