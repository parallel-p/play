import bot
import bot_no_psutil

def is_psutil():
    '''
    Returns if psutil installed
    '''
    try:
        import psutil
    except (Exception):
        return False
    else:
        return True

def create():
    '''
    Returns the constructor of the bot if psutil is installed and bot_no_psutil
    otherwise.
    '''
    if is_psutil():
        return bot.Bot
    else:
        return bot_no_psutil.Bot
