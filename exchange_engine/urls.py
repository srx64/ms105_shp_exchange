"""exchange_engine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from main import views
from django.urls import path, include
from django_registration.backends.one_step.views import RegistrationView
from main.forms import CustomRegistrationForm, EmailValidationOnForgotPassword
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from main.views import StocksListView, StockDetailView, StatisticsView, OrdersView, PortfolioUserView, \
    ProfileDetailView, PricesView, registration_view, CandlesView, SettingsView, CryptocurrenciesView, \
    ProfileAnotherView, StatisticsBalanceView

from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

schema_view = get_schema_view(
    openapi.Info(
        title='SHP.EXchange API',
        default_version='v1',
        description='Биржа. Просто биржа. Для проведения летней смены курса "Финансовые технологии"',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="dasha.mishkina117@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),
    path('api-token/', TokenObtainPairView.as_view(), name='api_token'),
    path('api-token-refresh/', TokenRefreshView.as_view()),
    path('api/v1/balance_statistics/', StatisticsBalanceView.as_view(), name='balance_statistics'),
    path('api/v1/stocks/', StocksListView.as_view(), name='stocks'),
    path('api/v1/stocks/<int:pk>/', StockDetailView.as_view(), name='stock'),
    path('api/v1/candles/<int:pk>/<int:c_type>', CandlesView.as_view(), name='candles'),
    path('api/v1/statistics/', StatisticsView.as_view(), name='statistics'),
    path('api/v1/register/', registration_view, name='reg'),
    path('api/v1/orders/', OrdersView.as_view(), name='orders'),
    path('trading/leverage/', views.LeverageTradingView.as_view(), name='leverage_trading'),
    path('api/v1/portfolio/', PortfolioUserView.as_view(), name='portfolio'),
    path('api/v1/settings/', SettingsView.as_view(), name='settings'),
    path('api/v1/cryptocurrencies/', CryptocurrenciesView.as_view(), name='cryptocurrencies'),
    path('api/v1/profile/', ProfileDetailView.as_view(), name='profile'),
    path('api/v1/profile/<int:pk>/', ProfileAnotherView.as_view(), name='another_profile'),
    path('orders/add', views.AddOrderView.as_view(), name='add_order'),
    path('api/v1/prices/', PricesView.as_view(), name='prices'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/',
         RegistrationView.as_view(
             form_class=CustomRegistrationForm
         ),
         name='django_registration_register',
         ),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='password/password_reset.html',
        form_class=EmailValidationOnForgotPassword
    ), name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
         name='password_reset_complete'),
    path('profile/balance_add', login_required(views.ProfileBalanceAdd.as_view()), name='balance_add'),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
