from django import forms
from django.contrib.auth import get_user_model
from django_registration.forms import RegistrationForm
from main.models import User

class CustomRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User

