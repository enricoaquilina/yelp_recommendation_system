#!/usr/bin/python
#import relationships as relationships
from py2neo import Graph, Node, Relationship
from mapperInput import MapperInput
from operator import itemgetter

YOUTUBE_USER = "YoutubeUser"
FB_USER = "FBUser"
YOUTUBE_VIDEO = "YoutubeVideo"
YOUTUBE_COMMENT = "Youtube_Comment"
MOVIE_DETAILS = "MovieDetails"
FB_POST = "FBPost"
HAS_TRAILER = "Has_Trailer"
COMMENTED = "COMMENTED"
LIKES = "LIKES"
LINKED_VIDEO = "LINKED_VIDEO"
LINKED_IN = "LINKED_IN"
HAS_NEIGHBOUR = "HAS_NEIGHBOUR"

def startConnection():
    graph = Graph("http://localhost:7474/db/data", password="123456")#Graph("bigData")
    return graph

#get user movie ratings
def get_users_without_neighbours():
    userComments = []
    graph = startConnection()
    query = "MATCH (user) WHERE (user:"+YOUTUBE_USER+" OR user:"+FB_USER+") AND  (NOT ((user)-[:"+HAS_NEIGHBOUR+"]->()))\
            RETURN user.id, labels(user)"

    user_ids = []
    users = graph.run(query)
    while users.forward():
        current_cursor =users.current()
        user_ids.append((current_cursor["user.id"],current_cursor["labels(user)"][0]))

    return user_ids

#get user movie ratings
def get_user_movie_ratings_from_db(user_id, type):
    userComments = []
    graph = startConnection()
    if type == YOUTUBE_USER:
        userComments = get_youtube_user_movie_ratings_from_db(graph,user_id)
    else:
        userComments = get_facebook_user_movie_ratings_from_db(graph, user_id)

    return userComments

#get user movie ratings for facebook users
def get_facebook_user_movie_ratings_from_db(graph, user_id):
    user_comments = []
    query = "MATCH (n:"+FB_USER+")-[yc]->(p:"+FB_POST+")\
            Where n.id = '"+user_id+"'\
            OPTIONAL MATCH (p)<-[lv:LINKED_IN]-(trl)\
            RETURN n,yc,p,lv,trl"

    videos = graph.run(query)

    while videos.forward():
        current_cursor =videos.current()
        user = current_cursor[0] #user node
        if current_cursor[3] is not None:
            fb_comment = current_cursor[1]
            trailer_det = current_cursor[4]
            current_comment = MapperInput(user['id'], trailer_det["id"],fb_comment["sentiment_score"])

            user_comments.append(current_comment)

    return user_comments

#get user movie ratings for youtube users
def get_youtube_user_movie_ratings_from_db(graph, user_id):
    user_comments = []
    query = "MATCH (n:"+YOUTUBE_USER+")-[r:"+YOUTUBE_COMMENT+"]->(y) \
             WHERE n.id = '"+user_id+"'\
             RETURN n,r,y;"

    videos = graph.run(query)

    while videos.forward():
        current_cursor = videos.current()
        user = current_cursor[0]  # user node
        comment = current_cursor[1]
        video = current_cursor[2]

        current_comment = MapperInput(user['id'], video["id"], comment["sentiment_score"])
        user_comments.append(current_comment)

        #videos.current()[0] returns user node
        #videos.current()[1] returns relationship node
        # videos.current()[2] returns video node
        #print [act for act in accounts]
    return user_comments


