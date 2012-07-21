# This test checks drawing frames using example.nim painter.
# P.S. If you think I misunderstood the meaning of integration test,
# please explain it to me.

import sys
import pickle


def main():
    import config_helpers
    config_helpers.initialize_game_environment(sys.argv[1])
    from main import Main
    from development_tools.frame_visualizer import FrameVisualizer


    file = open(sys.argv[2], mode='rb')
    test_game_controller = pickle.load(file)
    file.close()
    FrameVisualizer(test_game_controller).mainloop()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python log_viewer.py <game directory> <log file>')
        exit()
    main()
