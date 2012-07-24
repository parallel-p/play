import threading
import time
from subprocess import PIPE, Popen
from log import logger
import config
import copy


MEGABYTE = 1 << 20


class ExecuteError(OSError):
    '''
    This exception is raised when create_process
    cannot start bot process (e.g. invalid command)
    '''
    def __init__(self):
        OSError.__init__(self, 'can\'t start bot process')


class ProcessNotRunningException(OSError):
    '''
    This exception is raised after trying to
    send command to process that is not running.
    '''
    def __init__(self):
        OSError.__init__(self, 'process isn\'t running')


class TimeLimitException(OSError):
    '''
    This exception is raised when bot's process exceeded time limit.
    '''
    def __init__(self):
        OSError.__init__(self, 'time limit exceeded')


class BaseBot:
    '''
    This class wraps bot's process and stores its information.

    Examples:
        >>> from move import Move
        >>> from player_state import PlayerState # import *your* classes
        >>> p = BaseBot('python bot.py')
        >>> p.create_process()fixes
        >>> state = PlayerState(...)
        >>> move = Move(...)
        >>> p.get_move(state, serialize, deserialize)
        <move.Move object at ...>
        >>> p.kill_process()
    '''
    def __init__(self, player_command):
        '''
        Constructor for class Bot.
        `player_command` is a string which is used to invoke bot program.
        '''
        self._player_command = player_command
        self._process = None
        self._count_of_moves = 0

    def create_process(self):
        '''
        Starts bot's process.
        '''
        logger.info('executing \'%s\'', self._player_command)
        try:
            self._process = psutil.Popen(
                self._player_command.split(),
                stdout=PIPE,
                stdin=PIPE,
                # stderr=PIPE
            )
        except OSError:
            logger.critical('executing of \'%s\' failed: invalid command',
                            self._player_command)
            raise ExecuteError

        logger.info('executing successful')

    def _get_real_time(self):
        '''
        Returns real time used by bot's process.
        '''
        return time.time()

    def get_move(self, player_state, serialize, deserialize):
        '''
        Serialize player_state and transfer it to bot,
        then deserialize output received from bot to `move`.

        `player_state` - object, which will be passed to
        the bot after serialization.

        `serialize(player_state, writable_stream)` is a function,
        which is responsible for serializing `player_state` and
        writing it to `writable_stream`.

        `deserialize(readable_stream)` is a function, which is
        responsible for reading data from `readable_stream` and turning it
        to a valid `move` object.

        If bot's process isn't running, raise ProcessNotRunningException.
        '''

        if self._process is None:
            raise ProcessNotRunningException()

        real_time = self._get_real_time()
        self._get_move_exception = None

        get_move_thread = threading.Thread(
            target=self._get_move,
            args=(player_state, serialize, deserialize)
        )
        get_move_thread.start()

        if self._count_of_moves % config.time_limit_count_of_moves == 0:
            self._real_time_remainder = 0
        self._count_of_moves += 1
        real_time_start = self._get_real_time()

        try:
            while get_move_thread.is_alive():
                real_time = self._get_real_time()

                if real_time - real_time_start + self._real_time_remainder\
                        > config.real_time_limit_seconds:
                    self.kill_process()
                    logger.error('bot with cmd \'%s\' exceeded time limit',
                                 self._player_command)
                    raise TimeLimitException

                if hasattr(config, 'observe_period'):
                    time.sleep(config.observe_period)
        finally:
            self._real_time_remainder += real_time - real_time_start

        if self._get_move_exception:
            logger.error('exception has been raised during '
                         'interaction with bot')
            raise self._get_move_exception

        logger.debug('elapsed real time: %f sec',
                     self._get_real_time() - real_time)
        return self._deserialize_result

    def _get_move(self, player_state, serialize, deserialize):
        '''
        Serialize player_state with bot's `stdin`.
        `stdin` is a stream opened to write per *byte*.

        Deserialize move with bot's `stdout`.
        `stdout` is a stream opened to read per *byte*.
        Invokes author's deserialization function and
        stores received `move` into self._deserialize_result.

        If anyone raised an exception, this method stores
        information about exception for re-raising.
        '''
        try:
            serialize(player_state, self._process.stdin)
            self._deserialize_result = deserialize(self._process.stdout)
        except Exception as e:
            self._get_move_exception = e

    def kill_process(self):
        '''
        Kills bot's process if it is running or does nothing
        if the process was already killed.
        '''
        if self._process is not None:
            try:
                self._process.kill()
                self._process.communicate()
            except OSError:
                pass
        logger.info('process with cmd line \'%s\' was killed',
                    self._player_command)

    def __del__(self):
        '''
        Destructor for class bot.
        It automatically kills bot's process on delete.
        '''
        self.kill_process()


