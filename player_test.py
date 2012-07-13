import unittest
from player import Player


class PlayerTest(unittest.TestCase):

    def test_player(self):
        player = Player('python3 bot143.py', 'VasyaPupkin', 'SuperMegaKiller')
        self.assertEqual(player.author_name, 'VasyaPupkin')
        self.assertEqual(player.bot_name, 'SuperMegaKiller')
        self.assertEqual(player.command_line, 'python3 bot143.py')

if __name__=='__main__':
    unittest.main()
