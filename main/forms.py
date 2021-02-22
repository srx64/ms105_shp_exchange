from django import forms
from django.contrib.auth import get_user_model
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
    avatar = forms.URLField(label='Редактировать аватар:', required=False)


class PasswordEditingForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Старый пароль'}
        ),
        required=True,
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Новый пароль'}
        ),
        required=True,
    )
    repeat_new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Повторите новый пароль'}
        ),
        required=True,
    )
