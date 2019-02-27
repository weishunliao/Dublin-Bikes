#!coding:utf-8

import requests
import time
import json
import mysql.connector

while True:
    get_url = 'http://api.openweathermap.org/data/2.5/weather?q=Dublin&units=metric&APPID=adfe6377cfc67c4eba8b0cf52ec30bbf'
    response = requests.get(get_url)
    response_json = response.json()
    response.close()
    getDataTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    dynamicData = open('/home/ubuntu/scrape/weather_data/' +
                       getDataTime + '.json', 'w')
    json.dump(response.json(), dynamicData)
    dynamicData.close()

    conn = mysql.connector.connect(
        host="dbbikes.coj48ycjuqgc.us-east-2.rds.amazonaws.com",
        user="LFL_DBBIKES",
        passwd="MYrds123",
        database="dbbike")
    cursor = conn.cursor()

    sql_query = '''INSERT INTO weather(`temp`,`weather`,`w_description`,`visibility`,`wind_speed`,`wind_degree`,`datetime`) VALUES (%s, %s, %s, %s, %s, %s,%s)'''

    temp = response_json["main"]["temp"]
    weather = response_json["weather"][0]['main']
    description = response_json["weather"][0]["description"]
    visibility = response_json["visibility"]
    wind_speed = response_json["wind"]["speed"]
    wind_degree = response_json["wind"]["deg"]
    datetime = response_json["dt"]
    try:
        cursor.execute(sql_query, (temp, weather, description, visibility, wind_speed, wind_degree, datetime))
        conn.commit()
    except Exception as err:
        log = open('/home/ubuntu/scrape/log/db' + getDataTime, 'w')
        conn.rollback()
        log.close()

    conn.close()
    time.sleep(600)
