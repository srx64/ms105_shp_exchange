from rest_framework import serializers
from main.models import Stocks, Order, Portfolio, User, Quotes, Statistics, Candles, Settings, Cryptocurrencies


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password must match'})
        account.set_password(password)
        account.save()
        return account


class CandlesSerializer(serializers.ModelSerializer):
    """Свечи для графика"""

    class Meta:
        model = Candles
        fields = ('date', 'open', 'close', 'high', 'low', 'type')


class StocksSerializer(serializers.ModelSerializer):
    """Список всех акций"""

    class Meta:
        model = Stocks
        fields = '__all__'


class SettingsSerializer(serializers.ModelSerializer):
    """Настройки биржи"""

    class Meta:
        model = Settings
        fields = '__all__'


class ProfileDetailSerializer(serializers.ModelSerializer):
    """ Детальная информация о пользователе"""

    class Meta:
        model = User
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    """Заявки на покупку/продажу"""
    stock = StocksSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class StatisticsSerializer(serializers.ModelSerializer):
    statistics = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Statistics
        fields = '__all__'


class CryptocurrenciesSerializer(serializers.ModelSerializer):
    cryptocurrencies = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Cryptocurrencies
        fields = '__all__'


class PortfolioUserSerializer(serializers.ModelSerializer):
    """Портфолио"""
    stock = StocksSerializer()

    class Meta:
        model = Portfolio
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotes
        fields = '__all__'


class StatisticsBalanceSerializer(serializers.ModelSerializer):
    """ Детальная информация о пользователе"""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'balance')
