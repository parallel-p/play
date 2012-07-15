class Player:
    def __init__(self, cmd_line, author='John Doe', bot='Some_bot'):
        self.author_name = author
        self.bot_name = bot
        self.command_line = cmd_line

    def __repr__(self):
        return '{0}, {1}'.format(self.author_name, self.bot_name)
