import threading
import time
from subprocess import PIPE, Popen
from log import logger
import config
import copy


'''
TODO:
while process.is_running():
    // check limits and `sleep`
# to record information about CPU time,
# real time and memory
# then count of steps became equal to
# `y`, check limits and delete information
'''


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


class BadPipesError(OSError):
    '''
    This exception is raised when bot's process pipes are broken.
    '''
    def __init__(self):
        OSError.__init__(self, 'pipes are broken')


class Bot:
    '''
    This class wraps bot's process and stores its information.

    Examples:
        >>> from .move import Move
        >>> from .player_state import PlayerState # import *your* classes
        >>> p = bot('python bot.py')
        >>> p.create_process()
        >>> ps = PlayerState(...)
        >>> move = Move(...)
        >>> p.get_move(ps, move)
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
        self._running = False

    def create_process(self):
        '''
        Starts bot's process.
        '''
        logger.info('executing \'%s\'', self._player_command)
        try:
            self._process = Popen(
                self._player_command.split(),
                stdout=PIPE,
                stdin=PIPE,
                stderr=PIPE
            )
        except OSError:
            logger.critical(
                'executing of \'%s\' failed: invalid command',
                self._player_command
            )
            raise ExecuteError

        self._check_pipes()

        if not self._is_running():
            logger.critical(
                'executing of \'%s\' failed: invalid command',
                self._player_command
            )
            raise ExecuteError

        logger.info('executing successful')
        self._running = True

    def _check_pipes(self):
        if not self._process.stdin.writable() and self._process.stdout.readable():
            raise BadPipesError()

    def _get_real_time(self):
        '''
        Returns real time used by bot's process.
        '''
        return time.time()

    def _check_time_limits(self):
        real_time_start = self._get_real_time()

        while True:
            real_time = self._get_real_time()

            if real_time - real_time_start > config.real_time_limit_seconds:
                print()
                self.kill_process()
                logger.error('bot with cmd \'%s\' exceeded time limit',
                             self._player_command)
                raise TimeLimitException

            if hasattr(self, '_deserialize_exc') and self._deserialize_exc:
                print()
                logger.critical(
                    'unhandled exception has been raised in '
                    'deserialize thread, aborting'
                )
                exc_copy = copy.deepcopy(self._deserialize_exc)
                del self._deserialize_exc
                raise exc_copy

            if hasattr(self, '_deserialize_result'):
                break

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
        if not self._is_running():
            raise ProcessNotRunningException

        real_time = self._get_real_time()

        get_move_thread = threading.Thread(
            target=self._get_move,
            args=(player_state, serialize, deserialize)
        )
        get_move_thread.start()

        self._check_time_limits()

        res = copy.deepcopy(self._deserialize_result)
        del self._deserialize_result

        logger.debug(
            'elapsed real time: %f sec',
            self._get_real_time() - real_time,
        )
        return res

    def _get_move(self, player_state, serialize, deserialize):
        self._write(player_state, serialize)
        self._read(deserialize)

    def _write(self, player_state, serialize):
        '''
        Serialize player_state with bot's `stdin`.
        `stdin` is a stream opened to write per *byte*.
        '''
        if self._running:
            serialize(player_state, self._process.stdin)

    def _read(self, deserialize):
        '''
        Deserialize move with bot's `stdout`.
        `stdout` is a stream opened to read per *byte*.

        Invokes author's deserialization function and
        stores received `move` into self._deserialize_result.

        If deserialize function raised exception, this function stores
        information about exception for re-raising.

        If bot's process isn't running, raise ProcessNotRunningException.
        '''
        try:
            if not self._is_running():
                raise ProcessNotRunningException()
            self._check_pipes()
            self._deserialize_result = deserialize(self._process.stdout)
        except (BaseException, Exception) as exc:
            self._deserialize_exc = exc

    def kill_process(self):
        '''
        Kills bot's process if it is running or does nothing
        if the process was already killed.
        '''
        if not self._is_running():
            return
        try:
            self._process.kill()
        except OSError:
            pass
        self._process.communicate()
        logger.info('process with cmd line \'%s\' was killed',
                    self._player_command)
        self._running = False

    def _is_running(self):
        '''
        Returns true if the process exists and is running and false otherwise.
        '''
        return self._process and not bool(self._process.poll())

    def __del__(self):
        '''
        Destructor for class bot.
        It automatically kills bot's process on delete.
        '''
        self.kill_process()
