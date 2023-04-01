import random
import string


class Comment:
    """
    https://github.com/praw-dev/asyncpraw/blob/926d809c92a7364985db90f2d878c597ae317cb1/asyncpraw/models/reddit/comment.py#L23
    """
    def __init__(self):
        self.author = ""
        self.body = ""
        self.body_html = ""
        self.created_utc = 0.0
        self.distinguished = ""
        self.edited = ""
        self.id = "".join(random.choice(string.ascii_lowercase +
                          string.digits) for x in range(6))
        self.is_submitter = ""
        self.link_id = ""
        self.parent_id = ""
        self.permalink = ""
        self.replies = None
        self.saved = ""
        self.score = ""
        self.stickied = ""
        self.submission = ""
        self.subreddit = None
        self.subreddit_id = ""