#get list of users and their comments on (posts or trailers)
#get list of trailer ids and post ids which the user commented on
def get_similar_viewing_users(user_id, type):
    trailer_ids = []
    fb_posts_ids = []
    graph = startConnection()

    #if user_id == '10212958722620086':
    #    print user_id
    #get the ratings that the user gave for the movies he commented on
    user_ratings = get_user_movie_ratings_from_db(user_id,type)

    #get the trailer ids and post ids which match the movies that the user commented on
    if type == YOUTUBE_USER:
        query = "MATCH (user:"+YOUTUBE_USER+")-[comment:"+YOUTUBE_COMMENT+"]->(trailer:"+YOUTUBE_VIDEO+") \
                WHERE user.id = '"+user_id+"'\
                OPTIONAL MATCH (trailer)-[lv:"+LINKED_IN+"]->(post:"+FB_POST+")\
                Return trailer.id,post.fb_post_id"
    else:
        query = "MATCH (user:"+FB_USER+")-[comment:"+COMMENTED+"]->(post:"+FB_POST+") \
                WHERE user.id = '"+user_id+"'\
                OPTIONAL MATCH (post)-[lv:"+LINKED_VIDEO+"]->(trailer:"+YOUTUBE_VIDEO+")\
                Return trailer.id,post.fb_post_id"

    videos = graph.run(query)

    while videos.forward():
        trailer = videos.current()
        trailer_ids.append(trailer['trailer.id'])
        fb_posts_ids.append(trailer['post.fb_post_id'])

    similar_movies_threshold = get_threshold_allowed(len(trailer_ids))

    #iteratively reduce threshold if no similar users are found
    similar_users_and_comments = []
    while len(similar_users_and_comments) == 0:
        similar_fbusers_and_comments = get_facebook_similar_viewing_users(graph,user_id,fb_posts_ids, user_ratings, similar_movies_threshold)
        similar_yusers_and_comments = get_youtube_similar_viewing_users(graph, user_id,trailer_ids, user_ratings, similar_movies_threshold)

        similar_users_and_comments = similar_fbusers_and_comments + similar_yusers_and_comments
        similar_movies_threshold = similar_movies_threshold-1


    return similar_users_and_comments


#get similar users and their
#params user_Id - the user we are reccommending for, such that it is not returned as part of the similar users
#post_Ids the posts which the user to reccommend commented on
#user_ratings ar ethe ratings of the user such that they can be added to the ratings of the similar users
def get_facebook_similar_viewing_users(graph, user_id, post_ids, user_ratings,similar_movies_threshold):
    posts_string = '\',\''.join(str(e) for e in post_ids)

    userIds_list = []

    users = get_fb_similar_viewing_users_query(graph, user_id, posts_string, similar_movies_threshold)

    #get all similar users Ids
    while users.forward():
        similar_user = users.current()
        similar_user = similar_user[0]

        userIds_list.append(similar_user['id'])

    #get the user IDs and their rating on the movies, which are the same to those rated by the user
    similar_users_and_comments = get_fb_userlist_movies_from_db(graph,userIds_list, posts_string, user_ratings)

    return similar_users_and_comments

#create the query and coll the database, done separately such that it can be called in repetition
def get_fb_similar_viewing_users_query(graph, user_id, posts_string,similar_movies_threshold):
    query2 = "MATCH (user:" + FB_USER + ")-[comment:" + COMMENTED + "]->(post:" + FB_POST + ")\
                    WHERE user.id <> '" + user_id + "' AND post.fb_post_id IN [\'" + posts_string + "\']\
                    WITH user, collect(post) as posts\
                    WHERE size(posts) >= " + str(similar_movies_threshold) + "\
                    RETURN user"


    users = graph.run(query2)
    return users

#given a user, get the movies and ratings commented on by all the similar users
def get_fb_userlist_movies_from_db(graph, user_list_ids, posts_string, user_ratings):
    userComments = []
    userIds_string = '\',\''.join(str(e) for e in user_list_ids)
    query = "MATCH (n:"+FB_USER+")-[r:"+COMMENTED+"]->(p:"+FB_POST+") WHERE n.id IN ['"+userIds_string+"'] AND p.fb_post_id IN [\'"+posts_string+"\']\
             OPTIONAL MATCH (p)<-[lv:"+LINKED_IN+"]-(trl)\
             RETURN n,r,p,lv,trl"

    videos = graph.run(query)

    while videos.forward():
        current_cursor =  videos.current()
        user = current_cursor[0] #user node
        if current_cursor[3] is not None:
            fb_comment = current_cursor[1]
            trailer_det = current_cursor[4]

            fb_sentiment_score = fb_comment["sentiment_score"]
            if fb_sentiment_score is None:
                print user

            matching_user_rating = get_user_rating_by_movie(user_ratings,trailer_det["id"])
            if matching_user_rating is None:
                print user


            current_comment = MapperInput(user['id'], trailer_det["id"],fb_sentiment_score)
            current_comment.set_similar_user_rating(matching_user_rating)
            userComments.append(current_comment)

    return userComments


