import logging

logger = logging.getLogger('play_logger')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('(%(asctime)s)[%(levelname)s]: %(message)s')
logger.setFormatter(formatter)
