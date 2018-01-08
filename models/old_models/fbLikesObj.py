class FBLikesObject(object):

    """
    Attributes:
        user_id
        name
    """

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __repr__(self):
        return "\n----------------FB Like-----------------\nuser_id: %s \nname: %s\n"%\
               (self.user_id, self.name)
