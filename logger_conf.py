
LOGGER_LEVEL = {
'CRITICAL':	50,
'ERROR' :	40,
'WARNING' :	30,
'INFO' :	20,
'DEBUG' :	10,
'NOTSET' :	0,
}

LOG_FILES = {
    'default' : "./logs/test.log",
    'CRITICAL' : "./logs/test_critical.log",
    'ERROR' : "./logs/test_error.log",
}



LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file_handler': {
            'level': 'INFO',
            'filename': './logs/test.log',
            'class': 'logging.FileHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['file_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'file_handler': {
            'handlers': ['file_handler'],
            'level': 'INFO',
            'propagate': False
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
    },
}