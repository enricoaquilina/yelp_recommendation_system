#!/usr/bin/python

# from services.old_services.imdbApi import get_movie_details, insert_movie_details
# from services.old_services.FaceBookApi import get_app_access_token
# from services.helpers import get_movie_info_from_videos
# from urllib.request import HTTPError
# import facebook

from services.neoServices import startConnection, graphConstraints, insert_businesses, insert_reviews, insert_users, add_sentiment_to_comments
import json

PAGES_COUNT = 50
START_PAGE = 13
if __name__ == "__main__":
    # everything is called from here
    # once posts are obtained from fb, the video ids are extracted into a
    # list and fed to method get_video_details instead of the hardcoded list
    # this method retreives video data from youtube


    graph = startConnection()
    # graph.delete_all()
    # graphConstraints()
    nextPage = None
    iterateNextPage = True
    current_posts_page = 0

    # businesses = []
    # for idx, line in enumerate(open('./dataset/business.json', 'r', encoding="utf8")):
    #     # if idx < 20:
    #         businesses.append(json.loads(line))
    #     # else:
    #     #     break
    #
    # insert_businesses(businesses)

    # users = []
    # for idx, line in enumerate(open('./dataset/user.json', 'r', encoding="utf8")):
    #     # if idx < 20:
    #         users.append(json.loads(line))
    #     # else:
    #     #     break
    #
    # insert_users(users)

    reviews = []
    for idx, line in enumerate(open('./dataset/review.json', 'r', encoding="utf8")):
        # if idx < 20:
            reviews.append(json.loads(line))
        # else:
        #     break

    insert_reviews(reviews)

    print('Done')

    # while iterateNextPage :
    #     current_posts_page = current_posts_page+1
    #     feed, nextPage = get_feed(access_token, 144540227138,nextPage)
    #     print "Current Page: " + str(current_posts_page)
    #
    #     if current_posts_page < START_PAGE:
    #         print "skipping page {0}".format(current_posts_page)
    #         continue
    #     if nextPage is None or current_posts_page == PAGES_COUNT:
    #         iterateNextPage = False
    #
    #     try:
    #
    #         video_posts = get_video(feed)
    #
    #         for video_post in video_posts:
    #
    #             #feed, nextPage = get_feed(access_token, 144540227138,nextPage)
    #
    #             if "trailer" not in video_post.name.lower():
    #                 continue
    #
    #             if fb_post_exist(graph,video_post):
    #                 continue
    #
    #             # insert Video
    #             post_node = insert_fb_post(graph, video_post)
    #
    #             # get Comments and add them
    #             get_comments_and_add_to_post(graph, access_token, video_post, post_node)
    #
    #             # get likes and add them
    #             #get_likes_and_add_to_post(graph, access_token, video_post, post_node)
    #
    #             # search for youtube movie
    #             vidID = search_for_video(video_post.name)
    #             if vidID != "0":
    #                 # Get the video details
    #                 video_list = get_video_details(vidID)
    #
    #                 # then it is inserted into insert videos, which inserts video data to neo4j
    #                 vid_node = insert_video(video_list)
    #
    #                 insert_fb_post_to_video_relationship(graph, post_node, vid_node)
    #
    #                 # this list is just to initialize the dict
    #                 dict = {"video_Id": "CgJudU_jlZ8"}
    #                 # for each video insert user data and comments relationships into neo4j
    #
    #                 dict["video_Id"] = vidID
    #                 comment_list = get_video_comments(dict)
    #                 if comment_list is not None:
    #                     insert_comments(comment_list)
    #             else:
    #                 print "Cannot find video for " + video_post.name
    #
    #     except HTTPError as e:
    #         print("An HTTP error %d occurred: %s" % (e.resp.status, e.content))
    #
    #
    # try:
    #     # get all videos from neo4j which do not have a movie linked with them
    #     trailer_videos = get_videos_with_missing_details()
    #     # extract movie name and year from title
    #     # this does not work for all movie titles as text does not have a structure,
    #     # it will be updated later to cater for more cases later when more data is available in the database
    #     business_list = get_movie_info_from_videos(trailer_videos)
    #     for business in business_list:
    #         print("Business name: %s" % str(business.name))
    #         print("\n"
    #     # get movie details from api
    #     movies = get_movie_details(movie_list)
    #     insert_movie_details(movies)
    # except HTTPError as e:
    #     print("An HTTP error occurred: %s" % e)
    #
    # try:
    #     add_sentiment_to_comments()
    # except HTTPError as e:
    #     print("An HTTP error occurred: %s" % e)

