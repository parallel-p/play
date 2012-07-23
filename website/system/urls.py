from django.conf.urls import patterns, include, url


urlpatterns = patterns('system.views',
    url(r'^games/add/$', 'game_add', name='game_add'),
    url(r'^bots/add/$', 'bot_add', name='bot_add'),
)