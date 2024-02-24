from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

DATABASE = "./cows.sqlite3"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "cows.sqlite3")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable event system for performance
db = SQLAlchemy(app)


@app.route("/")
def hello_world():
    return "<p>Moo, World!</p>"

@app.route("/device_info", methods=["POST"])
def device_info(data):
    print("Data received:", data)
    return "OK"

class Cow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_reading_at = db.Column(db.DateTime, nullable=True)
    battery_plugged = db.Column(db.Boolean, nullable=True)
    battery_percent = db.Column(db.Integer, nullable=True)
    battery_remaining = db.Column(db.Integer, nullable=True)
    user = db.Column(db.String(100), nullable=True)
