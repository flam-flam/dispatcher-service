import structlog
import logging
from .config import Config

class Logger(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            structlog.configure(
                wrapper_class=structlog.make_filtering_bound_logger(
                    logging.DEBUG if Config().debug else logging.INFO
                ),
                processors=[
                    structlog.processors.add_log_level,
                    structlog.processors.TimeStamper(fmt="iso", utc=True),
                    structlog.processors.JSONRenderer()
                ]
            )
            cls.instance = structlog.get_logger()
        return cls.instance
