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
from main import views
from django.urls import path, include
from django_registration.backends.one_step.views import RegistrationView
from main.forms import CustomRegistrationForm, EmailValidationOnForgotPassword
from django.contrib.auth import views as auth_views
from main.views import StocksListView, StockDetailView, OffersView, PortfolioUserView, ProfileDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shares_list/', OffersView.as_view()),
    path('stocks/', StocksListView.as_view()),
    path('stock/<int:pk>/', StockDetailView.as_view()),
    path('offers/', OffersView.as_view()),
    path('portfolio/<int:pk>', PortfolioUserView.as_view()),
    path('profile/', ProfileDetailView.as_view()),
    path('login/', views.LoginView.as_view(), name='login'),
    path('accounts/register/',
         RegistrationView.as_view(
             form_class=CustomRegistrationForm
         ),
         name='django_registration_register',
         ),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password/password_reset.html',
                                                                 form_class=EmailValidationOnForgotPassword),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
         name='password_reset_complete'),

]
