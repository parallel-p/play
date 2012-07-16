import psutil
import threading
import time
from subprocess import PIPE
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


class ProcessNotRunningException(OSError):
    '''
    This exception is raised after trying to
    send command to process that is not running.
    '''


class TimeLimitException(OSError):
    '''
    This exception is raised when bot process exceeded time limit.
    '''


class MemoryLimitException(OSError):
    '''
    This exception is raised when bot process exceeded memory limit.
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
        player_command is a string which is used to invoke bot program.
        '''
        self._player_command = player_command
        self._process = None

    def create_process(self):
        '''
        Starts bot's process.
        '''
        logger.info('executing "%s"', self._player_command)
        self._process = psutil.Popen(
            self._player_command.split(),
            stdout=PIPE,
            stdin=PIPE,
            stderr=PIPE
        )

        self._checker = threading.Thread(target=self._check_memory_limits)
        self._checker.start()

    def _check_memory_limits(self):
        '''
        This function is running in a separate thread
        and check process exceed memory limit every `CHECK_TIME_SECONDS`
        seconds.
        '''
        CHECK_TIME_SECONDS = 0.15
        memory_limit_mb = config.memory_limit_mb

        exit_code = None
        while exit_code is None:
            try:
                exit_code = self._process.wait(CHECK_TIME_SECONDS)
            except psutil.TimeoutExpired:
                pass

            try:
                megabyte = 1 << 20
                process_memory = self._process.get_memory_info().rss / megabyte
            except psutil.NoSuchProcess:
                return

            if process_memory > memory_limit_mb:
                self.kill_process()
                logger.error("bot with cmd '%s' exceeded memory limit",
                             self._player_command)
                raise MemoryLimitException

    def _get_cpu_time(self):
        '''
        Get CPU time used by bot's process.
        '''
        try:
            times = self._process.get_cpu_times()
            return times.system + times.user
        except psutil.NoSuchProcess:
            return None

    def _get_real_time(self):
        '''
        Get real time used by bot's process.
        '''
        return time.time()

    def get_move(self, player_state, serialize, deserialize):
        '''
        Serialize player_state and transfer it to bot,
        then deserialize output received from bot to `move`.
            ``player_state`` - object, which will be passed to
        the bot after serialization.
            ``serialize(player_state, writable)`` is a function,
        which is responsible for serializing ``player_state`` and
        writing it to ``writable``.
            ``deserialize(readable)`` is a function, which is
        responsible for reading data from ``readable`` and turning it
        to a valid ``move`` object.
        '''
        if not self._is_running:
            raise ProcessNotRunningException
        self._write(player_state, serialize)
        move = self._read(deserialize)
        return move

    def _run_deserialize(self, deserialize):
        ''' Invokes author's deserialization function and
        stores received ``move`` into self._deserialize_result '''
        try:
            self._deserialize_result = deserialize(self._process.stdout)
        except (BaseException, Exception) as exc:
            self._deserialize_exc = exc

    def _read(self, deserialize):
        '''
        Deserialize move with bot's `stdout`.
        `stdout` is a stream opened to read per *byte*.
        '''
        if not self._is_running():
            raise ProcessNotRunningException

        deserialize_thread = threading.Thread(
            target=self._run_deserialize,
            args=(deserialize,),
            name="deserialize thread",
        )
        deserialize_thread.daemon = True
        deserialize_thread.start()

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
                logger.error("bot with cmd '%s' exceeded time limit",
                             self._player_command)
                raise TimeLimitException

            if cpu_time - cpu_time_start > config.cpu_time_limit_seconds:
                self.kill_process()
                logger.error("bot with cmd '%s' exceeded cpu time limit",
                             self._player_command)
                raise TimeLimitException

            if hasattr(self, "_deserialize_exc") and self._deserialize_exc:
                exc_copy = copy.deepcopy(self._deserialize_exc)
                raise self._deserialize_exc

            if not deserialize_thread.is_alive():
                break

        res = copy.deepcopy(self._deserialize_result)
        del self._deserialize_result
        return res

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
        logger.info('process with cmd line "%s" was killed',
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
