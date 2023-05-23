import structlog


class Logger(object):
    _instance = None

    def __init__(self):
        raise RuntimeError('Call Logger.instance() instead of Logger()')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            structlog.configure(
                processors=[
                    structlog.processors.JSONRenderer()
                ]
            )
            cls._instance = structlog.get_logger()

        return cls._instance
