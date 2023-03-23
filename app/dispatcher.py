import sys
import json
import socket
import requests
import time
import asyncpraw
import asyncio
import logging
from pythonjsonlogger import jsonlogger
from datetime import datetime as dt

from asyncpraw.models.reddit.submission import Submission
from asyncpraw.models.reddit.comment import Comment


class RedditDispatcher:
    """
    Dispatcher class that streams data from Reddit API and
    sends it to the consumer endpoints.
    """

    def __init__(self, **kwargs):
        self._setup_logging(kwargs.get("debug", False))
        api_config = kwargs.get("api_config", dict())

        self.submission_endpoint = kwargs.get("submission_endpoint", "http://localhost:8080")
        self.logger.info(f"Set submission endpoint", extra=dict(
            endpoint=self.submission_endpoint))

        self.comment_endpoint = kwargs.get("comment_endpoint", "http://localhost:8080")
        self.logger.info(f"Set comment endpoint", extra=dict(
            endpoint=self.comment_endpoint))

        self.subreddits = kwargs.get("subreddits", [])
        self.logger.info(f"Got subreddit list", extra=dict(
            subreddits=self.subreddits))

        self.reddit = asyncpraw.Reddit(**api_config)
        self.headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

    def _setup_logging(self, debug=False):
        """Set up the logger object
        """
        self.logger = logging.getLogger("dispatcher")
            
        logHandler = logging.StreamHandler()
        logHandler.setFormatter(jsonlogger.JsonFormatter())
        self.logger.addHandler(logHandler)
        
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
        self.logger.debug("Running with debug ON", extra=dict(level="DEBUG"))

    def start(self) -> None:
        """Starts streaming reddit activity and sending it to the bots.
        """
        loop = asyncio.get_event_loop()
        loop.create_task(self._stream_comments())
        loop.create_task(self._stream_submissions())
        self.logger.info("Started reddit dispatcher", extra=dict(level="INFO"))
        loop.run_forever()

    async def _stream_submissions(self) -> None:
        """Stream submissions asynchronously. Calls self._dispatch_submission()
        """
        subreddit = await self.reddit.subreddit(
            "+".join(self.subreddits))
        async for submission in subreddit.stream.submissions(pause_after=-1):
            if submission is None:
                continue
            await self._dispatch(self.submission_endpoint, dict(
                id=submission.id,
                created_utc=str(dt.fromtimestamp(submission.created_utc))
            ))

    async def _stream_comments(self) -> None:
        """Stream comments asynchronously. Calls self._dispatch_comment()
        """
        subreddit = await self.reddit.subreddit(
            "+".join(self.subreddits))
        async for comment in subreddit.stream.comments(pause_after=-1):
            if comment is None:
                continue
            await self._dispatch(self.comment_endpoint, dict(
                id=comment.id,
                created_utc=str(dt.fromtimestamp(comment.created_utc))
            ))

    async def _dispatch(self, endpoint: str, data: dict) -> None:
        """POST a json data object to an endpoint
        """
        try:
            response = requests.post(endpoint,
                data=json.dumps(data),
                headers=self.headers
            ).raise_for_status()
            self.logger.debug(f"Dispatch succeeded", extra=dict(
                level="DEBUG",
                endpoint=endpoint,
                data=data))
        except Exception as e:
            self.logger.error(f"Dispatch failed", extra=dict(
                level="ERROR",
                error=str(e),
                endpoint=endpoint,
                data=data))
            time.sleep(1) # wait for a bit to not flood the logs
