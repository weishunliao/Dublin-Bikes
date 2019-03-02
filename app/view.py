from app import app, db
from app.models import Stations, Bikes
from flask import render_template, request, jsonify
from sqlalchemy import func
import requests
import json
import time


@app.route('/')
def index():
    respose = requests.get(app.config["SECRET_WEATHER_KEY"])
    weather_json = respose.json()
    respose.close()

    stations_list = Stations.query.all()
    stations_list_arr = []
    for i in stations_list:
        stations_list_arr.append(i.name)

    # current = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    current2 = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    # past = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - 604800))
    week = time.localtime(time.time())[6] + 1
    week_data = db.session.query(func.count(Bikes.ID)). \
        filter(Bikes.ID == 2, Bikes.day < current2, Bikes.week == 1, func.date_format(Bikes.day, '%H') == 23). \
        all()
    num_week = week_data[0][0] / 6
    dynamic_data = db.session.query(func.date_format(Bikes.day, '%H'), func.sum(Bikes.available_bike_stands)). \
        filter(Bikes.week == 1). \
        group_by(func.date_format(Bikes.day, '%H')).all()

    last_7_data = {'cols': [{'id': 'Time of day', 'label': 'Time of day', 'type': 'timeofday'},
                            {'id': 'Usage', 'label': 'Usage', 'type': 'number'}], 'rows': []}

    for i in dynamic_data:
        c1 = {'v': [int(i[0]), 0, 0]}
        c2 = {'v': int(i[1]) / num_week}
        last_7_data['rows'].append({'c': [c1, c2]})
    return render_template('index.html', map_key=app.config["SECRET_MAP_KEY"],
                           bike_api_key=app.config['SECRET_JCD_KEY'], weather_json=weather_json,
                           station_list=json.dumps(stations_list_arr), last_7_data=json.dumps(last_7_data))


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
