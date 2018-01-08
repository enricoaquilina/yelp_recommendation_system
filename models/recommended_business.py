class recommended_business_model(object):

    """
    Attributes:
        id
        business_name
        star_rating
        city
        predicted_rating
    """
    def __init__(self, bid, business_name, star_rating, city, predicted_rating):
        self.id = bid
        self.business_name = business_name
        self.star_rating = star_rating
        self.city = city
        self.predicted_rating = predicted_rating

    def serialize(self):
        return {
            'id': self.bid,
            'business_name': self.business_name,
            'star_rating': self.star_rating,
            'city': self.city,
            'predicted_rating': self.predicted_rating
        }
