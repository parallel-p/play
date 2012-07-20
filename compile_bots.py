import bot_compiler
import os


def run_app():
    game_path = input("Enter path for your game: ")
    try:
        input_file = open(game_path + 'players_files', 'r')
    except FileNotFoundError:
        print("ERROR: File not found.")
        exit(1)
    try:
        os.remove(game_path + 'players_config')
    except:
        pass
    compiler = bot_compiler.BotCompiler()
    bots = input_file.readlines()
    players = []
    for bot in bots:
        s = bot.split('\"')
        players.append([s[1], s[3], s[5]])
    compiler.compile(players, game_path + 'players_config')
    print("File with commands saved in " + game_path + "players_config.")

if __name__ == '__main__':
    run_app()
