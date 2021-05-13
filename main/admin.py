from django.contrib import admin
from main.models import Order, Stocks, Settings

admin.site.register(Order)
admin.site.register(Stocks)
admin.site.register(Settings)
