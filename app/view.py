from app import app, db
from app.models import Stations, Bikes
from flask import render_template, request, jsonify
from sqlalchemy import func
import requests
import json
import time

stations_list = db.session.query(Stations.ID).all()
yesterday_json = {}
for i in stations_list:
    yesterday_json[i[0]] = [['Hour', 'Usages']]
yesterday = time.strftime("%Y-%m-%d", time.localtime(time.time() - 86400))
yesterday_data = db.session.query(Bikes.ID, func.date_format(Bikes.day, '%H'),
                                  func.sum(Bikes.available_bike_stands)). \
    filter(func.date_format(Bikes.day, '%Y-%m-%d') == yesterday).group_by(func.date_format(Bikes.day, '%H'),
                                                                          Bikes.ID).all()
for i in yesterday_data:
    yesterday_json[i[0]].append([int(i[1]), int(i[2])])

file1 = open("app/static/Cache/past24.json", "w")
json.dump(yesterday_json, file1)
file1.close()


@app.route('/')
def index():
    respose = requests.get(app.config["SECRET_WEATHER_KEY"])
    weather_json = respose.json()
    respose.close()
    file1 = open("app/static/Cache/past24.json", "r")
    past24 = json.load(file1)
    return render_template('new_index.html', map_key=app.config["SECRET_MAP_KEY"], weather_json=weather_json,
                           past24=past24)


@app.route('/update_map')
def search():
    t = request.args.get('t')
    if t == "current":
        respose = requests.get(
            'https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=31523d933c2ed2b25fd82ba42e3f0277eadf6184')
        bike_current_json = respose.json()
        respose.close()
    else:
        bike_current_json = []
        for h in range(24):
            bike_data = []
            query_data = db.session.query(Stations.name, Stations.p_latitude, Stations.p_longitude,
                                          Bikes.available_bikes,
                                          Bikes.available_bike_stands, Bikes.status). \
                filter(func.date_format(Bikes.day, '%H') == h, Bikes.week == 2, Stations.ID == Bikes.ID).group_by(
                Stations.name).all()

            for i in query_data:
                bike_data.append(
                    {'name': i[0], 'available_bike_stands': i[3], 'available_bikes': i[4], 'status': i[5],
                     'position': {'lat': i[1], 'lng': i[2]}})

            bike_current_json.append(bike_data)
        # print(bike_current_json)
    return jsonify(bike_current_json)
