import subprocess
import sys
import os


class BotCompiler():
    ''' Compiles players for current game.
    Usage:
    >>> compiler = BotCompiler().
    >>> config_filename = compiler.compile(players)
    Players should be a list of tuples, which should have an author name,
    bot name and file name. config_filename, returned by compile() should
    have an config filename, which should be used in players_parse()
    '''
    def __init__(self):
        pass

    def define_compiler(self, filename, extension):
        ''' Determines compiler by file extension. Supports:
        C++ (.cpp, .c++, .cxx)
        FreePascal (.pas)
        Python (.py) '''
        # TODO: Will we add C?
        if extension == 'cpp' or extension == 'c++' or (
                extension == 'cxx'):
            compiler_string = ['g++', '-o', filename]
        elif extension == 'pas':
            compiler_string = ['fpc']
        elif extension == 'py':
            compiler_string = []
            # TODO: Will we add Python 2?
        else:
            raise Exception('Language of this file is not supported')
        return compiler_string

    def define_execfile(self, filename, extension):
        ''' Determines execution command for compiled file.
        Supports c++, Pascal and Python. '''
        operating_system = sys.platform
        if extension == 'py':
            if operating_system.startswith('win'):
                execfile_string = 'python ' + filename + '.py'
            else:
                execfile_string = 'python3 ' + filename + '.py'
        else:
            if extension == 'cpp' or extension == 'c++' or (
                    extension == 'cxx'):
                execfile_string = os.path.join('.', filename)
            elif extension == 'pas':
                execfile_string = os.path.join('.', filename)
            else:
                raise Exception('Language of this file is not supported')
            if operating_system.startswith('win'):
                execfile_string += '.exe'
        return execfile_string

    def _compile_file(self, file_name):
        ''' Automatically selects compiler and starts
        compilation process for given file. Raises exception if
        compiler didn't terminate with 0 code. '''
        filename, extension = file_name.split('.')
        compiler_string = self.define_compiler(filename, extension)
        compiler_string.append(file_name)
        if len(compiler_string) >= 2:
            try:
                return_code = subprocess.call(compiler_string)
            except FileNotFoundError:
                raise Exception('Compiler for file ' + filename +
                    ' not found. Play requires g++, fpc and python.')
        else:
            return_code = 0
        if return_code == 0:
            compile_string = self.define_execfile(filename, extension)
            return compile_string
        else:
            raise Exception('Compilation Error: compiler exit code '
                + str(int(return_code)))

    def compile(self, players, players_config_file):
        ''' Compilates all bot source codes for each player and writes
        ``author's name`` ``name of the bot`` ``execution command`` string
        to file ``config.ini`` '''
        config_file = open(players_config_file, 'w')
        for player in players:
            author_name = player[0]
            bot_name = player[1]
            file_name = player[2]
            compile_string = self._compile_file(file_name)
            if compile_string is not None:
                config_file.writelines(['\'{}\' \'{}\' \'{}\'\n'.format(
                    author_name, bot_name, compile_string)])
        config_file.close()
