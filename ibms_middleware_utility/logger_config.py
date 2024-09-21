import logging
import logging.config
import os


def setup_logging(log_directory, log_file='app.log'):
    """
    Setups the logger configuration. Should be called before creating logging object.

    Args:
        log_directory (str): Path to folder where log files will be stored (Needs to have write permission).
        log_file (str): Log file name. Defaults to app.log.
    """
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'standard',
                'filename': os.path.join(log_directory, log_file),
                'when': 'midnight',
                'backupCount': 7,
            },
        },
        'loggers': {
            '': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
            '__main__': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }

    logging.config.dictConfig(logging_config)
