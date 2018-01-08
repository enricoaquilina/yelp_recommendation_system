#!/usr/bin/python
from mapReduce.MRNeighbours import MRNeighbours
from mapReduce.mrService import get_similar_viewing_users,get_user_movie_ratings_from_db,output_similarities_to_file, add_neighbours,get_users_without_neighbours
from mapReduce.mapperInput import MapperOutput

ITERATE_COUNT = 1
# everything is called from here
# once posts are obtained from fb, the video ids are extracted into a
# list and fed to method get_video_details instead of the hardcoded list
# this method retreives video data from youtube

def get_neighbours_for_all():
    users = get_users_without_neighbours()

    count = 0
    for user in users:

        #if count == ITERATE_COUNT:
         #   break

        user_id = user[0]
        user_type = user[1]
        similar_users = get_similar_viewing_users(user_id, user_type)

        output_similarities_to_file(similar_users)

        similar_users = []
        # mr_job = MRNeighbours(args=['-r', 'inline'])
        mr_job = MRNeighbours(args=['similarities.txt'])

        # mr_job = MRNeighbours()
        with mr_job.make_runner() as runner:
            runner.run()
            for line in runner.stream_output():
                key, value = mr_job.parse_output_line(line)
                similar_users.append(MapperOutput(key, value))
                print "Key: {0} Correlation: {1} ".format(key, value)

        add_neighbours(similar_users, user_id, user_type)
        count = count+1

def get_neighbours_for_user(user_id, user_type):

    similar_users = get_similar_viewing_users(user_id, user_type)

    output_similarities_to_file(similar_users)

    similar_users = []
    # mr_job = MRNeighbours(args=['-r', 'inline'])
    mr_job = MRNeighbours(args=['similarities.txt'])

    # mr_job = MRNeighbours()
    with mr_job.make_runner() as runner:
        runner.run()
        for line in runner.stream_output():
            key, value = mr_job.parse_output_line(line)
            similar_users.append(MapperOutput(key, value))
            print "Key: {0} Correlation: {1} ".format(key, value)

    add_neighbours(similar_users, user_id, user_type)