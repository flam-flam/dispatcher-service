from .subreddit import Subreddit


class Reddit:
    """
    https://asyncpraw.readthedocs.io/en/stable/code_overview/reddit/subreddit.html
    """
    def __init__(
        self,
        client_id: str = "",
        client_secret: str = "",
        user_agent: str = "",
        redirect_uri: str = ""
    ):
        assert isinstance(client_id, str) and len(client_id) > 0
        assert isinstance(client_secret, str) and len(client_secret) > 0
        assert isinstance(user_agent, str) and len(user_agent) > 0
        assert isinstance(redirect_uri, str) and len(redirect_uri) > 0

    async def subreddit(self, display_name) -> Subreddit:
        return Subreddit()

    async def close(self) -> None:
        pass
