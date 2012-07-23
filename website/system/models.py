from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField(_(u'name'), max_length=255)
    image = models.ImageField(_(u'image'), upload_to='games/images',
                              null=True, blank=True)
    author = models.ForeignKey(User, verbose_name=_(u'author name'),
                                    null=True, blank=True)
    source = models.FileField(_(u'source'), upload_to='games')
    description = models.TextField(_(u'description'))
    verified = models.BooleanField(_(u'verified'), default=False)

    class Meta:
        verbose_name = _(u'game')
        verbose_name_plural = _(u'games')
        unique_together = ('name', )
        ordering = ('name', )

    def __unicode__(self):
        return self.name


class Bot(models.Model):
    name = models.CharField(_(u'name'), max_length=255)
    author = models.ForeignKey(User, verbose_name=_(u'author name'),
                                    null=True, blank=True)
    game = models.ForeignKey(Game, verbose_name=_(u'game'))
    source = models.FileField(_('source'), upload_to='bots')

    class Meta:
        verbose_name = _(u'bot')
        verbose_name_plural = _(u'bots')
        unique_together = ('game', 'name')
        ordering = ('name', )

    def __unicode__(self):
        return self.name
