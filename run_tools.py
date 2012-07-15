import argparse
import config_helpers
import sys


def get_js():
    import generator
    from tournament_stages.game_signature import GameSignature
    import pickle

    gen = generator.Generator()
    signature = GameSignature(1, 1, 1, 1)
    return gen.generate_start_positions(signature, 2)

def create_players(cmd1, cmd2):
    import player

    player1 = player.Player(cmd1)
    player2 = player.Player(cmd2)
    return player1, player2

def play(args):
    import config
    from game_simulator import GameSimulator
    from tournament_stages.game_signature import GameSignature

    players = create_players(args.bot1, args.bot2)
    signature = GameSignature(1, 1, 1, 1)
    jury_state = next(get_js())
    game = GameSimulator(players, jury_state, signature)
    game_controller = game.play()
    return game_controller

def visuzlize(game_controller):
    import development_tools.ascii_visualizer as vizualizer
    ascii_viz = vizualizer.AsciiVisualizer(game_controller)
    ascii_viz.activate()

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('bot1')
    arg_parser.add_argument('bot2')
    arg_parser.add_argument('-d', '--directory', default='.')
    args = arg_parser.parse_args()
    config_helpers.initialize_game_environment(args.directory)

    game_controller = play(args)
    visuzlize(game_controller)

if __name__ == '__main__':
    main()
