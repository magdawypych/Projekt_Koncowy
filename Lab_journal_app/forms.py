from django import forms
from django.contrib.auth.models import User
from .models import Position


class AddUserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Hasło')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Powtórz hasło')
    position = forms.ChoiceField(choices=Position.POSITIONS, widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'position']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



