
# coding=utf-8
"""
if rotate_mode == "size":
    channel = logging.handlers.RotatingFileHandler(
        filename=options.log_file_prefix,
        maxBytes=options.log_file_max_size,
        backupCount=options.log_file_num_backups,
        encoding="utf-8",
    )  # type: logging.Handler
elif rotate_mode == "time":
    channel = logging.handlers.TimedRotatingFileHandler(
        filename=options.log_file_prefix,
        when=options.log_rotate_when,
        interval=options.log_rotate_interval,
        backupCount=options.log_file_num_backups,
        encoding="utf-8",
    )
"""
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
        'handlers': ['log'],
        'propagate': 'no'
      }
    },
    'formatters': {
      'simple': {
        'format': '%(levelname)s %(name)s-%(funcName)s-%(asctime)s %(pathname)s %(lineno)s:%(message)s'
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
        'class': 'logging.handlers.TimedRotatingFileHandler',  # time
        'level': 'DEBUG',
        'formatter': 'simple',
        'filename': './weblog/access.log',
        'when': 'midnight',
        'interval': 1,
        'backupCount': 2,    # u"备份数"
        'encoding': 'utf8'
        },
      'log': {
        'class': 'logging.handlers.RotatingFileHandler',    # size
        'level': 'INFO',
        'formatter': 'timedRotating',
        'filename': './weblog/log.log',
        # 'when': 'midnight',
        # 'interval': 1,
        'backupCount': 2,
        'maxBytes': 1 * 1024 * 1024,  # 文件最大50M
        'encoding': 'gbk'
        }
    }
}