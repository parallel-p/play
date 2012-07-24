import unittest
from unittest.mock import Mock, patch
from lib.colorama import Fore, Back, Style
from io import BytesIO, StringIO


def make_sample_frame(x):
    return '''
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
'''


config_mock = Mock(name='config')
my_ascii_painter = Mock()
my_ascii_painter.ascii_paint = Mock(side_effect=make_sample_frame)
config_mock.AsciiPainter = Mock(return_value=my_ascii_painter)


with patch.dict('sys.modules', config=config_mock):
    import development_tools.ascii_visualizer as vis_module

    class AsciiVisualizerTestCase(unittest.TestCase):
        def test__clear_nt(self):
            vis_module.name = 'nt'
            vis_module.system = Mock()
            vis_module._clear()
            vis_module.system.assert_called_once_with('cls')

        def test__clear_posix(self):
            vis_module.name = 'posix'
            vis_module.system = Mock()
            vis_module._clear()
            vis_module.system.assert_called_once_with('clear')

        def test__clear_raise(self):
            vis_module.name = 'ololo'
            vis_module.system = Mock()
            with self.assertRaises(Exception):
                vis_module._clear()

        def setUp(self):
            self.game_controller = Mock()
            self.game_controller.jury_states = list(range(10))
            self.vis_object = vis_module.AsciiVisualizer(self.game_controller)

        def test_creation(self):
            self.assertEqual(
                self.vis_object.game_controller, self.game_controller)
            self.assertEqual(
                self.vis_object.painter_factory, config_mock.AsciiPainter)

        def test__jury_state_count(self):
            self.assertEqual(self.vis_object._jury_state_count(), 10)

        def test__help(self):
            for i, name in enumerate(['posix', 'nt']):
                vis_module.name = name
                vis_module._clear = Mock()
                vis_module.print = Mock(name='Print mock')
                self.vis_object._help()
                vis_module._clear.assert_any_call()
                pos = lambda x: '\x1b[{};{}H'.format(x, x)
                vis_module.print.assert_called_once_with(pos(i),
                    '''{brt}{bl}Navigation help:
          ____     ____  ____  ____
         |{gr}HOME{bl}|   |{gr}PgUp{bl}||{gr} Up {bl}||{gr}PgDn{bl}|
         |{mg}1st {bl}|   |{mg}RW5%{bl}||{mg}auto{bl}||{mg}FF5%{bl}|
          ____     ____  ____  ____
         |{gr}END {bl}|   |{gr}Left{bl}||{gr}Down{bl}||{gr}Rght{bl}|
         |{mg}last{bl}|   |{mg}prev{bl}||{mg}jump{bl}||{mg}next{bl}|

        forward         : {gr}RIGHT,N,SPACE,ENTER{bl}   (Alt: {gr}>,],+{bl})
        back            : {gr}LEFT,B,\{bl}              (Alt: {gr}<,[,-{bl})
        jump to frame   : {gr}DOWN,J,G,all numerals{bl} (Alt: {gr}F,R{bl}  )
        autoplay        : {gr}UP,A,M,P{bl}
        stop            : {gr}^C{bl}

        quit            : {gr}Q,E{bl}

        display this message : {gr}any other key{norm}
        '''.format(
            gr=Fore.GREEN, bl=Fore.BLUE, mg=Fore.MAGENTA,
            brt=Style.BRIGHT, norm=Style.NORMAL) + Fore.RESET)

        def test__error(self):
            vis_module.print = Mock()
            self.vis_object._error('We have big problems!!!')
            vis_module.print.assert_called_once_with(
                Fore.RED + Style.BRIGHT + 'We have big problems!!!' +\
                Style.NORMAL + Fore.RESET, end='\n')


        def test__prompt(self):
            self.vis_object.frame_number = 0
            self.vis_object.lock = Mock()
            self.vis_object.lock.acquire = Mock()
            self.vis_object.lock.release = Mock()
            vis_module.clear_string = Mock()
            vis_module.print = Mock()
            vis_module.input = Mock(return_value='user answer')
            vis_module._clear = Mock()
            self.vis_object._print_frame = Mock()
            self.vis_object._help = Mock()

            retval = self.vis_object._prompt('Write!')

            self.vis_object.lock.acquire.assert_called_once_with()
            vis_module.print.assert_called_once_with(
                Fore.YELLOW + Style.BRIGHT +\
                'Write!', end=' : ' + Style.NORMAL + Fore.RESET)
            vis_module.input.assert_called_once_with()
            self.vis_object.lock.release.assert_called_once_with()
            self.vis_object._print_frame.assert_called_once_with(0)
            self.assertEqual(retval, 'user answer')

        def test__detect_arrow_posix(self):
            vis_module.name = 'posix'
            mydict = {
                '[A' : 'A',
                '[B' : 'B',
                '[C' : 'C',
                '[D' : 'D',
                '[5~' : 'U',
                '[6~' : 'N'
                }
            for arrow in mydict.keys():
                vis_module.getch = Mock(side_effect=iter(arrow))
                a = self.vis_object._detect_arrow('\x1b')
                self.assertEqual(a, mydict[arrow])

        def test__detect_arrow_nt(self):
            vis_module.name = 'nt'
            windict = {
                b'H': 'A',
                b'P': 'B',
                b'M': 'C',
                b'K': 'D',
                b'G': 'H',
                b'O': 'E',
                b'I': 'U',
                b'Q': 'N'
                }
            for arrow in windict.keys():
                vis_module.getch = Mock(return_value=arrow)
                self.assertEqual(
                    self.vis_object._detect_arrow(b'\xe0'), windict[arrow])

        def test__detect_arrow_wrong(self):
            self.assertIsNone(self.vis_object._detect_arrow('dsfsf'))

        def test__print_frame(self):
            self.vis_object.lock = Mock()
            self.vis_object.lock.acquire = Mock()
            self.vis_object.lock.release = Mock()
            self.vis_object.frame_number = 0
            vis_module.print = Mock()
            vis_module._clear = Mock()

            self.vis_object._print_frame(0)

            self.vis_object.lock.acquire.assert_called_once_with()
            vis_module._clear.assert_called_once_with()
            text = '{color}Frame #0001 of 10 :{nocolor}\n{0:s}\n'.format(
                    make_sample_frame(0), color=Fore.YELLOW +\
                    Style.BRIGHT, nocolor=Fore.RESET + Style.NORMAL)
            vis_module.print.assert_called_once_with('\n\r'.join(text.split('\n')))
            self.vis_object.lock.release.assert_called_once_with()
            self.assertEqual(
                self.vis_object.prev_frame, (
                    '\n\r'.join(text.split('\n'))).split('\n'))

        def test__print_frame_diff(self):
            for i, name in enumerate(['posix', 'nt']):
                vis_module.name = name
                self.vis_object.frame_number = 1
                text = '{color}Frame #0001 of 10 :{nocolor}\n{0:s}\n'.format(
                    make_sample_frame(0), color=Fore.YELLOW +\
                    Style.BRIGHT, nocolor=Fore.RESET + Style.NORMAL)
                old_splitted = text.split('\n')
                self.vis_object.prev_frame = text.split('\n')
                newtext = ('{color}Frame #0002 of 10 ' +\
                    ':{nocolor}\n{0:s}\n').format(
                        make_sample_frame(1), color=Fore.YELLOW +\
                        Style.BRIGHT, nocolor=Fore.RESET +\
                        Style.NORMAL)
                splitted = newtext.split('\n')
                vis_module.print = Mock()
                self.vis_object._print_frame_diff(1)
                for line in range(len(splitted)):
                    if old_splitted[line] is None or (
                            old_splitted[line] != splitted[line]):
                        vis_module.print.assert_any_call(
                            '\x1b[{};{}H'.format(
                                line + 1, i), splitted[line], sep='')
                vis_module.print.assert_any_call('\x1b[{};{}H'.format(
                    (len(splitted) + i), i), ' ' * 98, chr(13), sep='', end='')


        def test__read_key_posix(self):
            vis_module.name = 'posix'
            for i in 'ampqebjgJGBAMPQE':
                vis_module.getch = Mock(return_value=i)
                self.vis_object._detect_arrow = Mock(return_value=None)
                self.assertEqual(self.vis_object._read_key(), (i, None))
                self.vis_object._detect_arrow.assert_called_once_with(i)

        def test__read_key_nt(self):
            vis_module.name = 'nt'
            for i in [b'a', b'm', b'q', b'Q', b'E', b'e', b'A', b'M']:
                vis_module.getch = Mock(return_value=i)
                self.vis_object._detect_arrow = Mock(return_value=None)
                self.assertEqual(self.vis_object._read_key(), (
                    i.decode(), None))
                self.vis_object._detect_arrow.assert_called_once_with(i)

        def test_auto(self):
            def set_frame_num(d):
                self.vis_object.frame_number = d
            self.vis_object.frame_number
            self.vis_object.stop = False
            self.vis_object._print_frame_diff = Mock(
                side_effect=set_frame_num)
            vis_module.sleep = Mock()
            self.vis_object.auto(+1, 10, 100, 50, '')
            self.assertEqual(self.vis_object.frame_number, 50)
            self.vis_object.auto(+1, 10, 100, 110, '')
            self.assertEqual(self.vis_object.frame_number, 99)
            for i in range(1, 100, 1):
                self.vis_object._print_frame_diff.assert_any_call(i)

        def test_dump(self):
            my_log = StringIO()
            check = ''
            for i in range(10):
                check += 'Frame #{}:\n{}\n'.format(i, make_sample_frame(i))
            self.vis_object.dump(my_log)
            self.assertEqual(my_log.getvalue(), check)


    if __name__ == "__main__":
        unittest.main()
