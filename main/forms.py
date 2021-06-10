from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django_registration.forms import RegistrationForm
from main.models import User


class CustomRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not get_user_model().objects.filter(email__iexact=email, is_active=True).exists():
            msg = "Такого адреса электронной почты не существует"
            self.add_error('email', msg)
        return email


class AddOrderForm(forms.Form):
    price = forms.FloatField(
        label='Цена',
        required=True,
    )
    amount = forms.FloatField(
        label='Количество',
        required=True,
    )
    stock = forms.CharField(label='Акция', max_length=150)
    type = forms.BooleanField(label='Купить(0)/Продать(1)', required=False)


class UserBalance(forms.Form):
    money = forms.CharField(label='Деньги', max_length=150)


class LeverageTradingForm(forms.Form):
    ratio = forms.IntegerField(
        label='1 к',
        required=True,
        min_value=1,
    )
    stock = forms.CharField(
        label='Название акции',
        required=True,
        max_length=150,
    )
    type = forms.BooleanField(label='Купить(0)/Продать(1)', required=False)
