# -*- coding: utf-8 -*-
import requests
import json
import time

get_url = 'https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=31523d933c2ed2b25fd82ba42e3f0277eadf6184'
response = requests.get(get_url)


def bikeDynamicData():
    getDataTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    dynamicData = open('/home/ubuntu/scrape/data/' +
                       getDataTime + '.json', 'w')
    json.dump(response.json(), dynamicData)
    dynamicData.close()


bikeDynamicData()
while True:
    bikeDynamicData()
    time.sleep(600)
