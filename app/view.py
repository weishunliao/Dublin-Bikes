from app import app, db
from app.models import Stations, Bikes
from flask import render_template, request, jsonify
from sqlalchemy import func
import requests
import json
import time


# @app.route('/')
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
    current3 = time.strftime("%H", time.localtime(time.time()))
    # past = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - 604800))
    week = time.localtime(time.time())[6] + 1
    week_data = db.session.query(func.count(Bikes.ID)). \
        filter(Bikes.ID == 2, Bikes.day < current2, Bikes.week == 2, func.date_format(Bikes.day, '%H') == 23). \
        all()
    num_week = week_data[0][0] / 6
    dynamic_data = db.session.query(func.date_format(Bikes.day, '%H'), func.sum(Bikes.available_bike_stands)). \
        filter(Bikes.week == 1). \
        group_by(func.date_format(Bikes.day, '%H')).all()

    last_7_data = {'cols': [{'id': 'Time of day', 'label': 'Time of day', 'type': 'timeofday'},
                            {'id': 'Usage', 'label': 'Usage', 'type': 'number'}], 'rows': []}

    for i in dynamic_data:
        c1 = {'v': [int(i[0]), 0, 0]}
        # c2 = {'v': int(i[1]) / num_week}
        c2 = {'v': int(i[1])}
        last_7_data['rows'].append({'c': [c1, c2]})
    return render_template('index.html', map_key=app.config["SECRET_MAP_KEY"], weather_json=weather_json,
                           station_list=json.dumps(stations_list_arr), last_7_data=json.dumps(last_7_data),
                           current3=current3)


@app.route('/update_map')
def search():
    t = request.args.get('t')
    if t == "current":
        respose = requests.get(
            'https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=31523d933c2ed2b25fd82ba42e3f0277eadf6184')
        bike_current_json = respose.json()
        respose.close()
    else:
        bike_current_json=[]
        for h in range(24):
            bike_data = []
            query_data = db.session.query(Stations.name, Stations.p_latitude, Stations.p_longitude, Bikes.available_bikes,
                                          Bikes.available_bike_stands, Bikes.status). \
                filter(func.date_format(Bikes.day, '%H') == h, Bikes.week == 2, Stations.ID == Bikes.ID).group_by(Stations.name).all()

            for i in query_data:
                bike_data.append(
                    {'name': i[0], 'available_bike_stands': i[3], 'available_bikes': i[4], 'status': i[5],
                     'position': {'lat': i[1], 'lng': i[2]}})

            bike_current_json.append(bike_data)
        # print(bike_current_json)
    return jsonify(bike_current_json)


@app.route('/')
def new():
    respose = requests.get(app.config["SECRET_WEATHER_KEY"])
    weather_json = respose.json()
    respose.close()
    return render_template('new_index.html', weather_json=weather_json)
