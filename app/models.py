from app import db


class Stations(db.Model):
    ID = db.Column(db.Integer(), primary_key=True)
    address = db.Column(db.VARCHAR(255))
    p_latitude = db.Column(db.FLOAT())
    p_longitude = db.Column(db.FLOAT())
    banking = db.Column(db.VARCHAR(255))
    bonus = db.Column(db.VARCHAR(255))
    bike_stands = db.Column(db.Integer())

    def __init__(self, id, name, addrress, bonus, latitude, longtitude, bike_stands):
        self.id = id
        self.name = name
        self.address = addrress
        self.bonus = bonus
        self.p_latitude = latitude
        self.p_longitude = longtitude
        self.bike_stands = bike_stands
