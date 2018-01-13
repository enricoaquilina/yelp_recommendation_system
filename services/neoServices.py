#!/usr/bin/python
# import relationships as relationships
from py2neo import Graph, Node, Relationship
from services.sentimentService import get_sentiment_polarity, get_sentiment_score

# YOUTUBE_USER = "YoutubeUser"
# FB_USER = "FBUser"
# TEST_USER = "TestUser"
# YOUTUBE_VIDEO = "YoutubeVideo"
# YOUTUBE_COMMENT = "Youtube_Comment"
# MOVIE_DETAILS = "MovieDetails"
# FB_POST = "FBPost"
# HAS_TRAILER = "Has_Trailer"
# COMMENTED = "COMMENTED"
# LIKES = "LIKES"
# LINKED_VIDEO = business_"LINKED_VIDEO"
# LINKED_IN = "LINKED_IN"

YELP_USER = "YelpUser"
YELP_BUSINESS = "YelpBusiness"
REVIEW_COMMENT = "ReviewComment"
REVIEW_AUTHOR = "ReviewAuthor"
BUSINESS_REVIEW = "BusinessReview"
BUSINESS_DETAILS = "BusinessDetails"

REVIEWED = "REVIEWED"
HAS_REVIEW = "HasReview"


def startConnection():
    # graph = Graph("http://localhost:7474/db/data", password="123456")  # Graph("bigData")
    graph = Graph()
    return graph


def graphConstraints():
    graph = startConnection()
    # graph.schema.create_uniqueness_constraint(YOUTUBE_USER,"id")
    # graph.schema.create_uniqueness_constraint(YOUTUBE_VIDEO, "id")
    # graph.schema.create_uniqueness_constraint(MOVIE_DETAILS, "title")
    # graph.schema.create_uniqueness_constraint(COMMENTED, "fb_comment_id")
    # graph.schema.create_uniqueness_constraint(FB_USER, "id")

    graph.schema.create_uniqueness_constraint(YELP_BUSINESS, "business_id")
    graph.schema.create_uniqueness_constraint(BUSINESS_DETAILS, "name")
    # graph.schema.create_uniqueness_constraint(REVIEW_COMMENT, "id")
    # graph.schema.create_uniqueness_constraint(REVIEW_AUTHOR, "id")


def graphIndexes():
    graph = startConnection()
    # graph.schema.create_index(FB_USER,"id")
    # graph.schema.create_index(YOUTUBE_USER, "id")
    # graph.schema.create_index(YOUTUBE_VIDEO, "id")

    graph.schema.create_index(YELP_USER, "id")
    graph.schema.create_index(YELP_BUSINESS, "id")
    # graph.schema.create_index(REVIEW_AUTHOR, "id")


# given a list of businesses, iterates, checks if business exists and if not, insert it
def insert_businesses(businesses):
    graph = startConnection()
    for idx, business in enumerate(businesses):
        y_business = list(graph.find(YELP_BUSINESS,
                                     property_key="business_id",
                                     property_value=business["business_id"]))
        if len(y_business) == 0:
            y_business = Node(YELP_BUSINESS,
                              business_id=business["business_id"],
                              name=business["name"],
                              star_rating=business["stars"],
                              city=business["city"],
                              state=business["state"],
                              review_count=business["review_count"],
                              latitude=business["latitude"],
                              longitude=business["longitude"])
            graph.create(y_business)
            print("%s/%s | business %s!" % (str(idx),  str(len(businesses)), business["name"]))
        else:
            print("Business %s already exists!" % business["business_id"])


# given a list of businesses, iterates, checks if business exists and if not, insert it
def insert_users(users):
    graph = startConnection()
    for idx, user in enumerate(users):
        y_user = list(graph.find(YELP_USER,
                                 property_key="user_id",
                                 property_value=user["user_id"]))
        if len(y_user) == 0:
            y_user = Node(YELP_USER,
                          user_id=user["user_id"],
                          name=user["name"],
                          review_count=user["review_count"],
                          average_stars=user["average_stars"])
            graph.create(y_user)
            print("%s/%s | user %s!" % (str(idx),  str(len(users)), user["name"]))
        else:
            print("user %s already exists!" % user["user_id"])


