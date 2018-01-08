from flask import Flask,jsonify,request
from services.webApiServices import get_all_users, get_user_movies_from_db2, get_similar_viewing_users,\
    provide_suggestions, get_video_node, add_test_user, get_random_movies
from mapReduce.mrRunner import get_neighbours_for_user
import json
import numpy

app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello_world():
    response = jsonify({'some': 'data'})
    after_request(response)
    return response


@app.route('/users')
def get_users():
    users = get_all_users()
    response = jsonify(users=[user.serialize() for user in users])
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/users/<username>', methods=['POST'])
def get_users_by_username(username):
    if username == "":
        response = {}
        after_request(response)
        return response

    users = get_all_users(username)
    response = jsonify(users=[user.serialize() for user in users])
    after_request(response)
    return response


@app.route('/user_movies/<id>', methods=['POST'])
def get_user_movies(id):
    user_type= json.loads(request.data)["type"]
    users =  get_user_movies_from_db2(id,user_type)
    response = jsonify(users=[user.serialize() for user in users])
    after_request(response)
    return response


@app.route('/similar_users/<id>')
def get_similar_users(id):
    user_type = request.args.get('type')
    users = get_similar_viewing_users(id,user_type)
    response = jsonify(users=[user.serialize() for user in users])
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/reccomend/<id>', methods=['POST'])
def get_suggestions(id):
    user_type = json.loads(request.data)["type"]
    movies = provide_suggestions(id, user_type)
    movies = sorted(movies, key=lambda x: x.predicted_rating, reverse=True)[:5]
    response = jsonify(movies=[movie.serialize() for movie in movies])
    after_request(response)
    return response

@app.route('/addtestuser/', methods=['POST'])
def add_new_user():
    newUser = json.loads(request.data)

    for movie in newUser["Movies"]:
        VidNode = get_video_node(movie["ID"])
        add_test_user(movie, newUser["Name"])

    get_neighbours_for_user("test_"+newUser["Name"], "YoutubeUser")
    movies = provide_suggestions("test_"+newUser["Name"], "YoutubeUser")
    movies = sorted(movies, key=lambda x: x.predicted_rating, reverse=True)[:15]
    response =  jsonify(movies=[movie.serialize() for movie in movies])
    after_request(response)
    return response


@app.route('/randommovies/', methods=['POST'])
def get_movies():
    movies = get_random_movies()
    response = jsonify(movies=[movie.serialize() for movie in movies])
    after_request(response)
    return response

@app.route('/getmae/', methods=['POST'])
def get_MAE():
    newUser = json.loads(request.data)

    count = 0;
    total5 = 0
    total10 = 0
    total15 = 0

    for movie in newUser["Movies"]:
        if count < 5:
            total5 = total5 + abs(int(movie["PredictedRating"]) - int(movie["Rating"]))

        if count < 10:
            total10 = total10 + abs(int(movie["PredictedRating"]) - int(movie["Rating"]))

        total15 = total15 + abs(int(movie["PredictedRating"]) - int(movie["Rating"]))
        count += 1

    total5 = total5/5.0
    total10 = total10 / 10.0
    total15 = total15 / 15.0

    response = jsonify(MAE_5=total5, MAE_10=total10, MAE_15=total15)
    after_request(response)
    return response


def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug=True)

