from app import app
from app.models import Stations
from flask import render_template
import requests
import json


@app.route('/')
def index():
    Stations_info = Stations.query.all()
    respose=requests.get(app.config["SECRET_WEATHER_KEY"])
    weather_json=respose.json()
    respose.close()
    return render_template('index.html', station_list=Stations_info, map_key=app.config["SECRET_MAP_KEY"], bike_api_key=app.config['SECRET_JCD_KEY'], weather_json=weather_json)
