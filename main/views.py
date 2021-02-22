from main.models import Stocks, Offers, Portfolio, User, UserSettings

from django.conf import settings

from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login as auth_login
)
from django.contrib.auth.forms import (
    AuthenticationForm
)
from django.contrib.auth.views import SuccessURLAllowedHostsMixin

from django.contrib.sites.shortcuts import get_current_site

from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url, render

from django.utils.decorators import method_decorator
from django.utils.http import (
    url_has_allowed_host_and_scheme
)

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from django.views.generic.edit import FormView
from main.forms import ProfileEditingForm, PasswordEditingForm
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Stocks, Offers, Portfolio, User
from main import serializers


class LoginView(SuccessURLAllowedHostsMixin, FormView):
    """
    Display the login form and handle the login action.
    """
    form_class = AuthenticationForm
    authentication_form = None
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'registration/login.html'
    redirect_authenticated_user = False
    extra_context = None

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_redirect_url(),
            'site': current_site,
            'site_name': current_site.name,
            **(self.extra_context or {})
        })
        return context


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
        user = User.objects.get(id=request.user.pk)
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
    def get(self, request, pk):
        portfolio = Portfolio.objects.filter(user_id=pk)
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
        form = ProfileEditingForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.pk)
            user_avatar = UserSettings.objects.get(user_id=user.id)
            user.username = form.data['username']
            user.first_name = form.data['first_name']
            user.last_name = form.data['last_name']
            user.email = form.data['email']
            user_avatar.avatar = form.data['avatar']
            user.save()
            user_avatar.save()
            return HttpResponseRedirect("/profile/")
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
                        return HttpResponseRedirect("/profile/")
            return render(request, 'profile/password_editing.html', context)
        else:
            return HttpResponseRedirect("profile/editing/change_password/")
