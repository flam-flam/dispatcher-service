import asyncio
from .comment import Comment
from .submission import Submission


class SubredditStream:
    async def submissions(self, pause_after=0):
        while True:
            yield Submission()
            await asyncio.sleep(0.1)

    async def comments(self, pause_after=0):
        while True:
            yield Comment()
            await asyncio.sleep(0.1)


class Subreddit:
    async def __call__(self, *args, **kwargs):
        pass

    @property
    def stream(self) -> SubredditStream:
        return SubredditStream()
