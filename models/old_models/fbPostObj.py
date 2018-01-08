class FBPostObject(object):

    """
    Attributes:
        type
        Message
        fb_post_id
        Link
        name
    """

    def __init__(self, type, name, message, fb_post_id, link):
        self.type = type
        self.name = name
        self.message = message
        self.fb_post_id = fb_post_id
        self.link = link

    def __repr__(self):
        return "\n----------------FB Post-----------------\nType: %s \nMessage: %s\nFBPostID: %s\nLink: %s\nName: %s\n"%\
               (self.type, self.message,self.fb_post_id,self.name)
