class ReccommendObject(object):

    """
    Attributes:
        rating
        similarity
    """
    def __init__(self,rating, similarity):
        self.rating = rating
        self.similarity = similarity

    #def deposit(self, amount):
    #    """Return the balance remaining after depositing *amount*
    #    dollars."""
    #    self.balance += amount
    #    return self.balance