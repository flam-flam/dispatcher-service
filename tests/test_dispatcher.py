import os
import sys
import pytest
import requests_mock
from interruptingcow import timeout
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

TEST_CONFIG = dict(
    debug=False,
    comment_endpoint="http://test:8080",
    submission_endpoint="http://test:8080",
    subreddits=["test"],
    api_config=dict(
        client_id=os.environ.get("REDDIT_CLIENT_ID"),
        client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
        user_agent=f"python:flam-flam-dispatcher-service (by /u/timberhilly)",
        redirect_uri="http://flam-flam.github.io"
    )
)
TIMEOUT = 5 # seconds to run the streams for


def test_import() -> None:
    from app import RedditDispatcher


@pytest.mark.asyncio
async def test_init() -> None:
    from app import RedditDispatcher
    dispatcher = RedditDispatcher(**TEST_CONFIG)
    await dispatcher.reddit.close()


@pytest.mark.asyncio
async def test_config() -> None:
    from app import RedditDispatcher
    dispatcher = RedditDispatcher(**TEST_CONFIG)

    assert isinstance(dispatcher.comment_endpoint, str)
    assert isinstance(dispatcher.submission_endpoint, str)
    assert isinstance(dispatcher.subreddits, list) and \
        len(dispatcher.subreddits) == 1 and \
        isinstance(dispatcher.subreddits[0], str)

    await dispatcher.reddit.close()


@pytest.mark.asyncio
async def test_stream_comments() -> None:
    #Check if it runs at all
    from app import RedditDispatcher
    dispatcher = RedditDispatcher(**TEST_CONFIG)
    try:
        with timeout(TIMEOUT, RuntimeError):
            await dispatcher._stream_comments()
            assert False
    except RuntimeError:
        await dispatcher.reddit.close()
        assert True


@pytest.mark.asyncio
async def test_stream_submissions() -> None:
    #Check if it runs at all
    from app import RedditDispatcher
    dispatcher = RedditDispatcher(**TEST_CONFIG)
    try:
        with timeout(TIMEOUT, RuntimeError):
            await dispatcher._stream_submissions()
            assert False
    except RuntimeError:
        await dispatcher.reddit.close()
        assert True


@pytest.mark.asyncio
async def test_dispatch_comments() -> None:
    from app import RedditDispatcher
    dispatcher = RedditDispatcher(**TEST_CONFIG)
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
    dispatcher = RedditDispatcher(**TEST_CONFIG)
    with requests_mock.Mocker() as m:
        m.get(TEST_CONFIG["submission_endpoint"], text="ok")
        try:
            with timeout(TIMEOUT, RuntimeError):
                await dispatcher._stream_submissions()
                assert False
        except RuntimeError:
            await dispatcher.reddit.close()
            assert True
