from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext_lazy as _

from .models import Game, Bot

import os


class ExtFileField(forms.FileField):

    def __init__(self, *args, **kwargs):
        ext_whitelist = kwargs.pop("ext_whitelist")
        self.ext_whitelist = [i.lower() for i in ext_whitelist]

        super(ExtFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ExtFileField, self).clean(*args, **kwargs)
        filename = data.name
        ext = os.path.splitext(filename)[1]
        ext = ext.lower()
        if ext not in self.ext_whitelist:
            raise forms.ValidationError(_(u'Not allowed filetype'))
        return data


class GameForm(forms.ModelForm):
    image = forms.FileField(widget=AdminFileWidget, required=False)
    source = ExtFileField(widget=AdminFileWidget,
                          ext_whitelist=['.zip'])

    class Meta:
        model = Game
        fields = ('name', 'name_latin', 'image', 'description', 'source')


class BotForm(forms.ModelForm):
    source = ExtFileField(widget=AdminFileWidget,
                          ext_whitelist=['.pas', '.cpp', '.py'])

    class Meta:
        model = Bot
        fields = ('name', 'source')
