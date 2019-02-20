from app import app
from app.models import Stations
from flask import render_template


@app.route('/')
def hello_world():
    Stations_info = Stations.query.all()
    return render_template('index.html', station_list=Stations_info, map_key=app.config["SECRET_MAP_KEY"])
