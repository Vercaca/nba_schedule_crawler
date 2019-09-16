import time
import random


def build_logger(name):
    import logging
    return logging.getLogger(name)


def random_sleep(level: float = 1.0, logger=build_logger(__name__)):
    base_time = int(5 * level)
    sleep_time = random.randrange(base_time, base_time + 5)
    logger.info(f'-- randomly sleeping {sleep_time} seconds --')
    time.sleep(sleep_time)
    logger.info(f'-- Continue --')


