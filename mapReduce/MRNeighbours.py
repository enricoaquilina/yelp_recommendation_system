from mrjob.job import MRJob
from mrService import get_user_movie_ratings_from_db
from scipy import spatial
from scipy.stats import pearsonr
import numpy
import re
import math

WORD_RE = re.compile(r"[\w']+")


class MRNeighbours(MRJob):
    #INPUT_PROTOCOL = JSONProtocol

    def mapper(self, _, line):
        tokens = line.split('|')
        yield (tokens[0], [tokens[2], tokens[3]])


    def reducer(self, userId, ratings):
        this_user_ratings = []
        to_reccomend_ratings = []

        for rating in ratings:
            this_user_ratings.append(rating[0])
            to_reccomend_ratings.append(rating[1])
        if to_reccomend_ratings == 'None':
            print(to_reccomend_ratings)
        this_user_ratings = numpy.array(this_user_ratings, dtype=int)
        to_reccomend_ratings = numpy.array(to_reccomend_ratings, dtype=int)

        for r in this_user_ratings: print("user {0} ".format(r))
        for r in to_reccomend_ratings: print("user- {0} ".format(r))

        # perform pearson correlation, if it crashes, in cases where the movies of a particular neighbour are all rated the same
        # use cosine similarity
        try:
            pears_correlation = pearsonr(this_user_ratings, to_reccomend_ratings)
            correlation = pears_correlation[0]
            if math.isnan(correlation):
                correlation = spatial.distance.cosine(this_user_ratings, to_reccomend_ratings)
        except Exception, e:
            correlation = spatial.distance.cosine(this_user_ratings, to_reccomend_ratings)
        except Warning, w:
            correlation = spatial.distance.cosine(this_user_ratings, to_reccomend_ratings)

        print(correlation)


        yield (userId, correlation)


if __name__ == '__main__':
    MRNeighbours.run()
