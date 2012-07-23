from django.contrib import admin
from .models import Game, Bot


admin.site.register(Game,
    list_display=('name', 'author')
)
admin.site.register(Bot)
