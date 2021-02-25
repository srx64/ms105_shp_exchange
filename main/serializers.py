from rest_framework import serializers
from main.models import Stocks, Offers, Portfolio, User, UserSettings


class StocksSerializer(serializers.ModelSerializer):
    """ Список всех акций"""
    class Meta:
        model = Stocks
        fields = '__all__'


class StockDetailSerializer(serializers.ModelSerializer):
    """ Детальная информация об акции"""
    class Meta:
        model = Stocks
        fields = '__all__'


class ProfileDetailSerializer(serializers.ModelSerializer):
    """ Детальная информация об акции"""
    class Meta:
        model = User
        fields = '__all__'


class OffersSerializer(serializers.ModelSerializer):
    """Заявки на покупку/продажу"""
    stock = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Offers
        fields = '__all__'


class PortfolioUserSerializer(serializers.ModelSerializer):
    """Портфолио"""
    stock = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Portfolio
        fields = '__all__'


class ProfileUserAvatarSerializer(serializers.ModelSerializer):
    """Аватарка"""
    field = serializers.SlugRelatedField(slug_field="avatar", read_only=True)

    class Meta:
        model = UserSettings
        fields = '__all__'
