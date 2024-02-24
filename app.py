import os
import datetime

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cows.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


def server_ascii_art():
    return """
             __n__n__
      .------`-\00/-'
     /  ##  ## (oo)
    / \## __   ./
       |//YY \|/
       |||   |||
     Where's Bessie?
    """


@app.route("/hello_world")
def hello_world():
    return "Moo, World!"


@app.route("/")
def index():
    cows = Cow.query.all()
    print('index')
    print(cows)
    return "<p>Moo, World!</p>"


@app.route("/device_info", methods=["POST"])
def device_info():
    data = request.get_json()
    print("Data received:", data)

    # Extract data from JSON
    name = data.get("name")
    battery = data.get("battery", {})
    plugged = battery.get("plugged")
    percent = battery.get("percent")
    time_left = battery.get("time_left")
    user = data.get("user")

    current_cow = Cow.query.filter_by(name=name).first()

    if current_cow:
        print(f"{name} exists!")
        current_cow.name = name
        current_cow.battery_plugged = plugged
        current_cow.battery_percent = percent
        current_cow.battery_remaining = time_left
        current_cow.user = user
        db.session.commit()
        print(server_ascii_art())
        return f"Updated {name}"

    cow = Cow(
        name=name,
        battery_plugged=plugged,
        battery_percent=percent,
        battery_remaining=time_left,
        user=user,
    )
    print(f"saving {name}")
    db.session.add(cow)
    db.session.commit()

    return "OK"


class Cow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    last_reading_at = db.Column(db.DateTime, default=datetime.datetime.now())
    battery_plugged = db.Column(db.Boolean, nullable=True)
    battery_percent = db.Column(db.Integer, nullable=True)
    battery_remaining = db.Column(db.Integer, nullable=True)
    user = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return "{} is the COW name and {} is my user".format(self.name, self.user)


with app.app_context():
    print(server_ascii_art())
    db.create_all()
