from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'required': True}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'required': True}))
    email = forms.CharField(
        widget=forms.TextInput(attrs={'required': True}))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def __str__(self) -> str:
        return self.email


class UpdateUserForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
