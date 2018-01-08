# #!/usr/bin/python
#
# from models.youtubeComment import YoutubeComment
# from models.old_models.videoObj import VideoObject
#
# from googleapiclient.discovery import build
#
# #API_KEY=AIzaSyA7U8Vc10IqUoP0TSSm6qxhC-3G4mQobNQ
#
# #https://www.googleapis.com/youtube/v3/search?key=AIzaSyA7U8Vc10IqUoP0TSSm6qxhC-3G4mQobNQ&channelId=UCi8e0iOVk1fEOogdfu4YgfA&part=snippet,id&order=date&maxResults=50&type=video&pageToken=CDIQAA
#
# # Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# # tab of
# #   https://cloud.google.com/console
# # Please ensure that you have enabled the YouTube Data API for your project.
# DEVELOPER_KEY = "AIzaSyA7U8Vc10IqUoP0TSSm6qxhC-3G4mQobNQ"
# YOUTUBE_API_SERVICE_NAME = "youtube"
# YOUTUBE_API_VERSION = "v3"
# MAX_RESULTS = 50
#
# ID = "id"
# VIDEO_ID = "videoId"
# TOP_LEVEL_COMMENT = "topLevelComment"
# SNIPPET = "snippet"
# AUTHOR_CHANNEL_ID = "authorChannelId"
# VALUE = "value"
# AUTHOR_DISPLAY_NAME = "authorDisplayName"
# TEXT_ORIGINAL = "textOriginal"
# PUBLISHED_AT = "publishedAt"
# ITEMS = "items"
# PAGE_INFO = "pageInfo"
# TOTAL_RESULTS = "totalResults"
# NEXT_PAGE_TOKEN = "nextPageToken"
#
# TITLE = "title"
# DESCRIPTION = "description"
#
# CHANNEL_ID = "UCi8e0iOVk1fEOogdfu4YgfA"
#
# #get video comments
# def video_comments_request(options):
#   youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
#                   developerKey=DEVELOPER_KEY)
#
#   # Call the search.list method to retrieve results matching the specified
#   # query term.
#   if( not options.has_key('next_page')):
#       search_response = youtube.commentThreads().list(
#         part="id,snippet,replies",
#         maxResults = MAX_RESULTS,
#         videoId= options['video_Id']
#       ).execute()
#   else :
#       search_response = youtube.commentThreads().list(
#           part="id,snippet,replies",
#           maxResults=MAX_RESULTS,
#           videoId=options['video_Id'],
#           pageToken = options['next_page']
#       ).execute()
#
#   #print search_response
#   return search_response
#
# #get video comments
# def video_details_request(options):
#   youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
#                   developerKey=DEVELOPER_KEY)
#
#   #print "Options:", options, "\n"
#   # Call the search.list method to retrieve results matching the specified
#   # query term.
#   search_response = youtube.videos().list(
#     part="snippet,contentDetails,statistics",
#     id= options['video_Id']
#   ).execute()
#
#   #print search_response
#   return search_response
#
# #make page requests for video comments and create list of comments
# def get_video_comments(options):
#     try:
#         comments = []
#         search_response = video_comments_request(options)
#
#         totalPages = search_response[PAGE_INFO][TOTAL_RESULTS]
#         num = 0
#         while(search_response.has_key(NEXT_PAGE_TOKEN)):
#             num = num + 1
#             print "Getting Comments From Page ", num
#             if(num != 1):
#                 print "obatining ", num
#                 pageToken = search_response[NEXT_PAGE_TOKEN]
#                 options["next_page"] = pageToken
#                 search_response = video_comments_request(options)
#
#             for search_result in search_response.get(ITEMS, []):
#                 snippet = search_result[SNIPPET]
#                 comment = YoutubeComment(search_result[ID],
#                                          snippet[VIDEO_ID],
#                                          snippet[TOP_LEVEL_COMMENT][SNIPPET][AUTHOR_CHANNEL_ID][VALUE],
#                                          snippet[TOP_LEVEL_COMMENT][SNIPPET][AUTHOR_DISPLAY_NAME],
#                                          snippet[TOP_LEVEL_COMMENT][SNIPPET][TEXT_ORIGINAL],
#                                          snippet[TOP_LEVEL_COMMENT][SNIPPET][PUBLISHED_AT])
#                 comments.append(comment)
#                 # comments.append("%s | (%s) | %s | %s" % (snippet[TOP_LEVEL_COMMENT][SNIPPET][AUTHOR_CHANNEL_ID][VALUE],
#                 #                                         snippet[TOP_LEVEL_COMMENT][SNIPPET][AUTHOR_DISPLAY_NAME],
#                 #                                         snippet[TOP_LEVEL_COMMENT][SNIPPET][TEXT_ORIGINAL],
#                 #                                         snippet[TOP_LEVEL_COMMENT][SNIPPET][PUBLISHED_AT]))
#                 # print datetime.strptime(snippet[TOP_LEVEL_COMMENT][SNIPPET][PUBLISHED_AT], "%Y-%m-%dT%H:%M:%S.000Z")
#
#         #print [comment for comment in comments]
#         print "total comments = ", len(comments)
#         return comments
#     except Exception, e:
#         print "An error occurred:\n"
#         return None
#
# def get_videos_details(video_list):
#     dict = {"video_Id": "def"}
#     videos = []
#     for vid in video_list:
#         dict["video_Id"] = vid
#         search_response = video_details_request(dict)
#
#         for search_result in search_response.get(ITEMS, []):
#             snippet = search_result[SNIPPET]
#             comment = VideoObject(vid,
#                                      snippet[TITLE],
#                                      snippet[DESCRIPTION],
#                                      snippet[PUBLISHED_AT])
#             videos.append(comment)
#
#     #print [vid for vid in videos]
#     print "total videos = ", len(videos)
#     return videos
#
# def get_video_details(vid):
#     dict = {"video_Id": "def"}
#     videos = []
#     dict["video_Id"] = vid
#
#     search_response = video_details_request(dict)
#
#     for search_result in search_response.get(ITEMS, []):
#         snippet = search_result[SNIPPET]
#         comment = VideoObject(vid,
#                               snippet[TITLE],
#                               snippet[DESCRIPTION],
#                               snippet[PUBLISHED_AT])
#         videos.append(comment)
#
#     #print [vid for vid in videos]
#     print "total videos = ", len(videos)
#     return videos[0]
#
#
# def search_for_video(title):
#     youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
#                     developerKey=DEVELOPER_KEY)
#
#     search = youtube.search().list(
#         q=title,
#         part="id,snippet",
#         channelId=CHANNEL_ID,
#         maxResults=MAX_RESULTS
#       ).execute()
#
#     vid_id = "0"
#     for search_result in search.get("items", []):
#         vid_id = search_result["id"]["videoId"]
#         break
#
#     return vid_id
#
