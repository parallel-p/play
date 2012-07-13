import unittest
from player import Player


class PlayerTest(unittest.TestCase):

    def test_player(self):
        player = Player('python3 bot143.py', 'VasyaPupkin', 'SuperMegaKiller')
        assert_equal(player.author_name, 'VasyaPupkin')
        assert_equal(player.bot_name, 'SuperMegaKiller')
        assert_equal(player.command_line, 'python3 bot143.py')

if __name__=='__main__':
    unittest.main()
