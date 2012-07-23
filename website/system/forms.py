from django import forms
from django.contrib.admin.widgets import AdminFileWidget

from .models import Game, Bot


class GameForm(forms.ModelForm):
    source = forms.FileField(widget=AdminFileWidget)

    class Meta:
        model = Game


class BotForm(forms.ModelForm):
    source = forms.FileField(widget=AdminFileWidget)

    class Meta:
        model = Bot
