from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework import filters
from main.forms import ProfileEditingForm, PasswordEditingForm, AddOrderForm, LeverageTradingForm
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Stocks, Order, Portfolio, User, UserSettings, Quotes, LeverageData
from main import serializers

from django.shortcuts import get_object_or_404


class AddOrderView(APIView):
    """
    Добавление ордера

    :param price: Цена ордера
    :param stock: Имя акции
    :param type: Тип ордера
    """
    def get(self, request):
        form = AddOrderForm(initial={
                'price': 0,
                'stock': '',
                'type': 0,
                'amount': 0,
            })
        context = {
            'form': form,
        }
        return render(request, 'orders/add_order.html', context)

    @staticmethod
    def margin_call(user):
        try:
            user_data = LeverageData.objects.get(user=user)
            if user.balance <= 0:
                for object in Order.objects.filter(user=user, stock=user_data.stock):
                    object.is_closed = True
                    object.save()
        except:
            pass

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
        user = request.user
        name = request.POST.get('stock')
        stock = Stocks.objects.get(name=name)
        type = True if request.POST.get('type') else False
        price = float(request.POST.get('price'))
        amount = int(request.POST.get('amount'))
        order = Order(user=user, stock=stock, type=type, price=price, is_closed=False, amount=amount)
        try:
            p_u = Portfolio.objects.get(user=user, stock=stock)
            if type == 1:
                p_u.count += amount
                p_u.save()
        except Portfolio.DoesNotExist:
            if type == 1:
                p_u = Portfolio(user=user, stock=stock, count=amount)
            else:
                p_u = Portfolio(user=user, stock=stock, count=0)
            self.set_percentage(p_u)
        order.save()
        self.margin_call(user)
        if Order.objects.filter(type=not type, price=price, is_closed=False, stock=stock):
            order_rev = Order.objects.all().filter(type=not type, price=price, is_closed=False, stock=stock)
            for order_obj in order_rev:
                user_op = get_object_or_404(User, pk=order_obj.user_id)
                if user != user_op:

                    try:
                        p_up = Portfolio.objects.get(user=user_op, stock=stock)
                    except Portfolio.DoesNotExist:
                        p_up = Portfolio(user=user_op, stock=stock, count=0)
                        # покупка - 0; продажа - 1
                    if order.is_closed == False:
                        if type == 0:
                            if amount == order_obj.amount:
                                user.balance -= price * amount
                                user_op.balance += price * amount
                                p_u.count += amount
                                p_up.count -= amount
                                order.is_closed = True
                                order_obj.is_closed = True
                            elif amount < order_obj.amount:
                                user.balance -= price * amount
                                user_op.balance += price * amount
                                p_u.count += amount
                                p_up.count -= amount
                                order.is_closed = True
                                order_obj.amount -= amount
                                order.order_id = order_obj.pk
                            elif amount > order_obj.amount:
                                user.balance -= price * order_obj.amount
                                user_op.balance += price * order_obj.amount
                                p_u.count += order_obj.amount
                                p_up.count -= order_obj.amount
                                order_obj.is_closed = True
                                order.amount -= order_obj.amount
                                order_obj.order_id = order.pk
                        elif type == 1:
                            if amount == order_obj.amount:
                                user.balance += price * amount
                                user_op.balance -= price * amount
                                p_u.count -= amount
                                p_up.count += amount
                                order.is_closed = True
                                order_obj.is_closed = True
                            elif amount < order_obj.amount:
                                user.balance += price * amount
                                user_op.balance -= price * amount
                                p_u.count -= amount
                                p_up.count += amount
                                order.is_closed = True
                                order_obj.amount -= order.amount
                                order.order_id = order_obj.pk
                            elif amount > order_obj.amount:
                                user.balance += price * order_obj.amount
                                user_op.balance -= price * order_obj.amount
                                p_u.count -= order_obj.amount
                                p_up.count += order_obj.amount
                                order_obj.is_closed = True
                                order.amount -= order_obj.amount
                                order_obj.order_id = order.pk
                    self.margin_call(user)
                    self.margin_call(user_op)
                    self.set_percentage(p_up)
                    self.set_percentage(p_u)
                    order_obj.save()
                    p_u.save()
                    p_up.save()
                    order.save()
                    user.save()
                    user_op.save()
        return HttpResponseRedirect("/api/v1/orders/")


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
    def get(self, request):
        user = request.user
        user_avatar = UserSettings.objects.get(user_id=user.id)
        return Response(
            {
                'profile': serializers.ProfileDetailSerializer(user).data,
                'avatar': serializers.ProfileUserAvatarSerializer(user_avatar).data,
            }
        )


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
        portfolio = Portfolio.objects.filter(user_id=request.user.id)
        serializer = serializers.PortfolioUserSerializer(portfolio, many=True)
        return Response(serializer.data)


