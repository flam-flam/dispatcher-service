import asyncio
from unittest.mock import AsyncMock


class SubredditStream(AsyncMock):
    fake_comments = [
        type('Comment', (object,), dict(
                id=f"abcde{i}",
                created_utc=i+1681654036
            ))
        for i in range(3)
    ]
    fake_submissions = [
        type('Submission', (object,), dict(
                id=f"abcde{i}",
                created_utc=i+1681654036
            ))
        for i in range(3)
    ]

    async def submissions(self, pause_after=0):
        for i in range(3):
            yield self.fake_submissions[i]
            await asyncio.sleep(0.1)

    async def comments(self, pause_after=0):
        for i in range(3):
            yield self.fake_comments[i]
            await asyncio.sleep(0.1)
