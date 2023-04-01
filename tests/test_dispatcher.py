import os
import sys
import pytest
import requests_mock
from interruptingcow import timeout

from asyncpraw_mock import Reddit

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

TIMEOUT = 1  # seconds to run the streams for
TEST_CONFIG = dict(
    debug=False,
    comment_endpoint="http://test:8080",
    submission_endpoint="http://test:8080",
    subreddits=["test"],
)
API_CONFIG = dict(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
    user_agent="python:flam-flam-dispatcher-service (by /u/timberhilly)",
    redirect_uri="http://flam-flam.github.io"
)


def test_import() -> None:
    from app import RedditDispatcher
    assert isinstance(RedditDispatcher, type)


@pytest.mark.asyncio
async def test_init() -> None:
    from app import RedditDispatcher
    dispatcher = RedditDispatcher(Reddit(**API_CONFIG), TEST_CONFIG)
    await dispatcher.reddit.close()


@pytest.mark.asyncio
async def test_config() -> None:
    from app import RedditDispatcher
    dispatcher = RedditDispatcher(Reddit(**API_CONFIG), TEST_CONFIG)

    assert isinstance(dispatcher.comment_endpoint, str)
    assert isinstance(dispatcher.submission_endpoint, str)
    assert isinstance(dispatcher.subreddits, list) and \
        len(dispatcher.subreddits) == 1 and \
        isinstance(dispatcher.subreddits[0], str)

    await dispatcher.reddit.close()


@pytest.mark.asyncio
async def test_dispatch_comments() -> None:
    from app import RedditDispatcher
    dispatcher = RedditDispatcher(Reddit(**API_CONFIG), TEST_CONFIG)
    with requests_mock.Mocker() as m:
        m.get(TEST_CONFIG["comment_endpoint"], text="ok")
        try:
            with timeout(TIMEOUT, RuntimeError):
                await dispatcher._stream_submissions()
                assert False
        except RuntimeError:
            await dispatcher.reddit.close()
            assert True


@pytest.mark.asyncio
async def test_dispatch_submissions() -> None:
    from app import RedditDispatcher
    dispatcher = RedditDispatcher(Reddit(**API_CONFIG), TEST_CONFIG)
    with requests_mock.Mocker() as m:
        m.get(TEST_CONFIG["submission_endpoint"], text="ok")
        try:
            with timeout(TIMEOUT, RuntimeError):
                await dispatcher._stream_submissions()
                assert False
        except RuntimeError:
            await dispatcher.reddit.close()
            assert True
