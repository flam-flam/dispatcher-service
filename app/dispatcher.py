import json
import logging
import requests
import time
import asyncio
from datetime import datetime as dt


class RedditDispatcher:
    """
    Dispatcher class that streams data from Reddit API and
    sends it to the consumer endpoints.
    """

    def __init__(self, reddit, config):
        self.reddit = reddit
        self._setup_logging(config.get("config", False))

        self.submission_endpoint = \
            config.get("submission_endpoint", "http://localhost:8080")
        self.logger.info(
            f"Set submission endpoint to {self.submission_endpoint}")

        self.comment_endpoint = \
            config.get("comment_endpoint", "http://localhost:8080")
        self.logger.info(
            f"Set comment endpoint to {self.comment_endpoint}")

        self.subreddits = config.get("subreddits", [])
        self.logger.info(f"Watching subreddits {self.subreddits}")

        self.headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

    def _setup_logging(self, debug=False):
        """Set up the logger object
        """
        self.logger = logging.getLogger("dispatcher")
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
        self.logger.debug("Running with debug ON")

    def start(self) -> None:
        """Starts streaming reddit activity and sending it to the bots.
        """
        loop = asyncio.get_event_loop()
        loop.create_task(self._stream_comments())
        loop.create_task(self._stream_submissions())
        self.logger.info("Started reddit dispatcher")
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
            requests.post(endpoint,
                          data=json.dumps(data),
                          headers=self.headers
                          ).raise_for_status()
            self.logger.debug(f"Dispatched comment with ID={data.get('id')}")
        except Exception as e:
            self.logger.error(f"Failed to dispatch to {endpoint}, {e}")
            self.logger.error(
                f"DATA: {json.dumps(data)} HEADERS: {self.headers}")
            time.sleep(1)  # wait for a bit to not flood the logs
