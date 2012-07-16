class Player:
    def __init__(self, cmd_line, author='John Doe', bot='Some_bot'):
        self.author_name = author
        self.bot_name = bot
        self.command_line = cmd_line

    def __str__(self):
        return '{0}, {1}'.format(self.author_name, self.bot_name)

    def __repr__(self):
        return '<{0}>'.format(self.__str__())

    def __lt__(self, other):
        return (self.author_name, self.bot_name) < (other.author_name, other.bot_name)
