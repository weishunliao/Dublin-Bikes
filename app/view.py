from app import app
from app.models import Station
from flask import render_template


@app.route('/')
def hello_world():
    stations = Station.query.all()
    return render_template('index.html', station_list=stations)
