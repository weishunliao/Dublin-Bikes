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