def get_youtube_similar_viewing_users(graph, user_id, trailerIds, user_ratings, similar_movies_threshold):
    trailers_string = '\',\''.join(str(e) for e in trailerIds)

    userIds_list = []

    users = get_yt_similar_viewing_users_query(graph, user_id, trailers_string, similar_movies_threshold)

    while users.forward():
        similar_user = users.current()
        similar_user = similar_user[0]
        userIds_list.append(similar_user['id'])

    similar_users_and_comments = get_userlist_movies_from_db(graph,userIds_list,trailers_string, user_ratings)

    return similar_users_and_comments


#method which simply contains the query and runs it on demand
def get_yt_similar_viewing_users_query(graph, user_id, trailers_string,similar_movies_threshold):

    query2 = "MATCH (user:"+YOUTUBE_USER+")-[comment:"+YOUTUBE_COMMENT+"]->(trailer:YoutubeVideo)\
                WHERE user.id <> '"+user_id+"' AND trailer.id IN [\'"+trailers_string+"\']\
                WITH user, collect(trailer) as trailers\
                WHERE size(trailers) >= "+str(similar_movies_threshold)+"\
                RETURN user"

    users = graph.run(query2)
    return users


def get_userlist_movies_from_db(graph,user_list_ids,trailers_string, user_ratings):
    userComments = []
    userIds_string = '\',\''.join(str(e) for e in user_list_ids)
    query = "MATCH (n:"+YOUTUBE_USER+")-[r:"+YOUTUBE_COMMENT+"]->(y:"+YOUTUBE_VIDEO+") \
             WHERE n.id IN ['"+userIds_string+"'] AND y.id IN [\'"+trailers_string+"\']\
             RETURN n,r,y;"
    videos = graph.run(query)

    while videos.forward():
        current_cursor = videos.current()
        user = current_cursor[0]  # user node
        comment = current_cursor[1]
        video = current_cursor[2]

        sentiment_score = comment["sentiment_score"]
        if sentiment_score is None:
            print user

        matching_user_rating = get_user_rating_by_movie(user_ratings, video["id"])
        if matching_user_rating is None:
            print user

        current_comment = MapperInput(user['id'], video["id"], sentiment_score)
        current_comment.set_similar_user_rating(matching_user_rating)
        userComments.append(current_comment)

    return userComments


#given a list of user ratings and movie id
#return the rating for that movie Id
def get_user_rating_by_movie(user_rating,movie_id):
    for rating in user_rating:
        if rating.movie_id == movie_id:
            return rating.rating

def get_threshold_allowed(movies_interacted):
    similar_movies = 1

    if movies_interacted < 6:
        similar_movies = movies_interacted
    elif movies_interacted < 10:
        allow_similar = movies_interacted * 0.8
        similar_movies = int(round(allow_similar))
    else: # > 9
        allow_similar = movies_interacted * 0.6
        similar_movies = int(round(allow_similar))

    return similar_movies


def output_similarities_to_file(similarity_list):
    file = open("similarities.txt","w")
    for item in similarity_list:
        file.write("{0}|{1}|{2}|{3}\n".format(item.user_id,item.movie_id, item.rating,item.comparing_rating))

def add_neighbours(neighbour_list, user_id_to_reccommend, type):
    graph = startConnection()
    allowed_neighbours = 3

    neighbour_list = sorted(neighbour_list, key=lambda x:x.similarity, reverse=True)
    if len(neighbour_list) < allowed_neighbours:
        allowed_neighbours = len(neighbour_list)

    y_user = list(graph.find(type, property_key="id", property_value=user_id_to_reccommend))

    if len(y_user) > 0:
        user_to_reccommend = y_user[0]

        count = 0
        for neighbour in neighbour_list:

            if count == allowed_neighbours:
                break

            neighb = list(graph.find(YOUTUBE_USER, property_key="id", property_value=neighbour.user_id))
            if len(neighb) == 0:
                neighb= list(graph.find(FB_USER, property_key="id", property_value=neighbour.user_id))

            if len(neighb) > 0:
                neighb = neighb[0]

                rel = Relationship(user_to_reccommend,
                                   HAS_NEIGHBOUR,
                                   neighb)
                rel["similarity"] = neighbour.similarity
                graph.create(rel)

                count = count + 1
    return


