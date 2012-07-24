from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import os
import shutil
from zipfile import ZipFile


class BotQuerySet(QuerySet):

    def delete(self):
        for obj in self.all():
            obj.delete()


class BotManager(models.Manager):

    def get_query_set(self):
        return BotQuerySet(self.model, using=self._db)

    def delete(self):
        self.get_query_set().delete()


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
    objects = BotManager()

    class Meta:
        verbose_name = _(u'bot')
        verbose_name_plural = _(u'bots')
        #unique_together = ('game', 'name')
        ordering = ('name', )

    def __unicode__(self):
        return self.name

    def delete(self, *args, **kwargs):
        source_name = os.path.basename(self.source.path)
        game = self.game
        path = os.path.dirname(__file__)
        bots_dir_path = os.path.abspath(os.path.join(
                                        path, '..', '..', 'games',
                                        game.name_latin, 'bots'))
        bot_path = os.path.join(bots_dir_path, source_name)
        try:
            os.remove(bot_path)  # remove bot from bots
        except:
            pass

        new_lines = []
        author = self.author.username
        players_files_path = os.path.abspath(os.path.join(bots_dir_path, '..',
                                             'players_files'))
        #print players_files_path
        with open(players_files_path, 'r') as players_files:
            lines = players_files.readlines()
        for line in lines:
            line1 = line[1:len(line) - 2].split('\" \"')
            if line1[0] != author:
                new_lines.append(line)
        with open(players_files_path, 'w') as players_files:
            players_files.writelines(new_lines)
        super(Bot, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(Bot, self).save(*args, **kwargs)
        path = os.path.dirname(__file__)
        source_path = self.source.path
        source_name = os.path.basename(source_path)
        game = self.game
        author = self.author
        objects = Bot.objects.filter(game=game, author=author)
        for obj in objects:
            if obj.pk != self.pk:
                obj.delete()
        bots_dir_path = os.path.abspath(os.path.join(path, '..', '..', 'games',
                                        game.name_latin, 'bots'))
        shutil.copy(source_path, bots_dir_path)
        players_files_path = os.path.abspath(os.path.join(bots_dir_path, '..',
                                             'players_files'))
        players_path = os.path.join('games', game.name_latin, 'bots',
                                    source_name)
        with open(players_files_path, 'a') as players_files:
            players_files.write('\"{}\" \"{}\" \"{}\"\n'.format(
                                author.username, self.name, players_path))
