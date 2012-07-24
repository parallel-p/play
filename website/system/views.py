from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from .models import Bot, Game
from .forms import GameForm, BotForm


def games_list(request):
    qs = Game.objects.filter(verified=True)
    return render(request, 'games_list.html', {'object_list': qs})


def game(request, game_pk):
    obj = get_object_or_404(Game, pk=game_pk)
    return render(request, 'game.html', {'object': obj})


@login_required
def bot_add(request, game_pk):
    _game = get_object_or_404(Game, pk=game_pk)
    if request.method == 'POST':
        form = BotForm(request.POST, request.FILES)
        if form.is_valid():
            bot = form.save()
            bot.author = request.user
            bot.game = _game
            bot.save()
            return redirect(game, _game.pk)
    else:
        form = BotForm()
    return render(request, 'bot_add.html', {'game': _game, 'form': form})


@login_required
def game_add(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save()
            game.author = request.user
            game.save()
            return redirect(games_list)
    else:
        form = GameForm()
    return render(request, 'game_add.html', {'form': form})
