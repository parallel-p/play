import psutil
import subprocess


class BotCompiler():
    ''' Compiles players for current game.
    Usage:
    >>> compiler = BotCompiler().
    >>> config_filename = compiler.compile(players)
    Players should be a list of turples, which should have an author name,
    bot name and file name. config_filename, returned by compile() should
    have an config filename, which should be used in players_parse()
    '''
    def __init__(self):
        pass

    def define_compiler(self, filename, extension):
            if extension == "cpp":
                compiler_string = ["g++", "-o", filename]
            elif extension == "pas":
                compiler_string = ["fpc"]
            elif extension == "py":
                compiler_string = ["python", "-O"]
            else:
                raise Exception("Language of this file is not supported")
            return compiler_string

    def define_execfile(self, filename, extension):
            if extension == "cpp":
                execfile_string = "./" + filename
            elif extension == "pas":
                execfile_string = "./" + filename
            elif extension == "py":
                execfile_string = "python3 " + filename
            else:
                raise Exception("Language of this file is not supported")
            return execfile_string

    def _compile_file(self, file_name):
        filename, extension = file_name.split(".")
        compiler_string = self.define_compiler(filename, extension)
        compiler_string.append(file_name)
        return_code = subprocess.call(compiler_string)
        if return_code == 0:
            compile_string = self.define_execfile(filename, extension)
            return compile_string
        else:
            raise Exception("Compilation Error: compiler returned code "
                + str(int(return_code)))

    def compile(self, players):
        config_file = open('config.ini', 'w')
        for player in players:
            author_name = player[0]
            bot_name = player[1]
            file_name = player[2]
            compile_string = self._compile_file(file_name)
            if compile_string != None:
                config_file.writelines(['\"{}\" \"{}\" \"{}\"\n'.format(
                    author_name, bot_name, compile_string)])
