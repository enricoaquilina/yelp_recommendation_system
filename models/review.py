from services.sentimentService import get_sentiment_polarity, get_sentiment_score


class ReviewModel(object):

    """
    Attributes:
        review_id
        business_id
        author_id
        author_name
        text
        published_date
        polarity
        sentiment_score
    """

    def __init__(self, review_id, author_id, author_name, business_id, text, published_date):
        self.review_id = review_id
        self.business_id = business_id
        self.author_id = author_id
        self.author_name = author_name
        self.text = text
        self.published_date = published_date
        self.polarity = get_sentiment_polarity(self.text)
        self.sentiment_score = get_sentiment_score(self.text, self.polarity)
        # self.stars = stars

    def __repr__(self):
        return "\n----------------REVIEW-----------------\nreviewId: %s businessId: %s \nauthor Name: %s (%s) \npublished on %s \n%s " % \
               (self.review_id, self.business_id, self.author_name.encode('ascii', 'ignore'), self.author_id,
                self.published_date.encode('ascii', 'ignore'), self.text.encode('ascii', 'ignore'))

    def serialize(self):
        return {
            'review_id': self.review_id,
            'business_id': self.business_id,
            'author_id': self.author_id,
            'author_name': self.author_name,
            'text': self.text,
            'published_date': self.published_date,
            'polarity': self.polarity,
            'sentiment_score': self.sentiment_score
        }
