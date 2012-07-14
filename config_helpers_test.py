import unittest
import config_helpers
import imp
import os
import player


class TestConfigHelpers(unittest.TestCase):
    def setUp(self):
        os.chdir('..')
        conf_file = open('config.py', 'w')
        conf_file.write('some_value = 0\n')
        conf_file.close()

    def test_initialize_game_environment(self):
        config_helpers.initialize_game_environment('config.py')
        import config
        self.assertEqual(config.some_value, 0)


class TestPlayersParse(unittest.TestCase):

    def test_write_logs(self):
        test_logs = open('test_for_players_parse', 'w')
        test_logs.write("""


"Author Authorovich" "MegaBot" "/home/artur/bot_path"
Author Bot "/usr/lol"
Author "Bot and bot" /usr/lol
Author "Bot and bot'   '/usr/lol"
"Author and co"   Bot /usr/lol
"Author and co" Bot     "/usr/lol"
"Author and co"      'Bot' /usr/lol
Author   Bot     /usr/lol
  '   '   a   '   '  

  
     """)
        test_logs.close()
        gotten_list = config_helpers.players_parse('test_for_players_parse')
        answer_list = list()
        answer_list.append(player.Player('/home/artur/bot_path', 'Author Authorovich', 'MegaBot'))
        answer_list.append(player.Player('/usr/lol', 'Author', 'Bot'))
        answer_list.append(player.Player('/usr/lol', 'Author', 'Bot and bot'))
        answer_list.append(player.Player('/usr/lol', 'Author', 'Bot and bot'))
        answer_list.append(player.Player('/usr/lol', 'Author and co', 'Bot'))
        answer_list.append(player.Player('/usr/lol', 'Author and co', 'Bot'))
        answer_list.append(player.Player('/usr/lol', 'Author and co', 'Bot'))
        answer_list.append(player.Player('/usr/lol', 'Author', 'Bot'))
        answer_list.append(player.Player('   ', '   ', 'a'))
        for i in range(9):
            self.assertEqual(answer_list[i].bot_name, gotten_list[i].bot_name)
            self.assertEqual(answer_list[i].author_name, gotten_list[i].author_name)
            self.assertEqual(answer_list[i].command_line, gotten_list[i].command_line)
        os.remove('test_for_players_parse')
        

if __name__ == '__main__':
    unittest.main()
