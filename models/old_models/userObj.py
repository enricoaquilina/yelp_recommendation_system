class UserObject(object):

    """
    Attributes:
        id
        name
        type
    """
    def __init__(self,id, name, type):
        self.id = id
        self.name = name
        self.type = type


    def serialize(self):
        return{
            'id':self.id,
            'name': self.name,
            'type': self.type,
        }
    # def __repr__(self):
    #     return "\n----------------USER-----------------\nid: %s \nname: %s\ntype: %s\n"%\
    #            (self.id, self.name.encode('ascii', 'ignore'),self.type)
    #def deposit(self, amount):
    #    """Return the balance remaining after depositing *amount*
    #    dollars."""
    #    self.balance += amount
    #    return self.balance