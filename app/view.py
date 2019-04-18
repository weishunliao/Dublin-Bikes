from app import app, db
from app.models import Stations, Bikes
from flask import render_template, request, jsonify
from sqlalchemy import func
import requests
import json
import time
import pandas as pd
import pickle
import numpy as np
import csv
from sklearn.ensemble import RandomForestRegressor
import smtplib

response = requests.get(app.config["SECRET_WEATHER_KEY2"])
weather_forecast = response.json()
response.close()

response = requests.get(
    'https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=31523d933c2ed2b25fd82ba42e3f0277eadf6184')
bike_current = response.json()
response.close()

pickleFile_bikes = open('app/static/cache/model_available_bike.pickle', 'rb')
rg1 = pickle.load(pickleFile_bikes)
pickleFile_stand = open('app/static/cache/model_available_bike_stands.pickle', 'rb')
rg2 = pickle.load(pickleFile_stand)


@app.route('/')
def index():
    response = requests.get(app.config["SECRET_WEATHER_KEY"])
    weather_current = response.json()
    response.close()
    file1 = open("app/static/cache/past24.json", "r")
    past24 = json.load(file1)
    file1.close()
    # response = requests.get(app.config["SECRET_WEATHER_KEY2"])
    # weather_forecast = response.json()
    # response.close()
    return render_template('new_index.html', map_key=app.config["SECRET_MAP_KEY"], weather_current=weather_current,
                           past24=past24, weather_forecast=weather_forecast)


@app.route('/update_map')
def search():
    t = request.args.get('t')
    if t == "current":
        bike_json = bike_current
    else:
        bike_json = []
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

            bike_json.append(bike_data)
    return jsonify(bike_json)


@app.route('/get_prediction')
def get_prediction():
    stationID = request.args.get('id')
    past_available_bike = request.args.get('past_available_bike')
    past_available_bike_stands = request.args.get('past_available_bike_stands')

    hour = int(time.strftime("%H", time.localtime())) + 2
    week = int(time.strftime("%w", time.localtime())) + 1
    get_url = "http://api.openweathermap.org/data/2.5/forecast?q=Dublin&units=metric&APPID=adfe6377cfc67c4eba8b0cf52ec30bbf"
    response = requests.get(get_url)
    temp = response.json()['list'][1]['main']['temp']
    weather = response.json()['list'][1]['weather'][0]['main']
    if weather in ['Rain', 'Drizzle', 'Snow']:
        weather = 1
    else:
        weather = 0
    response.close()
    res = []
    predictions1 = rg1.predict(np.array([[stationID, hour, week, temp, weather, past_available_bike]]))
    res.append(int(predictions1))

    predictions2 = rg2.predict(np.array([[stationID, hour, week, temp, weather, past_available_bike_stands]]))
    res.append(int(predictions2))
    return jsonify(res)


