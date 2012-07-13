import psutil
import threading
import time
from subprocess import PIPE
from .log import logger


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
    def __init__(self, player_command, config):
        '''
        Constructor for class Bot.
        player_command is a string which is used to invoke bot program.
        '''
        self._player_command = player_command
        self._process = None
        self._config = config

    def create_process(self):
        '''
        Starts bot's process.
        '''
        logger.info('executing "%s"', self._player_command)
        self._process = psutil.Popen(
            self._player_command.split(),
            stdout=PIPE,
            stdin=PIPE
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
        memory_limit_mb = self._config.memory_limit_mb

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
                raise MemoryLimitException

    def _check_cpu_time_limit(self):
        '''
        This function is running in a separate thread
        and check process exceed cpu time limit every `CHECK_TIME_SECONDS`
        seconds.
        '''
        CHECK_TIME_SECONDS = 0.15
        cpu_limit = self._config.cpu_time_limit_seconds
        cpu_time_start = self._get_cpu_time()

        exit_code = None
        while exit_code is None:
            try:
                exit_code = self._process.wait(CHECK_TIME_SECONDS)
            except psutil.TimeoutExpired:
                pass
            try:
                process_cpu_time = self._get_cpu_time()
            except psutil.NoSuchProcess:
                return
            if process_cpu_time is None:
                return
            elif process_cpu_time - cpu_time_start > cpu_limit:
                self.kill_process()
                raise TimeLimitException

    def _check_real_time_limit(self):
        '''
        This function is running in a separate thread
        and check process exceed real time limit every `CHECK_TIME_SECONDS`
        seconds.
        '''
        CHECK_TIME_SECONDS = 0.15
        real_limit = self._config.real_time_limit_seconds
        real_time_start = time.time()

        exit_code = None
        while (exit_code is None) and (self._is_running()):
            try:
                exit_code = self._process.wait(CHECK_TIME_SECONDS)
            except psutil.TimeoutExpired:
                exit_code = self._process.wait()
            try:
                process_real_time = time.time()
            except psutil.NoSuchProcess:
                return

            if process_real_time - real_time_start > real_limit:
                self.kill_process()
                raise TimeLimitException

    def _get_cpu_time(self):
        '''
        Get CPU time used by bot's process.
        '''
        try:
            return self._process.get_cpu_times().system
        except psutil.NoSuchProcess:
            return None

    def get_move(self, player_state, move):
        '''
        Serialize player_state and transfer it to bot,
        then deserialize output received from bot to `move`.
        '''
        if not self._is_running:
            raise ProcessNotRunningException
        self._write(player_state)
        self._read(move)

    def _read(self, move):
        '''
        Invokes move.deserialize with bot's `stdout`.
        `stdout` is a stream opened to read per *byte*.
        '''
        real_time_limit_seconds = self._config.real_time_limit_seconds
        cpu_time_limit_seconds = self._config.cpu_time_limit_seconds

        time_cpu_limiter_thread = threading.Thread(
            target=self._check_cpu_time_limit
        )
        time_real_limiter_thread = threading.Thread(
            target=self._check_real_time_limit
        )
        time_cpu_limiter_thread.start()
        time_real_limiter_thread.start()
        move.deserialize(self._process.stdout)

    def _write(self, player_state):
        '''
        Invokes player_state.serialize with bot's `stdin`.
        `stdin` is a stream opened to write per *byte*.
        '''
        player_state.serialize(self._process.stdin)

    def kill_process(self):
        '''
        Kills bot's process if it is running or does nothing
        if the process was already killed.
        '''
        if not self._is_running():
            return
        self._process.kill()
        self._process.communicate()
        logger.info('process with cmd line "%s" was killed', self._player_command)

    def _is_running(self):
        '''
        Returns true if the process is running and false otherwise.
        '''
        return self._process and self._process.is_running()

    def __del__(self):
        '''
        Destructor for class bot.
        It automatically kills bot's process on delete.
        '''
        self.kill_process()

