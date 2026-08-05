import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logger(service_name):

    logger = logging.getLogger(service_name)

    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
