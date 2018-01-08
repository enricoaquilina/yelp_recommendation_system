class MovieObject(object):

    """
    Attributes:
        title
        year
    """
    def __init__(self,title, year, genre, plot, poster):
        self.title = title
        self.year = year
        self.genre = genre.split(',')
        self.plot = plot
        self.poster = poster

    def __repr__(self):
        return "\n----------------MOVIE-----------------\ntitle: %s \nyear: %s\ngenre: %s\nplot: %s\nposter: %s\n"%\
               (self.title, self.year,self.genre,self.plot,self.poster)
    #def deposit(self, amount):
    #    """Return the balance remaining after depositing *amount*
    #    dollars."""
    #    self.balance += amount
    #    return self.balance