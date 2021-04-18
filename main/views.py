from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework import filters, status
from main.forms import AddOrderForm, LeverageTradingForm, UserBalance
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Stocks, Order, Portfolio, User, UserSettings, Quotes, LeverageData
from main import serializers

from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = serializers.RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "succefully"
            data['email'] = account.email
            data['username'] = account.username
            us_settings = UserSettings(user_id=account)
            us_settings.save()
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
        if LeverageData.objects.filter(user=user):
            user_data = LeverageData.objects.get(user=user)
            if user.balance <= 0:
                for object in Order.objects.filter(user=user, stock=user_data.stock):
                    object.is_closed = True
                    object.save()

    @staticmethod
    def set_percentage(user_portfolio):
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
        data = request.data
        user = request.user
        name = data['stock']
        stock = Stocks.objects.get(name=name)
        type = data['type']
        price = float(data['price'])
        amount = int(data['amount'])
        if price <= 0 or amount <= 0:
            return Response({"detail": "uncorrect data"}, status=status.HTTP_400_BAD_REQUEST)
        self.margin_call(user)
        portfolio, created = Portfolio.objects.get_or_create(user=user, stock=stock)
        self.set_percentage(portfolio)
        order = Order(user=user, stock=stock, type=type, price=price, is_closed=False, amount=amount)
        order_ops = Order.objects.filter(stock=stock, type=not type, price=price, is_closed=False)
        for order_op in order_ops:
            if order.amount != 0:
                user_op = order_op.user
                portfolio_op = Portfolio.objects.get(user=user_op, stock=stock)

                min_count = min(order.amount, order_op.amount) if type == 0 else -min(order.amount, order_op.amount)

                order.amount -= abs(min_count)
                order_op.amount -= abs(min_count)

                portfolio.count += min_count
                portfolio_op.count -= min_count

                user_op.balance += min_count * price
                user.balance -= min_count * price

                if portfolio.count < 0:
                    portfolio.short_balance -= min_count * price
                    user.balance += min_count * price
                    portfolio.is_debt = True

                if portfolio_op.count < 0:
                    portfolio_op.short_balance += min_count * price
                    user_op.balance -= min_count * price
                    portfolio_op.is_debt = True

                if portfolio.count == 0 and portfolio.is_debt:
                    user.balance += 100000+user.short_balance
                    portfolio.short_balance = -100000
                    portfolio.is_debt = False

                if portfolio_op.count == 0 and portfolio_op.is_debt:
                    user.balance += 100000+user.short_balance
                    portfolio_op.short_balance = -100000
                    portfolio_op.is_debt = False

                if order_op.amount == 0:
                    order_op.is_closed = True
                    order_op.date_closed = timezone.now()

                self.margin_call(user)
                self.margin_call(user_op)
                self.set_percentage(portfolio)
                self.set_percentage(portfolio_op)

                user_op.save()
                order_op.save()
                portfolio_op.save()

            if order.amount == 0:
                order.is_closed = True
                order.date_closed = timezone.now()

        user.save()
        portfolio.save()
        order.save()
        return Response("/api/v1/orders/")


class StocksListView(ListAPIView):
    """
    Список акций
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
        stock = Stocks.objects.get(id=pk)
        serializer = serializers.StockDetailSerializer(stock)
        return Response(serializer.data)


class ProfileDetailView(APIView):
    """
        Информация о пользователе

        :param profile: Профиль
        :param avatar: Аватарка пользователя
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user_avatar = UserSettings.objects.get(user_id=user.id)
        return Response(
            {
                'profile': serializers.ProfileDetailSerializer(user).data,
                'avatar': serializers.ProfileUserAvatarSerializer(user_avatar).data,
            }
        )

    def patch(self, request):
        user = request.user
        data = request.data

        user.email = data.get("email", user.email)
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        password2 = data.get("password2", user.password)
        if password2:
            if user.check_password(data.get("password", user.password)):
                user.set_password(password2)
            else:
                return Response({"detail": "password must match"}, status=status.HTTP_400_BAD_REQUEST)

        if request.FILES:
            user_settings = UserSettings.objects.get(user_id=user)
            user_settings.avatar = request.FILES['file']
            user_settings.save()

        user.save()
        serializer = serializers.ProfileDetailSerializer(user)

        return Response(serializer.data)


class OrdersView(APIView):
    """
    Все заявки
    """

    def get(self, request):
        orders = Order.objects.filter(is_closed=False)
        serializer = serializers.OrdersSerializer(orders, many=True)
        return Response(serializer.data)


class PortfolioUserView(APIView):
    """
    Портфолио пользователя
    """

    def get(self, request):
        portfolio = Portfolio.objects.filter(~Q(count=0), user_id=request.user.id,)
        serializer = serializers.PortfolioUserSerializer(portfolio, many=True)
        return Response(serializer.data)


class LeverageTradingView(APIView):
    """
    Торговля с плечом
    """

    def get(self, request):
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
        form = LeverageTradingForm(request.POST)

        user = User.objects.get(id=request.user.pk)
        ratio = int(request.POST.get('ratio'))
        stock = Stocks.objects.get(name=request.POST.get('stock'))
        quote = Quotes.objects.filter(stock=stock.id).last()
        type = True if request.POST.get('type') else False
        cash = user.balance * ratio
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
                order = Order(user=user, stock=stock, type=type, price=quote.price, is_closed=False, amount=amount)
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
        context = {}
        form = UserBalance()
        context['form'] = form
        return render(request, 'profile/balance_add.html', context)

    def post(self, request):
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
        prices = Quotes.objects.all()
        serializer = serializers.PriceSerializer(prices, many=True)
        return Response(serializer.data)
