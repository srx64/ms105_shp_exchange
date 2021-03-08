from django.http import HttpResponseRedirect
from django.shortcuts import render
from main.forms import ProfileEditingForm, PasswordEditingForm, AddOfferForm
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Stocks, Offers, Portfolio, User, UserSettings
from main import serializers

from django.shortcuts import get_object_or_404


class AddOfferView(APIView):
    def get(self, request):
        form = AddOfferForm(initial={
                'price': 0,
                'stock': '',
                'type': 0,
            })
        context = {
            'form': form,
        }
        return render(request, 'offers/add_offer.html', context)

    def post(self, request):
        user = request.user
        name = request.POST.get('stock')
        stock = Stocks.objects.get(name=name)
        type = True if request.POST.get('type') else False
        price = float(request.POST.get('price'))
        offer = Offers(user=user, stock=stock, type=type, price=price, is_closed=False)
        offer.save()
        if Offers.objects.filter(type=not type, price=price, is_closed=False, stock=stock):
            offer_rev = Offers.objects.get(type=not type, price=price, is_closed=False, stock=stock)
            user_op = get_object_or_404(User, pk=offer_rev.user_id)
            p_u = Portfolio.objects.get(user=user, stock=stock)
            p_up = Portfolio.objects.get(user=user_op, stock=stock)
            if type == 0:
                user.balance -= price
                user_op.balance += price
                if Portfolio.objects.filter(user=user, stock=stock):
                    p_u.count += 1 #count
                if Portfolio.objects.filter(user=user_op, stock=stock):
                    p_up.count -= 1 #count
            elif type == 1:
                user.balance += price
                user_op.balance -= price
                if Portfolio.objects.filter(user=user, stock=stock):
                    p_u.count -= 1 #count
                if Portfolio.objects.filter(user=user_op, stock=stock):
                    p_up.count += 1 #count
            offer.is_closed = True
            offer_rev.is_closed = True
            p_u.save()
            p_up.save()
            offer.save()
            offer_rev.save()
            user.save()
            user_op.save()
        return HttpResponseRedirect("/apiv1/offers/")


class StocksListView(APIView):
    """Список акций"""
    def get(self, request):
        stocks = Stocks.objects.filter(is_active=True)
        serializer = serializers.StocksSerializer(stocks, many=True)
        return Response(serializer.data)


class StockDetailView(APIView):
    """Информация об акции"""
    def get(self, request, pk):
        stock = Stocks.objects.get(id=pk)
        serializer = serializers.StockDetailSerializer(stock)
        return Response(serializer.data)


class ProfileDetailView(APIView):
    """Информация о пользователе"""
    def get(self, request):
        user = request.user
        user_avatar = UserSettings.objects.get(user_id=user.id)
        return Response(
            {
                'profile': serializers.ProfileDetailSerializer(user).data,
                'avatar': serializers.ProfileUserAvatarSerializer(user_avatar).data,
            }
        )


class OffersView(APIView):
    """Все заявки"""
    def get(self, request):
        offers = Offers.objects.filter(is_closed=False)
        serializer = serializers.OffersSerializer(offers, many=True)
        return Response(serializer.data)


class PortfolioUserView(APIView):
    """Портфолио пользователя"""
    def get(self, request):
        portfolio = Portfolio.objects.filter(user_id=request.user.id)
        serializer = serializers.PortfolioUserSerializer(portfolio, many=True)
        return Response(serializer.data)


class ProfileEditingView(APIView):
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
            return render(request, 'profile/password_editing.html', context)
        else:
            return HttpResponseRedirect("profile/editing/change_password/")
