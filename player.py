import subprocess


class ProcessNotRunningException(OSError):
    '''
    This exception is raised after trying to
    send command to process that is not running.
    '''


class Player:
    '''
    This class wraps player's process and stores its information.

    Examples:
        >>> from .move import Move
        >>> from .player_state import PlayerState # import *your* classes
        >>> p = Player('python bot.py')
        >>> p.create_process()
        >>> ps = PlayerState(...)
        >>> move = Move(...)
        >>> p.get_move(ps, move)
        <move.Move object at ...>
        >>> p.kill_process()
    '''
    def __init__(self, player_command):
        '''
        Constructor for class Player.
        player_command is a string which is used to invoke player program.
        '''
        self._player_command = player_command.split()
        self._process = None

    def create_process(self):
        '''
        Starts player's process.
        '''
        self._process = subprocess.Popen(
            self._player_command,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE
        )

    def get_move(self, player_state, move):
        '''
        Serialize player_state and transfer it to player,
        then deserialize output received from player to `move`
        '''
        if not self._is_running:
            raise ProcessNotRunningException
        self._write(player_state)
        self._read(move)

    def _read(self, move):
        '''
        Invokes move.deserialize with player's `stdout`.
        `stdout` is a stream opened to read per *byte*.
        '''
        move.deserialize(self._process.stdout)

    def _write(self, player_state):
        '''
        Invokes player_state.serialize with player's `stdin`.
        `stdin` is a stream opened to write per *byte*.
        '''
        player_state.serialize(self._process.stdin)

    def kill_process(self):
        '''
        Kills player's process if it is running or does nothing
        if the process was already killed.
        '''
        if not self._is_running():
            return
        self._process.kill()
        self._process.communicate()

    def _is_running(self):
        '''
        Returns true if the process is running and false otherwise.
        '''
        return self._process and self._process.poll() is None

    def __del__(self):
        '''
        Destructor for class Player.
        It automatically kills player's process on delete.
        '''
        self.kill_process()
