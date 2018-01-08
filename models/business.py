class BusinessModel(object):

    """
    Attributes:
        business_id
        name
        star_rating
        city
        state
        review_count
        latitude
        longitude
    """
    def __init__(self, business_id, name, star_rating, city, state, review_count, latitude, longitude):
        self.business_id = business_id
        self.name = name
        self.star_rating = star_rating
        self.city = city
        self.state = state
        self.review_count = review_count
        self.latitude = latitude
        self.longitude = longitude

    def serialize(self):
        return {
            'business_id': self.business_id,
            'name': self.name,
            'star_rating': self.star_rating,
            'city': self.city,
            'state': self.state,
            'review_count': self.review_count,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

