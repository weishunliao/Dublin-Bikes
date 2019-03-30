from app import db
from app.models import Stations, Bikes
import mysql.connector

myRds = mysql.connector.connect(
    host="dbbikes.coj48ycjuqgc.us-east-2.rds.amazonaws.com",
    user="LFL_DBBIKES",
    passwd="MYrds123",
    database="dbbike"
)

myCursor = myRds.cursor()
myCursor.execute("SELECT * FROM dbbike.stations")
myresult = myCursor.fetchall()

for x in myresult:
    print(x)
