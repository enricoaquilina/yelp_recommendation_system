#!/usr/bin/python
from datetime import datetime
from models.old_models.movieObj import MovieObject

#get movie name from Movie Clip video names
def get_movie_info_from_videos(video_list):
    movies = []

    for vid in video_list:
        vid_title = vid["title"]
        vid_published = vid["publishedDate"]
        date = datetime.strptime(vid_published, '%Y-%m-%dT%H:%M:%S.000Z')
        movie_name = vid_title.split("#")

        if len(movie_name) > 0:
            movie_name = movie_name[0]
            movie_name = movie_name.split("/")

        if len(movie_name) > 0:
            movie_name = movie_name[0]
            movie_name = movie_name.split("(")

        if len(movie_name) > 0:
            movie_name = movie_name[0]
            movie_name = movie_name.split(" ")

            official_index = -1
            red_band_index = -1
            vol_index = -1

            try:
                official_index = movie_name.index("Official")
            except ValueError as e:
                print("not found")
            try:

                red_band_index = movie_name.index("Red")
            except ValueError as e:
                print("not found")
            try:

                vol_index = movie_name.index("Vol.")
            except ValueError as e:
                print("not found")


            index = -1
            if official_index > -1:
                index = official_index
            if red_band_index > -1 and red_band_index < index:
                index = red_band_index
            if vol_index > -1 and vol_index < index:
                index = vol_index

            if index > -1:
                movie_name = movie_name[0:index]

            movie_name = " ".join(movie_name)

        if len(movie_name) > 0:
            movie_name = movie_name.replace("Trailer", "")
            movie_name = movie_name.replace("Teaser", "")
            movie_name = movie_name.rstrip()
            movieObj = MovieObject(movie_name,
                                date.year,
                                "",
                                "",
                                "")
            movies.append(movieObj)

    return movies

def allow_comment(comment):
    not_accepted = ["1st", "2nd", "first", "second"]
    for word in not_accepted:
        if word.lower() in comment.commentText.lower():
            return False

    return isEnglish(comment)

def isEnglish(comment):
    try:
        comment.commentText.decode('ascii')
    except UnicodeDecodeError:
        return False
    except UnicodeEncodeError:
        return False
    else:
        return True