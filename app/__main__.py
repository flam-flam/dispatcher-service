import os
import json
import logging
import asyncpraw

from .dispatcher import RedditDispatcher

logger = logging.getLogger("__main__")

try:
    config_path = os.environ.get("CONFIG_PATH", "/src/config.json")
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    reddit_instance = asyncpraw.Reddit(
        client_id=os.environ.get("REDDIT_CLIENT_ID"),
        client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
        user_agent="python:flam-flam-dispatcher-service (by /u/timberhilly)",
        redirect_uri="http://flam-flam.github.io"
    )

    RedditDispatcher(reddit_instance, config).start()
except Exception as e:
    logger.error("Unhandled error occured", extra=dict(
                level="FATAL",
                error=str(e)))
