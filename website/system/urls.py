from django.conf.urls import patterns, include, url


urlpatterns = patterns('system.views',
    url(r'^games/$', 'games_list', name='games_list'),
    url(r'^games/add/$', 'game_add', name='game_add'),
    url(r'^games/(?P<game_pk>\d+)/$', 'game', name='game'),
    url(r'^games/(?P<game_pk>\d+)/bots/add/$', 'bot_add', name='bot_add'),
)