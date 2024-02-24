import os
import datetime

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "cows.sqlite3"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
    False  # Disable event system for performance
)
session_options = {"autocommit": False, "autoflush": False}
db = SQLAlchemy(app, session_options=session_options)

from app import app


def where_is_bessie():
    cow = """
             __n__n__
      .------`-\00/-'
     /  ##  ## (oo)
    / \## __   ./
       |//YY \|/
       |||   |||
     Where's Bessie?
    """
    print(cow)


@app.route("/")
def all_cows():
    cows = Cow.query.all()
    print(cows)
    return "<p>Moo, World!</p>"
    # return "OK"


@app.route("/device_info", methods=["POST"])
def device_info():
    data = request.get_json()
    print("Data received:", data)

    # Extract data from JSON
    cow_uuid = data.get("cow_uuid")
    name = data.get("name")
    battery = data.get("battery", {})
    plugged = battery.get("plugged")
    percent = battery.get("percent")
    time_left = battery.get("time_left")
    user = data.get("user")

    current_cow = Cow.query.filter_by(cow_uuid=cow_uuid).first()

    if current_cow:
        print(f"{name} exists!")
        current_cow.name = name
        current_cow.battery_plugged = plugged
        current_cow.battery_percent = percent
        current_cow.battery_remaining = time_left
        current_cow.cow_uuid = cow_uuid
        current_cow.user = user
        db.session.commit()
        where_is_bessie()
        return f"Updated {name}"

    cow = Cow(
        name=name,
        cow_uuid=cow_uuid,
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
    cow_uuid = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    last_reading_at = db.Column(db.DateTime, default=datetime.datetime.now())
    battery_plugged = db.Column(db.Boolean, nullable=True)
    battery_percent = db.Column(db.Integer, nullable=True)
    battery_remaining = db.Column(db.Integer, nullable=True)
    user = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return "{} is the COW name and {} is my user".format(self.name, self.user)


with app.app_context():
    where_is_bessie()
    db.create_all()
