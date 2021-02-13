from django.shortcuts import render
from main.models import Actives, Offers, Portfolio

from rest_framework.response import Response
from rest_framework.views import APIView
from main import serializers

# Create your views here.

#test
class ActivesListView(APIView):
    """Список активов"""
    def get(self, request):
        actives = Actives.objects.filter(is_active=True)
        serializer = serializers.ActivesSerializer(actives, many=True)
        return Response(serializer.data)

class ActiveDetailView(APIView):
    """Информация об активе"""
    def get(self, request, pk):
        active = Actives.objects.get(id=pk)
        serializer = serializers.ActiveDetailSerializer(active)
        return Response(serializer.data)

class OffersView(APIView):
    """Все заявки"""
    def get(self, request):
        offers = Offers.objects.filter(is_closed=False)
        serializer = serializers.OffersSerializer(offers, many=True)
        return Response(serializer.data)

class PortfolioUserView(APIView):
    """Все заявки"""
    def get(self, request, pk):
        portfolio = Portfolio.objects.filter(user_id=pk)
        serializer = serializers.PortfolioUserSerializer(portfolio, many=True)
        return Response(serializer.data)
