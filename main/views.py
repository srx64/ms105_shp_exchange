from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework import filters, status
from main.forms import LeverageTradingForm, UserBalance
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from bs4 import BeautifulSoup

from main.models import Stocks, Order, Portfolio, User, Quotes, LeverageData, Statistics, Candles, Settings, Cryptocurrencies
from main import serializers

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q


@api_view(['POST'])
def registration_view(request):
    """
    Регистрация пользователей

    На вход подаются имя пользователя, его электронная почта и пароль.
    """
    if request.method == 'POST':
        serializer = serializers.RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "succefully"
            data['email'] = account.email
            data['username'] = account.username
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data)


class AddOrderView(APIView):
    """
    Добавление ордера

    :param price: Цена ордера
    :param stock: Имя акции
    :param type: Тип ордера
    :param amount: Количество ордеров
    """
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def margin_call(user):
        """
        Margin call
        """
        if LeverageData.objects.filter(user=user):
            user_data = LeverageData.objects.get(user=user)
            if user.balance <= 0:
                for object in Order.objects.filter(user=user, stock=user_data.stock):
                    object.is_closed = True
                    object.save()

    @staticmethod
    def set_percentage(user_portfolio):
        """
        Установка процента в портфолио
        """
        sum = 0
        portfolios = Portfolio.objects.filter(stock_id=user_portfolio.stock_id)
        for object in portfolios:
            sum += object.count
        if sum == 0:
            per_stocks = 100
        else:
            per_stocks = (user_portfolio.count / sum) * 100
        user_portfolio.percentage = per_stocks
        user_portfolio.save()

    def post(self, request):
        """
        Создание ордера и обработка данных при POST запросе

        На вход подаются следующие параметры:
        - токен пользователя.
        """
        data = request.data
        user = User.objects.get(id=request.user.pk)
        name = data['stock']
        stock = Stocks.objects.get(name=name)
        type = data['type']
        price = float(data['price'])
        amount = int(data['amount'])
        balance = user.balance
        if price == 0:
            price = stock.price
        setting = None
        if Settings.objects.filter(stock_id=-1, name='short_switch'):
            setting = Settings.objects.filter(stock_id=-1, name='short_switch').last()
        elif Settings.objects.filter(stock_id=stock.id, name='short_switch'):
            setting = Settings.objects.filter(stock_id=stock.id, name='short_switch').last()
        if price <= 0 or amount <= 0:
            return Response({"detail": "incorrect data"}, status=status.HTTP_400_BAD_REQUEST)
        self.margin_call(user)

        flag = False
        if Portfolio.objects.filter(user=user, stock=stock).exists() and \
            Portfolio.objects.get(user=user, stock=stock).count > 0:
            flag = True
        if (setting is None or setting.data['is_active']) or (not setting.data['is_active'] and type == 0) or \
            (not setting.data['is_active'] and type == 1 and flag):
            portfolio, created = Portfolio.objects.get_or_create(user=user, stock=stock)
            self.set_percentage(portfolio)
            order = Order(user=user, stock=stock, type=type, price=price, is_closed=False, amount=amount, count=amount)

            if order.amount != 0:

                if type == 0 and not portfolio.is_debt:
                    if user.balance >= order.amount * order.price:
                        portfolio.count += order.amount
                        user.balance -= order.amount * order.price
                        user.save()
                        portfolio.save()
                    else:
                        # обработать ошибку не хватки денег
                        return Response({"detail": "incorrect data"}, status=status.HTTP_400_BAD_REQUEST)

                elif type == 1 and portfolio.count >= order.amount and not portfolio.is_debt:
                    portfolio.count -= order.amount
                    user.balance += order.amount * stock.price
                    user.save()
                    portfolio.save()

                elif type == 1 and portfolio.count == 0 and not portfolio.is_debt:
                    if (setting is None or setting.data['is_active']) or not setting.data['is_active']:
                        if order.amount * order.price <= 100000:
                            portfolio.short_balance += order.amount * order.price
                            portfolio.is_debt = True
                            portfolio.count = -order.amount
                            portfolio.save()
                        else:
                              # обработать ошибку нельзя торговать шорт при захождении заграницу
                            return Response({"detail": "incorrect data"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        # торговать в шорт не возможно
                        return Response({"detail": "incorrect data"}, status=status.HTTP_400_BAD_REQUEST)
                elif type == 1 and portfolio.count < order.amount and portfolio.count != 0 and not portfolio.is_debt:
                    if setting.data['is_active']:
                        if (order.amount - portfolio.count) * order.price <= 100000:
                            user.balance += portfolio.count * stock.price # цена на данный момент
                            portfolio.is_debt = True
                            portfolio.count = portfolio.count - order.amount
                            portfolio.short_balance -= portfolio.count * stock.price
                            user.save()
                            portfolio.save()
                        else:
                            # обработать ошибку нельзя торговать шорт при захождении заграницу
                            return Response({"detail": "incorrect data"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        # торговать в шорт не возможно
                        return Response({"detail": "incorrect data"}, status=status.HTTP_400_BAD_REQUEST)

                elif type == 1 and portfolio.is_debt:
                    if order.amount * order.price <= 100000:
                        portfolio.short_balance += order.amount * order.price
                        portfolio.count -= order.amount
                        user.save()
                        portfolio.save()

                elif type == 0 and portfolio.is_debt and portfolio.count < -order.amount:
                    user.balance += (100000 - portfolio.short_balance) - order.amount * stock.price
                    portfolio.count += order.amount
                    user.save()
                    portfolio.save()

                elif type == 0 and portfolio.is_debt and portfolio.count == -order.amount:
                    user.balance += (100000 - portfolio.short_balance) - order.amount * stock.price
                    portfolio.count = 0
                    portfolio.is_debt = False
                    user.save()
                    portfolio.save()

                elif type == 0 and portfolio.is_debt and portfolio.count > -order.amount:
                    if order.amount + portfolio.count * order.price < user.balance:
                        user.balance += (100000 - portfolio.short_balance) - portfolio.count * stock.price
                        portfolio.count = order.amount + portfolio.count
                        portfolio.is_debt = False
                        user.balance -= portfolio.count * order.price
                        user.save()
                        portfolio.save()
                    else:
                        # обработать ошибку не хватки денег
                        return Response({"detail": "incorrect data"}, status=status.HTTP_400_BAD_REQUEST)

                self.margin_call(user)
                self.set_percentage(portfolio)
                sred = portfolio.count
                portfolio.aver_price = ((sred * (sred - order.amount)
                                        + abs(order.amount) * order.price) / max(abs(sred), 1) * bool(sred))

            order.is_closed = True
            order.date_closed = timezone.now()
            order.save()
            portfolio.save()
        return Response("/api/v1/orders/")


class StocksListView(ListAPIView):
    """
    Отображение списка акций при GET запросе

    Список всех акций, присутсвующих на бирже.
    """
    queryset = Stocks.objects.filter(is_active=True)
    serializer_class = serializers.StocksSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class StockDetailView(APIView):
    """
    Информация об акции
    """

    def get(self, request, pk):
        """
        Отображение данных о конкретной акции при GET запросе

        На вход принимается id акции.
        """
        stock = Stocks.objects.get(id=pk)
        serializer = serializers.StocksSerializer(stock)
        return Response(serializer.data)


class SettingsView(APIView):

    def get(self, request):
        """
        Отображение текущих настроек при GET запросе.

        Просто отображение настроек. Изменять настройки могут только администраторы.
        На вход ничего не принимается.
        """
        serializer = serializers.SettingsSerializer(Settings.objects.all(), many=True)
        return Response(serializer.data)


class CryptocurrenciesView(APIView):

    def get(self, request):
        """
        Отображение текущей цены некоторых криптовалют

        На данный момент это не используется!
        """
        cryptocurrencies = Cryptocurrencies.objects.all()

        URL = 'https://coinmarketcap.com/ru/all/views/all/'
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36'
        }
        response = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('tr', class_='cmc-table-row')
        comps = []
        for item in items:
            comps.append({
                'title': item.find('a', class_='cmc-link').get_text(strip=True),
                'pric': item.find('div', class_='price___3rj7O')
            })

        for comp in comps:
            if comp['pric']:
                try:
                    cryptocurrencies = Cryptocurrencies.objects.get(name=comp['title'])
                    cryptocurrencies.name = comp['title']
                    cryptocurrencies.price = comp['pric'].string
                    cryptocurrencies.save()
                except ObjectDoesNotExist:
                    Cryptocurrencies.objects.create(name=comp['title'], price=comp['pric'].string)
        cryptocurrencies = Cryptocurrencies.objects.all()
        serializer = serializers.CryptocurrenciesSerializer(cryptocurrencies, many=True)
        return Response(serializer.data)


class StatisticsView(APIView):
    """
    Статистика биржи
    """
    def get(self, *args) -> Response:
        """
        Отображение статистики при GET запросе

        Здесь вы можете увидеть

        * количество открытых ордеров;
        * количество закрытых ордеров;
        * количество активных пользователей;
        * количество акций;
        * количество пользователей, торгующих в лонг;
        * количество пользователей, торгующих в шорт;
        * максимальный баланс на бирже и самого богатого пользователя.

        При обращении происходит перерасчёт значений.

        На вход ничего не принимается.
        """
        Statistics.update_statistics()
        serializer = serializers.StatisticsSerializer(Statistics.get_all_stats(), many=True)
        return Response(serializer.data)


class ProfileAnotherView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        serializer = serializers.ProfileDetailSerializer(user)
        return Response(serializer.data)


class ProfileDetailView(APIView):
    """
    Информация о пользователе

    :param profile: Профиль
    :param avatar: Аватарка пользователя
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Отображение профиля пользователя при GET запросе

        Просто отображение профиля. Данные доступны только зарегистрированным пользователям.

        На вход принимается только токен пользователя.
        """
        user = request.user
        return Response(serializers.ProfileDetailSerializer(user).data)

    def patch(self, request):
        """
        Редактирование профиля

        Изменение имени, фамилии, электронной почты и пароля пользователя. На вход принимается 1 параметр: токен пользователя.
        """
        user = request.user
        data = request.data

        user.email = data.get("email", user.email)
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        password2 = data.get("password2", user.password)
        if password2:
            if user.check_password(data.get("password", user.password)):
                user.set_password(password2)

        if request.FILES:
            user.avatar = request.FILES['file']

        user.save()
        serializer = serializers.ProfileDetailSerializer(user)

        return Response(serializer.data)


class CandlesView(APIView):
    """
    Свечи
    """
    def get(self, request, pk, c_type):
        """
        Отображение списка свечей данной акции и данного типа при GET запросе

        Свечи генерируются с помощью специального бота.
        """
        if c_type > 0:
            candles = Candles.objects.filter(stock_id=pk, type=c_type)
        elif c_type == 0:
            candles = Candles.objects.filter(stock_id=pk)
        serializer = serializers.CandlesSerializer(candles, many=True)
        return Response(serializer.data)


class OrdersView(APIView):
    """
    Все заявки пользователя
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Отображение всех ордеров пользователя при GET запросе

        На вход подаётся только токен пользователя.
        """
        user = request.user
        if user.is_staff:
            orders = Order.objects.filter(~Q(user_id=User.objects.get(username='admin')))
        else:
            orders = Order.objects.filter(user_id=user)
        serializer = serializers.OrdersSerializer(orders, many=True)
        return Response(serializer.data)


class PortfolioUserView(APIView):
    """
    Портфолио пользователя
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Отображение портфолио пользователя при GET запросе

        На вход подаётся только токен пользователя.
        """
        user = request.user
        if user.is_staff:
            portfolio = Portfolio.objects.filter(~Q(count=0), ~Q(user_id=User.objects.get(username='admin')))
        else:
            portfolio = Portfolio.objects.filter(~Q(count=0), user_id=request.user.id)
        serializer = serializers.PortfolioUserSerializer(portfolio, many=True)
        return Response(serializer.data)


class LeverageTradingView(APIView):
    """
    Торговля с плечом
    """

    def get(self, request):
        """
        Отображение формы для торговли с плечом при GET запросе

        Просто форма для торговли с плечом. На вход подаётся только токен пользователя.
        """
        form = LeverageTradingForm(initial={
            'type': 0,
            'stock': 0,
            'ratio': 2,
        })
        user = User.objects.get(id=request.user.pk)
        context = {
            'user': user,
            'form': form,
            'too_low': 0,
        }
        return render(request, 'trading/leverage.html', context)

    def post(self, request):
        """
        Торговля с плечом и обработка данных при POST запросе

        На вход принимается 3 параметра:
        - токен пользователя.
        - `stock` - акция, которой торгует пользователь.
        - `ratio` - размер плеча.
        """
        form = LeverageTradingForm(request.POST)
        data = request.data
        user = User.objects.get(id=request.user.pk)
        ratio = int(data['ratio'])
        stock = Stocks.objects.get(name=data['stock'])
        quote = Quotes.objects.filter(stock=stock.id).last()
        type = bool(data.get('type', False))
        cash = user.balance * ratio
        setting = 'None'
        if Settings.objects.filter(stock_id=-1, name='leverage'):
            setting = Settings.objects.filter(stock_id=-1, name='leverage').last()
        elif Settings.objects.filter(stock_id=stock.pk, name='leverage'):
            setting = Settings.objects.filter(stock_id=stock.pk, name='leverage').last()
        if setting != 'None':
            ratio_minimum = setting.data['min_leverage']
            ratio_maximum = setting.data['max_leverage']
            if ratio_minimum is not None:
                if ratio < ratio_minimum:
                    ratio = ratio_minimum
            if ratio_maximum is not None:
                if ratio > ratio_maximum:
                    ratio = ratio_maximum
        AddOrderView.margin_call(user)
        if cash // quote.price >= 1:
            amount = cash // quote.price
            try:
                broker = LeverageData.objects.get(user=user, stock=stock)
                order = Order.objects.get(user=user, stock=stock, type=type, price=quote.price, is_closed=False)
                order.amount = amount
                broker.ratio = ratio
            except LeverageData.DoesNotExist:
                broker = LeverageData(user=user, stock=stock, ratio=ratio)
                order = Order(user=user, stock=stock, type=type, price=quote.price, is_closed=False, amount=amount, count=amount)
            order.save()
            broker.save()
            return HttpResponseRedirect("/api/v1/orders/")
        else:
            context = {
                'too_low': 1,
                'form': form,
            }
            return render(request, 'trading/leverage.html', context)


class ProfileBalanceAdd(APIView):
    """
    Пополнение баланса пользователя
    """

    def get(self, request):
        """
        Отображение формы для пополнения баланса пользователя при GET запросе

        На вход подаётся только токен пользователя.
        """
        context = {}
        form = UserBalance()
        context['form'] = form
        return render(request, 'profile/balance_add.html', context)

    def post(self, request):
        """
        Пополение баланса пользователя и обработка данных при POST запросе

        На вход принимается токен и количество тугриков, на которое пользователь хочет пополнить баланс: `money`.
        """
        form = UserBalance(request.POST)
        user = User.objects.get(id=request.user.pk)
        if form.is_valid():
            context = {'form': form}
            money = request.POST['money']
            try:
                user.balance = float(money.replace(',', '.', 1)) + float(user.balance)
                user.save()
                return render(request, 'profile/balance_add_successfully.html', context)
            except ValueError:
                return render(request, 'profile/balance_add_failed.html')
        return render(request, 'profile/balance_add_failed.html')


class PricesView(APIView):
    """
    Страница с текущими и предыдущими котировками акций
    """
    def get(self, request):
        """
        Отображение всех котировок акций при GET запросе

        Котировки генерируются ботом.
        Сначала идут исторические данные, позже котировки акций генерируются по разным формулам.
        Для генерации по таблице на эмуляторе биржи SHP.EXchange есть папка с файлами с расширением csv. Именно оттуда берутся исторические данные о котировках акций.
        При генерации по формулам сперва рандомно выбирается тенденция: возрастающая или убывающая. Потом случайно определяется количество фигур. С небольшой вероятностью в эти фигуры подмешиваются противоположные. В случае, если посреди генерации по таблице вмешивается какая-либо настройка, то после этого генерация продолжается уже по формулам. Также во время генерации по таблице с некоторой вероятностью может случиться так называемая катастрофа, при которой цены акций начинают резко падать. Пример такой катастрофы - кризис.

        На вход не принимается никаких параметров.
        """
        prices = Quotes.objects.all()
        serializer = serializers.PriceSerializer(prices, many=True)
        return Response(serializer.data)
