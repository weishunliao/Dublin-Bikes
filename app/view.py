from app import app
from app.models import Stations
from flask import render_template, request, jsonify
import requests


@app.route('/')
def index():
    respose = requests.get(app.config["SECRET_WEATHER_KEY"])
    weather_json = respose.json()
    respose.close()
    return render_template('index.html', map_key=app.config["SECRET_MAP_KEY"],
                           bike_api_key=app.config['SECRET_JCD_KEY'], weather_json=weather_json)


@app.route('/search')
def search():
    like_search_keyword = request.args.get('input')
    result = {}
    if like_search_keyword != "":
        statioin_obj_arr = Stations.query.filter(Stations.name.like(like_search_keyword + '%')).all()
        for i in statioin_obj_arr:
            result[i.ID] = i.name
    return jsonify(result)


# @app.route('/')
def new():
    respose = requests.get(app.config["SECRET_WEATHER_KEY"])
    weather_json = respose.json()
    respose.close()
    return render_template('new_index.html', weather_json=weather_json)