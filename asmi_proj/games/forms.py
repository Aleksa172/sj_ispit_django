from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Game

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['name']

class RegisterForm(ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ["username", "password"]

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u'Username "%s" is already in use.' % username)