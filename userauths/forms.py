from django import  forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter a username"}))
    email = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter an email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Enter a password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm your password"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # widgets = {
        #     "username": forms.TextInput(attrs={"placeholder":"Enter a username"}),
        #     "email": forms.TextInput(attrs={"placeholder":"Enter an email"}),
        #     "password1": forms.PasswordInput(attrs={"placeholder":"Enter a password"}),
        #     "password2": forms.PasswordInput(attrs={"placeholder":"Confirm your password"}),
        # }