@app.route('/predict_occupancy')
def occupancy_map():
    res = []
    for i in range(13):
        tempList = []
        for j in bike_current:
            hour = int(time.strftime("%H", time.localtime()))
            week = int(time.strftime("%w", time.localtime())) + 1
            temp = weather_forecast['list'][i // 3]['main']['temp']
            weather = weather_forecast['list'][i // 3]['weather'][0]['main']
            if weather in ['Rain', 'Drizzle', 'Snow']:
                weather = 1
            else:
                weather = 0
            predictions1 = rg1.predict(np.array([[j['number'], hour + i, week, temp, weather, j['available_bikes']]]))
            predictions2 = rg2.predict(np.array([[j['number'], hour, week, temp, weather, j['available_bike_stands']]]))

            tempList.append(
                {'name': j['name'], 'available_bike_stands': int(predictions2), 'available_bikes': int(predictions1),
                 'status': 'OPEN',
                 'position': j['position']})
        res.append(tempList)
    return jsonify(res)


@app.route('/send_email')
def send_email():
    user_address = request.args.get('email')
    msg = request.args.get('message')
    name = request.args.get('name')
    msg += "  From " + name
    gmail_user = "dbbikes2019@gmail.com"
    gmail_password = "@dbbikes2019dbbikes2019"
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(gmail_user, gmail_password)
    server.sendmail(
        user_address,
        "jingyuan.feng@ucdconnect.ie",
        msg)
    server.quit()
    return render_template("submit.html")


def get_past24():
    stations_list = db.session.query(Stations.ID).all()
    yesterday_json = {}
    for i in stations_list:
        yesterday_json[i[0]] = [['Hour', 'Usages']]
    yesterday = time.strftime("%Y-%m-%d", time.localtime(time.time() - 86400))
    yesterday_data = db.session.query(Bikes.ID, func.date_format(Bikes.day, '%H'),
                                      func.sum(Bikes.available_bikes)). \
        filter(func.date_format(Bikes.day, '%Y-%m-%d') == yesterday).group_by(func.date_format(Bikes.day, '%H'),
                                                                              Bikes.ID).all()
    for i in yesterday_data:
        yesterday_json[i[0]].append([int(i[1]), int(i[2])])

    file1 = open("app/static/cache/past24.json", "w")
    json.dump(yesterday_json, file1)
    file1.close()


def get_training_data_available_bike_stand(myRds):
    myCursor = myRds.cursor()
    query = "SELECT table1.available_bike_stands, table1.id ,table1.h, table2.`week`, table3.past_available_bike_stands, table2.total_available_bike_stands, weather.temp, weather.weather,weather.wind_speed " \
            "FROM (SELECT id, DATE(`day`)as d,HOUR(`day`) as h, SUM(available_bike_stands)/6 as available_bike_stands FROM dbbike.bikes " \
            "WHERE last_update>=1551139651000 AND last_update <= 1553644391000 " \
            "GROUP BY id,DAY(`day`),HOUR(`day`)) as table1," \
            "(SELECT DATE(`day`) as d,HOUR(`day`) as h, `week`,sum(available_bikes)/6 as " \
            "total_available_bike_stands FROM dbbike.bikes WHERE" \
            " last_update>=1550707610000 and last_update<=1553212355000 GROUP BY DATE(`day`),HOUR(`day`)) as table2," \
            "(SELECT weather.temp, weather.weather,weather.visibility,weather.wind_speed,date(`day`) as d,HOUR(`day`) as h FROM weather " \
            "WHERE datetime>=1550707610 and datetime <= 1553212355) as weather," \
            "(SELECT id, DATE(`day`)as d,HOUR(`day`) +1 as h, SUM(available_bike_stands)/6 as past_available_bike_stands FROM dbbike.bikes " \
            "WHERE last_update>=1551139651000 AND last_update <= 1553644391000 " \
            "GROUP BY id,DAY(`day`),HOUR(`day`)) as table3 " \
            "WHERE table1.h=table2.h and table1.d=table2.d and table1.h=weather.h and " \
            "table1.d=weather.d and table1.h=table3.h and table1.d=table3.d and table1.id=table3.id"

    myCursor.execute(query)
    myresult = myCursor.fetchall()
    training_data = [
        ["Available_bike_stands", "StationID", "Hour", "Weekday", "past_available_bike_stands",
         "Total_Available_bike_stands", "Temp",
         "Weather(Rain)",
         "Wind_Speed"]]

    for i in myresult:
        sublist = []
        sublist.append(float(i[0]))
        sublist.append(int(i[1]))
        sublist.append(int(i[2]))
        sublist.append(int(i[3]))
        sublist.append(float(i[4]))
        sublist.append(float(i[5]))
        sublist.append(float(i[6]))
        if i[7] in ['Rain', 'Drizzle', 'Snow']:
            sublist.append(1)
        else:
            sublist.append(0)
        sublist.append(float(i[8]))
        training_data.append(sublist)
    myCursor.close()
    csvFile = open('app/static/cache/training_available_bike_stands.csv', 'w')
    writer = csv.writer(csvFile)
    for i in training_data:
        writer.writerow(i)
    csvFile.close()


def get_training_data_available_bike(myRds):
    myCursor = myRds.cursor()
    query = "SELECT table1.available_bike, table1.id ,table1.h, table2.`week`, table3.past_available_bike, table2.total_available_bike, weather.temp, weather.weather,weather.wind_speed " \
            "FROM (SELECT id, DATE(`day`)as d,HOUR(`day`) as h, SUM(available_bikes)/6 as available_bike FROM dbbike.bikes " \
            "WHERE last_update>=1551139651000 AND last_update <= 1553644391000 " \
            "GROUP BY id,DAY(`day`),HOUR(`day`)) as table1, " \
            "(SELECT DATE(`day`) as d,HOUR(`day`) as h, `week`,sum(available_bikes)/6 as total_available_bike FROM dbbike.bikes " \
            "WHERE last_update>=1550707610000 and last_update<=1553212355000 " \
            "GROUP BY DATE(`day`),HOUR(`day`)) as table2," \
            "(SELECT weather.temp, weather.weather,weather.visibility,weather.wind_speed,date(`day`) as d,HOUR(`day`) as h FROM weather " \
            "WHERE datetime>=1550707610 and datetime <= 1553212355) as weather," \
            "(SELECT id, DATE(`day`)as d,HOUR(`day`) + 2 as h, SUM(available_bikes)/6 as past_available_bike FROM dbbike.bikes " \
            "WHERE last_update>=1551139651000 AND last_update <= 1553644391000 " \
            "GROUP BY id,DAY(`day`),HOUR(`day`)) as table3 WHERE table1.h=table2.h and table1.d=table2.d and " \
            "table1.h=weather.h and table1.d=weather.d and table1.h=table3.h and table1.d=table3.d and table1.id=table3.id"

    myCursor.execute(query)
    myresult = myCursor.fetchall()
    training_data = [
        ["Available_bike", "StationID", "Hour", "Weekday", "past_available_bike", "Total_Available_Bikes", "Temp",
         "Weather(Rain)",
         "Wind_Speed"]]

    for i in myresult:
        sublist = []
        sublist.append(float(i[0]))
        sublist.append(int(i[1]))
        sublist.append(int(i[2]))
        sublist.append(int(i[3]))
        sublist.append(float(i[4]))
        sublist.append(float(i[5]))
        sublist.append(float(i[6]))
        if i[7] in ['Rain', 'Drizzle', 'Snow']:
            sublist.append(1)
        else:
            sublist.append(0)
        sublist.append(float(i[8]))
        training_data.append(sublist)
    myCursor.close()
    csvFile = open('app/static/cache/training_available_bike.csv', 'w')
    writer = csv.writer(csvFile)
    for i in training_data:
        writer.writerow(i)
    csvFile.close()


def build_model_available_bike():
    df = pd.read_csv("app/static/cache/training_available_bike.csv")
    cont_features = ['StationID', 'Hour', 'Weekday', 'Temp', 'Weather(Rain)', 'past_available_bike']
    X_1 = df[cont_features]
    Y_1 = df.Available_bike
    regr = RandomForestRegressor(max_depth=10, random_state=2, n_estimators=100)

    regr.fit(X_1, Y_1)
    RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=2,
                          max_features='auto', max_leaf_nodes=None,
                          min_impurity_decrease=0.0, min_impurity_split=None,
                          min_samples_leaf=1, min_samples_split=2,
                          min_weight_fraction_leaf=0.0, n_estimators=100, n_jobs=None,
                          oob_score=False, random_state=0, verbose=0, warm_start=False)

    pickleFile = open('app/static/cache/model_available_bike.pickle', 'wb')
    pickle.dump(regr, pickleFile)
    pickleFile.close()


def build_model_available_bike_stand():
    df = pd.read_csv("app/static/cache/training_available_bike_stands.csv")
    cont_features = ['StationID', 'Hour', 'Weekday', 'Temp', 'Weather(Rain)', 'past_available_bike_stands']
    X_1 = df[cont_features]
    Y_1 = df.Available_bike_stands
    regr = RandomForestRegressor(max_depth=10, random_state=2, n_estimators=100)

    regr.fit(X_1, Y_1)
    RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=2,
                          max_features='auto', max_leaf_nodes=None,
                          min_impurity_decrease=0.0, min_impurity_split=None,
                          min_samples_leaf=1, min_samples_split=2,
                          min_weight_fraction_leaf=0.0, n_estimators=100, n_jobs=None,
                          oob_score=False, random_state=0, verbose=0, warm_start=False)

    pickleFile = open('app/static/cache/model_available_bike_stands.pickle', 'wb')
    pickle.dump(regr, pickleFile)
    pickleFile.close()
