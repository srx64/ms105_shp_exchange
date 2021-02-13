from rest_framework import serializers
from main.models import Actives, Offers, Portfolio


class ActivesSerializer(serializers.ModelSerializer):
    """ Краткая информация об активе"""
    class Meta:
        model = Actives
        fields = ("name", "avg_price", "type")


class ActiveDetailSerializer(serializers.ModelSerializer):
    """ Детальная информация об активе"""
    type = serializers.SlugRelatedField(slug_field="name", read_only=True)
    class Meta:
        model = Actives
        fields = '__all__'


class OffersSerializer(serializers.ModelSerializer):
    """Заявки на покупку/продажу"""
    type = serializers.SlugRelatedField(slug_field="name", read_only=True)
    active = serializers.SlugRelatedField(slug_field="name", read_only=True)
    class Meta:
        model = Offers
        fields = '__all__'


class PortfolioUserSerializer(serializers.ModelSerializer):
    active = serializers.SlugRelatedField(slug_field="name", read_only=True)
    class Meta:
        model = Portfolio
        fields = '__all__'
