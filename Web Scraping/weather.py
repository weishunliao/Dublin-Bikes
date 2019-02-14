# -*- coding: utf-8 -*-
import requests
import json
import time

get_url = 'http://api.openweathermap.org/data/2.5/weather?q=Dublin&units=metric&APPID=adfe6377cfc67c4eba8b0cf52ec30bbf'
response = requests.get(get_url)


def getWeather():
    getDataTime = time.strftime("(W)%Y_%m_%d_%H_%M_%S", time.localtime())
    weather = open('/home/ubuntu/scrape/weather_data/' +
                   getDataTime + '.json', 'w')
    json.dump(response.json(), weather)
    weather.close()


getWeather()
while True:
    getWeather()
    time.sleep(3600)
