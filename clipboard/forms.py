from django import forms
from .models import Word, UserAccount
from django.contrib.auth.models import User

class WordInputForm(forms.ModelForm):
    class Meta:
        model=Word
        exclude=('user',)
        fields=[
            'polish_word','spanish_word', 'etymology',
            'notes',
        ]

class UserAccountForm(forms.ModelForm):
    class Meta:
        model=UserAccount
        exclude=('user',)
        fields=[
            'profile_picture',
        ]