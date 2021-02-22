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
from main.forms import CustomRegistrationForm
from main.views import StocksListView, StockDetailView, OffersView, PortfolioUserView, ProfileDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shares_list/', OffersView.as_view()),
    path('stocks/', StocksListView.as_view()),
    path('stock/<int:pk>/', StockDetailView.as_view()),
    path('offers/', OffersView.as_view()),
    path('portfolio/<int:pk>', PortfolioUserView.as_view()),
    path('profile/', login_required(ProfileDetailView.as_view())),
    path('login/', views.LoginView.as_view(), name='login'),
    path('accounts/register/',
         RegistrationView.as_view(
             form_class=CustomRegistrationForm
         ),
         name='django_registration_register',
         ),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('profile/editing/', login_required(views.ProfileEditingView.as_view()), name='profile_editing'),
    path('profile/editing/change_password/', login_required(views.PasswordEditingView.as_view()), name='change_password')
]
