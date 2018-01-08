# import urllib2
# import urllib
# import json
# #from objdict import ObjDict
# from models.old_models.fbPostObj import FBPostObject
# from models.fbCommentsObj import FBCommentsObject
# from models.review import FBLikesObject
# from models.user import UserObject
# from neoServices import get_fb_user_node, insert_fb_user_comments_post_relationship, \
#     insert_fb_user_likes_post_relationship, insert_fb_user
#
# LIMIT = 1000
# LIMIT_POSTS = 100
# ALL_PAGES = False
#
# # Get Acess Token
# def get_app_access_token(app_id, app_secret):
#     """Get the access_token for the app.
#
#     This token can be used for insights and creating test users.
#
#     @arg app_id :type string :desc retrieved from the developer page
#     @arg app_secret :type string :desc retrieved from the developer page
#
#     Returns the application access_token.
#
#     """
#     # Get an app access token
#     args = {'grant_type': 'client_credentials',
#             'client_id': app_id,
#             'client_secret': app_secret}
#
#     f = urllib2.urlopen("https://graph.facebook.com/oauth/access_token?" +
#                               urllib.urlencode(args))
#
#     try:
#         result = f.read()
#         Accesstoken = json.loads(result)
#     finally:
#         f.close()
#
#     return Accesstoken['access_token']
#
#
# def get_feed(access_token, page_id, link):
#     """Get the feed for the page.
#
#         The json of the feed.
#
#         @arg page_id :type int :desc the page ID
#         @arg limit :type int :desc the page limit by default it is set to 10
#
#         Returns The json for the page feed.
#
#         """
#     if link is None:
#         link = "https://graph.facebook.com/v2.9/" + str(page_id) +\
#                               "/posts?fields=message,properties,caption,link,message_tags,source,type,attachments&limit=" + str(LIMIT_POSTS)
#
#     request = urllib2.Request(link)
#     request.add_header("Authorization", "OAuth %s" % access_token)
#     f = urllib2.urlopen(request)
#
#     try:
#         result = f.read()
#         feed = json.loads(result)
#         if "paging" in feed and "next" in feed["paging"]:
#             NextPage = feed["paging"]["next"]
#         else:
#             NextPage = None
#     finally:
#         f.close()
#
#     return (feed, NextPage)
#
# def get_video(data_list):
#     """Get the videos for the list.
#
#             The list with only videos of the feed.
#
#             @arg data_list :type list :list of posts
#
#             Returns list with only videos.
#
#             """
#     ret_list = []
#
#     for dataItem in data_list["data"]:
#         try:
#             if dataItem["type"] == "video":
#
#                 if "message" not in dataItem:
#                     message = "N/A"
#                 else:
#                     message = dataItem["message"]
#
#                 current_data = FBPostObject("video",
#                                             dataItem["attachments"]["data"][0]["title"],
#                                             message,
#                                             dataItem["id"],
#                                             dataItem["link"])
#
#                 ret_list.append(current_data)
#         except Exception, e:
#             print "An error occurred:\n%s" % (e)
#             continue
#     return ret_list
#
#
# def get_response_info(request, access_token):
#     request = urllib2.Request(request)
#     request.add_header("Authorization", "OAuth %s" % access_token)
#     f = urllib2.urlopen(request)
#
#     try:
#         result = f.read()
#         commentsResponse = json.loads(result)
#     finally:
#         f.close()
#     return commentsResponse
#
# def insert_comment(graph, comment, post_node):
#     curComment = FBCommentsObject(comment["created_time"],
#                                   comment["message"],
#                                   comment["id"],
#                                   comment["from"]["id"],
#                                   comment["from"]["name"])
#
#     user_node = get_fb_user_node(graph, curComment.user_id)
#
#     if user_node is None:
#         user = UserObject(curComment.user_id, curComment.user_name, "")
#         user_node = insert_fb_user(graph, user)
#
#     # Create RelationShip from post to comment
#     insert_fb_user_comments_post_relationship(graph, post_node, user_node, curComment)
#
#
# def get_comments_and_add_to_post(graph, access_token, post, post_node):
#     # Get Comments
#     try:
#         response = get_response_info(
#             "https://graph.facebook.com/v2.9/" + str(post.fb_post_id) + "/comments?limit=" + str(LIMIT), access_token)
#     except Exception, e:
#         print "FB Comments size exceeded:\n%s" % (e)
#         response = get_response_info(
#             "https://graph.facebook.com/v2.9/" + str(post.fb_post_id) + "/comments?limit=" + str(LIMIT), access_token)
#
#
#     if ALL_PAGES :
#         while "next" in response["paging"]:
#             for comment in response["data"]:
#                 insert_comment(graph, comment, post_node)
#                 print("Added Comment")
#
#             print("Adding page of comments")
#             response = get_response_info(response["paging"]["next"], access_token)
#
#     for comment in response["data"]:
#         insert_comment(graph, comment, post_node)
#
#
# def insert_likes(graph, like, post_node):
#     cur_like = FBLikesObject(like["id"],
#                              like["name"])
#
#     user_node = get_fb_user_node(graph, cur_like.user_id)
#
#     if user_node is None:
#         user = UserObject(cur_like.user_id, cur_like.name, "")
#         user_node = insert_fb_user(graph, user)
#
#     # Create RelationShip from post to comment
#     insert_fb_user_likes_post_relationship(graph, post_node, user_node, cur_like)
#
#
# def get_likes_and_add_to_post(graph, access_token, post, post_node):
#     # Get Comments
#     response = get_response_info(
#         "https://graph.facebook.com/v2.9/" + str(post.fb_post_id) + "/likes?limit=" + str(LIMIT), access_token)
#
#     if ALL_PAGES :
#         while "next" in response["paging"]:
#             for comment in response["data"]:
#                 insert_likes(graph, comment, post_node)
#                 print("Added like")
#
#             print("Adding page of like")
#             response = get_response_info(response["paging"]["next"], access_token)
#
#     for comment in response["data"]:
#         insert_likes(graph, comment, post_node)
#
#
#
#
#
