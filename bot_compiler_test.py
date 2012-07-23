import bot_compiler
import subprocess
import unittest
import os

player_command_file = 'ololo'

HelloWorld = [
    ['cpp', '''
#include <iostream>

int main()
{
    std::cout << "Hello, world!";
    return 0;
}
'''], ['pas', '''
program MyProgram;

begin
 Write ('Hello, world!');
end.
'''], ['py', '''
print('Hello, world!', end='')
''']]


config = [
"John Smith" "HelloC" "hello1",
"John Smith" "HelloPas" "hello2",
"John Smith" "HelloPython" "hello3"
]

players = [
["John Smith", "HelloC", "hello1.cpp"],
["John Smith", "HelloPas", "hello2.pas"],
["John Smith", "HelloPython", "hello3.py"]
]


class BotCompilerTest(unittest.TestCase):
    def setUp(self):
        ''' Creates source code files to compile '''
        j = 1
        for extension, program in HelloWorld:
            f = open('hello{}.{}'.format(str(j), extension), 'w')
            for line in program:
                f.writelines([line])
            f.close()
            j = j + 1

    def tearDown(self):
        ''' Removes source code files from disk '''
        os.remove('hello1.cpp')
        if os.name == 'nt':
            os.remove('hello1.exe')
        else:
            os.remove('hello1')
        os.remove('hello2.pas')
        os.remove('hello2.o')
        if os.name == 'nt':
            os.remove('hello2.exe')
        else:
            os.remove('hello2')
        os.remove('hello3.py')
        os.remove('ololo')

    def test_compile(self):
        bot_c = bot_compiler.BotCompiler()
        bot_c.compile(players, player_command_file)
        f = open(player_command_file, 'r')
        bots = f.readlines()
        f.close()
        for bot in bots:
            command_line = bot.split("\'")[5]
            process = subprocess.Popen(command_line, shell=True,
                cwd=os.path.abspath(os.curdir),
                stdout=subprocess.PIPE)
            out = process.stdout.read()
            process.kill()
            self.assertEqual(out, b'Hello, world!')

if __name__ == '__main__':
    unittest.main()
