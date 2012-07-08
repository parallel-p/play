# -*- coding: utf-8 -*-
from hashlib import md5

class Player:
    def __init__(self,filename,author_name,bot_name):
        self.name=bot_name
        self.author_name=author_name
        self.file_name=filename
        self.player_id=md5((bot_name+author_name).encode('utf8')).hexdigest()
