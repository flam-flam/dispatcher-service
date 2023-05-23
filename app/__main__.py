import os
import asyncpraw

from .dispatcher import RedditDispatcher
from .logging import Logger
from .config import Config


try:
    config = Config()
    logger = Logger()

    logger.info("Setting up reddit instance")
    reddit = asyncpraw.Reddit(
        client_id=os.environ.get("REDDIT_CLIENT_ID"),
        client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
        user_agent="python:flam-flam-dispatcher-service (by /u/timberhilly)",
        redirect_uri="http://flam-flam.github.io"
    )

    logger.info("Setting up the dispatcher")
    RedditDispatcher(reddit, config).start()
except Exception as e:
    logger.error("Unhandled error occured", error=str(e))