class ProfileEditingView(APIView):
    """
        Профиль пользователя

        :param username: Никнейм пользователя
        :param first.name: Имя пользователя
        :param last.name: Фамилия пользователя
        :param user.email: Почта пользователя
        :param user_avatar: Аватарка пользователя
    """
    def get(self, request):
        user = User.objects.get(id=request.user.pk)
        user_avatar = UserSettings.objects.get(user_id=user.id).avatar
        form = ProfileEditingForm(
            initial={
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'avatar': user_avatar,
            }
        )
        context = {
            'form': form,
        }
        return render(request, 'profile/profile_editing.html', context)

    def post(self, request):
        form = ProfileEditingForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(id=request.user.pk)
            user.username = form.data['username']
            user.first_name = form.data['first_name']
            user.last_name = form.data['last_name']
            user.email = form.data['email']
            user.save()
            if request.FILES:
                user_avatar = UserSettings.objects.get(user_id=user.id)
                user_avatar.avatar = request.FILES['avatar']
                user_avatar.save()
            return HttpResponseRedirect("/api/v1/profile/")
        else:
            return HttpResponseRedirect("/profile/editing/")


class PasswordEditingView(APIView):
    """
    Страница восстановления пароля
    """
    def get(self, request):
        form = PasswordEditingForm()
        context = {
            'form': form,
        }
        return render(request, 'profile/password_editing.html', context)

    def post(self, request):
        form = PasswordEditingForm(request.POST)
        if form.is_valid():
            context = {
                'form': form,
                'is_old_password_wrong': True,
                'is_new_password_wrong': True,
                'is_repeat_password_wrong': True,
            }
            user = User.objects.get(id=request.user.pk)
            password = form.data['old_password']
            if user.check_password(password):
                new_password = form.data['new_password']
                repeat_new_password = form.data['repeat_new_password']
                context['is_old_password_wrong'] = False
                if new_password == repeat_new_password:
                    context['is_repeat_password_wrong'] = False
                    if len(new_password) > 7 and len(repeat_new_password) > 7:
                        context['is_new_password_wrong'] = False
                        user.set_password(new_password)
                        user.save()
                        return HttpResponseRedirect("api/v1/profile/")
            return render(request, 'profile/password_editing.', context)
        else:
            return HttpResponseRedirect("profile/editing/change_password/")

class LeverageTradingView(APIView):
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
    def get(self, request):
        return render(request, 'profile/balance_add.html')

    def post(self, request):
        user = User.objects.get(id=request.user.pk)
        if 'money' in request.POST:
            money = request.POST['money']
            if int(money) > 0:
                user.balance = int(money) + float(user.balance)
                user.save()
                return render(request, 'profile/balance_add_successfully.html')
        return render(request, 'profile/balance_add_failed.html')


class PricesView(APIView):
    def get(self, request):
        prices = Quotes.objects.all()
        serializer = serializers.PriceSerializer(prices, many=True)
        return Response(serializer.data)
