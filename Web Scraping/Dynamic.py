#!coding:utf-8


import json

import mysql.connector



# connect to database
conn = mysql.connector.connect(
  host="dbbikes.coj48ycjuqgc.us-east-2.rds.amazonaws.com",
  user="LFL_DBBIKES",
  passwd="MYrds123",
  database="dbbike")

# create cursor object
cursor = conn.cursor()



# read files
static_data = open('/Users/jingyuan/Desktop/2019_02_13_11_17_17.json', 'r')


# load json file
all_data = json.load(static_data)

# print(all_data)

# read and store into db
for i in all_data:

    number = (i["number"])
    last_update = (i["last_update"])
    available_bikes = (i["available_bikes"])
    available_stands = (i["available_bike_stands"])

    sql_query = '''INSERT INTO Dynamic(`number`,`last_update`,`available_bikes`,`available_bike_stands`) VALUES (%s, %s, %s, %s)'''
    try:
        cursor.execute(sql_query, (number, last_update,  available_bikes, available_stands))
        conn.commit()
    except Exception as err:
        print(err)
        conn.rollback()

conn.close()