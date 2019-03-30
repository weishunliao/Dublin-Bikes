from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

app = Flask(__name__, instance_relative_config=True)

# app.config.from_object('config.default')
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from app import view
myRds = mysql.connector.connect(
    host="dbbikes.coj48ycjuqgc.us-east-2.rds.amazonaws.com",
    user=app.config["MYSQL_CONNECT_USER"],
    passwd=app.config["MYSQL_CONNECT_PASSWORD"],
    database="dbbike"
)
# view.readDB()
# view.get_training_data(myRds)
# view.build_model()
