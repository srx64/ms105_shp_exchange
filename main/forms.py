from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django_registration.forms import RegistrationForm
from main.models import User


class CustomRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User


class ProfileEditingForm(forms.Form):
    username = forms.CharField(
        label='Редактировать имя пользователя:',
        max_length=150,
        required=True,
    )
    first_name = forms.CharField(label='Редактировать имя:', max_length=150, required=False)
    last_name = forms.CharField(label='Редактировать фамилию:', max_length=150, required=False)
    email = forms.EmailField(label='Редактировать email:', required=True)
    avatar = forms.ImageField(
        label='Редактировать аватар:',
        required=False,
        widget=forms.FileInput(
            attrs={'image': forms.FileInput,
                   'upload_to': 'avatars',
                   }
        )
    )


class PasswordEditingForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Старый пароль'}
        ),
        label='Введите старый пароль:',
        required=True,
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Новый пароль'}
        ),
        label='Введите новый пароль:',
        required=True,
    )
    repeat_new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Повторите новый пароль'}
        ),
        label='Повторите новый пароль:',
        required=True,
    )


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not get_user_model().objects.filter(email__iexact=email, is_active=True).exists():
            msg = "Такого адреса электронной почты не существует"
            self.add_error('email', msg)
        return email

class AddOfferForm(forms.Form):
    price = forms.FloatField(
        label='Цена',
        required=True,
    )
    stock = forms.CharField(label='Акция', max_length=150)
    type = forms.BooleanField(label='Купить(0)/Продать(1)', required=False)
