#!/usr/bin/python

import urllib2
import urllib
import json
import gdata.youtube
import gdata.youtube.service

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser


#API_KEY=AIzaSyA7U8Vc10IqUoP0TSSm6qxhC-3G4mQobNQ

#https://www.googleapis.com/youtube/v3/search?key=AIzaSyA7U8Vc10IqUoP0TSSm6qxhC-3G4mQobNQ&channelId=UCi8e0iOVk1fEOogdfu4YgfA&part=snippet,id&order=date&maxResults=50&type=video&pageToken=CDIQAA

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyA7U8Vc10IqUoP0TSSm6qxhC-3G4mQobNQ"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#yt_service = gdata.youtube.service.YouTubeService()

# Turn on HTTPS/SSL access.
# Note: SSL is not available at this time for uploads.
#yt_service.ssl = True

def google_library_search_name(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                  developerKey=DEVELOPER_KEY)

  #print "Options:", options, "\n"
  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(

    part="id,snippet",
    maxResults=options.max_results,
    channelId=options.channel_id,
    type="video",
    q=options.q
  ).execute()
  return search_response

def google_library_search_vid(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                  developerKey=DEVELOPER_KEY)

  #print "Options:", options, "\n"
  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.commentThreads().list(

    part="id,snippet,replies",
    maxResults=options.max_results,
    videoId= options.video_id
  ).execute()
  return search_response

def url_api_search_name(options):
  url = "https://www.googleapis.com/" + YOUTUBE_API_SERVICE_NAME
  url = url + "/" + YOUTUBE_API_VERSION
  url = url + "/search?"

  data = {}
  data['key'] = DEVELOPER_KEY
  data['part'] = "id,snippet"
  data['maxResults'] = options.max_results
  data['channelId'] = options.channel_id
  data['type'] = "video"
  data['q'] = options.q
  url_values = urllib.urlencode(data)

  full_url = url + url_values
  print full_url
  search_response = urllib2.urlopen(full_url)
  dict = json.loads(search_response.read())
  return dict

def youtube_search(options):
  search_response = google_library_search_vid(options)
  print search_response
  videos = []
  channels = []
  playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s) | (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"], search_result["snippet"]["description"] ))
    elif search_result["id"]["kind"] == "youtube#channel":
      channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
      playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))

  print "Videos:\n", "\n".join(videos), "\n"
  #print "Channels:\n", "\n".join(channels), "\n"
  #print "Playlists:\n", "\n".join(playlists), "\n"


if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--max-results", help="Max results", default=25)
  argparser.add_argument("--channel-id", help="channelId", default="UCi8e0iOVk1fEOogdfu4YgfA")
  argparser.add_argument("--video-id", help="videoId", default="CgJudU_jlZ8")
  args = argparser.parse_args()

  try:
    youtube_search(args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)