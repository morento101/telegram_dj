from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


    # def __init__(self, *args, **kwargs):
    #     super(LoginForm, self).__init__(*args, **kwargs)

    # def clean(self, *args, **kwargs):
    #     username = self.cleaned_data.get('username')
    #     user = User.objects.filter(username=username).exists()
    #     if not user:
    #         messages.error(self.request, 'User with such username does not exist')
    #         return redirect('login')
    #     password = self.cleaned_data.get('password')
    #     end_pass = User.objects.get(username=username).password
    #     check = check_password(password, end_pass)
    #     if not check:
    #         messages.error(self.request, 'Password is incorrect')
    #         return redirect('login')
    #     return self.cleaned_data

    # def clean_username(self, *args, **kwargs):
    #     username = self.cleaned_data.get('username')
    #     user = User.objects.filter(username=username).exists()
    #     if not user:
    #         messages.error(self.request, 'User with such username does not exist')
    #     return username
    #
    # def clean_password(self, *args, **kwargs):
    #     password = self.cleaned_data.get('password')
    #     username = self.cleaned_data.get('username')
    #     user = User.objects.get(username=username)
    #     if user:
    #     end_pass = User.objects.get(username=username).password
    #     check = check_password(password, end_pass)
    #     if not check:
    #         messages.error(self.request, 'Password is incorrect')
    #     return password