class ComplexBot(BaseBot):
    '''
    This class wraps bot's process and stores its information.

    Examples:
        >>> from move import Move
        >>> from player_state import PlayerState # import *your* classes
        >>> p = BaseBot('python bot.py')
        >>> p.create_process()
        >>> state = PlayerState(...)
        >>> move = Move(...)
        >>> p.get_move(state, serialize, deserialize)
        <move.Move object at ...>
        >>> p.kill_process()
    '''

    def create_process(self):
        '''
        Starts bot's process.
        '''
        import psutil
        logger.info('executing \'%s\'', self._player_command)
        try:
            self._process = psutil.Popen(
                self._player_command.split(),
                stdout=PIPE,
                stdin=PIPE,
                # stderr=PIPE
            )
        except OSError as e:
            logger.critical('executing of \'%s\' failed: invalid command',
                            self._player_command)
            raise ExecuteError

        logger.info('executing successful')

    def _get_cpu_time(self):
        '''
        Returns CPU time used by bot's process.
        '''
        times = self._process.get_cpu_times()
        return times.system + times.user

    def _get_memory(self):
        '''
        Returns memory used by process in *megabytes*.
        '''
        return self._process.get_memory_info().rss / MEGABYTE

    def get_move(self, player_state, serialize, deserialize):
        '''
        Serialize player_state and transfer it to bot,
        then deserialize output received from bot to `move`.

        `player_state` - object, which will be passed to
        the bot after serialization.

        `serialize(player_state, writable_stream)` is a function,
        which is responsible for serializing `player_state` and
        writing it to `writable_stream`.

        `deserialize(readable_stream)` is a function, which is
        responsible for reading data from `readable_stream` and turning it
        to a valid `move` object.

        If bot's process isn't running, raise ProcessNotRunningException.
        '''
        import psutil

        if self._process is None:
            raise ProcessNotRunningException()

        try:
            real_time = self._get_real_time()
            cpu_time = self._get_cpu_time()
            self._get_move_exception = None

            get_move_thread = threading.Thread(
                target=self._get_move,
                args=(player_state, serialize, deserialize)
            )
            get_move_thread.start()

            if self._count_of_moves % config.time_limit_count_of_moves == 0:
                self._real_time_remainder = 0
                self._cpu_time_remainder = 0
            self._count_of_moves += 1
            real_time_start = self._get_real_time()
            cpu_time_start = self._get_cpu_time()

            try:
                while get_move_thread.is_alive():
                    real_time = self._get_real_time()
                    cpu_time = self._get_cpu_time()

                    real_executing_time = real_time - real_time_start +\
                        self._real_time_remainder
                    if real_executing_time > config.real_time_limit_seconds:
                        self.kill_process()
                        logger.error('bot with cmd \'%s\' exceeded '
                                     'time limit', self._player_command)
                        raise TimeLimitException

                    cpu_executing_time = (cpu_time - cpu_time_start +
                                          self._cpu_time_remainder)
                    if cpu_executing_time > config.cpu_time_limit_seconds:
                        self.kill_process()
                        logger.error('bot with cmd \'%s\' exceeded '
                                     'cpu time limit', self._player_command)
                        raise TimeLimitException

                    if hasattr(config, 'observe_period'):
                        time.sleep(config.observe_period)
            finally:
                self._real_time_remainder += real_time - real_time_start
                self._cpu_time_remainder += cpu_time - cpu_time_start

            if self._get_move_exception:
                logger.error('exception has been raised during '
                             'interaction with bot')
                raise self._get_move_exception

            logger.debug('elapsed real time: %f sec, '
                         'elapsed cpu time: %f sec, '
                         'used memory: %f mb',
                         self._get_real_time() - real_time,
                         self._get_cpu_time() - cpu_time,
                         self._get_memory())
            return self._deserialize_result
        except psutil.NoSuchProcess:
            raise ProcessNotRunningException()

    def kill_process(self):
        '''
        Kills bot's process if it is running or does nothing
        if the process was already killed.
        '''
        import psutil
        if self._process is not None:
            try:
                self._process.kill()
                self._process.communicate()
            except (OSError, psutil.NoSuchProcess):
                pass
        logger.info('process with cmd line \'%s\' was killed',
                    self._player_command)


def is_psutil():
    '''
    Returns if psutil installed
    '''
    try:
        import psutil
    except Exception:
        return False
    else:
        return True


Bot = ComplexBot if is_psutil() else BaseBot
