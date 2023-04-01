import random
import string


class Submission:
    """
    https://github.com/praw-dev/asyncpraw/blob/926d809c92a7364985db90f2d878c597ae317cb1/asyncpraw/models/reddit/submission.py#L409
    """
    def __init__(self):
        self.author = ""
        self.author_flair_text = ""
        self.clicked = ""
        self.comments = ""
        self.created_utc = 0.0
        self.distinguished = ""
        self.edited = ""
        self.id = "".join(random.choice(string.ascii_lowercase +
                          string.digits) for x in range(6))
        self.is_original_content = ""
        self.is_self = ""
        self.link_flair_template_id = ""
        self.link_flair_text = ""
        self.locked = ""
        self.name = ""
        self.num_comments = ""
        self.over_18 = ""
        self.permalink = ""
        self.poll_data = ""
        self.saved = ""
        self.score = ""
        self.selftext = ""
        self.spoiler = ""
        self.stickied = ""
        self.subreddit = None
        self.title = ""
        self.upvote_ratio = ""
        self.url = ""
