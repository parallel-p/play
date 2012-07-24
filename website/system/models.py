from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import os
import shutil
from zipfile import ZipFile


class Game(models.Model):
    name = models.CharField(_(u'name'), max_length=255)
    name_latin = models.CharField(_(u'name on latin'), max_length=255)
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

    def save(self, *args, **kwargs):
        '''
        pk = self.pk
        try:
            obj = get_object_or_404(Game, pk=pk)
        else:
            obj = self
        if self.verified and (not obj.verified or
                              obj.source.path != self.source.path):
            file_dir = os.path.dirname(__file__)
            game_name = os.path.basename(obj.source.path).split('.', 1)[0]
            extract_dir = os.path.join(file_dir, '..', '..', 'games',
                                       game_name)
            extract_dir = os.path.abspath(extract_dir)
            print extract_dir
            if os.path.exists(extract_dir):
                shutil.rmtree(extract_dir)
            try:
                with ZipFile(self.source.path, 'r') as archive:
                    archive.extractall(extract_dir)
            except:
                pass
        '''
        super(Game, self).save(*args, **kwargs)


class Bot(models.Model):
    name = models.CharField(_(u'name'), max_length=255)
    author = models.ForeignKey(User, verbose_name=_(u'author name'),
                               null=True, blank=True)
    game = models.ForeignKey(Game, verbose_name=_(u'game'),
                             blank=True, null=True)
    source = models.FileField(_('source'), upload_to='bots')

    class Meta:
        verbose_name = _(u'bot')
        verbose_name_plural = _(u'bots')
        unique_together = ('game', 'name')
        ordering = ('name', )

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        '''
        try:
            obj = get_object_or_404(Bot, pk=pk)
        except:
            obj = self
        bots = Bot.objects.filter(author=obj.author, game=obj.game)
        cur_dir = os.path.dirname(__file__)
        game = obj.game
        if game:
            bots_dir = os.path.abspath(os.path.join(cur_dir, '..', '..',
                                       'games', game.name, 'bots'))
        else:
            bots_dir = None
        bot = bots[0]
        author = bot.author
        if bot.pk != obj.pk:
            os.remove(bot.source.path)
            name = os.path.basename(bot.source.path)
            if bots_dir:
                bot.delete()
        if game:
            shutil.copy(obj.source.path, bots_dir)
            new_lines = []
            if game:
                with open(os.path.join(bots_dir, '..',
                          'players_files'), 'r') as config:
                    lines = config.readlines()
                    for line in lines:
                        line1 = line[1:len(line) - 1]
                        line1 = line1.split('\" \"')
                        if not line1[0] == author:
                            new_lines.append(line)
                with open(os.path.join(bots_dir, '..',
                          'players_files'), 'w') as config:
                    config.writelines(new_lines)
                    bot_path = os.path.join('games', game.name, 'bots',
                                            os.path.basename(obj.source.path))
                    config.write('\"{}\" \"{}\" \"{}\"\n'.format(
                                 obj.author.username,
                                 obj.name,
                                 bot_path))
        '''
        super(Bot, self).save(*args, **kwargs)
