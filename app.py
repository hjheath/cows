import datetime

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_folder="static")
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


@app.route("/")
def hello_world():
    return "Moo, World!"


@app.route("/cows")
def list_cows():
    cows = Cow.query.all()
    template = "cows.html"
    return render_template(template_name_or_list=template, cows=cows)


@app.route("/api/cows")
def api_list_cows():
    cows = Cow.query.all()
    return jsonify([cow.serialize() for cow in cows])


@app.route("/api/cows/<name>")
def api_get_cow_by_name(name):
    cow = Cow.query.filter_by(name=name).first()
    if cow:
        return jsonify(cow.serialize())
    else:
        return jsonify({"error": "Cow not found"}), 404


@app.route("/cows/<name>")
def get_cow_by_name(name):
    cow = Cow.query.filter_by(name=name).first()
    if cow:
        return jsonify(cow.serialize())
    else:
        return jsonify({"error": "Cow not found"}), 404


@app.route("/cows/<name>", methods=["PUT"])
def create_or_update_cow_by_name(name):
    data = request.get_json()

    cow = Cow.query.filter_by(name=name).first()
    new_record = False
    if not cow:
        print(f"{name} not found, creating new record")
        new_record = True
        cow = Cow(name=name)

    timestamp = data["timestamp"]
    battery_data = data["battery"]

    cow.last_reading_at = datetime.datetime.fromtimestamp(timestamp)
    cow.battery_plugged = battery_data["plugged"]
    cow.battery_percent = battery_data["percent"]
    cow.battery_remaining = battery_data["time_remaining"]
    cow.user = data["username"]

    db.session.add(cow)
    db.session.commit()

    status = 201 if new_record else 200
    return jsonify(cow.serialize()), status


class Cow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    last_reading_at = db.Column(db.DateTime)
    battery_plugged = db.Column(db.Boolean, nullable=True)
    battery_percent = db.Column(db.Integer, nullable=True)
    battery_remaining = db.Column(db.Integer, nullable=True)
    user = db.Column(db.String(100), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_reading_at": self.last_reading_at.isoformat(),
            "battery_plugged": self.battery_plugged,
            "battery_percent": self.battery_percent,
            "battery_remaining": self.battery_remaining,
            "user": self.user,
        }

    def __repr__(self):
        return "{} is the COW name and {} is my user".format(self.name, self.user)


with app.app_context():
    print(server_ascii_art())
    db.create_all()
