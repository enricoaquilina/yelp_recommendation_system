from services.sentimentService import get_sentiment_polarity,get_sentiment_score
class YoutubeComment(object):

    """
    Attributes:
        id
        authorId
        authorName
        text:
        publishedAt
        videoId
        sentiment
    """

    def __init__(self,id, videoId, authorId, authorName, commentText, publishedDate):
        """Return a Customer object whose name is *name*."""
        self.id = id
        self.videoId = videoId
        self.authorId = authorId
        self.authorName = authorName
        self.commentText = commentText
        self.publishedDate = publishedDate
        self.polarity = get_sentiment_polarity(self.commentText)
        self.sentiment_score = get_sentiment_score(self.commentText, self.polarity)


    def __repr__(self):
        return "\n----------------COMMENT-----------------\ncommentId: %s videoId: %s \nauthor Name: %s (%s) \npublished on %s \n%s "% \
               (self.id, self.videoId, self.authorName.encode('ascii', 'ignore'), self.authorId, self.publishedDate.encode('ascii', 'ignore'), self.commentText.encode('ascii', 'ignore'))
    #def deposit(self, amount):
    #    """Return the balance remaining after depositing *amount*
    #    dollars."""
    #    self.balance += amount
    #    return self.balance