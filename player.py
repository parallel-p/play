class Player:
    def __init__(self, cmd_line, author='John Doe', bot='Some bot'):
        self.author_name = author
        self.bot_name = bot
        self.command_line = cmd_line

    def __str__(self):
        return '{}, {}'.format(self.author_name, self.bot_name)

    def __repr__(self):
        return '<{}>'.format(self.__str__())

    def _as_tuple(self):
        return (self.author_name, self.bot_name, self.command_line)

    def __lt__(self, other):
        return self._as_tuple() < other._as_tuple()

    def __eq__(self, other):
        return self._as_tuple() == other._as_tuple()
