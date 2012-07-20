import logging

LOG_FORMAT = '(%(asctime)s)[%(levelname)s]: %(message)s'

logging.basicConfig(format=LOG_FORMAT, datefmt='%m.%d.%Y %H:%M:%S')

logger = logging.getLogger('play_logger')
logger.setLevel(logging.INFO)
