from services.sentimentService import get_sentiment_polarity,get_sentiment_score
class FBCommentsObject(object):
    """
        Attributes:
            date
            comment
            fb_comment_id
            id
            user_name
        """

    def __init__(self, date, comment, fb_comment_id, user_id, user_name):
        self.date = date
        self.comment = comment
        self.fb_comment_id = fb_comment_id
        self.user_id = user_id
        self.user_name = user_name
        self.polarity = get_sentiment_polarity(self.comment)
        self.sentiment_score = get_sentiment_score(self.comment, self.polarity)

    def __repr__(self):
        return "\n----------------FB Comment-----------------\ndate: %s \ncomment: %s\nfb_comment_id: %s\nuser_id: %s\nuser_name: %s\n" % \
               (self.date, self.comment, self.fb_comment_id, self.user_id, self.user_name)
