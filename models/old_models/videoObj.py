class VideoObject(object):

    """
    Attributes:
        Id
        title
        publishedAt
        description
        link
    """

    def __init__(self,id, title, description, publishedDate):
        """Return a Customer object whose name is *name*."""
        self.id = id
        self.title = title
        self.description = description
        self.publishedDate = publishedDate

    def __repr__(self):
        return "\n----------------VIDEO-----------------\nvideoId: %s \nTitle : %s \ndescription %s\npublished on %s \n"% \
               (self.id, self.title, self.description.encode('ascii', 'ignore'), self.publishedDate.encode('ascii', 'ignore'))
    #def deposit(self, amount):
    #    """Return the balance remaining after depositing *amount*
    #    dollars."""
    #    self.balance += amount
    #    return self.balance