from django import forms
from .models import Word
from django.contrib.auth.models import User


class WordInputForm(forms.ModelForm):
    class Meta:
        model = Word
        exclude = ("user",)
        fields = [
            "polish_word",
            "spanish_word",
            "etymology",
            "notes",
        ]


