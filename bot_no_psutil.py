import subprocess
import threading
import time
from log import logger
import config
import copy


class ProcessNotRunningException(OSError):
    '''
    This exception is raised after trying to
    send command to process that is not running.
    '''


class TimeLimitException(OSError):
    '''
    This exception is raised when bot process exceeded time limit.
    '''


class Bot:
    '''
    This class wraps bot's process and stores its information.
    This is a simplified version of bot.py: it doesn't use psutil.

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
        self._process = subprocess.Popen(
            self._player_command.split(),
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    def _get_real_time(self):
        '''
        Get real time used by bot's process.
        '''
        return time.time()

    def get_move(self, player_state, serialize, deserialize):
        '''
        Serialize player_state and transfer it to bot,
        then deserialize output received from bot to `move`.
        '''
        if not self._is_running():
            raise ProcessNotRunningException
        self._write(player_state, serialize)
        move = self._read(deserialize)
        return move

    def _run_deserialize(self, deserialize):
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

        while True:
            real_time = self._get_real_time()

            if real_time - real_time_start > config.real_time_limit_seconds:
                self.kill_process()
                logger.error("bot with cmd '%s' exceeded time limit",
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
        self._process.kill()
        self._process.communicate()
        logger.info('process with cmd line "%s" was killed',
                    self._player_command)

    def _is_running(self):
        '''
        Returns true if the process is running and false otherwise.
        '''
        return not bool(self._process.poll())

    def __del__(self):
        '''
        Destructor for class bot.
        It automatically kills bot's process on delete.
        '''
        self.kill_process()
