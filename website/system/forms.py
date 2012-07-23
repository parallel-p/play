from django import forms
from django.contrib.admin.widgets import AdminFileWidget

from .models import Game, Bot


class GameForm(forms.ModelForm):
    image = forms.FileField(widget=AdminFileWidget)
    source = forms.FileField(widget=AdminFileWidget)

    class Meta:
        model = Game
        fields = ('name', 'image', 'description', 'source')


class BotForm(forms.ModelForm):
    source = forms.FileField(widget=AdminFileWidget)

    class Meta:
        model = Bot
        fields = ('name', 'game', 'source')
