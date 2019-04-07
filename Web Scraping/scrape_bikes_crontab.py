import requests
import time
import json
import mysql.connector


get_url = 'https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=31523d933c2ed2b25fd82ba42e3f0277eadf6184'
response = requests.get(get_url)
response_json = response.json()
response.close()
getDataTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
dynamicData = open('/home/ubuntu/scrape/bikes_data/' +
                   getDataTime + '.json', 'w')
json.dump(response.json(), dynamicData)
dynamicData.close()

conn = mysql.connector.connect(
    host="dbbikes.coj48ycjuqgc.us-east-2.rds.amazonaws.com",
    user="LFL_DBBIKES",
    passwd="MYrds123",
    database="dbbike")
cursor = conn.cursor()

sql_query = '''INSERT INTO bikes(`id`,`last_update`,`day`,`week`,`available_bikes`,`available_bike_stands`,`status`) VALUES (%s, %s, %s, %s, %s, %s, %s)'''

for i in response_json:
    number = (i["number"])
    last_update = (i["last_update"])
    ltime = time.gmtime(last_update / 1000.0)
    day = time.strftime("%Y-%m-%d %H:%M:%S", ltime)
    week = ltime[6] + 1
    available_bikes = (i["available_bikes"])
    available_stands = (i["available_bike_stands"])
    status = (i["status"])
    try:
        cursor.execute(sql_query, (number, last_update, day, week,
                                   available_bikes, available_stands, status))
        conn.commit()
    except Exception as err:
        log = open('/home/ubuntu/scrape/log/db/' + getDataTime, 'w')
        log.write(str(err))
        conn.rollback()
        log.close()

conn.close()