import os
import datetime

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

DATABASE = "./cows.sqlite3"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "cows.sqlite3"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
    False  # Disable event system for performance
)
db = SQLAlchemy(app)


@app.route("/")
def hello_world():
    return "<p>Moo, World!</p>"


# @app.route("/device_info", methods=["POST"])
# def device_info():
#     data = request.get_json()
#     print("Data received:", data)
#     return "OK"


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

    print(name, battery, plugged, percent, time_left, user)
    cow()

    # Find or create cow entry
    # cow = Cow.query.filter_by(name=name).first()
    # if cow is None:
    #     print("creating cow")
    #     cow = Cow(name=name)

    # # Update cow entry with latest data
    # cow.last_reading_at = datetime.fromtimestamp(data.get("timestamp"))
    # cow.battery_plugged = plugged
    # cow.battery_percent = percent
    # cow.battery_remaining = time_left
    # cow.user = user

    # Commit changes to the database
    # print("committing cow")
    # db.session.add(cow)
    # db.session.commit()

    return "OK"


class Cow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_reading_at = db.Column(db.DateTime, nullable=True)
    battery_plugged = db.Column(db.Boolean, nullable=True)
    battery_percent = db.Column(db.Integer, nullable=True)
    battery_remaining = db.Column(db.Integer, nullable=True)
    user = db.Column(db.String(100), nullable=True)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)


def cow():
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
