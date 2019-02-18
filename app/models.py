from app import db

class Station(db.Model):
    station_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), unique=True)
    address = db.Column(db.String(32))
    number = db.Column(db.Integer())
    latitude = db.Column(db.FLOAT())
    longitude = db.Column(db.FLOAT())

    def __init__(self, id, name, addr, num, latitude, longtitude):
        self.id = id
        self.name = name
        self.address = addr
        self.number = num
        self.latitude = latitude
        self.longitude = longtitude
