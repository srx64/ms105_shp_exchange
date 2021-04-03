from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework import filters
from django.utils import timezone
from main.forms import ProfileEditingForm, PasswordEditingForm, AddOrderForm
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Stocks, Order, Portfolio, User, UserSettings
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

    def post(self, request):
        user = request.user
        name = request.POST.get('stock')
        stock = Stocks.objects.get(name=name)
        type = True if request.POST.get('type') else False
        price = float(request.POST.get('price'))
        amount = int(request.POST.get('amount'))
        portfolio, created = Portfolio.objects.get_or_create(user=user, stock=stock)
        order = Order(user=user, stock=stock, type=type, price=price, is_closed=False, amount=amount)
        order_ops = Order.objects.filter(stock=stock, type=not type, price=price, is_closed=False)
        for order_op in order_ops:
            if order.amount != 0:
                user_op = order_op.user
                portfolio_op = Portfolio.objects.get(user=user_op, stock=stock)

                min_count = min(order.amount, order_op.amount) if type == 0 else -min(order.amount, order_op.amount)

                order.amount -= abs(min_count)
                order_op.amount -= abs(min_count)

                if portfolio.count > 0:
                    user_op.balance += min_count * price
                    user.balance -= min_count * price

                portfolio.count += min_count
                portfolio_op.count -= min_count

                if portfolio.count < 0:
                    user.short_balance -= portfolio.count * price
                    user.balance += (min_count + portfolio.count) * price
                    user.is_debt = True

                if portfolio.count >= 0 and user.is_debt:

                    user.balance += 100000+user.short_balance
                    user.short_balance = -100000
                    user.is_debt = False

                if order_op.amount == 0:
                    order_op.is_closed = True
                    order_op.date_closed = timezone.now()

                user_op.save()
                order_op.save()
                portfolio_op.save()

            if order.amount == 0:
                order.is_closed = True
                order.date_closed = timezone.now()

        user.save()
        portfolio.save()
        order.save()
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
