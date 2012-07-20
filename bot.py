import psutil
import threading
import time
from subprocess import PIPE
from log import logger
import config
import copy


MEGABYTE = 1 << 20

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


class ProcessNotRunningException(OSError):
    '''
    This exception is raised after trying to
    send command to process that is not running.
    '''


class TimeLimitException(OSError):
    '''
    This exception is raised when bot's process exceeded time limit.
    '''


class MemoryLimitException(OSError):
    '''
    This exception is raised when bot's process exceeded memory limit.
    '''


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
                stderr=PIPE
            )
        except OSError:
            logger.critical(
                'executing of \'%s\' failed: invalid command',
                self._player_command
            )
            raise ExecuteError

        self._checker = threading.Thread(target=self._check_memory_limits)
        self._checker.start()
        logger.info('executing successful')

    def _check_memory_limits(self):
        '''
        This function is running in a separate thread
        and check process exceed memory limit every `CHECK_TIME_SECONDS`
        seconds.
        '''
        CHECK_TIME_SECONDS = 0.15
        memory_limit_mb = config.memory_limit_mb

        exit_code = None
        while exit_code is None or self._is_running():
            try:
                exit_code = self._process.wait(CHECK_TIME_SECONDS)
            except psutil.TimeoutExpired:
                pass

            process_memory = self._get_memory()
            if not process_memory:
                break
            else:
                process_memory /= MEGABYTE
                if process_memory > memory_limit_mb:
                    self.kill_process()
                    logger.error('bot with cmd \'%s\' exceeded memory limit',
                                 self._player_command)
                    raise MemoryLimitException

    def _get_cpu_time(self):
        '''
        Returns CPU time used by bot's process.
        If psutil.NoSuchProcess exception has been raised, returns None.
        '''
        try:
            times = self._process.get_cpu_times()
            return times.system + times.user
        except psutil.NoSuchProcess:
            return None

    def _get_real_time(self):
        '''
        Returns real time used by bot's process.
        '''
        return time.time()

    def _get_memory(self):
        '''
        Returns memory used by process in *megabytes*.
        If psutil.NoSuchProcess exception has been raised, returns None.
        '''
        try:
            return self._process.get_memory_info().rss / MEGABYTE
        except psutil.NoSuchProcess:
            return None

    def _check_time_limits(self):
        real_time_start = self._get_real_time()
        cpu_time_start = self._get_cpu_time()

        while True:
            cpu_time = self._get_cpu_time()
            real_time = self._get_real_time()
            if cpu_time is None:
                # psutil was raised NoSuchProcess
                raise ProcessNotRunningException

            if real_time - real_time_start > config.real_time_limit_seconds:
                self.kill_process()
                logger.error('bot with cmd \'%s\' exceeded time limit',
                             self._player_command)
                raise TimeLimitException

            if cpu_time - cpu_time_start > config.cpu_time_limit_seconds:
                self.kill_process()
                logger.error('bot with cmd \'%s\' exceeded cpu time limit',
                             self._player_command)
                raise TimeLimitException

            if hasattr(self, '_deserialize_exc') and self._deserialize_exc:
                logger.critical(
                    'unhandled exception has been raised in'
                    'deserialize thread, aborting'
                )
                exc_copy = copy.deepcopy(self._deserialize_exc)
                raise self._deserialize_exc

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
        cpu_time = self._get_cpu_time()

        get_move_thread = threading.Thread(
            target=self._get_move,
            args=(player_state, serialize, deserialize)
        )
        get_move_thread.start()

        self._check_time_limits()

        res = copy.deepcopy(self._deserialize_result)
        del self._deserialize_result
        return res

        memory = self._get_memory()

        logger.debug(
            'elapsed real time: %f sec'
            ', elapsed cpu time: %f sec, used memory: %f mb',
            self._get_real_time() - real_time,
            self._get_cpu_time() - cpu_time,
            memory
        )

        return move

    def _get_move(self, player_state, serialize, deserialize):
        self._write(player_state, serialize)
        self._read(deserialize)

    def _run_deserialize(self, deserialize):
        '''
        Invokes author's deserialization function and
        stores received `move` into self._deserialize_result.

        If deserialize function raised exception, this function stores
        information about exception for re-raising.
        '''
        try:
            self._deserialize_result = deserialize(self._process.stdout)
        except (BaseException, Exception) as exc:
            self._deserialize_exc = exc
            return

    def _read(self, deserialize):
        '''
        Deserialize move with bot's `stdout`.
        `stdout` is a stream opened to read per *byte*.

        If bot's process isn't running, raise ProcessNotRunningException.
        '''
        if not self._is_running():
            raise ProcessNotRunningException

        self._run_deserialize(deserialize)

    def _write(self, player_state, serialize):
        '''
        Serialize player_state with bot's `stdin`.
        `stdin` is a stream opened to write per *byte*.
        '''
        serialize(player_state, self._process.stdin)

    def kill_process(self):
        '''
        Kills bot's process if it is running or does nothing
        if the process was already killed.
        '''
        if not self._is_running():
            return
        try:
            self._process.kill()
        except psutil.NoSuchProcess:
            pass
        self._process.communicate()
        logger.info('process with cmd line \'%s\' was killed',
                    self._player_command)

    def _is_running(self):
        '''
        Returns true if the process exists and is running and false otherwise.
        '''
        return self._process and self._process.is_running()

    def __del__(self):
        '''
        Destructor for class bot.
        It automatically kills bot's process on delete.
        '''
        self.kill_process()