# insert a single business
def insert_business(business):
    graph = startConnection()
    y_business = list(graph.find(YELP_BUSINESS,
                                 property_key="id",
                                 property_value=business.id))
    if len(y_business) == 0:
        y_business = Node(YELP_BUSINESS,
                          id=business.id,
                          name=business.name,
                          star_rating=business.star_rating,
                          city=business.city,
                          state=business.state,
                          review_count=business.review_count,
                          latitude=business.latitude,
                          longitude=business.longitude)
        graph.create(y_business)
    else:
        print("Business %s already exists!" % business.id)

    return y_business


# find a business
def get_business_node(bid):
    graph = startConnection()
    y_business = list(graph.find(YELP_BUSINESS,
                                 property_key="id",
                                 property_value=bid))
    if len(y_business) != 0:
        return y_business
    else:
        return None


def business_exists(graph, business_node):
    fb_post = list(graph.find(YELP_BUSINESS, property_key="id", property_value=business_node.id))
    if len(fb_post) > 0:
        return True

    return False


# given a list of reviews, it iterates them and inserts the user who wrote that review
def insert_reviews(review_list):
    graph = startConnection()

    review_count = 0
    user_count = 0
    # graph.schema.create_uniqueness_constraint(YELP_USER, "id")

    # for each review in the list
    for idx, review in enumerate(review_list):
        # reviewed_business = list(graph.find(YELP_BUSINESS,
        #                                     property_key="business_id",
        #                                     property_value=review["business_id"]))

        reviewed_business = graph.find_one(YELP_BUSINESS, "business_id", review["business_id"])

        print("Review: %s/%s" % (str(idx), str(len(review_list))))

        if idx % 10 == 0:
            print("Current review count: %s" % str(review_count))
            print("Current user count: %s" % str(user_count))

        if reviewed_business["state"] == "QC" or reviewed_business["state"] == "OH":

            # y_user = list(graph.find(YELP_USER,
            #                          property_key="user_id",
            #                          property_value=review["user_id"]))

            y_user = graph.find_one(YELP_USER, "id", review["user_id"])

            # if user doesn't exist
            if y_user is None:
                # create user
                y_user = Node(YELP_USER,
                              id=review["user_id"])
                user_count += 1
                graph.create(y_user)

            # create relationship between user and business AND remove review
            user_reviews_business = Relationship(y_user, REVIEWED, reviewed_business)
            user_reviews_business["review_id"] = review["review_id"]
            user_reviews_business["text"] = review["text"]
            user_reviews_business["published_date"] = review["date"]
            user_reviews_business["author_id"] = review["user_id"]
            user_reviews_business["business_id"] = review["business_id"]
            user_reviews_business["id"] = 0
            # user_reviews_business["polarity"] = get_sentiment_polarity(review["polarity"])
            # user_reviews_business["sentiment_score"] = \
            #     get_sentiment_score(review["polarity"], user_reviews_business["polarity"])

            graph.create(user_reviews_business)
            review_count += 1
            del review_list[idx]

            # find other user reviews and repeat
            # remaining_user_reviews = [x for x in review_list if x["user_id"] == y_user["id"]]
            # for remaining_review in remaining_user_reviews:
            #     # create relationship between user and business AND remove review
            #     user_reviews_remaining_business = Relationship(y_user, REVIEWED, reviewed_business)
            #     user_reviews_remaining_business["review_id"] = remaining_review["review_id"]
            #     user_reviews_remaining_business["text"] = remaining_review["text"]
            #     user_reviews_remaining_business["published_date"] = remaining_review["published_date"]
        else:
            del review_list[idx]




# given a business node, user node and review, check whether the relationship already exists, if no create it
# if yes, check whether the review is the same as this one (multiple reviews can exist on same video)
def insert_review(graph, business_node, user_node, review):
    relationships = list(graph.match(start_node=user_node, rel_type=REVIEWED, end_node=business_node))
    if len(relationships) == 0:
        user_reviews_business = Relationship(user_node, REVIEWED, business_node)
        user_reviews_business["review_id"] = review["review_id"]
        user_reviews_business["text"] = review["text"]
        user_reviews_business["published_date"] = review["published_date"]
        user_reviews_business["polarity"] = review["polarity"]
        user_reviews_business["sentiment_score"] = review["sentiment_score"]
        graph.create(user_reviews_business)
    elif len(relationships) > 0:
        if (not any(rvw["id"] == review.id for rvw in relationships)):
            user_reviews_business = Relationship(user_node, BUSINESS_REVIEW, business_node)
            user_reviews_business["review_id"] = review["review_id"]
            user_reviews_business["text"] = review["text"]
            user_reviews_business["published_date"] = review["published_date"]
            user_reviews_business["polarity"] = review["polarity"]
            user_reviews_business["sentiment_score"] = review["sentiment_score"]
            graph.create(user_reviews_business)


