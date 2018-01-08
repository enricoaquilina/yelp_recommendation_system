class ReccomendedMovie(object):

    """
    Attributes:
        title, year, genre, plot, poster, youtube_trailer_name, youtube_id, comment, polarity, sentiment
    """
    def __init__(self, youtube_id, title, year, genre, plot,poster,link,youtube_description, predicted_rating):
        self.youtube_id = youtube_id
        self.title = title
        self.year = year
        self.genre = genre
        self.plot = plot
        self.poster = poster
        self.link= link
        self.youtube_description = youtube_description
        self.predicted_rating = predicted_rating

    def serialize(self):
        return {
            'youtube_id': self.youtube_id,
            'title': self.title,
            'year': self.year,
            'genre': self.genre,
            'plot': self.plot,
            'poster': self.poster,
            'link': self.link,
            'youtube_description': self.youtube_description,
            'predicted_rating': self.predicted_rating
        }

