#!/usr/bin/python
from numpy import matrix
from pandas import DataFrame
from mapReduce.MRNeighbours import MRNeighbours
from mapReduce.mrService import get_similar_viewing_users,get_user_movie_ratings_from_db,output_similarities_to_file, add_neighbours,get_users_without_neighbours
from mapReduce.mapperInput import MapperOutput
from mapReduce.mrRunner import get_neighbours_for_all,get_neighbours_for_user
from scipy import spatial

if __name__ == "__main__":

    get_neighbours_for_all()
