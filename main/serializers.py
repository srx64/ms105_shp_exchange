from rest_framework import serializers

from .models import Offers


class OfferListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = ("id", "price", "is_closed", "active_id", "type_id", "user_id")
