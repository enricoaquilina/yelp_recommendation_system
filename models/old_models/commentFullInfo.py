class CommentFullInfo(object):

    """
    Attributes:
        title, year, genre, plot, poster, youtube_trailer_name, youtube_id, comment, polarity, sentiment
    """
    def __init__(self, youtube_trailer_name, youtube_id, comment, polarity, sentiment):
        self.title = ""
        self.year = ""
        self.genre = "".split(',')
        self.plot = ""
        self.poster = ""
        self.youtube_trailer_name = youtube_trailer_name
        self.youtube_id = youtube_id
        self.comment= comment
        self.polarity = polarity
        self.sentiment = sentiment

    def set_movie_details(self,title, year, genre, plot, poster):
        self.title = title
        self.year = year
        self.genre = genre
        self.plot = plot
        self.poster = poster

    def serialize(self):
        return {
            'movie_title': self.title,
            'movie_year': self.year,
            'movie_genres': self.genre,
            'movie_plot': self.plot,
            'movie_poster': self.poster,
            'trailer_name': self.youtube_trailer_name,
            'trailer_id': self.youtube_id,
            'user_comment': self.comment,
            'comment_polarity': self.polarity,
            'comment_sentiment': self.sentiment
        }


    #def deposit(self, amount):
    #    """Return the balance remaining after depositing *amount*
    #    dollars."""
    #    self.balance += amount
    #    return self.balance