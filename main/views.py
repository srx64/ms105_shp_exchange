from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Stocks, Offers, Portfolio, User
from main import serializers


class StocksListView(APIView):
    """Список акций"""
    def get(self, request):
        stocks = Stocks.objects.filter(is_active=True)
        serializer = serializers.StocksSerializer(stocks, many=True)
        return Response(serializer.data)


class StockDetailView(APIView):
    """Информация об акции"""
    def get(self, request, pk):
        stock = Stocks.objects.get(id=pk)
        serializer = serializers.StockDetailSerializer(stock)
        return Response(serializer.data)


class ProfileDetailView(APIView):
    """Информация об акции"""
    def get(self, request):
        user = User.objects.get(id=1)
        serializer = serializers.ProfileDetailSerializer(user)
        return Response(serializer.data)


class OffersView(APIView):
    """Все заявки"""
    def get(self, request):
        offers = Offers.objects.filter(is_closed=False)
        serializer = serializers.OffersSerializer(offers, many=True)
        return Response(serializer.data)


class PortfolioUserView(APIView):
    """Портфолио пользователя"""
    def get(self, request, pk):
        portfolio = Portfolio.objects.filter(user_id=pk)
        serializer = serializers.PortfolioUserSerializer(portfolio, many=True)
        return Response(serializer.data)
