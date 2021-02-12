from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Offers
from .serializers import OfferListSerializer

class OfferListView(APIView):

    def get(self, request):
        offers = Offers.objects.all()
        serializer = OfferListSerializer(offers, many=True)
        return Response(serializer.data)
