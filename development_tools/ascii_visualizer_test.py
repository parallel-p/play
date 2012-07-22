import unittest
from unittest.mock import Mock, patch
config_mock = Mock(name='config')
my_ascii_painter = Mock()
config_mock.AsciiPainter = Mock(return_value=my_ascii_painter)
my_ascii_painter.ascii_paint = Mock(side_effect=lambda x: '''
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXX This is a sample game field XXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXX Frame: ''' + str(x) + ''' XXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
''')
with patch.dict('sys.modules', config=config_mock):
    from development_tools.ascii_visualizer import AsciiVisualizer

    class AsciiVisualizerTestCase(unittest.TestCase):
        def test_ui(self):
            ''' It is testing of UI, so we can't do assertions or something
            like this here, just to look ourselves if everything is OK. '''
            game_controller = Mock()
            game_controller.jury_states = list(range(10))
            viz = AsciiVisualizer(game_controller)
            viz.activate()

    if __name__ == "__main__":
        unittest.main()
