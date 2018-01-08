class MapperInput(object):

    """
    Attributes:
        user_id
        ratings
    """
    def __init__(self, user_id, movie_id, rating):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating

    def set_similar_user_rating(self, comparing_rating):
        self.comparing_rating = comparing_rating

    def serialize(self):
        return {
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'rating': self.rating
        }


class MapperOutput(object):

    """
    Attributes:
        user_id
        similarity
    """
    def __init__(self, user_id, similarity):
        self.user_id = user_id
        self.similarity = similarity

    def serialize(self):
        return {
            'user_id': self.user_id,
            'similarity': self.similarity
        }
