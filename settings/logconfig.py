
# coding=utf-8

logconfig = {

    'version': 1,
    'loggers': {
      'root': {
        'level': 'DEBUG',
        'handlers': ['console']
      },
      'tornado': {
        'level': 'DEBUG',
        'handlers': ['console', 'log'],
        'propagate': 'no'
      },
      'tornado.access': {
        'level': 'DEBUG',
        'handlers': ['console', 'access'],
        'propagate': 'no'
      },
      'log': {
        'level': 'DEBUG',
        'handlers': ['console', 'log'],
        'propagate': 'no'
      }
    },
    'formatters': {
      'simple': {
        'format': '[%(levelname)s %(name)s]-[%(funcName)s]-[%(asctime)s %(pathname)s %(lineno)s]:(%(message)s)'
      },
      'timedRotating': {
        'format': '%(asctime)s %(name)-12s %(levelname)-8s - %(message)s'
      }
    },
    'handlers': {
      'console': {
        'class': 'logging.StreamHandler',
        'level': 'DEBUG',
        'formatter': 'simple',
        },
      'access': {
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'level': 'DEBUG',
        'formatter': 'simple',
        'filename': './weblog/access.log',
        'when': 'midnight',
        'interval': 1,
        'backupCount': 180
        },
      'log': {
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'level': 'DEBUG',
        'formatter': 'timedRotating',
        'filename': './weblog/log.log',
        'when': 'midnight',
        'interval': 1,
        'backupCount': 180,
        'encoding': 'utf8'
        }
    }
}