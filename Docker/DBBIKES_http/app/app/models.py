from app import db


class Stations(db.Model):
    ID = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.VARCHAR(255))
    address = db.Column(db.VARCHAR(255))
    p_latitude = db.Column(db.FLOAT())
    p_longitude = db.Column(db.FLOAT())
    banking = db.Column(db.VARCHAR(255))
    bonus = db.Column(db.VARCHAR(255))
    bike_stands = db.Column(db.Integer())

    def __init__(self, ID, name, address, bonus, latitude, longitude, bike_stands, banking):
        self.ID = ID
        self.name = name
        self.address = address
        self.bonus = bonus
        self.p_latitude = latitude
        self.p_longitude = longitude
        self.bike_stands = bike_stands
        self.banking = banking


class Bikes(db.Model):
    ID = db.Column(db.Integer(), primary_key=True)
    last_update = db.Column(db.BigInteger(), primary_key=True)
    day = db.Column(db.TIMESTAMP())
    week = db.Column(db.Integer())
    available_bikes = db.Column(db.Integer())
    available_bike_stands = db.Column(db.Integer())
    status = db.Column(db.VARCHAR(255))

    def __init__(self, ID, last_update, day, week, available_bikes, available_bike_stands, status):
        self.ID = ID
        self.last_update = last_update
        self.day = day
        self.week = week
        self.available_bikes = available_bikes
        self.available_bike_stands = available_bike_stands
        self.status = status


class Weather(db.Model):
    ID = db.Column(db.Integer(), primary_key=True)
    temp = db.Column(db.FLOAT())
    weather = db.Column(db.VARCHAR(255))
    w_description = db.Column(db.VARCHAR(255))
    visibility = db.Column(db.Integer())
    wind_speed = db.Column(db.Integer())
    datetime = db.Column(db.BigInteger())
    day = db.Column(db.TIMESTAMP())
    week = db.Column(db.Integer())

    def __init__(self, ID, temp, weather, w_description, visibility, wind_speed, datetime, day, week):
        self.ID = ID
        self.temp = temp
        self.weather = weather
        self.w_description = w_description
        self.visibility = visibility
        self.wind_speed = wind_speed
        self.datetime = datetime
        self.day = day
        self.week = week
