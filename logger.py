import json
import logging
from datetime import time

from django.core.handlers.wsgi import WSGIRequest

log_file = 'api-' + time().strftime("%Y%m%d-%H%M%S") + '.log'

logging.basicConfig(
    handlers=[
        logging.handlers.RotatingFileHandler(
            log_file, maxBytes=50 * 1024 * 1024,
            backupCount=5, encoding='utf-8'
        )
    ],
    format='%(asctime)s, %(levelname)s, %(message)s',
    datefmt='%m.%d.%y %H:%M',
    level=logging.DEBUG
)

log = logging.getLogger("logger")


def info_logger(func):
    def wrapper(*args, **kwargs):
        if isinstance(args[0], WSGIRequest):
            try:
                log.info(
                    str(args[0].user) + ": " + str(
                        json.loads(
                            args[0].body or json.dumps({})
                        )
                    ) + str(str(args[0].META).split(',')[70:])
                )
            except Exception as e:
                log.error(e)
            return func(*args, **kwargs)
        else:
            log.info(args[0])
            func(*args, **kwargs)

    return wrapper
