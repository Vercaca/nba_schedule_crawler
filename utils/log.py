import logging
import datetime
from pathlib import Path
from functools import wraps

from utils.file import DEFAULT_ENCODING


def log_print(start_msg='Running'):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            logging.info(f'>> {start_msg} {f.__name__} ...')
            result = f(*args, **kwargs)
            logging.info(f' {f.__name__} | Finish.')
            return result
        return wrapper
    return decorator


def init_log(filename, save_log=True, level=logging.INFO):
    filename = Path(filename).stem
    log_filename = datetime.datetime.now().strftime(f"log/{filename}__%Y-%m-%d_%H_%M_%S.log")
    Path(log_filename).parent.mkdir(exist_ok=True)
    logger = logging.getLogger(filename)

    fmt = '%(asctime)s - %(levelname)s - %(name)30s -   %(message)s'
    date_fmt = '%m/%d/%Y %H:%M:%S'
    level = level

    if save_log:
        logging.basicConfig(handlers=[logging.FileHandler(log_filename, encoding=DEFAULT_ENCODING)],
                            format=fmt, datefmt=date_fmt, level=level)
        _init_console_log(logger, level=level)
    else:
        logging.basicConfig(format=fmt, datefmt=date_fmt, level=level)
    return logger


def _init_console_log(logger, level=logging.INFO):
    """ create console handler, set level and formatter """
    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # create formatter
    ch.setFormatter(formatter)  # add formatter to ch
    logger.addHandler(ch)  # add ch to logger
