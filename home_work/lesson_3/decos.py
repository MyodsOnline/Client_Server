import sys
import logging
import traceback


def log(func_to_log):
    def log_saver(*args, **kwargs):
        logger_name = 'app.server' if 'server.py' in sys.argv[0] else 'app.client'
        LOGGER = logging.getLogger(logger_name)
        ret = func_to_log(*args, **kwargs)
        LOGGER.debug(f'\nThe "{func_to_log.__name__}" function with parameters \n"{args}, {kwargs}" is called.\n'
                     f'Calling from module "{func_to_log.__module__}".\n'
                     f'Calling from function "{traceback.format_stack()[0].strip().split()[-1]}".')
        return ret
    return log_saver
