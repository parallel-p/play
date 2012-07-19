import bot_compiler
import shutil

def main():
    '''
    Creates tournament from all the bots that listed in players_config
    '''
    compiler = bot_compiler.BotCompiler()
    players_config = open('games/pepelac/players_files', 'r')
    bot = players_config.readline().split('"')
    bots = []
    while bot != ['']:
        bots.append((bot[1], bot[3], bot[5]))
        bot = players_config.readline().split('"')
    compiler.compile(bots)
    shutil.copyfile('config.ini', 'games/pepelac/players_config')

if __name__ == "__main__":
    main()