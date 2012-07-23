from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


admin.autodiscover()


urlpatterns = patterns('',
   url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'auth/login.html'},
        name='login',
    ),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'auth/logout.html'},
        name='logout'
    ),
    url(r'^registration/$', 'auth.views.registration', name='registration'),
    url(r'^', include('system.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