# method to get youtube videos which do not have an incoming HAS_TRAILER Relationship
# MATCH (vid:YoutubeVideo) WHERE NOT ()-[:Has_Trailer]->(vid) RETURN vid
# def get_videos_with_missing_details():
#     trailers = []
#     graph = startConnection()
#     cypher_query = "MATCH(vid:" + YOUTUBE_VIDEO + ") WHERE NOT ()-[:"+HAS_TRAILER+"]->(vid) RETURN vid"
#     videos = graph.run(cypher_query)
#
#     while videos.forward():
#         trailers.append(videos.current()[0])
#
#     return trailers


# given a list of businesses, iterate, check if business exists by name. If no, create business, if yes check
# if the returned movie is of the same year (movies with same name may be created at different years)
# get youtube video trailer which has the movie title in its name, and create relationship between movie and trailer
def insert_business_details(business_list):
    try:
        graph = startConnection()

        for business in business_list:
            business_det = list(graph.find(BUSINESS_DETAILS, property_key="name", property_value=business.name))
            if len(business_det) == 0:
                business_det = Node(BUSINESS_DETAILS,
                                    name=business.name,
                                    star_rating=business.year,
                                    city=business.genre,
                                    state=business.plot,
                                    review_count=business.poster,
                                    latitude=business.latitude,
                                    longitude=business.longitude)
                graph.create(business_det)
    except Exception as e:
        print("Error Encountered(%s)" % e)


# given a youtube video and movie details, create a HAS_TRAILER Relationship if it does not exist
# def insert_movie_video_relationship(graph, video_node, movie_node):
#     relationships = list(graph.match(start_node=movie_node, rel_type=HAS_TRAILER, end_node=video_node))
#     if len(relationships) == 0:
#         has_trailer = Relationship(movie_node, HAS_TRAILER, video_node)
#         graph.create(has_trailer)

# def insert_fb_post(graph, fb_post_node):
#     node = Node(FB_POST,
#         type=fb_post_node.type,
#         message=fb_post_node.message,
#         fb_post_id=fb_post_node.fb_post_id,
#         link=fb_post_node.link,
#         name=fb_post_node.name)
#     graph.create(node)
#     return node

# def insert_user_review_post_relationship(graph, post_node, user_node, review):
#     rel = Relationship(user_node,
#                        REVIEWED,
#                        post_node,
#                        comment=commentobj.comment,
#                        comment_id=commentobj.fb_comment_id,
#                        date=commentobj.date,
#                        polarity=commentobj.polarity,
#                        sentiment_score=commentobj.sentiment_score)
#     graph.create(rel)
#     return rel


# def insert_fb_user_likes_post_relationship(graph, post_node, user_node, likeobj):
#     rel = Relationship(user_node,
#                        LIKES,
#                        post_node)
#     graph.create(rel)
#     return rel
#
#     return

#
# def get_fb_user_node(graph, user_id):
#     cypher_query = "MATCH(user:" + FB_USER + ") WHERE  user.id = '" + user_id + "' RETURN user"
#     user = graph.run(cypher_query)
#
#     ret_user = None
#
#     while user.forward():
#         ret_user = user.current()[0]
#
#     return ret_user

#
# def insert_fb_user(graph, user):
#     node = Node(FB_USER,
#                 id=user.id,
#                 name=user.name)
#     graph.create(node)
#     return node

#
# def insert_test_user(graph, username):
#     node = Node(TEST_USER,
#                 id=username,
#                 name=username)
#     graph.create(node)
#     return node
#
#
# def insert_fb_post_to_video_relationship(graph, post_node, video_node):
#     rel = Relationship(post_node,
#                        LINKED_VIDEO,
#                        video_node)
#     graph.create(rel)
#
#     rel = Relationship(video_node,
#                        LINKED_IN,
#                        post_node)
#     graph.create(rel)


# add sentiment score to yelp reviews
def add_sentiment_to_comments():
    graph = startConnection()

    for rel in graph.match(rel_type=REVIEWED):
        review_text = rel['review_text']
        polarity = get_sentiment_polarity(review_text)
        sentiment_score = get_sentiment_score(review_text, polarity)
        rel["polarity"] = polarity
        rel["sentiment_score"] = sentiment_score
        rel.push()
        print(rel)
