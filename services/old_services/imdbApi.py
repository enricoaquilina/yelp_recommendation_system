# #!/usr/bin/python
#
# import urllib2
# import json
# from models.old_models.movieObj import MovieObject
#
# #BASEAPI = "https://www.theimdbapi.org/api/find/movie?"
# BASEAPI = "http://www.omdbapi.com/?apikey=a9a63a89"
#
# def get_movie_details(movie_list):
#     movies = []
#
#     for mov in movie_list:
#         movie_title = mov.title.replace(" ", "+")
#         url = BASEAPI + "&t=" + movie_title + "&y=" + str(mov.year)
#         print url
#         try:
#             req = urllib2.Request(url)
#             req.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)")
#             response = urllib2.urlopen(req)
#             data = json.load(response)
#
#             if 'Error' not in data:
#                 movie = MovieObject(data["Title"],
#                                     data["Year"],
#                                     data["Genre"],
#                                     data["Plot"],
#                                     data["Poster"])
#                 movies.append(movie)
#             #time.sleep(2)#delay such as not to flood the server
#             #print data
#         except Exception, e:
#             print "Cannot find %s"%movie_title
#
#     try:
#         print [mov for mov in movies]
#     except Exception, e:
#         print "Cannot print {0}".format(movie_title)
#     print "total moviess = ", len(movies)
#     return movies
#
#
# # try:
# #     movie_list = []
# #     movie_list.append(MovieObject("Trolls",2016,"","",""))
# #     movie_list.append(MovieObject("Suicide Squad", 2016,"","",""))
# #     movie_list.append(MovieObject("Split", 2016,"","",""))
# #     movie_list.append(MovieObject("Sing", 2016,"","",""))
# #     movie_list.append(MovieObject("Doctor Strange", 2016,"","",""))
# #     #videoIds = ['pNpc4Eqqc-I']
# #     movies = get_movie_details(movie_list)
# #     insert_movie_details(movies)
# # except HTTPError, e:
# #     print "An HTTP error occurred:\n%s" % ( e)