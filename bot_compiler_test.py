import bot_compiler
import subprocess
import unittest
import os

HelloWorld = [
['cpp',
'''
#include <iostream>
 
int main()
{
    std::cout << "Hello, world!" << std::endl;
    return 0;
}
'''],
['pas',
'''
program MyProgram;
begin
 WriteLn ('Hello, world!');
end.
'''],
['py',
'''
print("Hello, world!")
''']
]


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
        j = 1
        for extension, program in HelloWorld:
            f = open("hello" + str(j) + "." + extension, 'w')
            for line in program:
                f.writelines([line])
            f.close()
            j = j + 1

    def tearDown(self):
        os.remove("hello1.cpp")
        os.remove("hello1")
        os.remove("hello2.pas")
        os.remove("hello2")
        os.remove("hello3.py")

    def test_compile(self):
        bot_c = bot_compiler.BotCompiler()
        bot_c.compile(players)
        f = open('config.ini', 'r')
        bots = f.readlines()
        for bot in bots:
            command_line = bot.split('\"')[5]
            print(os.path.abspath(os.curdir))
            process = subprocess.Popen(command_line, shell=True,
                cwd = os.path.abspath(os.curdir),
                stdout = subprocess.PIPE)
            out = process.stdout.read()
            process.kill()
            self.assertEqual(out, b'Hello, world!\n')

if __name__ == '__main__':
    unittest.main()