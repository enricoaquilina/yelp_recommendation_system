class UserModel(object):
    """
    Attributes:
        user_id
        name
        review_count
        average_stars
    """

    def __init__(self, user_id, name, review_count, average_stars):
        self.user_id = user_id
        self.name = name
        self.review_count = review_count
        self.average_stars = average_stars

    def serialize(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'review_count': self.review_count,
            'average_stars': self.average_stars
        }
