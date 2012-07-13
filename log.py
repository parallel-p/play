import logging

LOG_FORMAT = '(%(asctime)s)[%(levelname)s]: %(message)s'

logging.basicConfig(format=LOG_FORMAT)

logger = logging.getLogger('play_logger')
logger.setLevel(logging.DEBUG)
