#!/usr/local/bin/python3


import MySQLdb
import json

# connect to database
conn = MySQLdb.connect("localhost", "root", "", "flaskDb")

# create cursoe object
cursor = conn.cursor()

# create table
cursor.execute('''CREATE TABLE Station (
station_id  int UNSIGNED AUTO_INCREMENT,
name		varchar(128),
address     text,
latitude    float,
longitude	float,
number      int(200)
PRIMARY KEY(station_id)
)DEFAULT CHARSET=utf8;''')


# read files
static_data = open('Dublin_Bike_Station.json', 'r')

# load json file
all_data = json.load(static_data)

# read and store into db
for i in all_data:
    name = i["name"]
    address = i["address"]
    latitude = float(i["latitude"])
    longitude = float(i["longitude"])
    number = int(i["number"])

    sql_query = '''INSERT INTO Station(`name`,`address`,`latitude`,`longitude`,`number`) VALUES (%s, %s, %s, %s, %s )'''
    try:
        cursor.execute(sql_query, (name, address, latitude, longitude, number))
        conn.commit()
    except Exception as err:
        conn.rollback()

conn.close()
