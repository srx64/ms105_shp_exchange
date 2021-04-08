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
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from main import views
from django.urls import path, include
from django_registration.backends.one_step.views import RegistrationView
from main.forms import CustomRegistrationForm, EmailValidationOnForgotPassword
from django.contrib.auth import views as auth_views
from main.views import StocksListView, StockDetailView, OrdersView, PortfolioUserView, ProfileDetailView, PricesView
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token/', TokenObtainPairView.as_view()),
    path('api-token-refresh/', TokenRefreshView.as_view()),
    path('api/v1/stocks/', StocksListView.as_view(), name='stocks'),
    path('api/v1/stock/<int:pk>/', StockDetailView.as_view(), name='stock'),
    path('api/v1/orders/', OrdersView.as_view(), name='orders'),
    path('trading/leverage/', views.LeverageTradingView.as_view(), name='add_order'),
    path('api/v1/portfolio/', PortfolioUserView.as_view(), name='portfolio'),
    path('api/v1/profile/', ProfileDetailView.as_view(), name='profile'),
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
    path('profile/editing/', login_required(views.ProfileEditingView.as_view()), name='profile_editing'),
    path('profile/editing/change_password/', login_required(views.PasswordEditingView.as_view()), name='change_password'),
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
    path('profile/balance_add', login_required(views.ProfileBalanceAdd.as_view()))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
