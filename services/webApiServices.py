# #!/usr/bin/python
#
# from neoServices import  startConnection, YOUTUBE_USER, YOUTUBE_COMMENT,HAS_TRAILER, \
#     MOVIE_DETAILS,FB_USER,COMMENTED, FB_POST,YOUTUBE_VIDEO,LINKED_VIDEO,LINKED_IN, get_video_node, \
#     insert_user
# from models.user import  UserObject
# from models.userComments import UserComments
# from models.old_models.commentFullInfo import CommentFullInfo
# from models.recommended_business import ReccommendObject
# from models.youtubeComment import YoutubeComment
# from mapReduce.mrService import get_user_movie_ratings_from_db, HAS_NEIGHBOUR
# from random import randint
# import numpy
# from models.business import ReccomendedMovie
#
# YOUTUBE_BASE = "https://www.youtube.com/watch?v="
#
#
# def get_all_users():
#     accounts = []
#     graph = startConnection()
#     for user in graph.find(YOUTUBE_USER):
#         account = UserObject(user["id"],
#                             user["authorName"],
#                             YOUTUBE_USER)
#         accounts.append(account)
#
#     for user in graph.find(FB_USER):
#         account = UserObject(user["id"],
#                             user["name"],
#                              FB_USER)
#         accounts.append(account)
#
#     print [act for act in accounts]
#     return accounts
#
# def get_all_users(name):
#     accounts = []
#     graph = startConnection()
#
#     query = "MATCH (user:"+YOUTUBE_USER+")\
#             Where toLower(user.authorName) CONTAINS  toLower('"+name+"')\
#             RETURN user"
#
#     for user in graph.run(query):
#         account = UserObject(user[0]["id"],
#                             user[0]["authorName"],
#                             YOUTUBE_USER)
#         accounts.append(account)
#
#     query = "MATCH (user:" + FB_USER + ")\
#                 Where toLower(user.name) CONTAINS  toLower('" + name + "')\
#                 RETURN user"
#
#     for user in graph.run(query):
#         account = UserObject(user[0]["id"],
#                             user[0]["name"],
#                              FB_USER)
#         accounts.append(account)
#
#     print [act for act in accounts]
#     return accounts
#
# #not used
# def get_user_movies_from_db(user_id, type):
#     accounts = []
#     graph = startConnection()
#
#     users = list(graph.find(YOUTUBE_USER, property_key="id", property_value=user_id))
#     if len(users):
#         user_node = users[0]
#         relationships = list(graph.match(start_node=user_node, rel_type=YOUTUBE_COMMENT))
#         for relation in relationships:
#             print relation
#
#
#     return accounts
#
# def get_user_movies_from_db2(user_id, type):
#     userComments = []
#     graph = startConnection()
#     if type == YOUTUBE_USER:
#         userComments = get_youtube_user_movies_from_db(graph, user_id, type)
#     else:
#         userComments = get_facebook_user_movies_from_db(graph, user_id, type)
#
#     return userComments
#
#
# def get_facebook_user_movies_from_db(graph, user_id, type):
#     userComments = []
#     query = "MATCH (n)-[yc]->(p:"+FB_POST+")\
#             Where n.id = '"+user_id+"'\
#             OPTIONAL MATCH (p)<-[lv:LINKED_IN]-(trl)<-[ht:Has_Trailer*0..1]-(tr:MovieDetails)\
#             RETURN n,yc,p,lv,trl,ht,tr"
#
#     #query = "MATCH (n)-[r:"+COMMENTED+"]->(y) WHERE n.id = '"+user_id+"' OPTIONAL MATCH (y)<-[ht:"+HAS_TRAILER+"*0..1]-(tr:"+MOVIE_DETAILS+") " \
#     #                                                        "RETURN n,r,y,ht,tr;"
#     videos = graph.run(query)
#
#     current_user = None
#     while videos.forward():
#         try:
#             current_cursor =  videos.current()
#             user = current_cursor[0] #user node
#             if current_user is None:
#                 current_user = UserComments(user['name'],user['id'],type)
#                 userComments.append(current_user)
#             elif current_user.user_id != user['id']:
#                 if any(x for x in userComments if x.user_id == user['id']):
#                     for userComment in userComments:
#                         if userComment.user_id == user['id']:
#                             current_user = userComment
#
#                 else:
#                     current_user = UserComments(user['name'], user['id'], type)
#                     userComments.append(current_user)
#
#             relationship = current_cursor[1]#youtube comment or like relationship
#             post = current_cursor[2]#fb post node
#             youtube_vid = current_cursor[4]  # fb post node
#             current_comment = CommentFullInfo(post['name'], youtube_vid['id'], relationship['comment'], relationship['polarity']
#                                               , relationship['sentiment_score'])
#             if current_cursor[3] is not None and current_cursor[5] is not None:
#                 #if post has a video relation and video has details relation, get movie details
#                 trailer_det = current_cursor[6]
#                 current_comment.set_movie_details(trailer_det['title'],trailer_det['year'],trailer_det['genre'],trailer_det['plot'],trailer_det['poster'])
#
#
#             current_user.addComment(current_comment)
#         except Exception, e:
#             print "Error"
#     return userComments
#
#
# def get_youtube_user_movies_from_db(graph, user_id, type):
#     userComments = []
#     query = "MATCH (n)-[r:"+YOUTUBE_COMMENT+"]->(y) WHERE n.id = '"+user_id+"' OPTIONAL MATCH (y)<-[ht:"+HAS_TRAILER+"*0..1]-(tr:"+MOVIE_DETAILS+") " \
#                                                             "RETURN n,r,y,ht,tr;"
#     videos = graph.run(query)
#
#     current_user = None
#     while videos.forward():
#         current_cursor =  videos.current()
#         user = current_cursor[0] #user node
#         if current_user is None:
#             current_user = UserComments(user['authorName'],user['id'],type)
#             userComments.append(current_user)
#         elif current_user.user_id != user['id']:
#             if any(x for x in userComments if x.user_id == user['id']):
#                 for userComment in userComments:
#                     if userComment.user_id == user['id']:
#                         current_user = userComment
#
#             else:
#                 current_user = UserComments(user['authorName'], user['id'], type)
#                 userComments.append(current_user)
#
#         relationship = current_cursor[1]#youtube comment relationship
#         trailer = current_cursor[2]#youtube trailer node
#         current_comment = CommentFullInfo(trailer['title'], trailer['id'], relationship['commentText'], relationship['polarity']
#                                           , relationship['sentiment_score'])
#         if current_cursor[3] is not None:#if has trailer relation exists get movie details
#             trailer_det = current_cursor[4]
#             current_comment.set_movie_details(trailer_det['title'],trailer_det['year'],trailer_det['genre'],trailer_det['plot'],trailer_det['poster'])
#
#
#         current_user.addComment(current_comment)
#         #videos.current()[0] returns user node
#         #videos.current()[1] returns relationship node
#         # videos.current()[2] returns video node
#         #print [act for act in accounts]
#     return userComments
#
# #get list of commented on posts or trailers and get users which have commented in the same posts and trailers
# def get_similar_viewing_users(user_id, type):
#     trailerIds = []
#     fb_posts_Ids = []
#     graph = startConnection()
#
#     if type == YOUTUBE_USER:
#         query = "MATCH (user:"+YOUTUBE_USER+")-[comment:"+YOUTUBE_COMMENT+"]->(trailer:"+YOUTUBE_VIDEO+") \
#                 WHERE user.id = '"+user_id+"'\
#                 OPTIONAL MATCH (trailer)-[lv:"+LINKED_IN+"]->(post:"+FB_POST+")\
#                 Return trailer.id,post.fb_post_id"
#     else:
#         query = "MATCH (user:"+FB_USER+")-[comment:"+COMMENTED+"]->(post:"+FB_POST+") \
#                 WHERE user.id = '"+user_id+"'\
#                 OPTIONAL MATCH (post)-[lv:"+LINKED_VIDEO+"]->(trailer:"+YOUTUBE_VIDEO+")\
#                 Return trailer.id,post.fb_post_id"
#
#     videos = graph.run(query)
#
#     while videos.forward():
#         trailer = videos.current()
#         trailerIds.append(trailer['trailer.id'])
#         fb_posts_Ids.append(trailer['post.fb_post_id'])
#
#     similar_fbusers_and_comments = get_facebook_similar_viewing_users(graph,fb_posts_Ids)
#     similar_yusers_and_comments = get_youtube_similar_viewing_users(graph, trailerIds)
#
#     similar_users_and_comments = similar_fbusers_and_comments + similar_yusers_and_comments
#     return similar_users_and_comments
# #MATCH (user:FBUser)-[comment:COMMENTED]->(post:FBPost)
# #WHERE post.fb_post_id IN ['144540227138_10155317286922357', '144540227138_10155496525672139','144540227138_10155488383592139']
# #WITH user, collect(post) as posts
# #WHERE size(posts) = 1
# #RETURN user
#
# def get_facebook_similar_viewing_users(graph, postIds):
#     posts_string = '\',\''.join(str(e) for e in postIds)
#     query2 = "MATCH (user:"+FB_USER+")-[comment:"+COMMENTED+"]->(post:"+FB_POST+")\
#                 WHERE post.fb_post_id IN [\'"+posts_string+"\']\
#                 WITH user, collect(post) as posts\
#                 WHERE size(posts) = "+str(len(postIds))+"\
#                 RETURN user"
# #str(len(postIds))
#     userIds_list = []
#     users = graph.run(query2)
#
#     while users.forward():
#         try:
#             similar_user = users.current()
#             similar_user = similar_user[0]
#
#             userIds_list.append(similar_user['id'])
#         except Exception,e:
#             print "error, %s"% e
#             continue
#
#     similar_users_and_comments = get_fb_userlist_movies_from_db(graph,userIds_list,FB_USER)
#
#     return similar_users_and_comments
#
#
# def get_fb_userlist_movies_from_db(graph,user_list_ids, type):
#     userComments = []
#     userIds_string = '\',\''.join(str(e) for e in user_list_ids)
#     query = "MATCH (n:"+FB_USER+")-[r:"+COMMENTED+"]->(y:"+FB_POST+") WHERE n.id IN ['"+userIds_string+"'] \
#              OPTIONAL MATCH (y)<-[lv:"+LINKED_IN+"]-(trl)<-[ht:"+HAS_TRAILER+"*0..1]-(tr:"+MOVIE_DETAILS+")\
#              RETURN n,r,y,lv,trl,ht,tr"
#
#     videos = graph.run(query)
#
#     current_user = None
#     while videos.forward():
#         current_cursor =  videos.current()
#         user = current_cursor[0] #user node
#         if current_user is None:
#             current_user = UserComments(user['name'],user['id'],type)
#             userComments.append(current_user)
#         elif current_user.user_id != user['id']:
#             if any(x for x in userComments if x.user_id == user['id']):
#                 for userComment in userComments:
#                     if userComment.user_id == user['id']:
#                         current_user = userComment
#
#             else:
#                 current_user = UserComments(user['name'], user['id'], type)
#                 userComments.append(current_user)
#
#         relationship = current_cursor[1]  # youtube comment or like relationship
#         post = current_cursor[2]  # fb post node
#         current_comment = CommentFullInfo(post['name'], post['fb_post_id'], relationship['comment'],
#                                           relationship['polarity']
#                                           , relationship['sentiment_score'])
#
#         if current_cursor[3] is not None and current_cursor[5] is not None:
#             # if post has a video relation and video has details relation, get movie details
#             trailer_det = current_cursor[6]
#             current_comment.set_movie_details(trailer_det['title'], trailer_det['year'], trailer_det['genre'],
#                                               trailer_det['plot'], trailer_det['poster'])
#
#         current_user.addComment(current_comment)
#     return userComments
#
#
# def get_youtube_similar_viewing_users(graph, trailerIds):
#     trailers_string = '\',\''.join(str(e) for e in trailerIds)
#     query2 = "MATCH (user:YoutubeUser)-[comment:Youtube_Comment]->(trailer:YoutubeVideo)\
#                 WHERE trailer.id IN [\'"+trailers_string+"\']\
#                 WITH user, collect(trailer) as trailers\
#                 WHERE size(trailers) = "+str(len(trailerIds))+"\
#                 RETURN user"
# #str(len(trailerIds))
#     userIds_list = []
#     users = graph.run(query2)
#
#     while users.forward():
#         similar_user = users.current()
#         similar_user = similar_user[0]
#         userIds_list.append(similar_user['id'])
#
#     similar_users_and_comments = get_userlist_movies_from_db(graph,userIds_list,YOUTUBE_USER)
#
#     return similar_users_and_comments
#
# def get_userlist_movies_from_db(graph,user_list_ids, type):
#     userComments = []
#     userIds_string = '\',\''.join(str(e) for e in user_list_ids)
#     query = "MATCH (n:"+YOUTUBE_USER+")-[r:"+YOUTUBE_COMMENT+"]->(y:"+YOUTUBE_VIDEO+") \
#              WHERE n.id IN ['"+userIds_string+"'] OPTIONAL MATCH (y)<-[ht:"+HAS_TRAILER+"*0..1]-(tr:"+MOVIE_DETAILS+") \
#              RETURN n,r,y,ht,tr;"
#     videos = graph.run(query)
#
#     current_user = None
#     while videos.forward():
#         current_cursor =  videos.current()
#         user = current_cursor[0] #user node
#         if current_user is None:
#             current_user = UserComments(user['authorName'],user['id'],type)
#             userComments.append(current_user)
#         elif current_user.user_id != user['id']:
#             if any(x for x in userComments if x.user_id == user['id']):
#                 for userComment in userComments:
#                     if userComment.user_id == user['id']:
#                         current_user = userComment
#
#             else:
#                 current_user = UserComments(user['authorName'], user['id'], type)
#                 userComments.append(current_user)
#
#         relationship = current_cursor[1]#youtube comment relationship
#         trailer = current_cursor[2]#youtube trailer node
#         current_comment = CommentFullInfo(trailer['title'], trailer['id'], relationship['commentText'], relationship['polarity']
#                                           , relationship['sentiment_score'])
#         if current_cursor[3] is not None:#if has trailer relation exists get movie details
#             trailer_det = current_cursor[4]
#             current_comment.set_movie_details(trailer_det['title'],trailer_det['year'],trailer_det['genre'],trailer_det['plot'],trailer_det['poster'])
#
#
#         current_user.addComment(current_comment)
#         #videos.current()[0] returns user node
#         #videos.current()[1] returns relationship node
#         # videos.current()[2] returns video node
#         #print [act for act in accounts]
#     return userComments
#
# def provide_suggestions(user_id, type):
#     graph = startConnection()
#     user_movies_ids = []
#     user_movies = get_user_movie_ratings_from_db(user_id, type)
#     for movie in user_movies:
#         user_movies_ids.append(movie.movie_id)
#     suggestions=get_neighbour_movies(graph,user_id, user_movies_ids)
#     return suggestions
#
#
# #get movies that the neighbour users interacted with, do not get movies which this user already commented on
# def get_neighbour_movies(graph, user_id, user_movies_ids):
#     movie_ids_string = '\',\''.join(str(e) for e in user_movies_ids)
#     query = "MATCH p=(u)-[r:"+HAS_NEIGHBOUR+"]->(n)\
#             WHERE u.id = '"+user_id+"'\
#             OPTIONAL MATCH v =(n)-[youtubecmt:"+YOUTUBE_COMMENT+"]->(youtubetrl:"+YOUTUBE_VIDEO+")\
#             OPTIONAL MATCH fb =(n)-[fbcomment:"+COMMENTED+"]->(fbpost:"+FB_POST+")-[:"+LINKED_VIDEO+"]->(trailer)\
#             WHERE NOT youtubetrl IN ['"+movie_ids_string+"'] AND NOT trailer IN ['"+movie_ids_string+"']\
#             RETURN youtubetrl.id, youtubecmt.sentiment_score, r.similarity,fbcomment.sentiment_score,trailer.id"
#
#     recommended_movies = dict()
#
#     interacted_movies = graph.run(query)
#     while interacted_movies.forward():
#         current_interactions = interacted_movies.current()
#         trailer_id = current_interactions['youtubetrl.id']
#         if trailer_id is None:
#             trailer_id = current_interactions['trailer.id']
#
#         if not (trailer_id is None):
#             if not (trailer_id in recommended_movies):
#                 recommended_movies[trailer_id] = []
#
#             #get comment rating
#             rating = current_interactions['youtubecmt.sentiment_score']
#             if rating is None:
#                 rating = current_interactions['fbcomment.sentiment_score']
#
#             # get uer similarity
#             similarity = current_interactions['r.similarity']
#             if not (rating is None) and not (similarity is None):
#                 reccommendation = ReccommendObject(rating, similarity)
#                 recommended_movies[trailer_id].append(reccommendation)
#
#         #print current_interactions
#         #print "movie"
#
#     if len(recommended_movies) == 0:
#         print "User has no neighbours"
#
#
#     movies_to_suggest = dict()
#     for key in sorted(recommended_movies, key=lambda x: len(recommended_movies[x]), reverse=True):
#         #iterate on keys
#         rating = calculate_rating(recommended_movies[key])
#         if rating > 2:
#             movies_to_suggest[key] = min(5, rating)
#         #calculate rating
#
#     #if rating is greater than 2 add it to list
#     suggested_movies = get_movies(graph, movies_to_suggest)
#
#     #get list of movies
#     return suggested_movies
#
#
# #method which calculated rating by taking a weighted average
# #reccomendObj list of reccomendations
# def calculate_rating(reccomendObjs):
#     denominator = 0
#     numerator = 0
#     for obj in reccomendObjs:
#         if numpy.isnan(obj.similarity):
#             continue
#         numerator = numerator + (obj.rating * obj.similarity)
#         denominator = denominator + obj.similarity
#
#     if denominator == 0:
#         return 0
#
#     decimal_rating = numerator/denominator
#     return int(round(decimal_rating))
#
# #method which calculated rating by taking a weighted average
# #reccomendObj list of reccomendations
# def get_movies(graph, movies_to_suggest_ids):
#
#     movies_keys = list(movies_to_suggest_ids.keys())
#
#     movie_ids_string = '\',\''.join(str(e) for e in movies_keys)
#     query = "MATCH (yv:"+YOUTUBE_VIDEO+")\
#             WHERE yv.id IN ['" + movie_ids_string + "']\
#             OPTIONAL MATCH (yv)<-[has:"+HAS_TRAILER+"]-(md:"+MOVIE_DETAILS+")\
#             RETURN yv.id,yv.title,yv.description,has,md.title,md.plot,md.genre,md.year,md.poster"
#
#     movie_details = []
#     suggested_movies = graph.run(query)
#     while suggested_movies.forward():
#         movie_det = suggested_movies.current()
#
#         title = movie_det['yv.title']
#         if not (movie_det['md.title'] is None):
#             title = movie_det['md.title']
#
#         link = YOUTUBE_BASE + movie_det['yv.id']
#
#         movie_rating = movies_to_suggest_ids[movie_det['yv.id']]
#
#         movie = ReccomendedMovie(movie_det['yv.id'],title,movie_det['md.year'],movie_det['md.genre'],movie_det['md.plot'],
#                                  movie_det['md.poster'],link ,movie_det['yv.description'],movie_rating)
#         movies_to_suggest_ids[movie_det['yv.id']] = movie
#
#     movie_details = list(movies_to_suggest_ids.values())
#
#     return movie_details
#
#
# def add_test_user(movie, name):
#     graph = startConnection()
#     comment  = YoutubeComment("test_" + movie["ID"],
#                               movie["ID"],
#                               "test_"+name,
#                               name,
#                               movie["Comment"],
#                               "N/A")
#
#     return insert_user(graph, comment)
#
# def get_random_movies():
#     graph = startConnection()
#
#     moviesfound = []
#     movies = []
#     for i in range(10):
#         randNum = randint(1, 123)
#
#         while randNum in moviesfound:
#             randNum = randint(1, 123)
#
#         moviesfound.append(randNum)
#
#         query = "MATCH (a:YoutubeVideo)\
#                 RETURN a\
#                 SKIP %i LIMIT 1" % randNum
#
#         suggested_movies = graph.run(query)
#         while suggested_movies.forward():
#             movie_det = suggested_movies.current()[0]
#             title = movie_det['title']
#
#             link = YOUTUBE_BASE + movie_det['id']
#
#             movie = ReccomendedMovie(movie_det['id'], title, movie_det['year'], movie_det['genre'],
#                                      movie_det['plot'],
#                                      movie_det['poster'], link, movie_det['description'], 'N/A')
#             movies.append(movie)
#
#     return movies
#
