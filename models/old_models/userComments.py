from flask import jsonify

class UserComments(object):

    """
    Attributes:
        user_name
        user_id
        user_type
        comments
    """
    def __init__(self,user_name,user_id, user_type):
        self.user_name = user_name
        self.user_id = user_id
        self.user_type = user_type
        self.comments = []

    def addComment(self,comment):
        self.comments.append(comment)

    def serialize(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_type': self.user_type,
            'comments': ([comment.serialize() for comment in self.comments])
        }

    #def deposit(self, amount):
    #    """Return the balance remaining after depositing *amount*
    #    dollars."""
    #    self.balance += amount
    #    return self.balance