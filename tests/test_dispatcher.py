import os
import sys
import pytest
import requests_mock
from unittest.mock import AsyncMock, MagicMock
from .helpers import SubredditStream
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

TIMEOUT = 1  # seconds to run the streams for
TEST_CONFIG = dict(
    debug=False,
    comment_endpoint="http://comment",
    submission_endpoint="http://submission",
    subreddits=["test"],
)
API_CONFIG = dict(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
    user_agent="python:flam-flam-dispatcher-service (by /u/timberhilly)",
    redirect_uri="http://flam-flam.github.io"
)


@pytest.fixture
def reddit_mock() -> MagicMock:
    instance = MagicMock(**API_CONFIG)
    instance.close = AsyncMock()
    instance.subreddit = AsyncMock()
    return instance


def test_import() -> None:
    from app import RedditDispatcher
    assert isinstance(RedditDispatcher, type)


@pytest.mark.asyncio
async def test_init(reddit_mock) -> None:
    from app import RedditDispatcher
    dispatcher = RedditDispatcher(reddit_mock, TEST_CONFIG)
    assert dispatcher.reddit == reddit_mock
    await dispatcher.reddit.close()


@pytest.mark.asyncio
async def test_config(reddit_mock) -> None:
    from app import RedditDispatcher
    dispatcher = RedditDispatcher(reddit_mock, TEST_CONFIG)

    assert isinstance(dispatcher.comment_endpoint, str) and \
        dispatcher.comment_endpoint == \
        TEST_CONFIG.get("comment_endpoint")

    assert isinstance(dispatcher.submission_endpoint, str) and \
        dispatcher.submission_endpoint == \
        TEST_CONFIG.get("submission_endpoint")

    assert isinstance(dispatcher.subreddits, list) and \
        len(dispatcher.subreddits) == len(TEST_CONFIG.get("subreddits")) and \
        dispatcher.subreddits.sort() == TEST_CONFIG.get("subreddits").sort()

    await dispatcher.reddit.close()


@pytest.mark.asyncio
async def test_get_subreddit(reddit_mock) -> None:
    from app import RedditDispatcher
    dispatcher = RedditDispatcher(reddit_mock, TEST_CONFIG)
    subreddit = await dispatcher._get_subreddit()
    assert subreddit is not None
    dispatcher.reddit.subreddit.assert_called_with(
        "+".join(TEST_CONFIG.get("subreddits"))
    )
    await dispatcher.reddit.close()


@pytest.mark.asyncio
async def test_dispatch_comments(reddit_mock) -> None:
    from app import RedditDispatcher
    dispatcher = RedditDispatcher(reddit_mock, TEST_CONFIG)

    with requests_mock.mock() as endpoint:
        # Create a mock API endpoint
        endpoint.register_uri("POST", TEST_CONFIG["comment_endpoint"])
        # Replace the subreddit stream with a proper mock
        await dispatcher._get_subreddit()
        dispatcher._subreddit_object.stream = SubredditStream()
        # Stream fake comments
        await dispatcher._stream_comments()
        # Clean up
        await dispatcher.reddit.close()
        # Assertions
        assert endpoint.called
        assert endpoint.call_count == 3
        for i in range(len(SubredditStream.fake_comments)):
            assert \
                SubredditStream.fake_comments[i].id == \
                endpoint.request_history[i].json().get("id")
            sent_properties = [
                property
                for property in SubredditStream.fake_comments[i].__dict__
                if not property.startswith('_')
            ]
            received_properties = [
                property
                for property in endpoint.request_history[i].json()
            ]
            assert sent_properties == received_properties


@pytest.mark.asyncio
async def test_dispatch_submissions(reddit_mock) -> None:
    from app import RedditDispatcher
    dispatcher = RedditDispatcher(reddit_mock, TEST_CONFIG)

    with requests_mock.mock() as endpoint:
        # Create a mock API endpoint
        endpoint.register_uri("POST", TEST_CONFIG["submission_endpoint"])
        # Replace the subreddit stream with a proper mock
        await dispatcher._get_subreddit()
        dispatcher._subreddit_object.stream = SubredditStream()
        # Stream fake submissions
        await dispatcher._stream_submissions()
        # Clean up
        await dispatcher.reddit.close()
        # Assertions
        assert endpoint.called
        assert endpoint.call_count == 3
        for i in range(len(SubredditStream.fake_submissions)):
            assert \
                SubredditStream.fake_submissions[i].id == \
                endpoint.request_history[i].json().get("id")
            sent_properties = [
                property
                for property in SubredditStream.fake_submissions[i].__dict__
                if not property.startswith('_')
            ]
            received_properties = [
                property
                for property in endpoint.request_history[i].json()
            ]
            assert sent_properties == received_properties
